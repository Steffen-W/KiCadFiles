#!/usr/bin/env python3
"""Large test for recursive folder parsing of KiCad files."""

import pathlib
from typing import List, Tuple

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


def collect_files_by_type(test_folder: str) -> List[Tuple[str, pathlib.Path]]:
    """Collect all KiCad files grouped by type for parallel testing."""
    test_path = pathlib.Path(test_folder)

    if not test_path.exists():
        return []

    # Mapping of file extensions/names to classes
    file_class_map = {
        ".kicad_pcb": "KicadPcb",
        ".kicad_sch": "KicadSch",
        ".kicad_sym": "KicadSymbolLib",
        ".kicad_mod": "Footprint",
        ".kicad_wks": "KicadWks",
        ".kicad_dru": "KiCadDesignRules",
        ".kicad_pro": "KicadProject",
        "fp-lib-table": "FpLibTable",
        "sym-lib-table": "SymLibTable",
    }

    files_by_type = []

    # Recursively find all KiCad files
    for file_path in test_path.rglob("*"):
        if file_path.is_file():
            file_type = None

            # Check for extension-based files
            if file_path.suffix in file_class_map:
                file_type = file_class_map[file_path.suffix]
            # Check for special library table files (no extension)
            elif file_path.name in file_class_map:
                file_type = file_class_map[file_path.name]

            if file_type:
                files_by_type.append((file_type, file_path))

    return files_by_type


# USAGE EXAMPLES:
#
# Run grouped tests (slower, but with summary):
# pytest tests/large_test.py::test_file_type_parsing -k "KicadPcb" -n 16
# pytest tests/large_test.py::test_file_type_parsing -k "_large_test and KicadSch" -n 16
# pytest tests/large_test.py::test_file_type_parsing -k "not _large_test" -n 16
#
# Run individual file tests (faster, true parallelization on 16 cores):
# pytest tests/large_test.py::test_large_kicadpcb_individual -n 16
# pytest tests/large_test.py::test_large_kicadsch_individual -n 16
# pytest tests/large_test.py::test_large_footprint_individual -n 16
# pytest tests/large_test.py::test_large_kicadsymbollib_individual -n 16
# pytest tests/large_test.py::test_large_kicadwks_individual -n 16
# pytest tests/large_test.py::test_large_kicaddesignrules_individual -n 16
# pytest tests/large_test.py::test_large_kicadproject_individual -n 16
# pytest tests/large_test.py::test_large_fplibtable_individual -n 16
# pytest tests/large_test.py::test_large_symlibtable_individual -n 16
#
# List all available tests:
# pytest tests/large_test.py --collect-only
#
# Run all individual tests:
# pytest tests/large_test.py -k "_individual" -n 16
@pytest.mark.parametrize("test_folder", ["tests/fixtures", "_large_test"])
@pytest.mark.parametrize(
    "file_type",
    [
        "KicadPcb",
        "KicadSch",
        "KicadSymbolLib",
        "Footprint",
        "KicadWks",
        "KiCadDesignRules",
        "KicadProject",
        "FpLibTable",
        "SymLibTable",
    ],
)
def test_file_type_parsing(test_folder: str, file_type: str):
    """Test parsing of specific file type in parallel."""

    test_path = pathlib.Path(test_folder)

    if not test_path.exists():
        pytest.skip(f"Test folder {test_folder} does not exist")

    # Mapping of file types to classes
    type_class_map = {
        "KicadPcb": KicadPcb,
        "KicadSch": KicadSch,
        "KicadSymbolLib": KicadSymbolLib,
        "Footprint": Footprint,
        "KicadWks": KicadWks,
        "KiCadDesignRules": KiCadDesignRules,
        "KicadProject": KicadProject,
        "FpLibTable": FpLibTable,
        "SymLibTable": SymLibTable,
    }

    cls = type_class_map[file_type]

    # Collect all files of this type
    files_by_type = collect_files_by_type(test_folder)
    target_files = [
        file_path for ftype, file_path in files_by_type if ftype == file_type
    ]

    if not target_files:
        pytest.skip(f"No {file_type} files found in {test_folder}")

    parsed_files = []
    failed_files = []

    print(f"\n=== {file_type} PARSING TEST ===")
    print(f"Testing {len(target_files)} {file_type} files in {test_path}")

    # Parse all files of this type
    for file_path in target_files:
        try:
            # Parse the file
            parsed_obj = cls.from_file(str(file_path), ParseStrictness.FAILSAFE)

            # Try round-trip test
            if hasattr(parsed_obj, "to_sexpr"):
                # S-expression based files
                sexpr = parsed_obj.to_sexpr()
                reparsed_obj = cls.from_sexpr(sexpr, ParseStrictness.FAILSAFE)
            else:
                # JSON based files
                data_dict = parsed_obj.to_dict()
                reparsed_obj = cls.from_dict(data_dict)

            parsed_files.append(str(file_path.relative_to(test_path)))
            print(f"✅ {file_path.relative_to(test_path)}")

        except Exception as e:
            failed_files.append((str(file_path.relative_to(test_path)), str(e)))
            print(f"❌ {file_path.relative_to(test_path)}: {e}")

    # Summary
    print(f"\n=== {file_type} SUMMARY ===")
    print(f"✅ Parsed: {len(parsed_files)} files")
    print(f"❌ Failed: {len(failed_files)} files")

    if failed_files:
        print("\nFailed files:")
        for file_path, error in failed_files:
            print(f"  {file_path}: {error}")

    # Test should pass even if no files found for this type
    assert (
        len(target_files) == 0 or len(parsed_files) > 0
    ), f"Found {len(target_files)} {file_type} files but none parsed successfully"


