#!/usr/bin/env python3
"""
Simple Charlieplex Wiring Example

Demonstrates creating wires, junctions, and labels in a KiCad schematic.
Shows basic schematic element creation without complex abstractions.
"""

from kicadfiles import GRID, At, GlobalLabel, Junction, Label, Wire
from kicadfiles.templates import KiCadTemplates


def create_simple_wiring_example() -> None:
    """Create a simple schematic demonstrating basic wiring elements."""
    print("Creating simple wiring example...")

    # Create empty schematic using template
    schematic = KiCadTemplates.schematic(
        generator="kicadfiles", generator_version="1.0"
    )

    # Initialize lists
    schematic.wires = []
    schematic.junctions = []
    schematic.global_labels = []
    schematic.labels = []

    # Example 1: Simple wire between two points (using grid units)
    wire1 = Wire()
    wire1.uuid.new_id()
    wire1.pts.xy(50 * GRID, 50 * GRID)
    wire1.pts.xy(60 * GRID, 50 * GRID)
    schematic.wires.append(wire1)

    # Example 2: Wire with custom stroke (dotted line)
    wire2 = Wire()
    wire2.uuid.new_id()
    wire2.pts.xy(60 * GRID, 50 * GRID)
    wire2.pts.xy(60 * GRID, 60 * GRID)
    wire2.stroke.width(0.4)
    wire2.stroke.type.value = "dot"
    schematic.wires.append(wire2)

    # Example 3: Junction at wire intersection
    junction = Junction()
    junction.uuid.new_id()
    junction.at.xy(60 * GRID, 50 * GRID)
    schematic.junctions.append(junction)

    # Example 4: Global label
    global_label = GlobalLabel(text="ROW_1")
    global_label.uuid.new_id()
    global_label.at = At(x=50 * GRID, y=50 * GRID, angle=0.0)
    schematic.global_labels.append(global_label)

    # Example 5: Local label (with rotation)
    local_label = Label(text="COL_1")
    local_label.uuid.new_id()
    local_label.at = At(x=60 * GRID, y=60 * GRID, angle=90.0)
    schematic.labels.append(local_label)

    print(f"Created schematic with:")
    print(f"  - {len(schematic.wires)} wires")
    print(f"  - {len(schematic.junctions)} junctions")
    print(f"  - {len(schematic.global_labels)} global labels")
    print(f"  - {len(schematic.labels)} local labels")

    # Save to file
    try:
        output_file = "simple_wiring_example.kicad_sch"
        with open(output_file, "w") as f:
            f.write(schematic.to_sexpr_str())
        print(f"\nSaved to: {output_file}")
    except Exception as e:
        print(f"\nCould not save: {e}")


def demonstrate_charlieplex_concept() -> None:
    """
    Demonstrate Charlieplex wiring concept.

    NOTE: This is a simplified demonstration showing the wiring pattern.
    A complete implementation would require:
    - TODO: Symbol instance placement (see symbol_placement_example.py)
    - TODO: Proper pin-to-wire connections using net names
    - TODO: Hierarchical sheet system for larger arrays
    - TODO: Design rule checks for Charlieplex topology validation
    """
    print("\n" + "=" * 60)
    print("Charlieplex Wiring Concept")
    print("=" * 60)

    # Create schematic using template
    schematic = KiCadTemplates.schematic(
        generator="kicadfiles", generator_version="1.0"
    )

    schematic.wires = []
    schematic.junctions = []
    schematic.global_labels = []

    # TODO: Add LED symbol instances here
    # This example only shows the wiring pattern, not the actual LEDs
    # See symbol_placement_example.py for how to place symbols

    # Create a simple 3-pin Charlieplex pattern (2 LEDs)
    # Pin 1 -- LED1 --> Pin 2 -- LED2 --> Pin 3

    spacing = 10
    y_pos = 50

    # Horizontal bus lines for each pin
    for i in range(3):
        x_start = 40
        x_end = 80
        y = y_pos + (i * spacing)

        # Bus wire
        wire = Wire()
        wire.uuid.new_id()
        wire.pts.xy(x_start * GRID, y * GRID)
        wire.pts.xy(x_end * GRID, y * GRID)
        schematic.wires.append(wire)

        # Global label
        label = GlobalLabel(text=f"CHRLY_{i + 1}")
        label.uuid.new_id()
        label.at = At(x=x_start * GRID, y=y * GRID, angle=0.0)
        schematic.global_labels.append(label)

    # TODO: Add LED symbol connections here
    # LED1 would connect between CHRLY_1 and CHRLY_2
    # LED2 would connect between CHRLY_2 and CHRLY_3

    print(f"\nCreated Charlieplex wiring pattern with:")
    print(f"  - {len(schematic.wires)} bus wires")
    print(f"  - {len(schematic.global_labels)} control lines")
    print(f"\nLimitations of this example:")
    print(f"  - No actual LED symbols placed (see TODOs in code)")
    print(f"  - No pin connections (requires net system)")
    print(f"  - Simplified 3-pin pattern only")


if __name__ == "__main__":
    # Run simple wiring example
    create_simple_wiring_example()

    # Show Charlieplex concept
    demonstrate_charlieplex_concept()

    print("\n" + "=" * 60)
    print("Key takeaways:")
    print("  - Wires connect two points with Pts and Xy coordinates")
    print("  - Junctions mark wire intersections")
    print("  - Labels (global/local) name nets")
    print("  - Stroke can customize wire appearance")
    print("\nFor symbol placement, see: symbol_placement_example.py")
    print("=" * 60)
