# -*- coding: UTF-8 -*-
#
# copyright: 2023, Electric Mass Records
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Tests for the `_parser_` module."""

import sys
from argparse import Namespace
from pytest import mark, raises
from arrangio import __version__, __project__, _parser_ as parser


@mark.parametrize('args,exception,exit_code', [
    ([], SystemExit, 2),
    ([__project__, '--quiet'], SystemExit, 2),
    ([__project__, '--groups', '2', 'fake'], SystemExit, 2),
    ([__project__, '--groups', '2', '--fake'], SystemExit, 2),
    ([__project__, '--version'], SystemExit, 0),
    ([__project__, '--help'], SystemExit, 0),
    ([__project__, '--song', 'song_01:1m32s'], None, 0),
    ([__project__, '--song', 'song_01:1m32s', '--groups', '2'], None, 0),
])
def test__parser__get_parser(mocker, args, exception, exit_code):
    """test__parser__get_parser."""
    mocker.patch.object(sys, 'argv', args)
    if exception:
        with raises(exception) as error:
            test_parser = parser.get_parser()
            _ = test_parser.parse_args()
        assert error.type == exception
        assert error.value.code == exit_code
    else:
        test_parser = parser.get_parser()
        options = test_parser.parse_args()
        assert options
        assert isinstance(options, Namespace)


def test__parser__version(capsys, mocker):
    """test__parser__version."""
    mocker.patch.object(sys, 'argv', ['prog', '--version'])
    with raises(SystemExit) as error:
        test_parser = parser.get_parser(prog='prog', version=__version__)
        _ = test_parser.parse_args()
    captured = capsys.readouterr()
    assert captured.out == f'{__version__}\n'
    assert captured.err == ''
    assert error.type == SystemExit
    assert error.value.code == 0
