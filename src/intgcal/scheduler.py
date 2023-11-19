from datetime import datetime, timedelta

def calculate_next_quarter_hour():
    now = datetime.now()
    return (now + timedelta(minutes=(15 - now.minute % 15))).replace(second=0, microsecond=0)

def schedule_tasks(tasks, start_time, time_limit):
    scheduled_tasks = []
    current_date = datetime.now().date()
    time_limit = datetime.combine(current_date, time_limit)
    #time_slot_start = datetime.combine(current_date, start_time)
    time_slot_start = start_time
    cumulative_short_duration = 0

    for calendar_key, task_description, duration in tasks:
        # Handle short tasks for gap calculation
        if duration < 15:
            cumulative_short_duration += duration
            # Align the next task to the nearest quarter hour if cumulative duration reaches 15 minutes
            if cumulative_short_duration >= 15:
                cumulative_short_duration = cumulative_short_duration % 15  # Keep the remainder
                time_slot_start = (time_slot_start + timedelta(minutes=15)).replace(second=0, microsecond=0)

        else:
            time_slot_end = time_slot_start + timedelta(minutes=duration)
            if time_slot_end > time_limit:
                # Adjust start time for overlapping tasks
                time_slot_start = time_limit - timedelta(minutes=duration)
                time_slot_end = time_limit

            scheduled_tasks.append((calendar_key, task_description, duration, time_slot_start, time_slot_end))
            time_slot_start = time_slot_end  # Update start time for the next task

    # Add buffer event if there's remaining time
    if time_slot_start < time_limit:
        buffer_end_time = datetime.combine(current_date, time_limit)
        scheduled_tasks.append(
            ("&", "Buffer", 
             (buffer_end_time - time_slot_start).seconds // 60, time_slot_start, buffer_end_time)
        )

    return scheduled_tasks
