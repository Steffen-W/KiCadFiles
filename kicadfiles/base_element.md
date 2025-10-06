# base_element.py - Documentation

## Overview

`base_element.py` is the foundation of the KiCadFiles library. It defines the base classes and parser infrastructure for all KiCad S-Expression objects.

## Architecture

### Class Hierarchy

```
SExpressionBase (ABC)
├── KiCadPrimitive (ABC)
│   ├── KiCadStr
│   ├── KiCadInt
│   └── KiCadFloat
├── OptionalFlagBase
│   ├── OptionalFlag
│   └── OptionalSimpleFlag
└── KiCadObject (ABC)
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

### 2. KiCadPrimitive

**Purpose**: Wrapper for primitive KiCad values (strings, integers, floats) with optional token names.

#### Properties

```python
@dataclass(eq=False)
class KiCadPrimitive(SExpressionBase):
    token: str = ""           # Token name (can be set per instance)
    value: Any = None         # The actual value
    base_type: ClassVar[type] # Type of value (str/int/float)
```

#### Formats

**Named Format**: `(token_name value)`
```python
# S-expression: (layer "F.Cu")
layer = KiCadStr.from_sexpr(['layer', 'F.Cu'])
# → KiCadStr(token='layer', value='F.Cu')
```

**Positional Format**: `value`
```python
# S-expression: 1.27
size = KiCadFloat.from_sexpr(1.27)
# → KiCadFloat(token='', value=1.27)
```

#### Subclasses

```python
# String values
KiCadStr(token: str, value: str)
# Example: KiCadStr('layer', 'F.Cu')

# Integer values
KiCadInt(token: str, value: int)
# Example: KiCadInt('width', 2)

# Float values
KiCadFloat(token: str, value: float)
# Example: KiCadFloat('size', 1.27)
```

#### Usage

```python
# Create manually
layer = KiCadStr(token='layer', value='F.Cu')

# Parse from S-expression
layer = KiCadStr.from_sexpr(['layer', 'F.Cu'])

# Serialize to S-expression
sexpr = layer.to_sexpr()  # → ['layer', 'F.Cu']

# Boolean conversion
if layer:  # True if value is not empty
    print(layer.value)
```

---

### 3. OptionalFlag

**Purpose**: Represents optional flags with optional values.

#### Properties

```python
@dataclass(eq=False)
class OptionalFlag(OptionalFlagBase):
    token: str                    # Flag name
    token_value: Optional[str]    # Optional value
```

#### Formats

**Flag only**: `(flag)`
```python
# S-expression: (locked)
flag = OptionalFlag.from_sexpr(['locked'])
# → OptionalFlag(token='locked', token_value=None)
```

**Flag with value**: `(flag value)`
```python
# S-expression: (hide yes)
flag = OptionalFlag.from_sexpr(['hide', 'yes'])
# → OptionalFlag(token='hide', token_value='yes')
```

#### Important Constraints

`OptionalFlag` supports **only simple flags** with at most 2 elements:
- ✅ `(token)` - 1 element
- ✅ `(token value)` - 2 elements with simple value
- ❌ `(token value1 value2)` - More than 2 elements → ERROR
- ❌ `(token (nested list))` - Nested list → ERROR

Nested S-expressions like `(fill (type none))` are **NOT** OptionalFlags and must use their own classes (e.g., `Fill`).

#### Validation

In **STRICT mode**, invalid structures are rejected:

```python
# ERROR: Too many elements
OptionalFlag.from_sexpr(['at', '10', '20', '90'])
# → ValueError: OptionalFlag 'at' has 4 elements, max 2 allowed

# ERROR: Nested list
OptionalFlag.from_sexpr(['fill', ['type', 'none']])
# → ValueError: OptionalFlag 'fill' has nested list - use proper class instead
```

In **FAILSAFE mode**, warnings are logged and parsing continues.

#### Usage

```python
# Create manually
locked = OptionalFlag(token='locked', token_value=None)
hide = OptionalFlag(token='hide', token_value='yes')

