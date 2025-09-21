"""Symbol library elements for KiCad S-expressions - schematic symbol definitions."""

from dataclasses import dataclass, field
from typing import Any, Optional

from .base_element import KiCadObject, OptionalFlag, ParseStrictness
from .base_types import At, Effects, Property
from .enums import PinElectricalType, PinGraphicStyle
from .text_and_documents import Generator, Version


@dataclass
class Extends(KiCadObject):
    """Symbol extension definition token.

    The 'extends' token defines inheritance from another symbol in the format::

        (extends "LIBRARY_ID")

    Args:
        library_id: Parent symbol library ID (str)
    """

    __token_name__ = "extends"

    library_id: str = field(
        default="", metadata={"description": "Parent symbol library ID"}
    )


@dataclass
class FieldsAutoplaced(KiCadObject):
    """Fields autoplaced flag token.

    The 'fields_autoplaced' token indicates that symbol fields were automatically placed in the format::

        (fields_autoplaced)

    This is a flag token that indicates fields were autoplaced when present.

    Args:
        value: Always True when token is present (bool)
    """

    __token_name__ = "fields_autoplaced"

    value: bool = field(
        default=True, metadata={"description": "Fields autoplaced flag"}
    )


@dataclass
class InBom(KiCadObject):
    """In BOM flag definition token.

    The 'in_bom' token defines whether a symbol appears in bill of materials in the format::

        (in_bom yes | no)

    Args:
        value: Whether symbol appears in BOM (bool)
    """

    __token_name__ = "in_bom"

    value: bool = field(
        default=True, metadata={"description": "Whether symbol appears in BOM"}
    )


@dataclass
class Instances(KiCadObject):
    """Symbol instances definition token.

    The 'instances' token defines symbol instances in a schematic in the format::

        (instances
            (project "PROJECT_NAME"
                (path "/PATH" (reference "REF") (unit N) (value "VALUE") (footprint "FOOTPRINT"))
            )
        )

    Args:
        instances: List of instance data (list of objects)
    """

    __token_name__ = "instances"

    instances: list[Any] = field(
        default_factory=list, metadata={"description": "List of instance data"}
    )


@dataclass
class Number(KiCadObject):
    """Pin number definition token.

    The 'number' token defines a pin number with text effects in the format::

        (number "NUMBER" TEXT_EFFECTS)

    Args:
        number: Pin number string (str)
        effects: Text effects (Effects object, optional)
    """

    __token_name__ = "number"

    number: str = field(default="", metadata={"description": "Pin number string"})
    effects: Optional[Effects] = field(
        default=None, metadata={"description": "Text effects", "required": False}
    )


@dataclass
class Pin(KiCadObject):
    """Symbol pin definition token.

    The 'pin' token defines a symbol pin in the format::

        (pin
            PIN_ELECTRICAL_TYPE
            PIN_GRAPHIC_STYLE
            POSITION_IDENTIFIER
            (length LENGTH)
            (name "NAME" TEXT_EFFECTS)
            (number "NUMBER" TEXT_EFFECTS)
        )

    Args:
        electrical_type: Pin electrical type (str)
        graphic_style: Pin graphic style (str)
        at: Position and rotation (At object)
        length: Pin length (float)
        name: Pin name (str, optional)
        name_effects: Pin name text effects (Effects object, optional)
        number: Pin number (str, optional)
        number_effects: Pin number text effects (Effects object, optional)
        hide: Whether pin is hidden (bool, optional)
    """

    __token_name__ = "pin"

    electrical_type: PinElectricalType = field(
        default=PinElectricalType.PASSIVE,
        metadata={"description": "Pin electrical type"},
    )
    graphic_style: PinGraphicStyle = field(
        default=PinGraphicStyle.LINE, metadata={"description": "Pin graphic style"}
    )
    at: At = field(
        default_factory=lambda: At(), metadata={"description": "Position and rotation"}
    )
    length: float = field(default=2.54, metadata={"description": "Pin length"})
    name: Optional[str] = field(
        default=None, metadata={"description": "Pin name", "required": False}
    )
    name_effects: Optional[Effects] = field(
        default=None,
        metadata={"description": "Pin name text effects", "required": False},
    )
    number: Optional[Number] = field(
        default=None, metadata={"description": "Pin number", "required": False}
    )
    number_effects: Optional[Effects] = field(
        default=None,
        metadata={"description": "Pin number text effects", "required": False},
    )
    hide: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag("hide"),
        metadata={"description": "Whether pin is hidden", "required": False},
    )


