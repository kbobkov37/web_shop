import os
import sys

# Добавляем корень проекта в путь Python, чтобы Sphinx мог импортировать модули
sys.path.insert(0, os.path.abspath('..'))

project = 'Интернет магазин'
copyright = '2025, Бобков Константин'
author = 'Бобков Константин'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',        # Автогенерация из docstrings
    'sphinx.ext.viewcode',       # Ссылки на исходный код
    'sphinx.ext.napoleon',       # Поддержка Google-style docstrings
    'sphinx.ext.githubpages',    # Для размещения на GitHub Pages
]
# Путь к шаблонам
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'ru'


# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'  # Тема Read the Docs
html_static_path = ['_static']
html_title = "Документация интернет-магазина"

