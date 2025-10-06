"""Advanced graphics elements for KiCad S-expressions - complex graphical objects."""

from dataclasses import dataclass, field
from typing import ClassVar, Optional

from .base_element import NamedFloat, NamedInt, NamedObject, NamedString, TokenFlag
from .base_types import (
    At,
    Center,
    Effects,
    End,
    Layer,
    Mid,
    Pts,
    Start,
    Stroke,
    Type,
    Uuid,
)


@dataclass
class GrArc(NamedObject):
    """Graphical arc definition token.

    The 'gr_arc' token defines an arc graphic object in the format::

        (gr_arc
            (start X Y)
            (mid X Y)
            (end X Y)
            (layer LAYER_DEFINITION)
            (width WIDTH)
            (uuid UUID)
        )

    Args:
        start: Start point coordinates
        mid: Mid point coordinates
        end: End point coordinates
        stroke: Stroke definition (optional)
        layer: Layer definition (optional)
        width: Line width (deprecated, use stroke) (optional)
        uuid: Unique identifier
    """

    __token_name__: ClassVar[str] = "gr_arc"

    start: Start = field(
        default_factory=lambda: Start(),
        metadata={"description": "Start point coordinates"},
    )
    mid: Mid = field(
        default_factory=lambda: Mid(), metadata={"description": "Mid point coordinates"}
    )
    end: End = field(
        default_factory=lambda: End(), metadata={"description": "End point coordinates"}
    )
    stroke: Optional[Stroke] = field(
        default=None, metadata={"description": "Stroke definition", "required": False}
    )
    layer: Optional[Layer] = field(
        default=None, metadata={"description": "Layer definition", "required": False}
    )
    width: NamedFloat = field(
        default_factory=lambda: NamedFloat("width", 0.0),
        metadata={
            "description": "Line width (deprecated, use stroke)",
            "required": False,
        },
    )
    uuid: Uuid = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )


@dataclass
class GrBbox(NamedObject):
    """Graphical bounding box definition token.

    The 'gr_bbox' token defines a bounding box inside which annotations will be shown in the format::

        (gr_bbox
            (start X Y)
            (end X Y)
        )

    Args:
        start: Coordinates of the upper left corner
        end: Coordinates of the lower right corner
    """

    __token_name__: ClassVar[str] = "gr_bbox"

    start: Start = field(
        default_factory=lambda: Start(),
        metadata={"description": "Coordinates of the upper left corner"},
    )
    end: End = field(
        default_factory=lambda: End(),
        metadata={"description": "Coordinates of the lower right corner"},
    )


@dataclass
class GrCircle(NamedObject):
    """Graphical circle definition token.

    The 'gr_circle' token defines a circle graphic object in the format::

        (gr_circle
            (center X Y)
            (end X Y)
            (layer LAYER_DEFINITION)
            (width WIDTH)
            [(fill yes | no)]
            (uuid UUID)
        )

    Args:
        center: Center point coordinates
        end: End point defining radius
        layer: Layer definition
        width: Line width
        fill: Fill definition (optional)
        uuid: Unique identifier
    """

    __token_name__: ClassVar[str] = "gr_circle"

    center: Center = field(
        default_factory=lambda: Center(),
        metadata={"description": "Center point coordinates"},
    )
    end: End = field(
        default_factory=lambda: End(),
        metadata={"description": "End point defining radius"},
    )
    layer: Layer = field(
        default_factory=lambda: Layer(), metadata={"description": "Layer definition"}
    )
    width: NamedFloat = field(
        default_factory=lambda: NamedFloat("width", 0.0),
        metadata={"description": "Line width"},
    )
    fill: TokenFlag = field(
        default_factory=lambda: TokenFlag("fill"),
        metadata={"description": "Fill definition", "required": False},
    )
    uuid: Uuid = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )


@dataclass
class GrText(NamedObject):
    """Graphical text definition token.

    The 'gr_text' token defines text graphic objects in the format::

        (gr_text
            "TEXT"
            POSITION_IDENTIFIER
            (layer LAYER_DEFINITION [knockout])
            (uuid UUID)
            (effects TEXT_EFFECTS)
        )

    Args:
        text: Text content
        at: Position and rotation coordinates
        layer: Layer definition
        uuid: Unique identifier
        effects: Text effects
    """

    __token_name__: ClassVar[str] = "gr_text"

    text: str = field(default="", metadata={"description": "Text content"})
    at: At = field(
        default_factory=lambda: At(),
        metadata={"description": "Position and rotation coordinates"},
    )
    layer: Layer = field(
        default_factory=lambda: Layer(), metadata={"description": "Layer definition"}
    )
    uuid: Uuid = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )
    effects: Effects = field(
        default_factory=lambda: Effects(), metadata={"description": "Text effects"}
    )


@dataclass
class GrTextBox(NamedObject):
    """Graphical text box definition token.

    The 'gr_text_box' token defines a rectangle containing line-wrapped text in the format::

        (gr_text_box
            [locked]
            "TEXT"
            [(start X Y)]
            [(end X Y)]
            [(pts (xy X Y) (xy X Y) (xy X Y) (xy X Y))]
            [(angle ROTATION)]
            (layer LAYER_DEFINITION)
            (uuid UUID)
            TEXT_EFFECTS
            [STROKE_DEFINITION]
            [(render_cache RENDER_CACHE)]
        )

    Args:
        locked: Whether the text box can be moved (optional)
        text: Content of the text box
        start: Top-left corner of cardinally oriented text box (optional)
        end: Bottom-right corner of cardinally oriented text box (optional)
        pts: Four corners of non-cardinally oriented text box (optional)
        angle: Rotation of the text box in degrees (optional)
        layer: Layer definition
        uuid: Unique identifier
        effects: Text effects
        stroke: Stroke definition for optional border (optional)
        render_cache: Text rendering cache for TrueType fonts (optional)
    """

    __token_name__: ClassVar[str] = "gr_text_box"

    locked: TokenFlag = field(
        default_factory=lambda: TokenFlag("locked"),
        metadata={
            "description": "Whether the text box can be moved",
            "required": False,
        },
    )
    text: str = field(default="", metadata={"description": "Content of the text box"})
    start: Optional[Start] = field(
        default=None,
        metadata={
            "description": "Top-left corner of cardinally oriented text box",
            "required": False,
        },
    )
    end: Optional[End] = field(
        default=None,
        metadata={
            "description": "Bottom-right corner of cardinally oriented text box",
            "required": False,
        },
    )
    pts: Optional[Pts] = field(
        default=None,
        metadata={
            "description": "Four corners of non-cardinally oriented text box",
            "required": False,
        },
    )
    angle: NamedFloat = field(
        default_factory=lambda: NamedFloat("angle", 0.0),
        metadata={
            "description": "Rotation of the text box in degrees",
            "required": False,
        },
    )
    layer: Layer = field(
        default_factory=lambda: Layer(), metadata={"description": "Layer definition"}
    )
    uuid: Uuid = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )
    effects: Effects = field(
        default_factory=lambda: Effects(), metadata={"description": "Text effects"}
    )
    stroke: Optional[Stroke] = field(
        default=None,
        metadata={
            "description": "Stroke definition for optional border",
            "required": False,
        },
    )
    render_cache: NamedString = field(
        default_factory=lambda: NamedString("render_cache", ""),
        metadata={
            "description": "Text rendering cache for TrueType fonts",
            "required": False,
        },
    )


@dataclass
class FpTextAt(NamedObject):
    """Position identifier token for FpText that supports flexible coordinate formats.

    The 'at' token for fp_text defines positional coordinates in the format:
        (at X [Y] [ANGLE])

    Special case: Sometimes only one coordinate is provided like (at 0).

    Args:
        x: Horizontal position of the text
        y: Vertical position of the text (optional)
        angle: Rotation angle of the text (optional)
    """

    __token_name__: ClassVar[str] = "at"

    x: float = field(
        default=0.0,
        metadata={"description": "Horizontal position of the text"},
    )
    y: Optional[float] = field(
        default=None,
        metadata={"description": "Vertical position of the text", "required": False},
    )
    angle: Optional[float] = field(
        default=None,
        metadata={"description": "Rotation angle of the text", "required": False},
    )