@dataclass
class PinNames(KiCadObject):
    """Pin names attributes definition token.

    The 'pin_names' token defines attributes for all pin names of a symbol in the format::

        (pin_names [(offset OFFSET)] [hide])

    Args:
        offset: Pin name offset (float, optional)
        hide: Whether pin names are hidden (bool, optional)
    """

    __token_name__ = "pin_names"

    offset: Optional[float] = field(
        default=None, metadata={"description": "Pin name offset", "required": False}
    )
    hide: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag("hide"),
        metadata={"description": "Whether pin names are hidden", "required": False},
    )


@dataclass
class PinNumbers(KiCadObject):
    """Pin numbers visibility definition token.

    The 'pin_numbers' token defines visibility of pin numbers for a symbol in the format::

        (pin_numbers [hide])

    Args:
        hide: Whether pin numbers are hidden (bool, optional)
    """

    __token_name__ = "pin_numbers"

    hide: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag("hide"),
        metadata={"description": "Whether pin numbers are hidden", "required": False},
    )


@dataclass
class Pinfunction(KiCadObject):
    """Pin function definition token.

    The 'pinfunction' token defines the function name for a pin in the format::

        (pinfunction "FUNCTION_NAME")

    Args:
        function: Pin function name (str)
    """

    __token_name__ = "pinfunction"

    function: str = field(default="", metadata={"description": "Pin function name"})


@dataclass
class Pintype(KiCadObject):
    """Pin type definition token.

    The 'pintype' token defines the electrical type for a pin in the format::

        (pintype "TYPE")

    Where TYPE can be: input, output, bidirectional, tri_state, passive, free,
    unspecified, power_in, power_out, open_collector, open_emitter, no_connect

    Args:
        type: Pin electrical type (str)
    """

    __token_name__ = "pintype"

    type: PinElectricalType = field(
        default=PinElectricalType.PASSIVE,
        metadata={"description": "Pin electrical type"},
    )


@dataclass
class Prefix(KiCadObject):
    """Reference prefix definition token.

    The 'prefix' token defines the reference prefix for a symbol in the format::

        (prefix "PREFIX")

    Args:
        prefix: Reference prefix string (str)
    """

    __token_name__ = "prefix"

    prefix: str = field(default="", metadata={"description": "Reference prefix string"})


@dataclass
class UnitName(KiCadObject):
    """Unit name definition token.

    The 'unit_name' token defines the display name for a symbol subunit in the format::

        (unit_name "NAME")

    Args:
        name: Unit display name (str)
    """

    __token_name__ = "unit_name"

    name: str = field(default="", metadata={"description": "Unit display name"})


