# -*- coding: UTF-8 -*-
#
# copyright: 2023, Electric Mass Records
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Tests for the module entry point."""

import sys
from pytest import mark, raises
from arrangio import __version__, __project__, __main__ as main


@mark.parametrize('args,output,exception,exit_code', [
    ([__project__, '--dummy'], None, SystemExit, 2),
    ([__project__, '--quiet'], None, SystemExit, 2),
    ([__project__, '-s', '0:00:01'], None, SystemExit, 9),
    ([__project__, '--version'], f"{__version__}\n", SystemExit, 0),
    (
        [__project__, '-s', 'song05:5m54s', '-s', 'song03:5m37s', '-s', 'song06:5m16s', '-s', 'song04:4m51s', '-s', 'song08:4m41s', '-s', 'song07:3m45s', '-s', 'song02:3m41s', '-s', 'song09:2m50s', '-s', 'song01:0m55s'],
        "arrangio version 0.1.0\nby Electric Mass Records under MIT license\nDifference (in seconds): 8\nGroups:\n  [1] 0:18:49 ['song01 (0:00:55)', 'song02 (0:03:41)', 'song07 (0:03:45)', 'song04 (0:04:51)', 'song03 (0:05:37)']\n  [2] 0:18:41 ['song09 (0:02:50)', 'song08 (0:04:41)', 'song06 (0:05:16)', 'song05 (0:05:54)']\n",
        None,
        0
    ),
    (
        [__project__, '-s', 'song05:5m54s', '-s', 'song03:5m37s', '-s', 'song06:5m16s', '-s', 'song04:4m51s', '-s', 'song08:4m41s', '-s', 'song07:3m45s', '-s', 'song02:3m41s', '-s', 'song09:2m50s', '-s', 'song01:0m55s', '-g', '2'],
        "arrangio version 0.1.0\nby Electric Mass Records under MIT license\nDifference (in seconds): 8\nGroups:\n  [1] 0:18:49 ['song01 (0:00:55)', 'song02 (0:03:41)', 'song07 (0:03:45)', 'song04 (0:04:51)', 'song03 (0:05:37)']\n  [2] 0:18:41 ['song09 (0:02:50)', 'song08 (0:04:41)', 'song06 (0:05:16)', 'song05 (0:05:54)']\n",
        None,
        0
    ),
    (
        [__project__, '-s', 'song05:5m54s', '-s', 'song03:5m37s', '-s', 'song06:5m16s', '-s', 'song04:4m51s', '-s', 'song08:4m41s', '-s', 'song07:3m45s', '-s', 'song02:3m41s', '-s', 'song09:2m50s', '-s', 'song01:0m55s', '-g', '3'],
        "arrangio version 0.1.0\nby Electric Mass Records under MIT license\nDifference (in seconds): 20\nGroups:\n  [1] 0:12:26 ['song01 (0:00:55)', 'song03 (0:05:37)', 'song05 (0:05:54)']\n  [2] 0:12:22 ['song09 (0:02:50)', 'song08 (0:04:41)', 'song04 (0:04:51)']\n  [3] 0:12:42 ['song02 (0:03:41)', 'song07 (0:03:45)', 'song06 (0:05:16)']\n",
        None,
        0
    ),
    (
        [__project__, '--quiet', '-s', 'song05:5m54s', '-s', 'song03:5m37s', '-s', 'song06:5m16s', '-s', 'song04:4m51s', '-s', 'song08:4m41s', '-s', 'song07:3m45s', '-s', 'song02:3m41s', '-s', 'song09:2m50s', '-s', 'song01:0m55s', '-g', '2'],
        "(8, ((1129, ((55, 'song01'), (221, 'song02'), (225, 'song07'), (291, 'song04'), (337, 'song03'))), (1121, ((170, 'song09'), (281, 'song08'), (316, 'song06'), (354, 'song05')))))\n",
        None,
        0
    ),
])
def test___main__(capsys, mocker, args, output, exception, exit_code):
    """test___main__."""
    mocker.patch.object(sys, 'argv', args)
    if exception:
        with raises(exception) as error:
            main.main()
        assert error.type == exception
        assert error.value.code == exit_code
    else:
        main.main()
        stdout, _ = capsys.readouterr()
        assert output == stdout
