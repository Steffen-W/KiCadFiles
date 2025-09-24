API Reference
=============

This section provides an overview of all KiCadFiles modules organized by functionality.

For detailed documentation of each module, see :doc:`modules_detailed`.

Core Classes
------------

.. autosummary::

   kicadfiles.base_element.KiCadObject
   kicadfiles.base_element.ParseStrictness

File Format Classes
-------------------

These classes represent complete KiCad file formats and support both ``from_file()`` and ``save_to_file()`` methods:

.. autosummary::

   kicadfiles.board_layout.KicadPcb
   kicadfiles.schematic_system.KicadSch
   kicadfiles.footprint_library.Footprint
   kicadfiles.symbol_library.KicadSymbolLib
   kicadfiles.text_and_documents.KicadWks
   kicadfiles.project_settings.KicadProject
   kicadfiles.design_rules.KiCadDesignRules
   kicadfiles.library_tables.FpLibTable
   kicadfiles.library_tables.SymLibTable

Complete Module Reference
-------------------------

.. toctree::
   :maxdepth: 1

   modules_detailed