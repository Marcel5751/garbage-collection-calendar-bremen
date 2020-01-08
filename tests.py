# -*- coding: utf-8 -*-
import unittest
import requests

import get_html


class TestHTMLMethods(unittest.TestCase):

    def test_read_html_from_file(self):
        actual = get_html.read_html_from_file("./testing/reduced_example.html")
        actual_length = len(actual)
        expected = 7939
        self.assertEqual(expected, actual_length)

    def test_get_important_part_of_html(self):
        complete_html_as_string = get_html.read_html_from_file("./testing/full_test_example.html")
        actual = get_html.get_important_part_of_html("./testing/test_result.html", complete_html_as_string)
        expected = "./testing/test_result.html"
        self.assertEqual(expected, actual)
        self.assertEqual(7939, len(get_html.read_html_from_file("./testing/test_result.html")))

    def test_download(self):
        url_to_download = "http://213.168.213.236/bremereb/bify/bify.jsp?strasse=XXX-Testweg&hausnummer=777"
        filename = "./testing/full_test_example.html"
        html_download = requests.get(url_to_download).text
        get_html.write_string_to_html_file(html_download, filename)
        actual_length = len(get_html.read_html_from_file("./testing/full_test_example.html"))
        self.assertEqual(len(html_download) + 1, actual_length)


if __name__ == '__main__':
    unittest.main()
