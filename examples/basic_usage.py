#!/usr/bin/env python3
"""
Basic usage examples for KiCadFiles library.

This script demonstrates the core functionality of the KiCadFiles library,
including creating objects, parsing S-expressions, and handling different
strictness modes.
"""

from kicadfiles import (
    At,
    Footprint,
    Layer,
    Pad,
    ParseStrictness,
    Size,
    sexpr_to_str,
    str_to_sexpr,
)


def basic_object_creation():
    """Demonstrate basic object creation."""
    print("=== Basic Object Creation ===")

    # Create position and size objects
    position = At(x=10.0, y=20.0, angle=90.0)
    size = Size(width=1.2, height=0.8)
    layer = Layer(name="F.Cu")

    print(f"Position: {position}")
    print(f"Size: {size}")
    print(f"Layer: {layer}")
    print()


def sexpr_parsing():
    """Demonstrate S-expression parsing."""
    print("=== S-Expression Parsing ===")

    # Parse from S-expression string
    sexpr_str = "(at 25.4 38.1 180.0)"
    at_obj = At.from_sexpr(sexpr_str, ParseStrictness.STRICT)
    print(f"Parsed: {at_obj}")

    # Convert back to S-expression
    regenerated = at_obj.to_sexpr_str()
    print(f"Regenerated: {regenerated}")
    print()


def strictness_modes():
    """Demonstrate different parser strictness modes."""
    print("=== Parser Strictness Modes ===")

    # Complete S-expression
    complete_sexpr = "(at 10.0 20.0 90.0)"

    # Incomplete S-expression (missing angle)
    incomplete_sexpr = "(at 10.0 20.0)"

    print("Complete S-expression:")
    at_complete = At.from_sexpr(complete_sexpr, ParseStrictness.STRICT)
    print(f"  Result: {at_complete}")

    print("Incomplete S-expression with STRICT mode:")
    at_strict = At.from_sexpr(incomplete_sexpr, ParseStrictness.STRICT)
    print(f"  Result: {at_strict} (angle: {at_strict.angle})")

    print("Incomplete S-expression with FAILSAFE mode:")
    at_failsafe = At.from_sexpr(incomplete_sexpr, ParseStrictness.FAILSAFE)
    print(f"  Result: {at_failsafe} (angle: {at_failsafe.angle})")

    print("Incomplete S-expression with SILENT mode:")
    at_silent = At.from_sexpr(incomplete_sexpr, ParseStrictness.SILENT)
    print(f"  Result: {at_silent} (angle: {at_silent.angle})")
    print()


def complex_object_example():
    """Demonstrate working with complex nested objects."""
    print("=== Complex Object Example ===")

    # Create a simple footprint with pads
    footprint = Footprint(
        library_link="Resistor_SMD:R_0603",
        at=At(x=50.0, y=30.0, angle=0.0),
        layer=Layer(name="F.Cu"),
    )

    print(f"Footprint: {footprint}")

    # Convert to S-expression with pretty printing
    sexpr_str = footprint.to_sexpr_str(pretty_print=True)
    print("S-expression representation:")
    print(sexpr_str)
    print()


def low_level_sexpr_handling():
    """Demonstrate low-level S-expression handling."""
    print("=== Low-Level S-Expression Handling ===")

    # Parse string to raw S-expression
    sexpr_str = '(at 10.0 20.0 (comment "test position"))'
    sexpr = str_to_sexpr(sexpr_str)
    print(f"Raw S-expression: {sexpr}")

    # Convert back to string
    regenerated = sexpr_to_str(sexpr, pretty_print=True)
    print(f"Regenerated string:\n{regenerated}")
    print()


def main():
    """Run all examples."""
    print("KiCadFiles Library - Basic Usage Examples")
    print("=" * 50)
    print()

    basic_object_creation()
    sexpr_parsing()
    strictness_modes()
    complex_object_example()
    low_level_sexpr_handling()

    print("All examples completed successfully!")


if __name__ == "__main__":
    main()