@dataclass
class Symbol(KiCadObject):
    """Symbol definition token.

    The 'symbol' token defines a complete schematic symbol in the format::

        (symbol "LIBRARY_ID"
            [(extends "LIBRARY_ID")]
            [(pin_numbers hide)]
            [(pin_names [(offset OFFSET)] hide)]
            (in_bom yes | no)
            (on_board yes | no)
            SYMBOL_PROPERTIES...
            GRAPHIC_ITEMS...
            PINS...
            UNITS...
            [(unit_name "UNIT_NAME")]
        )

    Args:
        library_id: Unique library identifier or unit ID (str)
        extends: Parent library ID for derived symbols (str, optional)
        pin_numbers: Pin numbers visibility settings (PinNumbers object, optional)
        pin_names: Pin names attributes (PinNames object, optional)
        in_bom: Whether symbol appears in BOM (bool)
        on_board: Whether symbol is exported to PCB (bool)
        properties: List of symbol properties (list of Property objects, optional)
        graphic_items: List of graphical items (list, optional)
        pins: List of symbol pins (list of Pin objects, optional)
        units: List of child symbol units (list of Symbol objects, optional)
        unit_name: Display name for subunits (str, optional)
    """

    __token_name__ = "symbol"

    library_id: str = field(
        default="", metadata={"description": "Unique library identifier or unit ID"}
    )
    extends: Optional[str] = field(
        default=None,
        metadata={
            "description": "Parent library ID for derived symbols",
            "required": False,
        },
    )
    pin_numbers: Optional[PinNumbers] = field(
        default=None,
        metadata={"description": "Pin numbers visibility settings", "required": False},
    )
    pin_names: Optional[PinNames] = field(
        default=None,
        metadata={"description": "Pin names attributes", "required": False},
    )
    in_bom: bool = field(
        default=True, metadata={"description": "Whether symbol appears in BOM"}
    )
    on_board: bool = field(
        default=True, metadata={"description": "Whether symbol is exported to PCB"}
    )
    properties: Optional[list[Property]] = field(
        default_factory=list,
        metadata={"description": "List of symbol properties", "required": False},
    )
    graphic_items: Optional[list[Any]] = field(
        default_factory=list,
        metadata={"description": "List of graphical items", "required": False},
    )
    pins: Optional[list[Pin]] = field(
        default_factory=list,
        metadata={"description": "List of symbol pins", "required": False},
    )
    units: Optional[list["Symbol"]] = field(
        default_factory=list,
        metadata={"description": "List of child symbol units", "required": False},
    )
    unit_name: Optional[str] = field(
        default=None,
        metadata={"description": "Display name for subunits", "required": False},
    )


@dataclass
class LibSymbols(KiCadObject):
    """Library symbols container token.

    The 'lib_symbols' token defines a symbol library containing all symbols used in the schematic in the format::

        (lib_symbols
            SYMBOL_DEFINITIONS...
        )

    Args:
        symbols: List of symbols (list of Symbol objects)
    """

    __token_name__ = "lib_symbols"

    symbols: list[Symbol] = field(
        default_factory=list, metadata={"description": "List of symbols"}
    )


@dataclass
class KicadSymbolLib(KiCadObject):
    """KiCad symbol library file definition.

    The 'kicad_symbol_lib' token defines a complete symbol library file in the format::

        (kicad_symbol_lib
            (version VERSION)
            (generator GENERATOR)
            ;; symbol definitions...
        )

    Args:
        version: File format version
        generator: Generator application name
        symbols: List of symbol definitions (optional)
    """

    __token_name__ = "kicad_symbol_lib"

    version: Version = field(
        default_factory=lambda: Version(),
        metadata={"description": "File format version"},
    )
    generator: Generator = field(
        default_factory=lambda: Generator(),
        metadata={"description": "Generator application name"},
    )
    symbols: Optional[list[Symbol]] = field(
        default_factory=list,
        metadata={"description": "List of symbol definitions", "required": False},
    )

    @classmethod
    def from_file(
        cls,
        file_path: str,
        strictness: ParseStrictness = ParseStrictness.STRICT,
        encoding: str = "utf-8",
    ) -> "KicadSymbolLib":
        """Parse from S-expression file - convenience method for symbol library operations."""
        if not file_path.endswith(".kicad_sym"):
            raise ValueError("Unsupported file extension. Expected: .kicad_sym")
        with open(file_path, "r", encoding=encoding) as f:
            content = f.read()
        return cls.from_str(content, strictness)

    def save_to_file(self, file_path: str, encoding: str = "utf-8") -> None:
        """Save to .kicad_sym file format.

        Args:
            file_path: Path to write the .kicad_sym file
            encoding: File encoding (default: utf-8)
        """
        if not file_path.endswith(".kicad_sym"):
            raise ValueError("Unsupported file extension. Expected: .kicad_sym")
        content = self.to_sexpr_str(pretty_print=True)
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)
