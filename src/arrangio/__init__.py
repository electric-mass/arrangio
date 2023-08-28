# -*- coding: UTF-8 -*-
#
# copyright: 2023, Electric Mass Records
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""arrangio.

Arranges a set of songs in groups with similar total play time.

This tool will try to arrange a set of songs into subsets of songs
(groups) whose total play time will be the most sililar possible.

## Prerequisites

Python, version 3.8 or above, needs to be installed on your local
computer.

### Python 3.x

Python version 3.8 or above is required for the tool to work. Python
setup can be found [here](https://www.python.org/downloads/).

## Installation

The simplest way to install this tool is using pip:

```shell
pip3 install arrangio
```

## Usage

A simple example of how to use this tool:

```shell
arrangio --groups 2 --song song01:3m24s --song song02:4m01s  --song song03:1m47s
```

List of all the options:

```shell
usage: arrangio [-h] [-g [NUM]] [-q] -s LABEL:HHhMMmSSs [LABEL:HHhMMmSSs ...] [-v]

options:
  -h, --help            show this help message and exit
  -g [NUM], --groups [NUM]
                        number of groups to create (default: 2)
  -q, --quiet           quiet mode (default: False)
  -s LABEL:HHhMMmSSs [LABEL:HHhMMmSSs ...], --song LABEL:HHhMMmSSs [LABEL:HHhMMmSSs ...]
                        song information (e.g.: label:00h03m27s) (default: None)
  -v, --version         show program's version number and exit
```
"""  # pylint: disable=line-too-long  # noqa: E501,W505

from typing import Final


__all__: Final[tuple] = ()

__author__: Final[str] = 'Electric Mass Records'
__license__: Final[str] = 'MIT'
__project__: Final[str] = __package__
__version__: Final[str] = '0.4.0'
