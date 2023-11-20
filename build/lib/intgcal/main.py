import json
import datetime as dt
import argparse
from argparse import RawDescriptionHelpFormatter
from intgcal.task_parser import parse_tasks
from intgcal.scheduler import schedule_tasks, calculate_next_quarter_hour
from intgcal.ics_creator import create_ics_files
from intgcal.gcalcli_importer import import_to_gcalcli

def read_task_list(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def load_config():
    config_path = 'config.json'  # Path to the config file in the root directory
    with open(config_path, 'r') as file:
        return json.load(file)

def main(task_list_path, gcalcli_import=False, start_time=None):

    # Load configuration
    config = load_config()
    calendar_mapping = config["calendar_mapping"]
    time_limit_str = config["time_limit"]
    time_limit = dt.datetime.strptime(time_limit_str, '%H:%M').time()

    # Read task list from a file
    task_list = read_task_list(task_list_path)
    
    # Parse tasks
    tasks = parse_tasks(task_list)
    
    # Schedule tasks
    scheduled_tasks = schedule_tasks(tasks, start_time, time_limit)
    
    # Create .ics files in task list file directory
    create_ics_files(scheduled_tasks, calendar_mapping, task_list_path)

    # import .ics files to Google calendar with gcalcli
    if gcalcli_import:
        import_to_gcalcli(calendar_mapping, task_list_path)

def cli_wrapper():
    parser = argparse.ArgumentParser(
        description=''' 
        Schedule Intend.do lists on Google Calendar.\n\n
        Add the estimated duration of the intention in minutes enclosed in
        brackets after the description.\n\n
        Example: '1) Work on report [120]' would generate 120 minute event at
        the next full quarter hour in the calendar '1) Work' as per the default
        config.json.\n\n
        For each goal prefix one .ics file is created. Automatic import of .ics
        files is done with gcalcli (install separately, including vobject
        required for the import functionality). Use config.json to set up the
        mapping between goals and calendars.\n\n
        ''',
        formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "task_list_path", 
        help='Path to the task list file'
    )
    parser.add_argument(
        "--gcalcli-import", action="store_true",
        help='Directly import .ics files with gcalcli'
    )
    parser.add_argument(
        "--start-time",
        help="Optional start time in HH:MM format (24-hour)", 
        default=None
    )  


    args = parser.parse_args()


    # Convert start_time_str to a datetime.time object
    if args.start_time:
        try:
            start_time = dt.datetime.strptime(args.start_time, '%H:%M').time()
        except ValueError:
            raise ValueError(f"Invalid time format: {start_time_str}. Please use HH:MM format.")
    else:
        start_time = calculate_next_quarter_hour().time()


    main(args.task_list_path, args.gcalcli_import, start_time)

if __name__ == "__main__":
    cli_wrapper()
