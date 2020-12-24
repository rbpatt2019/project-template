# -*- coding: utf-8 -*-
"""Sphinx configuration"""
import os
import sys

import sphinx_rtd_theme  # pylint: disable=unused-import

sys.path.insert(0, os.path.abspath("../"))
sys.path.insert(0, os.path.abspath("../tests/"))
sys.path.insert(0, os.path.abspath("../src/"))

project = "project-template"
author = "Ryan B Patterson-Cross"
copyright = f"2020, {author}"  # pylint: disable=redefined-builtin
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx_rtd_theme"]

napoleon_google_docstrings = False
napoleon_numpy_docstrings = True
napoleon_use_param = False

html_theme = "sphinx_rtd_theme"
