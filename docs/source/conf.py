# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
import os
import datetime

sys.path.insert(0, os.path.abspath('../src'))

project = 'Parasite'
copyright = f'2024-{datetime.date.today().year}, Hendrik Boeck <hendrikboeck.dev@protonmail.com>'
author = 'Hendrik Boeck <hendrikboeck.dev@protonmail.com>'
release = 'v0.1.4'
html_title = f"{project} {release}"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    'qiskit_sphinx_theme',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = 'qiskit-ecosystem'
html_static_path = ['_static']
html_logo = "_static/parasite-logo.png"

html_theme_options = {
    "disable_ecosystem_logo": False,
}

# ----------------------------------------------------------------------------------
# Autodoc
# ----------------------------------------------------------------------------------

# Note that setting autodoc defaults here may not have as much of an effect as you may expect; any
# documentation created by autosummary uses a template file (in autosummary in the templates path),
# which likely overrides the autodoc defaults.

# Move type hints from signatures to the parameter descriptions (except in overload cases, where
# that's not possible).
# autodoc_typehints = "description"
# Only add type hints from signature to description body if the parameter has documentation.  The
# return type is always added to the description (if in the signature).
# autodoc_typehints_description_target = "documented_params"

autoclass_content = "both"

# autosummary_generate = True
# autosummary_generate_overwrite = False

# We only use Google-style docstrings, and allowing Napoleon to parse Numpy-style docstrings both
# slows down the build (a little) and can sometimes result in _regular_ section headings in
# module-level documentation being converted into surprising things.
napoleon_google_docstring = True
napoleon_numpy_docstring = False
