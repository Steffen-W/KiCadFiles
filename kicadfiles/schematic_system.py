"""Schematic system elements for KiCad S-expressions - schematic drawing and connectivity."""

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
from .base_types import (
    At,
    AtXY,
    Color,
    Effects,
    Fill,
    Font,
    Justify,
    Property,
    Pts,
    Size,
    Stroke,
    Text,
    Uuid,
)
from .enums import LabelShape
from .primitive_graphics import Arc, Bezier, Circle, Line, Polygon, Polyline, Rectangle
from .symbol_library import LibSymbols
from .text_and_documents import (
    Image,
    Paper,
    TitleBlock,
)


@dataclass
class TableBorder(NamedObject):
    """Table border definition token.

    The 'border' token defines border configuration for tables in the format::
        (border (external yes) (header yes) (stroke (width WIDTH) (type TYPE)))

    Args:
        external: Whether external border is shown (optional)
        header: Whether header border is shown (optional)
        stroke: Stroke definition for border lines (optional)
    """

    __token_name__: ClassVar[str] = "border"

    external: TokenFlag = field(
        default_factory=lambda: TokenFlag("external"),
        metadata={"description": "Whether external border is shown", "required": False},
    )
    header: TokenFlag = field(
        default_factory=lambda: TokenFlag("header"),
        metadata={"description": "Whether header border is shown", "required": False},
    )
    stroke: Optional[Stroke] = field(
        default=None,
        metadata={
            "description": "Stroke definition for border lines",
            "required": False,
        },
    )


@dataclass
class TableSeparators(NamedObject):
    """Table separators definition token.

    The 'separators' token defines separator configuration for tables in the format::
        (separators (rows yes) (cols yes) (stroke (width WIDTH) (type TYPE)))

    Args:
        rows: Whether row separators are shown (optional)
        cols: Whether column separators are shown (optional)
        stroke: Stroke definition for separator lines (optional)
    """

    __token_name__: ClassVar[str] = "separators"

    rows: TokenFlag = field(
        default_factory=lambda: TokenFlag("rows"),
        metadata={"description": "Whether row separators are shown", "required": False},
    )
    cols: TokenFlag = field(
        default_factory=lambda: TokenFlag("cols"),
        metadata={
            "description": "Whether column separators are shown",
            "required": False,
        },
    )
    stroke: Optional[Stroke] = field(
        default=None,
        metadata={
            "description": "Stroke definition for separator lines",
            "required": False,
        },
    )


@dataclass
class TableMargins(NamedObject):
    """Table margins definition token.

    The 'margins' token defines cell margins in the format::
        (margins LEFT TOP RIGHT BOTTOM)

    Args:
        left: Left margin
        top: Top margin
        right: Right margin
        bottom: Bottom margin
    """

    __token_name__: ClassVar[str] = "margins"

    left: float = field(default=0.0, metadata={"description": "Left margin"})
    top: float = field(default=0.0, metadata={"description": "Top margin"})
    right: float = field(default=0.0, metadata={"description": "Right margin"})
    bottom: float = field(default=0.0, metadata={"description": "Bottom margin"})


@dataclass
class TableSpan(NamedObject):
    """Table span definition token.

    The 'span' token defines cell span in the format::
        (span COLS ROWS)

    Args:
        cols: Number of columns to span
        rows: Number of rows to span
    """

    __token_name__: ClassVar[str] = "span"

    cols: int = field(default=1, metadata={"description": "Number of columns to span"})
    rows: int = field(default=1, metadata={"description": "Number of rows to span"})


