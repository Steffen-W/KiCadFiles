"""Optimized S-expression parser for KiCad objects with cursor-based approach."""

from __future__ import annotations

import logging
from abc import ABC
from dataclasses import MISSING, dataclass, fields
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
    get_type_hints,
)

from .sexpr_parser import SExpr, SExprParser, sexpr_to_str, str_to_sexpr

T = TypeVar("T", bound="KiCadObject")


@dataclass
class ParseCursor:
    """Lightweight cursor for tracking position in S-expression."""

    sexpr: SExpr  # Current S-expression
    parser: SExprParser  # Single parser (passed through)
    path: List[str]  # Path for debugging
    strictness: ParseStrictness  # Parse strictness level

    def enter(self, sexpr: SExpr, name: str) -> "ParseCursor":
        """Create new cursor for nested object."""
        return ParseCursor(
            sexpr=sexpr,
            parser=self.parser,  # Same parser passed through
            path=self.path + [name],
            strictness=self.strictness,  # Pass through strictness
        )

    def get_path_str(self) -> str:
        return " > ".join(self.path)


class ParseStrictness(Enum):
    """Parser strictness levels for error handling."""

    STRICT = "strict"  # Raise exceptions for all parsing errors
    SILENT = "silent"  # Silently use defaults for missing fields
    FAILSAFE = "failsafe"  # Log warnings and use defaults for missing fields


class FieldType(Enum):
    """Optimized classification with correct Optional/Required handling."""

    PRIMITIVE = "primitive"  # str, int, float (required)
    OPTIONAL_PRIMITIVE = "optional_primitive"  # Optional[str], etc. (optional)
    LIST = "list"  # List[T] AND Optional[List[T]] - both treated equally!
    KICAD_OBJECT = "kicad_object"  # KiCadObject (required)
    OPTIONAL_KICAD_OBJECT = "optional_kicad_object"  # Optional[KiCadObject] (optional)
    OPTIONAL_FLAG = "optional_flag"  # OptionalFlag (always optional by definition)


@dataclass
class FieldInfo:
    """Complete field information for optimized parsing."""

    name: str
    field_type: FieldType
    inner_type: Type[Any]
    position_index: int
    token_name: Optional[str] = None


