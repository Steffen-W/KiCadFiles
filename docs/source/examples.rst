Examples
========

This section provides practical examples of using KiCadFiles in real-world scenarios.

Basic Usage Examples
--------------------

Parsing KiCad Files
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from kicadfiles import (
       KicadPcb, KicadSch, Footprint, KicadSymbolLib, KicadWks,
       KicadProject, KiCadDesignRules, FpLibTable, SymLibTable,
       ParseStrictness
   )

   # Parse a PCB file
   pcb = KicadPcb.from_file("tests/fixtures/pcb/minimal.kicad_pcb", ParseStrictness.STRICT)
   print(f"Board has {len(pcb.footprints)} footprints")

   # Parse a schematic file
   schematic = KicadSch.from_file("tests/fixtures/schematic/minimal.kicad_sch", ParseStrictness.STRICT)
   symbol_count = len(schematic.lib_symbols.symbols) if schematic.lib_symbols else 0
   print(f"Schematic has {symbol_count} symbols")

   # Parse a footprint file
   footprint = Footprint.from_file("tests/fixtures/footprints/small.kicad_mod", ParseStrictness.STRICT)
   print(f"Footprint has {len(footprint.pads)} pads")

   # Parse a symbol library file
   symbol_lib = KicadSymbolLib.from_file("tests/fixtures/symbols/small.kicad_sym", ParseStrictness.STRICT)
   print(f"Library has {len(symbol_lib.symbols)} symbols")

   # Parse a worksheet/template file
   worksheet = KicadWks.from_file("tests/fixtures/worksheets/small.kicad_wks", ParseStrictness.STRICT)
   print(f"Worksheet loaded successfully")

   # Parse a project file (JSON format)
   project = KicadProject.from_file("tests/fixtures/projects/minimal.kicad_pro", ParseStrictness.STRICT)
   print(f"Project loaded successfully")

   # Parse design rules file
   design_rules = KiCadDesignRules.from_file("tests/fixtures/design_rules/minimal.kicad_dru", ParseStrictness.STRICT)
   print(f"Design rules loaded")

   # Footprint library table
   fp_lib_table = FpLibTable.from_file("tests/fixtures/tables/fp-lib-table", ParseStrictness.STRICT)
   print(f"Footprint library tables loaded")

   # Symbol library table
   sym_lib_table = SymLibTable.from_file("tests/fixtures/tables/sym-lib-table", ParseStrictness.STRICT)
   print(f"Symbol library tables loaded")


Creating Objects Programmatically
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from kicadfiles import At, Size, ParseStrictness

   # Create basic objects programmatically
   position = At(x=10.0, y=20.0, angle=90.0)
   size = Size(width=1.0, height=0.5)

   print(f"Position: {position}")
   print(f"Size: {size}")

   # Convert simple objects to S-expression
   position_sexpr = position.to_sexpr_str(pretty_print=False)
   print(f"Position S-expression: {position_sexpr}")

   # Parse from S-expression
   at_obj = At.from_sexpr("(at 10.0 20.0 90.0)", ParseStrictness.STRICT)
   print(f"Parsed position: {at_obj}")

Error Handling Strategies
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from kicadfiles import KicadPcb, ParseStrictness
   import logging

   # Configure logging to see warnings
   logging.basicConfig(level=logging.WARNING)

   # Test different strictness modes with a valid file
   # STRICT mode - raises exceptions on errors
   try:
       pcb = KicadPcb.from_file("tests/fixtures/pcb/minimal.kicad_pcb", ParseStrictness.STRICT)
       print("STRICT mode: File parsed successfully")
   except ValueError as e:
       print(f"Parsing failed: {e}")

   # FAILSAFE mode - logs warnings, uses defaults for problems
   pcb = KicadPcb.from_file("tests/fixtures/pcb/minimal.kicad_pcb", ParseStrictness.FAILSAFE)
   print("FAILSAFE mode: File parsed with warnings logged for any issues")

   # SILENT mode - uses defaults without warnings
   pcb = KicadPcb.from_file("tests/fixtures/pcb/minimal.kicad_pcb", ParseStrictness.SILENT)
   print("SILENT mode: File parsed silently, using defaults for any problems")

