KiCad File Format Classes
==========================

This section documents all KiCad-specific classes organized by file format and functionality.

Main File Format Classes
------------------------

These classes represent complete KiCad file formats with ``from_file()`` and ``save_to_file()`` support.

kicadfiles.board_layout module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PCB board files (.kicad_pcb) including footprints, traces, zones, and board settings.

.. automodule:: kicadfiles.board_layout
   :members:

kicadfiles.schematic_system module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Schematic files (.kicad_sch) including wires, symbols, labels, and connections.

.. automodule:: kicadfiles.schematic_system
   :members:

kicadfiles.symbol_library module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Symbol library files (.kicad_sym) for schematic components.

.. automodule:: kicadfiles.symbol_library
   :members:

kicadfiles.footprint_library module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Footprint files (.kicad_mod) for PCB component footprints.

.. automodule:: kicadfiles.footprint_library
   :members:

kicadfiles.project_settings module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Project files (.kicad_pro) with project-wide settings (JSON format).

.. automodule:: kicadfiles.project_settings
   :members:

kicadfiles.text_and_documents module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Worksheet/template files (.kicad_wks) for title blocks and page layouts.

.. automodule:: kicadfiles.text_and_documents
   :members:

kicadfiles.design_rules module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Design rules files (.kicad_dru) for manufacturing constraints.

.. automodule:: kicadfiles.design_rules
   :members:

kicadfiles.library_tables module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Library table files (fp-lib-table, sym-lib-table) for library management.

.. automodule:: kicadfiles.library_tables
   :members:

Component and Drawing Classes
------------------------------

kicadfiles.pad_and_drill module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pad, via, and drill definitions for PCB footprints.

.. automodule:: kicadfiles.pad_and_drill
   :members:

kicadfiles.primitive_graphics module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Basic graphical elements (lines, circles, rectangles, arcs, polygons).

.. automodule:: kicadfiles.primitive_graphics
   :members:

kicadfiles.advanced_graphics module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Advanced graphical elements (images, text boxes, dimension annotations).

.. automodule:: kicadfiles.advanced_graphics
   :members:

kicadfiles.zone_system module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Copper zones, keepout areas, and filled polygon regions.

.. automodule:: kicadfiles.zone_system
   :members:
