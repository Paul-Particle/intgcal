import pytest
from task_parser import parse_tasks

def test_normal_task_parsing(sample_tasks()):
    # Extract only normal tasks from sample_tasks
    normal_tasks = [task for i, task in sample_tasks if i < 38]

    # Call the parser function
    parsed_tasks = parse_tasks(normal_tasks)

    # Assertions to check if the parsing is as expected
    assert parsed_tasks == expected_output

@pytest.mark.parametrize("task_input, expected_output", [
    ("1) Example task [30]", [('1', 'Example task', 30)]),
    # Add more test cases as needed
])
def test_various_task_formats(task_input, expected_output):
    assert parse_tasks([task_input]) == expected_output
