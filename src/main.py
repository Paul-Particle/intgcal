import json
import datetime
import argparse
from task_parser import parse_tasks
from scheduler import schedule_tasks, calculate_next_quarter_hour
from ics_creator import create_ics_files
from gcalcli_importer import import_to_gcalcli

def read_task_list(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def load_config():
    config_path = 'config.json'  # Path to the config file in the root directory
    with open(config_path, 'r') as file:
        return json.load(file)

def main(task_list_path):
    # Load configuration
    config = load_config()
    calendar_mapping = config["calendar_mapping"]
    time_limit_str = config["time_limit"]
    time_limit = datetime.datetime.strptime(time_limit_str, '%H:%M').time()

    # Read task list from a file
    task_list = read_task_list(task_list_path)
    
    # Parse tasks
    tasks = parse_tasks(task_list)
    
    # Calculate the next quarter hour from the current time
    start_time = calculate_next_quarter_hour()

    # Schedule tasks
    scheduled_tasks = schedule_tasks(tasks, start_time, time_limit)
    
    # Create .ics files in task list file directory
    create_ics_files(scheduled_tasks, calendar_mapping, task_list_path)

    # import .ics files to Google calendar with gcalcli
    if args.gcalcli_import:
        import_to_gcalcli(calendar_mapping, task_list_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Intentional Calendar Event Generator")
    parser.add_argument(
        "task_list_path",
        help="Path to the task list file"
    )
    parser.add_argument(
        "--gcalcli-import", 
        action="store_true", 
        help="Import to Google Calendar using gcalcli"
    )

    args = parser.parse_args()
    main(args.task_list_path)
