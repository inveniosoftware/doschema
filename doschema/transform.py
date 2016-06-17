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

"""Transformation module."""


import jsonschema
import six


class Transform(object):
    """Class for transforming schemas.

    It is assumed that schemas have already been validated for backward
    compatibility before transforming.
    """

    def __init__(self, schema, uri='#', resolver_factory=False):
        """Constructor.

        :param schema: Schema that is currently processed.
        :param resolver_factory: Resolver used to retrieve referenced schemas.
                                 If not provided it will use default.
        """
        self.resolver_factory = resolver_factory or jsonschema.RefResolver
        self.resolver = self.resolver_factory(base_uri=uri, referrer=schema)
        self.schema = schema

    # TODO - dodac test z patternami
    def transform(self, schema=None):
        """Transform schema to a form without references.

        :param schema: Schema that is currently processed.
                       If not provided it will use default.
        """""
        schema = schema or self.schema

        def resolve_ref(ref):
            return self.resolver.resolve(ref)[1]

        if isinstance(schema, dict):
            for key, schema_part in six.iteritems(schema):
                if schema_part:
                    if '$ref' in schema_part:
                        ref = schema_part.pop('$ref', None)
                        schema[key] = resolve_ref(ref)
                self.transform(schema[key])

        elif isinstance(schema, list):
            for curr_index in range(len(schema)):
                schema_part = schema[curr_index]
                if '$ref' in schema_part:
                    ref = schema_part.pop('$ref', None)
                    schema[curr_index] = resolve_ref(ref)
                self.transform(schema_part)

        return schema