def create_individual_file_tests(test_folder: str, file_type: str):
    """Create individual test functions for each file to enable true parallelization."""
    files_by_type = collect_files_by_type(test_folder)
    target_files = [
        file_path for ftype, file_path in files_by_type if ftype == file_type
    ]

    # Mapping of file types to classes
    type_class_map = {
        "KicadPcb": KicadPcb,
        "KicadSch": KicadSch,
        "KicadSymbolLib": KicadSymbolLib,
        "Footprint": Footprint,
        "KicadWks": KicadWks,
        "KiCadDesignRules": KiCadDesignRules,
        "KicadProject": KicadProject,
        "FpLibTable": FpLibTable,
        "SymLibTable": SymLibTable,
    }

    cls = type_class_map[file_type]

    # Create parametrized test for each file
    test_ids = [str(f.relative_to(pathlib.Path(test_folder))) for f in target_files]

    @pytest.mark.parametrize("file_path", target_files, ids=test_ids)
    def test_individual_file_parsing(file_path):
        """Test parsing of individual file for parallel execution."""
        try:
            # Parse the file
            parsed_obj = cls.from_file(str(file_path), ParseStrictness.FAILSAFE)

            # Try round-trip test
            if hasattr(parsed_obj, "to_sexpr"):
                # S-expression based files
                sexpr = parsed_obj.to_sexpr()
                reparsed_obj = cls.from_sexpr(sexpr, ParseStrictness.FAILSAFE)
            else:
                # JSON based files
                data_dict = parsed_obj.to_dict()
                reparsed_obj = cls.from_dict(data_dict)

            print(f"✅ {file_path}")

        except Exception as e:
            print(f"❌ {file_path}: {e}")
            raise

    return test_individual_file_parsing


# Generate individual tests for _large_test files by type
if pathlib.Path("_large_test").exists():
    files_by_type = collect_files_by_type("_large_test")

    # Mapping of file types to classes
    type_class_map = {
        "KicadPcb": KicadPcb,
        "KicadSch": KicadSch,
        "KicadSymbolLib": KicadSymbolLib,
        "Footprint": Footprint,
        "KicadWks": KicadWks,
        "KiCadDesignRules": KiCadDesignRules,
        "KicadProject": KicadProject,
        "FpLibTable": FpLibTable,
        "SymLibTable": SymLibTable,
    }

    # Create individual test functions for each file type
    for file_type, cls in type_class_map.items():
        target_files = [
            file_path for ftype, file_path in files_by_type if ftype == file_type
        ]

        if target_files:
            test_ids = [
                str(f.relative_to(pathlib.Path("_large_test"))) for f in target_files
            ]

            def create_test_function(file_type, cls, target_files, test_ids):
                @pytest.mark.parametrize("file_path", target_files, ids=test_ids)
                def test_function(file_path):
                    f"""Test individual {file_type} files from _large_test for parallel execution."""
                    try:
                        parsed_obj = cls.from_file(
                            str(file_path), ParseStrictness.FAILSAFE
                        )

                        # Try round-trip test
                        if hasattr(parsed_obj, "to_sexpr"):
                            sexpr = parsed_obj.to_sexpr()
                            reparsed_obj = cls.from_sexpr(
                                sexpr, ParseStrictness.FAILSAFE
                            )
                        else:
                            data_dict = parsed_obj.to_dict()
                            reparsed_obj = cls.from_dict(data_dict)

                        print(f"✅ {file_path}")
                    except Exception as e:
                        print(f"❌ {file_path}: {e}")
                        raise

                return test_function

            # Create the test function with a unique name
            test_func = create_test_function(file_type, cls, target_files, test_ids)
            test_func.__name__ = f"test_large_{file_type.lower()}_individual"
            globals()[test_func.__name__] = test_func


if __name__ == "__main__":
    # Run the test directly for a specific type
    test_file_type_parsing("_large_test", "Footprint")
