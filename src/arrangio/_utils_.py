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

# from functools import lru_cache as cache
from datetime import datetime as _datetime, timedelta as _timedelta
from re import compile as _compile
from typing import Final


REGXPR: Final[str] = (
    r'^(?P<label>\w+):'
    r'((?P<hours>\d+)h)?((?P<minutes>\d+)m)?(?P<seconds>\d+)s$')
TIMEFMT: Final[str] = '%H:%M:%S'


def _to_seconds(timestamp: str) -> int:
    """converts the timestamp into seconds.

    Args:
        timestamp (str): The timestamp to converto to seconds. Format
            needs to be 'HH:MM:SS'.

    Returns:
        int: The timestamp in seconds.
    """
    return int(
        (_datetime.strptime(
            timestamp, TIMEFMT) - _datetime(1900, 1, 1)).total_seconds())


def _to_time(seconds: int) -> str:
    """converts the seconds into a timestamp.

    Args:
        seconds (int): The seconds to converto to timestamp.

    Returns:
        str: The timestamp string.
    """
    return str(_timedelta(seconds=seconds))


def get_songs(songs: list) -> list:
    """Parses the songs entered in the options.

    Args:
        songs (list(str)): The list of songs inputed by the user (as
            collected by the `_parser_` module).

    Returns:
        list(tuple(str, int)): The list of songs defined as a tuple of
            song name and song lenght (in seconds).

    Raises:
        ValueError: If the song info is not in the form of
            'label:00h00m00s'.
    """
    pattern = _compile(REGXPR)
    unsorted_songs = []
    for song in songs:
        matched = pattern.match(song)
        if matched is None:
            raise ValueError(f'[ERROR] Invalid song information ({song}).')
        info = matched.groupdict(default='0')
        seconds = _to_seconds(
            f'{info["hours"]}:{info["minutes"]}:{info["seconds"]}')
        unsorted_songs.append((seconds, info['label']))
    return sorted(unsorted_songs, reverse=True)


# def __list_to_tuple(function):
#     def wrapper(*args, **kwargs):
#         args = [tuple(x) if isinstance(x, list) else x for x in args]
#         kwargs = {
#             k: tuple(x) if isinstance(x, list) else x
#             for k, x in kwargs.items()}
#         print('---->', args, kwargs)
#         print('---->', *args, **kwargs)
#         return function(*args, **kwargs)
#     return wrapper


# @__list_to_tuple
# @cache(maxsize=None, typed=False)
def __get_subsets(
        songs: list,
        songs_length: int,
        subsets: list) -> list:
    """Auxiliar function for `get_subsets`.

    Args:
        songs (list): The list of songs (from `get_songs`).
        songs_length (int): The length of `songs`.
        subsets (list): The list of possible subsets.

    Returns:
        tuple(int, list(tuple(int, str))): The list of subsets.
    """
    if songs_length == 0:
        _min, _ = min(subsets)
        _max, _ = max(subsets)
        return (_max - _min, subsets)
    _songs = songs.copy()
    _songs_length = songs_length - 1
    _song = _songs.pop(0)
    _possible_subsets = []
    for element in subsets:
        _subset = element[1].copy()
        _subset.append(_song)
        _element = (element[0] + _song[0], _subset)
        _subsets = subsets.copy()
        _subsets.remove(element)
        _subsets.append(_element)
        _possible_subsets.append(_subsets)
    return min([
        __get_subsets(_songs, _songs_length, sub)
        for sub
        in _possible_subsets])


def get_subsets(songs: list, num: int) -> list:
    """Parses the songs entered in the options.

    Args:
        songs (list): The list of songs (from `get_songs`).
        num (int): The number of subsets to divide the set into.

    Returns:
        list(tuple(int, list(tuple(int, str)))): The list of subsets).
    """
    # total_length = sum(l for l, _ in songs)
    songs_length = len(songs)
    subsets = [(0, [])] * num
    return __get_subsets(
        songs,
        songs_length,
        subsets)


def show_results(result: tuple) -> None:
    """Parses result of `get_subsets` and prints it to the screen.

    Args:
        result (tuple(int, list()): the result from `get_subsets`.
    """
    print('Difference (in seconds):', result[0])
    print('Groups:')
    for idx, subset in enumerate(result[1]):
        print(
            f'  [{idx + 1}] {_to_time(subset[0])}',
            [f'{song[1]} ({_to_time(song[0])})' for song in subset[1]])
