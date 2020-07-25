# -*- coding: utf-8 -*-
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
#sys.path.insert(0, os.path.abspath('.'))
#sys.path.insert(0, os.path.abspath('../'))
#
here = os.path.abspath(os.path.dirname(__file__))
d = os.path.abspath(os.path.join(here, '..', 'marketdata'))
print('here={:s}'.format(here))
print('d={:s}'.format(d))
sys.path.insert(0, d)
#here = os.path.abspath(os.path.dirname(__file__))
#d = os.path.abspath(os.path.join(here, '..', 'marketdata', 'ISO3166MIC'))
#print('here={:s}'.format(here))
#print('d={:s}'.format(d))
#sys.path.insert(0, d)


# -- Project information -----------------------------------------------------

project = 'marketdata'
copyright = '2020, Peter Dahl Vestergaard'
author = 'Peter Dahl Vestergaard'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]
#
# Document Python Code
#
use_module = 'autoapi'

if use_module == 'autodoc':
    #
    # Using autodoc
    # https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
    extensions.append('sphinx.ext.autodoc')
elif use_module == 'autoapi':
    #
    # Using autoapi
    # https://sphinx-autoapi.readthedocs.io/en/latest/
    extensions.append('autoapi.extension')
    autoapi_type = 'python'
    autoapi_dirs = []
    autoapi_dirs.append('../marketdata')
    # autoapi_dirs.append('../marketdata/iso10383mic')
#
# Support for NumPy and Google style docstrings
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
extensions.append('sphinx.ext.napoleon')
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
