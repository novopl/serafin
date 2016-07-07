# -*- coding: utf-8 -*-
import os
project = u'igor-serialize'
copyright = u'2016, Mateusz \'novo\' Klos'
author = u'Mateusz \'novo\' Klos'


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.imgmath',
    'sphinx.ext.viewcode',
]

version = read('VERSION').strip()
release = read('VERSION').strip()
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'README'
language = None
exclude_patterns = ['env', 'tmp', '_build', 'Thumbs.db', '.DS_Store']
todo_include_todos = False
intersphinx_mapping = {'https://docs.python.org/': None}

pygments_style = 'monokai'
html_theme = 'bizstyle'
html_static_path = ['_static']
htmlhelp_basename = 'igor-serializedoc'

latex_elements = {}
latex_documents = [
    (master_doc, 'igor-serialize.tex', u'igor-serialize Documentation',
     u'Mateusz \'novo\' Klos', 'manual'),
]
man_pages = [
    (master_doc, 'igor-serialize', u'igor-serialize Documentation',
     [author], 1)
]
texinfo_documents = [
    (master_doc, 'igor-serialize', u'igor-serialize Documentation',
     author, 'igor-serialize', 'One line description of project.',
     'Miscellaneous'),
]
