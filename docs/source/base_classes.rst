Base Classes and Utilities
===========================

This section documents the core base classes, enums, and utility modules that form the foundation of the KiCadFiles library.

Core Base Classes
-----------------

kicadfiles.base_element module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Base class for S-expression based KiCad objects. Provides parsing and serialization functionality for KiCad S-expression format.

.. automodule:: kicadfiles.base_element
   :members:

kicadfiles.json_base_element module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Base class for JSON based KiCad objects (e.g., project files). Provides parsing and serialization functionality for KiCad JSON format.

.. automodule:: kicadfiles.json_base_element
   :members:

Basic Types
-----------

kicadfiles.base_types module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Common basic types used across KiCad files (At, Size, Layer, Stroke, etc.).

.. automodule:: kicadfiles.base_types
   :members:

kicadfiles.enums module
~~~~~~~~~~~~~~~~~~~~~~~

Enumeration types for various KiCad properties (PadType, PadShape, StrokeType, etc.).

.. automodule:: kicadfiles.enums
   :members:

Parser and Data Utilities
--------------------------

kicadfiles.sexpr_parser module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

S-expression parser for KiCad file formats.

.. automodule:: kicadfiles.sexpr_parser
   :members:

kicadfiles.sexpdata module
~~~~~~~~~~~~~~~~~~~~~~~~~~

Low-level S-expression data structures and utilities.

.. automodule:: kicadfiles.sexpdata
   :members:
