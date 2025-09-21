"""Advanced graphics elements for KiCad S-expressions - complex graphical objects."""

from dataclasses import dataclass, field
from typing import Optional

from . import text_and_documents
from .base_element import KiCadObject, OptionalFlag
from .base_types import (
    Angle,
    At,
    Center,
    Effects,
    End,
    Fill,
    Height,
    Layer,
    Locked,
    Pos,
    Pts,
    Start,
    Stroke,
    Style,
    Tstamp,
    Type,
    Units,
    Unlocked,
    Uuid,
    Width,
)


@dataclass
class LeaderLength(KiCadObject):
    """Leader length definition token for radial dimensions.

    The 'leader_length' token defines leader line length in the format::

        (leader_length LENGTH)

    Args:
        length: Length value for leader line
    """

    __token_name__ = "leader_length"

    length: float = field(
        default=0.0, metadata={"description": "Length value for leader line"}
    )


@dataclass
class UnitsFormat(KiCadObject):
    """Units format definition token for dimensions.

    The 'units_format' token defines units display format in the format::

        (units_format FORMAT)

    Args:
        format: Units format (0=no suffix, 1=bare, 2=parenthesis)
    """

    __token_name__ = "units_format"

    format: int = field(
        default=1,
        metadata={"description": "Units format (0=no suffix, 1=bare, 2=parenthesis)"},
    )


@dataclass
class Precision(KiCadObject):
    """Precision definition token for dimension formatting.

    The 'precision' token defines decimal precision in the format::

        (precision DIGITS)

    Args:
        digits: Number of decimal places to display
    """

    __token_name__ = "precision"

    digits: int = field(
        default=2, metadata={"description": "Number of decimal places to display"}
    )


@dataclass
class SuppressZeros(KiCadObject):
    """Suppress zeros definition token for dimension formatting.

    The 'suppress_zeros' token defines zero suppression in the format::

        (suppress_zeros yes | no)

    Args:
        suppress: Whether to suppress trailing zeros
    """

    __token_name__ = "suppress_zeros"

    suppress: bool = field(
        default=False, metadata={"description": "Whether to suppress trailing zeros"}
    )


@dataclass
class RenderCache(KiCadObject):
    """Render cache definition token for text rendering optimization.

    The 'render_cache' token defines cached text rendering data in the format::

        (render_cache "CACHE_DATA")

    Args:
        data: Cached rendering data for TrueType fonts
    """

    __token_name__ = "render_cache"

    data: str = field(
        default="", metadata={"description": "Cached rendering data for TrueType fonts"}
    )


