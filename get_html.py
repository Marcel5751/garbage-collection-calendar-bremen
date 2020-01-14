# -*- coding: utf-8 -*-
import codecs
import os
import uuid
from datetime import datetime

import requests
import main

PATH_TO_HTML_FOLDER = "./html-data"


def get_important_part_of_html(filename, html_as_string):
    """Removes useless beginning and end of html file. Uses HTML Comments as Orientation

    Args:
        filename (str): Path to where reduced file should be saved
        html_as_string (str): Content of File

    Returns:
        list: a list of calendar Events
    """

    if not "Kontroll-Abschnitt" in html_as_string:
        # raise ValueError("Keine gültige Adresse in Bremen!")
        return main.NOT_A_VALID_ADDRESS_ERROR_MESSAGE

    # Start Inhalt Termine Jahr 2018
    substring_to_spilt_at = "Start Inhalt Termine Jahr 2018 -->"

    split_one = html_as_string.split(substring_to_spilt_at, 1)
    important_part_one = split_one[1]

    # End Inhalt Termine Jahr 2020
    substring_to_spilt_at_end = "<!-- End Inhalt Termine Jahr 2020"
    split_cut_off_end = important_part_one.split(substring_to_spilt_at_end, 1)
    important_part_two = split_cut_off_end[0]
    write_string_to_html_file(important_part_two, filename)
    return filename


def read_html_from_file(path_to_file):
    """Reads UTF-8 HTML file from disk and returns it as String.

    Args:
        path_to_file (str): Path to the file

    Returns:
        str: content of file as string
    """
    f = codecs.open(path_to_file, 'r', 'utf-8')
    print("reading file {}...".format(path_to_file))
    string = f.read()
    f.close()
    return string


def write_string_to_html_file(string_to_write, filename):
    """Writes String to  UTF-8 HTML file.

    Args:
        string_to_write (str): String to be saved
        filename (str): Path to the file

    Returns:
        str: content of file as string
    """
    text_file = codecs.open(filename, "w", "utf-8-sig")
    n = text_file.write(string_to_write)
    text_file.close()
    return n


def download_html_file_from_url(url_to_download):
    """Downloads content of url and saves it to a html file with a unique filename

    Args:
        url_to_download (str): Url as string

    Returns:
        str: filename
    """
    html_download = requests.get(url_to_download).text
    filename = PATH_TO_HTML_FOLDER + "/" + get_unique_name_for_html_file()
    if not os.path.exists(PATH_TO_HTML_FOLDER):
        os.makedirs(PATH_TO_HTML_FOLDER)
    return get_important_part_of_html(filename, html_download)


def get_unique_name_for_html_file():
    unique_string = uuid.uuid1()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return "{}_{}.html".format(unique_string, timestamp)
