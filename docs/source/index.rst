.. KiCadFiles documentation master file, created by
   sphinx-quickstart on Sun Sep 21 14:26:17 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

KiCadFiles documentation
========================

A comprehensive Python library for parsing and manipulating KiCad file formats.

Features
--------

* **Complete KiCad S-expression support**: 207 classes representing all KiCad tokens
* **Type-safe parsing**: Full Python type hints for all classes and methods
* **Flexible error handling**: Three strictness modes (STRICT, FAILSAFE, SILENT)
* **Round-trip parsing**: Parse KiCad files and convert back to S-expressions
* **Minimal dependencies**: Uses only sexpdata for S-expression parsing

Installation
------------

.. code-block:: bash

   pip install kicadfiles

Quick Start
-----------

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from kicadfiles import At, Layer, ParseStrictness

   # Create objects using dataclass syntax
   position = At(x=10.0, y=20.0, angle=90.0)
   layer = Layer(name="F.Cu")

   # Parse from S-expression
   at_obj = At.from_sexpr("(at 10.0 20.0 90.0)", ParseStrictness.STRICT)

   # Convert back to S-expression string
   sexpr_str = at_obj.to_sexpr_str(pretty_print=False)

Main File Format Classes
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from kicadfiles import (
       KicadSymbolLib, KicadPcb, KicadSch, KicadWks,
       Footprint, KicadProject, ParseStrictness
   )

   # Symbol library (.kicad_sym)
   symbol_lib = KicadSymbolLib.from_file("library.kicad_sym", ParseStrictness.STRICT)
   symbol_lib.save_to_file("output.kicad_sym")

   # PCB board (.kicad_pcb)
   pcb = KicadPcb.from_file("board.kicad_pcb", ParseStrictness.STRICT)
   pcb.save_to_file("output.kicad_pcb")

   # Schematic (.kicad_sch)
   schematic = KicadSch.from_file("schematic.kicad_sch", ParseStrictness.STRICT)
   schematic.save_to_file("output.kicad_sch")

   # Worksheet (.kicad_wks)
   worksheet = KicadWks.from_file("worksheet.kicad_wks", ParseStrictness.STRICT)
   worksheet.save_to_file("output.kicad_wks")

   # Footprint (.kicad_mod)
   footprint = Footprint.from_file("footprint.kicad_mod", ParseStrictness.STRICT)
   footprint.save_to_file("output.kicad_mod")

   # Project settings (.kicad_pro)
   project = KicadProject.from_file("project.kicad_pro", ParseStrictness.STRICT)
   project.save_to_file("output.kicad_pro")

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   kicadfiles

