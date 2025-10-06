# base_element.py - Documentation

## Overview

`base_element.py` is the foundation of the KiCadFiles library. It defines the base classes and parser infrastructure for all KiCad S-Expression objects.

## Architecture

### Class Hierarchy

```
SExpressionBase (ABC)
├── NamedValue (ABC)
│   ├── NamedString
│   ├── NamedInt
│   └── NamedFloat
├── TokenBase
│   ├── TokenFlag
│   └── SymbolValue
└── NamedObject (ABC)
    └── [All KiCad file formats]
```

## Core Classes

### 1. SExpressionBase

**Purpose**: Abstract base class for all S-expression parseable/serializable types.

**Interface**:
```python
class SExpressionBase(ABC):
    __token_name__: ClassVar[str] = ""  # Class-level token name

    @classmethod
    @abstractmethod
    def from_sexpr(cls, sexpr, strictness, cursor) -> Self:
        """Parse from S-expression."""

    @abstractmethod
    def to_sexpr(self) -> Union[List, str]:
        """Serialize to S-expression."""
```

**Usage**: All KiCad types must inherit from this class and implement both methods.

---

### 2. NamedValue

**Purpose**: Wrapper for primitive KiCad values (strings, integers, floats) with optional token names.

#### Properties

```python
@dataclass(eq=False)
class NamedValue(SExpressionBase):
    token: str = ""           # Token name (can be set per instance)
    value: Any = None         # The actual value
    base_type: ClassVar[type] # Type of value (str/int/float)
```

#### Formats

**Named Format**: `(token_name value)`
```python
# S-expression: (layer "F.Cu")
layer = NamedString.from_sexpr(['layer', 'F.Cu'])
# → NamedString(token='layer', value='F.Cu')
```

**Positional Format**: `value`
```python
# S-expression: 1.27
size = NamedFloat.from_sexpr(1.27)
# → NamedFloat(token='', value=1.27)
```

#### Subclasses

```python
# String values
NamedString(token: str, value: str)
# Example: NamedString('layer', 'F.Cu')

# Integer values
NamedInt(token: str, value: int)
# Example: NamedInt('width', 2)

# Float values
NamedFloat(token: str, value: float)
# Example: NamedFloat('size', 1.27)
```

#### Usage

```python
# Create manually
layer = NamedString(token='layer', value='F.Cu')

# Parse from S-expression
layer = NamedString.from_sexpr(['layer', 'F.Cu'])

# Serialize to S-expression
sexpr = layer.to_sexpr()  # → ['layer', 'F.Cu']

# Boolean conversion
if layer:  # True if value is not empty
    print(layer.value)
```

---

### 3. TokenFlag

**Purpose**: Represents optional flags with optional values.

#### Properties

```python
@dataclass(eq=False)
class TokenFlag(TokenBase):
    token: str                    # Flag name
    token_value: Optional[str]    # Optional value
```

#### Formats

**Flag only**: `(flag)`
```python
# S-expression: (locked)
flag = TokenFlag.from_sexpr(['locked'])
# → TokenFlag(token='locked', token_value=None)
```

**Flag with value**: `(flag value)`
```python
# S-expression: (hide yes)
flag = TokenFlag.from_sexpr(['hide', 'yes'])
# → TokenFlag(token='hide', token_value='yes')
```

#### Important Constraints

`TokenFlag` supports **only simple flags** with at most 2 elements:
- ✅ `(token)` - 1 element
- ✅ `(token value)` - 2 elements with simple value
- ❌ `(token value1 value2)` - More than 2 elements → ERROR
- ❌ `(token (nested list))` - Nested list → ERROR

Nested S-expressions like `(fill (type none))` are **NOT** TokenFlags and must use their own classes (e.g., `Fill`).

#### Validation

In **STRICT mode**, invalid structures are rejected:

```python
# ERROR: Too many elements
TokenFlag.from_sexpr(['at', '10', '20', '90'])
# → ValueError: TokenFlag 'at' has 4 elements, max 2 allowed

# ERROR: Nested list
TokenFlag.from_sexpr(['fill', ['type', 'none']])
# → ValueError: TokenFlag 'fill' has nested list - use proper class instead
```

In **FAILSAFE mode**, warnings are logged and parsing continues.

#### Usage

```python
# Create manually
locked = TokenFlag(token='locked', token_value=None)
hide = TokenFlag(token='hide', token_value='yes')

# Parse from S-expression
locked = TokenFlag.from_sexpr(['locked'])
hide = TokenFlag.from_sexpr(['hide', 'yes'])

# Serialize to S-expression
locked.to_sexpr()  # → ['locked']
hide.to_sexpr()    # → ['hide', 'yes']

# Boolean conversion
if hide:  # True if token_value in ('yes', 'true', '1') OR presence
    print("Hidden!")
```

---

### 4. SymbolValue

**Purpose**: Simple symbol flags without values (e.g., `oval`, `locked`).

#### Properties

```python
@dataclass(eq=False)
class SymbolValue(TokenBase):
    token: str  # Symbol name
```

#### Format

**Symbol only**: `symbol`
```python
# S-expression: oval
flag = SymbolValue.from_sexpr('oval')
# → SymbolValue(token='oval')
```

#### Difference from TokenFlag

| Property | TokenFlag | SymbolValue |
|----------|--------------|-------------------|
| Format | `(token)` or `(token value)` | `symbol` (no parentheses!) |
| Value | Optional | Never |
| Usage | Named tokens with optional value | Standalone symbols |

#### Usage

```python
# Create manually
oval = SymbolValue(token='oval')

# Parse from S-expression
oval = SymbolValue.from_sexpr('oval')

# Serialize to S-expression
oval.to_sexpr()  # → 'oval'

# Boolean conversion
if oval:  # Always True if instance exists
    print("Oval shape")
```

---

### 5. NamedObject

**Purpose**: Base class for all complex KiCad objects (PCBs, schematics, symbols, etc.).

#### Properties

```python
@dataclass
class NamedObject(SExpressionBase):
    __token_name__: ClassVar[str] = ""  # Class-level token name

    # All fields are defined via dataclass fields
```

#### Parsing Mechanism

NamedObject implements a generic parser that:

1. **Classifies fields** (NamedValue, NamedObject, List, TokenFlag, etc.)
2. **Delegates** to subclasses via `from_sexpr()`
3. **Handles errors** based on strictness level
4. **Detects unused tokens** for validation

#### Field Types

```python
class FieldType(Enum):
    PRIMITIVE = "primitive"                    # int, str, float, bool, Enum
    KICAD_PRIMITIVE = "kicad_primitive"        # NamedString, NamedInt, NamedFloat
    OPTIONAL_KICAD_PRIMITIVE = "optional_kicad_primitive"
    KICAD_OBJECT = "kicad_object"              # Nested NamedObject
    OPTIONAL_KICAD_OBJECT = "optional_kicad_object"
    OPTIONAL_FLAG = "optional_flag"             # TokenFlag
    OPTIONAL_SIMPLE_FLAG = "optional_simple_flag"  # SymbolValue
    LIST = "list"                              # List[...]
```

#### Usage

```python
@dataclass
class MyNamedObject(NamedObject):
    __token_name__: ClassVar[str] = "my_object"

    # Required fields
    name: NamedString = field(default_factory=lambda: NamedString("name", ""))

    # Optional fields
    locked: Optional[TokenFlag] = None
    layer: Optional[NamedString] = None

    # Lists
    points: List[Point] = field(default_factory=list)

# Parse
obj = MyNamedObject.from_sexpr(sexpr, ParseStrictness.STRICT)

# Serialize
sexpr = obj.to_sexpr()
```

---

## Parse Infrastructure

### ParseStrictness

Controls behavior on parse errors:

