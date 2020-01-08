import sys

import garbageWebsiteParser
import get_html
import iCalExport


def parse_cmd_arguments():
    user_args = sys.argv[1:]
    return user_args


if __name__ == "__main__":
    strasse_hausnummer_tuple = parse_cmd_arguments()
    strasse, hausnummer = strasse_hausnummer_tuple
    print("Looking up Abfallkalender for Address: {} {}".format(strasse, hausnummer))
    garbage_url = "http://213.168.213.236/bremereb/bify/bify.jsp?strasse={}&hausnummer={}".format(strasse, hausnummer)
    path_to_downloaded_html = get_html.download_html_file_from_url(garbage_url)

    if path_to_downloaded_html != "Not a valid address in Bremen!":
        list_of_events = garbageWebsiteParser.getCalendarEvent(path_to_downloaded_html)
        iCalExport.create_ical_file(list_of_events, strasse, hausnummer)