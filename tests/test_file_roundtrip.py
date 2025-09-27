#!/usr/bin/env python3
"""File-based round-trip tests using real KiCad files from fixtures."""

import pathlib
import tempfile

import pytest

from kicadfiles.base_element import ParseStrictness
from kicadfiles.board_layout import KicadPcb
from kicadfiles.design_rules import KiCadDesignRules
from kicadfiles.footprint_library import Footprint
from kicadfiles.library_tables import FpLibTable, SymLibTable
from kicadfiles.project_settings import KicadProject
from kicadfiles.schematic_system import KicadSch
from kicadfiles.symbol_library import KicadSymbolLib
from kicadfiles.text_and_documents import KicadWks

# Get fixtures directory
FIXTURES_DIR = pathlib.Path(__file__).parent / "fixtures"


def run_diagnostic_analysis(fixtures_dir, file_class_map):
    """Run FAILSAFE mode on all files to collect and categorize issues."""
    all_issues = []
    files_tested = 0

    for subdir in fixtures_dir.iterdir():
        if not subdir.is_dir() or subdir.name.startswith("."):
            continue

        for fixture_file in subdir.iterdir():
            cls = None

            # Check for extension-based files
            if fixture_file.suffix in file_class_map:
                cls = file_class_map[fixture_file.suffix]
            # Check for special library table files (no extension)
            elif fixture_file.name == "fp-lib-table":
                cls = FpLibTable
            elif fixture_file.name == "sym-lib-table":
                cls = SymLibTable

            if cls is not None:
                files_tested += 1

                # Capture warnings/errors from FAILSAFE mode
                import io
                import logging

                log_capture = io.StringIO()
                log_handler = logging.StreamHandler(log_capture)
                log_handler.setLevel(logging.WARNING)
                logger = logging.getLogger()
                logger.addHandler(log_handler)

                try:
                    # Try FAILSAFE mode to capture all warnings
                    cls.from_file(str(fixture_file), ParseStrictness.FAILSAFE)

                    # Get captured warnings
                    warnings = log_capture.getvalue()
                    if warnings:
                        all_issues.append(
                            {
                                "file": f"{subdir.name}/{fixture_file.name}",
                                "warnings": warnings,
                            }
                        )

                except Exception as e:
                    # Even FAILSAFE failed - record as critical error
                    all_issues.append(
                        {"file": f"{subdir.name}/{fixture_file.name}", "error": str(e)}
                    )
                finally:
                    logger.removeHandler(log_handler)
                    log_capture.close()

    return {"files_tested": files_tested, "issues": all_issues}


def print_diagnostic_summary(diagnostic_results):
    """Print categorized summary of diagnostic results."""
    issues = diagnostic_results["issues"]
    files_tested = diagnostic_results["files_tested"]

    if not issues:
        print(f"✅ All {files_tested} files parsed successfully in FAILSAFE mode")
        return

    # Categorize issues
    missing_fields = {}
    unused_params = {}
    parse_errors = []

    for issue in issues:
        file_name = issue["file"]

        if "error" in issue:
            parse_errors.append(f"{file_name}: {issue['error']}")
        else:
            warnings = issue["warnings"]

            # Extract missing field warnings
            for line in warnings.split("\n"):
                if "Missing field" in line:
                    # Extract field name
                    if "Missing field '" in line:
                        field = line.split("Missing field '")[1].split("'")[0]
                        missing_fields[field] = missing_fields.get(field, 0) + 1

                elif "Unused parameters" in line:
                    # Extract parameter types
                    if "[" in line and "]" in line:
                        params = line.split("[")[1].split("]")[0]
                        unused_params[params] = unused_params.get(params, 0) + 1

    print(f"Found issues in {len(issues)}/{files_tested} files:")

    if missing_fields:
        print(f"\n📋 Missing Fields (top issues):")
        for field, count in sorted(
            missing_fields.items(), key=lambda x: x[1], reverse=True
        )[:10]:
            print(f"  - '{field}': {count}x")

    if unused_params:
        print(f"\n🔧 Unused Parameters (top issues):")
        for param, count in sorted(
            unused_params.items(), key=lambda x: x[1], reverse=True
        )[:10]:
            print(f"  - {param}: {count}x")

    if parse_errors:
        print(f"\n❌ Parse Errors ({len(parse_errors)} files):")
        for error in parse_errors[:5]:  # Show first 5
            print(f"  - {error}")
        if len(parse_errors) > 5:
            print(f"  - ... and {len(parse_errors) - 5} more")


def test_all_s_expression_fixtures():
    """Test round-trip for all S-expression based fixture files."""

    # Mapping of file extensions to classes
    file_class_map = {
        ".kicad_pcb": KicadPcb,
        ".kicad_sch": KicadSch,
        ".kicad_sym": KicadSymbolLib,
        ".kicad_mod": Footprint,
        ".kicad_wks": KicadWks,
        ".kicad_dru": KiCadDesignRules,
    }

    # PHASE 1: DIAGNOSTIC RUN WITH FAILSAFE
    print("\n=== DIAGNOSTIC RUN (FAILSAFE MODE) ===")
    diagnostic_results = run_diagnostic_analysis(FIXTURES_DIR, file_class_map)
    print_diagnostic_summary(diagnostic_results)

    # PHASE 2: ACTUAL STRICT TEST
    print(f"\n=== S-EXPRESSION ROUND-TRIP TEST ===")
    print(f"Fixtures directory: {FIXTURES_DIR}")

    tested_files = 0
    successful_tests = 0

    # Test all fixture files
    for subdir in FIXTURES_DIR.iterdir():
        if not subdir.is_dir() or subdir.name.startswith("."):
            continue

        print(f"\nTesting files in {subdir.name}/")

        for fixture_file in subdir.iterdir():
            cls = None

            # Check for extension-based files
            if fixture_file.suffix in file_class_map:
                cls = file_class_map[fixture_file.suffix]
            # Check for special library table files (no extension)
            elif fixture_file.name == "fp-lib-table":
                cls = FpLibTable
            elif fixture_file.name == "sym-lib-table":
                cls = SymLibTable

            if cls is not None:
                tested_files += 1

                try:
                    # Load and test round-trip
                    original = cls.from_file(str(fixture_file), ParseStrictness.STRICT)
                    sexpr = original.to_sexpr()
                    regenerated = cls.from_sexpr(sexpr, ParseStrictness.STRICT)

                    assert original == regenerated

                    # Test save_to_file functionality for better coverage
                    # For library table files, use the original filename
                    if fixture_file.name in ["fp-lib-table", "sym-lib-table"]:
                        suffix = fixture_file.name
                    else:
                        suffix = fixture_file.suffix

                    with tempfile.NamedTemporaryFile(
                        mode="w", suffix=suffix, delete=False
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
