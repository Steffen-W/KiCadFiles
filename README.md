# KiCadFiles

A comprehensive Python library for parsing and manipulating KiCad file formats.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/kicadfiles.svg)](https://badge.fury.io/py/kicadfiles)

## Features

- **Complete KiCad S-expression support**: 207 classes representing all KiCad tokens
- **Type-safe parsing**: Full Python type hints for all classes and methods
- **Flexible error handling**: Three strictness modes (STRICT, FAILSAFE, SILENT)
- **Round-trip parsing**: Parse KiCad files and convert back to S-expressions
- **Minimal dependencies**: Uses only `sexpdata` from https://github.com/jd-boyd/sexpdata for S-expression parsing
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
sexpr_str = at_obj.to_sexpr_str(pretty_print=False)
print(sexpr_str)  # Output: ("at" ("x" 10.0) ("y" 20.0) ("angle" 90.0))
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
print(f"Angle defaulted to: {at_obj.angle}")  # Output: None

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
sexpr = footprint.to_sexpr_str(pretty_print=True)
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

The library provides three levels of error handling:

1. **STRICT**: Raises `ValueError` for any parsing errors
2. **FAILSAFE**: Logs warnings and uses default values for missing fields
3. **SILENT**: Silently uses default values without warnings

```python
# Handle parsing errors gracefully
from kicadfiles import Footprint, ParseStrictness
import logging

logging.basicConfig(level=logging.WARNING)

# This will log warnings but continue parsing
footprint = Footprint.from_sexpr(
    "(footprint incomplete_data)",
    ParseStrictness.FAILSAFE
)
```

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
black kicadfiles/
isort kicadfiles/
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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any problems or have questions, please open an issue on the [GitHub repository](https://github.com/Steffen-W/KiCadFiles/issues).
