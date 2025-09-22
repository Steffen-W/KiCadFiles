"""Base class for JSON-based KiCad file parsing.

This module provides automatic JSON serialization/deserialization for KiCad files
like .kicad_pro project files. It mirrors the functionality of base_element.py
but is designed specifically for JSON format files.

Key Features:
- Automatic type-aware parsing based on dataclass field definitions
- Round-trip preservation with exact structure preservation option
- Nested object handling for complex data structures
- File I/O methods with proper encoding and extension validation
"""

import copy
import json
from abc import ABC
from dataclasses import MISSING, dataclass, field, fields
from typing import Any, Dict, List, Optional, Type, TypeVar, Union, get_args, get_origin

from .base_element import ParseStrictness

T = TypeVar("T", bound="JsonObject")


@dataclass
class JsonObject(ABC):
    """Base class for JSON-based KiCad objects.

    This class provides similar functionality to KiCadObject but for JSON format files
    like .kicad_pro project files. It automatically handles serialization/deserialization
    based on dataclass field definitions.

    Features:
    - Automatic JSON parsing based on dataclass field definitions
    - Round-trip preservation with `preserve_original` option
    - Type-aware serialization/deserialization for nested objects
    - File I/O methods with extension validation and encoding support
    - Recursive handling of Optional, List, and nested JsonObject types

    Usage:
        @dataclass
        class MyKiCadFile(JsonObject):
            version: int = 1
            data: Optional[Dict[str, Any]] = None

        # Parse from file
        obj = MyKiCadFile.from_file("file.json")

        # Parse from dictionary
        obj = MyKiCadFile.from_dict({"version": 2, "data": {...}})

        # Export with exact round-trip preservation
        data = obj.to_dict(preserve_original=True)
    """

    _original_data: Optional[Dict[str, Any]] = field(
        default=None, init=False, repr=False
    )

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Create instance from dictionary data.

        Args:
            data: Dictionary containing the data

        Returns:
            Instance of the class
        """
        class_fields = {f.name: f for f in fields(cls) if f.init}
        kwargs = {}

        for field_name, field_obj in class_fields.items():
            if field_name in data:
                kwargs[field_name] = cls._parse_field_value(
                    data[field_name], field_obj.type
                )
            elif field_obj.default is not MISSING:
                kwargs[field_name] = field_obj.default
            elif field_obj.default_factory is not MISSING:
                kwargs[field_name] = field_obj.default_factory()

        instance = cls(**kwargs)
        instance._original_data = copy.deepcopy(data)
        return instance

    @classmethod
    def _parse_field_value(cls, value: Any, field_type: Any) -> Any:
        """Parse a field value based on its type annotation.

        Args:
            value: The value to parse
            field_type: The expected type

        Returns:
            Parsed value
        """
        if value is None:
            return None

        origin = get_origin(field_type)

        if origin is Union:
            args = get_args(field_type)
            if len(args) == 2 and type(None) in args:
                # Handle Optional[SomeType]
                actual_type = args[0] if args[1] is type(None) else args[1]
                if value is not None and _is_json_object_type(actual_type):
                    return actual_type.from_dict(value)
            return value

        elif origin is list or origin is List:
            if not isinstance(value, list):
                return value
            args = get_args(field_type)
            if args and _is_json_object_type(args[0]):
                return [args[0].from_dict(item) for item in value]
            return value

        elif _is_json_object_type(field_type):
            # Direct JsonObject type
            return field_type.from_dict(value)

        return value

    @classmethod
    def from_str(
        cls: Type[T],
        json_string: str,
        strictness: ParseStrictness = ParseStrictness.STRICT,
    ) -> T:
        """Parse from JSON string.

        Args:
            json_string: JSON content as string
            strictness: Parse strictness level (not used for JSON, kept for compatibility)

        Returns:
            Instance of the class

        Raises:
            ValueError: If the JSON string is invalid
        """
        try:
            data = json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}") from e

        return cls.from_dict(data)

    @classmethod
    def from_file(
        cls: Type[T],
        file_path: str,
        strictness: ParseStrictness = ParseStrictness.STRICT,
        encoding: str = "utf-8",
    ) -> T:
        """Parse from JSON file.

        Args:
            file_path: Path to JSON file
            strictness: Parse strictness level (not used for JSON, kept for compatibility)
            encoding: File encoding (default: utf-8)

        Returns:
            Instance of the class

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file contains invalid JSON
            UnicodeDecodeError: If the file encoding is incorrect
        """
        # Subclasses should override this for file extension validation
        with open(file_path, "r", encoding=encoding) as f:
            content = f.read()

        return cls.from_str(content, strictness)

    def to_dict(self, preserve_original: bool = False) -> Dict[str, Any]:
        """Convert to dictionary format.

        Args:
            preserve_original: If True and original data exists, return updated
                              original data preserving the exact structure

        Returns:
            Dictionary representation
        """
        if preserve_original and self._original_data is not None:
            return self._update_original_data()
        else:
            return self._to_dict_full()

    def _to_dict_full(self) -> Dict[str, Any]:
        """Convert to full dictionary with all fields."""
        result = {}

        for field_obj in fields(self):
            if not field_obj.init or field_obj.name.startswith("_"):
                continue

            value = getattr(self, field_obj.name)

            if value is not MISSING:
                result[field_obj.name] = self._serialize_value(value)

        return result

    def _serialize_value(self, value: Any) -> Any:
        """Serialize a single value for dictionary output."""
        if value is None:
            return None
        if isinstance(value, JsonObject):
            return value.to_dict(preserve_original=False)
        if isinstance(value, list):
            return [self._serialize_value(item) for item in value]
        if isinstance(value, dict):
            return {k: self._serialize_value(v) for k, v in value.items()}
        return value

    def _update_original_data(self) -> Dict[str, Any]:
        """Update original data with current values while preserving structure."""
        if self._original_data is None:
            return self._to_dict_full()

        updated = copy.deepcopy(self._original_data)
        current_full = self._to_dict_full()
        self._update_nested_dict(updated, current_full)
        return updated

    def _update_nested_dict(
        self, original: Dict[str, Any], current: Dict[str, Any]
    ) -> None:
        """Recursively update nested dictionary preserving original structure."""
        for key in original:
            if key in current:
                if isinstance(original[key], dict) and isinstance(current[key], dict):
                    self._update_nested_dict(original[key], current[key])
                else:
                    original[key] = current[key]

    def to_json_str(
        self, pretty_print: bool = True, preserve_original: bool = False
    ) -> str:
        """Convert to JSON string format.

        Args:
            pretty_print: Whether to format JSON with indentation
            preserve_original: If True, preserve original structure for exact round-trip

        Returns:
            JSON string representation
        """
        data = self.to_dict(preserve_original=preserve_original)
        return (
            json.dumps(data, indent=2, ensure_ascii=False)
            if pretty_print
            else json.dumps(data, separators=(",", ":"), ensure_ascii=False)
        )

    def save_to_file(
        self, file_path: str, encoding: str = "utf-8", preserve_original: bool = False
    ) -> None:
        """Save to JSON file format.

        Args:
            file_path: Path to write the JSON file
            encoding: File encoding (default: utf-8)
            preserve_original: Whether to preserve original structure
        """
        content = self.to_json_str(
            pretty_print=True, preserve_original=preserve_original
        )
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)


def _is_json_object_type(type_hint: Any) -> bool:
    """Check if a type hint represents a JsonObject subclass."""
    try:
        return isinstance(type_hint, type) and issubclass(type_hint, JsonObject)
    except (TypeError, AttributeError):
        return False
