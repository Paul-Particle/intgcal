import pytest
from datetime import datetime, timedelta
from scheduler import schedule_tasks, calculate_next_quarter_hour

def test_simple_scheduling():
    tasks = [("1", "Task 1", 30), ("2", "Task 2", 45)]
    start_time = calculate_next_quarter_hour().time()
    time_limit = datetime.now().replace(hour=23, minute=0, second=0, microsecond=0).time()

    scheduled_tasks = schedule_tasks(tasks, start_time, time_limit)

    assert len(scheduled_tasks) == len(tasks) + 1 # 2 from list, +1 for buffer
    # additional tests omitted

def test_short_tasks():
    # Test scheduling of short tasks
    pass
