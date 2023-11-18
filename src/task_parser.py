import re

def parse_tasks(task_list):
    tasks = []

    # Named regex sub-patterns for clarity
    calendar_prefix = r"[0-9\~\&\<\>\?]"
    additional_info = r".{0,5}"
    trailing_parentheses = r"\){1,4}"
    
    # Combining sub-patterns into the final regex pattern
    task_regex = re.compile(rf"""
        ^                          # Start of the line
        (?:                        # Non-capturing group for the whole prefix
            \(({calendar_prefix}{additional_info}){trailing_parentheses}  # Capturing group for '(X)' format
            |                      # OR
            ({calendar_prefix}{additional_info}){trailing_parentheses}      # Capturing group for 'X)' format
        )                          # Closing parenthesis of the prefix
        \s*                        # Optional whitespace
        ([^\[]+)                   # Capturing group for the task description (anything not a '[')
        \[([0-9]+)\]               # Capturing group for the duration '[Y]'
    """, re.VERBOSE)
    for line in task_list:
        # Ignore lines starting with '-' or '+'
        if line.startswith('-') or line.startswith('+'):
            continue

        # Match the line with the regular expression
        match = task_regex.match(line)
        if match:
            # Handle '(X)' and 'X)' cases. 
            # If no match, .group() returns None, so the first .group(). 'or'
            # only checks the first operand's 'truthyness' and returns it if it
            # is true, and the second operand if not.
            calendar_key = match.group(1) or match.group(2)
            task_description = match.group(3).strip()
            duration = int(match.group(4))

            tasks.append((calendar_key, task_description, duration))
        else:
            # Handle error: malformed task line
            print(f"Warning: Ignored malformed task line: '{line}'")

    return tasks
