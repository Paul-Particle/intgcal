import re
import math
from collections import namedtuple


Task = namedtuple('Task', ['calendar_key', 'full_prefix', 'description', 'duration'])

MAX_DURATION_HOURS = 18

def compile_regex():
    # Regex to capture tasks like '2,3)) Do the thing [60]'
    calendar_key_prefix = r'[0-9\~\&\<\>\?]'    # task category e.g. '2)' (determines calendar)
    additional_prefix_info = r'.{0,5}'      # extra task categories, separated by ',' e.g. '2,3)'
    trailing_parentheses = r'\){1,4}'       # intend's notation for "NotDones"
    task_description = r'[^\[]+'            # anything not a '['

    task_regex = re.compile(rf"""
        ^                                   # Start of the line
        (                                   # Start capture groups 1 for full prefix
            \(?                             # Optional opening parenthesis '('
            ({calendar_key_prefix})         # Capture group 2 for calendar determining prefix
            {additional_prefix_info}        # Secondary task categories
            {trailing_parentheses}          # Intend's notation for "NotDones"
        )                                   # End of capturing group 1
        \s*                                 # Optional whitespace
        ({task_description})                # Capturing group 2 for the task description
        \[([0-9]+)\]                        # Capturing group 3 for the duration '[60]'
    """, re.VERBOSE)
    return task_regex


def parse_line(line, task_regex):
   match = task_regex.match(line)
   if match:
       full_prefix = match.group(1)
       calendar_key = match.group(2)
       description = match.group(3).strip()
       duration = int(match.group(4))
       duration = math.ceil(duration / 5) * 5

       return Task(calendar_key, full_prefix, description, duration)


def print_info(tasks, total_duration):
    print(
        f'Parsed {len(tasks)} tasks.',
        f'Expected duration: {total_duration // 60} h {total_duration % 60} min'
    )
    if total_duration > 60 * MAX_DURATION_HOURS:
        print(f'ABORT: Total duration > {MAX_DURATION_HOURS} h !')
        return

def parse_tasks(task_list):
    task_regex = compile_regex()
    tasks = []
    total_duration = 0

    for line in task_list:
        # silently ignore empty lines and tasks marked '-', '+' 
        # (notation for 'not today-ed' and 'done' before entering into Intend)
        if line.startswith(('-', '+', '\n')):
            continue
        Task = parse_line(line, task_regex)
        if Task:
            tasks.append(Task)
            total_duration += Task.duration
        else:
            print(f'Ignored task line: "{line}"')

    print_info(tasks, total_duration)

    return tasks
