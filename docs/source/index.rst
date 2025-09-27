.. KiCadFiles documentation master file, created by
   sphinx-quickstart on Sun Sep 21 14:26:17 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

KiCadFiles documentation
========================

A comprehensive Python library for parsing and manipulating KiCad file formats.

Features
--------

* **Complete KiCad S-expression support**: >200 classes representing KiCad tokens (missing tokens? `create an issue <https://github.com/Steffen-W/KiCadFiles/issues>`_ with examples)
* **Type-safe parsing**: Full Python type hints for all classes and methods
* **Flexible error handling**: Three strictness modes (STRICT, FAILSAFE, SILENT)
* **Round-trip parsing**: Parse KiCad files and convert back to S-expressions
* **Minimal dependencies**: Self-contained S-expression parsing (no external dependencies)

Installation
------------

.. code-block:: bash

   pip install kicadfiles

Quick Start
-----------

Main File Format Classes
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from kicadfiles import (
       KicadPcb, KicadSch, Footprint, KicadWks, KicadSymbolLib,
       KicadProject, KiCadDesignRules, FpLibTable, SymLibTable,
       ParseStrictness
   )

   # PCB board (.kicad_pcb)
   pcb = KicadPcb.from_file("tests/fixtures/pcb/minimal.kicad_pcb", ParseStrictness.STRICT)
   # pcb.save_to_file("output.kicad_pcb")  # Uncomment to save

   # Schematic (.kicad_sch)
   schematic = KicadSch.from_file("tests/fixtures/schematic/minimal.kicad_sch", ParseStrictness.STRICT)
   # schematic.save_to_file("output.kicad_sch")  # Uncomment to save

   # Footprint (.kicad_mod)
   footprint = Footprint.from_file("tests/fixtures/footprints/small.kicad_mod", ParseStrictness.STRICT)
   # footprint.save_to_file("output.kicad_mod")  # Uncomment to save

   # Symbol library (.kicad_sym)
   symbol_lib = KicadSymbolLib.from_file("tests/fixtures/symbols/small.kicad_sym", ParseStrictness.STRICT)
   # symbol_lib.save_to_file("output.kicad_sym")  # Uncomment to save

   # Worksheet (.kicad_wks)
   worksheet = KicadWks.from_file("tests/fixtures/worksheets/small.kicad_wks", ParseStrictness.STRICT)
   # worksheet.save_to_file("output.kicad_wks")  # Uncomment to save

   # Project settings (.kicad_pro)
   project = KicadProject.from_file("tests/fixtures/projects/minimal.kicad_pro", ParseStrictness.STRICT)
   # project.save_to_file("output.kicad_pro")  # Uncomment to save

   # Design rules (.kicad_dru)
   design_rules = KiCadDesignRules.from_file("tests/fixtures/design_rules/minimal.kicad_dru", ParseStrictness.STRICT)
   # design_rules.save_to_file("output.kicad_dru")  # Uncomment to save

   # Footprint library table
   fp_lib_table = FpLibTable.from_file("tests/fixtures/tables/fp-lib-table", ParseStrictness.STRICT)
   # fp_lib_table.save_to_file("output-fp-lib-table")  # Uncomment to save

   # Symbol library table
   sym_lib_table = SymLibTable.from_file("tests/fixtures/tables/sym-lib-table", ParseStrictness.STRICT)
   # sym_lib_table.save_to_file("output-sym-lib-table")  # Uncomment to save

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
   sexpr_str = at_obj.to_sexpr_str()
   print(sexpr_str)  # Output: (at 10.0 20.0 90.0)

Parsing with Different Strictness Modes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from kicadfiles import At, ParseStrictness

   # STRICT mode: Raises exceptions for any parsing errors
   try:
       at_obj = At.from_sexpr("(at 10.0 20.0)", ParseStrictness.STRICT)
   except ValueError as e:
       print(f"Parsing failed: {e}")

   # FAILSAFE mode: Logs warnings and uses defaults for missing fields
   at_obj = At.from_sexpr("(at 10.0 20.0)", ParseStrictness.FAILSAFE)
   print(f"Angle defaulted to: {at_obj.angle}")  # Output: 0.0

   # SILENT mode: Silently uses defaults for missing fields
   at_obj = At.from_sexpr("(at 10.0 20.0)", ParseStrictness.SILENT)

Working with Complex Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from kicadfiles import Footprint, Pad, At, Size

   # Create a footprint with pads
   footprint = Footprint(
       library_link="Resistor_SMD:R_0603",
       at=At(x=50.0, y=30.0, angle=0.0),
       pads=[
           Pad(
               number="1",
               type="smd",
               shape="roundrect",
               at=At(x=-0.8, y=0.0),
               size=Size(width=0.7, height=0.9)
           ),
           Pad(
               number="2",
               type="smd",
               shape="roundrect",
               at=At(x=0.8, y=0.0),
               size=Size(width=0.7, height=0.9)
           )
       ]
   )

   # Convert to S-expression
   sexpr = footprint.to_sexpr_str()
   print(sexpr)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api
   examples

.. toctree::
   :maxdepth: 1
   :caption: Links:

   GitHub Repository <https://github.com/Steffen-W/KiCadFiles>
   PyPI Package <https://pypi.org/project/kicadfiles/>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

