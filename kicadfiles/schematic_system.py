"""Schematic system elements for KiCad S-expressions - schematic drawing and connectivity."""

from dataclasses import dataclass, field
from typing import Any, Optional

from .base_element import KiCadObject, ParseStrictness
from .base_types import At, Color, Effects, Fill, Property, Pts, Size, Stroke, Uuid
from .symbol_library import LibSymbols, Pin
from .text_and_documents import Generator, GeneratorVersion, Page, Paper, Version


@dataclass
class Bus(KiCadObject):
    """Bus definition token.

    The 'bus' token defines buses in the schematic in the format::

        (bus
            COORDINATE_POINT_LIST
            STROKE_DEFINITION
            UNIQUE_IDENTIFIER
        )

    Args:
        pts: List of X and Y coordinates of start and end points
        stroke: How the bus is drawn
        uuid: Universally unique identifier
    """

    __token_name__ = "bus"

    pts: Pts = field(
        default_factory=lambda: Pts(), metadata={"description": "Bus connection points"}
    )
    stroke: Stroke = field(
        default_factory=lambda: Stroke(), metadata={"description": "Stroke definition"}
    )
    uuid: str = field(default="", metadata={"description": "Unique identifier"})


@dataclass
class BusEntry(KiCadObject):
    """Bus entry definition token.

    The 'bus_entry' token defines a bus entry in the schematic in the format::

        (bus_entry
            POSITION_IDENTIFIER
            (size X Y)
            STROKE_DEFINITION
            UNIQUE_IDENTIFIER
        )

    Args:
        at: X and Y coordinates of the bus entry
        size: X and Y distance of the end point from the position
        stroke: How the bus entry is drawn
        uuid: Universally unique identifier
    """

    __token_name__ = "bus_entry"

    at: At = field(default_factory=lambda: At(), metadata={"description": "Position"})
    size: Size = field(
        default_factory=lambda: Size(), metadata={"description": "Entry size"}
    )
    stroke: Stroke = field(
        default_factory=lambda: Stroke(), metadata={"description": "Stroke definition"}
    )
    uuid: str = field(default="", metadata={"description": "Unique identifier"})


@dataclass
class GlobalLabel(KiCadObject):
    """Global label definition token.

    The 'global_label' token defines a label visible across all schematics in the format::

        (global_label
            "TEXT"
            (shape SHAPE)
            [(fields_autoplaced)]
            POSITION_IDENTIFIER
            TEXT_EFFECTS
            UNIQUE_IDENTIFIER
            PROPERTIES
        )

    Args:
        text: Global label text
        shape: Way the global label is drawn (optional)
        fields_autoplaced: Whether properties are placed automatically (optional)
        at: X and Y coordinates and rotation angle
        effects: How the global label text is drawn (optional)
        uuid: Universally unique identifier
        properties: Properties of the global label (optional)
    """

    __token_name__ = "global_label"

    text: str = field(default="", metadata={"description": "Global label text"})
    shape: Optional[str] = field(
        default=None,
        metadata={"description": "Way the global label is drawn", "required": False},
    )
    fields_autoplaced: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Whether properties are placed automatically",
            "required": False,
        },
    )
    at: At = field(
        default_factory=lambda: At(),
        metadata={"description": "X and Y coordinates and rotation angle"},
    )
    effects: Optional[Effects] = field(
        default=None,
        metadata={
            "description": "How the global label text is drawn",
            "required": False,
        },
    )
    uuid: str = field(
        default="", metadata={"description": "Universally unique identifier"}
    )
    properties: Optional[list[Property]] = field(
        default_factory=list,
        metadata={"description": "Properties of the global label", "required": False},
    )


