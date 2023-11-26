# main.py
import os
import json
import argparse
from datetime import datetime
from argparse import RawDescriptionHelpFormatter

from intgcal.task_parser import parse_tasks
from intgcal.scheduler import schedule_tasks
from intgcal.ics_creator import create_ics_files
from intgcal.gcalcli_importer import import_with_gcalcli


def parse_time(time_str):
    # If given convert string from command line argument to datetime
    if time_str:
        try:
            return datetime.strptime(time_str, '%H:%M').time()
        except ValueError:
            raise ValueError(
                f'Invalid time format: {time_str}. Please use HH:MM format.'
            )
    return None


def load_config(path='config.json', start_time=None, end_time=None):
    # Load the configuration file
    if path is None or not os.path.exists(path):
        package_dir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(package_dir, 'config.json')
    with open(path, 'r') as file:
        config = json.load(file)

    # Set default values from the config file if not provided
    calendar_mapping = config['calendar_mapping']
    if not end_time:
        time_limit_str = config['end_time']
        end_time = datetime.strptime(time_limit_str, '%H:%M').time()
    if not start_time:
        start_time = datetime.now().time()

    return calendar_mapping, start_time, end_time


def read_task_list(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()


def main(task_list_path, config_path=None, gcalcli_import=False, start_time=None, end_time=None):

    # Load configuration
    calendar_mapping, start_time, end_time = load_config(config_path, start_time, end_time)

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
        Schedule Intend.do lists on Google Calendar.
        ''',
        formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'task_list_path', 
        help='Path to the task list file'
    )
    parser.add_argument(
        '--config-path',
        help='Optional path to config.json file', 
        default=None
    )  
    parser.add_argument(
        '--gcalcli-import', action='store_true',
        help='Directly import .ics files with gcalcli'
    )
    parser.add_argument(
        '--start-time',
        help='Optional start time in HH:MM format (24-hour)', 
        default=None
    )  
    parser.add_argument(
        '--end-time',
        help='Optional end time in HH:MM format (24-hour)', 
        default=None
    )  

    args = parser.parse_args()

    start_time = parse_time(args.start_time)
    end_time = parse_time(args.end_time)

    main(args.task_list_path, args.config_path, args.gcalcli_import, start_time, end_time)

if __name__ == '__main__':
    cli_wrapper()