@dataclass
class Format(NamedObject):
    """Dimension format definition token.

    The 'format' token defines formatting for dimension text in the format::

        (format
            [(prefix "PREFIX")]
            [(suffix "SUFFIX")]
            (units UNITS)
            (units_format UNITS_FORMAT)
            (precision PRECISION)
            [(override_value "VALUE")]
            [(suppress_zeros yes | no)]
        )

    Args:
        prefix: Text prefix (optional)
        suffix: Text suffix (optional)
        units: Units type (0=inches, 1=mils, 2=mm, 3=auto)
        units_format: Units format (0=no suffix, 1=bare, 2=parenthesis)
        precision: Precision digits
        override_value: Override text value (optional)
        suppress_zeros: Whether to suppress trailing zeros (optional)
    """

    __token_name__: ClassVar[str] = "format"

    prefix: NamedString = field(
        default_factory=lambda: NamedString("prefix", ""),
        metadata={"description": "Text prefix", "required": False},
    )
    suffix: NamedString = field(
        default_factory=lambda: NamedString("suffix", ""),
        metadata={"description": "Text suffix", "required": False},
    )
    units: NamedString = field(
        default_factory=lambda: NamedString("units", "mm"),
        metadata={"description": "Units type (0=inches, 1=mils, 2=mm, 3=auto)"},
    )
    units_format: NamedInt = field(
        default_factory=lambda: NamedInt("units_format", 0),
        metadata={"description": "Units format (0=no suffix, 1=bare, 2=parenthesis)"},
    )
    precision: NamedInt = field(
        default_factory=lambda: NamedInt("precision", 2),
        metadata={"description": "Precision digits"},
    )
    override_value: NamedString = field(
        default_factory=lambda: NamedString("override_value", ""),
        metadata={"description": "Override text value", "required": False},
    )
    suppress_zeros: TokenFlag = field(
        default_factory=lambda: TokenFlag("suppress_zeros"),
        metadata={
            "description": "Whether to suppress trailing zeros",
            "required": False,
        },
    )


@dataclass
class Dimension(NamedObject):
    """Dimension definition token.

    The 'dimension' token defines measurement dimensions in the format::

        (dimension
            [locked]
            (type DIMENSION_TYPE)
            (layer LAYER_DEFINITION)
            (uuid UUID)
            (pts (xy X Y) (xy X Y))
            [(height HEIGHT)]
            [(orientation ORIENTATION)]
            [(leader_length LEADER_LENGTH)]
            [(gr_text GRAPHICAL_TEXT)]
            [(format DIMENSION_FORMAT)]
            (style DIMENSION_STYLE)
        )

    Args:
        locked: Whether dimension is locked (optional)
        type: Dimension type (aligned | leader | center | orthogonal | radial)
        layer: Layer definition
        uuid: Unique identifier
        pts: Dimension points
        height: Height for aligned dimensions (optional)
        orientation: Orientation angle for orthogonal dimensions (optional)
        leader_length: Leader length for radial dimensions (optional)
        gr_text: Dimension text (optional)
        format: Dimension format (optional)
        style: Dimension style
    """

    __token_name__: ClassVar[str] = "dimension"

    locked: TokenFlag = field(
        default_factory=lambda: TokenFlag("locked"),
        metadata={"description": "Whether dimension is locked", "required": False},
    )
    type: Type = field(
        default_factory=lambda: Type(),
        metadata={
            "description": "Dimension type (aligned | leader | center | orthogonal | radial)"
        },
    )
    layer: Layer = field(
        default_factory=lambda: Layer(), metadata={"description": "Layer definition"}
    )
    uuid: Uuid = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )
    pts: Pts = field(
        default_factory=lambda: Pts(), metadata={"description": "Dimension points"}
    )
    height: NamedFloat = field(
        default_factory=lambda: NamedFloat("height", 0.0),
        metadata={"description": "Height for aligned dimensions", "required": False},
    )
    orientation: NamedFloat = field(
        default_factory=lambda: NamedFloat("orientation", 0.0),
        metadata={
            "description": "Orientation angle for orthogonal dimensions",
            "required": False,
        },
    )  # todo: use orientation
    leader_length: NamedFloat = field(
        default_factory=lambda: NamedFloat("leader_length", 0.0),
        metadata={
            "description": "Leader length for radial dimensions",
            "required": False,
        },
    )
    gr_text: Optional[GrText] = field(
        default=None, metadata={"description": "Dimension text", "required": False}
    )
    format: Optional[Format] = field(
        default=None, metadata={"description": "Dimension format", "required": False}
    )
    style: NamedString = field(
        default_factory=lambda: NamedString("style", ""),
        metadata={"description": "Dimension style"},
    )