```python
class ParseStrictness(Enum):
    STRICT = "strict"        # Error → Exception
    FAILSAFE = "failsafe"    # Error → Log warning, continue
    SILENT = "silent"        # Error → Ignore, continue
```

**Usage**:
```python
# Strict: Abort on errors
obj = KicadSch.from_file('file.kicad_sch', ParseStrictness.STRICT)

# Failsafe: Log errors but continue parsing
obj = KicadSch.from_file('file.kicad_sch', ParseStrictness.FAILSAFE)

# Silent: Ignore errors
obj = KicadSch.from_file('file.kicad_sch', ParseStrictness.SILENT)
```

---

### ParseCursor

Tracking object during parsing:

```python
@dataclass
class ParseCursor:
    sexpr: SExpr                   # Current S-expression
    parser: SExprParser            # Parser for usage tracking
    path: List[str]                # Path for debugging
    strictness: ParseStrictness    # Strictness level

    def log_issue(self, message: str):
        """Log parse issue based on strictness."""

    def enter(self, sexpr: SExpr, name: str) -> ParseCursor:
        """Create cursor for nested object."""
```

**Internal usage**:
```python
@classmethod
def from_sexpr(cls, sexpr, strictness):
    cursor = ParseCursor(
        sexpr=sexpr,
        parser=SExprParser(sexpr),
        path=[cls.__token_name__],
        strictness=strictness
    )
    return cls._parse_from_cursor(cursor)
```

---

### SExprParser

Tracks which tokens have been used:

```python
class SExprParser:
    def __init__(self, sexpr: SExpr):
        self.sexpr = sexpr
        self.used_indices: Set[int] = set()

    def mark_used(self, index: int):
        """Mark index as used."""

    def get_unused_tokens(self) -> List[Tuple[int, Any]]:
        """Get all unused tokens."""
```

**Purpose**: Detects unknown/unused tokens for validation.

---

## Best Practices

### 1. Define Optional Fields Correctly

```python
@dataclass
class MyClass(NamedObject):
    # ✅ CORRECT: Optional with None default
    locked: Optional[TokenFlag] = None
    layer: Optional[NamedString] = None

    # ❌ WRONG: Non-optional but None default
    name: NamedString = None  # → Parse error if not found

    # ✅ CORRECT: Required field with default factory
    name: NamedString = field(default_factory=lambda: NamedString("name", ""))
```

### 2. Initialize Lists

```python
@dataclass
class MyClass(NamedObject):
    # ✅ CORRECT: default_factory for lists
    points: List[Point] = field(default_factory=list)

    # ❌ WRONG: Mutable default
    points: List[Point] = []  # Shared between instances!
```

### 3. Use Nested Structures

```python
# ❌ WRONG: TokenFlag for complex structure
fill: TokenFlag  # (fill (type none)) → Nested!

# ✅ CORRECT: Own class for complex structure
@dataclass
class Fill(NamedObject):
    __token_name__: ClassVar[str] = "fill"
    type: Type = field(default_factory=lambda: Type("none"))

fill: Optional[Fill] = None
```

### 4. Use Token Names Consistently

```python
@dataclass
class MyClass(NamedObject):
    __token_name__: ClassVar[str] = "my_class"  # Class level

    # Field-level token names
    name: NamedString = field(
        default_factory=lambda: NamedString("name", "")
    )
```

---

## Serialization

### Rules

1. **`None` fields are skipped**:
   ```python
   locked: Optional[TokenFlag] = None
   # to_sexpr() → locked is NOT serialized
   ```

2. **Instances are always serialized** (even if "empty"):
   ```python
   locked: TokenFlag = TokenFlag("locked", None)
   # to_sexpr() → ["locked"] is serialized
   ```

3. **Empty lists are serialized**:
   ```python
   points: List[Point] = []
   # to_sexpr() → No point entries, but list exists
   ```

4. **Delegation to subclasses**:
   ```python
   # NamedObject delegates to to_sexpr() of all fields
   for field in fields:
       if isinstance(value, SExpressionBase):
           result.append(value.to_sexpr())
   ```

---

## Error Handling

### Validation

`TokenFlag.from_sexpr()` validates structure:

```python
# STRICT mode: Throw error
try:
    flag = TokenFlag.from_sexpr(['at', '10', '20', '90'],
                                   ParseStrictness.STRICT, cursor)
except ValueError as e:
    print(e)  # TokenFlag 'at' has 4 elements, max 2 allowed

# FAILSAFE mode: Log warning
flag = TokenFlag.from_sexpr(['at', '10', '20', '90'],
                               ParseStrictness.FAILSAFE, cursor)
# WARNING: TokenFlag 'at' has 4 elements, max 2 allowed
```

### Unused Tokens

After parsing, unused tokens are checked:

```python
unused = cursor.parser.get_unused_tokens()
if unused:
    cursor.log_issue(f"Unused tokens: {unused}")
```

---

## Migration & Compatibility

### Current Implementation

The current implementation maintains **backward compatibility**:

```python
# ✅ Works: token as instance variable
layer = NamedString(token='layer', value='F.Cu')

# ✅ Works: __token_name__ as ClassVar
class MyStr(NamedString):
    __token_name__: ClassVar[str] = "my_token"
```

### Future Changes

Possible future refactorings (see `docs/refactoring/`):

1. ~~Remove `__found__` attribute~~ (already removed)
2. Consistent naming (TokenFlag → KiCadFlag?)
3. Further parser optimizations
4. Performance improvements

---

## Examples

### Complete Example: Custom KiCad Object

```python
from dataclasses import dataclass, field
from typing import ClassVar, List, Optional
from kicadfiles.base_element import (
    NamedObject, NamedString, NamedInt, NamedFloat,
    TokenFlag, ParseStrictness
)

@dataclass
class CustomPad(NamedObject):
    """Custom pad definition."""

    __token_name__: ClassVar[str] = "custom_pad"

    # Required fields
    number: NamedString = field(
        default_factory=lambda: NamedString("number", "1")
    )

    # Optional primitives
    layer: Optional[NamedString] = None

    # Optional flags
    locked: Optional[TokenFlag] = None

    # Numeric values
    width: NamedFloat = field(
        default_factory=lambda: NamedFloat("width", 1.0)
    )

    # Lists
    drill_holes: List[DrillHole] = field(default_factory=list)

# Usage
pad = CustomPad.from_sexpr(sexpr, ParseStrictness.STRICT)
print(f"Pad #{pad.number.value} on layer {pad.layer.value if pad.layer else 'any'}")

# Modify
pad.locked = TokenFlag("locked", None)
pad.width.value = 2.0

# Serialize
sexpr = pad.to_sexpr()
```

### Roundtrip Test

```python
# Parse original
original = KicadSch.from_file('input.kicad_sch', ParseStrictness.STRICT)

# Convert to S-expression
sexpr = original.to_sexpr()

# Parse back
regenerated = KicadSch.from_sexpr(sexpr, ParseStrictness.STRICT)

# Compare
assert original == regenerated  # Should be identical
```

---

## Debugging

### Show Parse Path

```python
cursor.get_path_str()  # → "kicad_sch > lib_symbols > symbol > pin"
```

### Find Unused Tokens

```python
unused = cursor.parser.get_unused_tokens()
print(f"Unused tokens: {unused}")
```

### Strictness for Debugging

```python
# FAILSAFE: Shows problems but continues parsing
obj = KicadSch.from_file('problematic.kicad_sch', ParseStrictness.FAILSAFE)
# → See warnings in log for all problems
```

---

## Summary

`base_element.py` provides:

✅ **Unified interface** for all KiCad types
✅ **Flexible parsing** with strictness control
✅ **Type-safe** wrappers for primitive values
✅ **Validation** of S-expression structures
✅ **Delegation** to subclasses for parsing/serialization
✅ **Backward compatibility** with existing code

The architecture enables reliable parsing, modification, and re-serialization of complex KiCad files.
