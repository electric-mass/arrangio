# -*- coding: UTF-8 -*-
#
# copyright: 2023, Electric Mass Records
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Tests for the `_utils_` module."""

from pytest import mark, raises
from arrangio import _utils_ as utils


@mark.parametrize('args,result,exception', [
    ([], None, TypeError),
    (['01'], None, ValueError),
    (['00:01'], None, ValueError),
    (['0:0:1'], 1, None),
    (['00:00:01'], 1, None),
    (['00:01:00'], 60, None),
    (['01:00:00'], 3600, None),
    (['01:10:12'], 4212, None),
])
def test__utils___to_seconds(args, result, exception):
    """test__utils___to_seconds."""
    if exception:
        with raises(exception):
            _ = utils._to_seconds(*args)
    else:
        assert result == utils._to_seconds(*args)


@mark.parametrize('args,result,exception', [
    ([], None, TypeError),
    (['01'], None, TypeError),
    ([1.5], '0:00:01.500000', None),
    ([1], '0:00:01', None),
    ([60], '0:01:00', None),
    ([3600], '1:00:00', None),
    ([4212], '1:10:12', None),
])
def test__utils___to_time(args, result, exception):
    """test__utils___to_time."""
    if exception:
        with raises(exception):
            _ = utils._to_time(*args)
    else:
        assert result == utils._to_time(*args)


@mark.parametrize('args,result,exception', [
    (['01'], None, ValueError),
    (['00:01'], None, ValueError),
    (['label'], None, ValueError),
    (['label:'], None, ValueError),
    (['label:00:01'], None, ValueError),
    (['song_01:0h0m1s'], [(1, 'song_01')], None),
    (['song_01:00h00m01s'], [(1, 'song_01')], None),
    (['song_01:00m01s'], [(1, 'song_01')], None),
    (['song_01:01s'], [(1, 'song_01')], None),
    (['song01:02s', 'song02:01s'], [(2, 'song01'), (1, 'song02')], None),
])
def test__utils__get_songs(args, result, exception):
    """test__utils__get_songs."""
    if exception:
        with raises(exception):
            _ = utils.get_songs(args)
    else:
        assert result == utils.get_songs(args)


@mark.parametrize('args,result', [
    ([[], 0, [(0, [])]], (0, [(0, [])])),
    ([[(2, 'song_01')], 1, [(0, [])]], (0, [(2, [(2, 'song_01')])])),
])
def test__utils____get_subsets(args, result):
    """test__utils____get_subsets."""
    assert result == utils.__get_subsets(*args)


@mark.parametrize('args,result', [
    ([[], 1], (0, [(0, [])])),
    (
        [[(354, 'song05'), (337, 'song03'), (316, 'song06'), (291, 'song04'), (281, 'song08'), (225, 'song07'), (221, 'song02'), (170, 'song09'), (55, 'song01')], 2],
        (8, [(1121, [(354, 'song05'), (316, 'song06'), (281, 'song08'), (170, 'song09')]), (1129, [(337, 'song03'), (291, 'song04'), (225, 'song07'), (221, 'song02'), (55, 'song01')])])
    ),
    (
        [[(354, 'song05'), (337, 'song03'), (316, 'song06'), (291, 'song04'), (281, 'song08'), (225, 'song07'), (221, 'song02'), (170, 'song09'), (55, 'song01')], 3],
        (20, [(762, [(316, 'song06'), (225, 'song07'), (221, 'song02')]), (742, [(291, 'song04'), (281, 'song08'), (170, 'song09')]), (746, [(354, 'song05'), (337, 'song03'), (55, 'song01')])])
    ),
])
def test__utils__get_subsets(args, result):
    """test__utils__get_subsets."""
    assert result == utils.get_subsets(*args)


@mark.parametrize('args,result', [
    (
        (8, [(1121, [(354, 'song05'), (316, 'song06'), (281, 'song08'), (170, 'song09')]), (1129, [(337, 'song03'), (291, 'song04'), (225, 'song07'), (221, 'song02'), (55, 'song01')])]),
        "Difference (in seconds): 8\nGroups:\n  [1] 0:18:41 ['song05 (0:05:54)', 'song06 (0:05:16)', 'song08 (0:04:41)', 'song09 (0:02:50)']\n  [2] 0:18:49 ['song03 (0:05:37)', 'song04 (0:04:51)', 'song07 (0:03:45)', 'song02 (0:03:41)', 'song01 (0:00:55)']\n"
    ),
    (
        (20, [(762, [(316, 'song06'), (225, 'song07'), (221, 'song02')]), (742, [(291, 'song04'), (281, 'song08'), (170, 'song09')]), (746, [(354, 'song05'), (337, 'song03'), (55, 'song01')])]),
        "Difference (in seconds): 20\nGroups:\n  [1] 0:12:42 ['song06 (0:05:16)', 'song07 (0:03:45)', 'song02 (0:03:41)']\n  [2] 0:12:22 ['song04 (0:04:51)', 'song08 (0:04:41)', 'song09 (0:02:50)']\n  [3] 0:12:26 ['song05 (0:05:54)', 'song03 (0:05:37)', 'song01 (0:00:55)']\n"
    ),
])
def test__utils__show_results(capsys, args, result):
    """test__utils__show_results."""
    utils.show_results(args)
    stdout, _ = capsys.readouterr()
    assert result == stdout