# Footprint Graphics Elements


@dataclass
class FpArc(NamedObject):
    """Footprint arc definition token.

    The 'fp_arc' token defines an arc in a footprint in the format::

        (fp_arc
            (start X Y)
            [(mid X Y)]
            (end X Y)
            (layer LAYER_DEFINITION)
            (width WIDTH)
            [STROKE_DEFINITION]
            [(locked)]
            [(uuid UUID)]
            [(angle ANGLE)]
        )

    Args:
        start: Start point coordinates
        mid: Mid point coordinates (optional)
        end: End point coordinates
        layer: Layer definition
        width: Line width (prior to version 7) (optional)
        stroke: Stroke definition (from version 7) (optional)
        locked: Whether the arc is locked (optional)
        angle: Arc angle in degrees (optional)
        uuid: Unique identifier (optional)
    """

    __token_name__: ClassVar[str] = "fp_arc"

    start: Start = field(
        default_factory=lambda: Start(),
        metadata={"description": "Start point coordinates"},
    )
    mid: Optional[Mid] = field(
        default=None,
        metadata={"description": "Mid point coordinates", "required": False},
    )
    end: End = field(
        default_factory=lambda: End(), metadata={"description": "End point coordinates"}
    )
    layer: Optional[Layer] = field(
        default_factory=lambda: Layer(), metadata={"description": "Layer definition"}
    )
    width: NamedFloat = field(
        default_factory=lambda: NamedFloat("width", 0.0),
        metadata={"description": "Line width (prior to version 7)", "required": False},
    )
    stroke: Optional[Stroke] = field(
        default=None,
        metadata={
            "description": "Stroke definition (from version 7)",
            "required": False,
        },
    )
    locked: TokenFlag = field(
        default_factory=lambda: TokenFlag("locked"),
        metadata={"description": "Whether the arc is locked", "required": False},
    )
    angle: NamedFloat = field(
        default_factory=lambda: NamedFloat("angle", 0.0),
        metadata={"description": "Arc angle in degrees", "required": False},
    )
    uuid: Optional[Uuid] = field(
        default=None, metadata={"description": "Unique identifier", "required": False}
    )


@dataclass
class FpCircle(NamedObject):
    """Footprint circle definition token.

    The 'fp_circle' token defines a circle in a footprint in the format::

        (fp_circle
            (center X Y)
            (end X Y)
            (layer LAYER)
            (width WIDTH)
            [(tstamp UUID)]
        )

    Args:
        center: Center point
        end: End point
        layer: Layer definition
        width: Line width (optional)
        tstamp: Timestamp UUID (optional)
        uuid: Unique identifier (optional)
        stroke: Stroke definition (optional)
        fill: Fill definition (optional)
        locked: Whether the circle is locked (optional)
    """

    __token_name__: ClassVar[str] = "fp_circle"

    center: Center = field(
        default_factory=lambda: Center(), metadata={"description": "Center point"}
    )
    end: End = field(
        default_factory=lambda: End(), metadata={"description": "End point"}
    )
    layer: Layer = field(
        default_factory=lambda: Layer(), metadata={"description": "Layer definition"}
    )
    width: NamedFloat = field(
        default_factory=lambda: NamedFloat("width", 0.0),
        metadata={"description": "Line width", "required": False},
    )
    tstamp: NamedString = field(
        default_factory=lambda: NamedString("tstamp", ""),
        metadata={"description": "Timestamp UUID", "required": False},
    )
    uuid: Optional[Uuid] = field(
        default=None, metadata={"description": "Unique identifier", "required": False}
    )
    stroke: Optional[Stroke] = field(
        default=None, metadata={"description": "Stroke definition", "required": False}
    )
    fill: TokenFlag = field(
        default_factory=lambda: TokenFlag("fill"),
        metadata={"description": "Fill definition", "required": False},
    )
    locked: TokenFlag = field(
        default_factory=lambda: TokenFlag("locked"),
        metadata={"description": "Whether the circle is locked", "required": False},
    )


