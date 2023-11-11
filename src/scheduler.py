from datetime import datetime, timedelta

def schedule_tasks(tasks, start_time, time_limit):
    scheduled_tasks = []
    current_time = start_time
    cumulative_short_duration = 0

    for calendar_key, task_description, duration in tasks:
        # Handle short tasks for gap calculation
        if duration < 15:
            cumulative_short_duration += duration
            if cumulative_short_duration >= 15:
                # Add a gap and reset the counter
                current_time += timedelta(minutes=15)
                cumulative_short_duration -= 15
            continue

        # Check if adding the current task exceeds the time limit
        if current_time + timedelta(minutes=duration) > datetime.combine(datetime.today(), time_limit):
            # Adjust end time to the time limit and schedule overlapping tasks
            end_time = datetime.combine(datetime.today(), time_limit)
            scheduled_tasks.append((calendar_key, task_description, duration, current_time, end_time))
            continue

        # Schedule normal tasks
        end_time = current_time + timedelta(minutes=duration)
        scheduled_tasks.append((calendar_key, task_description, duration, current_time, end_time))
        
        # Update current time for the next task
        current_time = end_time

    # Add buffer event if there's remaining time
    if current_time.time() < time_limit:
        buffer_end_time = datetime.combine(datetime.today(), time_limit)
        scheduled_tasks.append(("buffer", "Buffer Time", (buffer_end_time - current_time).seconds // 60, current_time, buffer_end_time))

    return scheduled_tasks

# Example usage
time_limit = datetime.now().replace(hour=23, minute=0, second=0, microsecond=0).time()
start_time = calculate_next_quarter_hour()  # This function needs to be implemented

scheduled_tasks = schedule_tasks(parsed_tasks, start_time, time_limit)
