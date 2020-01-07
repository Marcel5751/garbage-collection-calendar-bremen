import sys
from lxml import etree
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
    return 'CalendarEvent(name=' + self.name + ', year=' + str(self.year) + ', month=' + str(self.month) + ', day=' + str(self.day) + ')'


"""Reads the html and generates a list of calendar events

Args:
    html_to_parse (str): Path to the file to be parsed

Returns:
    list: a list of calendar Events
"""
def getCalendarEvent(path_to_html_file):

    tree = LH.parse(path_to_html_file) # type lxml.etree._ElementTree

    list_of_cal_events = []

    # default values set to January 2019
    currentYear = 2019
    currentMonth = 1

    # for td in doc.xpath('//td'): # type lxml.html.HtmlElement
    for td in tree.xpath('//td'): # type lxml.html.HtmlElement
        for elem in td.iter(): # iterate over each individual table cell
            if type(elem) is LH.HtmlElement: # dont parse HtmlComment
                oneMonth = elem.text_content()
                stringWithout = '"'.join(oneMonth.split('\n')[:1])
                print("#####")
                print(stringWithout)
                print("#####")
                if stringWithout == "" or stringWithout == "\r": # handle case of empty string
                    pass
                    # if any(month in stringWithout for month in german_months.values()):
                elif stringWithout.isdigit():
                    currentYear = int(stringWithout)
                # handle case e.g. Juli 2018
                elif any(month in stringWithout for month in german_months.keys()):
                    splitted_string = stringWithout.split(' ', 1)
                    month = splitted_string[0]
                    currentMonth = german_months.get(month)
                    print(str(month))
                    year = splitted_string[1]
                    print("year")
                    print(year)
                    only_year = year[:4]
                    currentYear = int(only_year)
                    print(str(only_year))
                elif stringWithout != "" and not any(month in stringWithout for month in german_months.keys()) and not "\\r\\n\\r\\n" in stringWithout and not "\\r\\n\\t\\t" in stringWithout: # '\\r\\n\\r\\n' \r\n\r\n
                    # parse 19.02. Restmüll / Bioabfall
                    split_string = stringWithout.strip().split('.', 2)
                    print("split_string")
                    print(split_string)
                    #['22', '08', '\xa0Restmüll / Bioabfall']
                    day = remove_sa(split_string[0])
                    print(day)
                    if day.find("  ") != -1:
                        day = day.split("  ")[1]
                    print(day)
                    month = split_string[1]
                    currentMonth = month
                    title = split_string[2]
                    # title, year, month, day
                    calEvent = CalendarEvent(title, currentYear, int(currentMonth), int(day))
                    list_of_cal_events.append(calEvent)

    print_all_cal_events(list_of_cal_events)
    return list_of_cal_events


# handle case where there is a prefix of (sa) before the date, eg. (Sa) 29.12. Restm. / Bioabf.
def remove_sa(day):
    if day.find("(Sa)") != -1:
        return day.split(")")[1]
    else:
        return day


def print_all_cal_events(list_of_cal_events):
    for calEvent in list_of_cal_events:
        print(str(calEvent))
