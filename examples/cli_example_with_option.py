# SPDX-FileCopyrightText: 2016 CERN.
# SPDX-License-Identifier: MIT

"""In this example, "with_index" option is enabled.
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
from io import open

import doschema.validation
from doschema.utils import detect_encoding

schemas = [
    './examples/jsonschema_with_index_option.json'
]

schema_validator = doschema.validation.JSONSchemaValidator(ignore_index=False)
for schema in schemas:
    with open(schema, 'rb') as infile:
        byte_file = infile.read()
        encoding = detect_encoding(byte_file)
        string_file = byte_file.decode(encoding)
        json_schema = json.loads(string_file)
        schema_validator.validate(json_schema, schema)