@dataclass
class GrArc(KiCadObject):
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
        layer: Layer definition
        width: Line width
        uuid: Unique identifier
    """

    __token_name__ = "gr_arc"

    start: Start = field(
        default_factory=lambda: Start(),
        metadata={"description": "Start point coordinates"},
    )
    mid: Pos = field(
        default_factory=lambda: Pos(), metadata={"description": "Mid point coordinates"}
    )
    end: End = field(
        default_factory=lambda: End(), metadata={"description": "End point coordinates"}
    )
    layer: Layer = field(
        default_factory=lambda: Layer(), metadata={"description": "Layer definition"}
    )
    width: Width = field(
        default_factory=lambda: Width(), metadata={"description": "Line width"}
    )
    uuid: Uuid = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )


@dataclass
class GrBbox(KiCadObject):
    """Graphical bounding box definition token.

    The 'gr_bbox' token defines a bounding box inside which annotations will be shown in the format::

        (gr_bbox
            (start X Y)
            (end X Y)
        )

    Args:
        start: Coordinates of the upper left corner of the rectangle
        end: Coordinates of the lower right corner of the rectangle
    """

    __token_name__ = "gr_bbox"

    start: Start = field(
        default_factory=lambda: Start(),
        metadata={"description": "Coordinates of the upper left corner"},
    )
    end: End = field(
        default_factory=lambda: End(),
        metadata={"description": "Coordinates of the lower right corner"},
    )


@dataclass
class GrCircle(KiCadObject):
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

    __token_name__ = "gr_circle"

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
    width: Width = field(
        default_factory=lambda: Width(), metadata={"description": "Line width"}
    )
    fill: Optional[Fill] = field(
        default=None, metadata={"description": "Fill definition", "required": False}
    )
    uuid: Uuid = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )


@dataclass
class GrText(KiCadObject):
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

    __token_name__ = "gr_text"

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
class GrTextBox(KiCadObject):
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

    __token_name__ = "gr_text_box"

    locked: Optional[Locked] = field(
        default=None,
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
    angle: Optional[Angle] = field(
        default=None,
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
    render_cache: Optional[RenderCache] = field(
        default=None,
        metadata={
            "description": "Text rendering cache for TrueType fonts",
            "required": False,
        },
    )


@dataclass
class OverrideValue(KiCadObject):
    """Override value definition token.

    The 'override_value' token defines an override value in the format::

        (override_value "VALUE")

    Args:
        value: Override value string
    """

    __token_name__ = "override_value"

    value: str = field(default="", metadata={"description": "Override value string"})


@dataclass
class Format(KiCadObject):
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

    __token_name__ = "format"

    prefix: Optional[text_and_documents.Suffix] = (
        field(  # Using Suffix as prefix implementation
            default=None, metadata={"description": "Text prefix", "required": False}
        )
    )
    suffix: Optional[text_and_documents.Suffix] = field(
        default=None, metadata={"description": "Text suffix", "required": False}
    )
    units: Units = field(
        default_factory=lambda: Units(),
        metadata={"description": "Units type (0=inches, 1=mils, 2=mm, 3=auto)"},
    )
    units_format: UnitsFormat = field(
        default_factory=lambda: UnitsFormat(),
        metadata={"description": "Units format (0=no suffix, 1=bare, 2=parenthesis)"},
    )
    precision: Precision = field(
        default_factory=lambda: Precision(),
        metadata={"description": "Precision digits"},
    )
    override_value: Optional[OverrideValue] = field(
        default=None, metadata={"description": "Override text value", "required": False}
    )
    suppress_zeros: Optional[SuppressZeros] = field(
        default=None,
        metadata={
            "description": "Whether to suppress trailing zeros",
            "required": False,
        },
    )


@dataclass
class Dimension(KiCadObject):
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

    __token_name__ = "dimension"

    locked: Optional[Locked] = field(
        default=None,
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
    height: Optional[Height] = field(
        default=None,
        metadata={"description": "Height for aligned dimensions", "required": False},
    )
    orientation: Optional[Angle] = field(
        default=None,
        metadata={
            "description": "Orientation angle for orthogonal dimensions",
            "required": False,
        },
    )  # todo: use orientation
    leader_length: Optional[LeaderLength] = field(
        default=None,
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
    style: Style = field(
        default_factory=lambda: Style(), metadata={"description": "Dimension style"}
    )


# Footprint Graphics Elements


@dataclass
class FpArc(KiCadObject):
    """Footprint arc definition token.

    The 'fp_arc' token defines an arc in a footprint in the format::

        (fp_arc
            (start X Y)
            (mid X Y)
            (end X Y)
            (layer LAYER_DEFINITION)
            (width WIDTH)
            STROKE_DEFINITION
            [(locked)]
            (uuid UUID)
        )

    Args:
        start: Start point coordinates
        mid: Mid point coordinates
        end: End point coordinates
        layer: Layer definition
        width: Line width (prior to version 7)
        stroke: Stroke definition (from version 7)
        locked: Whether the arc is locked (optional)
        uuid: Unique identifier
    """

    __token_name__ = "fp_arc"

    start: Start = field(
        default_factory=lambda: Start(),
        metadata={"description": "Start point coordinates"},
    )
    mid: Pos = field(
        default_factory=lambda: Pos(), metadata={"description": "Mid point coordinates"}
    )
    end: End = field(
        default_factory=lambda: End(), metadata={"description": "End point coordinates"}
    )
    layer: Layer = field(
        default_factory=lambda: Layer(), metadata={"description": "Layer definition"}
    )
    width: Width = field(
        default_factory=lambda: Width(),
        metadata={"description": "Line width (prior to version 7)"},
    )
    stroke: Stroke = field(
        default_factory=lambda: Stroke(),
        metadata={"description": "Stroke definition (from version 7)"},
    )
    locked: Optional[Locked] = field(
        default=None,
        metadata={"description": "Whether the arc is locked", "required": False},
    )
    uuid: Uuid = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )


@dataclass
class FpCircle(KiCadObject):
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
        center: Center point coordinates
        end: End point coordinates
        layer: Layer definition
        width: Line width
        tstamp: Timestamp UUID (optional)
        stroke: Stroke definition (optional)
        fill: Fill definition (optional)
        locked: Whether the circle is locked (optional)
    """

    __token_name__ = "fp_circle"

    center: Center = field(
        default_factory=lambda: Center(), metadata={"description": "Center point"}
    )
    end: End = field(
        default_factory=lambda: End(), metadata={"description": "End point"}
    )
    layer: Layer = field(
        default_factory=lambda: Layer(), metadata={"description": "Layer definition"}
    )
    width: Optional[Width] = field(
        default=None, metadata={"description": "Line width", "required": False}
    )
    tstamp: Optional[Tstamp] = field(
        default=None, metadata={"description": "Timestamp UUID", "required": False}
    )
    uuid: Optional[Uuid] = field(
        default=None, metadata={"description": "Unique identifier", "required": False}
    )
    stroke: Optional[Stroke] = field(
        default=None, metadata={"description": "Stroke definition", "required": False}
    )
    # fill: Optional[Fill] = field(
    #     default=None, metadata={"description": "Fill definition", "required": False}
    # )
    fill: Optional[bool] = field(
        default=None, metadata={"description": "Fill definition", "required": False}
    )
    locked: Optional[Locked] = field(
        default=None,
        metadata={"description": "Whether the circle is locked", "required": False},
    )


