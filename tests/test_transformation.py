# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import os

import jsonschema
import pytest

from doschema.transform import resolve_references


def test_ref_no_array_pass():
    v1 = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "definitions": {
            "address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "string"}
                }
            }
        },

        "type": "object",

        "properties": {
            "billing_address": {"$ref": "#/definitions/address"},
            "shipping_address": {"$ref": "#/definitions/address"}
        }
    }
    expected = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "definitions": {
            "address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "string"}
                }
            }
        },

        "type": "object",

        "properties": {
            "billing_address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "string"}
                }
            },
            "shipping_address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "string"}
                }
            }
        }
    }
    result = resolve_references(v1)
    assert expected == result


def test_ref_no_conflict_inside_schema_pass():
    """Test that having no conflict in schema with references passes."""
    v1 = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "definitions": {
            "address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "string"}
                }
            }
        },

        "type": "object",

        "properties": {
            "billing_address": {"$ref": "#/definitions/address"},
            "shipping_address": {
                "allOf": [
                    {"$ref": "#/definitions/address"},
                    {
                        "properties":   {
                            "type": {"enum": ["residential", "business"]}
                        }
                    }
                ]
            }
        }
    }
    expected = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "definitions": {
            "address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "string"}
                }
            }
        },

        "type": "object",

        "properties": {
            "billing_address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "string"}
                }
            },
            "shipping_address": {
                "allOf": [
                    {
                        "type": "object",
                        "properties": {
                            "street_address": {"type": "string"}
                        }
                    },
                    {
                        "properties": {
                            "type": {"enum": ["residential", "business"]}
                        }
                    }
                ]
            }
        }
    }
    result = resolve_references(v1)
    assert expected == result


def test_ref_conflict_inside_schema():
    """Test that having an invalid reference in the schema raises
    RefResolutionError."""
    v1 = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "type": "object",

        "properties": {
            "billing_address": {"$ref": "#/definitions/differentaddress"},
        }
    }
    with pytest.raises(jsonschema.exceptions.RefResolutionError):
        resolve_references(v1)


def test_ref_outside_schema():
    """Test that having a reference to schema in different file passes."""
    v1 = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "definitions": {
            "address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "string"}
                }
            }
        },

        "type": "object",

        "properties": {
            "billing_address": {
                "$ref": "test_outside.json#/definitions/address"

            },
            "shipping_address": {
                "allOf": [
                    {"$ref": "#/definitions/address"},
                    {
                        "properties":   {
                            "type": {"enum": ["residential", "business"]}
                        }
                    }
                ]
            }
        }
    }
    expected = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "definitions": {
            "address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "string"}
                }
            }
        },

        "type": "object",

        "properties": {
            "billing_address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "differenttype"}
                }
            },
            "shipping_address": {
                "allOf": [
                    {
                        "type": "object",
                        "properties": {
                            "street_address": {"type": "string"}
                        }
                    },
                    {
                        "properties":   {
                            "type": {"enum": ["residential", "business"]}
                        }
                    }
                ]
            }
        }
    }
    result = resolve_references(
        v1,
        'file://' + os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test_outside',
            'test_outside'
        )
    )
    assert expected == result


def test_internal_resolving():
    """Test internal resolving passes."""
    v1 = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "definitions": {
            "^[a-zA-Z0-9]+$": {"type": "string"}
        },

        "type": "object",

        "properties": {
            "^[a-zA-Z]+$": {"$ref": "#/definitions"}
        }
    }
    expected = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "definitions": {
            "^[a-zA-Z0-9]+$": {"type": "string"}
        },

        "type": "object",

        "properties": {
            "^[a-zA-Z]+$": {
                "^[a-zA-Z0-9]+$": {"type": "string"}
            }
        }
    }
    result = resolve_references(v1)
    assert expected == result


def test_in_place_false_option():
    """Test if in_place option set to False not modifies schema."""
    v1 = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "definitions": {
            "address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "string"}
                }
            }
        },

        "type": "object",

        "properties": {
            "billing_address": {"$ref": "#/definitions/address"},
        }
    }
    result = resolve_references(v1, in_place=False)
    assert result is not v1
    assert result != v1


def test_in_place_true_option():
    """Test if in_place option set to True modifies schema."""
    v1 = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "definitions": {
            "address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "string"}
                }
            }
        },

        "type": "object",

        "properties": {
            "billing_address": {"$ref": "#/definitions/address"},
        }
    }
    result = resolve_references(v1, in_place=True)
    assert result is v1
    assert result == v1
