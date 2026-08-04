# SPDX-FileCopyrightText: 2016 CERN.
# SPDX-License-Identifier: MIT

"""In this example, there is no option set, so by default
"--ignore_index" option is enabled.
Thus array indexes are ignored and for each array field, all items have to be
of the same type.

Run this example:
.. code-block:: console
    $ cd examples
    $ python app.py
The same result could be created with the cli:
.. code-block:: console
    $ doschema file1.json file2.json
"""

import json
from io import open

import doschema.validation
from doschema.utils import detect_encoding

schemas = [
    './examples/jsonschema_ignore_index_option.json'
]

schema_validator = doschema.validation.JSONSchemaValidator()
for schema in schemas:
    with open(schema, 'rb') as infile:
        byte_file = infile.read()
        encoding = detect_encoding(byte_file)
        string_file = byte_file.decode(encoding)
        json_schema = json.loads(string_file)
        schema_validator.validate(json_schema, schema)
