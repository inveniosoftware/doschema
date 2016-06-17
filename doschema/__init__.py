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

"""JSON Schema utility functions and commands.

Compatibility Validation
-------------------------

It validates compatibility between different JSON schemas versions.

A schema is backward compatible if the fields' type remain the same in all
JSON schemas declaring it and JSON schemas are type consistent within
themselves too.

>>> import json
>>> import os
>>> from io import open
>>>
>>> import chardet
>>> import click
>>>
>>> import doschema.validation
>>>
>>> schemas = ['jsonschema_f1.json', 'jsonschema_f2.json']
>>>
>>> schema_validator = doschema.validation.JSONSchemaValidator()
>>> for schema in schemas:
...     path = os.path.join(os.getcwd(), 'tests', 'data_files', schema)
...     with open(path, 'rb') as infile:
...         byte_file = infile.read()
...         encoding = chardet.detect(byte_file)['encoding']
...         if encoding in ['UTF-16BE', 'UTF-16LE']:
...             encoding = 'UTF-16'
...         elif encoding in ['UTF-32BE', 'UTF-32LE']:
...             encoding = 'UTF-32'
...         string_file = byte_file.decode(encoding)
...         schema = json.loads(string_file)
...         schema_validator.validate(schema, path)

By default the index of "array" "items" are ignored. Thus all the values of
an array should have the same type in order to be compatible.
This behavior can be disabled by setting "ignore_index = False" in the
validator's constructor.

>>> import json
>>> import os
>>> from io import open
>>>
>>> import chardet
>>> import click
>>>
>>> import doschema.validation
>>>
>>> schemas = ['jsonschema_f1.json', 'jsonschema_f2.json']
>>>
>>> schema_validator = doschema.validation.JSONSchemaValidator(
...     ignore_index = False
... )
>>> for schema in schemas:
...     path = os.path.join(os.getcwd(), 'tests', 'data_files', schema)
...     with open(path, 'rb') as infile:
...         byte_file = infile.read()
...         encoding = chardet.detect(byte_file)['encoding']
...         if encoding in ['UTF-16BE', 'UTF-16LE']:
...             encoding = 'UTF-16'
...         elif encoding in ['UTF-32BE', 'UTF-32LE']:
...             encoding = 'UTF-32'
...         string_file = byte_file.decode(encoding)
...         schema = json.loads(string_file)
...         schema_validator.validate(schema, path)

CLI usage
--------------
.. code-block:: console

    $ doschema file1.json file2.json
    $ doschema file1.json file2.json --with_index

"""

from __future__ import absolute_import, print_function

from .version import __version__

__all__ = ('__version__')
