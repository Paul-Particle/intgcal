# main.py
import json
import argparse
from datetime import datetime
from argparse import RawDescriptionHelpFormatter

from intgcal.task_parser import parse_tasks
from intgcal.scheduler import schedule_tasks
from intgcal.ics_creator import create_ics_files
from intgcal.gcalcli_importer import import_with_gcalcli

def parse_time(time_str):
    # Convert time_str to a datetime.time object
    if time_str:
        try:
            time_dt = datetime.strptime(args.time_dt, '%H:%M').time()
        except ValueError:
            raise ValueError(
                f"Invalid time format: {time_str}. Please use HH:MM format."
            )
        return time_dt

def load_config(path, start_time, end_time):
    if not path:
        path = '/Users/peter/Programming/intgcal/config.json'
    with open(path, 'r') as file:
        config = json.load(file)
        calendar_mapping = config["calendar_mapping"]
        time_limit_str = config["end_time"]
        if not end_time:
            end_time = datetime.strptime(time_limit_str, '%H:%M').time()
        if not start_time:
            start_time = datetime.now().time()
        return calendar_mapping, start_time, end_time

def read_task_list(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()


def main(task_list_path, gcalcli_import=False, start_time=None, end_time=None):

    # Load configuration
    calendar_mapping, start_time, end_time = load_config()

    # Read task list from a file
    task_list = read_task_list(task_list_path)
    
    # Parse tasks
    tasks = parse_tasks(task_list)
    
    # Schedule tasks
    scheduled_tasks = schedule_tasks(tasks, start_time, end_time)
    
    # Create .ics files in task list file directory
    create_ics_files(scheduled_tasks, calendar_mapping, task_list_path)

    # import .ics files to Google calendar with gcalcli
    if gcalcli_import:
        import_with_gcalcli(calendar_mapping, task_list_path)


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
    parser.add_argument(
        "--end-time",
        help="Optional start time in HH:MM format (24-hour)", 
        default=None
    )  

    args = parser.parse_args()

    start_time = parse_time(args.start_time)
    end_time = parse_time(args.end_time)

    main(args.task_list_path, args.gcalcli_import, start_time, end_time)

if __name__ == "__main__":
    cli_wrapper()
