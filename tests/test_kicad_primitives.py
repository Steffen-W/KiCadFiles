#!/usr/bin/env python3
"""Tests for KiCad primitive classes."""

from dataclasses import dataclass, field
from typing import ClassVar, Optional

from kicadfiles.base_element import (
    NamedFloat,
    NamedInt,
    NamedObject,
    NamedString,
    ParseStrictness,
)


@dataclass
class SamplePrimitiveObject(NamedObject):
    """Sample object using KiCad primitives for testing."""

    __token_name__: ClassVar[str] = "test_primitive"

    # Required primitives (metadata defines required/optional behavior)
    name: NamedString = field(
        default_factory=lambda: NamedString(token="name", value=""),
        metadata={"description": "Component name", "required": True},
    )
    width: NamedFloat = field(
        default_factory=lambda: NamedFloat(token="width", value=0.0),
        metadata={"description": "Component width", "required": True},
    )
    count: NamedInt = field(
        default_factory=lambda: NamedInt(token="count", value=0),
        metadata={"description": "Component count", "required": True},
    )

    # Optional primitives (metadata is the source of truth)
    description: NamedString = field(
        default_factory=lambda: NamedString(token="description", value=""),
        metadata={"description": "Component description", "required": False},
    )
    height: NamedFloat = field(
        default_factory=lambda: NamedFloat(token="height", value=0.0),
        metadata={"description": "Component height", "required": False},
    )
    version: NamedInt = field(
        default_factory=lambda: NamedInt(token="version", value=1),
        metadata={"description": "Component version", "required": False},
    )


class TestNamedValues:
    """Test suite for KiCad primitive classes."""

    def test_primitive_basic(self):
        """Test basic primitive functionality."""
        # Basic construction (required is now a read-only property)
        name = NamedString(token="name", value="test_component")
        assert name.value == "test_component"
        assert name.required is True  # Default value
        assert name.token == "name"

        # to_sexpr works for manually created objects
        sexpr_result = name.to_sexpr()
        assert sexpr_result == ["name", "test_component"]

        # Equality
        name2 = NamedString(token="name", value="test_component")
        assert name == name2

    def test_sample_primitive_object_roundtrip(self):
        """Test roundtrip parsing - this is where __found__ should be set automatically."""
        # Create S-expression manually (simulates a file being parsed)
        sexpr = [
            "test_primitive",
            ["name", "MyComponent"],
            ["width", 2.54],
            ["count", 5],
            ["description", "Test description"],
        ]

        # Parse from S-expression (this should set __found__=True automatically)
        parsed = SamplePrimitiveObject.from_sexpr(sexpr, ParseStrictness.STRICT)

        # Verify values were parsed correctly
        assert parsed.name.value == "MyComponent"
        assert parsed.width.value == 2.54
        assert parsed.count.value == 5
        assert parsed.description.value == "Test description"

        # Verify that parser correctly parsed all values

        # Test that serialization works (note: may include default values)
        parsed_sexpr = parsed.to_sexpr()
        # Check that the basic structure is correct
        assert parsed_sexpr[0] == "test_primitive"
        assert ["name", "MyComponent"] in parsed_sexpr
        assert ["width", 2.54] in parsed_sexpr
        assert ["count", 5] in parsed_sexpr
        assert ["description", "Test description"] in parsed_sexpr

    def test_test_primitive_object_roundtrip_minimal(self):
        """Test roundtrip with minimal (required only) S-expression."""
        # Minimal S-expression with only required fields
        sexpr = [
            "test_primitive",
            ["name", "MinimalComponent"],
            ["width", 1.0],
            ["count", 1],
        ]

        # Parse from S-expression
        parsed = SamplePrimitiveObject.from_sexpr(sexpr, ParseStrictness.STRICT)

        # Verify values
        assert parsed.name.value == "MinimalComponent"

        # Serialization should work correctly
        parsed_sexpr = parsed.to_sexpr()
        assert parsed_sexpr[0] == "test_primitive"
        assert ["name", "MinimalComponent"] in parsed_sexpr
        assert ["width", 1.0] in parsed_sexpr
        assert ["count", 1] in parsed_sexpr


if __name__ == "__main__":
    import os
    import sys

    # Add project root to path for imports
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Run basic tests
    test = TestNamedValues()

    print("=== Testing KiCad Primitives ===")
    test.test_primitive_basic()
    print("✅ KiCad primitive basic tests passed")

    test.test_sample_primitive_object_roundtrip()
    print("✅ SamplePrimitiveObject full roundtrip tests passed")

    test.test_test_primitive_object_roundtrip_minimal()
    print("✅ SamplePrimitiveObject minimal roundtrip tests passed")

    print("\n🎉 All KiCad primitive tests passed!")
