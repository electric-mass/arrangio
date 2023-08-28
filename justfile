#!/usr/bin/env -S just --justfile
# -*- coding: UTF-8 -*-
#
# copyright: 2023, Electric Mass Records
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

PROJECT_DIR := absolute_path(justfile_directory())
PACKAGE_NAME := file_name(PROJECT_DIR)
DOCS_DIR := join(PROJECT_DIR, 'docs')
SOURCE_DIR := join(PROJECT_DIR, 'src')
VENV_DIR := join(PROJECT_DIR, '.venv')
VENV_BIN_DIR := join(VENV_DIR, 'bin')
__PYPROJECT_TOML__ := join(PROJECT_DIR, 'pyproject.toml')
__PYVENV_CFG__ := join(VENV_DIR, 'pyvenv.cfg')

BUILD_ARTIFACTS := 'build dist src/*.egg-info'
CACHE_ITEMS := '.mypy_cache .pytest_cache .coverage* .ruff_cache'

AUTOPEP := 'autopep8'
LINT := 'ruff'
PDOC := 'pdoc3'
PYLINT := 'pylint'
PYTEST := 'pytest'
PYTHON := 'python3'
STUBGEN := 'stubgen'
TWINE := 'twine'
VERMIN := 'vermin'

FIND := 'find'
MV := 'mv'
RM := 'rm -rf'

AUTOPEP_ARGS := '--aggressive --aggressive --recursive'
LINT_ARGS := 'check --exit-zero'
PDOC_ARGS := '--force --html --skip-errors'
PIP_ARGS := '--quiet --upgrade --editable'
PYLINT_ARGS := '--exit-zero'
PYTEST_ARGS := '--quiet --no-header --color=auto --code-highlight=yes'
PYTEST_DOC_ARGS := '--doctest-modules --doctest-continue-on-failure --suppress-no-test-exit-code'
STUBGEN_ARGS := '--quiet --export-less'
VERMIN_ARGS := '--no-tips --eval-annotations --no-parse-comments'

[private]
default: help

# Creates the library package(s).
build: build-clean
    # Building package(s)...
    @'{{join(VENV_BIN_DIR, PYTHON)}}' -m build '{{PROJECT_DIR}}'

# Cleans the build artifacts.
[private]
build-clean:
    # Cleaning build artifacts...
    @for artifact in {{BUILD_ARTIFACTS}}; do \
        {{RM}} "{{join(PROJECT_DIR, '$artifact')}}"; \
    done

# Cleans the project caches.
[private]
cache-clean:
    # Cleaning caches...
    @for file in {{CACHE_ITEMS}}; do \
        {{RM}} "{{join(PROJECT_DIR, '$file')}}"; \
    done
    @{{FIND}} '{{PROJECT_DIR}}' -mindepth 1 -type f -name "*.py[co]" -delete \
        -o -type d -name "__pycache__" -delete

# Cleans the project caches and builds.
clean: build-clean cache-clean

# Cleans everything.
clean-all: clean init-clean

