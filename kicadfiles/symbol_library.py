"""Symbol library elements for KiCad S-expressions - schematic symbol definitions."""

from dataclasses import dataclass, field
from typing import Any, ClassVar, List, Optional, Union

from .base_element import (
    NamedFloat,
    NamedInt,
    NamedObject,
    NamedString,
    ParseStrictness,
    TokenFlag,
)
from .base_types import At, Effects, Property, Text
from .enums import PinElectricalType, PinGraphicStyle
from .primitive_graphics import Arc, Bezier, Circle, Line, Polygon, Polyline, Rectangle


@dataclass
class Instances(NamedObject):
    """Symbol instances definition token.

    The 'instances' token defines symbol instances in a schematic in the format::

        (instances
            (project "PROJECT_NAME"
                (path "/PATH" (reference "REF") (unit N) (value "VALUE") (footprint "FOOTPRINT"))
            )
        )

    Args:
        instances: List of instance data
    """

    __token_name__: ClassVar[str] = "instances"

    instances: List[Any] = field(
        default_factory=list, metadata={"description": "List of instance data"}
    )


@dataclass
class PinName(NamedObject):
    """Pin name definition token.

    The 'name' token defines a pin name with text effects in the format::

        (name "NAME" TEXT_EFFECTS)

    Args:
        name: Pin name string
        effects: Text effects (optional)
    """

    __token_name__: ClassVar[str] = "name"

    name: str = field(default="", metadata={"description": "Pin name string"})
    effects: Effects = field(
        default_factory=lambda: Effects(),
        metadata={"description": "Text effects", "required": False},
    )


@dataclass
class Number(NamedObject):
    """Pin number definition token.

    The 'number' token defines a pin number with text effects in the format::

        (number "NUMBER" TEXT_EFFECTS)

    Args:
        number: Pin number string
        effects: Text effects (optional)
    """

    __token_name__: ClassVar[str] = "number"

    number: str = field(default="", metadata={"description": "Pin number string"})
    effects: Effects = field(
        default_factory=lambda: Effects(),
        metadata={"description": "Text effects", "required": False},
    )


