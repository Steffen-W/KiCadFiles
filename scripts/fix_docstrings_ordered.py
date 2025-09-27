#!/usr/bin/env python3
"""
Enhanced script to automatically add Args sections to KiCadObject class docstrings
based on dataclass field metadata with correct field order and (optional) markers.
"""

import ast
import re
import subprocess
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Tuple


class FieldInfo(NamedTuple):
    name: str
    description: str
    is_optional: bool


class DocstringFixer(ast.NodeVisitor):
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.lines = source_code.splitlines()
        self.fixes: List[Tuple[int, int, str]] = (
            []
        )  # (start_line, end_line, new_content)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        # Check if class inherits from KiCadObject
        inherits_from_kicad = False
        for base in node.bases:
            if isinstance(base, ast.Name) and base.id == "KiCadObject":
                inherits_from_kicad = True
                break

        if not inherits_from_kicad:
            self.generic_visit(node)
            return

        # Check if class has @dataclass decorator
        has_dataclass = False
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == "dataclass":
                has_dataclass = True
                break

        if not has_dataclass:
            self.generic_visit(node)
            return

        # Extract field information in correct order
        fields = self.extract_fields_ordered(node)
        if not fields:
            self.generic_visit(node)
            return

        # Get current docstring
        current_docstring = ast.get_docstring(node)
        if not current_docstring:
            self.generic_visit(node)
            return

        # Check if Args section already exists and is complete
        if self.has_complete_args_section(current_docstring, fields):
            self.generic_visit(node)
            return

        # Generate new docstring with Args section
        new_docstring = self.add_args_section(current_docstring, fields)

        # Find docstring location in source
        docstring_node = (
            node.body[0]
            if (
                node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
            )
            else None
        )

        if docstring_node:
            start_line = docstring_node.lineno - 1  # Convert to 0-based
            end_line = (
                docstring_node.end_lineno - 1
                if docstring_node.end_lineno
                else start_line
            )

            # Create replacement content
            indent = self.get_indent(start_line)
            replacement = f'{indent}"""{new_docstring}"""'

            self.fixes.append((start_line, end_line, replacement))

        self.generic_visit(node)

    def extract_fields_ordered(self, node: ast.ClassDef) -> List[FieldInfo]:
        """Extract field information in the order they appear in the class."""
        fields = []

        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                field_name = item.target.id

                # Skip private fields
                if field_name.startswith("_"):
                    continue

                # Look for field() call with metadata
                if isinstance(item.value, ast.Call):
                    description, is_optional = self.extract_field_info(item.value)
                    if description:
                        fields.append(FieldInfo(field_name, description, is_optional))

        return fields

    def extract_field_info(self, call: ast.Call) -> Tuple[Optional[str], bool]:
        """Extract description and optional status from field(metadata={...}) call."""
        if not (isinstance(call.func, ast.Name) and call.func.id == "field"):
            return None, False

        description = None
        is_optional = False

        # Look for metadata keyword argument
        for keyword in call.keywords:
            if keyword.arg == "metadata" and isinstance(keyword.value, ast.Dict):
                # Look for 'description' and 'required' keys in metadata dict
                for key, value in zip(keyword.value.keys, keyword.value.values):
                    if (
                        isinstance(key, ast.Constant)
                        and key.value == "description"
                        and isinstance(value, ast.Constant)
                        and isinstance(value.value, str)
                    ):
                        description = value.value
                    elif (
                        isinstance(key, ast.Constant)
                        and key.value == "required"
                        and isinstance(value, ast.Constant)
                        and value.value is False
                    ):
                        is_optional = True

        # Also check if the annotation indicates Optional
        if description and not is_optional:
            # This is a simplified check - could be enhanced to parse the full annotation
            is_optional = "Optional[" in str(call) or "None" in str(call)

        return description, is_optional

    def has_complete_args_section(
        self, docstring: str, fields: List[FieldInfo]
    ) -> bool:
        """Check if docstring already has a complete Args section."""
        # Look for Args section
        args_match = re.search(r"\n\s*Args:\s*\n", docstring)
        if not args_match:
            return False

        # Extract Args section content
        args_start = args_match.end()

        # Find end of Args section (next section or end of docstring)
        next_section = re.search(r"\n\s*[A-Z][a-z]+:\s*\n", docstring[args_start:])
        if next_section:
            args_content = docstring[args_start : args_start + next_section.start()]
        else:
            args_content = docstring[args_start:]

        # Check if all fields are documented
        for field_info in fields:
            if not re.search(rf"\n\s*{re.escape(field_info.name)}:", args_content):
                return False

        return True

    def add_args_section(self, docstring: str, fields: List[FieldInfo]) -> str:
        """Add or update Args section in docstring with correct order and optional markers."""
        # Remove existing Args section if present
        args_pattern = r'\n\s*Args:\s*\n.*?(?=\n\s*[A-Z][a-z]+:\s*\n|\n\s*"""|\Z)'
        cleaned_docstring = re.sub(args_pattern, "", docstring, flags=re.DOTALL)

        # Find insertion point (before closing or at end)
        insertion_point = len(cleaned_docstring.rstrip())

        # Generate Args section without indentation - let Black handle it
        args_lines = ["\n\nArgs:"]
        for field_info in fields:
            optional_marker = " (optional)" if field_info.is_optional else ""
            args_lines.append(
                f"    {field_info.name}: {field_info.description}{optional_marker}"
            )

        args_section = "\n".join(args_lines)

        # Insert Args section
        new_docstring = (
            cleaned_docstring.rstrip()
            + args_section
            + "\n"
            + cleaned_docstring[insertion_point:]
        )

        return new_docstring.strip() + "\n"

    def get_indent(self, line_num: int) -> str:
        """Get indentation of a line."""
        if line_num < len(self.lines):
            line = self.lines[line_num]
            return line[: len(line) - len(line.lstrip())]
        return ""

    def apply_fixes(self) -> str:
        """Apply all fixes and return modified source code."""
        if not self.fixes:
            return self.source_code

        # Sort fixes by line number (reverse order to avoid offset issues)
        self.fixes.sort(key=lambda x: x[0], reverse=True)

        lines = self.lines[:]

        for start_line, end_line, replacement in self.fixes:
            # Replace lines
            lines[start_line : end_line + 1] = [replacement]

        return "\n".join(lines)


