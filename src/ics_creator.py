from icalendar import Calendar, Event
import pytz

def create_ics_files(scheduled_tasks, calendar_mapping, timezone='UTC'):
    for calendar_key, task_description, duration, start_time, end_time in scheduled_tasks:
        # Create a calendar
        cal = Calendar()

        # Create an event
        event = Event()
        event.add('summary', f'{task_description} [{duration} mins]')
        event.add('dtstart', start_time.astimezone(pytz.timezone(timezone)))
        event.add('dtend', end_time.astimezone(pytz.timezone(timezone)))

        # Add the event to the calendar
        cal.add_component(event)

        # Save the calendar to an .ics file
        calendar_id = calendar_mapping.get(calendar_key, 'default')
        file_name = f'{calendar_id}_{start_time.strftime("%Y%m%dT%H%M%S")}.ics'
        with open(file_name, 'wb') as ics_file:
            ics_file.write(cal.to_ical())

create_ics_files(scheduled_tasks, calendar_mapping)
