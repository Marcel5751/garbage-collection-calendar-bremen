# -*- coding: utf-8 -*-
import unittest
import requests
import codecs

import get_html
import main


class TestHTMLMethods(unittest.TestCase):

    def test_read_html_from_file(self):
        actual = read_html_from_file("./testing/reduced_example.html")
        actual_length = len(actual)
        expected = 7939
        self.assertEqual(expected, actual_length)

    def test_get_important_part_of_html(self):
        complete_html_as_string = read_html_from_file("./testing/full_test_example.html")
        start_year = 2018
        end_year = 2020
        actual = get_html.get_important_part_of_html("./testing/test_result.html", complete_html_as_string, start_year, end_year)
        expected = "./testing/test_result.html"
        self.assertEqual(expected, actual)
        self.assertEqual(7939, len(read_html_from_file("./testing/test_result.html")))

    def test_download(self):
        url_to_download = main.ABFUEHR_KALENDER_URL.format("XXX-Testweg", 777)
        filename = "./testing/full_test_example.html"
        html_download = requests.get(url_to_download).text
        get_html.write_string_to_html_file(html_download, filename)
        actual_length = len(read_html_from_file("./testing/full_test_example.html"))
        self.assertEqual(len(html_download) + 1, actual_length)


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


if __name__ == '__main__':
    unittest.main()
