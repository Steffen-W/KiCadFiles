# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-09-21

### Added

- Initial release of KiCadFiles library
- Complete support for KiCad S-expression parsing with 207 classes
- Simplified parser strictness modes: STRICT, FAILSAFE, SILENT
- Comprehensive type safety with Python type hints
- Round-trip parsing capabilities (parse → modify → serialize)
- Zero external dependencies for core functionality
- Base object classes:
  - `KiCadObject`: Base class for all KiCad objects
  - `ParseStrictness`: Enum for error handling modes
- Object categories:
  - Base Types (37 classes): At, Size, Layer, Stroke, etc.
  - Text and Documents (27 classes): TitleBlock, Page, Comment, etc.
  - Pad and Drill (18 classes): Pad, Drill, Via, etc.
  - Graphics (28 classes): Line, Circle, Arc, Polygon, etc.
  - Symbol Library (15 classes): Symbol, Pin, Property, etc.
  - Footprint Library (12 classes): Footprint, Model, Tags, etc.
  - Zone System (28 classes): Zone, Hatch, FilledPolygon, etc.
  - Board Layout (15 classes): General, Layers, Nets, etc.
  - Schematic System (13 classes): Wire, Junction, Label, etc.
- S-Expression parser utilities:
  - `str_to_sexpr()`: Parse strings to S-expressions
  - `sexpr_to_str()`: Convert S-expressions back to strings
  - `SExprParser`: Low-level parser class

### Features

- **Flexible Error Handling**: Three levels of strictness for different use cases
  - STRICT: Raises exceptions for any parsing errors
  - FAILSAFE: Logs warnings and uses defaults for missing fields
  - SILENT: Silently uses defaults without warnings
- **Type Safety**: Full Python type hints throughout the codebase
- **Pretty Printing**: S-expressions can be formatted for human readability
- **Dataclass Integration**: All objects are Python dataclasses with standard features
- **Memory Efficient**: Optimized parsing with cursor-based approach

### Documentation

- Comprehensive README with usage examples
- API documentation in docstrings
- Type hints for IDE support
- Example scripts in `examples/` directory

### Development Tools

- PyPI-ready package configuration
- Development dependencies for testing and linting
- GitHub-ready project structure
- MIT License

## [Unreleased]

### Changed

- Renamed base classes for better clarity and consistency:
  - `KiCadPrimitive` → `NamedValue`
  - `KiCadObject` → `NamedObject`
  - `KiCadStr` → `NamedString`
  - `KiCadInt` → `NamedInt`
  - `KiCadFloat` → `NamedFloat`
  - `OptionalFlag` → `TokenFlag`
  - `OptionalSimpleFlag` → `SymbolValue`
  - `OptionalFlagBase` → `TokenBase`
- Changed `Optional[ComplexType]` fields from `default=None` to `default_factory=lambda: ComplexType()` for proper initialization:
  - Affected classes: `General`, `BoardLayers`, `Setup`, `Keepout`, `Mid`, `Stroke`, `Fill`, `At`, `Effects`, `Uuid`, `ERCSettings`
  - Enum types (e.g., `LabelShape`, `ZoneConnection`) remain with `default=None`
  - Ensures all complex type fields are properly initialized with default instances

### Planned

- Extended test suite
- Documentation website
- More usage examples
- Performance optimizations
- Additional utility functions for common KiCad operations