@dataclass
class Junction(KiCadObject):
    """Junction definition token.

    The 'junction' token defines a junction in the schematic in the format::

        (junction
            POSITION_IDENTIFIER
            (diameter DIAMETER)
            (color R G B A)
            UNIQUE_IDENTIFIER
        )

    Args:
        at: X and Y coordinates of the junction
        diameter: Diameter of the junction (0 for default)
        color: Red, Green, Blue, and Alpha transparency (optional)
        uuid: Universally unique identifier
    """

    __token_name__ = "junction"

    at: At = field(default_factory=lambda: At(), metadata={"description": "Position"})
    diameter: float = field(
        default=0.0, metadata={"description": "Junction diameter (0 for default)"}
    )
    color: Optional[Color] = field(
        default=None, metadata={"description": "Junction color", "required": False}
    )
    uuid: str = field(default="", metadata={"description": "Unique identifier"})


@dataclass
class Label(KiCadObject):
    """Local label definition token.

    The 'label' token defines a local label in the format::

        (label
            "TEXT"
            (at X Y ANGLE)
            (fields_autoplaced)
            (effects EFFECTS)
            (uuid UUID)
        )

    Args:
        text: Label text
        at: Position and rotation
        fields_autoplaced: Whether fields are autoplaced (optional)
        effects: Text effects (optional)
        uuid: Unique identifier
    """

    __token_name__ = "label"

    text: str = field(default="", metadata={"description": "Label text"})
    at: At = field(
        default_factory=lambda: At(), metadata={"description": "Position and rotation"}
    )
    fields_autoplaced: Optional[bool] = field(
        default=None,
        metadata={"description": "Whether fields are autoplaced", "required": False},
    )
    effects: Optional[Effects] = field(
        default=None, metadata={"description": "Text effects", "required": False}
    )
    uuid: str = field(default="", metadata={"description": "Unique identifier"})


@dataclass
class NoConnect(KiCadObject):
    """No connect definition token.

    The 'no_connect' token defines a no-connect symbol in the format::

        (no_connect
            (at X Y)
            (uuid UUID)
        )

    Args:
        at: Position
        uuid: Unique identifier
    """

    __token_name__ = "no_connect"

    at: At = field(default_factory=lambda: At(), metadata={"description": "Position"})
    uuid: str = field(default="", metadata={"description": "Unique identifier"})


@dataclass
class Sheet(KiCadObject):
    """Hierarchical sheet definition token.

    The 'sheet' token defines a hierarchical sheet in the format::

        (sheet
            (at X Y)
            (size WIDTH HEIGHT)
            (fields_autoplaced)
            (stroke STROKE_DEFINITION)
            (fill FILL)
            (uuid UUID)
            (property "Sheetname" "NAME")
            (property "Sheetfile" "FILE")
            (pin "NAME" SHAPE (at X Y ANGLE) (effects EFFECTS) (uuid UUID))
            ...
        )

    Args:
        at: Position
        size: Sheet size
        fields_autoplaced: Whether fields are autoplaced (optional)
        stroke: Stroke definition (optional)
        fill: Fill definition (optional)
        uuid: Unique identifier
        properties: List of properties
        pins: List of sheet pins (optional)
    """

    __token_name__ = "sheet"

    at: At = field(default_factory=lambda: At(), metadata={"description": "Position"})
    size: Size = field(
        default_factory=lambda: Size(), metadata={"description": "Sheet size"}
    )
    fields_autoplaced: Optional[bool] = field(
        default=None,
        metadata={"description": "Whether fields are autoplaced", "required": False},
    )
    stroke: Optional[Stroke] = field(
        default=None, metadata={"description": "Stroke definition", "required": False}
    )
    fill: Optional[Fill] = field(
        default=None, metadata={"description": "Fill definition", "required": False}
    )
    uuid: str = field(default="", metadata={"description": "Unique identifier"})
    properties: list[Property] = field(
        default_factory=list, metadata={"description": "List of properties"}
    )
    pins: Optional[list[Pin]] = field(
        default_factory=list,
        metadata={"description": "List of sheet pins", "required": False},
    )


