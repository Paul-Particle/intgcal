from icalendar import Calendar, Event
import pytz

def save_ics_files(calendars, task_list_path):
    file_path_prefix = task_list_path.split('.txt')[0]
    for calendar_id, cal in calendars.items():
        file_name = f'{file_path_prefix} {calendar_id}.ics'
        with open(file_name, 'wb') as ics_file:
            ics_file.write(cal.to_ical())

def create_ics_files(scheduled_tasks, calendar_mapping, task_list_path, timezone='UTC'):

    calendars = {}

    for calendar_key, task_description, duration, start_time, end_time in scheduled_tasks:

        # Get the calendar ID ('(' prefix is irrelevant for mapping)
        calendar_id = calendar_mapping.get(calendar_key.removeprefix('('), '&) Misc')

        event = Event()
        event.add('summary', f'{calendar_key}) {task_description} [{duration}]')
        event.add('dtstart', start_time.astimezone(pytz.timezone(timezone)))
        event.add('dtend', end_time.astimezone(pytz.timezone(timezone)))

        if calendar_id not in calendars:
            calendars[calendar_id] = Calendar()
        calendars[calendar_id].add_component(event)

    save_ics_files(calendars, task_list_path)

