#!/usr/bin/env python3
"""Tests for KiCad primitive classes."""

from dataclasses import dataclass, field
from typing import ClassVar, Optional

from kicadfiles.base_element import (
    KiCadFloat,
    KiCadInt,
    KiCadObject,
    KiCadStr,
    ParseStrictness,
)


@dataclass
class SamplePrimitiveObject(KiCadObject):
    """Sample object using KiCad primitives for testing."""

    __token_name__: ClassVar[str] = "test_primitive"

    # Required primitives
    name: KiCadStr = field(
        default_factory=lambda: KiCadStr(token="name", value="", required=True)
    )
    width: KiCadFloat = field(
        default_factory=lambda: KiCadFloat(token="width", value=0.0, required=True)
    )
    count: KiCadInt = field(
        default_factory=lambda: KiCadInt(token="count", value=0, required=True)
    )

    # Optional primitives
    description: KiCadStr = field(
        default_factory=lambda: KiCadStr(token="description", value="", required=False)
    )
    height: KiCadFloat = field(
        default_factory=lambda: KiCadFloat(token="height", value=0.0, required=False)
    )
    version: KiCadInt = field(
        default_factory=lambda: KiCadInt(token="version", value=1, required=False)
    )


class TestKiCadPrimitives:
    """Test suite for KiCad primitive classes."""

    def test_primitive_basic(self):
        """Test basic primitive functionality."""
        # Basic construction
        name = KiCadStr(token="name", value="test_component", required=True)
        assert name.value == "test_component"
        assert name.required is True
        assert name.token == "name"

        # to_sexpr works for manually created objects
        sexpr_result = name.to_sexpr()
        assert sexpr_result == ["name", "test_component"]

        # Equality
        name2 = KiCadStr(token="name", value="test_component", required=True)
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
    test = TestKiCadPrimitives()

    print("=== Testing KiCad Primitives ===")
    test.test_primitive_basic()
    print("✅ KiCad primitive basic tests passed")

    test.test_sample_primitive_object_roundtrip()
    print("✅ SamplePrimitiveObject full roundtrip tests passed")

    test.test_test_primitive_object_roundtrip_minimal()
    print("✅ SamplePrimitiveObject minimal roundtrip tests passed")

    print("\n🎉 All KiCad primitive tests passed!")