@dataclass
class FpCurve(NamedObject):
    """Footprint curve definition token.

    The 'fp_curve' token defines a Bezier curve in a footprint in the format::

        (fp_curve
            (pts (xy X Y) (xy X Y) (xy X Y) (xy X Y))
            (layer LAYER)
            (width WIDTH)
            [(tstamp UUID)]
        )

    Args:
        pts: Control points
        layer: Layer definition
        width: Line width
        tstamp: Timestamp UUID (optional)
        stroke: Stroke definition (optional)
        locked: Whether the curve is locked (optional)
    """

    __token_name__: ClassVar[str] = "fp_curve"

    pts: Pts = field(
        default_factory=lambda: Pts(), metadata={"description": "Control points"}
    )
    layer: Layer = field(
        default_factory=lambda: Layer(), metadata={"description": "Layer definition"}
    )
    width: NamedFloat = field(
        default_factory=lambda: NamedFloat("width", 0.0),
        metadata={"description": "Line width"},
    )
    tstamp: NamedString = field(
        default_factory=lambda: NamedString("tstamp", ""),
        metadata={"description": "Timestamp UUID", "required": False},
    )
    stroke: Optional[Stroke] = field(
        default=None, metadata={"description": "Stroke definition", "required": False}
    )
    locked: TokenFlag = field(
        default_factory=lambda: TokenFlag("locked"),
        metadata={"description": "Whether the curve is locked", "required": False},
    )


@dataclass
class FpLine(NamedObject):
    """Footprint line definition token.

    The 'fp_line' token defines a line in a footprint in the format::

        (fp_line
            (start X Y)
            (end X Y)
            (layer LAYER)
            (width WIDTH)
            [(tstamp UUID)]
        )

    Args:
        start: Start point
        end: End point
        layer: Layer definition
        width: Line width (optional)
        tstamp: Timestamp UUID (optional)
        uuid: Unique identifier (optional)
        stroke: Stroke definition (optional)
        locked: Whether the line is locked (optional)
    """

    __token_name__: ClassVar[str] = "fp_line"

    start: Start = field(
        default_factory=lambda: Start(), metadata={"description": "Start point"}
    )
    end: End = field(
        default_factory=lambda: End(), metadata={"description": "End point"}
    )
    layer: Layer = field(
        default_factory=lambda: Layer(), metadata={"description": "Layer definition"}
    )
    width: NamedFloat = field(
        default_factory=lambda: NamedFloat("width", 0.0),
        metadata={"description": "Line width", "required": False},
    )
    tstamp: NamedString = field(
        default_factory=lambda: NamedString("tstamp", ""),
        metadata={"description": "Timestamp UUID", "required": False},
    )
    uuid: Optional[Uuid] = field(
        default=None, metadata={"description": "Unique identifier", "required": False}
    )
    stroke: Optional[Stroke] = field(
        default=None, metadata={"description": "Stroke definition", "required": False}
    )
    locked: TokenFlag = field(
        default_factory=lambda: TokenFlag("locked"),
        metadata={"description": "Whether the line is locked", "required": False},
    )


