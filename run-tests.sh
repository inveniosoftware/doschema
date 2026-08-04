# SPDX-FileCopyrightText: 2016 CERN.
# SPDX-License-Identifier: MIT

pydocstyle doschema && \
isort -rc -c -df **/*.py && \
sphinx-build -qnNW docs docs/_build/html && \
pytest && \
sphinx-build -qnNW -b doctest docs docs/_build/doctest
