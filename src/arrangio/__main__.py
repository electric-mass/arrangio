# -*- coding: UTF-8 -*-
#
# copyright: 2023, Electric Mass Records
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""arrangio.

This module arranges a set of songs into groups with similar total play
time.
"""

import sys

from arrangio import __author__, __license__, __project__, __version__
from arrangio._parser_ import get_parser
from arrangio._utils_ import get_songs, get_subsets, to_json, to_text


def main() -> None:
    """Divide group of songs into several groups."""
    header = (
        f'{__project__} version {__version__}\n'
        f'by {__author__} under {__license__} license')
    parser = get_parser(prog=__project__, version=__version__)
    options = parser.parse_args()
    if not options.quiet:
        print(header)
    try:
        songs = get_songs(options.song)
    except ValueError as error:
        print(error)
        sys.exit(9)
    subsets = get_subsets(songs, options.groups)
    if not options.quiet:
        print(to_text(subsets))
    else:
        print(to_json(subsets))


if __name__ == '__main__':
    sys.exit(main())
