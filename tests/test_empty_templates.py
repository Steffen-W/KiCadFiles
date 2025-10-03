"""Tests for KiCad file templates.

Verifies that template generation produces valid, serializable objects
and matches expected structures from fixture files where available.
"""

from pathlib import Path

from kicadfiles import (
    Footprint,
    KicadPcb,
    KicadProject,
    KicadSch,
    KicadSymbolLib,
    KiCadTemplates,
    KicadWks,
    ParseStrictness,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "empty"


def test_empty_pcb():
    """Test PCB template generation against fixture."""
    fixture = KicadPcb.from_file(
        str(FIXTURES_DIR / "empty.kicad_pcb"), ParseStrictness.FAILSAFE
    )
    template = KiCadTemplates.pcb()

    # Compare structure, not internal __found__ state
    # Convert both to sexpr and back to normalize __found__ states
    template_sexpr = template.to_sexpr_str()
    fixture_sexpr = fixture.to_sexpr_str()

    template_reparsed = KicadPcb.from_sexpr(template_sexpr, ParseStrictness.FAILSAFE)
    fixture_reparsed = KicadPcb.from_sexpr(fixture_sexpr, ParseStrictness.FAILSAFE)

    assert template_reparsed == fixture_reparsed


def test_empty_schematic():
    """Test schematic template generation against fixture."""
    fixture = KicadSch.from_file(str(FIXTURES_DIR / "empty.kicad_sch"))
    template = KiCadTemplates.schematic()

    # Match UUID from fixture for comparison
    template.uuid = fixture.uuid

    assert template == fixture


def test_empty_footprint():
    """Test footprint template generation.

    TODO: Add fixture file tests/fixtures/empty/empty.kicad_mod for comparison.
    """
    template = KiCadTemplates.footprint("TestFootprint")

    # Verify basic structure
    assert template.library_link == "TestFootprint"

    # Test serialization and deserialization
    sexpr = template.to_sexpr_str()
    reparsed = Footprint.from_sexpr(sexpr)

    assert reparsed.library_link == template.library_link


def test_empty_symbol_library():
    """Test symbol library template generation.

    TODO: Add fixture file tests/fixtures/empty/empty.kicad_sym for comparison.
    """
    template = KiCadTemplates.symbol_library()

    # Verify it's a valid library with no symbols
    assert template.symbols == []

    # Test serialization and deserialization
    sexpr = template.to_sexpr_str()
    reparsed = KicadSymbolLib.from_sexpr(sexpr)

    assert reparsed == template


def test_empty_worksheet():
    """Test worksheet template generation.

    TODO: Add fixture file tests/fixtures/empty/empty.kicad_wks for comparison.
    """
    template = KiCadTemplates.worksheet()

    # Test serialization and deserialization
    sexpr = template.to_sexpr_str()
    reparsed = KicadWks.from_sexpr(sexpr)

    assert reparsed == template


def test_empty_project():
    """Test project template generation against fixture."""
    template = KiCadTemplates.project()

    # Verify it's a valid project object
    assert isinstance(template, KicadProject)

    # Test serialization and deserialization
    json_str = template.to_json_str()
    reparsed = KicadProject.from_str(json_str)

    # Compare JSON output instead of objects (due to _original_data differences)
    assert reparsed.to_json_str() == template.to_json_str()

    # Verify fixture can be loaded TODO
    # (The fixture is much more detailed than template, so we don't compare them)
    fixture = KicadProject.from_file(str(FIXTURES_DIR / "empty.kicad_pro"))
    assert isinstance(fixture, KicadProject)
    assert fixture.meta.filename == "empty.kicad_pro"
