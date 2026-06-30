import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

extensions = [
    'sphinx.ext.mathjax',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = u'otfftw'
copyright = u'2009-2013, EDF-EADS-Phimeca'

version = '0.10'
release = '0.10'

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = 'friendly'

sys.path.append(os.path.join(os.path.dirname(__file__), 'themes'))
html_theme = 'openturns'
html_theme_path = [os.path.join(os.path.dirname(__file__), 'themes')]
html_static_path = ['_static']
html_logo = '_static/logo-openturns-wo-bg.png'
html_favicon = '_static/favicon.ico'

html_context = {
    'theme_sidebarwidth': 230,
}

intersphinx_mapping = {
    'openturns': ('http://openturns.github.io/openturns/latest/', 'openturns-objects.inv'),
}

mathjax_config = {
    'TeX': {
        'Macros': {
            'Rset': '\\mathbb{R}',
            'Nset': '\\mathbb{N}',
            'Cset': '\\mathbb{C}',
            'Eset': '\\mathbb{E}',
            'Pset': '\\mathbb{P}',
            'Qset': '\\mathbb{Q}',
            'Zset': '\\mathbb{Z}',
            'vect': ['\\underline{#1}', 1],
            'mat': ['\\underline{\\underline{#1}}', 1],
            'Tr': ['{#1}^t', 1],
        }
    }
}
