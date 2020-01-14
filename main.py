# -*- coding: utf-8 -*-

import urllib.request
from urllib.error import URLError

import garbageWebsiteParser
import get_html
import iCalExport

BASE_URL = "http://213.168.213.236/bremereb/bify/bify.jsp"
ABFUEHR_KALENDER_URL = BASE_URL + "?strasse={}&hausnummer={}"
NOT_A_VALID_ADDRESS_ERROR_MESSAGE = "Not a valid address in Bremen!"


def is_site_online():
    try:
        urllib.request.urlopen(BASE_URL).getcode()
        print("Abfallkalender-Website online...")
        return True
    except URLError:
        print("Abfallkalender-Website offline")
        return False


def garbage_calendar(args):
    street = args['street']
    number = args['number']
    start_year = args['start']
    end_year = args['end']

    if is_site_online():
        print("Looking up Abfallkalender for Address: {} {}".format(street, number))
        garbage_url = ABFUEHR_KALENDER_URL.format(street, number)
        path_to_downloaded_html = get_html.download_html_file_from_url(garbage_url, start_year, end_year)

        if path_to_downloaded_html != NOT_A_VALID_ADDRESS_ERROR_MESSAGE:
            list_of_events = garbageWebsiteParser.get_calendar_events(path_to_downloaded_html)
            iCalExport.create_ical_file(list_of_events, street, number)
        else:
            print(NOT_A_VALID_ADDRESS_ERROR_MESSAGE)
