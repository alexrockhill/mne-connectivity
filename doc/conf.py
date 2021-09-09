"""Configure details for documentation with sphinx."""
from datetime import date
import os
import sys
import warnings

import sphinx_gallery  # noqa: F401
from sphinx_gallery.sorting import ExampleTitleSortKey

import mne
sys.path.insert(0, os.path.abspath(".."))
import mne_connectivity  # noqa: E402

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
curdir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(curdir, '..')))
sys.path.append(os.path.abspath(os.path.join(curdir, '..', 'mne_connectivity')))
sys.path.append(os.path.abspath(os.path.join(curdir, 'sphinxext')))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
needs_sphinx = '4.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx_autodoc_typehints',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx_gallery.gen_gallery',
    'sphinxcontrib.bibtex',
    'numpydoc',
    'sphinx_copybutton',
    'gh_substitutions',  # custom extension, see sphinxext/gh_substitutions.py
]

# configure sphinx-copybutton
copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True

# generate autosummary even if no references
# -- sphinx.ext.autosummary
autosummary_generate = True

autodoc_default_options = {'inherited-members': None}
autodoc_typehints = 'signature'

# prevent jupyter notebooks from being run even if empty cell
# nbsphinx_execute = 'never'
# nbsphinx_allow_errors = True

# -- numpydoc
# Below is needed to prevent errors
numpydoc_class_members_toctree = False
numpydoc_attributes_as_param_list = True
numpydoc_use_blockquotes = True

default_role = 'py:obj'

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'MNE-Connectivity'
td = date.today()
copyright = u'2021-%s, MNE Developers. Last updated on %s' % (td.year,
                                                              td.isoformat())

author = u'Adam Li'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = mne_connectivity.__version__
# The full version, including alpha/beta/rc tags.
release = version

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', "**.ipynb_checkpoints"]

# HTML options (e.g., theme)
# see: https://sphinx-bootstrap-theme.readthedocs.io/en/latest/README.html
# Clean up sidebar: Do not show "Source" link
html_show_sourcelink = False
html_copy_source = False

html_theme = 'pydata_sphinx_theme'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
html_static_path = ['_static']
html_css_files = ['style.css']

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    'icon_links': [
        dict(name='GitHub',
             url='https://github.com/mne-tools/mne-connectivity',
             icon='fab fa-github-square'),
    ],
    'use_edit_page_button': False,
    'navigation_with_keys': False,
    'show_toc_level': 1,
    'navbar_end': ['version-switcher', 'navbar-icon-links'],
}
# Custom sidebar templates, maps document names to template names.
html_sidebars = {
    'index': ['search-field.html'],
}

html_context = {
    'versions_dropdown': {
        'dev': 'v0.3 (devel)',
        'stable': 'v0.2 (stable)',
        'v0.1': 'v0.1',
    },
}

# html_sidebars = {'**': ['localtoc.html']}

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'mne': ('https://mne.tools/dev', None),
    'mne-bids': ('https://mne.tools/mne-bids/dev/', None),
    'numpy': ('https://numpy.org/devdocs', None),
    'scipy': ('https://scipy.github.io/devdocs', None),
    'matplotlib': ('https://matplotlib.org', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/dev', None),
    'sklearn': ('https://scikit-learn.org/stable', None),
    'pyvista': ('https://docs.pyvista.org', None),
    'joblib': ('https://joblib.readthedocs.io/en/latest', None),
    'nibabel': ('https://nipy.org/nibabel', None),
    'nilearn': ('http://nilearn.github.io', None),
}
intersphinx_timeout = 5

# Resolve binder filepath_prefix. From the docs:
# "A prefix to append to the filepath in the Binder links. You should use this
# if you will store your built documentation in a sub-folder of a repository,
# instead of in the root."
# we will store dev docs in a `dev` subdirectory and all other docs in a
# directory "v" + version_str. E.g., "v0.3"
if 'dev' in version:
    filepath_prefix = 'dev'
else:
    filepath_prefix = 'v{}'.format(version)

os.environ['_MNE_BUILDING_DOC'] = 'true'
scrapers = ('matplotlib',)
try:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        import pyvista
    pyvista.OFF_SCREEN = False
except Exception:
    pass
else:
    scrapers += ('pyvista',)
if 'pyvista' in scrapers:
    brain_scraper = mne.viz._brain._BrainScraper()
    scrapers = list(scrapers)
    scrapers.insert(scrapers.index('pyvista'), brain_scraper)
    scrapers = tuple(scrapers)

sphinx_gallery_conf = {
    'doc_module': 'mne_connectivity',
    'reference_url': {
        'mne_connectivity': None,
    },
    'backreferences_dir': 'generated',
    'plot_gallery': 'True',  # Avoid annoying Unicode/bool default warning
    'within_subsection_order': ExampleTitleSortKey,
    'examples_dirs': ['../examples'],
    'gallery_dirs': ['auto_examples'],
    'filename_pattern': '^((?!sgskip).)*$',
    'matplotlib_animations': True,
    'compress_images': ('images', 'thumbnails'),
    'image_scrapers': scrapers,
}

# sphinxcontrib-bibtex
bibtex_bibfiles = ['./references.bib']
bibtex_style = 'unsrt'
bibtex_footbibliography_header = ''


# Enable nitpicky mode - which ensures that all references in the docs
# resolve.

nitpicky = True
nitpick_ignore = []
