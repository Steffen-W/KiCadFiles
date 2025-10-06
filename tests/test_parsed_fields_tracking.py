"""Tests for _parsed_fields tracking to ensure roundtrip fidelity."""

from dataclasses import dataclass, field
from typing import ClassVar, Optional

from kicadfiles.base_element import NamedObject, NamedString


@dataclass
class FileData(NamedObject):
    """Sample class representing embedded file data."""

    __token_name__: ClassVar[str] = "data"

    content: NamedString = field(
        default_factory=lambda: NamedString("content", ""),
        metadata={"description": "Base64 encoded data"},
    )


@dataclass
class EmbeddedFile(NamedObject):
    """Sample class representing an embedded file."""

    __token_name__: ClassVar[str] = "file"

    name: NamedString = field(
        default_factory=lambda: NamedString("name", ""),
        metadata={"description": "File name"},
    )
    file_type: NamedString = field(
        default_factory=lambda: NamedString("type", ""),
        metadata={"description": "File type"},
    )
    data: Optional[FileData] = field(
        default=None,
        metadata={"description": "File data", "required": False},
    )
    checksum: NamedString = field(
        default_factory=lambda: NamedString("checksum", ""),
        metadata={"description": "File checksum", "required": False},
    )


def test_roundtrip_without_optional_field():
    """Test that optional fields not in original data are not serialized."""
    # Parse file without 'data' field
    original = '(file (name "test.txt") (type "text"))'
    file_obj = EmbeddedFile.from_sexpr(original)

    # Verify parsed_fields is set correctly
    assert hasattr(file_obj, "_parsed_fields")
    assert "name" in file_obj._parsed_fields
    assert "file_type" in file_obj._parsed_fields
    assert "data" not in file_obj._parsed_fields
    assert "checksum" not in file_obj._parsed_fields

    # Verify data has default value but is not serialized
    assert file_obj.data is None

    # Serialize and verify 'data' is not included
    serialized = file_obj.to_sexpr()
    assert serialized == ["file", ["name", "test.txt"], ["type", "text"]]

    # Verify roundtrip produces exact same output
    roundtrip = file_obj.to_sexpr_str()
    assert "(data" not in roundtrip


def test_roundtrip_with_optional_field():
    """Test that optional fields in original data are preserved."""
    # Parse file with 'data' field
    original = '(file (name "test.txt") (type "text") (data (content "base64data")))'
    file_obj = EmbeddedFile.from_sexpr(original)

    # Verify parsed_fields includes 'data'
    assert hasattr(file_obj, "_parsed_fields")
    assert "data" in file_obj._parsed_fields

    # Verify data is present
    assert file_obj.data is not None
    assert file_obj.data.content.value == "base64data"

    # Serialize and verify 'data' is included
    serialized = file_obj.to_sexpr()
    assert ["data", ["content", "base64data"]] in serialized


def test_manual_creation_includes_all_set_fields():
    """Test that manually created objects include all non-None fields."""
    # Create object manually (no parsing)
    file_obj = EmbeddedFile()
    file_obj.name.value = "manual.txt"
    file_obj.file_type.value = "text"
    # Don't set data - leave as None
    file_obj.checksum.value = "abc123"

    # Verify _parsed_fields is None for manually created objects
    assert not hasattr(file_obj, "_parsed_fields") or file_obj._parsed_fields is None

    # Serialize - should include all fields with non-None values
    serialized = file_obj.to_sexpr()

    # Should include name, file_type, and checksum
    assert ["name", "manual.txt"] in serialized
    assert ["type", "text"] in serialized
    assert ["checksum", "abc123"] in serialized

    # Should NOT include data (it's None)
    data_found = any(
        item[0] == "data" if isinstance(item, list) else False for item in serialized
    )
    assert not data_found


def test_manual_creation_with_optional_object():
    """Test manually setting an optional nested object."""
    # Create object manually
    file_obj = EmbeddedFile()
    file_obj.name.value = "manual.txt"
    file_obj.file_type.value = "text"

    # Manually set data
    file_obj.data = FileData()
    file_obj.data.content.value = "manual_base64"

    # Serialize - should include data since it's not None
    serialized = file_obj.to_sexpr()

    assert ["name", "manual.txt"] in serialized
    assert ["type", "text"] in serialized
    assert ["data", ["content", "manual_base64"]] in serialized


def test_hybrid_add_field_after_parsing():
    """Test adding a field to a parsed object."""
    # Parse without data
    original = '(file (name "test.txt") (type "text"))'
    file_obj = EmbeddedFile.from_sexpr(original)

    # Initially data is not serialized
    serialized1 = file_obj.to_sexpr()
    assert not any(
        item[0] == "data" if isinstance(item, list) else False for item in serialized1
    )

    # Now add data and mark it as parsed
    file_obj.data = FileData()
    file_obj.data.content.value = "added_later"
    file_obj._parsed_fields.add("data")

    # Now data should be serialized
    serialized2 = file_obj.to_sexpr()
    assert ["data", ["content", "added_later"]] in serialized2


def test_nested_object_preserves_parsed_fields():
    """Test that nested objects also preserve their parsed_fields."""
    # Parse with nested data
    original = '(file (name "test.txt") (type "text") (data (content "base64")))'
    file_obj = EmbeddedFile.from_sexpr(original)

    # Verify nested object also has _parsed_fields
    assert hasattr(file_obj.data, "_parsed_fields")
    assert "content" in file_obj.data._parsed_fields

    # Roundtrip should preserve structure
    serialized = file_obj.to_sexpr()
    assert ["data", ["content", "base64"]] in serialized


if __name__ == "__main__":
    import sys

    import pytest

    sys.exit(pytest.main([__file__, "-v"]))