@dataclass
class KiCadObject(ABC):
    """Base class for KiCad S-expression objects with cursor-based parsing."""

    __token_name__: ClassVar[str] = ""
    _field_info_cache: ClassVar[List[FieldInfo]]
    _field_defaults_cache: ClassVar[Dict[str, Any]]

    def __post_init__(self) -> None:
        """Validate token name is defined."""
        if not self.__token_name__:
            raise ValueError(
                f"Class {self.__class__.__name__} must define __token_name__"
            )

    @classmethod
    def _log_parse_issue(cls, cursor: ParseCursor, message: str) -> None:
        """Log parsing issues based on strictness level from cursor."""
        if cursor.strictness == ParseStrictness.STRICT:
            raise ValueError(message)
        elif cursor.strictness == ParseStrictness.FAILSAFE:
            logging.warning(message)
        # SILENT mode: do nothing

    @classmethod
    def from_sexpr(
        cls: Type[T],
        sexpr: Union[str, SExpr],
        strictness: ParseStrictness = ParseStrictness.STRICT,
    ) -> T:
        """Single public entry point - parser created once here."""

        # Create parser only once here
        if isinstance(sexpr, str):
            parser = SExprParser.from_string(sexpr)
            sexpr = parser.sexpr
        else:
            parser = SExprParser(sexpr, track_usage=False)

        # Create cursor with parser and parse directly
        cursor = ParseCursor(
            sexpr=sexpr, parser=parser, path=[cls.__name__], strictness=strictness
        )
        return cls._parse_recursive(cursor)

    @classmethod
    def from_str(
        cls: Type[T],
        sexpr_string: str,
        strictness: ParseStrictness = ParseStrictness.STRICT,
    ) -> T:
        """Parse from S-expression string - convenience method for better clarity."""
        sexpr = str_to_sexpr(sexpr_string)
        return cls.from_sexpr(sexpr, strictness)

    @classmethod
    def _parse_recursive(cls: Type[T], cursor: ParseCursor) -> T:
        """Internal recursive parse function - uses existing parser."""

        if not cursor.sexpr or str(cursor.sexpr[0]) != cls.__token_name__:
            raise ValueError(
                f"Token mismatch at {cursor.get_path_str()}: "
                f"expected '{cls.__token_name__}', got '{cursor.sexpr[0] if cursor.sexpr else 'empty'}'"
            )

        field_infos = cls._classify_fields()
        field_defaults = cls._get_field_defaults()
        parsed_values = {}

        for field_info in field_infos:
            value = cls._parse_field_recursive(field_info, cursor, field_defaults)
            if value is not None:
                parsed_values[field_info.name] = value
            elif field_info.name in field_defaults:
                parsed_values[field_info.name] = field_defaults[field_info.name]

        # Usage check removed - COMPLETE mode no longer supported

        return cls(**parsed_values)

    @classmethod
    def _classify_fields(cls) -> List[FieldInfo]:
        """Pre-classify all fields for optimized parsing with caching."""
        if not hasattr(cls, "_field_info_cache"):
            field_types = get_type_hints(cls)
            field_infos: List[FieldInfo] = []
            position_index = 0

            for field in fields(cls):
                if field.name.startswith("_"):
                    continue

                field_type = field_types[field.name]
                field_info = cls._classify_field(field.name, field_type, position_index)
                field_infos.append(field_info)
                position_index += 1

            cls._field_info_cache = field_infos

        return cls._field_info_cache

    @classmethod
    def _get_field_defaults(cls) -> Dict[str, Any]:
        """Get field defaults with caching."""
        if not hasattr(cls, "_field_defaults_cache"):
            cls._field_defaults_cache = {
                f.name: f.default for f in fields(cls) if f.default != MISSING
            }
        return cls._field_defaults_cache

    @classmethod
    def _classify_field(
        cls, name: str, field_type: Type[Any], position: int
    ) -> FieldInfo:
        """Correct classification with list simplification."""

        is_optional = get_origin(field_type) is Union and type(None) in get_args(
            field_type
        )
        inner_type = field_type
        if is_optional:
            inner_type = next(
                arg for arg in get_args(field_type) if arg is not type(None)
            )

        # Lists are ALWAYS treated equally - Optional[List] = List
        if get_origin(inner_type) in (list, List):
            list_element_type = get_args(inner_type)[0] if get_args(inner_type) else str
            return FieldInfo(
                name=name,
                field_type=FieldType.LIST,  # Always LIST, never optional
                inner_type=list_element_type,
                position_index=position,
                token_name=(
                    getattr(list_element_type, "__token_name__", None)
                    if hasattr(list_element_type, "__token_name__")
                    else None
                ),
            )

        # OptionalFlag
        try:
            if isinstance(inner_type, type) and issubclass(inner_type, OptionalFlag):
                return FieldInfo(
                    name=name,
                    field_type=FieldType.OPTIONAL_FLAG,
                    inner_type=inner_type,
                    position_index=position,
                )
        except TypeError:
            pass

        # KiCadObject
        try:
            if isinstance(inner_type, type) and issubclass(inner_type, KiCadObject):
                field_type_enum = (
                    FieldType.OPTIONAL_KICAD_OBJECT
                    if is_optional
                    else FieldType.KICAD_OBJECT
                )
                return FieldInfo(
                    name=name,
                    field_type=field_type_enum,
                    inner_type=inner_type,
                    position_index=position,
                    token_name=getattr(inner_type, "__token_name__", None),
                )
        except TypeError:
            pass

        # Primitive
        field_type_enum = (
            FieldType.OPTIONAL_PRIMITIVE if is_optional else FieldType.PRIMITIVE
        )
        return FieldInfo(
            name=name,
            field_type=field_type_enum,
            inner_type=inner_type,
            position_index=position,
        )

    @classmethod
    def _parse_field_recursive(
        cls,
        field_info: FieldInfo,
        cursor: ParseCursor,
        field_defaults: Dict[str, Any],
    ) -> Any:
        """Simplified logic with correct Required/Optional handling."""

        if field_info.field_type == FieldType.LIST:
            return cls._parse_list_with_cursor(field_info, cursor)

        elif field_info.field_type == FieldType.OPTIONAL_FLAG:
            return cls._parse_optional_flag_with_cursor(field_info, cursor)

        elif field_info.field_type in (
            FieldType.KICAD_OBJECT,
            FieldType.OPTIONAL_KICAD_OBJECT,
        ):
            result = cls._parse_nested_object(field_info, cursor)
            # Validation: Required objects must be found
            if result is None and field_info.field_type == FieldType.KICAD_OBJECT:
                cls._log_parse_issue(
                    cursor,
                    f"{cursor.get_path_str()}: Required object '{field_info.name}' not found",
                )
            return result

        else:  # PRIMITIVE or OPTIONAL_PRIMITIVE
            result = cls._parse_primitive_with_cursor(
                field_info, cursor, field_defaults
            )
            # Validation: Required primitives must be found
            if result is None and field_info.field_type == FieldType.PRIMITIVE:
                cls._log_parse_issue(
                    cursor,
                    f"{cursor.get_path_str()}: Required field '{field_info.name}' not found",
                )
            return result

    @classmethod
    def _parse_list_with_cursor(
        cls,
        field_info: FieldInfo,
        cursor: ParseCursor,
    ) -> List[Any]:
        """Parse list of values with cursor tracking."""
        result: List[Any] = []
        sexpr_data = cursor.sexpr[1:]  # Skip token name

        if field_info.token_name:  # List of KiCadObjects
            for i, item in enumerate(sexpr_data, 1):
                if (
                    isinstance(item, list)
                    and item
                    and str(item[0]) == field_info.token_name
                ):
                    cursor.parser.mark_used(i)  # Mark in main parser
                    item_cursor = cursor.enter(
                        item, f"{field_info.token_name}[{len(result)}]"
                    )
                    parsed_item = field_info.inner_type._parse_recursive(item_cursor)
                    result.append(parsed_item)
        else:  # List of primitives: (field_name val1 val2 val3)
            for i, item in enumerate(sexpr_data, 1):
                if (
                    isinstance(item, list)
                    and len(item) > 1
                    and str(item[0]) == field_info.name
                ):
                    cursor.parser.mark_used(i)  # Mark in main parser
                    for value in item[1:]:
                        converted = cls._convert_value(value, field_info.inner_type)
                        result.append(converted)
                    break

        return result  # Always list, never None

    @classmethod
    def _parse_nested_object(
        cls,
        field_info: FieldInfo,
        cursor: ParseCursor,
    ) -> Optional[KiCadObject]:
        """Parse nested KiCadObject using token name."""
        if not field_info.token_name:
            return None

        sexpr_data = cursor.sexpr[1:]  # Skip token name
        for i, item in enumerate(sexpr_data, 1):
            if (
                isinstance(item, list)
                and item
                and str(item[0]) == field_info.token_name
            ):
                cursor.parser.mark_used(i)  # Mark in main parser
                nested_cursor = cursor.enter(item, field_info.token_name)
                return cast(
                    KiCadObject,
                    field_info.inner_type._parse_recursive(nested_cursor),
                )

        return None

    @classmethod
    def _parse_optional_flag_with_cursor(
        cls,
        field_info: FieldInfo,
        cursor: ParseCursor,
    ) -> OptionalFlag:
        """Parse OptionalFlag with cursor tracking."""
        sexpr_data = cursor.sexpr[1:]  # Skip token name

        for i, item in enumerate(sexpr_data, 1):
            if str(item) == field_info.name:
                cursor.parser.mark_used(i)  # Mark in main parser
                result = OptionalFlag(field_info.name)
                result.__found__ = True
                return result

        # Not found
        return OptionalFlag(field_info.name)

    @classmethod
    def _parse_primitive_with_cursor(
        cls,
        field_info: FieldInfo,
        cursor: ParseCursor,
        field_defaults: Dict[str, Any],
    ) -> Any:
        """Parse primitive value with cursor tracking."""
        sexpr_data = cursor.sexpr[1:]  # Skip token name

        # Try named field first: (field_name value)
        for i, item in enumerate(sexpr_data, 1):
            if (
                isinstance(item, list)
                and len(item) >= 2
                and str(item[0]) == field_info.name
            ):
                cursor.parser.mark_used(i)  # Mark in main parser
                try:
                    return cls._convert_value(item[1], field_info.inner_type)
                except ValueError as e:
                    cls._log_parse_issue(
                        cursor,
                        f"{cursor.get_path_str()}: Conversion failed for '{field_info.name}': {e}",
                    )

        # Try positional access
        if field_info.position_index < len(sexpr_data):
            value = sexpr_data[field_info.position_index]
            if not isinstance(value, list):
                cursor.parser.mark_used(
                    field_info.position_index + 1
                )  # Mark in main parser
                try:
                    return cls._convert_value(value, field_info.inner_type)
                except ValueError as e:
                    cls._log_parse_issue(
                        cursor,
                        f"{cursor.get_path_str()}: Positional conversion failed for '{field_info.name}': {e}",
                    )

        # Handle missing values
        is_optional_field = field_info.field_type in (
            FieldType.OPTIONAL_PRIMITIVE,
            FieldType.OPTIONAL_KICAD_OBJECT,
            FieldType.OPTIONAL_FLAG,
        )

        default_value = field_defaults.get(field_info.name)
        if default_value is not None:
            if not is_optional_field:
                cls._log_parse_issue(
                    cursor,
                    f"{cursor.get_path_str()}: Missing field '{field_info.name}' (using default: {default_value})",
                )
            return default_value

        if not is_optional_field:
            cls._log_parse_issue(
                cursor,
                f"{cursor.get_path_str()}: Missing required field '{field_info.name}', returning None",
            )

        return None

    @classmethod
    def _convert_value(cls, value: Any, target_type: Type[Any]) -> Any:
        """Convert value to target type with error handling."""
        if value is None:
            raise ValueError(f"Cannot convert None to {target_type.__name__}")

        try:
            if target_type == int:
                return int(value)
            elif target_type == str:
                return str(value)
            elif target_type == float:
                return float(value)
            elif target_type == bool:
                return str(value).lower() in ("yes", "true", "1")
            elif isinstance(target_type, type) and issubclass(target_type, Enum):
                # Handle enum conversion - try by value first, then by name
                if isinstance(value, target_type):
                    return value
                try:
                    return target_type(value)
                except ValueError:
                    # Try by name if value lookup failed
                    return target_type[str(value).upper()]
            else:
                raise ValueError(f"Unsupported type: {target_type}")
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert '{value}' to {target_type.__name__}: {e}")

    def to_sexpr(self) -> SExpr:
        """Convert to S-expression using simple field iteration."""
        result: SExpr = [self.__token_name__]
        field_infos = self._classify_fields()
        field_defaults = self._get_field_defaults()

        for field_info in field_infos:
            value = getattr(self, field_info.name)

            # Lists are never None - always serialize (even if empty)
            if field_info.field_type == FieldType.LIST:
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, KiCadObject):
                            result.append(item.to_sexpr())
                        elif isinstance(item, Enum):
                            result.append(item.value)
                        else:
                            result.append(item)
                # Empty lists are serialized as empty, not skipped

            elif value is None:
                is_optional_field = field_info.field_type in (
                    FieldType.OPTIONAL_PRIMITIVE,
                    FieldType.OPTIONAL_KICAD_OBJECT,
                    FieldType.OPTIONAL_FLAG,
                )
                has_default = field_info.name in field_defaults

                if is_optional_field or has_default:
                    continue  # Skip optional None fields
                else:
                    raise ValueError(
                        f"Required field '{field_info.name}' is None in {self.__class__.__name__}. "
                        f"Field type: {field_info.field_type}"
                    )
            else:
                # Normal serialization for primitives/objects
                if isinstance(value, KiCadObject):
                    result.append(value.to_sexpr())
                elif isinstance(value, OptionalFlag):
                    # Only add the flag to the result if it was found
                    if value.is_present():
                        result.append(value.get_value())
                else:
                    # Primitives as named fields: (field_name value)
                    # Convert enum to its value for serialization
                    if isinstance(value, Enum):
                        result.append([field_info.name, value.value])
                    else:
                        result.append([field_info.name, value])

        return result

    def __eq__(self, other: object) -> bool:
        """Fast and robust equality comparison for KiCadObjects."""
        if not isinstance(other, KiCadObject):
            return False

        if self.__class__ != other.__class__:
            return False

        field_infos = self._classify_fields()

        for field_info in field_infos:
            self_value = getattr(self, field_info.name)
            other_value = getattr(other, field_info.name)

            if (self_value is None) != (other_value is None):
                return False

            if self_value is None and other_value is None:
                continue

            if not isinstance(other_value, type(self_value)):
                return False

            if isinstance(self_value, list):
                if len(self_value) != len(other_value):
                    return False

                for self_item, other_item in zip(self_value, other_value):
                    if isinstance(self_item, KiCadObject):
                        if not self_item.__eq__(other_item):  # Recursive comparison
                            return False
                    else:
                        if self_item != other_item:
                            return False

            elif isinstance(self_value, KiCadObject):
                if not self_value.__eq__(other_value):  # Recursive comparison
                    return False

            else:
                if self_value != other_value:
                    return False

        return True

    def __hash__(self) -> int:
        """Hash implementation - required when implementing __eq__."""
        return hash((self.__class__.__name__, self.__token_name__))

    def to_sexpr_str(self, pretty_print: bool = True) -> str:
        """Convert to formatted S-expression string."""
        return sexpr_to_str(self.to_sexpr(), pretty_print=pretty_print)

    def __str__(self) -> str:
        """String representation showing only non-None values (except for required fields)."""
        field_infos = self._classify_fields()
        field_defaults = self._get_field_defaults()

        non_none_fields = []

        for field_info in field_infos:
            value = getattr(self, field_info.name)

            # Check if field is optional
            is_optional_field = field_info.field_type in (
                FieldType.OPTIONAL_PRIMITIVE,
                FieldType.OPTIONAL_KICAD_OBJECT,
                FieldType.OPTIONAL_FLAG,
            )
            has_default = field_info.name in field_defaults

            # Show field if:
            # 1. Value is not None (for any field), OR
            # 2. Field is required (not optional and no default) even if None
            # Skip optional fields that are None
            if is_optional_field and value is None:
                continue
            elif value is not None or (not is_optional_field and not has_default):
                # Format value for display
                if isinstance(value, list) and len(value) == 0:
                    # Skip empty lists for optional fields
                    if is_optional_field or has_default:
                        continue
                    display_value = "[]"
                elif isinstance(value, OptionalFlag):
                    # Use OptionalFlag's own __str__ method
                    if value.is_present():
                        display_value = str(value)
                    else:
                        continue
                elif isinstance(value, KiCadObject):
                    # Use the custom __str__ for nested KiCadObjects
                    display_value = str(value)
                elif isinstance(value, list):
                    # Handle lists of KiCadObjects recursively
                    if value and isinstance(value[0], KiCadObject):
                        formatted_items = [str(item) for item in value]
                        display_value = f"[{', '.join(formatted_items)}]"
                    else:
                        display_value = repr(value)
                else:
                    display_value = repr(value)

                non_none_fields.append(f"{field_info.name}={display_value}")

        return f"{self.__class__.__name__}({', '.join(non_none_fields)})"


@dataclass
class OptionalFlag:
    """Simple flag container for optional string tokens in S-expressions."""

    _value_: str
    __found__: bool = False

    def __init__(self, value: str):
        self._value_ = value
        self.__found__ = False

    def __str__(self) -> str:
        """Clean string representation."""
        return f"OptionalFlag({self._value_}={self.__found__})"

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"OptionalFlag(value='{self._value_}', found={self.__found__})"

    def __eq__(self, other: object) -> bool:
        """Equality comparison for OptionalFlag objects."""
        if not isinstance(other, OptionalFlag):
            return False
        return self._value_ == other._value_ and self.__found__ == other.is_present()

    def __hash__(self) -> int:
        """Hash implementation - required when implementing __eq__."""
        return hash((self._value_, self.__found__))

    def __bool__(self) -> bool:
        """Boolean conversion - returns True if flag was found."""
        return self.__found__

    def is_present(self) -> bool:
        """Explicit method to check if flag is present."""
        return self.__found__

    def get_value(self) -> str:
        """Return the expected value regardless of found status."""
        return self._value_
