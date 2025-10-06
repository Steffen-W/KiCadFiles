#!/usr/bin/env python3
"""Script to analyze NamedObject classes and their variables with types."""

import ast
import importlib.util
import os
import sys
from dataclasses import fields, is_dataclass
from pathlib import Path
from typing import Dict, List, Set, Tuple


def find_kicad_files(directory: str) -> List[Path]:
    """Find all Python files in the kicadfiles directory."""
    kicad_dir = Path(directory) / "kicadfiles"
    if not kicad_dir.exists():
        print(f"Directory {kicad_dir} does not exist!")
        return []

    return list(kicad_dir.glob("*.py"))


def extract_class_info_from_ast(file_path: Path) -> Dict[str, Dict]:
    """Extract class information using AST parsing."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content)
        classes_info = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if class inherits from NamedObject
                inherits_from_kicad = False
                for base in node.bases:
                    if isinstance(base, ast.Name) and base.id == "NamedObject":
                        inherits_from_kicad = True
                        break

                if inherits_from_kicad:
                    class_name = node.name
                    variables = {}

                    # Look for dataclass fields in annotations and __token_name__
                    token_name = None
                    for item in node.body:
                        if isinstance(item, ast.AnnAssign) and isinstance(
                            item.target, ast.Name
                        ):
                            var_name = item.target.id
                            if item.annotation:
                                type_str = (
                                    ast.unparse(item.annotation)
                                    if hasattr(ast, "unparse")
                                    else str(item.annotation)
                                )
                                variables[var_name] = type_str
                        elif isinstance(item, ast.Assign):
                            for target in item.targets:
                                if (
                                    isinstance(target, ast.Name)
                                    and target.id == "__token_name__"
                                ):
                                    if isinstance(item.value, ast.Constant):
                                        token_name = item.value.value

                    classes_info[class_name] = {
                        "file": str(file_path),
                        "variables": variables,
                        "token_name": token_name or class_name.lower(),
                    }

        return classes_info
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return {}


def extract_class_info_from_import(file_path: Path) -> Dict[str, Dict]:
    """Extract class information by importing the module."""
    try:
        # Add the parent directory to sys.path temporarily
        parent_dir = str(file_path.parent.parent)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)

        # Import the module
        module_name = f"kicadfiles.{file_path.stem}"
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None or spec.loader is None:
            return {}

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        classes_info = {}

        # Iterate through all objects in the module
        for name in dir(module):
            obj = getattr(module, name)

            # Check if it's a class that inherits from NamedObject
            if (
                isinstance(obj, type)
                and hasattr(obj, "__bases__")
                and any(base.__name__ == "NamedObject" for base in obj.__mro__)
            ):

                variables = {}

                # Check if it's a dataclass and get field information
                if is_dataclass(obj):
                    for field in fields(obj):
                        field_type = str(field.type)
                        # Clean up type strings
                        if hasattr(field.type, "__name__"):
                            field_type = field.type.__name__
                        elif hasattr(field.type, "_name"):
                            field_type = field.type._name
                        variables[field.name] = field_type
                else:
                    # For non-dataclass, try to get annotations
                    if hasattr(obj, "__annotations__"):
                        for var_name, var_type in obj.__annotations__.items():
                            type_str = str(var_type)
                            if hasattr(var_type, "__name__"):
                                type_str = var_type.__name__
                            variables[var_name] = type_str

                # Get token name
                token_name = getattr(obj, "__token_name__", name.lower())

                classes_info[name] = {
                    "file": str(file_path),
                    "variables": variables,
                    "token_name": token_name,
                }

        return classes_info

    except Exception as e:
        print(f"Error importing {file_path}: {e}")
        return {}


def analyze_kicad_classes(directory: str = ".") -> Dict[str, Dict]:
    """Analyze all NamedObject classes and their variables."""
    files = find_kicad_files(directory)
    all_classes = {}

    for file_path in files:
        print(f"Analyzing {file_path.name}...")

        # Try importing first (more accurate), fall back to AST parsing
        class_info = extract_class_info_from_import(file_path)
        if not class_info:
            class_info = extract_class_info_from_ast(file_path)

        all_classes.update(class_info)

    return all_classes


def print_class_analysis(
    classes: Dict[str, Dict], filter_single_variable: bool = False
):
    """Print the analysis results."""
    print("\n" + "=" * 80)
    print("KICAD OBJECT CLASSES ANALYSIS")
    print("=" * 80)

    # Sort classes by name
    sorted_classes = sorted(classes.items())

    single_var_classes = []

    for class_name, info in sorted_classes:
        variables = info["variables"]

        if filter_single_variable and len(variables) != 1:
            continue

        if len(variables) == 1:
            single_var_classes.append(class_name)

        print(f"\nclass {Path(info['file']).stem}.{class_name}: # {info['token_name']}")

        if not variables:
            print("  No variables found")
        else:
            for var_name, var_type in sorted(variables.items()):
                print(f"    {var_name}: {var_type}")

    print(f"\n" + "=" * 80)
    print(f"SUMMARY: Found {len(classes)} NamedObject classes")
    print(f"Classes with exactly 1 variable: {len(single_var_classes)}")

    if single_var_classes:
        print("\nClasses with single variable:")
        for class_name in sorted(single_var_classes):
            var_name, var_type = next(iter(classes[class_name]["variables"].items()))
            print(f"  {class_name}: {var_name} ({var_type})")


def main():
    """Main function to run the analysis."""
    import argparse

    parser = argparse.ArgumentParser(description="Analyze NamedObject classes")
    parser.add_argument(
        "--directory", "-d", default=".", help="Directory containing kicadfiles folder"
    )
    parser.add_argument(
        "--single-variable",
        "-s",
        action="store_true",
        help="Show only classes with exactly one variable",
    )

    args = parser.parse_args()

    classes = analyze_kicad_classes(args.directory)
    print_class_analysis(classes, args.single_variable)


if __name__ == "__main__":
    main()
