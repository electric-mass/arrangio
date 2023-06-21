# -*- coding: UTF-8 -*-
#
# copyright: 2023, Electric Mass Records
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""arrangio

This module arranges a set of songs into groups with similar total play
time.
"""

import sys
from arrangio import __author__, __license__, __project__, __version__
from arrangio._parser_ import get_parser
from arrangio._utils_ import get_songs, get_subsets, show_results


def main() -> None:
    """main method"""
    header = (
        f'{__project__} version {__version__}\n'
        f'by {__author__} under {__license__} license')
    parser = get_parser(prog=__project__, version=__version__)
    options = parser.parse_args()
    if not options.quiet:
        print(header)
    # print(options)
    try:
        songs = get_songs(options.song)
    except ValueError as error:
        print(error)
        sys.exit(9)
    # print(songs)
    subsets = get_subsets(songs, options.groups)
    # print(subsets)
    if not options.quiet:
        show_results(subsets)
    else:
        print(subsets)


if __name__ == '__main__':
    sys.exit(main())
