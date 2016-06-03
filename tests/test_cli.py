# -*- coding: utf-8 -*-
#
# This file is part of DoSchema.
# Copyright (C) 2016 CERN.
#
# DoSchema is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# DoSchema is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DoSchema; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

import os

from click.testing import CliRunner

from doschema.cli import validate


def test_repetition():
    """Test that adding field with the same type returns
    with zero exit code."""
    runner = CliRunner()
    schemas = ['jsonschema_f1.json', 'jsonschema_f2.json']
    current_dir = os.getcwd()

    def data_path(filename):
        return os.path.join(current_dir, 'tests', 'data_files', filename)

    result = runner.invoke(
        validate, [data_path(filename) for filename in schemas])
    assert result.exit_code == 0


def test_difference():
    """Test that adding field with different type returns
    with non-zero exit code."""
    runner = CliRunner()
    schemas = ['jsonschema_f2.json', 'jsonschema_f3.json']
    current_dir = os.getcwd()

    def data_path(filename):
        return os.path.join(current_dir, 'tests', 'data_files', filename)

    result = runner.invoke(
        validate, [data_path(filename) for filename in schemas])
    assert result.exit_code != 0


def test_ref():
    """Test that references works."""
    runner = CliRunner()
    schemas = ['jsonschema_f4.json', 'jsonschema_f5.json']
    current_dir = os.getcwd()

    def data_path(filename):
        return os.path.join(current_dir, 'tests', 'data_files', filename)

    result = runner.invoke(
        validate, [data_path(filename) for filename in schemas])
    assert result.exit_code != 0


def test_ignoring_indexes():
    """Test that with no option "--ignore_index" option  is set."""
    runner = CliRunner()
    schemas = ['jsonschema_f6.json']
    current_dir = os.getcwd()

    def data_path(filename):
        return os.path.join(current_dir, 'tests', 'data_files', filename)

    result = runner.invoke(
        validate, [data_path(filename) for filename in schemas])
    assert result.exit_code != 0


def test_not_ignoring_indexes():
    """Test that "--with_index" option references works."""
    runner = CliRunner()
    current_dir = os.getcwd()

    def data_path(filename):
        return os.path.join(current_dir, 'tests', 'data_files', filename)

    result = runner.invoke(
        validate, [data_path('jsonschema_f6.json'), '--with_index'])
    assert result.exit_code == 0
