# scheduler.py
from datetime import datetime, timedelta

def calculate_next_quarter_hour(input_time=None):
    if input_time is None:
        input_time = datetime.now()
    elif not isinstance(input_time, datetime):
        raise ValueError("input_time must be datetime")

    remaining_minutes = timedelta(minutes=(15 - input_time.minute % 15))
    next_quarter = (input_time + remaining_minutes)
    return next_quarter.replace(second=0, microsecond=0)


def add_date(start_time, end_time):
    now = datetime.now()
    current_time = now.time()
    current_date = now.date()

    start_time = datetime.combine(current_date, start_time)
    start_time = calculate_next_quarter_hour(start_time)
    if current_time > start_time.time():
        start_time = start_time + timedelta(days=1)

    end_time = datetime.combine(start_time.date(), end_time)

    return start_time, end_time


def get_previous_duration(scheduled_tasks):
    *_, start_time, end_time = scheduled_tasks[-1]
    duration = end_time - start_time
    return duration.minute


def schedule_tasks(tasks, start_time, end_time):

    start_time, end_time = add_date(start_time, end_time)

    time_slot_start = start_time
    cumulative_short_duration = 0
    scheduled_tasks = []

    for calendar_key, task_description, duration in tasks:
        
        if duration > 15:
            cumulative_short_duration = 0

        elif cumulative_short_duration + duration <= 15:
            # Schedule short tasks as overlapping 15 min events
            cumulative_short_duration += duration
            duration = 15
            time_slot_start -= timedelta(minutes=15)

        time_slot_end = time_slot_start + timedelta(minutes=duration)

        if time_slot_end > end_time:
            # If there are too many tasks, schedule them 'bunched up'
            time_slot_start = end_time - timedelta(minutes=duration)
            time_slot_end = end_time

        task = (calendar_key, task_description, duration,
                time_slot_start, time_slot_end)
        scheduled_tasks.append(task)

        if time_slot_end.minute % 15 > 0:
            time_slot_end = calculate_next_quarter_hour(time_slot_end)

        time_slot_start = time_slot_end  # Update start time for the next task

    return scheduled_tasks
