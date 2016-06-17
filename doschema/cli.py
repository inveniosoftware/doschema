# -*- coding: utf-8 -*-
#
# This file is part of DoMapping.
# Copyright (C) 2015, 2016 CERN.
#
# DoMapping is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# DoMapping is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DoMapping; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""CLI commands."""

import json
import os
from io import open

import chardet
import click

import doschema.validation
from doschema.errors import EncodingError


@click.group()
def cli():
    """CLI group."""
    pass  # pragma: no cover


@cli.command()
@click.argument('schemas',
                type=click.Path(
                    exists=True, file_okay=True, dir_okay=False
                ),
                nargs=-1)
@click.option('--ignore_index/--with_index',
              default=True, help='Disable ignoring array indexes')
def validate(schemas, ignore_index):
    """Main function for cli."""
    schema_validator = doschema.validation.JSONSchemaValidator(
        ignore_index)
    for schema in schemas:
        path = os.path.join(os.getcwd(), 'tests', 'data_files', schema)
        with open(path, 'rb') as infile:
            byte_file = infile.read()
            encoding = chardet.detect(byte_file)['encoding']
            if encoding in ['UTF-16BE', 'UTF-16LE']:
                encoding = 'UTF-16'
            elif encoding in ['UTF-32BE', 'UTF-32LE']:
                encoding = 'UTF-32'
            string_file = byte_file.decode(encoding)
            schema = json.loads(string_file)
            schema_validator.validate(schema, path)