# Creates the project documentation.
docs: docs-clean
    # Checking documentation examples...
    @'{{join(VENV_BIN_DIR, PYTEST)}}' {{PYTEST_ARGS}} {{PYTEST_DOC_ARGS}} \
        --rootdir='{{PROJECT_DIR}}' '{{join(SOURCE_DIR, PACKAGE_NAME)}}'
    # Generating documentation...
    @'{{join(VENV_BIN_DIR, PDOC)}}' {{PDOC_ARGS}} \
        --template-dir '{{join(SOURCE_DIR, "docs", "templates")}}' \
        --output-dir '{{DOCS_DIR}}' '{{join(SOURCE_DIR, PACKAGE_NAME)}}'
    @{{MV}} '{{join(DOCS_DIR, PACKAGE_NAME)}}'/* '{{DOCS_DIR}}'
    @{{RM}} '{{join(DOCS_DIR, PACKAGE_NAME)}}'

# Cleans the documentation folder.
[private]
docs-clean:
    # Cleaning documentation...
    @{{FIND}} '{{DOCS_DIR}}' -mindepth 1 -type f -not -name '.*' -delete \
        -o -type d -delete

# Formats the code.
format:
    # Formating code...
    @'{{join(VENV_BIN_DIR, AUTOPEP)}}' {{AUTOPEP_ARGS}} --in-place \
        '{{join(SOURCE_DIR, PACKAGE_NAME)}}'

# Shows the required code formats.
format-show:
    # Getting required code formats...
    @'{{join(VENV_BIN_DIR, AUTOPEP)}}' {{AUTOPEP_ARGS}} \
        --diff '{{join(SOURCE_DIR, PACKAGE_NAME)}}'

# Shows this help message.
help:
    @just --list

# (Re)Creates the development environment.
init: init-clean && init-show
    # Creating the venv...
    @{{PYTHON}} -m venv --upgrade-deps '{{VENV_DIR}}'
    # Instaling project requirements...
    @'{{join(VENV_BIN_DIR, PYTHON)}}' -m pip install {{PIP_ARGS}} \
        '{{PROJECT_DIR}}'[dev]

# Cleans the venv.
[private]
init-clean _active=env_var_or_default('VIRTUAL_ENV', ''):
    # Deleting the venv...
    @{{RM}} '{{VENV_DIR}}'/*
    {{ if _active != "" { '# !! Python venv active. Deactivate it using the command "deactivate".' } else { '' } }}

# Shows venv info
init-show:
    # Getting venv information...
    @echo 'VIRTUAL_ENV="{{VENV_DIR}}"'
    @'{{join(VENV_BIN_DIR, PYTHON)}}' \
        -c "import sys; print(f'Python ' + sys.version.replace('\n',''))"
    @'{{join(VENV_BIN_DIR, PYTHON)}}' -m pip --version

# Checks the project for code smells.
lint:
    # Checking the code...
    @'{{join(VENV_BIN_DIR, LINT)}}' {{LINT_ARGS}} \
        '{{join(SOURCE_DIR, PACKAGE_NAME)}}'

# Calculates python minimum version required.
pyversion:
    #Finding minimum Python version...
    @'{{join(VENV_BIN_DIR, VERMIN)}}' {{VERMIN_ARGS}} \
        '{{join(SOURCE_DIR, PACKAGE_NAME)}}'

# Uploads the project to 'pypi.org'.
publish: build
    # Publishing to 'pypi.org'...
    @'{{join(VENV_BIN_DIR, TWINE)}}' upload '{{join(PROJECT_DIR, "dist")}}'/*

# Uploads the project to 'test.pypi.org'.
publish-test: build
    # Publishing to 'test.pypi.org'...
    @'{{join(VENV_BIN_DIR, TWINE)}}' upload --repository testpypi \
        '{{join(PROJECT_DIR, "dist")}}'/*

# Checks the project for code smells.
pylint:
    # Checking the code...
    @'{{join(VENV_BIN_DIR, PYLINT)}}' {{PYLINT_ARGS}} \
        '{{join(SOURCE_DIR, PACKAGE_NAME)}}'

# Generates stubs for the project.
stubs: stubs-clean
    # Generating stubs...
    @'{{join(VENV_BIN_DIR, STUBGEN)}}' {{STUBGEN_ARGS}} \
        --package {{PACKAGE_NAME}} --search-path '{{SOURCE_DIR}}' \
        --output '{{SOURCE_DIR}}'

# Deletes the stubs.
[private]
stubs-clean:
    # Deleting stubs...
    @{{FIND}} '{{join(SOURCE_DIR, PACKAGE_NAME)}}' -mindepth 1 -type f \
        -name "*.pyi" -delete

# Runs the tests.
tests:
    # Running tests...
    @'{{join(VENV_BIN_DIR, PYTEST)}}' {{PYTEST_ARGS}} --cov={{PACKAGE_NAME}} \
        --rootdir='{{PROJECT_DIR}}'
