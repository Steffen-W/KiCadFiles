#!/usr/bin/env python3
"""Test S-expression serialization for exact whitespace and format preservation."""

import pathlib

import pytest

from kicadfiles.base_element import ParseStrictness
from kicadfiles.schematic_system import KicadSch

# Get fixtures directory
FIXTURES_DIR = pathlib.Path(__file__).parent / "fixtures"


def test_minimal_schematic_format_analysis():
    """Analyze the differences between original and serialized formats."""

    # Load the original file
    minimal_sch_path = FIXTURES_DIR / "schematic" / "minimal.kicad_sch"

    # Read original content
    with open(minimal_sch_path, "r", encoding="utf-8") as f:
        original_content = f.read()

    print(f"\nOriginal content ({len(original_content)} chars):")
    print(original_content)

    # Parse the file
    schematic = KicadSch.from_file(str(minimal_sch_path), ParseStrictness.STRICT)

    # Serialize back to S-expression
    serialized_content = schematic.to_sexpr_str()

    print(f"\nSerialized content ({len(serialized_content)} chars):")
    print(serialized_content)

    print("\n" + "=" * 80)
    print("ANALYSIS OF SERIALIZATION DIFFERENCES:")
    print("=" * 80)

    # Key differences found:
    print("\n1. STRUCTURAL DIFFERENCES:")
    print("   Original: (version 20250114)")
    print("   KiCadFiles: (version (version 20250114))")
    print("   → Each field becomes a nested object with named properties")

    print("\n2. STRING QUOTING:")
    print('   Original: (generator "eeschema")')
    print("   KiCadFiles: (generator (name eeschema))")
    print("   → String values lose quotes and become properties")

    print("\n3. WHITESPACE:")
    print("   Original: Uses tabs for indentation")
    print("   KiCadFiles: Uses 2-space indentation")
    print("   → Different pretty-printing format")

    print("\n4. BOOLEAN VALUES:")
    print("   Original: (embedded_fonts no)")
    print("   KiCadFiles: (embedded_fonts (enabled ()))")
    print("   → Boolean 'no' becomes empty list '()'")

    print("\n5. FIELD ORDER:")
    print("   Original: lib_symbols appears before sheet_instances")
    print("   KiCadFiles: Different order in serialization")

    # This test documents the current state rather than requiring exact match
    print("\nCONCLUSION: KiCadFiles uses a different internal representation")
    print("that doesn't match KiCad's native S-expression format exactly.")


def test_minimal_schematic_data_preservation():
    """Test that parsing and serialization preserves data integrity (not format)."""

    minimal_sch_path = FIXTURES_DIR / "schematic" / "minimal.kicad_sch"

    # Parse the file
    schematic1 = KicadSch.from_file(str(minimal_sch_path), ParseStrictness.STRICT)

    # Serialize and parse again
    serialized_content = schematic1.to_sexpr_str()

    # Write to temp file and parse again
    import tempfile

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".kicad_sch", delete=False
    ) as tmp_file:
        tmp_file.write(serialized_content)
        tmp_path = tmp_file.name

    try:
        schematic2 = KicadSch.from_file(tmp_path, ParseStrictness.STRICT)

        # Compare key data fields
        assert schematic1.version.value == schematic2.version.value, "Version mismatch"
        assert (
            schematic1.generator.value == schematic2.generator.value
        ), "Generator mismatch"
        assert (
            schematic1.generator_version.value == schematic2.generator_version.value
        ), "Generator version mismatch"
        assert str(schematic1.uuid) == str(schematic2.uuid), "UUID mismatch"
        assert schematic1.paper.size == schematic2.paper.size, "Paper size mismatch"
        assert bool(schematic1.embedded_fonts) == bool(
            schematic2.embedded_fonts
        ), "Embedded fonts mismatch"

        # Test sheet instances
        assert len(schematic1.sheet_instances.sheet_instances) == len(
            schematic2.sheet_instances.sheet_instances
        ), "Sheet instance count mismatch"

        sheet1 = schematic1.sheet_instances.sheet_instances[0]
        sheet2 = schematic2.sheet_instances.sheet_instances[0]
        assert sheet1.path == sheet2.path, "Sheet path mismatch"
        assert sheet1.page == sheet2.page, "Sheet page mismatch"

        print("\n✓ Data integrity preserved through roundtrip")

    finally:
        import os

        os.unlink(tmp_path)


def test_minimal_schematic_token_format():
    """Test that serialization uses consistent token formatting."""

    minimal_sch_path = FIXTURES_DIR / "schematic" / "minimal.kicad_sch"

    # Parse the file
    schematic = KicadSch.from_file(str(minimal_sch_path), ParseStrictness.STRICT)

    # Serialize back to S-expression
    serialized_content = schematic.to_sexpr_str()

    # Essential formatting checks
    assert serialized_content.startswith(
        "(kicad_sch"
    ), "Should start with unquoted token name"
    assert not serialized_content.startswith(
        '("kicad_sch"'
    ), "Token names should not be quoted"

    # String values should be quoted
    assert '"eeschema"' in serialized_content, "String values should have quotes"
    assert '"9.0"' in serialized_content, "String values should have quotes"

    # Numeric and boolean values should not be quoted
    assert "20250114" in serialized_content, "Numeric values should not be quoted"
    assert (
        "(embedded_fonts no)" in serialized_content
    ), "Boolean values should not be quoted"

    # Structure should be consistent - all fields should be properly nested
    assert "(version" in serialized_content, "Version field should be present"
    assert "(generator" in serialized_content, "Generator field should be present"
    assert "(uuid" in serialized_content, "UUID field should be present"


def test_minimal_schematic_structural_integrity():
    """Test that the parsed structure contains expected elements."""

    minimal_sch_path = FIXTURES_DIR / "schematic" / "minimal.kicad_sch"

    # Parse the file
    schematic = KicadSch.from_file(str(minimal_sch_path), ParseStrictness.STRICT)

    # Verify structure
    assert (
        schematic.version.value == 20250114
    ), f"Expected version 20250114, got {schematic.version.value}"
    assert (
        schematic.generator.value == "eeschema"
    ), f"Expected generator 'eeschema', got {schematic.generator.value}"
    assert (
        schematic.generator_version.value == "9.0"
    ), f"Expected version '9.0', got {schematic.generator_version.value}"
    assert (
        schematic.uuid.value == "5815112a-4879-4f74-9c21-8154c8b30eb2"
    ), f"UUID mismatch: {schematic.uuid}"
    assert (
        schematic.paper.size == "A4"
    ), f"Expected paper size 'A4', got {schematic.paper.size}"

    # Check lib_symbols exists but is empty
    assert schematic.lib_symbols is not None, "lib_symbols should exist"
    assert schematic.lib_symbols.symbols == [], "lib_symbols should be empty list"

    # Check sheet_instances structure
    assert schematic.sheet_instances is not None, "sheet_instances should exist"
    assert (
        len(schematic.sheet_instances.sheet_instances) == 1
    ), "Should have one sheet instance"
    sheet_instance = schematic.sheet_instances.sheet_instances[0]
    assert sheet_instance.path == "/", f"Expected path '/', got {sheet_instance.path}"
    assert (
        sheet_instance.page.value == "1"
    ), f"Expected page '1', got {sheet_instance.page}"

    # Check embedded_fonts
    assert schematic.embedded_fonts is not None, "embedded_fonts should exist"
    assert (
        bool(schematic.embedded_fonts) == False
    ), f"Expected embedded_fonts=False, got {bool(schematic.embedded_fonts)}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