@dataclass
class TableCell(NamedObject):
    """Table cell definition token.

    The 'table_cell' token defines individual table cells in the format::
        (table_cell "TEXT"
            (exclude_from_sim BOOLEAN)
            (at X Y ANGLE)
            (size WIDTH HEIGHT)
            (margins LEFT TOP RIGHT BOTTOM)
            (span COLS ROWS)
            (fill FILL_DEF)
            (effects EFFECTS_DEF)
            (uuid UUID)
        )

    Args:
        text: Cell text content
        exclude_from_sim: Whether to exclude from simulation (optional)
        at: Position and rotation (optional)
        size: Cell size (optional)
        margins: Cell margins (optional)
        span: Cell span (optional)
        fill: Fill definition (optional)
        effects: Text effects (optional)
        uuid: Unique identifier (optional)
    """

    __token_name__: ClassVar[str] = "table_cell"

    text: str = field(default="", metadata={"description": "Cell text content"})
    exclude_from_sim: TokenFlag = field(
        default_factory=lambda: TokenFlag("exclude_from_sim"),
        metadata={
            "description": "Whether to exclude from simulation",
            "required": False,
        },
    )
    at: Optional[At] = field(
        default=None,
        metadata={"description": "Position and rotation", "required": False},
    )
    size: Optional[Size] = field(
        default=None,
        metadata={"description": "Cell size", "required": False},
    )
    margins: Optional[TableMargins] = field(
        default=None,
        metadata={"description": "Cell margins", "required": False},
    )
    span: Optional[TableSpan] = field(
        default=None,
        metadata={"description": "Cell span", "required": False},
    )
    fill: Optional[Fill] = field(
        default=None,
        metadata={"description": "Fill definition", "required": False},
    )
    effects: Optional[Effects] = field(
        default=None,
        metadata={"description": "Text effects", "required": False},
    )
    uuid: Optional[Uuid] = field(
        default=None,
        metadata={"description": "Unique identifier", "required": False},
    )


@dataclass
class RowHeights(NamedObject):
    """Row heights definition token.

    The 'row_heights' token defines row height values in the format::
        (row_heights HEIGHT1 HEIGHT2 ...)

    Args:
        heights: List of row height values
    """

    __token_name__: ClassVar[str] = "row_heights"

    heights: List[float] = field(
        default_factory=list,
        metadata={"description": "List of row height values"},
    )


@dataclass
class ColumnWidths(NamedObject):
    """Column widths definition token.

    The 'column_widths' token defines column width values in the format::
        (column_widths WIDTH1 WIDTH2 ...)

    Args:
        widths: List of column width values
    """

    __token_name__: ClassVar[str] = "column_widths"

    widths: List[float] = field(
        default_factory=list,
        metadata={"description": "List of column width values"},
    )


@dataclass
class Cells(NamedObject):
    """Table cells container token.

    The 'cells' token contains a list of table_cell objects in the format::
        (cells
            (table_cell ...)
            (table_cell ...)
            ...
        )

    Args:
        cells: List of table cell objects
    """

    __token_name__: ClassVar[str] = "cells"

    cells: List[TableCell] = field(
        default_factory=list,
        metadata={"description": "List of table cell objects"},
    )


@dataclass
class Table(NamedObject):
    """Table definition token for schematics.

    The 'table' token defines tables in schematics.
    This is a basic implementation for parsing support.

    Args:
        column_count: Number of columns (optional)
        border: Border configuration (optional)
        separators: Separator configuration (optional)
        column_widths: Column width values (optional)
        row_heights: Row height values (optional)
        cells: Table cells (optional)
    """

    __token_name__: ClassVar[str] = "table"

    column_count: Optional[int] = field(
        default=None,
        metadata={"description": "Number of columns", "required": False},
    )
    border: Optional[TableBorder] = field(
        default=None,
        metadata={"description": "Border configuration", "required": False},
    )
    separators: Optional[TableSeparators] = field(
        default=None,
        metadata={"description": "Separator configuration", "required": False},
    )
    column_widths: Optional[ColumnWidths] = field(
        default=None,
        metadata={"description": "Column width values", "required": False},
    )
    row_heights: Optional[RowHeights] = field(
        default=None,
        metadata={"description": "Row height values", "required": False},
    )
    cells: Optional[Cells] = field(
        default=None,
        metadata={"description": "Table cells", "required": False},
    )


@dataclass
class HierarchicalLabel(NamedObject):
    """Hierarchical label definition token.

    The 'hierarchical_label' token defines hierarchical labels in schematics.

    Args:
        text: Label text
        shape: Label shape (optional)
        at: Position (optional)
        effects: Text effects (optional)
        uuid: Unique identifier (optional)
    """

    __token_name__: ClassVar[str] = "hierarchical_label"

    text: str = field(default="", metadata={"description": "Label text"})
    shape: Optional[LabelShape] = field(
        default=None, metadata={"description": "Label shape", "required": False}
    )
    at: Optional[At] = field(
        default=None, metadata={"description": "Position", "required": False}
    )
    effects: Optional[Effects] = field(
        default=None, metadata={"description": "Text effects", "required": False}
    )
    uuid: Optional[Uuid] = field(
        default=None, metadata={"description": "Unique identifier", "required": False}
    )


