# KiCadFiles

A comprehensive Python library for parsing and manipulating KiCad file formats.

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![CI/CD](https://github.com/Steffen-W/KiCadFiles/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/Steffen-W/KiCadFiles/actions)
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

### Basic Usage

```python
from kicadfiles import At, Layer, Footprint, ParseStrictness

# Create objects using dataclass syntax
position = At(x=10.0, y=20.0, angle=90.0)
layer = Layer(name="F.Cu")

# Parse from S-expression
at_obj = At.from_sexpr("(at 10.0 20.0 90.0)", ParseStrictness.STRICT)

# Convert back to S-expression string
sexpr_str = at_obj.to_sexpr_str()
print(sexpr_str)  # Output: (at 10.0 20.0 90.0)
```

### Parsing with Different Strictness Modes

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

### Working with Complex Objects

```python
from kicadfiles import Footprint, Pad, At, Size

# Create a footprint with pads
footprint = Footprint(
    library_link="Resistor_SMD:R_0603",
    at=At(x=50.0, y=30.0, angle=0.0),
    pads=[
        Pad(
            number="1",
            type="smd",
            shape="roundrect",
            at=At(x=-0.8, y=0.0),
            size=Size(width=0.7, height=0.9)
        ),
        Pad(
            number="2",
            type="smd",
            shape="roundrect",
            at=At(x=0.8, y=0.0),
            size=Size(width=0.7, height=0.9)
        )
    ]
)

# Convert to S-expression
sexpr = footprint.to_sexpr_str()
print(sexpr)
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

- **Base Types** (37 classes): At, Size, Layer, Stroke, etc.
- **Text and Documents** (27 classes): TitleBlock, Page, Comment, etc.
- **Pad and Drill** (18 classes): Pad, Drill, Via, etc.
- **Graphics** (28 classes): Line, Circle, Arc, Polygon, etc.
- **Symbol Library** (15 classes): Symbol, Pin, Property, etc.
- **Footprint Library** (12 classes): Footprint, Model, Tags, etc.
- **Zone System** (28 classes): Zone, Hatch, FilledPolygon, etc.
- **Board Layout** (15 classes): General, Layers, Nets, etc.
- **Schematic System** (13 classes): Wire, Junction, Label, etc.

## Error Handling

| Mode | Behavior |
|------|----------|
| **STRICT** | Raises `ValueError` on errors |
| **FAILSAFE** | Logs warnings, uses defaults |
| **SILENT** | Uses defaults silently |

```python
from kicadfiles import At, ParseStrictness

# STRICT: Will raise ValueError for missing angle
at_obj = At.from_sexpr("(at 10.0 20.0)", ParseStrictness.STRICT)

# FAILSAFE: Logs warning, angle defaults to 0.0
at_obj = At.from_sexpr("(at 10.0 20.0)", ParseStrictness.FAILSAFE)
```

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

### Code Formatting

```bash
# Complete pipeline (recommended)
black .
isort .
flake8 kicadfiles
pyright kicadfiles
mypy kicadfiles
```

### Linting

```bash
flake8 kicadfiles/
```

### Type Checking

```bash
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
