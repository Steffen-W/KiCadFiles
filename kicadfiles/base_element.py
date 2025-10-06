"""S-expression parser for KiCad objects.

Architecture:
- Unified token handling via __token_name__ in SExpressionBase
- Central parsing utilities in ParseCursor
- Type-based field classification (PRIMITIVE vs SEXPR_BASE)
- Clean separation between instance fields and list containers
- Field metadata as single source of truth for required/optional behavior
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from enum import Enum
from typing import (
    Any,
    ClassVar,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from .sexpdata import Symbol
from .sexpr_parser import SExpr, SExprParser, str_to_sexpr

T = TypeVar("T", bound="NamedObject")


# =============================================================================
# Utility Functions
# =============================================================================


def _convert_to_type(value: Any, target_type: Type) -> Any:
    """Convert value to target type with Enum support."""
    try:
        if isinstance(target_type, type) and issubclass(target_type, Enum):
            if isinstance(value, int):
                return target_type(value)
            try:
                return target_type(str(value))
            except ValueError:
                return target_type[str(value).upper()]
    except (TypeError, KeyError):
        pass

    if target_type == int:
        return int(value)
    elif target_type == float:
        return float(value)
    elif target_type == bool:
        return str(value).lower() in ("yes", "true", "1")
    elif target_type == str:
        return str(value)
    return value


# =============================================================================
# Parsing Infrastructure
# =============================================================================


class ParseStrictness(Enum):
    """Parser strictness levels for error handling."""

    STRICT = "strict"  # Raise exceptions for all parsing errors
    SILENT = "silent"  # Silently use defaults for missing fields
    FAILSAFE = "failsafe"  # Log warnings and use defaults for missing fields


@dataclass
class ParseCursor:
    """Cursor for tracking position in S-expression during parsing.

    Provides centralized parsing utilities for all primitive types.
    """

    sexpr: SExpr  # Current S-expression
    parser: SExprParser  # Parser for tracking used indices
    path: List[str]  # Path for debugging
    strictness: ParseStrictness  # Parse strictness level

    def enter(self, sexpr: SExpr, name: str) -> "ParseCursor":
        """Create new cursor for nested object."""
        nested_parser = SExprParser(sexpr)
        return ParseCursor(
            sexpr=sexpr,
            parser=nested_parser,
            path=self.path + [name],
            strictness=self.strictness,
        )

    def get_path_str(self) -> str:
        """Get current path as string for debugging."""
        return " > ".join(self.path)

    def log_issue(self, message: str) -> None:
        """Log parsing issue based on strictness."""
        if self.strictness == ParseStrictness.STRICT:
            raise ValueError(message)
        elif self.strictness == ParseStrictness.FAILSAFE:
            logging.warning(message)
        # SILENT: do nothing

    def _get_value_at_index(
        self, index: int, field_name: str, type_name: str, required: bool
    ) -> Optional[Any]:
        """Get value at index with validation and error handling.

        Returns:
            The raw value at index, or None if not available or invalid
        """
        if index >= len(self.sexpr):
            if required:
                self.log_issue(
                    f"{self.get_path_str()}: Missing required {type_name} '{field_name}' at index {index}"
                )
            return None

        value = self.sexpr[index]
        if isinstance(value, list):
            if required:
                self.log_issue(
                    f"{self.get_path_str()}: Expected {type_name} for '{field_name}', got list"
                )
            return None

        self.parser.mark_used(index)
        return value

    def _parse_typed(
        self, index: int, field_name: str, target_type: Type, required: bool = True
    ) -> Optional[Any]:
        """Generic parser for typed values at given index."""
        type_name = getattr(target_type, "__name__", str(target_type))
        value = self._get_value_at_index(index, field_name, type_name, required)
        if value is None:
            return None
        try:
            return _convert_to_type(value, target_type)
        except (ValueError, TypeError, KeyError) as e:
            self.log_issue(
                f"{self.get_path_str()}: Cannot convert '{value}' to {type_name} for '{field_name}': {e}"
            )
            return None

    def parse_int(
        self, index: int, field_name: str, required: bool = True
    ) -> Optional[int]:
        """Parse integer at given index."""
        return self._parse_typed(index, field_name, int, required)

    def parse_float(
        self, index: int, field_name: str, required: bool = True
    ) -> Optional[float]:
        """Parse float at given index."""
        return self._parse_typed(index, field_name, float, required)

    def parse_str(
        self, index: int, field_name: str, required: bool = True
    ) -> Optional[str]:
        """Parse string at given index."""
        return self._parse_typed(index, field_name, str, required)

    def parse_bool(
        self, index: int, field_name: str, required: bool = True
    ) -> Optional[bool]:
        """Parse boolean at given index (yes/no, true/false, 1/0)."""
        return self._parse_typed(index, field_name, bool, required)

    def parse_enum(
        self, index: int, field_name: str, enum_class: Type[Enum], required: bool = True
    ) -> Optional[Enum]:
        """Parse enum at given index."""
        return self._parse_typed(index, field_name, enum_class, required)

    def find_token(self, token_name: str, mark_used: bool = True) -> SExpr:
        """Find and return S-expression with given token name.

        Returns:
            The S-expression as list if found, empty list otherwise.
            Always returns a list for consistent handling.
        """
        for idx, item in enumerate(self.sexpr[1:], start=1):
            if isinstance(item, list) and item and str(item[0]) == token_name:
                if mark_used:
                    self.parser.mark_used(idx)
                return item
            elif isinstance(item, (str, Symbol)) and str(item) == token_name:
                if mark_used:
                    self.parser.mark_used(idx)
                return [item]
        return []


# =============================================================================
# Base Classes
# =============================================================================


@dataclass
class SExpressionBase(ABC):
    """Abstract base class for all S-expression objects.

    Attributes:
        __token_name__: Token identifier for this object (ClassVar)
    """

    __token_name__: ClassVar[str] = ""

    @classmethod
    @abstractmethod
    def from_sexpr(
        cls: Type,
        sexpr: Union[str, SExpr],
        strictness: ParseStrictness = ParseStrictness.STRICT,
        cursor: Optional[ParseCursor] = None,
    ) -> Optional[Any]:
        """Parse from S-expression."""
        pass

    @abstractmethod
    def to_sexpr(self) -> Union[SExpr, str, int, float]:
        """Serialize to S-expression."""
        pass


# =============================================================================
# KiCad Primitives
# =============================================================================


@dataclass(eq=False)
class NamedValue(SExpressionBase):
    """Base class for named primitive wrapper types (str, int, float)."""

    base_type: ClassVar[type] = object

    def __post_init__(self) -> None:
        """Post-initialization hook for primitives.

        Note: Primitives have instance-specific tokens, not class-level tokens.
        """
        pass

    @property
    def required(self) -> bool:
        """Whether this field is required."""
        return getattr(self, "_required", True)

    def __str__(self) -> str:
        return str(getattr(self, "value", None))

    def __repr__(self) -> str:
        value = getattr(self, "value", None)
        parts = [repr(value)]
        if self.__token_name__:
            parts.append(f"token={repr(self.__token_name__)}")
        if not self.required:
            parts.append("optional")
        return f"{self.__class__.__name__}({', '.join(parts)})"

    def __bool__(self) -> bool:
        """Boolean conversion based on value."""
        return bool(getattr(self, "value", None))

    def __call__(self, new_value: Any) -> "NamedValue":
        """Allow calling the primitive to update its value.

        This enables convenient syntax like: pcb.version(20240101)
        instead of: pcb.version = NamedInt("version", 20240101)

        Args:
            new_value: New value to set

        Returns:
            Self for method chaining
        """
        self.value = self._convert_value(new_value)
        return self

    @classmethod
    def from_sexpr(
        cls: Type,
        sexpr: Union[str, SExpr],
        strictness: ParseStrictness = ParseStrictness.STRICT,
        cursor: Optional[ParseCursor] = None,
    ) -> Optional["NamedValue"]:
        """Parse primitive from S-expression (named or positional)."""
        if cursor is None:
            raise ValueError("NamedValue requires cursor for parsing")

        value = None
        token = ""

        if isinstance(sexpr, list):
            if len(sexpr) >= 2:
                token = str(sexpr[0])
                value = sexpr[1]
        else:
            value = sexpr

        if value is None:
            return None

        try:
            converted = cls._convert_value(value)
            instance: "NamedValue" = cls(token=token, value=converted)
            return instance
        except (ValueError, TypeError):
            return None

    @classmethod
    def _convert_value(cls, value: Any) -> Any:
        return _convert_to_type(value, cls.base_type)

    def to_sexpr(self) -> Union[List[Any], Any]:
        """Serialize to S-expression."""
        value = getattr(self, "value", None)
        token = getattr(self, "token", "")
        if token:
            return [token, value]
        else:
            return value

    def __eq__(self, other: object) -> bool:
        """Equality comparison based on token and value only."""
        if not isinstance(other, NamedValue):
            return False
        return (
            self.__class__ == other.__class__
            and getattr(self, "token", "") == getattr(other, "token", "")
            and getattr(self, "value", None) == getattr(other, "value", None)
        )


@dataclass(eq=False)
class NamedString(NamedValue):
    """String wrapper for named values."""

    token: str = ""
    value: str = ""
    base_type: ClassVar[type] = str


@dataclass(eq=False)
class NamedInt(NamedValue):
    """Integer wrapper for named values."""

    token: str = ""
    value: int = 0
    base_type: ClassVar[type] = int


@dataclass(eq=False)
class NamedFloat(NamedValue):
    """Float wrapper for named values."""

    token: str = ""
    value: float = 0.0
    base_type: ClassVar[type] = float


# =============================================================================
# Optional Flags
# =============================================================================


class UnquotedToken(str):
    """Marker class for tokens that should not be quoted in serialization."""

    pass


@dataclass(eq=False)
class TokenBase(SExpressionBase):
    """Base class for optional flags with instance-level tokens."""

    token: str = ""

    def __post_init__(self) -> None:
        """Copy token to __token_name__ for consistency."""
        if self.token and not self.__class__.__token_name__:
            type.__setattr__(self.__class__, "__token_name__", self.token)


@dataclass(eq=False)
class TokenFlag(TokenBase):
    """Optional flag with optional value.

    Formats:
        (token) -> token="token", token_value=None
        (token value) -> token="token", token_value="value"
    """

    token_value: Optional[str] = None

    def __str__(self) -> str:
        if self.token_value:
            return f"({self.token} {self.token_value})"
        return f"({self.token})"

    def __bool__(self) -> bool:
        """Boolean conversion based on token_value."""
        if self.token_value:
            return self.token_value.lower() in ("yes", "true", "1")
        return True  # Presence = True

    def __call__(self, new_value: Optional[str] = None) -> "TokenFlag":
        """Allow calling the flag to update its value.

        This enables convenient syntax like: pcb.legacy_teardrops("no")
        instead of: pcb.legacy_teardrops = TokenFlag("legacy_teardrops", "no")

        Args:
            new_value: New token value to set

        Returns:
            Self for method chaining
        """
        self.token_value = new_value
        return self

    @classmethod
    def from_sexpr(
        cls: Type["TokenFlag"],
        sexpr: Union[str, SExpr],
        strictness: ParseStrictness = ParseStrictness.STRICT,
        cursor: Optional[ParseCursor] = None,
    ) -> Optional["TokenFlag"]:
        """Parse from S-expression.

        TokenFlag supports only simple flags:
        - (token) or (token value) where value is NOT a nested list

        Invalid: (fill (type none)) -> Use proper Fill class instead
        """
        if cursor is None:
            raise ValueError("TokenFlag requires cursor for parsing")

        # Standalone symbol: (token)
        if isinstance(sexpr, (str, Symbol)):
            instance: TokenFlag = cls(token=str(sexpr), token_value=None)
            return instance

        # List format: (token) or (token value)
        if isinstance(sexpr, list) and len(sexpr) >= 1:
            token_name = str(sexpr[0])

            if len(sexpr) > 2:
                cursor.log_issue(
                    f"TokenFlag '{token_name}' has {len(sexpr)} elements, max 2 allowed"
                )

            if len(sexpr) == 2 and isinstance(sexpr[1], list):
                cursor.log_issue(
                    f"TokenFlag '{token_name}' has nested list - use proper class instead"
                )

            # Extract value
            token_value = str(sexpr[1]) if len(sexpr) == 2 else None
            instance2: TokenFlag = cls(token=token_name, token_value=token_value)
            return instance2

        return None

    def to_sexpr(self) -> Union[List, str]:
        """Serialize to S-expression."""
        if self.token_value:
            return [self.token, UnquotedToken(self.token_value)]
        return [self.token]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TokenFlag):
            return False
        return self.token == other.token and self.token_value == other.token_value


@dataclass(eq=False)
class SymbolValue(TokenBase):
    """Simple flag for optional symbols.

    Represents standalone tokens like 'oval', 'locked' without values.
    Does not consume positional slots during parsing.
    """

    def __str__(self) -> str:
        return self.token

    def __bool__(self) -> bool:
        """Always True if instance exists."""
        return True

    @classmethod
    def from_sexpr(
        cls: Type,
        sexpr: Union[str, SExpr],
        strictness: ParseStrictness = ParseStrictness.STRICT,
        cursor: Optional[ParseCursor] = None,
    ) -> Optional["SymbolValue"]:
        """Parse from S-expression."""
        if cursor is None:
            raise ValueError("SymbolValue requires cursor for parsing")

        # Handle both direct symbols and lists with single symbol (from find_token)
        if isinstance(sexpr, (str, Symbol)) and not isinstance(sexpr, list):
            instance: "SymbolValue" = cls(token=str(sexpr))
            return instance
        elif (
            isinstance(sexpr, list)
            and len(sexpr) == 1
            and isinstance(sexpr[0], (str, Symbol))
        ):
            instance2: "SymbolValue" = cls(token=str(sexpr[0]))
            return instance2

        return None

    def to_sexpr(self) -> UnquotedToken:
        """Serialize to S-expression."""
        return UnquotedToken(self.token)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SymbolValue):
            return False
        return self.token == other.token


# =============================================================================
# NamedObject - Main Parser
# =============================================================================


class FieldType(Enum):
    """Field type classification."""

    PRIMITIVE = "primitive"
    SEXPR_BASE = "sexpr_base"


@dataclass
class FieldInfo:
    """Field metadata for parsing.

    Attributes:
        name: Field name in dataclass
        field_type: Type classification of elements (PRIMITIVE, SEXPR_BASE)
        inner_type: Actual element type (for List[T], this is T)
        is_optional: Whether field is Optional[T]
        is_list: Whether field is List[T]
        token_name: Token name for parsing (from __token_name__ or None)
        position_index: Positional index in S-expression (for non-named fields)
    """

    name: str
    field_type: FieldType
    inner_type: Type[Any]
    is_optional: bool
    is_list: bool
    token_name: Optional[str] = None
    position_index: int = 0

    @property
    def can_self_parse(self) -> bool:
        """Whether type is SExpressionBase (has from_sexpr)."""
        return self.field_type == FieldType.SEXPR_BASE


@dataclass
class NamedObject(SExpressionBase):
    """Base class for named S-expression objects.

    Subclasses should define __token_name__ as ClassVar[str].
    """

    __legacy_token_names__: ClassVar[List[str]] = []
    _field_info_cache: ClassVar[List[FieldInfo]]

    def __post_init__(self) -> None:
        """Validate token name is defined."""
        if not self.__token_name__:
            raise ValueError(
                f"Class {self.__class__.__name__} must define __token_name__"
            )

    @classmethod
    def from_sexpr(
        cls: Type[T],
        sexpr: Union[str, SExpr],
        strictness: ParseStrictness = ParseStrictness.STRICT,
        cursor: Optional[ParseCursor] = None,
    ) -> T:
        """Parse from S-expression."""
        # Create root cursor if needed
        if cursor is None:
            if isinstance(sexpr, str):
                sexpr = str_to_sexpr(sexpr)
            parser = SExprParser(sexpr)
            cursor = ParseCursor(
                sexpr=sexpr,
                parser=parser,
                path=[cls.__name__],
                strictness=strictness,
            )

        # Validate token
        token = str(cursor.sexpr[0]) if cursor.sexpr else "empty"
        valid_tokens = [cls.__token_name__] + (cls.__legacy_token_names__ or [])

        if token not in valid_tokens:
            raise ValueError(
                f"Token mismatch at {cursor.get_path_str()}: "
                f"expected '{cls.__token_name__}', got '{token}'"
            )

        # Parse fields using delegation
        field_infos = cls._classify_fields()
        parsed_values = {}

        for field_info in field_infos:
            value = cls._parse_field(field_info, cursor)
            # For SymbolValue, always set the value (even if None) to prevent
            # default_factory from being called when the token is not present
            if value is not None:
                parsed_values[field_info.name] = value
            elif field_info.inner_type.__name__ == "SymbolValue":
                parsed_values[field_info.name] = None

        return cls(**parsed_values)

    @classmethod
    def from_str(
        cls: Type[T],
        sexpr_string: str,
        strictness: ParseStrictness = ParseStrictness.STRICT,
    ) -> T:
        """Parse from S-expression string - convenience method for better clarity."""
        sexpr = str_to_sexpr(sexpr_string)
        return cls.from_sexpr(sexpr, strictness=strictness)

    @classmethod
    def _parse_field(
        cls,
        field_info: FieldInfo,
        cursor: ParseCursor,
    ) -> Any:
        """Parse single field based on field metadata."""
        if field_info.is_list:
            return cls._parse_list_field(field_info, cursor)

        elif field_info.field_type == FieldType.PRIMITIVE:
            return cls._parse_primitive_field(field_info, cursor)

        elif field_info.field_type == FieldType.SEXPR_BASE:
            return cls._parse_sexpr_base_field(field_info, cursor)

        else:
            raise ValueError(f"Unknown field type: {field_info.field_type}")

    @classmethod
    def _parse_primitive_field(cls, field_info: FieldInfo, cursor: ParseCursor) -> Any:
        """Parse primitive field (named token or positional)."""
        if field_info.token_name:
            named_sexpr = cursor.find_token(field_info.token_name)
            if len(named_sexpr) >= 2:
                return _convert_to_type(named_sexpr[1], field_info.inner_type)
            if not field_info.is_optional and not named_sexpr:
                cursor.log_issue(
                    f"{cursor.get_path_str()}: Required token '{field_info.token_name}' not found"
                )
            # If token not found and field is optional, return None early
            if not named_sexpr:
                return None

        # Find next unused positional index
        # Start from position_index + 1 and skip already used indices
        index = field_info.position_index + 1
        while index < len(cursor.sexpr) and index in cursor.parser.used_indices:
            index += 1

        inner_type = field_info.inner_type
        required = not field_info.is_optional

        try:
            if isinstance(inner_type, type) and issubclass(inner_type, Enum):
                return cursor.parse_enum(index, field_info.name, inner_type, required)
        except TypeError:
            pass

        parser_map = {
            int: cursor.parse_int,
            float: cursor.parse_float,
            bool: cursor.parse_bool,
            str: cursor.parse_str,
        }

        parser = parser_map.get(inner_type, cursor.parse_str)
        return parser(index, field_info.name, required)

    @classmethod
    def _parse_list_field(cls, field_info: FieldInfo, cursor: ParseCursor) -> List[Any]:
        """Parse list field by collecting all matching elements."""
        if not field_info.can_self_parse:
            return []

        result: List[Any] = []
        has_token = field_info.token_name is not None

        for idx, item in enumerate(cursor.sexpr[1:], start=1):
            if not isinstance(item, list):
                continue

            # Skip already used indices for unnamed tokens
            if not has_token and idx in cursor.parser.used_indices:
                continue

            # Check token match for named tokens
            if has_token and (not item or str(item[0]) != field_info.token_name):
                continue

            # Try to parse element
            try:
                if has_token:
                    cursor.parser.mark_used(idx)

                nested_cursor = cursor.enter(item, f"{field_info.name}[{len(result)}]")
                element = field_info.inner_type.from_sexpr(
                    item, cursor.strictness, nested_cursor
                )

                if element is not None:
                    if not has_token:
                        cursor.parser.mark_used(idx)
                    result.append(element)
            except (ValueError, TypeError):
                # In STRICT mode, propagate exceptions instead of silently skipping
                if cursor.strictness == ParseStrictness.STRICT:
                    raise
                continue

        return result

    @classmethod
    def _parse_sexpr_base_field(
        cls, field_info: FieldInfo, cursor: ParseCursor
    ) -> Optional[Any]:
        """Parse SExpressionBase field via from_sexpr delegation."""
        result = None

        if field_info.token_name:
            named_sexpr = cursor.find_token(field_info.token_name)
            if named_sexpr:
                nested_cursor = cursor.enter(named_sexpr, field_info.name)
                result = field_info.inner_type.from_sexpr(
                    named_sexpr, cursor.strictness, nested_cursor
                )

            if not field_info.is_optional and not named_sexpr:
                cursor.log_issue(
                    f"{cursor.get_path_str()}: Required token '{field_info.token_name}' not found"
                )
            if not named_sexpr:
                return None
        else:
            index = field_info.position_index + 1
            if index >= len(cursor.sexpr):
                if not field_info.is_optional:
                    cursor.log_issue(
                        f"{cursor.get_path_str()}: Required field '{field_info.name}' "
                        f"not found at index {index}"
                    )
                return None

            try:
                cursor.parser.mark_used(index)
                nested_cursor = cursor.enter(cursor.sexpr[index], field_info.name)
                result = field_info.inner_type.from_sexpr(
                    cursor.sexpr[index], cursor.strictness, nested_cursor
                )
            except (ValueError, TypeError) as e:
                if not field_info.is_optional:
                    cursor.log_issue(
                        f"{cursor.get_path_str()}: Failed to parse '{field_info.name}': {e}"
                    )
                return None

        # Set _required attribute from field metadata for primitives
        if result is not None and isinstance(result, NamedValue):
            object.__setattr__(result, "_required", not field_info.is_optional)

        return result

    @classmethod
    def _classify_fields(cls) -> List[FieldInfo]:
        """Classify all fields for parsing with caching."""
        if hasattr(cls, "_field_info_cache"):
            return cls._field_info_cache

        field_types = get_type_hints(cls)
        field_infos: List[FieldInfo] = []
        position_index = 0

        for dataclass_field in fields(cls):
            if dataclass_field.name.startswith("_"):
                continue

            field_type = field_types[dataclass_field.name]
            field_info = cls._classify_field(
                dataclass_field.name, field_type, position_index, dataclass_field
            )
            field_infos.append(field_info)

            if not (
                field_info.field_type == FieldType.SEXPR_BASE
                and field_info.inner_type.__name__ == "SymbolValue"
            ):
                position_index += 1

        cls._field_info_cache = field_infos
        return field_infos

    @classmethod
    def _classify_field(
        cls,
        name: str,
        field_type: Type[Any],
        position: int,
        dataclass_field: Any = None,
    ) -> FieldInfo:
        """Classify a single field."""
        is_union_with_none = get_origin(field_type) is Union and type(None) in get_args(
            field_type
        )

        inner_type = field_type
        if is_union_with_none:
            inner_type = next(
                arg for arg in get_args(field_type) if arg is not type(None)
            )

        is_optional = is_union_with_none
        if dataclass_field and dataclass_field.metadata.get("required") is False:
            is_optional = True

        is_list = get_origin(inner_type) in (list, List)

        if is_list:
            element_type = get_args(inner_type)[0] if get_args(inner_type) else Any
            token_name = None
            element_field_type = FieldType.PRIMITIVE

            try:
                # Type guard to ensure element_type is a proper type before issubclass check
                if (
                    isinstance(element_type, type)
                    and not isinstance(element_type, TypeVar)  # type: ignore[arg-type]
                    and issubclass(element_type, SExpressionBase)  # type: ignore[arg-type]
                ):
                    token_name = getattr(element_type, "__token_name__", None)
                    element_field_type = FieldType.SEXPR_BASE
            except TypeError:
                pass

            return FieldInfo(
                name=name,
                field_type=element_field_type,
                inner_type=element_type,  # type: ignore[arg-type]
                is_optional=False,
                is_list=True,
                token_name=token_name,
                position_index=position,
            )

        try:
            if isinstance(inner_type, type) and issubclass(inner_type, SExpressionBase):
                # For NamedValue, TokenFlag, and SymbolValue subclasses,
                # each instance has its own token, so we need to extract it from the default_factory
                token_name = None
                if issubclass(inner_type, (NamedValue, TokenFlag, SymbolValue)):
                    if dataclass_field and dataclass_field.default_factory:
                        try:
                            default_instance = dataclass_field.default_factory()
                            token_name = getattr(default_instance, "token", None)
                        except (TypeError, AttributeError):
                            pass
                else:
                    token_name = getattr(inner_type, "__token_name__", None)

                return FieldInfo(
                    name=name,
                    field_type=FieldType.SEXPR_BASE,
                    inner_type=inner_type,
                    is_optional=is_optional,
                    is_list=False,
                    token_name=token_name,
                    position_index=position,
                )
        except TypeError:
            pass

        return FieldInfo(
            name=name,
            field_type=FieldType.PRIMITIVE,
            inner_type=inner_type,
            is_optional=is_optional,
            is_list=False,
            token_name=None,
            position_index=position,
        )

    def to_sexpr(self) -> SExpr:
        """Serialize to S-expression."""
        result: SExpr = [self.__token_name__]
        for field_info in self._classify_fields():
            value = getattr(self, field_info.name)

            if value is None:
                continue
            if isinstance(value, SExpressionBase):
                result.append(value.to_sexpr())
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, SExpressionBase):
                        result.append(item.to_sexpr())
                    else:
                        result.append(item)
            elif isinstance(value, Enum):
                result.append(value.value)
            else:
                result.append(value)

        return result

    def to_sexpr_str(self, _indent_level: int = 0) -> str:
        """Convert to KiCad-formatted S-expression string.

        Args:
            _indent_level: Internal parameter for recursion depth

        Returns:
            Formatted S-expression string
        """
        sexpr = self.to_sexpr()
        return self._format_sexpr_kicad_style(sexpr, _indent_level)

    def _format_sexpr_kicad_style(self, sexpr: Any, indent_level: int = 0) -> str:
        """Format S-expression in KiCad style with tabs and unquoted tokens."""
        if not isinstance(sexpr, list):
            return self._format_primitive_value(sexpr)

        if not sexpr:
            return "()"

        current_indent = "\t" * indent_level
        token_name = str(sexpr[0])

        if len(sexpr) == 1:
            return f"{current_indent}({token_name})"

        # Separate primitives and nested lists
        primitive_values = []
        nested_lists = []

        for item in sexpr[1:]:
            if isinstance(item, list):
                nested_lists.append(item)
            else:
                primitive_values.append(self._format_primitive_value(item))

        # Check for single line format: only primitives and short enough
        if not nested_lists and len(sexpr) <= 4:
            all_items = [token_name] + primitive_values
            return f"{current_indent}({' '.join(all_items)})"

        # Multi-line format: primitives on first line, nested lists indented
        primitive_part = f" {' '.join(primitive_values)}" if primitive_values else ""
        lines = [f"{current_indent}({token_name}{primitive_part}"]

        for nested_item in nested_lists:
            nested_formatted = self._format_sexpr_kicad_style(
                nested_item, indent_level + 1
            )
            lines.append(nested_formatted)

        lines.append(f"{current_indent})")
        return "\n".join(lines)

    def _format_primitive_value(self, value: Any) -> str:
        """Format primitive values for S-expression serialization."""
        if isinstance(value, bool):
            return "yes" if value else "no"
        elif isinstance(value, UnquotedToken):
            return str(value)
        elif isinstance(value, Enum):
            return str(value.value)
        elif isinstance(value, str):
            escaped_value = value.replace("\\", "\\\\").replace('"', '\\"')
            return f'"{escaped_value}"'
        else:
            return str(value)


__all__ = [
    "NamedString",
    "NamedInt",
    "NamedFloat",
    "NamedObject",
    "TokenFlag",
    "SymbolValue",
    "ParseStrictness",
]
