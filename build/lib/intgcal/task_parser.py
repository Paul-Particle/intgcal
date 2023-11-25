import re

def parse_tasks(task_list):

    calendar_prefix = r"[0-9\~\&\<\>\?]"
    additional_info = r".{0,5}"
    trailing_parentheses = r"\){1,4}"
    
    task_regex = re.compile(rf"""
        ^                          # Start of the line
        (?:                        # Non-capturing group for the whole prefix
            (\({calendar_prefix}){additional_info}{trailing_parentheses}  # Capturing group for '(X)' format
            |                      # OR
            ({calendar_prefix}){additional_info}{trailing_parentheses}      # Capturing group for 'X)' format
        )                          # Closing parenthesis of the prefix
        \s*                        # Optional whitespace
        ([^\[]+)                   # Capturing group for the task description (anything not a '[')
        \[([0-9]+)\]               # Capturing group for the duration '[Y]'
    """, re.VERBOSE)

    tasks = []
    total_duration = 0

    for line in task_list:
        # Ignore lines starting with '-' or '+' and empty lines
        if line.startswith('-') or line.startswith('+') or line.startswith('\n'):
            continue

        match = task_regex.match(line)
        if match:
            # Handle '(X)' and 'X)' cases. 
            calendar_key = match.group(1) or match.group(2)
            task_description = match.group(3).strip()
            duration = int(match.group(4))
            duration = duration + (- duration % -5)

            tasks.append((calendar_key, task_description, duration))
            total_duration += duration
        else:
            print(f"Warning: Ignored malformed task line: '{line}'")

    print(
        f'Parsed {len(tasks)} tasks.',
        f'Expected duration: {total_duration // 60} h {total_duration % 60} min'
    )
    if total_duration > 60 * 8:
        print('WARNING: Significant workload')
    elif total_duration > 60 * 12:
        print('DANGER: Unsustainable workload!')
    elif total_duration > 60 * 18:
        print('ABORT: Total duration > 18 h !')
        return

    return tasks
