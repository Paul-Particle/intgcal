from datetime import datetime, timedelta

def calculate_next_quarter_hour():
    now = datetime.datetime.now()
    return (now + datetime.timedelta(minutes=(15 - now.minute % 15))).replace(second=0, microsecond=0)

def schedule_tasks(tasks, start_time, time_limit):
    scheduled_tasks = []
    # next time slot for scheduling
    time_slot_start = start_time
    cumulative_short_duration = 0

    for calendar_key, task_description, duration in tasks:
        # Handle short tasks for gap calculation
        if duration < 15:
            cumulative_short_duration += duration
            if cumulative_short_duration >= 15:
                # Add a gap and reset the counter
                time_slot_start += timedelta(minutes=15)
                cumulative_short_duration -= 15
            continue

        # Check if adding the current task exceeds the time limit
        if time_slot_start + timedelta(minutes=duration) > datetime.combine(datetime.today(), time_limit):
            # Adjust task end time to the time limit 
            time_slot_end = datetime.combine(datetime.today(), time_limit)
            scheduled_tasks.append(
                    (calendar_key, task_description, duration, time_slot_start, time_slot_end)
                )
            # schedule tasks overlapping from this point onwards
            continue

        # Schedule normal tasks
        time_slot_end = time_slot_start + timedelta(minutes=duration)
        scheduled_tasks.append((calendar_key, task_description, duration, time_slot_start, time_slot_end))
        
        # Update current time for the next task
        time_slot_start = time_slot_end

    # Add buffer event if there's remaining time
    if time_slot_start.time() < time_limit:
        buffer_end_time = datetime.combine(datetime.today(), time_limit)
        scheduled_tasks.append(
                (
                    "&", "Buffer Time", 
                    (buffer_end_time - time_slot_start).seconds // 60, 
                    time_slot_start, buffer_end_time
                )
            )

    return scheduled_tasks

# Example usage
time_limit = datetime.now().replace(hour=23, minute=0, second=0, microsecond=0).time()
start_time = calculate_next_quarter_hour()

scheduled_tasks = schedule_tasks(parsed_tasks, start_time, time_limit)