# Parse from S-expression
locked = OptionalFlag.from_sexpr(['locked'])
hide = OptionalFlag.from_sexpr(['hide', 'yes'])

# Serialize to S-expression
locked.to_sexpr()  # → ['locked']
hide.to_sexpr()    # → ['hide', 'yes']

# Boolean conversion
if hide:  # True if token_value in ('yes', 'true', '1') OR presence
    print("Hidden!")
```

---

### 4. OptionalSimpleFlag

**Purpose**: Simple symbol flags without values (e.g., `oval`, `locked`).

#### Properties

```python
@dataclass(eq=False)
class OptionalSimpleFlag(OptionalFlagBase):
    token: str  # Symbol name
```

#### Format

**Symbol only**: `symbol`
```python
# S-expression: oval
flag = OptionalSimpleFlag.from_sexpr('oval')
# → OptionalSimpleFlag(token='oval')
```

#### Difference from OptionalFlag

| Property | OptionalFlag | OptionalSimpleFlag |
|----------|--------------|-------------------|
| Format | `(token)` or `(token value)` | `symbol` (no parentheses!) |
| Value | Optional | Never |
| Usage | Named tokens with optional value | Standalone symbols |

#### Usage

```python
# Create manually
oval = OptionalSimpleFlag(token='oval')

# Parse from S-expression
oval = OptionalSimpleFlag.from_sexpr('oval')

# Serialize to S-expression
oval.to_sexpr()  # → 'oval'

# Boolean conversion
if oval:  # Always True if instance exists
    print("Oval shape")
```

---

### 5. KiCadObject

**Purpose**: Base class for all complex KiCad objects (PCBs, schematics, symbols, etc.).

#### Properties

```python
@dataclass
class KiCadObject(SExpressionBase):
    __token_name__: ClassVar[str] = ""  # Class-level token name

    # All fields are defined via dataclass fields
```

#### Parsing Mechanism

KiCadObject implements a generic parser that:

1. **Classifies fields** (KiCadPrimitive, KiCadObject, List, OptionalFlag, etc.)
2. **Delegates** to subclasses via `from_sexpr()`
3. **Handles errors** based on strictness level
4. **Detects unused tokens** for validation

#### Field Types

```python
class FieldType(Enum):
    PRIMITIVE = "primitive"                    # int, str, float, bool, Enum
    KICAD_PRIMITIVE = "kicad_primitive"        # KiCadStr, KiCadInt, KiCadFloat
    OPTIONAL_KICAD_PRIMITIVE = "optional_kicad_primitive"
    KICAD_OBJECT = "kicad_object"              # Nested KiCadObject
    OPTIONAL_KICAD_OBJECT = "optional_kicad_object"
    OPTIONAL_FLAG = "optional_flag"             # OptionalFlag
    OPTIONAL_SIMPLE_FLAG = "optional_simple_flag"  # OptionalSimpleFlag
    LIST = "list"                              # List[...]
```

#### Usage

```python
@dataclass
class MyKiCadObject(KiCadObject):
    __token_name__: ClassVar[str] = "my_object"

    # Required fields
    name: KiCadStr = field(default_factory=lambda: KiCadStr("name", ""))

    # Optional fields
    locked: Optional[OptionalFlag] = None
    layer: Optional[KiCadStr] = None

    # Lists
    points: List[Point] = field(default_factory=list)

# Parse
obj = MyKiCadObject.from_sexpr(sexpr, ParseStrictness.STRICT)

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
class MyClass(KiCadObject):
    # ✅ CORRECT: Optional with None default
    locked: Optional[OptionalFlag] = None
    layer: Optional[KiCadStr] = None

    # ❌ WRONG: Non-optional but None default
    name: KiCadStr = None  # → Parse error if not found

    # ✅ CORRECT: Required field with default factory
    name: KiCadStr = field(default_factory=lambda: KiCadStr("name", ""))
