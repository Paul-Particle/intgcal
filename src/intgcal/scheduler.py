# scheduler.py
from datetime import datetime, timedelta


def calculate_next_quarter_hour(input_time=None):
    # Validate input or default to current time
    if input_time is None:
        input_time = datetime.now()
    elif not isinstance(input_time, datetime):
        raise ValueError("input_time must be datetime")

    # Calculate the next quarter hour
    next_quarter = (input_time + timedelta(minutes=(15 - input_time.minute % 15)))
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

def schedule_tasks(tasks, start_time, end_time):

    start_time, end_time = add_date(start_time, end_time)

    time_slot_start = start_time

    cumulative_short_duration = 0
    scheduled_tasks = []

    for calendar_key, task_description, duration in tasks:
        # Handle short tasks for gap calculation
        if duration < 15:
            cumulative_short_duration += duration
            # Align the next task to the nearest quarter hour 
        if cumulative_short_duration >= 15:
            # Keep the remainder
            cumulative_short_duration = cumulative_short_duration % 15
            time_slot_start = (time_slot_start + timedelta(minutes=15)).replace(second=0, microsecond=0)
        continue

        time_slot_end = time_slot_start + timedelta(minutes=duration)
        if time_slot_end > end_time:
            # Adjust start time to get overlapping tasks at end of day
            time_slot_start = end_time - timedelta(minutes=duration)
            time_slot_end = end_time

        scheduled_tasks.append(
            (
                calendar_key, task_description, duration,
                time_slot_start, time_slot_end
            )
        )

        time_slot_start = time_slot_end  # Update start time for the next task

    # Add buffer event if there's remaining time
    if time_slot_start < end_time:
        buffer_end_time = end_time
#        scheduled_tasks.append(
#            ("&", "Buffer", 
#             (buffer_end_time - time_slot_start).seconds // 60, time_slot_start, buffer_end_time)
#        )

    return scheduled_tasks
