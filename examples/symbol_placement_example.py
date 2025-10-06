#!/usr/bin/env python3
"""
Symbol Placement Example

Demonstrates how KiCad manages symbol libraries and instances:
1. Load a symbol from a library
2. Embed the symbol definition in the schematic
3. Create multiple instances with different positions and references
"""

import copy

from kicadfiles import (
    At,
    KicadSch,
    KicadSymbolLib,
    LibSymbols,
    NamedInt,
    NamedString,
    Property,
    Symbol,
    Uuid,
)
from kicadfiles.base_element import TokenFlag
from kicadfiles.schematic_system import PinRef, SchematicSymbol


def load_symbol_from_library(library_path: str, symbol_name: str) -> Symbol:
    """
    Load a symbol definition from a library file.

    Args:
        library_path: Path to .kicad_sym file
        symbol_name: Name of the symbol to load (e.g., "R")

    Returns:
        Symbol object from the library
    """
    lib = KicadSymbolLib.from_file(library_path)

    # Find the symbol by name
    if lib.symbols is None:
        raise ValueError(f"Library has no symbols")

    for symbol in lib.symbols:
        if symbol.library_id == symbol_name:
            return symbol

    raise ValueError(f"Symbol '{symbol_name}' not found in library")


def create_schematic_with_symbols() -> None:
    """
    Create a schematic with symbol instances from a library.

    This demonstrates the KiCad workflow:
    1. Load symbol definition from library
    2. Embed symbol in schematic's lib_symbols section
    3. Create multiple instances with different positions
    """

    print("=== Creating Schematic with Symbol Instances ===\n")

    # Step 1: Load symbol from library
    print("Step 1: Loading symbol from library...")
    try:
        symbol_template = load_symbol_from_library(
            "examples/test/New_Library.kicad_sym", "R"
        )
        print(f"  Loaded symbol: {symbol_template.library_id}")
        print(f"  Pins: {len(symbol_template.pins) if symbol_template.pins else 0}")
    except Exception as e:
        print(f"  Error: {e}")
        return

    # Step 2: Create schematic
    print("\nStep 2: Creating schematic...")
    from kicadfiles.schematic_system import Paper

    schematic = KicadSch(
        version=NamedInt("version", 20250114),
        generator=NamedString("generator", "kicadfiles"),
        generator_version=NamedString("generator_version", "1.0"),
        uuid=Uuid.create(),
        paper=Paper(size="A4"),
    )

    # Step 3: Embed symbol definition in schematic
    print("\nStep 3: Embedding symbol definition in schematic...")

    # Create lib_symbols section
    schematic.lib_symbols = LibSymbols()

    # Deep copy the symbol and add library namespace
    embedded_symbol = copy.deepcopy(symbol_template)
    embedded_symbol.library_id = f"New_Library:{symbol_template.library_id}"

    schematic.lib_symbols.symbols = [embedded_symbol]
    print(f"  Embedded symbol: {embedded_symbol.library_id}")

    # Step 4: Create symbol instances
    print("\nStep 4: Creating symbol instances...")

    # Instance 1: R1 at position (123.19, 85.09), horizontal
    r1 = create_symbol_instance(
        lib_id="New_Library:R",
        reference="R1",
        value="R",
        position=(123.19, 85.09),
        angle=0.0,
        footprint="sym:R_0805_2012Metric",
        pin_count=2,
    )
    if r1.at:
        print(
            f"  Created instance: {r1.lib_id} at ({r1.at.x}, {r1.at.y}), angle={r1.at.angle}"
        )
    else:
        print(f"  Created instance: {r1.lib_id}")

    # Instance 2: R2 at position (152.4, 102.87), vertical (90°)
    r2 = create_symbol_instance(
        lib_id="New_Library:R",
        reference="R2",
        value="R",
        position=(152.4, 102.87),
        angle=90.0,
        footprint="sym:R_0805_2012Metric",
        pin_count=2,
    )
    if r2.at:
        print(
            f"  Created instance: {r2.lib_id} at ({r2.at.x}, {r2.at.y}), angle={r2.at.angle}"
        )
    else:
        print(f"  Created instance: {r2.lib_id}")

    # Add instances to schematic
    if schematic.symbols is None:
        schematic.symbols = []
    schematic.symbols.extend([r1, r2])

    # Step 5: Save schematic
    print("\nStep 5: Saving schematic...")
    output_file = "examples/test/generated_schematic.kicad_sch"
    try:
        schematic.save_to_file(output_file)
        print(f"  Saved to: {output_file}")
    except Exception as e:
        print(f"  Could not save: {e}")
        # Print S-expression instead
        print("\nGenerated S-expression (first 500 chars):")
        sexpr = schematic.to_sexpr_str()
        print(sexpr[:500] + "...")

    print("\n=== Summary ===")
    print(f"Library symbols embedded: {len(schematic.lib_symbols.symbols)}")
    print(f"Symbol instances created: {len(schematic.symbols)}")
    print("\nKey concepts:")
    print("1. lib_symbols section contains the symbol DEFINITION (template)")
    print("2. symbol instances reference lib_id with 'LibraryName:SymbolName' format")
    print("3. Each instance has unique position, reference, and UUIDs")
    print("4. All instances share the same symbol definition from lib_symbols")


