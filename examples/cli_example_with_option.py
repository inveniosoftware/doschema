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


"""In this example, with_index option is enabled.
Thus, types in arrays will be checked with their indexes and items of the same
array can have different types.

Run this example:
.. code-block:: console
    $ cd examples
    $ python app.py
The same result could be created with the cli:
.. code-block:: console
    $ doschema file1.json file2.json --with_index
"""

import json
import os
from io import open

import chardet
import click

import doschema.validation

schemas = ['jsonschema_f1.json', 'jsonschema_f2.json']

schema_validator = doschema.validation.JSONSchemaValidator(ignore_index=False)
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
