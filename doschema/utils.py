# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Utils module."""

import chardet


def detect_encoding(byte_file):
    """Detect encoding of a file with schema."""
    encoding = chardet.detect(byte_file)['encoding']
    if encoding in ['UTF-16BE', 'UTF-16LE']:
        encoding = 'UTF-16'
    elif encoding in ['UTF-32BE', 'UTF-32LE']:
        encoding = 'UTF-32'
    return encoding
