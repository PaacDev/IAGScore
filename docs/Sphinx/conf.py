# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
import django

# Añadir la ruta del proyecto Django al sys.path
sys.path.insert(0, os.path.abspath("../.."))

# Configuración de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iagscore.settings")
django.setup()

project = "iagscore"
copyright = "2025, Pedro Antonio Abellaneda Canales"
author = "Pedro Antonio Abellaneda Canales"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",  # Soporte para Markdown
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",  # Genera resúmenes automáticos de la documentación
    "sphinx.ext.coverage",  # Genera informes de cobertura
    "sphinx.ext.doctest",  # Ejecuta ejemplos de código en la documentación
    "sphinx.ext.inheritance_diagram",  # Genera diagramas de herencia
    "sphinx.ext.napoleon",  # Para docstrings estilo Google/NumPy
    "sphinx.ext.viewcode",  # Enlaces al código fuente
]


templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

language = "en"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
# -- Tutorial for sphinx_book_theme -------------------------------------------------
# https://sphinx-book-theme.readthedocs.io/en/latest/tutorials/get-started.html

html_theme = "sphinx_book_theme"
html_theme_options = {
    "repository_provider": "github",
    "repository_url": "https://github.com/pac1006/IAGScore",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": True,
    "path_to_docs": "docs",
    "home_page_in_toc": True,
    "show_navbar_depth": 2,
}
html_static_path = ["_static"]

# Extensión de autodoc de Sphinx
autodoc_mock_imports = ["django"]

# Para métodos privados
autodoc_typehints = "description"
autodoc_class_signature = "separated"

# Extensión de coverage de Sphinx
coverage_ignore_functions = ["runserver", "runtest", "test"]
intersphinx_mapping = {
    "rtd": ("https://docs.readthedocs.io/en/stable/", None),
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]
