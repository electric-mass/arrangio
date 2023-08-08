# -*- coding: UTF-8 -*-
#
# copyright: 2023, Electric Mass Records
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Command-line parsing module.

This module is based on the `argparse` command-line parsing library.

The following resources are provided by this module:

| Name         | Type                      | Description      |
+--------------+---------------------------+------------------+
| get_parser() | `argparse.ArgumentParser` | gets the parser  |


All other resources in this module are considered implementation
details.
"""

from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from typing import Final


__all__: Final[tuple] = ('get_parser',)


def get_parser(
        prog: str = __package__,
        version: str = '0.0.0') -> ArgumentParser:
    """Initialize the parser.

    Args:
        prog (str): The name of the program. Defaults to `__package__`.
        version (string): The program version. Defaults to '0.0.0'.

    Returns:
        ArgumentParser: The parser.
    """
    parser = ArgumentParser(  # main parser
        prog=prog,
        formatter_class=ArgumentDefaultsHelpFormatter,
        add_help=True,
        allow_abbrev=False)
    parser.add_argument(
        '-g',
        '--groups',
        action='store',
        nargs='?',
        default=2,
        metavar='NUM',
        type=int,
        help='number of groups to create')
    parser.add_argument(
        '-q',
        '--quiet',
        action='store_true',
        help='quiet mode')
    parser.add_argument(
        '-s',
        '--song',
        action='extend',
        nargs='+',
        metavar='LABEL:HHhMMmSSs',
        type=str,
        required=True,
        help='song information (e.g.: label:00h03m27s)')
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=version)
    return parser
