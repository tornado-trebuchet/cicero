# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Cicero'
copyright = '2025, JaneenDaredevil'
author = 'JaneenDaredevil'
release = '0.0.69'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',        # Auto import docstrings
    'sphinx.ext.napoleon',       # Google/Numpy-style docstrings
    'sphinx.ext.viewcode',       # Adds links to source code
    'myst_parser',               # Markdown support
    'sphinx_autodoc_typehints',  # Type hint support
]

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
    'inherited-members': True,
}

templates_path = ['_templates']
exclude_patterns = []

import os
import sys
# Add both the root directory and src to Python path
sys.path.insert(0, os.path.abspath(os.path.join('..', '..')))  # Root directory
sys.path.insert(0, os.path.abspath(os.path.join('..', '..', 'src')))  # src directory

# Mock imports for problematic dependencies that might not be available during doc build
autodoc_mock_imports = [
    'torch',
    'spacy',
    'gensim',
    'bertopic',
    'umap',
    'hdbscan',
    'sentence_transformers',
    'sklearn',
    'pandas',
    'numpy',
    'sqlalchemy',
    'psycopg2',
    'fastapi',
    'uvicorn',
    'requests',
]



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