@dataclass
class RuleArea(NamedObject):
    """Rule area definition token.

    The 'rule_area' token defines rule areas in schematics.

    Args:
        polylines: Polylines defining area (optional)
    """

    __token_name__: ClassVar[str] = "rule_area"

    polylines: Optional[List[Polyline]] = field(
        default_factory=list,
        metadata={"description": "Polylines defining area", "required": False},
    )


@dataclass
class NetclassFlag(NamedObject):
    """Netclass flag definition token.

    The 'netclass_flag' token defines netclass flags in schematics.

    Args:
        name: Netclass name
        length: Flag length (optional)
        shape: Flag shape (optional)
        at: Position (optional)
        fields_autoplaced: Whether fields are auto-placed (optional)
        effects: Text effects (optional)
        uuid: Unique identifier (optional)
        properties: Properties of the netclass flag (optional)
    """

    __token_name__: ClassVar[str] = "netclass_flag"

    name: str = field(default="", metadata={"description": "Netclass name"})
    length: Optional[float] = field(
        default=None, metadata={"description": "Flag length", "required": False}
    )
    shape: Optional[str] = field(
        default=None, metadata={"description": "Flag shape", "required": False}
    )
    at: Optional[At] = field(
        default=None, metadata={"description": "Position", "required": False}
    )
    fields_autoplaced: TokenFlag = field(
        default_factory=lambda: TokenFlag("fields_autoplaced"),
        metadata={"description": "Whether fields are auto-placed", "required": False},
    )
    effects: Optional[Effects] = field(
        default=None, metadata={"description": "Text effects", "required": False}
    )
    uuid: Optional[Uuid] = field(
        default=None, metadata={"description": "Unique identifier", "required": False}
    )
    properties: Optional[List[Property]] = field(
        default_factory=list,
        metadata={"description": "Properties of the netclass flag", "required": False},
    )


@dataclass
class Bus(NamedObject):
    """Bus definition token.

    The 'bus' token defines buses in the schematic in the format::

        (bus
            COORDINATE_POINT_LIST
            STROKE_DEFINITION
            UNIQUE_IDENTIFIER
        )

    Args:
        pts: Bus connection points
        stroke: Stroke definition
        uuid: Unique identifier
    """

    __token_name__: ClassVar[str] = "bus"

    pts: Pts = field(
        default_factory=lambda: Pts(), metadata={"description": "Bus connection points"}
    )
    stroke: Stroke = field(
        default_factory=lambda: Stroke(), metadata={"description": "Stroke definition"}
    )
    uuid: Uuid = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )


@dataclass
class BusEntry(NamedObject):
    """Bus entry definition token.

    The 'bus_entry' token defines a bus entry in the schematic in the format::

        (bus_entry
            POSITION_IDENTIFIER
            (size X Y)
            STROKE_DEFINITION
            UNIQUE_IDENTIFIER
        )

    Args:
        at: Position
        size: Entry size
        stroke: Stroke definition
        uuid: Unique identifier
    """

    __token_name__: ClassVar[str] = "bus_entry"

    at: AtXY = field(
        default_factory=lambda: AtXY(), metadata={"description": "Position"}
    )
    size: Size = field(
        default_factory=lambda: Size(), metadata={"description": "Entry size"}
    )
    stroke: Stroke = field(
        default_factory=lambda: Stroke(), metadata={"description": "Stroke definition"}
    )
    uuid: Uuid = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )


@dataclass
class GlobalLabel(NamedObject):
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

    __token_name__: ClassVar[str] = "global_label"

    text: str = field(default="", metadata={"description": "Global label text"})
    shape: NamedString = field(
        default_factory=lambda: NamedString("shape", "bidirectional"),
        metadata={"description": "Way the global label is drawn", "required": False},
    )
    fields_autoplaced: TokenFlag = field(
        default_factory=lambda: TokenFlag("fields_autoplaced"),
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
        default_factory=lambda: Effects(font=Font(), justify=Justify()),
        metadata={
            "description": "How the global label text is drawn",
            "required": False,
        },
    )
    uuid: Uuid = field(
        default_factory=lambda: Uuid(),
        metadata={"description": "Universally unique identifier"},
    )
    properties: Optional[List[Property]] = field(
        default_factory=lambda: [
            Property(
                key="Intersheetrefs",
                value="${INTERSHEET_REFS}",
                effects=Effects(font=Font(), hide=TokenFlag("hide")),
            )
        ],
        metadata={"description": "Properties of the global label", "required": False},
    )