@dataclass
class FpPoly(NamedObject):
    """Footprint polygon definition token.

    The 'fp_poly' token defines a polygon in a footprint in the format::

        (fp_poly
            (pts (xy X Y) ...)
            (layer LAYER)
            (width WIDTH)
            [(tstamp UUID)]
        )

    Args:
        pts: Polygon points
        layer: Layer definition (optional)
        width: Line width (optional)
        tstamp: Timestamp UUID (optional)
        stroke: Stroke definition (optional)
        fill: Fill definition (optional)
        locked: Whether thepolygon is locked (optional)
        uuid: Unique identifier (optional)
    """

    __token_name__: ClassVar[str] = "fp_poly"

    pts: Pts = field(
        default_factory=lambda: Pts(), metadata={"description": "Polygon points"}
    )
    layer: Optional[Layer] = field(
        default=None, metadata={"description": "Layer definition", "required": False}
    )
    width: NamedFloat = field(
        default_factory=lambda: NamedFloat("width", 0.0),
        metadata={"description": "Line width", "required": False},
    )
    tstamp: NamedString = field(
        default_factory=lambda: NamedString("tstamp", ""),
        metadata={"description": "Timestamp UUID", "required": False},
    )
    stroke: Optional[Stroke] = field(
        default=None, metadata={"description": "Stroke definition", "required": False}
    )
    fill: TokenFlag = field(
        default_factory=lambda: TokenFlag("fill"),
        metadata={"description": "Fill definition", "required": False},
    )
    locked: TokenFlag = field(
        default_factory=lambda: TokenFlag("locked"),
        metadata={"description": "Whether thepolygon is locked", "required": False},
    )
    uuid: Optional[Uuid] = field(
        default=None, metadata={"description": "Unique identifier", "required": False}
    )


@dataclass
class FpRect(NamedObject):
    """Footprint rectangle definition token.

    The 'fp_rect' token defines a graphic rectangle in a footprint definition in the format::

        (fp_rect
            (start X Y)
            (end X Y)
            (layer LAYER_DEFINITION)
            (width WIDTH)
            STROKE_DEFINITION
            [(fill yes | no)]
            [(locked)]
            (uuid UUID)
        )

    Args:
        start: Coordinates of the upper left corner
        end: Coordinates of the lower right corner
        layer: Layer definition
        width: Line width (prior to version 7) (optional)
        stroke: Stroke definition (from version 7) (optional)
        fill: Whether the rectangle is filled (yes/no) (optional)
        locked: Whether the rectangle cannot be edited (optional)
        uuid: Unique identifier
    """

    __token_name__: ClassVar[str] = "fp_rect"

    start: Start = field(
        default_factory=lambda: Start(),
        metadata={"description": "Coordinates of the upper left corner"},
    )
    end: End = field(
        default_factory=lambda: End(),
        metadata={"description": "Coordinates of the lower right corner"},
    )
    layer: Layer = field(
        default_factory=lambda: Layer(), metadata={"description": "Layer definition"}
    )
    width: NamedFloat = field(
        default_factory=lambda: NamedFloat("width", 0.0),
        metadata={"description": "Line width (prior to version 7)", "required": False},
    )
    stroke: Optional[Stroke] = field(
        default=None,
        metadata={
            "description": "Stroke definition (from version 7)",
            "required": False,
        },
    )
    fill: TokenFlag = field(
        default_factory=lambda: TokenFlag("fill"),
        metadata={
            "description": "Whether the rectangle is filled (yes/no)",
            "required": False,
        },
    )
    locked: TokenFlag = field(
        default_factory=lambda: TokenFlag("locked"),
        metadata={
            "description": "Whether the rectangle cannot be edited",
            "required": False,
        },
    )
    uuid: Uuid = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )


@dataclass
class FpText(NamedObject):
    """Footprint text definition token.

    The 'fp_text' token defines text in a footprint in the format::

        (fp_text
            TYPE
            "TEXT"
            POSITION_IDENTIFIER
            [unlocked]
            (layer LAYER_DEFINITION)
            [hide]
            (effects TEXT_EFFECTS)
            (uuid UUID)
        )

    Args:
        type: Text type (reference | value | user)
        text: Text content
        at: Position and rotation coordinates
        unlocked: Whether text orientation can be other than upright (optional)
        layer: Layer definition
        hide: Whether text is hidden (optional)
        effects: Text effects
        uuid: Unique identifier
    """

    __token_name__: ClassVar[str] = "fp_text"

    type: str = field(
        default="",
        metadata={"description": "Text type (reference | value | user)"},
    )
    text: str = field(default="", metadata={"description": "Text content"})
    at: FpTextAt = field(
        default_factory=lambda: FpTextAt(),
        metadata={"description": "Position and rotation coordinates"},
    )
    unlocked: TokenFlag = field(
        default_factory=lambda: TokenFlag("unlocked"),
        metadata={
            "description": "Whether text orientation can be other than upright",
            "required": False,
        },
    )
    layer: Layer = field(
        default_factory=lambda: Layer(), metadata={"description": "Layer definition"}
    )
    hide: TokenFlag = field(
        default_factory=lambda: TokenFlag("hide"),
        metadata={"description": "Whether text is hidden", "required": False},
    )
    effects: Effects = field(
        default_factory=lambda: Effects(), metadata={"description": "Text effects"}
    )
    uuid: Optional[Uuid] = field(
        default=None, metadata={"description": "Unique identifier"}
    )


