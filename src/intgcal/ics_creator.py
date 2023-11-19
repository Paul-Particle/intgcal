from icalendar import Calendar, Event
import pytz

def create_ics_files(scheduled_tasks, calendar_mapping, task_list_path, timezone='UTC'):
    # Dictionary to hold events for each calendar
    calendars = {}

    for calendar_key, task_description, duration, start_time, end_time in scheduled_tasks:
        # Get the calendar ID (omitting possible '(' in key)
        calendar_id = calendar_mapping.get(calendar_key[-1], '&) Misc')

        # Create an event
        event = Event()
        event.add('summary', f'{calendar_key}) {task_description} [{duration}]')
        event.add('dtstart', start_time.astimezone(pytz.timezone(timezone)))
        event.add('dtend', end_time.astimezone(pytz.timezone(timezone)))

        # Add event to the corresponding calendar in the dictionary
        if calendar_id not in calendars:
            calendars[calendar_id] = Calendar()
        calendars[calendar_id].add_component(event)

    # Write each calendar to its own .ics file
    # Place .ics files in same dir and name as input task list file
    file_path_prefix = task_list_path.split('.txt')[0]
    for calendar_id, cal in calendars.items():
        file_name = f'{file_path_prefix}_{calendar_id}.ics'
        with open(file_name, 'wb') as ics_file:
            ics_file.write(cal.to_ical())
