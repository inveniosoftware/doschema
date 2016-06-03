# -*- coding: utf-8 -*-
#
# This file is part of DoSchema
# Copyright (C) 2016 CERN.
#
# DoSchema is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Define all DoSchema exceptions."""


class DoSchemaError(Exception):
    """Parent for all DoSchema exceptions.

    .. versionadded:: 1.0.0
    """

    pass


class JSONSchemaCompatibilityError(DoSchemaError):
    """Exception raised when a JSON schema is not backward compatible."""

    def __init__(self, err_msg, schema, prev_schema=None):
        """Constructor."""
        self.prev_schema = prev_schema
        """Index of schema in which field has occured before."""
        self.schema = schema
        """Index of schema in which field occurs now."""
        super(JSONSchemaCompatibilityError, self).__init__(err_msg)
        """Error message."""


class EncodingError(DoSchemaError):
    """Exception raised when file encoding is not compatible."""

    pass
