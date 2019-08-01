# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""CLI commands."""

import json
from io import open

import click

import doschema.validation
from doschema.errors import JSONSchemaCompatibilityError
from doschema.utils import detect_encoding


@click.group()
def cli():
    """CLI group."""
    pass  # pragma: no cover


@cli.command()
@click.argument(
    'schemas',
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True
    ),
    nargs=-1
)
@click.option(
    '--ignore_index/--with_index',
    default=True,
    help="Enable/Disable conflict detection between different indices of "
    "array fields in JSON-Schemas. Enabled by default."
)
def validate(schemas, ignore_index):
    """Validate the schemas."""
    try:
        schema_validator = doschema.validation.JSONSchemaValidator(
            ignore_index)
        for schema in schemas:
            with open(schema, 'rb') as infile:
                byte_file = infile.read()
                encoding = detect_encoding(byte_file)
                string_file = byte_file.decode(encoding)
                json_schema = json.loads(string_file)
                schema_validator.validate(json_schema, schema)
    except JSONSchemaCompatibilityError as e:
        raise click.ClickException(str(e))