```

### 2. Initialize Lists

```python
@dataclass
class MyClass(KiCadObject):
    # ✅ CORRECT: default_factory for lists
    points: List[Point] = field(default_factory=list)

    # ❌ WRONG: Mutable default
    points: List[Point] = []  # Shared between instances!
```

### 3. Use Nested Structures

```python
# ❌ WRONG: OptionalFlag for complex structure
fill: OptionalFlag  # (fill (type none)) → Nested!

# ✅ CORRECT: Own class for complex structure
@dataclass
class Fill(KiCadObject):
    __token_name__: ClassVar[str] = "fill"
    type: Type = field(default_factory=lambda: Type("none"))

fill: Optional[Fill] = None
```

### 4. Use Token Names Consistently

```python
@dataclass
class MyClass(KiCadObject):
    __token_name__: ClassVar[str] = "my_class"  # Class level

    # Field-level token names
    name: KiCadStr = field(
        default_factory=lambda: KiCadStr("name", "")
    )
```

---

## Serialization

### Rules

1. **`None` fields are skipped**:
   ```python
   locked: Optional[OptionalFlag] = None
   # to_sexpr() → locked is NOT serialized
   ```

2. **Instances are always serialized** (even if "empty"):
   ```python
   locked: OptionalFlag = OptionalFlag("locked", None)
   # to_sexpr() → ["locked"] is serialized
   ```

3. **Empty lists are serialized**:
   ```python
   points: List[Point] = []
   # to_sexpr() → No point entries, but list exists
   ```

4. **Delegation to subclasses**:
   ```python
   # KiCadObject delegates to to_sexpr() of all fields
   for field in fields:
       if isinstance(value, SExpressionBase):
           result.append(value.to_sexpr())
   ```

---

## Error Handling

### Validation

`OptionalFlag.from_sexpr()` validates structure:

```python
# STRICT mode: Throw error
try:
    flag = OptionalFlag.from_sexpr(['at', '10', '20', '90'],
                                   ParseStrictness.STRICT, cursor)
except ValueError as e:
    print(e)  # OptionalFlag 'at' has 4 elements, max 2 allowed

# FAILSAFE mode: Log warning
flag = OptionalFlag.from_sexpr(['at', '10', '20', '90'],
                               ParseStrictness.FAILSAFE, cursor)
# WARNING: OptionalFlag 'at' has 4 elements, max 2 allowed
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
layer = KiCadStr(token='layer', value='F.Cu')

# ✅ Works: __token_name__ as ClassVar
class MyStr(KiCadStr):
    __token_name__: ClassVar[str] = "my_token"
```

### Future Changes

Possible future refactorings (see `docs/refactoring/`):

1. ~~Remove `__found__` attribute~~ (already removed)
2. Consistent naming (OptionalFlag → KiCadFlag?)
3. Further parser optimizations
4. Performance improvements

---

## Examples

### Complete Example: Custom KiCad Object

```python
from dataclasses import dataclass, field
from typing import ClassVar, List, Optional
from kicadfiles.base_element import (
    KiCadObject, KiCadStr, KiCadInt, KiCadFloat,
    OptionalFlag, ParseStrictness
)

@dataclass
class CustomPad(KiCadObject):
    """Custom pad definition."""

    __token_name__: ClassVar[str] = "custom_pad"

    # Required fields
    number: KiCadStr = field(
        default_factory=lambda: KiCadStr("number", "1")
    )

    # Optional primitives
    layer: Optional[KiCadStr] = None

    # Optional flags
    locked: Optional[OptionalFlag] = None

    # Numeric values
    width: KiCadFloat = field(
        default_factory=lambda: KiCadFloat("width", 1.0)
    )

    # Lists
    drill_holes: List[DrillHole] = field(default_factory=list)

# Usage
pad = CustomPad.from_sexpr(sexpr, ParseStrictness.STRICT)
print(f"Pad #{pad.number.value} on layer {pad.layer.value if pad.layer else 'any'}")

# Modify
pad.locked = OptionalFlag("locked", None)
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
