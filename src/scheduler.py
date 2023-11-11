# Scheduler module

from datetime import datetime, timedelta

def schedule_tasks(tasks, start_time, time_limit):
    scheduled_tasks = []
    current_time = start_time

    for calendar_key, task_description, duration in tasks:
        # Skip tasks less than 15 minutes but count them for gap calculation
        if duration < 15:
            continue

        # Add a task
        end_time = current_time + timedelta(minutes=duration)
        scheduled_tasks.append((calendar_key, task_description, duration, current_time, end_time))
        
        # Update current time for the next task
        current_time = end_time

        # Check if total time exceeds the limit
        if current_time.time() > time_limit:
            # Logic to handle overlapping tasks
            break

    # Logic for buffer event if needed
    # ...

    return scheduled_tasks

# Example usage
time_limit = datetime.now().replace(hour=23, minute=0, second=0, microsecond=0).time()
start_time = calculate_next_quarter_hour()  # This function needs to be implemented

scheduled_tasks = schedule_tasks(parsed_tasks, start_time, time_limit)