Advanced Usage Examples
-----------------------

Modifying PCB Files
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from kicadfiles import KicadPcb, Footprint, At, ParseStrictness

   # Load existing PCB
   pcb = KicadPcb.from_file("tests/fixtures/pcb/minimal.kicad_pcb", ParseStrictness.STRICT)

   # Example: Move all footprints by 5mm to the right
   for footprint in pcb.footprints:
       if footprint.at:
           footprint.at.x += 5.0  # Move 5mm to the right
           print(f"Moved footprint to ({footprint.at.x}, {footprint.at.y})")

   # Save modified PCB (uncomment to actually save)
   # pcb.save_to_file("output.kicad_pcb")
   print("PCB modifications complete")

Working with Symbols
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from kicadfiles import KicadSymbolLib, Symbol, Pin, At, ParseStrictness

   # Load symbol library
   lib = KicadSymbolLib.from_file("tests/fixtures/symbols/small.kicad_sym", ParseStrictness.STRICT)

   # Examine all symbols in the library
   for i, symbol in enumerate(lib.symbols):
       print(f"Symbol {i+1}: {len(symbol.pins)} pins")

       # List first few pins (to avoid too much output)
       for j, pin in enumerate(symbol.pins[:3]):
           print(f"  Pin {pin.number}: {pin.name} at ({pin.at.x}, {pin.at.y})")
       if len(symbol.pins) > 3:
           print(f"  ... and {len(symbol.pins) - 3} more pins")

   # Create a new symbol
   new_symbol = Symbol(
       library_link="my_new_component",
       pins=[
           Pin(number="1", name="VCC", at=At(x=0, y=2.54)),
           Pin(number="2", name="GND", at=At(x=0, y=-2.54))
       ]
   )

   # Add to library and save (uncomment to actually save)
   lib.symbols.append(new_symbol)
   # lib.save_to_file("modified_library.kicad_sym")
   print(f"Added new symbol, library now has {len(lib.symbols)} symbols")

Batch Processing
~~~~~~~~~~~~~~~~

.. code-block:: python

   import os
   from pathlib import Path
   from kicadfiles import Footprint, ParseStrictness

   # Process all footprints in the fixtures directory
   footprint_dir = Path("tests/fixtures/footprints/")

   for footprint_file in footprint_dir.glob("*.kicad_mod"):
       try:
           footprint = Footprint.from_file(footprint_file, ParseStrictness.STRICT)

           # Analyze footprint
           pad_count = len(footprint.pads)
           print(f"{footprint_file.name}: {pad_count} pads")

           # Example: Add metadata
           if footprint.properties is None:
               footprint.properties = []

           # Save with modifications (uncomment to actually save)
           # output_file = Path("processed") / footprint_file.name
           # footprint.save_to_file(output_file)
           print(f"  Processed footprint with {pad_count} pads")

       except Exception as e:
           print(f"Error processing {footprint_file}: {e}")

Round-trip Verification
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from kicadfiles import KicadPcb, ParseStrictness

   # Load, convert to S-expression, and parse again
   original_pcb = KicadPcb.from_file("tests/fixtures/pcb/minimal.kicad_pcb", ParseStrictness.STRICT)

   # Convert to S-expression string
   sexpr_string = original_pcb.to_sexpr_str(pretty_print=True)

   # Parse the S-expression back to object
   reconstructed_pcb = KicadPcb.from_sexpr(sexpr_string, ParseStrictness.STRICT)

   # Verify complete equality
   assert original_pcb.footprints == reconstructed_pcb.footprints
   assert original_pcb.nets == reconstructed_pcb.nets
   assert original_pcb.layers == reconstructed_pcb.layers

   # test the complete object
   assert original_pcb == reconstructed_pcb
   print("Round-trip verification successful - objects are identical!")

