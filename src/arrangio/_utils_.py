# -*- coding: UTF-8 -*-
#
# copyright: 2023, Electric Mass Records
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""helper functions module.

The following resources are provided by this module:

| Name         | Type                      | Description               |
+--------------+---------------------------+---------------------------+
| get_songs()  | `list(tuple(int, str))`   | gets the list of songs    |
| get_subsets  | `list(tuple(int, list))`  | gets the subsets of songs |
| show_results | `None`                    | shows the results         |

All other resources in this module are considered implementation
details.
"""

from datetime import timedelta as _timedelta
from functools import lru_cache as cache
from json import dumps as _dumps
from re import compile as _compile
from typing import Final


REGXPR: Final[str] = (
    r'^(?P<label>\w+):'
    r'((?P<hours>\d+)h)?((?P<minutes>\d+)m)?(?P<seconds>\d+)s$')
TIMEFMT: Final[str] = '%H:%M:%S'


def _to_seconds(
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0) -> int:
    """Convert `hours`, `minutes`, and `seconds` into seconds.

    Args:
        hours (int): Amount of hours to convert. Defaults to 0.
        minutes (int): Amount of minutes to convert. Defaults to 0.
        seconds (int): Amount of seconds to convert. Defaults to 0.

    Returns:
        int: The timestamp in seconds.
    """
    return int(_timedelta(
        seconds=seconds, minutes=minutes, hours=hours).total_seconds())


def _to_time(seconds: int) -> str:
    """Convert `seconds` into a timestamp.

    Args:
        seconds (int): The seconds to converto to timestamp.

    Returns:
        str: The timestamp string.
    """
    return str(_timedelta(seconds=seconds))


def get_songs(songs: list) -> tuple:
    """Parse a list of songs.

    Parses the `songs` variable that should be a list with all the
    songs captured by the `_parser_` module.

    Args:
        songs (list(str)): The list of songs inputed by the user (as
            collected by the `_parser_` module).

    Returns:
        tuple(tuple(str, int)): The list of songs defined as a tuple of
            tuples with the song name and the song lenght (in seconds).

    Raises:
        ValueError: If the song info is not in the form of
            'label:00h00m00s'.
    """
    pattern = _compile(REGXPR)
    unsorted_songs = []
    for song in songs:
        matched = pattern.match(song)
        if matched is None:
            msg = f'[ERROR] Invalid song information ({song}).'
            raise ValueError(msg)
        info = matched.groupdict(default='0')
        seconds = _to_seconds(
            hours=int(info['hours']),
            minutes=int(info['minutes']),
            seconds=int(info['seconds']))
        unsorted_songs.append((seconds, info['label']))
    return tuple(sorted(unsorted_songs, reverse=True))


@cache(maxsize=None, typed=False)
def __get_subsets(
        songs: tuple,
        songs_length: int,
        subsets: tuple) -> tuple:
    """Auxiliar function for `get_subsets`.

    Args:
        songs (tuple): The list of songs (from `get_songs`).
        songs_length (int): The length of `songs`.
        subsets (tuple): The list of possible subsets.

    Returns:
        tuple(int, tuple(tuple(int, str))): The list of subsets.
    """
    if songs_length == 0:
        _min, _ = min(subsets)
        _max, _ = max(subsets)
        return (_max - _min, subsets)
    _songs = songs[1:]
    _song = songs[0]
    _songs_length = songs_length - 1
    _possible_subsets = ()
    for index, element in enumerate(subsets):
        _subset = (_song, *element[1])
        _element = (element[0] + _song[0], _subset)
        _subsets = (_element, *subsets[:index], *subsets[index + 1:])
        _possible_subsets = (_subsets, *_possible_subsets)
    return min(
        __get_subsets(_songs, _songs_length, sub)
        for sub
        in _possible_subsets)


def get_subsets(songs: tuple, num: int) -> tuple:
    """Divide `songs` into `num` groups.

    Divide the songs present in the `songs` variable into `num` groups
    such that the difference between the total lenght of the songs on
    each group is the minimum possible.

    Args:
        songs (tuple): The list of songs (from `get_songs`).
        num (int): The number of subsets to divide the set into.

    Returns:
        tuple(tuple(int, tuple(tuple(int, str)))): The list of subsets).
    """
    songs_length = len(songs)
    subsets = ((0, ()),) * num
    return __get_subsets(
        songs,
        songs_length,
        subsets)


def to_json(result: tuple) -> str:
    """Convert the `result` to JSON.

    Convert the content of the `result` variable to a JSON string. The
    `result` should be the output of the `get_subsets` function.

    Args:
        result (tuple(int, list()): the result from `get_subsets`.

    Returns:
        str: The JSON string that represents the `result`.
    """
    _groups = []
    for idx, subset in enumerate(result[1]):
        _group = {
            'id': idx,
            'lenght': subset[0],
            'songs': [{'name': nm, 'lenght': ln} for (ln, nm) in subset[1]]}
        _groups.append(_group)
    return _dumps({'difference': result[0], 'groups': _groups})


def to_text(result: tuple) -> str:
    """Convert the `result` to text.

    Convert the content of the `result` variable into a printable
    string. The `result` should be the output of the `get_subsets`
    function.

    Args:
        result (tuple(int, list()): the result from `get_subsets`.

    Returns:
        str: The string that represents the `result`.
    """
    text = [
        f'Difference (in seconds): {result[0]}',
        'Groups:']
    for idx, subset in enumerate(result[1]):
        text.append(
            f'  [{idx + 1}] {_to_time(subset[0])} '
            f'{[f"{song[1]} ({_to_time(song[0])})" for song in subset[1]]}')
    return '\n'.join(text)