def process_file(file_path: Path) -> bool:
    """Process a single Python file."""
    print(f"Processing {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        # Parse AST
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            print(f"  Syntax error in {file_path}: {e}")
            return False

        # Find and fix docstrings
        fixer = DocstringFixer(source_code)
        fixer.visit(tree)

        if not fixer.fixes:
            print(f"  No changes needed")
            return True

        # Apply fixes
        new_source = fixer.apply_fixes()

        # Write back
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_source)

        print(f"  Fixed {len(fixer.fixes)} docstring(s)")
        return True

    except Exception as e:
        print(f"  Error processing {file_path}: {e}")
        return False


def main():
    """Main function."""
    # Find kicadfiles directory relative to script location
    script_dir = Path(__file__).parent
    kicadfiles_dir = script_dir.parent / "kicadfiles"

    if not kicadfiles_dir.exists():
        print(f"Directory {kicadfiles_dir} not found!")
        return

    # Find all Python files
    python_files = list(kicadfiles_dir.glob("*.py"))

    if not python_files:
        print(f"No Python files found in {kicadfiles_dir}")
        return

    print(f"Found {len(python_files)} Python files")

    success_count = 0

    for file_path in python_files:
        if file_path.name.startswith("__"):
            continue  # Skip __init__.py, etc.

        if process_file(file_path):
            success_count += 1

    print(f"\nProcessed {success_count}/{len(python_files)} files successfully")

    # Run black formatter on the kicadfiles directory
    print("\nRunning Black formatter...")
    try:
        result = subprocess.run(
            ["black", str(kicadfiles_dir)], capture_output=True, text=True, check=True
        )
        print("Black formatting completed successfully")
        if result.stdout.strip():
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Black formatting failed: {e}")
        if e.stdout:
            print("stdout:", e.stdout)
        if e.stderr:
            print("stderr:", e.stderr)
    except FileNotFoundError:
        print("Black formatter not found. Please install with: pip install black")


if __name__ == "__main__":
    main()
