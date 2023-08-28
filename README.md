# arrangio

Arranges a set of songs in groups with similar total play time.

## Synopsis

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
                        song information (e.g.: song01:00h03m27s) (default: None)
  -v, --version         show program's version number and exit
```

## Build (from source)

[just](https://just.systems) is used to automate several steps of the
development process.

All of the commands described bellow are to be executed on the root folder
of this project.

A development environment can be created using the following command:

```shell
just init
```

To build a Python package for this library use the following command:

```shell
just build
```

After this you should have a wheel file (`*.whl`) inside a folder called
`dist`.

The library can be install using the wheel file and pip3:

```shell
pip3 --quiet install dist/arrangio-*.whl
```

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

Please read the [CONTRIBUTING.md](https://github.com/electric-mass/arrangio/blob/master/CONTRIBUTING.md)
file for more details on how to contribute to this project.

## Versioning

This project uses [SemVer](http://semver.org/) for versioning. For the versions
available, see the [tags on this repository](https://github.com/electric-mass/arrangio/tags).

## Authors

* **Frederico Martins** - [fscm](https://github.com/fscm)

See also the list of [contributors](https://github.com/electric-mass/arrangio/contributors)
who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/electric-mass/arrangio/blob/master/LICENSE)
file for details
