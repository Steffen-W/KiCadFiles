API Reference
=============

This section provides an overview of all KiCadFiles modules organized by functionality.

For detailed documentation of each module, see :doc:`modules_detailed`.

Core Classes
------------

.. autosummary::

   kicadfiles.base_element
   kicadfiles.base_types
   kicadfiles.enums

File Format Classes
-------------------

These classes represent complete KiCad file formats:

.. autosummary::

   kicadfiles.board_layout
   kicadfiles.symbol_library
   kicadfiles.footprint_library
   kicadfiles.schematic_system
   kicadfiles.project_settings

Graphics and Drawing
--------------------

.. autosummary::

   kicadfiles.primitive_graphics
   kicadfiles.advanced_graphics
   kicadfiles.text_and_documents

PCB Components
--------------

.. autosummary::

   kicadfiles.pad_and_drill
   kicadfiles.zone_system

Utilities
---------

.. autosummary::

   kicadfiles.sexpdata
   kicadfiles.sexpr_parser
   kicadfiles.json_base_element
   kicadfiles.design_rules

Complete Module Reference
-------------------------

.. toctree::
   :maxdepth: 1

   modules_detailed