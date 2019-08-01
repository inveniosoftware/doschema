# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import os

from click.testing import CliRunner

from doschema.cli import validate


def path_helper(filename):
    """Make the path for test files."""
    return os.path.join('.', 'examples', filename)


def test_repetition():
    """Test that adding field with the same type passes."""
    runner = CliRunner()
    schemas = [
        'jsonschema_for_repetition.json',
        'jsonschema_repetition.json'
    ]

    files = [path_helper(filename) for filename in schemas]
    result = runner.invoke(validate, files)

    assert result.exit_code == 0


def test_difference():
    """Test that adding field with different type fails."""
    runner = CliRunner()
    schemas = [
        'jsonschema_for_repetition.json',
        'jsonschema_no_repetition.json'
    ]

    files = [path_helper(filename) for filename in schemas]
    result = runner.invoke(validate, files)

    assert result.exit_code == 1


def test_ref():
    """Test that references works."""
    runner = CliRunner()
    schemas = ['jsonschema_ref.json', 'jsonschema_other_ref.json']

    files = [path_helper(filename) for filename in schemas]
    result = runner.invoke(validate, files)

    assert result.exit_code == 1


def test_ignore_option():
    """Test that with no option "--ignore_index" option  is set."""
    runner = CliRunner()
    schemas = ['jsonschema_ignore_index_option.json']

    files = [path_helper(filename) for filename in schemas]
    result = runner.invoke(validate, files)

    assert result.exit_code == 0


def test_with_option():
    """Test that "--with_index" option references works."""
    runner = CliRunner()
    schemas = ['jsonschema_with_index_option.json']

    files = [path_helper(filename) for filename in schemas]
    files.append('--with_index')
    result = runner.invoke(validate, files)
    assert result.exit_code == 0
