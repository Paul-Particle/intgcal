# scheduler.py
from datetime import datetime, timedelta

SHORT_DURATION = 15

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

    start_time = datetime.combine(now.date(), start_time)
    start_time = calculate_next_quarter_hour(start_time)

    # Schedule for next day
    if now > start_time:
        start_time = start_time + timedelta(days=1)

    end_time = datetime.combine(start_time.date(), end_time)

    return start_time, end_time


def schedule_tasks(tasks, start_time, end_time):

    start_time, end_time = add_date(start_time, end_time)

    time_slot_start = start_time

    batched_duration = 0
    scheduled_tasks = []

    for Task in tasks:
        calendar_key, description, duration = Task

        # Schedule short tasks as overlapping 15 min events
        is_batchable = batched_duration + duration <= SHORT_DURATION
        is_short = duration <= SHORT_DURATION
        if is_batchable:
            time_slot_start -= timedelta(minutes=SHORT_DURATION)
            batched_duration += duration
            duration = SHORT_DURATION
        elif is_short:
            duration = SHORT_DURATION
            batched_duration = 0
        else:
            batched_duration = 0

        # Schedule task end time
        time_slot_end = time_slot_start + timedelta(minutes=duration)

        # If total duration is too long, schedule remaining tasks overlapping
        is_over_time_limit = time_slot_end > end_time
        if is_over_time_limit:
            time_slot_end = end_time
            time_slot_start = end_time - timedelta(minutes=duration)

        # Save task
        task = (calendar_key, description, duration,
                time_slot_start, time_slot_end)
        scheduled_tasks.append(task)

        # Update start time for the next task
        if time_slot_end.minute % SHORT_DURATION > 0:
            time_slot_end = calculate_next_quarter_hour(time_slot_end)
        time_slot_start = time_slot_end

    return scheduled_tasks
