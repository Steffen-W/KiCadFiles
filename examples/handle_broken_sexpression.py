#!/usr/bin/env python3
"""
Handle Broken S-Expressions Example

This example demonstrates how the KiCad S-expression parser detects and handles
various bracket/parentheses errors with informative error messages.
"""

from kicadfiles.sexpr_parser import str_to_sexpr


def test_bracket_errors() -> None:
    """Test various bracket/parentheses errors and show error messages."""

    error_cases = [
        # Missing closing brackets
        ("Missing closing bracket", "(font (size 2 2) bold"),
        ("Nested missing bracket", "(via (at 10 20) (size 0.5"),
        ("Complex missing bracket", "(font (size 2 2"),
        # Extra closing brackets
        ("Extra closing bracket", "(font (size 2 2) bold))"),
        ("Multiple extra brackets", "(at 10 20)))"),
        # Mismatched brackets
        ("Mismatched nested", "(font (size 2 2 bold)"),
        ("Complex mismatch", "(via (at 10 20) (drill 0.3) (layers F.Cu B.Cu"),
    ]

    valid_cases = [
        # These should work fine
        ("Empty expression", "()"),
        ("Empty nested", "(font ())"),
        ("Brackets in string", '(text "Hello (world)")'),
        ("Valid expression", "(at 10 20 90)"),
    ]

    print("=== BRACKET ERROR DETECTION ===\n")

    # Test error cases
    for name, expr in error_cases:
        print(f"[TEST] {name}:")
        print(f"   Input: {expr}")
        try:
            result = str_to_sexpr(expr)
            print(f"   [WARN] Unexpectedly parsed: {result}")
        except Exception as e:
            error_msg = str(e)
            # Extract key info from error message
            if "Not enough closing brackets" in error_msg:
                print(f"   [ERROR] Missing closing bracket detected")
            elif "Too many closing brackets" in error_msg:
                print(f"   [ERROR] Extra closing bracket detected")
            else:
                print(f"   [ERROR] Other error: {type(e).__name__}")

            # Show position info if available
            if "column" in error_msg:
                import re

                match = re.search(r"column (\d+)", error_msg)
                if match:
                    col = int(match.group(1))
                    print(f"   [POS] Position: column {col}")
        print()

    print("=== VALID EXPRESSIONS (SHOULD WORK) ===\n")

    # Test valid cases
    for name, expr in valid_cases:
        print(f"[OK] {name}:")
        print(f"   Input: {expr}")
        try:
            result = str_to_sexpr(expr)
            print(f"   Result: {result}")
        except Exception as e:
            print(f"   [ERROR] Unexpected error: {e}")
        print()


def demonstrate_error_recovery() -> None:
    """Show how to handle parsing errors gracefully."""

    print("=== ERROR HANDLING EXAMPLE ===\n")

    expressions = [
        "(font (size 2 2) bold)",  # Valid
        "(font (size 2 2) bold",  # Invalid - missing bracket
        "(font (size 2 2) bold))",  # Invalid - extra bracket
        "(at 10 20 90)",  # Valid
    ]

    for expr in expressions:
        print(f"Processing: {expr}")
        try:
            parsed = str_to_sexpr(expr)
            print(f"[OK] Success: {parsed}")
        except ValueError as e:
            if "closing brackets" in str(e):
                print(f"[ERROR] Bracket error: {str(e).split('.')[0]}")
            else:
                print(f"[ERROR] Parse error: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected error: {type(e).__name__}: {e}")
        print()


if __name__ == "__main__":
    print("KiCad S-Expression Bracket Error Handling Demo")
    print("=" * 50)
    print()

    test_bracket_errors()
    demonstrate_error_recovery()

    print("=" * 50)
    print("Key takeaways:")
    print("- All bracket errors are detected with precise error messages")
    print("- Error messages include line and column information")
    print("- Parser fails fast and cleanly without crashes")
    print("- Brackets inside strings are handled correctly")
    print("- Empty expressions are valid and parse to empty lists")
