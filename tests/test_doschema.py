# SPDX-FileCopyrightText: 2016 CERN.
# SPDX-License-Identifier: MIT

"""Module tests."""

from __future__ import absolute_import, print_function


def test_version():
    """Test version import."""
    from doschema import __version__
    assert __version__
