# KiCadFiles

A comprehensive Python library for parsing and manipulating KiCad file formats.

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![CI/CD](https://github.com/Steffen-W/KiCadFiles/workflows/CI%20Pipeline/badge.svg)](https://github.com/Steffen-W/KiCadFiles/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/kicadfiles.svg)](https://badge.fury.io/py/kicadfiles)
[![Documentation](https://img.shields.io/badge/docs-sphinx-blue.svg)](https://steffen-w.github.io/KiCadFiles/)
[![codecov](https://codecov.io/gh/Steffen-W/KiCadFiles/branch/master/graph/badge.svg)](https://codecov.io/gh/Steffen-W/KiCadFiles)

📚 **[View Full Documentation](https://steffen-w.github.io/KiCadFiles/)** - Complete API reference and examples

## Features

- **Complete KiCad S-expression support**: >200 classes representing KiCad tokens (missing tokens? [create an issue](https://github.com/Steffen-W/KiCadFiles/issues) with examples)
- **Type-safe parsing**: Full Python type hints for all classes and methods
- **Flexible error handling**: Three strictness modes (STRICT, FAILSAFE, SILENT)
- **Round-trip parsing**: Parse KiCad files and convert back to S-expressions
- **Minimal dependencies**: Self-contained S-expression parsing (no external dependencies)
- **Extensive testing**: Comprehensive test suite ensuring reliability

## Installation

```bash
pip install kicadfiles
```

## Quick Start

### Main File Format Classes

```python
from kicadfiles import (
    KicadPcb, KicadSch, Footprint, KicadWks, KicadSymbolLib,
    KicadProject, KiCadDesignRules, FpLibTable, SymLibTable,
    KiCadTemplates
)

# PCB board (.kicad_pcb)
pcb = KicadPcb.from_file("board.kicad_pcb")
# pcb.save_to_file("output.kicad_pcb")

# Schematic (.kicad_sch)
schematic = KicadSch.from_file("schematic.kicad_sch")
# schematic.save_to_file("output.kicad_sch")

# Footprint (.kicad_mod)
footprint = Footprint.from_file("component.kicad_mod")
# footprint.save_to_file("output.kicad_mod")

# Symbol library (.kicad_sym)
symbol_lib = KicadSymbolLib.from_file("library.kicad_sym")
# symbol_lib.save_to_file("output.kicad_sym")

# Worksheet (.kicad_wks)
worksheet = KicadWks.from_file("template.kicad_wks")
# worksheet.save_to_file("output.kicad_wks")

# Project settings (.kicad_pro)
project = KicadProject.from_file("project.kicad_pro")
# project.save_to_file("output.kicad_pro")

# Design rules (.kicad_dru)
design_rules = KiCAdDesignRules.from_file("rules.kicad_dru")
# design_rules.save_to_file("output.kicad_dru")

# Footprint library table
fp_lib_table = FpLibTable.from_file("fp-lib-table")
# fp_lib_table.save_to_file("output-fp-lib-table")

# Symbol library table
sym_lib_table = SymLibTable.from_file("sym-lib-table")
# sym_lib_table.save_to_file("output-sym-lib-table")
```

### Working with PCB Files

```python
from kicadfiles import KicadPcb, KiCadTemplates

# Load and modify existing PCB
pcb = KicadPcb.from_file("board.kicad_pcb")

# Access elements
for footprint in pcb.footprints:
    print(f"Footprint: {footprint.library_link} at ({footprint.at.x}, {footprint.at.y})")

# Create new PCB from template
new_pcb = KiCAdTemplates.pcb()
new_pcb.setup.pad_to_mask_clearance(0.05)
new_pcb.save_to_file("new_board.kicad_pcb")
```

## API Overview

### Core Classes

- **KiCadObject**: Base class for all KiCad objects
- **ParseStrictness**: Enum controlling error handling (STRICT, FAILSAFE, SILENT)

### Main File Format Classes

These classes represent complete KiCad file formats and support both `from_file()` and `save_to_file()` methods:

- **KicadSymbolLib**: Symbol library files (.kicad_sym)
- **KicadPcb**: PCB board files (.kicad_pcb)
- **KicadSch**: Schematic files (.kicad_sch)
- **KicadWks**: Worksheet files (.kicad_wks)
- **Footprint**: Individual footprint files (.kicad_mod)
- **KicadProject**: Project settings files (.kicad_pro)

### Main Object Categories

- **Base Types**: At, Size, Layer, Stroke, etc.
- **Text and Documents**: TitleBlock, Page, Comment, etc.
- **Pad and Drill**: Pad, Drill, Via, etc.
- **Graphics**: Line, Circle, Arc, Polygon, etc.
- **Symbol Library**: Symbol, Pin, Property, etc.
- **Footprint Library**: Footprint, Model, Tags, etc.
- **Zone System**: Zone, Hatch, FilledPolygon, etc.
- **Board Layout**: General, Layers, Nets, etc.
- **Schematic System**: Wire, Junction, Label, etc.

## Error Handling with Strictness Modes

```python
from kicadfiles import At, ParseStrictness

# STRICT mode: Raises exceptions for any parsing errors
try:
    at_obj = At.from_sexpr("(at 10.0 20.0)", ParseStrictness.STRICT)
except ValueError as e:
    print(f"Parsing failed: {e}")

# FAILSAFE mode: Logs warnings and uses defaults for missing fields
at_obj = At.from_sexpr("(at 10.0 20.0)", ParseStrictness.FAILSAFE)
print(f"Angle defaulted to: {at_obj.angle}")  # Output: 0.0

# SILENT mode: Silently uses defaults for missing fields
at_obj = At.from_sexpr("(at 10.0 20.0)", ParseStrictness.SILENT)
```

| Mode | Behavior |
|------|----------|
| **STRICT** | Raises `ValueError` on errors |
| **FAILSAFE** | Logs warnings, uses defaults |
| **SILENT** | Uses defaults silently |

For a complete overview of all classes and their module organization, see **[kicadfiles/CLASSES.md](kicadfiles/CLASSES.md)**.

## Development

### Setting up Development Environment

```bash
git clone https://github.com/Steffen-W/KiCadFiles.git
cd KiCadFiles
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/ -v
```

### Code Quality

```bash
# Format code
black .
isort .

# Linting
flake8 kicadfiles/

# Type checking
mypy kicadfiles/
pyright kicadfiles/
```

### Documentation with sphinx

```bash
cd docs && make clean && make html && cd ..
# Open docs/build/html/index.html in browser
```

### Coverage

```bash
pytest --cov=kicadfiles --cov-report=html tests/
# Open htmlcov/index.html in browser
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any problems or have questions, please open an issue on the [GitHub repository](https://github.com/Steffen-W/KiCadFiles/issues).
