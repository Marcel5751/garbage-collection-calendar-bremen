# -*- coding: utf-8 -*-
import os
from datetime import datetime

import pytz
from icalendar import Calendar, Event
from icalendar import vText

PATH_TO_OUTPUT_FOLDER = "./ics-data"

# following tutorial from https://icalendar.readthedocs.io/en/latest/usage.html
def create_ical_file(list_of_events, strasse, hausnummer):
    cal = Calendar()

    # Some properties are required to be compliant:
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')

    # We need at least one subcomponent for a calendar to be compliant:
    all_ical_events = create_cal_events(list_of_events, strasse, hausnummer)
    for evnt in all_ical_events:
        # Add the event to the calendar:
        cal.add_component(evnt)

    now = datetime.now()

    # Write iCal file to disk
    # if not os.path.exists(PATH_TO_OUTPUT_FOLDER):
    if not os.path.isdir(PATH_TO_OUTPUT_FOLDER):
        os.makedirs(PATH_TO_OUTPUT_FOLDER)

    filename = PATH_TO_OUTPUT_FOLDER + '/' + 'Abfuhrkalender_{}_{}_.ics'.format(strasse + hausnummer, now.strftime("%Y%m%d"))
    f = open(filename, 'wb')
    print(str(f))
    f.write(cal.to_ical())
    f.close()


def create_cal_events(list_of_events, strasse, hausnummer):
    list_of_ical_events = []

    for calendarEvent in list_of_events:
        event = Event()
        event.add('summary', calendarEvent.name)
        event.add('dtstart', datetime(calendarEvent.year, calendarEvent.month, calendarEvent.day, 8, 0, 0, tzinfo=pytz.utc))
        event.add('dtend', datetime(calendarEvent.year, calendarEvent.month, calendarEvent.day, 10, 0, 0, tzinfo=pytz.utc))
        event.add('dtstamp', datetime(calendarEvent.year, calendarEvent.month, calendarEvent.day, 8, 0, 0, tzinfo=pytz.utc))

        # Automatic encoding is not yet implemented for parameter values, so you must use the ‘v*’ types you can import from the icalendar package (they’re defined in icalendar.prop):
        event['location'] = vText('{} {}, Bremen'.format(strasse, hausnummer))

        # event['uid'] = '20050115T101010/27346262376@mxm.dk'
        # TODO uid exaclty according to specification https://www.kanzaki.com/docs/ical/uid.html
        event['uid'] = event['dtstart'].to_ical()
        event.add('priority', 5)
        list_of_ical_events.append(event)

    return list_of_ical_events

