"""Library table classes for KiCad library management.

This module provides dataclasses for parsing and managing KiCad library tables:
- FpLibTable: Footprint library table (fp-lib-table)
- SymLibTable: Symbol library table (sym-lib-table)

Both table types share the same structure with library entries containing:
- name: Library identifier
- type: Library type (typically "KiCad")
- uri: Path to library
- options: Additional options
- descr: Human readable description
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, List

from .base_element import NamedInt, NamedObject, NamedString, ParseStrictness


@dataclass
class LibraryEntry(NamedObject):
    """A single library entry in a library table.

    Represents a (lib ...) entry with name, type, uri, options, and description.

    Args:
        name: Library name/identifier
        type: Library type (e.g., 'KiCad')
        uri: Path to library
        options: Additional options
        descr: Human readable description
    """

    __token_name__: ClassVar[str] = "lib"

    name: NamedString = field(
        default_factory=lambda: NamedString(token="name", value=""),
        metadata={"description": "Library name/identifier"},
    )
    type: NamedString = field(
        default_factory=lambda: NamedString(token="type", value=""),
        metadata={"description": "Library type (e.g., 'KiCad')"},
    )
    uri: NamedString = field(
        default_factory=lambda: NamedString(token="uri", value=""),
        metadata={"description": "Path to library"},
    )
    options: NamedString = field(
        default_factory=lambda: NamedString(token="options", value=""),
        metadata={"description": "Additional options"},
    )
    descr: NamedString = field(
        default_factory=lambda: NamedString(token="descr", value=""),
        metadata={"description": "Human readable description"},
    )


@dataclass
class FpLibTable(NamedObject):
    """Footprint library table (fp-lib-table file).

    Contains version information and a list of footprint library entries.

    Args:
        version: Table format version
        libraries: List of library entries
    """

    __token_name__: ClassVar[str] = "fp_lib_table"

    version: NamedInt = field(
        default_factory=lambda: NamedInt(token="version", value=7),
        metadata={"description": "Table format version"},
    )
    libraries: List[LibraryEntry] = field(
        default_factory=list, metadata={"description": "List of library entries"}
    )

    @classmethod
    def from_file(
        cls,
        file_path: str,
        strictness: ParseStrictness = ParseStrictness.STRICT,
        encoding: str = "utf-8",
    ) -> "FpLibTable":
        """Parse from fp-lib-table file - convenience method for library table operations."""
        if not file_path.endswith("fp-lib-table"):
            raise ValueError("Unsupported file extension. Expected: fp-lib-table")
        with open(file_path, "r", encoding=encoding) as f:
            content = f.read()
        return cls.from_str(content, strictness)

    def save_to_file(self, file_path: str, encoding: str = "utf-8") -> None:
        """Save to fp-lib-table file format.

        Args:
            file_path: Path to write the fp-lib-table file
            encoding: File encoding (default: utf-8)
        """
        if not file_path.endswith("fp-lib-table"):
            raise ValueError("Unsupported file extension. Expected: fp-lib-table")
        content = self.to_sexpr_str()
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)


@dataclass
class SymLibTable(NamedObject):
    """Symbol library table (sym-lib-table file).

    Contains version information and a list of symbol library entries.

    Args:
        version: Table format version
        libraries: List of library entries
    """

    __token_name__: ClassVar[str] = "sym_lib_table"

    version: NamedInt = field(
        default_factory=lambda: NamedInt(token="version", value=7),
        metadata={"description": "Table format version"},
    )
    libraries: List[LibraryEntry] = field(
        default_factory=list, metadata={"description": "List of library entries"}
    )

    @classmethod
    def from_file(
        cls,
        file_path: str,
        strictness: ParseStrictness = ParseStrictness.STRICT,
        encoding: str = "utf-8",
    ) -> "SymLibTable":
        """Parse from sym-lib-table file - convenience method for library table operations."""
        if not file_path.endswith("sym-lib-table"):
            raise ValueError("Unsupported file extension. Expected: sym-lib-table")
        with open(file_path, "r", encoding=encoding) as f:
            content = f.read()
        return cls.from_str(content, strictness)

    def save_to_file(self, file_path: str, encoding: str = "utf-8") -> None:
        """Save to sym-lib-table file format.

        Args:
            file_path: Path to write the sym-lib-table file
            encoding: File encoding (default: utf-8)
        """
        if not file_path.endswith("sym-lib-table"):
            raise ValueError("Unsupported file extension. Expected: sym-lib-table")
        content = self.to_sexpr_str()
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)