@dataclass
class Wire(KiCadObject):
    """Wire definition token.

    The 'wire' token defines wires in the schematic in the format::

        (wire
            COORDINATE_POINT_LIST
            STROKE_DEFINITION
            UNIQUE_IDENTIFIER
        )

    Args:
        pts: List of X and Y coordinates of start and end points
        stroke: How the wire is drawn
        uuid: Universally unique identifier
    """

    __token_name__ = "wire"

    pts: Pts = field(
        default_factory=lambda: Pts(),
        metadata={"description": "Wire connection points"},
    )
    stroke: Stroke = field(
        default_factory=lambda: Stroke(), metadata={"description": "Stroke definition"}
    )
    uuid: str = field(default="", metadata={"description": "Unique identifier"})


@dataclass
class Project(KiCadObject):
    """Project definition token for symbol instances.

    The 'project' token defines project information in the format::

        (project
            "PROJECT_NAME"
            (path "/PATH" (reference "REF") (unit N) (value "VALUE") (footprint "FOOTPRINT"))
        )

    Args:
        name: Project name
        instances: List of symbol instances
    """

    __token_name__ = "project"

    name: str = field(default="", metadata={"description": "Project name"})
    instances: list[Any] = field(
        default_factory=list, metadata={"description": "List of symbol instances"}
    )


@dataclass
class Incrx(KiCadObject):
    """Increment X definition token.

    The 'incrx' token defines X increment value in the format::

        (incrx VALUE)

    Args:
        value: X increment value
    """

    __token_name__ = "incrx"

    value: float = field(default=0.0, metadata={"description": "X increment value"})


@dataclass
class Incry(KiCadObject):
    """Increment Y definition token.

    The 'incry' token defines Y increment value in the format::

        (incry VALUE)

    Args:
        value: Y increment value
    """

    __token_name__ = "incry"

    value: float = field(default=0.0, metadata={"description": "Y increment value"})


@dataclass
class Length(KiCadObject):
    """Length definition token.

    The 'length' token defines a length value in the format::

        (length VALUE)

    Args:
        value: Length value
    """

    __token_name__ = "length"

    value: float = field(default=0.0, metadata={"description": "Length value"})


@dataclass
class Repeat(KiCadObject):
    """Repeat definition token.

    The 'repeat' token defines repeat settings in the format::

        (repeat VALUE)

    Args:
        value: Repeat value
    """

    __token_name__ = "repeat"

    value: int = field(default=1, metadata={"description": "Repeat value"})


@dataclass
class SheetInstance(KiCadObject):
    """Sheet instance definition token.

    The 'path' token defines a sheet instance in the format::

        (path "PATH_STRING"
            (page "PAGE_NUMBER")
        )

    Args:
        path: Hierarchical path string
        page: Page object
    """

    __token_name__ = "path"

    path: str = field(default="", metadata={"description": "Hierarchical path string"})
    page: Page = field(
        default_factory=lambda: Page(),
        metadata={"description": "Page object"},
    )


@dataclass
class SheetInstances(KiCadObject):
    """Sheet instances container definition token.

    The 'sheet_instances' token defines sheet instances in the format::

        (sheet_instances
            (path "PATH1" (page "PAGE1"))
            (path "PATH2" (page "PAGE2"))
            ...
        )

    Args:
        sheet_instances: List of sheet instances
    """

    __token_name__ = "sheet_instances"

    sheet_instances: list[SheetInstance] = field(
        default_factory=list,
        metadata={"description": "List of sheet instances"},
    )


@dataclass
class EmbeddedFonts(KiCadObject):
    """Embedded fonts definition token.

    The 'embedded_fonts' token defines whether fonts are embedded in the format::

        (embedded_fonts yes)
        (embedded_fonts no)

    Args:
        enabled: Whether embedded fonts are enabled
    """

    __token_name__ = "embedded_fonts"

    enabled: bool = field(
        default=False, metadata={"description": "Whether embedded fonts are enabled"}
    )


