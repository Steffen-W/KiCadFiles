"""Symbol library elements for KiCad S-expressions - schematic symbol definitions."""

from dataclasses import dataclass, field
from typing import Any, List, Optional

from .base_element import KiCadObject, OptionalFlag, ParseStrictness
from .base_types import At, Effects, Length, Property
from .enums import PinElectricalType, PinGraphicStyle
from .primitive_graphics import Arc, Bezier, Circle, Line, Polygon, Polyline, Rectangle
from .text_and_documents import Generator, GeneratorVersion, Version


@dataclass
class Extends(KiCadObject):
    """Symbol extension definition token.

    The 'extends' token defines inheritance from another symbol in the format::

        (extends "LIBRARY_ID")

    Args:
        library_id: Parent symbol library ID
    """

    __token_name__ = "extends"

    library_id: str = field(
        default="", metadata={"description": "Parent symbol library ID"}
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
        instances: List of instance data
    """

    __token_name__ = "instances"

    instances: List[Any] = field(
        default_factory=list, metadata={"description": "List of instance data"}
    )


@dataclass
class PinName(KiCadObject):
    """Pin name definition token.

    The 'name' token defines a pin name with text effects in the format::

        (name "NAME" TEXT_EFFECTS)

    Args:
        name: Pin name string
        effects: Text effects (optional)
    """

    __token_name__ = "name"

    name: str = field(default="", metadata={"description": "Pin name string"})
    effects: Optional[Effects] = field(
        default=None, metadata={"description": "Text effects", "required": False}
    )


@dataclass
class Number(KiCadObject):
    """Pin number definition token.

    The 'number' token defines a pin number with text effects in the format::

        (number "NUMBER" TEXT_EFFECTS)

    Args:
        number: Pin number string
        effects: Text effects (optional)
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
        electrical_type: Pin electrical type
        graphic_style: Pin graphic style
        at: Position and rotation
        length: Pin length
        name: Pin name (optional)
        number: Pin number (optional)
        hide: Whether pin is hidden (optional)
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
    length: Length = field(
        default_factory=lambda: Length(value=2.54),
        metadata={"description": "Pin length"},
    )
    name: Optional[PinName] = field(
        default=None, metadata={"description": "Pin name", "required": False}
    )
    number: Optional[Number] = field(
        default=None, metadata={"description": "Pin number", "required": False}
    )
    hide: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("hide"),
        metadata={"description": "Whether pin is hidden", "required": False},
    )


@dataclass
class PinNames(KiCadObject):
    """Pin names attributes definition token.

    The 'pin_names' token defines attributes for all pin names of a symbol in the format::

        (pin_names [(offset OFFSET)] [hide])

    Args:
        offset: Pin name offset (optional)
        hide: Whether pin names are hidden (optional)
    """

    __token_name__ = "pin_names"

    offset: Optional[float] = field(
        default=None, metadata={"description": "Pin name offset", "required": False}
    )
    hide: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("hide"),
        metadata={"description": "Whether pin names are hidden", "required": False},
    )


@dataclass
class PinNumbers(KiCadObject):
    """Pin numbers visibility definition token.

    The 'pin_numbers' token defines visibility of pin numbers for a symbol in the format::

        (pin_numbers [hide])

    Args:
        hide: Whether pin numbers are hidden (optional)
    """

    __token_name__ = "pin_numbers"

    hide: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("hide"),
        metadata={"description": "Whether pin numbers are hidden", "required": False},
    )


@dataclass
class Pinfunction(KiCadObject):
    """Pin function definition token.

    The 'pinfunction' token defines the function name for a pin in the format::

        (pinfunction "FUNCTION_NAME")

    Args:
        function: Pin function name
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
        type: Pin electrical type
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
        prefix: Reference prefix string
    """

    __token_name__ = "prefix"

    prefix: str = field(default="", metadata={"description": "Reference prefix string"})


@dataclass
class UnitName(KiCadObject):
    """Unit name definition token.

    The 'unit_name' token defines the display name for a symbol subunit in the format::

        (unit_name "NAME")

    Args:
        name: Unit display name
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
        library_id: Unique library identifier or unit ID
        extends: Parent library ID for derived symbols (optional)
        pin_numbers: Pin numbers visibility settings (optional)
        pin_names: Pin names attributes (optional)
        in_bom: Whether symbol appears in BOM (optional)
        on_board: Whether symbol is exported to PCB (yes/no) (optional)
        exclude_from_sim: Whether symbol is excluded from simulation (optional)
        embedded_fonts: Whether embedded fonts are used (optional)
        power: Whether symbol is a power symbol (optional)
        properties: List of symbol properties (optional)
        arcs: List of arc graphical items (optional)
        beziers: List of bezier graphical items (optional)
        circles: List of circle graphical items (optional)
        lines: List of line graphical items (optional)
        polygons: List of polygon graphical items (optional)
        polylines: List of polyline graphical items (optional)
        rectangles: List of rectangle graphical items (optional)
        pins: List of symbol pins (optional)
        units: List of child symbol units (optional)
        unit_name: Display name for subunits (optional)
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
    in_bom: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("in_bom"),
        metadata={"description": "Whether symbol appears in BOM", "required": False},
    )
    on_board: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("on_board"),
        metadata={
            "description": "Whether symbol is exported to PCB (yes/no)",
            "required": False,
        },
    )
    exclude_from_sim: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("exclude_from_sim"),
        metadata={
            "description": "Whether symbol is excluded from simulation",
            "required": False,
        },
    )
    embedded_fonts: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("embedded_fonts"),
        metadata={
            "description": "Whether embedded fonts are used",
            "required": False,
        },
    )
    power: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("power"),
        metadata={
            "description": "Whether symbol is a power symbol",
            "required": False,
        },
    )
    properties: Optional[List[Property]] = field(
        default_factory=list,
        metadata={"description": "List of symbol properties", "required": False},
    )
    # graphic_items: Optional[
    #     List[Union[Arc, Bezier, Circle, Line, Polygon, Polyline, Rectangle]]
    # ] = field(
    #     default_factory=list,
    #     metadata={"description": "List of graphical items", "required": False},
    # )
    arcs: Optional[List[Arc]] = field(
        default_factory=list,
        metadata={"description": "List of arc graphical items", "required": False},
    )
    beziers: Optional[List[Bezier]] = field(
        default_factory=list,
        metadata={"description": "List of bezier graphical items", "required": False},
    )
    circles: Optional[List[Circle]] = field(
        default_factory=list,
        metadata={"description": "List of circle graphical items", "required": False},
    )
    lines: Optional[List[Line]] = field(
        default_factory=list,
        metadata={"description": "List of line graphical items", "required": False},
    )
    polygons: Optional[List[Polygon]] = field(
        default_factory=list,
        metadata={"description": "List of polygon graphical items", "required": False},
    )
    polylines: Optional[List[Polyline]] = field(
        default_factory=list,
        metadata={"description": "List of polyline graphical items", "required": False},
    )
    rectangles: Optional[List[Rectangle]] = field(
        default_factory=list,
        metadata={
            "description": "List of rectangle graphical items",
            "required": False,
        },
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


@dataclass
class LibSymbols(KiCadObject):
    """Library symbols container token.

    The 'lib_symbols' token defines a symbol library containing all symbols used in the schematic in the format::

        (lib_symbols
            SYMBOL_DEFINITIONS...
        )

    Args:
        symbols: List of symbols
    """

    __token_name__ = "lib_symbols"

    symbols: List[Symbol] = field(
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
        generator_version: Generator version (optional)
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
    generator_version: Optional[GeneratorVersion] = field(
        default=None,
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