@dataclass
class Pin(NamedObject):
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
        electrical_type: Pin electrical type
        graphic_style: Pin graphic style
        at: Position and rotation
        length: Pin length
        name: Pin name (optional)
        number: Pin number (optional)
        hide: Whether pin is hidden (optional)
    """

    __token_name__: ClassVar[str] = "pin"

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
    length: NamedFloat = field(
        default_factory=lambda: NamedFloat("length", 2.54),
        metadata={"description": "Pin length"},
    )
    name: PinName = field(
        default_factory=lambda: PinName(),
        metadata={"description": "Pin name", "required": False},
    )
    number: Number = field(
        default_factory=lambda: Number(),
        metadata={"description": "Pin number", "required": False},
    )
    hide: TokenFlag = field(
        default_factory=lambda: TokenFlag("hide"),
        metadata={"description": "Whether pin is hidden", "required": False},
    )


@dataclass
class PinNames(NamedObject):
    """Pin names attributes definition token.

    The 'pin_names' token defines attributes for all pin names of a symbol in the format::

        (pin_names [(offset OFFSET)] [hide])

    Args:
        offset: Pin name offset (optional)
        hide: Whether pin names are hidden (optional)
    """

    __token_name__: ClassVar[str] = "pin_names"

    offset: Optional[float] = field(
        default=None, metadata={"description": "Pin name offset", "required": False}
    )
    hide: TokenFlag = field(
        default_factory=lambda: TokenFlag("hide"),
        metadata={"description": "Whether pin names are hidden", "required": False},
    )


@dataclass
class PinNumbers(NamedObject):
    """Pin numbers visibility definition token.

    The 'pin_numbers' token defines visibility of pin numbers for a symbol in the format::

        (pin_numbers [hide])

    Args:
        hide: Whether pin numbers are hidden (optional)
    """

    __token_name__: ClassVar[str] = "pin_numbers"

    hide: TokenFlag = field(
        default_factory=lambda: TokenFlag("hide"),
        metadata={"description": "Whether pin numbers are hidden", "required": False},
    )


@dataclass
class Pintype(NamedObject):
    """Pin type definition token.

    The 'pintype' token defines the electrical type for a pin in the format::

        (pintype "TYPE")

    Where TYPE can be: input, output, bidirectional, tri_state, passive, free,
    unspecified, power_in, power_out, open_collector, open_emitter, no_connect

    Args:
        type: Pin electrical type
    """

    __token_name__: ClassVar[str] = "pintype"

    type: PinElectricalType = field(
        default=PinElectricalType.PASSIVE,
        metadata={"description": "Pin electrical type"},
    )


@dataclass
class Symbol(NamedObject):
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
        library_id: Unique library identifier or unit ID
        extends: Parent library ID for derived symbols (optional)
        pin_numbers: Pin numbers visibility settings (optional)
        pin_names: Pin names attributes (optional)
        in_bom: Whether symbol appears in BOM (optional)
        on_board: Whether symbol is exported to PCB (yes/no) (optional)
        exclude_from_sim: Whether symbol is excluded from simulation (optional)
        power: Whether symbol is a power symbol (optional)
        properties: List of symbol properties (optional)
        graphic_items: List of graphical items (optional)
        text: List of text elements (optional)
        pins: List of symbol pins (optional)
        units: List of child symbol units (optional)
        unit_name: Display name for subunits (optional)
        embedded_fonts: Whether embedded fonts are used (optional)
    """

    __token_name__: ClassVar[str] = "symbol"

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
    in_bom: TokenFlag = field(
        default_factory=lambda: TokenFlag("in_bom"),
        metadata={"description": "Whether symbol appears in BOM", "required": False},
    )
    on_board: TokenFlag = field(
        default_factory=lambda: TokenFlag("on_board"),
        metadata={
            "description": "Whether symbol is exported to PCB (yes/no)",
            "required": False,
        },
    )
    exclude_from_sim: TokenFlag = field(
        default_factory=lambda: TokenFlag("exclude_from_sim"),
        metadata={
            "description": "Whether symbol is excluded from simulation",
            "required": False,
        },
    )
    power: TokenFlag = field(
        default_factory=lambda: TokenFlag("power"),
        metadata={
            "description": "Whether symbol is a power symbol",
            "required": False,
        },
    )
    properties: Optional[List[Property]] = field(
        default_factory=list,
        metadata={"description": "List of symbol properties", "required": False},
    )
    graphic_items: Optional[
        List[Union[Arc, Bezier, Circle, Line, Polygon, Polyline, Rectangle]]
    ] = field(
        default_factory=list,
        metadata={"description": "List of graphical items", "required": False},
    )
    text: Optional[List[Text]] = field(
        default_factory=list,
        metadata={"description": "List of text elements", "required": False},
    )
    pins: Optional[List[Pin]] = field(
        default_factory=list,
        metadata={"description": "List of symbol pins", "required": False},
    )
    units: Optional[List["Symbol"]] = field(
        default_factory=list,
        metadata={"description": "List of child symbol units", "required": False},
    )
    unit_name: Optional[str] = field(
        default=None,
        metadata={"description": "Display name for subunits", "required": False},
    )
    embedded_fonts: TokenFlag = field(
        default_factory=lambda: TokenFlag("embedded_fonts"),
        metadata={
            "description": "Whether embedded fonts are used",
            "required": False,
        },
    )


@dataclass
class LibSymbols(NamedObject):
    """Library symbols container token.

    The 'lib_symbols' token defines a symbol library containing all symbols used in the schematic in the format::

        (lib_symbols
            SYMBOL_DEFINITIONS...
        )

    Args:
        symbols: List of symbols
    """

    __token_name__: ClassVar[str] = "lib_symbols"

    symbols: List[Symbol] = field(
        default_factory=list, metadata={"description": "List of symbols"}
    )


@dataclass
class KicadSymbolLib(NamedObject):
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
        generator_version: Generator version (optional)
        symbols: List of symbol definitions (optional)
    """

    __token_name__: ClassVar[str] = "kicad_symbol_lib"

    version: NamedInt = field(
        default_factory=lambda: NamedInt("version", 20240101),
        metadata={"description": "File format version"},
    )
    generator: NamedString = field(
        default_factory=lambda: NamedString("generator", ""),
        metadata={"description": "Generator application name"},
    )
    generator_version: NamedString = field(
        default_factory=lambda: NamedString("generator_version", ""),
        metadata={"description": "Generator version", "required": False},
    )
    symbols: Optional[List[Symbol]] = field(
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
        content = self.to_sexpr_str()
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)
