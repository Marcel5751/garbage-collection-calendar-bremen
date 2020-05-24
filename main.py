# -*- coding: utf-8 -*-

import urllib.request
from urllib.error import URLError

import garbageWebsiteParser
import get_html
import iCalExport

BASE_URL = "http://213.168.213.236/bremereb/bify/bify.jsp"
ABFUEHR_KALENDER_URL = BASE_URL + "?strasse={}&hausnummer={}"
NOT_A_VALID_ADDRESS_ERROR_MESSAGE = "Not a valid address in Bremen!"
SUCCESS_MESSAGE = "successfully created calendar file"
NOT_AVAILABLE_MESSAGE = "Abfallkalender-Website offline oder server offline"


class ResultDTO:
    status_code = 0
    result_messages = ""
    result = ""

    def __init__(self, status_code, error_messages, result):
        self.status_code = status_code
        self.result_messages = error_messages
        self.result = result

    def __repr__(self):
        return {'status_code': self.status_code, 'error_messages': self.result_messages}

    def __str__(self):
        return 'resultDTO(status_code=' + self.status_code + ', error_messages=' + str(self.result_messages) + ')'


def is_site_online():
    try:
        urllib.request.urlopen(BASE_URL).getcode()
        print("Abfallkalender-Website online...")
        return True
    except URLError:
        print("Abfallkalender-Website offline")
        return False


def get_garbage_calendar(args):
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
            saved_filename = iCalExport.create_ical_file(list_of_events, street, number)
            only_filename = saved_filename.split("/")[2]
            return ResultDTO(200, SUCCESS_MESSAGE, only_filename)
        else:
            print(NOT_A_VALID_ADDRESS_ERROR_MESSAGE)
            return ResultDTO(400, NOT_A_VALID_ADDRESS_ERROR_MESSAGE, None)
    else:
        return ResultDTO(400, NOT_AVAILABLE_MESSAGE, None)