@dataclass
class FpCurve(KiCadObject):
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

    __token_name__ = "fp_curve"

    pts: Pts = field(
        default_factory=lambda: Pts(), metadata={"description": "Control points"}
    )
    layer: Layer = field(
        default_factory=lambda: Layer(), metadata={"description": "Layer definition"}
    )
    width: Width = field(
        default_factory=lambda: Width(), metadata={"description": "Line width"}
    )
    tstamp: Optional[Tstamp] = field(
        default=None, metadata={"description": "Timestamp UUID", "required": False}
    )
    stroke: Optional[Stroke] = field(
        default=None, metadata={"description": "Stroke definition", "required": False}
    )
    locked: Optional[Locked] = field(
        default=None,
        metadata={"description": "Whether the curve is locked", "required": False},
    )


@dataclass
class FpLine(KiCadObject):
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
        start: Start point coordinates
        end: End point coordinates
        layer: Layer definition
        width: Line width
        tstamp: Timestamp UUID (optional)
        stroke: Stroke definition (optional)
        locked: Whether the line is locked (optional)
    """

    __token_name__ = "fp_line"

    start: Start = field(
        default_factory=lambda: Start(), metadata={"description": "Start point"}
    )
    end: End = field(
        default_factory=lambda: End(), metadata={"description": "End point"}
    )
    layer: Layer = field(
        default_factory=lambda: Layer(), metadata={"description": "Layer definition"}
    )
    width: Width = field(
        default_factory=lambda: Width(), metadata={"description": "Line width"}
    )
    tstamp: Optional[Tstamp] = field(
        default=None, metadata={"description": "Timestamp UUID", "required": False}
    )
    stroke: Optional[Stroke] = field(
        default=None, metadata={"description": "Stroke definition", "required": False}
    )
    locked: Optional[Locked] = field(
        default=None,
        metadata={"description": "Whether the line is locked", "required": False},
    )


@dataclass
class FpPoly(KiCadObject):
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
        layer: Layer definition
        width: Line width
        tstamp: Timestamp UUID (optional)
        stroke: Stroke definition (optional)
        fill: Fill definition (optional)
        locked: Whether the polygon is locked (optional)
    """

    __token_name__ = "fp_poly"

    pts: Pts = field(
        default_factory=lambda: Pts(), metadata={"description": "Polygon points"}
    )
    layer: Layer = field(
        default_factory=lambda: Layer(), metadata={"description": "Layer definition"}
    )
    width: Width = field(
        default_factory=lambda: Width(), metadata={"description": "Line width"}
    )
    tstamp: Optional[Tstamp] = field(
        default=None, metadata={"description": "Timestamp UUID", "required": False}
    )
    stroke: Optional[Stroke] = field(
        default=None, metadata={"description": "Stroke definition", "required": False}
    )
    fill: Optional[Fill] = field(
        default=None, metadata={"description": "Fill definition", "required": False}
    )
    locked: Optional[Locked] = field(
        default=None,
        metadata={"description": "Whether thepolygon is locked", "required": False},
    )


