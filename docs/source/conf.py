# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "KiCadFiles"
copyright = "2025, Steffen-W"
author = "Steffen-W"
release = "1.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.doctest",
    "sphinx.ext.autosummary",
    "sphinx.ext.inheritance_diagram",
]

templates_path = ["_templates"]
exclude_patterns = []

language = "en"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]


# -- Options for autodoc extension -------------------------------------------

autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__,__dict__,__module__",
    "imported-members": False,
}

# Reduce duplicate warnings
autodoc_inherit_docstrings = False

autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"

# -- Options for autosummary extension ---------------------------------------

autosummary_generate = True
autosummary_generate_overwrite = True
autosummary_imported_members = False

# Suppress duplicate warnings by configuring autosummary properly
add_module_names = False

# -- Suppress specific warnings ----------------------------------------------

suppress_warnings = [
    "toc.not_included",  # Suppress autosummary files not in toctree warnings
    "autosummary.import_cycle",  # Suppress autosummary import cycle warnings
    "autodoc.duplicate_object",  # Suppress duplicate object warnings
    "ref.python",  # Suppress cross-reference ambiguity warnings
    "docutils",  # Suppress docstring formatting warnings
]

# -- Options for Napoleon extension ------------------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# -- Options for HTML theme ----------------------------------------------

html_theme_options = {
    "canonical_url": "",
    "analytics_id": "",
    "logo_only": False,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}
