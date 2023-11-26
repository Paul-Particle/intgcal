import re
import math
from collections import namedtuple


Task = namedtuple('Task', ['calendar_key', 'description', 'duration'])

MAX_DURATION_HOURS = 18
WARNING_DURATION_HOURS = 12
NOTICE_DURATION_HOURS = 8


def compile_regex():
    calendar_prefix = r'[0-9\~\&\<\>\?]'
    additional_prefix_info = r'.{0,5}'  # a few extra prefixes and ','
    task_description = r'[^\[]+'        # anything not a '['
    trailing_parentheses = r'\){1,4}'   # intend's notation for "NotDones"

    task_regex = re.compile(rf"""
        ^                               # Start of the line
        (                               # Capturing group for the whole prefix
            \(?                         # Optional opening parenthesis '('
            {calendar_prefix}           # Calendar prefix
        )                               # End of the prefix capturing group
        {additional_prefix_info}        # Additional prefix info
        {trailing_parentheses}          # Trailing parentheses ')'
        \s*                             # Optional whitespace
        ({task_description})            # Capturing group for the task description
        \[([0-9]+)\]                    # Capturing group for the duration '[60]'
    """, re.VERBOSE)
    return task_regex


def parse_line(line, task_regex):
   match = task_regex.match(line)
   if match:
       # Handle '(X)' and 'X)' cases. 
       calendar_key = match.group(1)
       task_description = match.group(2).strip()

       duration = int(match.group(3))
        duration = math.ceil(duration / 5) * 5

       return Task(calendar_key, task_description, duration)


def print_info(tasks, total_duration):
    print(
        f'Parsed {len(tasks)} tasks.',
        f'Expected duration: {total_duration // 60} h {total_duration % 60} min'
    )
    if total_duration > 60 * MAX_DURATION_HOURS:
        print('ABORT: Total duration > 18 h !')
        return
    elif total_duration > 60 * WARNING_DURATION_HOURS:
        print('DANGER: Unsustainable workload!')
    elif total_duration > 60 * NOTICE_DURATION_HOURS:
        print('WARNING: Significant workload')


def parse_tasks(task_list):
    task_regex = compile_regex()
    tasks = []
    total_duration = 0

    for line in task_list:
        if line.startswith(('-', '+', '\n')):
            continue
        Task = parse_line(line, task_regex)
        if Task:
            tasks.append(Task)
            total_duration += Task.duration
        else:
            print(f'Warning: Ignored malformed task line: "{line}"')

    print_info(tasks, total_duration)

    return tasks