@dataclass
class FpRect(KiCadObject):
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
        start: Coordinates of the upper left corner of the rectangle
        end: Coordinates of the lower right corner of the rectangle
        layer: Layer definition
        width: Line width of the rectangle (prior to version 7)
        stroke: Stroke definition for line width and style (from version 7)
        fill: Whether the rectangle is filled (optional)
        locked: Whether the rectangle cannot be edited (optional)
        uuid: Unique identifier of the rectangle object
    """

    __token_name__ = "fp_rect"

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
    width: Optional[Width] = field(
        default=None,
        metadata={"description": "Line width (prior to version 7)", "required": False},
    )
    stroke: Optional[Stroke] = field(
        default=None,
        metadata={
            "description": "Stroke definition (from version 7)",
            "required": False,
        },
    )
    # fill: Optional[Fill] = field(
    #     default=None,
    #     metadata={"description": "Whether the rectangle is filled", "required": False},
    # )
    fill: Optional[bool] = field(
        default=None,
        metadata={"description": "Whether the rectangle is filled", "required": False},
    )
    locked: Optional[Locked] = field(
        default=None,
        metadata={
            "description": "Whether the rectangle cannot be edited",
            "required": False,
        },
    )
    uuid: Uuid = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )


@dataclass
class FpText(KiCadObject):
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

    __token_name__ = "fp_text"

    type: str = field(
        default="",
        metadata={"description": "Text type (reference | value | user)"},
    )
    text: str = field(default="", metadata={"description": "Text content"})
    at: At = field(
        default_factory=lambda: At(),
        metadata={"description": "Position and rotation coordinates"},
    )
    unlocked: Optional[Unlocked] = field(
        default=None,
        metadata={
            "description": "Whether text orientation can be other than upright",
            "required": False,
        },
    )
    layer: Layer = field(
        default_factory=lambda: Layer(), metadata={"description": "Layer definition"}
    )
    hide: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag("hide"),
        metadata={"description": "Whether text is hidden", "required": False},
    )
    effects: Effects = field(
        default_factory=lambda: Effects(), metadata={"description": "Text effects"}
    )
    uuid: Uuid = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )


@dataclass
class FpTextBox(KiCadObject):
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

    __token_name__ = "fp_text_box"

    locked: Optional[Locked] = field(
        default=None,
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
    angle: Optional[Angle] = field(
        default=None,
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
    render_cache: Optional[RenderCache] = field(
        default=None,
        metadata={
            "description": "Text rendering cache for TrueType fonts",
            "required": False,
        },
    )
