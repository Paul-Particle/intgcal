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
            {calendar_prefix}{additional_info}{trailing_parentheses}      # Capturing group for 'X)' format
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

# Example usage
task_list = [
    "2 [1]", #invalid
    "",#invalid
    "4) Randomness & Surprises $wf:r:efbbaef317e2", # invalid (no [time])
    "Invalid task format",
    "1) Check email [5]",
    "(2) Write report [30]",
    "-3) Ignored task [10]",
    "+4) Another ignored task [15]",
    "~) General task [20]",
    "&) Another task [25]",
    "+(~) water 1 [5]",
    "+(~) log am [5]",
    "+(<) outcomes [30]",
    "+(>) intentions [15]",
    "(?) plan day [15]",
    "-(~) food 1 [30]",
    "+4) Sarah outcomes nachlesen",
    "5) System tüfteln weiter [180]",
    "5) Pay invoice Fr. Mathew [5]",
    "4)) Marielis anrufen wg. Essen [10] $wf:458bd987bc3b",
    "4,5)) Spanien planen [45] $wf:520783331385",
    "4)) Plan Marielis Essen [15] $wf:c7cb5ca23a2e",
    "4)) Jakob schreiben [5] $wf:884d12d5475e",
]

parsed_tasks = parse_tasks(task_list)
print(parsed_tasks)
