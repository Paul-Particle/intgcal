import os
import subprocess

def import_with_gcalcli(calendar_mapping, task_list_path):
    # Create a set of unique calendar IDs
    unique_calendar_ids = set(calendar_mapping.values())
    
    file_path_prefix = task_list_path.split('.ido')[0]

    for calendar_id in unique_calendar_ids:
        ics_file = f'{file_path_prefix} {calendar_id}.ics'
        if os.path.exists(ics_file):
            # Escape parentheses in calendar name (causes error for gcalcli)
            calendar_name = calendar_id.replace("(", r"\(").replace(")", r"\)")
            subprocess.run(["gcalcli", "import", ics_file, "--calendar",
                            calendar_name], check=True)
