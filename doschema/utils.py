# SPDX-FileCopyrightText: 2016 CERN.
# SPDX-License-Identifier: MIT

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