@dataclass
class FpTextBox(NamedObject):
    """Footprint text box definition token.

    The 'fp_text_box' token defines a rectangle containing line-wrapped text in the format::

        (fp_text_box
            [locked]
            "TEXT"
            [(start X Y)]
            [(end X Y)]
            [(pts (xy X Y) (xy X Y) (xy X Y) (xy X Y))]
            [(angle ROTATION)]
            (layer LAYER_DEFINITION)
            (uuid UUID)
            TEXT_EFFECTS
            [STROKE_DEFINITION]
            [(render_cache RENDER_CACHE)]
        )

    Args:
        locked: Whether the text box can be moved (optional)
        text: Content of the text box
        start: Top-left corner of cardinally oriented text box (optional)
        end: Bottom-right corner of cardinally oriented text box (optional)
        pts: Four corners of non-cardinally oriented text box (optional)
        angle: Rotation of the text box in degrees (optional)
        layer: Layer definition
        uuid: Unique identifier
        effects: Text effects
        stroke: Stroke definition for optional border (optional)
        render_cache: Text rendering cache for TrueType fonts (optional)
    """

    __token_name__: ClassVar[str] = "fp_text_box"

    locked: TokenFlag = field(
        default_factory=lambda: TokenFlag("locked"),
        metadata={
            "description": "Whether the text box can be moved",
            "required": False,
        },
    )
    text: str = field(default="", metadata={"description": "Content of the text box"})
    start: Optional[Start] = field(
        default=None,
        metadata={
            "description": "Top-left corner of cardinally oriented text box",
            "required": False,
        },
    )
    end: Optional[End] = field(
        default=None,
        metadata={
            "description": "Bottom-right corner of cardinally oriented text box",
            "required": False,
        },
    )
    pts: Optional[Pts] = field(
        default=None,
        metadata={
            "description": "Four corners of non-cardinally oriented text box",
            "required": False,
        },
    )
    angle: NamedFloat = field(
        default_factory=lambda: NamedFloat("angle", 0.0),
        metadata={
            "description": "Rotation of the text box in degrees",
            "required": False,
        },
    )
    layer: Layer = field(
        default_factory=lambda: Layer(), metadata={"description": "Layer definition"}
    )
    uuid: Uuid = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )
    effects: Effects = field(
        default_factory=lambda: Effects(), metadata={"description": "Text effects"}
    )
    stroke: Optional[Stroke] = field(
        default=None,
        metadata={
            "description": "Stroke definition for optional border",
            "required": False,
        },
    )
    render_cache: NamedString = field(
        default_factory=lambda: NamedString("render_cache", ""),
        metadata={
            "description": "Text rendering cache for TrueType fonts",
            "required": False,
        },
    )


# Graphics (Gr*) classes derived from Footprint (Fp*) classes
# These share the same structure but use different token names


@dataclass
class GrLine(FpLine):
    """Graphical line derived from footprint line.

    Inherits all fields from FpLine but uses 'gr_line' token.
    """

    __token_name__: ClassVar[str] = "gr_line"


@dataclass
class GrRect(FpRect):
    """Graphical rectangle derived from footprint rectangle.

    Inherits all fields from FpRect but uses 'gr_rect' token.
    """

    __token_name__: ClassVar[str] = "gr_rect"


@dataclass
class GrPoly(FpPoly):
    """Graphical polygon derived from footprint polygon.

    Inherits all fields from FpPoly but uses 'gr_poly' token.
    """

    __token_name__: ClassVar[str] = "gr_poly"


@dataclass
class GrCurve(FpCurve):
    """Graphical curve derived from footprint curve.

    Inherits all fields from FpCurve but uses 'gr_curve' token.
    """

    __token_name__: ClassVar[str] = "gr_curve"