def create_symbol_instance(
    lib_id: str,
    reference: str,
    value: str,
    position: tuple[float, float],
    angle: float,
    footprint: str,
    pin_count: int,
) -> SchematicSymbol:
    """
    Create a symbol instance with all required properties.

    Args:
        lib_id: Library ID (e.g., "New_Library:R")
        reference: Reference designator (e.g., "R1")
        value: Component value (e.g., "R")
        position: (x, y) position in mm
        angle: Rotation angle in degrees
        footprint: Footprint name
        pin_count: Number of pins

    Returns:
        SchematicSymbol object
    """
    instance = SchematicSymbol(
        lib_id=NamedString("lib_id", lib_id),
        at=At(x=position[0], y=position[1], angle=angle),
        unit=NamedInt("unit", 1),
        exclude_from_sim=TokenFlag("exclude_from_sim", "no"),
        in_bom=TokenFlag("in_bom", "yes"),
        on_board=TokenFlag("on_board", "yes"),
        dnp=TokenFlag("dnp", "no"),
        fields_autoplaced=TokenFlag("fields_autoplaced", "yes"),
        uuid=Uuid.create(),
    )

    # Add properties
    instance.properties = [
        Property(
            key="Reference",
            value=reference,
            at=At(x=position[0] + 2.54, y=position[1] - 2.54),
        ),
        Property(
            key="Value",
            value=value,
            at=At(x=position[0] + 2.54, y=position[1]),
        ),
        Property(
            key="Footprint",
            value=footprint,
            at=At(x=position[0], y=position[1]),
        ),
    ]

    # Add pin references (each pin needs a unique UUID)
    instance.pins = []
    for pin_num in range(1, pin_count + 1):
        pin = PinRef(
            number=str(pin_num),
            uuid=Uuid.create(),
        )
        instance.pins.append(pin)

    return instance


def demonstrate_library_workflow() -> None:
    """Demonstrate complete library workflow."""
    print("\n" + "=" * 60)
    print("KiCad Library Workflow Demonstration")
    print("=" * 60 + "\n")

    print("Understanding the relationship:")
    print("1. LIBRARY FILE (.kicad_sym)")
    print("   - Contains master symbol definitions")
    print("   - Shared across projects")
    print("   - Example: New_Library.kicad_sym with symbol 'R'")
    print()

    print("2. LIBRARY TABLE (sym-lib-table)")
    print("   - Registers available libraries")
    print("   - Maps library names to file paths")
    print("   - Example: 'New_Library' -> './New_Library.kicad_sym'")
    print()

    print("3. SCHEMATIC (.kicad_sch)")
    print("   a) lib_symbols section:")
    print("      - Embedded copy of symbol definition")
    print("      - Namespaced: 'LibraryName:SymbolName'")
    print("      - One copy regardless of instance count")
    print()
    print("   b) symbol instances:")
    print("      - Multiple instances reference same lib_symbols entry")
    print("      - Each has unique: position, reference, UUID")
    print("      - Each pin gets unique UUID per instance")
    print()

    create_schematic_with_symbols()


if __name__ == "__main__":
    demonstrate_library_workflow()
