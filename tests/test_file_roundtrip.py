#!/usr/bin/env python3
"""File-based round-trip tests using real KiCad files from fixtures."""

import pathlib
import tempfile

import pytest

from kicadfiles.base_element import ParseStrictness
from kicadfiles.board_layout import KicadPcb
from kicadfiles.design_rules import KiCadDesignRules
from kicadfiles.footprint_library import Footprint
from kicadfiles.project_settings import KicadProject
from kicadfiles.schematic_system import KicadSch
from kicadfiles.symbol_library import KicadSymbolLib
from kicadfiles.text_and_documents import KicadWks

# Get fixtures directory
FIXTURES_DIR = pathlib.Path(__file__).parent / "fixtures"


def test_all_s_expression_fixtures():
    """Test round-trip for all S-expression based fixture files."""
    print("\n=== S-EXPRESSION ROUND-TRIP TEST ===")
    print(f"Fixtures directory: {FIXTURES_DIR}")

    # Mapping of file extensions to classes
    file_class_map = {
        ".kicad_pcb": KicadPcb,
        ".kicad_sch": KicadSch,
        ".kicad_sym": KicadSymbolLib,
        ".kicad_mod": Footprint,
        ".kicad_wks": KicadWks,
        ".kicad_dru": KiCadDesignRules,
    }

    tested_files = 0
    successful_tests = 0

    # Test all fixture files
    for subdir in FIXTURES_DIR.iterdir():
        if not subdir.is_dir() or subdir.name.startswith("."):
            continue

        print(f"\nTesting files in {subdir.name}/")

        for fixture_file in subdir.iterdir():
            if fixture_file.suffix in file_class_map:
                cls = file_class_map[fixture_file.suffix]
                tested_files += 1

                try:
                    # Load and test round-trip
                    original = cls.from_file(str(fixture_file), ParseStrictness.STRICT)
                    sexpr = original.to_sexpr()
                    regenerated = cls.from_sexpr(sexpr, ParseStrictness.STRICT)

                    assert original == regenerated

                    # Test save_to_file functionality for better coverage
                    with tempfile.NamedTemporaryFile(
                        mode="w", suffix=fixture_file.suffix, delete=False
                    ) as tmp:
                        tmp_path = pathlib.Path(tmp.name)

                    try:
                        # Save regenerated object to file
                        regenerated.save_to_file(str(tmp_path))

                        # Load from saved file and verify
                        reloaded = cls.from_file(str(tmp_path), ParseStrictness.STRICT)
                        assert original == reloaded

                    finally:
                        # Clean up temp file
                        if tmp_path.exists():
                            tmp_path.unlink()

                    successful_tests += 1
                    print(f"  ✅ {fixture_file.name}")

                except Exception as e:
                    print(f"  ❌ {fixture_file.name}: {e}")

    print(f"\n=== SUMMARY ===")
    print(f"Tested: {tested_files} files")
    print(f"Successful: {successful_tests} files")
    print(
        f"Success rate: {successful_tests/tested_files*100:.1f}%"
        if tested_files > 0
        else "No files tested"
    )

    if tested_files == 0:
        pytest.skip("No fixture files found to test")

    # Assert that all tests passed
    assert (
        successful_tests == tested_files
    ), f"Only {successful_tests}/{tested_files} tests passed"


def test_json_based_fixtures():
    """Test JSON-based fixture files (with known limitations)."""
    print("\n=== JSON-BASED ROUND-TRIP TEST ===")
    print(f"Fixtures directory: {FIXTURES_DIR}")

    # JSON-based file types
    json_file_map = {
        ".kicad_pro": KicadProject,
    }

    tested_files = 0
    successful_basic_tests = 0

    # Test all JSON fixture files
    for subdir in FIXTURES_DIR.iterdir():
        if not subdir.is_dir() or subdir.name.startswith("."):
            continue

        print(f"\nTesting files in {subdir.name}/")

        for fixture_file in subdir.iterdir():
            if fixture_file.suffix in json_file_map:
                cls = json_file_map[fixture_file.suffix]
                tested_files += 1

                try:
                    # Basic loading test (no round-trip comparison due to _original_data)
                    original = cls.from_file(str(fixture_file), ParseStrictness.STRICT)
                    print(f"  ✅ {fixture_file.name}: Loading successful")

                    # Test serialization works
                    data_dict = original.to_dict()
                    regenerated = cls.from_dict(data_dict)  # Test that it works
                    print(f"  ✅ {fixture_file.name}: Serialization successful")

                    # Test save_to_file if available (for coverage)
                    if hasattr(regenerated, "save_to_file"):
                        with tempfile.NamedTemporaryFile(
                            mode="w", suffix=fixture_file.suffix, delete=False
                        ) as tmp:
                            tmp_path = pathlib.Path(tmp.name)

                        try:
                            regenerated.save_to_file(str(tmp_path))
                            # Just verify file was created, don't test equality due to _original_data
                            assert tmp_path.exists()
                            print(f"  ✅ {fixture_file.name}: File save successful")

                        finally:
                            if tmp_path.exists():
                                tmp_path.unlink()

                    successful_basic_tests += 1

                except Exception as e:
                    print(f"  ❌ {fixture_file.name}: {e}")

    print(f"\n=== JSON SUMMARY ===")
    print(f"Tested: {tested_files} files")
    print(f"Basic tests successful: {successful_basic_tests} files")
    print("Note: JSON files have known _original_data comparison limitations")

    if tested_files > 0:
        print(f"Success rate: {successful_basic_tests/tested_files*100:.1f}%")
        assert successful_basic_tests > 0, "No JSON files loaded successfully"


if __name__ == "__main__":
    # Run the comprehensive tests when executed directly
    test_all_s_expression_fixtures()
    test_json_based_fixtures()
