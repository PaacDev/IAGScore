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
sys.path.insert(0, os.path.abspath('../..')) 

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iagscore.settings')
django.setup()

project = 'iagscore'
copyright = '2025, Pedro Antonio Abellaneda Canales'
author = 'Pedro Antonio Abellaneda Canales'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',  # Genera resúmenes automáticos de la documentación
    'sphinx.ext.coverage',  # Genera informes de cobertura
    'sphinx.ext.doctest',  # Ejecuta ejemplos de código en la documentación
    'sphinx.ext.inheritance_diagram',  # Genera diagramas de herencia
    'sphinx.ext.napoleon',  # Para docstrings estilo Google/NumPy
    'sphinx.ext.viewcode',  # Enlaces al código fuente
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'es'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
# -- Tutorial for sphinx_book_theme -------------------------------------------------
#https://sphinx-book-theme.readthedocs.io/en/latest/tutorials/get-started.html

html_theme = 'sphinx_book_theme'
html_theme_options = {
    "repository_provider": "github",
    "repository_url": "https://github.com/pac1006/IAGScore",
    "use_repository_button": True,
}
html_static_path = ['_static']