@dataclass
class Junction(NamedObject):
    """Junction definition token.

    The 'junction' token defines a junction in the schematic in the format::

        (junction
            POSITION_IDENTIFIER
            (diameter DIAMETER)
            (color R G B A)
            UNIQUE_IDENTIFIER
        )

    Args:
        at: Position
        diameter: Junction diameter
        color: Junction color (optional)
        uuid: Unique identifier
    """

    __token_name__: ClassVar[str] = "junction"

    at: AtXY = field(
        default_factory=lambda: AtXY(), metadata={"description": "Position"}
    )
    diameter: NamedFloat = field(
        default_factory=lambda: NamedFloat("diameter", 0.0),
        metadata={"description": "Junction diameter"},
    )
    color: Optional[Color] = field(
        default=None, metadata={"description": "Junction color", "required": False}
    )
    uuid: Uuid = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )


@dataclass
class Label(NamedObject):
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

    __token_name__: ClassVar[str] = "label"

    text: str = field(default="", metadata={"description": "Label text"})
    at: At = field(
        default_factory=lambda: At(), metadata={"description": "Position and rotation"}
    )
    fields_autoplaced: TokenFlag = field(
        default_factory=lambda: TokenFlag("fields_autoplaced"),
        metadata={"description": "Whether fields are autoplaced", "required": False},
    )
    effects: Optional[Effects] = field(
        default=None, metadata={"description": "Text effects", "required": False}
    )
    uuid: Uuid = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )


@dataclass
class NoConnect(NamedObject):
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

    __token_name__: ClassVar[str] = "no_connect"

    at: AtXY = field(
        default_factory=lambda: AtXY(), metadata={"description": "Position"}
    )
    uuid: Uuid = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )


@dataclass
class Path(NamedObject):
    """Path definition token.

    The 'path' token defines a hierarchical path in the format::
        (path "PATH"
            (reference "REF")
            (unit NUMBER)
        )

    Args:
        value: Path value
        reference: Component reference (optional)
        unit: Unit number (optional)
        page: Page number (optional)
    """

    __token_name__: ClassVar[str] = "path"

    value: str = field(default="", metadata={"description": "Path value"})
    reference: NamedString = field(
        default_factory=lambda: NamedString("reference", ""),
        metadata={"description": "Component reference", "required": False},
    )
    unit: NamedInt = field(
        default_factory=lambda: NamedInt("unit", 0),
        metadata={"description": "Unit number", "required": False},
    )
    page: NamedString = field(
        default_factory=lambda: NamedString("page", ""),
        metadata={"description": "Page number", "required": False},
    )


@dataclass
class Project(NamedObject):
    """Project definition token.

    The 'project' token defines a project instance in the format::
        (project "PROJECT_NAME"
            (path "PATH"
                (reference "REF")
                (unit NUMBER)
            )
        )

    Args:
        name: Project name
        path: Hierarchical path (optional)
    """

    __token_name__: ClassVar[str] = "project"

    name: str = field(default="", metadata={"description": "Project name"})
    path: Optional[Path] = field(
        default=None,
        metadata={"description": "Hierarchical path", "required": False},
    )


@dataclass
class SheetPin(NamedObject):
    """Sheet pin definition token.

    The 'pin' token defines a hierarchical sheet pin in the format::

        (pin "NAME" SHAPE (at X Y ANGLE) (effects EFFECTS) (uuid UUID))

    Args:
        name: Pin name string
        shape: Pin shape/direction
        at: Position and angle
        effects: Text effects (optional)
        uuid: Unique identifier
    """

    __token_name__: ClassVar[str] = "pin"

    name: str = field(default="", metadata={"description": "Pin name string"})
    shape: LabelShape = field(
        default=LabelShape.INPUT, metadata={"description": "Pin shape/direction"}
    )
    at: At = field(
        default_factory=lambda: At(), metadata={"description": "Position and angle"}
    )
    effects: Optional[Effects] = field(
        default=None, metadata={"description": "Text effects", "required": False}
    )
    uuid: Uuid = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )


@dataclass
class SheetLocalInstances(NamedObject):
    """Sheet local instances definition token.

    The 'instances' token defines local sheet instances in the format::

        (instances
            (project "PROJECT_NAME"
                (path "/PATH" (page "PAGE"))
            )
        )

    Args:
        project: List of project data
    """

    __token_name__: ClassVar[str] = "instances"

    project: List[Project] = field(
        default_factory=list, metadata={"description": "List of project data"}
    )


@dataclass
class Sheet(NamedObject):
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
        exclude_from_sim: Whether sheet is excluded from simulation (optional)
        in_bom: Whether sheet appears in BOM (optional)
        on_board: Whether sheet is exported to PCB (optional)
        dnp: Do not populate flag (optional)
        rectangles: List of rectangle graphical items (optional)
        instances: Sheet local instances (optional)
    """

    __token_name__: ClassVar[str] = "sheet"

    at: AtXY = field(
        default_factory=lambda: AtXY(), metadata={"description": "Position"}
    )
    size: Size = field(
        default_factory=lambda: Size(), metadata={"description": "Sheet size"}
    )
    fields_autoplaced: TokenFlag = field(
        default_factory=lambda: TokenFlag("fields_autoplaced"),
        metadata={"description": "Whether fields are autoplaced", "required": False},
    )
    stroke: Optional[Stroke] = field(
        default=None, metadata={"description": "Stroke definition", "required": False}
    )
    fill: Optional[Fill] = field(
        default=None, metadata={"description": "Fill definition", "required": False}
    )
    uuid: Uuid = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )
    properties: List[Property] = field(
        default_factory=list, metadata={"description": "List of properties"}
    )
    pins: Optional[List[SheetPin]] = field(
        default_factory=list,
        metadata={"description": "List of sheet pins", "required": False},
    )
    exclude_from_sim: TokenFlag = field(
        default_factory=lambda: TokenFlag("exclude_from_sim"),
        metadata={
            "description": "Whether sheet is excluded from simulation",
            "required": False,
        },
    )
    in_bom: TokenFlag = field(
        default_factory=lambda: TokenFlag("in_bom"),
        metadata={"description": "Whether sheet appears in BOM", "required": False},
    )
    on_board: TokenFlag = field(
        default_factory=lambda: TokenFlag("on_board"),
        metadata={"description": "Whether sheet is exported to PCB", "required": False},
    )
    dnp: TokenFlag = field(
        default_factory=lambda: TokenFlag("dnp"),
        metadata={"description": "Do not populate flag", "required": False},
    )
    rectangles: Optional[List[Rectangle]] = field(
        default_factory=list,
        metadata={
            "description": "List of rectangle graphical items",
            "required": False,
        },
    )
    instances: Optional[SheetLocalInstances] = field(
        default=None,
        metadata={"description": "Sheet local instances", "required": False},
    )


@dataclass
class Wire(NamedObject):
    """Wire definition token.

    The 'wire' token defines wires in the schematic in the format::

        (wire
            COORDINATE_POINT_LIST
            STROKE_DEFINITION
            UNIQUE_IDENTIFIER
        )

    Args:
        pts: Wire connection points
        stroke: Stroke definition
        uuid: Unique identifier
    """

    __token_name__: ClassVar[str] = "wire"

    pts: Pts = field(
        default_factory=lambda: Pts(),
        metadata={"description": "Wire connection points"},
    )
    stroke: Stroke = field(
        default_factory=lambda: Stroke(), metadata={"description": "Stroke definition"}
    )
    uuid: Uuid = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )


@dataclass
class SheetInstance(NamedObject):
    """Sheet instance definition token.

    The 'path' token defines a sheet instance in the format::

        (path "PATH_STRING"
            (page "PAGE_NUMBER")
        )

    Args:
        path: Hierarchical path string
        page: Page object
    """

    __token_name__: ClassVar[str] = "path"

    path: str = field(default="", metadata={"description": "Hierarchical path string"})
    page: NamedString = field(
        default_factory=lambda: NamedString("page", ""),
        metadata={"description": "Page object"},
    )


@dataclass
class SheetInstances(NamedObject):
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

    __token_name__: ClassVar[str] = "sheet_instances"

    sheet_instances: List[SheetInstance] = field(
        default_factory=list,
        metadata={"description": "List of sheet instances"},
    )


@dataclass
class PinRef(NamedObject):
    """Pin reference definition token for schematic symbols.

    The 'pin' token in schematic symbols references a pin by number in the format::
        (pin "NUMBER"
            (uuid UUID)
        )

    Args:
        number: Pin number
        uuid: Unique identifier (optional)
    """

    __token_name__: ClassVar[str] = "pin"

    number: str = field(default="", metadata={"description": "Pin number"})
    uuid: Optional[Uuid] = field(
        default=None,
        metadata={"description": "Unique identifier", "required": False},
    )


@dataclass
class SymbolInstances(NamedObject):
    """Symbol instances definition token.

    The 'instances' token defines symbol instance data in the format::
        (instances
            (project "PROJECT_NAME"
                (path "PATH"
                    (reference "REF")
                    (unit NUMBER)
                )
            )
        )

    Args:
        projects: List of project instances
    """

    __token_name__: ClassVar[str] = "instances"

    projects: List[Project] = field(
        default_factory=list,
        metadata={"description": "List of project instances"},
    )


@dataclass
class SchematicSymbol(NamedObject):
    """Schematic symbol instance definition token.

    References a symbol definition via lib_id and adds instance-specific properties.

    The 'symbol' token in schematics defines symbol instances in the format::
        (symbol
            (lib_id "LIBRARY:SYMBOL")
            (at X Y ANGLE)
            (unit NUMBER)
            (exclude_from_sim BOOLEAN)
            (in_bom BOOLEAN)
            (on_board BOOLEAN)
            (dnp BOOLEAN)
            (fields_autoplaced BOOLEAN)
            (uuid UUID)
            PROPERTIES...
            PINS...
            (instances ...)
        )

    Args:
        lib_name: Library name (optional)
        lib_id: Library identifier referencing symbol definition (optional)
        at: Position and rotation (optional)
        mirror: Mirror transformation (optional)
        unit: Unit number (optional)
        exclude_from_sim: Whether to exclude from simulation (optional)
        in_bom: Whether to include in BOM (optional)
        on_board: Whether to place on board (optional)
        dnp: Do not populate flag (optional)
        fields_autoplaced: Whether fields are auto-placed (optional)
        uuid: Unique identifier (optional)
        properties: List of properties (optional)
        pins: List of pin references (optional)
        text: List of text elements (optional)
        instances: Symbol instances (optional)
    """

    __token_name__: ClassVar[str] = "symbol"

    lib_name: Optional[str] = field(
        default=None,
        metadata={"description": "Library name", "required": False},
    )
    lib_id: NamedString = field(
        default_factory=lambda: NamedString("lib_id", ""),
        metadata={
            "description": "Library identifier referencing symbol definition",
            "required": False,
        },
    )
    at: Optional[At] = field(
        default=None,
        metadata={"description": "Position and rotation", "required": False},
    )
    mirror: NamedString = field(
        default_factory=lambda: NamedString("mirror", "x"),
        metadata={"description": "Mirror transformation", "required": False},
    )
    unit: NamedInt = field(
        default_factory=lambda: NamedInt("unit", 0),
        metadata={"description": "Unit number", "required": False},
    )
    exclude_from_sim: TokenFlag = field(
        default_factory=lambda: TokenFlag("exclude_from_sim"),
        metadata={
            "description": "Whether to exclude from simulation",
            "required": False,
        },
    )
    in_bom: TokenFlag = field(
        default_factory=lambda: TokenFlag("in_bom"),
        metadata={"description": "Whether to include in BOM", "required": False},
    )
    on_board: TokenFlag = field(
        default_factory=lambda: TokenFlag("on_board"),
        metadata={"description": "Whether to place on board", "required": False},
    )
    dnp: TokenFlag = field(
        default_factory=lambda: TokenFlag("dnp"),
        metadata={"description": "Do not populate flag", "required": False},
    )
    fields_autoplaced: TokenFlag = field(
        default_factory=lambda: TokenFlag("fields_autoplaced"),
        metadata={"description": "Whether fields are auto-placed", "required": False},
    )
    uuid: Optional[Uuid] = field(
        default=None,
        metadata={"description": "Unique identifier", "required": False},
    )
    properties: Optional[List[Property]] = field(
        default_factory=list,
        metadata={"description": "List of properties", "required": False},
    )
    pins: Optional[List[PinRef]] = field(
        default_factory=list,
        metadata={"description": "List of pin references", "required": False},
    )
    text: Optional[List[Text]] = field(
        default_factory=list,
        metadata={"description": "List of text elements", "required": False},
    )
    instances: Optional[SymbolInstances] = field(
        default=None,
        metadata={"description": "Symbol instances", "required": False},
    )


@dataclass
class KicadSch(NamedObject):
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
        generator_version: Generator version (optional)
        uuid: Universally unique identifier for the schematic
        paper: Paper settings (optional)
        title_block: Title block (optional)
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
        graphic_items: List of graphical items (optional)
        tables: List of tables (optional)
        hierarchical_labels: List of hierarchical labels (optional)
        rule_areas: List of rule areas (optional)
        netclass_flags: List of netclass flags (optional)
        symbols: List of symbol instances (optional)
        text: List of text elements (optional)
        images: List of image elements (optional)
        sheet_instances: Sheet instances (optional)
        embedded_fonts: Embedded fonts setting (optional)
    """

    __token_name__: ClassVar[str] = "kicad_sch"

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
    uuid: Uuid = field(
        default_factory=lambda: Uuid(),
        metadata={"description": "Universally unique identifier for the schematic"},
    )
    paper: Optional[Paper] = field(
        default=None,
        metadata={"description": "Paper settings", "required": False},
    )
    title_block: Optional[TitleBlock] = field(
        default=None,
        metadata={"description": "Title block", "required": False},
    )
    lib_symbols: Optional[LibSymbols] = field(
        default=None,
        metadata={"description": "Symbol library container", "required": False},
    )
    junctions: Optional[List[Junction]] = field(
        default_factory=list,
        metadata={"description": "List of junctions", "required": False},
    )
    no_connects: Optional[List[NoConnect]] = field(
        default_factory=list,
        metadata={"description": "List of no connect markers", "required": False},
    )
    bus_entries: Optional[List[BusEntry]] = field(
        default_factory=list,
        metadata={"description": "List of bus entries", "required": False},
    )
    wires: Optional[List[Wire]] = field(
        default_factory=list,
        metadata={"description": "List of wires", "required": False},
    )
    buses: Optional[List[Bus]] = field(
        default_factory=list,
        metadata={"description": "List of buses", "required": False},
    )
    labels: Optional[List[Label]] = field(
        default_factory=list,
        metadata={"description": "List of labels", "required": False},
    )
    global_labels: Optional[List[GlobalLabel]] = field(
        default_factory=list,
        metadata={"description": "List of global labels", "required": False},
    )
    sheets: Optional[List[Sheet]] = field(
        default_factory=list,
        metadata={"description": "List of hierarchical sheets", "required": False},
    )
    instances: Optional[List[Any]] = field(
        default_factory=list,
        metadata={"description": "List of symbol instances", "required": False},
    )
    graphic_items: Optional[
        List[Union[Arc, Bezier, Circle, Line, Polygon, Polyline, Rectangle]]
    ] = field(
        default_factory=list,
        metadata={"description": "List of graphical items", "required": False},
    )
    tables: Optional[List[Table]] = field(
        default_factory=list,
        metadata={"description": "List of tables", "required": False},
    )
    hierarchical_labels: Optional[List[HierarchicalLabel]] = field(
        default_factory=list,
        metadata={"description": "List of hierarchical labels", "required": False},
    )
    rule_areas: Optional[List[RuleArea]] = field(
        default_factory=list,
        metadata={"description": "List of rule areas", "required": False},
    )
    netclass_flags: Optional[List[NetclassFlag]] = field(
        default_factory=list,
        metadata={"description": "List of netclass flags", "required": False},
    )
    symbols: Optional[List[SchematicSymbol]] = field(
        default_factory=list,
        metadata={"description": "List of symbol instances", "required": False},
    )
    text: Optional[List[Text]] = field(
        default_factory=list,
        metadata={"description": "List of text elements", "required": False},
    )
    images: Optional[List[Image]] = field(
        default_factory=list,
        metadata={"description": "List of image elements", "required": False},
    )
    sheet_instances: Optional[SheetInstances] = field(
        default=None,
        metadata={"description": "Sheet instances", "required": False},
    )
    embedded_fonts: TokenFlag = field(
        default_factory=lambda: TokenFlag("embedded_fonts", token_value="yes"),
        metadata={"description": "Embedded fonts setting", "required": False},
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
        content = self.to_sexpr_str()
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)
