#!/usr/bin/env python3
"""Comprehensive round-trip test for all KiCad classes."""

import inspect
from dataclasses import fields
from typing import get_args, get_origin

import kicadfiles
from kicadfiles.base_element import KiCadObject, ParseStrictness


def get_all_kicad_classes():
    """Get all KiCadObject classes from kicadfiles."""
    classes = []

    # Get all exported classes from __all__
    for name in kicadfiles.__all__:
        obj = getattr(kicadfiles, name)

        # Check if it's a class and inherits from KiCadObject
        if (
            inspect.isclass(obj) and issubclass(obj, KiCadObject) and obj != KiCadObject
        ):  # Exclude base class
            classes.append(obj)

    return sorted(classes, key=lambda cls: cls.__name__)


def create_default_instance(cls):
    """Create a default instance of a KiCad class."""
    try:
        # Try to create with all defaults
        return cls()
    except Exception as e:
        print(f"  ❌ Could not create default instance: {e}")
        return None


def run_class_round_trip(cls):
    """Test round-trip for a single KiCad class."""
    print(f"\n--- Testing {cls.__name__} ---")

    # Create default instance
    original = create_default_instance(cls)
    if original is None:
        return False

    print(f"  ✅ Created instance: {original}")

    try:
        # Convert to S-expression
        sexpr = original.to_sexpr()
        print(f"  ✅ Serialized: {sexpr}")

        # Try STRICT mode first
        try:
            regenerated = cls.from_sexpr(sexpr, ParseStrictness.STRICT)
            print(f"  ✅ Parsed back (STRICT): {regenerated}")
            parsing_mode = "STRICT"
        except Exception:
            # If STRICT fails, try FAILSAFE mode
            try:
                regenerated = cls.from_sexpr(sexpr, ParseStrictness.FAILSAFE)
                print(f"  ✅ Parsed back (FAILSAFE): {regenerated}")
                parsing_mode = "FAILSAFE"
            except Exception as e2:
                print(f"  ❌ Parsing failed in both STRICT and FAILSAFE modes: {e2}")
                return False

        # Test equality
        are_equal = original == regenerated

        if are_equal:
            print(f"  ✅ Round-trip successful for {cls.__name__} ({parsing_mode})")
            return True
        else:
            print(
                f"  ❌ Round-trip failed for {cls.__name__}: objects not equal ({parsing_mode})"
            )

            # Debug differences
            print(f"    Original:    {original}")
            print(f"    Regenerated: {regenerated}")

            # Compare field by field
            field_infos = original._classify_fields()
            for field_info in field_infos:
                orig_val = getattr(original, field_info.name)
                regen_val = getattr(regenerated, field_info.name)
                if orig_val != regen_val:
                    print(f"    Diff in {field_info.name}: {orig_val} != {regen_val}")

            return False

    except Exception as e:
        print(f"  ❌ Round-trip failed for {cls.__name__}: {e}")
        return False


def test_all_classes():
    """Test round-trip for all KiCad classes."""
    print("=== COMPREHENSIVE ROUND-TRIP TEST FOR ALL KICAD CLASSES ===")
    print(f"KiCadFiles version: {kicadfiles.__version__}")

    # Get all classes
    classes = get_all_kicad_classes()
    print(f"Found {len(classes)} KiCad classes to test")

    # Track results
    passed = []
    failed = []
    skipped = []

    # Test each class
    for cls in classes:
        try:
            success = run_class_round_trip(cls)
            if success:
                passed.append(cls.__name__)
            else:
                failed.append(cls.__name__)
        except Exception as e:
            print(f"\n--- Testing {cls.__name__} ---")
            print(f"  ❌ Exception during test: {e}")
            skipped.append((cls.__name__, str(e)))

    # Print summary
    print("\n" + "=" * 60)
    print("ROUND-TRIP TEST SUMMARY")
    print("=" * 60)

    print(f"\n✅ PASSED ({len(passed)}):")
    for name in passed:
        print(f"  - {name}")

    if failed:
        print(f"\n❌ FAILED ({len(failed)}):")
        for name in failed:
            print(f"  - {name}")

    if skipped:
        print(f"\n⚠️  SKIPPED ({len(skipped)}):")
        for name, reason in skipped:
            print(f"  - {name}: {reason}")

    print(f"\nTotal: {len(classes)} classes")
    print(
        f"Success rate: {len(passed)}/{len(classes)} ({100*len(passed)/len(classes):.1f}%)"
    )

    # Overall result
    success = len(failed) == 0 and len(skipped) == 0
    if success:
        print("\n🎉 ALL TESTS PASSED! 🎉")
    else:
        print(f"\n⚠️  {len(failed)} failures, {len(skipped)} skipped")
        # Use assert for pytest compatibility
        assert success, f"{len(failed)} failures, {len(skipped)} skipped"


def test_specific_classes():
    """Test specific classes that are commonly used."""
    print("\n=== TESTING SPECIFIC IMPORTANT CLASSES ===")

    # Import specific classes for targeted testing
    from kicadfiles.base_types import At, Layer, Size, Xy
    from kicadfiles.pad_and_drill import Net
    from kicadfiles.text_and_documents import Generator, Version

    important_classes = [At, Layer, Size, Xy, Version, Generator, Net]

    for cls in important_classes:
        run_class_round_trip(cls)


def test_parser_strictness_modes():
    """Test that different parser strictness modes work correctly."""
    print("\n=== TESTING PARSER STRICTNESS MODES ===")

    from kicadfiles.base_types import At

    # Create a test object
    at_obj = At(x=10.0, y=20.0, angle=90.0)
    sexpr = at_obj.to_sexpr()

    print(f"Testing with S-expression: {sexpr}")

    # Test each strictness mode
    for mode in [
        ParseStrictness.STRICT,
        ParseStrictness.FAILSAFE,
        ParseStrictness.SILENT,
    ]:
        try:
            parsed = At.from_sexpr(sexpr, mode)
            print(f"  ✅ {mode.value}: {parsed}")
        except Exception as e:
            print(f"  ❌ {mode.value}: {e}")


def run_all_tests_and_return_result():
    """Run all tests and return success status (for __main__ usage)."""
    print("KiCadFiles - Comprehensive Round-Trip Testing")
    print("=" * 50)

    # Test parser strictness modes
    test_parser_strictness_modes()

    # Test important classes first
    test_specific_classes()

    # Get all classes and run tests
    classes = get_all_kicad_classes()
    passed = []
    failed = []
    skipped = []

    for cls in classes:
        try:
            success = run_class_round_trip(cls)
            if success:
                passed.append(cls.__name__)
            else:
                failed.append(cls.__name__)
        except Exception as e:
            print(f"\n--- Testing {cls.__name__} ---")
            print(f"  ❌ Exception during test: {e}")
            skipped.append((cls.__name__, str(e)))

    # Return success status
    return len(failed) == 0 and len(skipped) == 0


if __name__ == "__main__":
    success = run_all_tests_and_return_result()

    if success:
        print("\n🎉 All round-trip tests completed successfully!")
        exit(0)
    else:
        print("\n❌ Some tests failed. Check output above for details.")
        exit(1)
