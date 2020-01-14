# -*- coding: utf-8 -*-
import lxml.html as LH

german_months = {
    "Januar": 1,
    "Februar": 2,
    "März": 3,
    "April": 4,
    "Mai": 5,
    "Juni": 6,
    "Juli": 7,
    "August": 8,
    "September": 9,
    "Oktober": 10,
    "November": 11,
    "Dezember": 12,
}


class CalendarEvent:
    def __init__(self, name, year, month, day):
        self.name = name
        self.year = year
        self.month = month
        self.day = day

    def __str__(self):
        return 'CalendarEvent(name=' + self.name + ', year=' + str(self.year) + ', month=' + str(
            self.month) + ', day=' + str(self.day) + ')'


def get_calendar_events(path_to_html_file):
    """Reads the html and generates a list of calendar events

    Args:
        path_to_html_file (str): Path to the file to be parsed

    Returns:
        list: a list of calendar Events
    """

    tree = LH.parse(path_to_html_file)  # type lxml.etree._ElementTree

    list_of_cal_events = []

    # default values set to January 2019
    currentYear = 2019
    currentMonth = 1

    # for td in doc.xpath('//td'): # type lxml.html.HtmlElement
    for td in tree.xpath('//td'):  # type lxml.html.HtmlElement
        for elem in td.iter():  # iterate over each individual table cell
            if type(elem) is LH.HtmlElement:  # dont parse HtmlComment
                oneMonth = elem.text_content()
                stringWithout = '"'.join(oneMonth.split('\n')[:1])
                if stringWithout == "" or stringWithout == "\r":  # handle case of empty string
                    pass
                    # if any(month in stringWithout for month in german_months.values()):
                elif stringWithout.isdigit():
                    currentYear = int(stringWithout)
                # handle case e.g. Juli 2018
                elif any(month in stringWithout for month in german_months.keys()):
                    splitted_string = stringWithout.split(' ', 1)
                    month = splitted_string[0]
                    currentMonth = german_months.get(month)
                    year = splitted_string[1]
                    only_year = year[:4]
                    currentYear = int(only_year)
                elif stringWithout != "" and not any(month in stringWithout for month in
                                                     german_months.keys()) and not "\\r\\n\\r\\n" in stringWithout and not "\\r\\n\\t\\t" in stringWithout:  # '\\r\\n\\r\\n' \r\n\r\n
                    # parse 19.02. Restmüll / Bioabfall
                    split_string = stringWithout.strip().split('.', 2)
                    # ['22', '08', '\xa0Restmüll / Bioabfall']
                    day = remove_sa(split_string[0])
                    if day.find("  ") != -1:
                        day = day.split("  ")[1]
                    month = split_string[1]
                    currentMonth = month
                    title = split_string[2]
                    # title, year, month, day
                    calEvent = CalendarEvent(title, currentYear, int(currentMonth), int(day))
                    list_of_cal_events.append(calEvent)

    return list_of_cal_events


# handle case where there is a prefix of (sa) before the date, eg. (Sa) 29.12. Restm. / Bioabf.
# Remove the Sa because we do not need it
def remove_sa(day):
    if day.find("(Sa)") != -1:
        return day.split(")")[1]
    else:
        return day


def print_all_cal_events(list_of_cal_events):
    for calEvent in list_of_cal_events:
        print(str(calEvent))


def filter_list(list_of_events, start_year, end_year):
    years = list(range(start_year, end_year + 1))  # add 1 to include the year
    return list(filter(lambda x: (x.year in years), list_of_events))
