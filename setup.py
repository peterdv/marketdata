#!/usr/bin/env python
# -*- coding: utf-8; mode: python-mode; -*-

"""Set Up for `pytest`

See:

* https://docs.pytest.org/en/stable/goodpractices.html#test-discovery
* https://github.com/willprice/pytest-coverage-examples

"""

from setuptools import setup, find_packages
from glob import glob
from os.path import basename
# from os.path import dirname
# from os.path import join
from os.path import splitext

setup(
    name='marketdata',
    package_dir={'': 'marketdata'},
    packages=find_packages(where='src', exclude=('tests',)),
    py_modules=[splitext(basename(path))[0] for path in glob('marketdata/*.py')],
)
