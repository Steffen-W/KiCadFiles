#!/usr/bin/env python3
"""Basic functionality tests for KiCadFiles library."""

import pytest

from kicadfiles import (
    At,
    Layer,
    ParseStrictness,
    Size,
    __version__,
)
from kicadfiles.sexpr_parser import sexpr_to_str, str_to_sexpr


def test_version():
    """Test that version information is available."""
    assert __version__ is not None
    assert isinstance(__version__, str)
    print(f"KiCadFiles version: {__version__}")


def test_basic_object_creation():
    """Test basic object creation."""
    # Test At object
    at_obj = At(x=10.0, y=20.0, angle=90.0)
    assert at_obj.x == 10.0
    assert at_obj.y == 20.0
    assert at_obj.angle == 90.0

    # Test Size object
    size_obj = Size(width=1.2, height=0.8)
    assert size_obj.width == 1.2
    assert size_obj.height == 0.8

    # Test Layer object
    layer_obj = Layer(name="F.Cu")
    assert layer_obj.name == "F.Cu"


def test_sexpr_serialization():
    """Test S-expression serialization."""
    at_obj = At(x=10.0, y=20.0, angle=90.0)

    # Convert to S-expression
    sexpr = at_obj.to_sexpr()
    assert sexpr is not None
    assert sexpr[0] == "at"

    # Convert to string
    sexpr_str = at_obj.to_sexpr_str()
    assert isinstance(sexpr_str, str)
    assert "at" in sexpr_str


def test_sexpr_parsing():
    """Test S-expression parsing."""
    # Test with complete S-expression
    sexpr_str = "(at 25.4 38.1 180.0)"
    at_obj = At.from_sexpr(sexpr_str, ParseStrictness.STRICT)

    assert at_obj.x == 25.4
    assert at_obj.y == 38.1
    assert at_obj.angle == 180.0


def test_round_trip():
    """Test complete round-trip parsing."""
    # Create original object
    original = At(x=100.0, y=200.0, angle=45.0)

    # Serialize to S-expression
    sexpr_str = original.to_sexpr_str()

    # Parse back
    regenerated = At.from_sexpr(sexpr_str, ParseStrictness.STRICT)

    # Should be equal
    assert original == regenerated
    assert original.x == regenerated.x
    assert original.y == regenerated.y
    assert original.angle == regenerated.angle


def test_strictness_modes():
    """Test different parser strictness modes."""
    # Complete S-expression
    complete_sexpr = "(at 10.0 20.0 90.0)"

    # Incomplete S-expression (missing angle)
    incomplete_sexpr = "(at 10.0 20.0)"

    # STRICT mode with complete data should work
    at_complete = At.from_sexpr(complete_sexpr, ParseStrictness.STRICT)
    assert at_complete.x == 10.0
    assert at_complete.y == 20.0
    assert at_complete.angle == 90.0

    # STRICT mode with incomplete data should work (unused parameters are ignored)
    at_strict_incomplete = At.from_sexpr(incomplete_sexpr, ParseStrictness.STRICT)
    assert at_strict_incomplete.x == 10.0
    assert at_strict_incomplete.y == 20.0
    assert at_strict_incomplete.angle is None  # Optional field is None when missing

    # FAILSAFE mode should work with incomplete data
    at_failsafe = At.from_sexpr(incomplete_sexpr, ParseStrictness.FAILSAFE)
    assert at_failsafe.x == 10.0
    assert at_failsafe.y == 20.0
    assert at_failsafe.angle is None  # Optional field is None when missing

    # SILENT mode should work silently with incomplete data
    at_silent = At.from_sexpr(incomplete_sexpr, ParseStrictness.SILENT)
    assert at_silent.x == 10.0
    assert at_silent.y == 20.0
    assert at_silent.angle is None  # Optional field is None when missing


def test_sexpr_utilities():
    """Test S-expression utility functions."""
    # Test string to S-expression conversion
    sexpr_str = "(at 10.0 20.0 90.0)"
    sexpr = str_to_sexpr(sexpr_str)

    assert isinstance(sexpr, list)
    assert str(sexpr[0]) == "at"  # Convert Symbol to string for comparison
    assert sexpr[1] == 10.0
    assert sexpr[2] == 20.0
    assert sexpr[3] == 90.0

    # Test S-expression to string conversion
    regenerated_str = sexpr_to_str(sexpr)
    assert isinstance(regenerated_str, str)
    assert "at" in regenerated_str
    assert "10.0" in regenerated_str


def test_object_equality():
    """Test object equality comparison."""
    at1 = At(x=10.0, y=20.0, angle=90.0)
    at2 = At(x=10.0, y=20.0, angle=90.0)
    at3 = At(x=10.0, y=20.0, angle=0.0)

    # Same values should be equal
    assert at1 == at2

    # Different values should not be equal
    assert at1 != at3

    # Different types should not be equal
    size = Size(width=10.0, height=20.0)
    assert at1 != size


def test_string_representation():
    """Test string representation of objects."""
    at_obj = At(x=10.0, y=20.0, angle=90.0)
    str_repr = str(at_obj)

    assert "At" in str_repr
    assert "10.0" in str_repr
    assert "20.0" in str_repr
    assert "90.0" in str_repr


if __name__ == "__main__":
    print("Running basic functionality tests...")

    test_version()
    test_basic_object_creation()
    test_sexpr_serialization()
    test_sexpr_parsing()
    test_round_trip()
    test_strictness_modes()
    test_sexpr_utilities()
    test_object_equality()
    test_string_representation()

    print("✅ All basic functionality tests passed!")
