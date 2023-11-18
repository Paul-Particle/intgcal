import pytest
from task_parser import parse_tasks

# sample_tasks is a setup function 
def test_normal_task_parsing(sample_tasks):
    pass

@pytest.mark.parametrize("task_input, expected_output", [
    ("1) Example task [30]", [('1', 'Example task', 30)]),
    # Add more test cases as needed
])
def test_various_task_formats(task_input, expected_output):
    assert parse_tasks([task_input]) == expected_output
