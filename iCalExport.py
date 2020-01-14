# -*- coding: utf-8 -*-
import os
from datetime import datetime

import pytz
from icalendar import Calendar, Event
from icalendar import vText

PATH_TO_OUTPUT_FOLDER = "./ics-data"
total_number_of_events = 0


def create_ical_file(list_of_events, strasse, hausnummer):
    """ Creates an iCal file from a list of Events
    Inspired by tutorial from https://icalendar.readthedocs.io/en/latest/usage.html

    Args:
        list_of_events (list): List of Calender Events to be converted into iCal Format
        strasse (str): Street name
        hausnummer (str): Street number

    Returns:
        str: path to created iCal file
    """
    cal = Calendar()

    # Some properties are required to be compliant:
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')

    global total_number_of_events
    total_number_of_events = len(list_of_events)

    all_ical_events = create_cal_events(list_of_events, strasse, hausnummer)
    for evnt in all_ical_events:
        # Add the event to the calendar:
        cal.add_component(evnt)

    cal_as_ical = cal.to_ical()
    create_folder_if_not_exists()
    # Write iCal file to disk
    return save_ical_file(cal_as_ical, get_filename(strasse, hausnummer))


def create_cal_events(list_of_events, strasse, hausnummer):
    """ Creates iCal events file from a list of Events

    Args:
        list_of_events (list): List of Calender Events to be converted into iCal Format
        strasse (str): Street name
        hausnummer (str): Street number

    Returns:
        list: list of icalendar Events
    """
    list_of_ical_events = []

    for calendarEvent in list_of_events:
        event = Event()
        event = create_ical_event_from_calendar_event(event, calendarEvent, 8, 10)

        # Automatic encoding is not yet implemented for parameter values, so you must use the ‘v*’ types you can import from the icalendar package (they’re defined in icalendar.prop):
        event['location'] = vText('{} {}, Bremen'.format(strasse, hausnummer))

        # TODO uid exaclty according to specification https://www.kanzaki.com/docs/ical/uid.html
        event['uid'] = event['dtstart'].to_ical()
        event.add('priority', 5)
        list_of_ical_events.append(event)

    return list_of_ical_events


def create_ical_event_from_calendar_event(event, calendar_event, starttime, endtime):
    event.add('summary', calendar_event.name)
    event.add('dtstart',
              datetime(calendar_event.year, calendar_event.month, calendar_event.day, starttime, 0, 0, tzinfo=pytz.utc))
    event.add('dtend',
              datetime(calendar_event.year, calendar_event.month, calendar_event.day, endtime, 0, 0, tzinfo=pytz.utc))
    event.add('dtstamp',
              datetime(calendar_event.year, calendar_event.month, calendar_event.day, starttime, 0, 0, tzinfo=pytz.utc))
    return event


def create_folder_if_not_exists():
    if not os.path.isdir(PATH_TO_OUTPUT_FOLDER):
        os.makedirs(PATH_TO_OUTPUT_FOLDER)


def get_filename(strasse, hausnummer):
    now = datetime.now()
    return PATH_TO_OUTPUT_FOLDER + '/' + 'Abfuhrkalender_{}_{}_.ics'.format(strasse + hausnummer,
                                                                            now.strftime("%Y%m%d"))


def save_ical_file(ical, filename):
    f = open(filename, 'wb')
    print("{} Calendar Events successfully saved to {}".format(total_number_of_events, filename))
    f.write(ical)
    f.close()
    return filename