@dataclass
class KicadSch(KiCadObject):
    """KiCad schematic file definition.

    The 'kicad_sch' token defines a complete schematic file in the format::

        (kicad_sch
            (version VERSION)
            (generator GENERATOR)
            (uuid UNIQUE_IDENTIFIER)
            (lib_symbols ...)
            ;; schematic elements...
        )

    Args:
        version: File format version
        generator: Generator application name
        uuid: Universally unique identifier for the schematic
        lib_symbols: Symbol library container (optional)
        junctions: List of junctions (optional)
        no_connects: List of no connect markers (optional)
        bus_entries: List of bus entries (optional)
        wires: List of wires (optional)
        buses: List of buses (optional)
        labels: List of labels (optional)
        global_labels: List of global labels (optional)
        sheets: List of hierarchical sheets (optional)
        instances: List of symbol instances (optional)
    """

    __token_name__ = "kicad_sch"

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
    uuid: Uuid = field(
        default_factory=lambda: Uuid(),
        metadata={"description": "Universally unique identifier for the schematic"},
    )
    paper: Optional[Paper] = field(
        default=None,
        metadata={"description": "Paper settings", "required": False},
    )
    sheet_instances: Optional[SheetInstances] = field(
        default=None,
        metadata={"description": "Sheet instances", "required": False},
    )
    embedded_fonts: Optional[EmbeddedFonts] = field(
        default=None,
        metadata={"description": "Embedded fonts setting", "required": False},
    )
    lib_symbols: Optional[LibSymbols] = field(
        default=None,
        metadata={"description": "Symbol library container", "required": False},
    )
    junctions: Optional[list[Junction]] = field(
        default_factory=list,
        metadata={"description": "List of junctions", "required": False},
    )
    no_connects: Optional[list[NoConnect]] = field(
        default_factory=list,
        metadata={"description": "List of no connect markers", "required": False},
    )
    bus_entries: Optional[list[BusEntry]] = field(
        default_factory=list,
        metadata={"description": "List of bus entries", "required": False},
    )
    wires: Optional[list[Wire]] = field(
        default_factory=list,
        metadata={"description": "List of wires", "required": False},
    )
    buses: Optional[list[Bus]] = field(
        default_factory=list,
        metadata={"description": "List of buses", "required": False},
    )
    labels: Optional[list[Label]] = field(
        default_factory=list,
        metadata={"description": "List of labels", "required": False},
    )
    global_labels: Optional[list[GlobalLabel]] = field(
        default_factory=list,
        metadata={"description": "List of global labels", "required": False},
    )
    sheets: Optional[list[Sheet]] = field(
        default_factory=list,
        metadata={"description": "List of hierarchical sheets", "required": False},
    )
    instances: Optional[list[Any]] = field(
        default_factory=list,
        metadata={"description": "List of symbol instances", "required": False},
    )

    @classmethod
    def from_file(
        cls,
        file_path: str,
        strictness: ParseStrictness = ParseStrictness.STRICT,
        encoding: str = "utf-8",
    ) -> "KicadSch":
        """Parse from S-expression file - convenience method for schematic operations."""
        if not file_path.endswith(".kicad_sch"):
            raise ValueError("Unsupported file extension. Expected: .kicad_sch")
        with open(file_path, "r", encoding=encoding) as f:
            content = f.read()
        return cls.from_str(content, strictness)

    def save_to_file(self, file_path: str, encoding: str = "utf-8") -> None:
        """Save to .kicad_sch file format.

        Args:
            file_path: Path to write the .kicad_sch file
            encoding: File encoding (default: utf-8)
        """
        if not file_path.endswith(".kicad_sch"):
            raise ValueError("Unsupported file extension. Expected: .kicad_sch")
        content = self.to_sexpr_str(pretty_print=True)
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)
