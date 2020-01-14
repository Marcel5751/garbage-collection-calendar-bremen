# -*- coding: utf-8 -*-

import argparse
import datetime

import main
from __init__ import __version__


def get_parser():
    parser = argparse.ArgumentParser(description='get garbage calendar dates as ical for Bremen')

    parser.add_argument('street', metavar='STREET', help='Der Straßenname', nargs='?')
    parser.add_argument('number', metavar='NUMBER', help='Die Hausnummer', nargs='?')

    current_year = datetime.date.today().year
    parser.add_argument('-start', '--start', help='starting year', default=current_year, type=int)
    parser.add_argument('-end', '--end', help='end year', default=current_year, type=int)
    parser.add_argument('-v', '--version', help='displays the current version of garbage-calendar',
                        action='store_true')
    return parser


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(__version__)
        return

    if not args['street'] or not args['number']:
        parser.print_help()
        return

    if args['start']:
        pass  # TODO verify

    if args['end']:
        pass  # TODO verify

    main.garbage_calendar(args)


if __name__ == "__main__":
    command_line_runner()
