"""Primitive graphics elements for KiCad S-expressions - basic geometric shapes."""

from dataclasses import dataclass, field
from typing import Optional

from .base_element import KiCadObject, OptionalFlag
from .base_types import (
    Center,
    End,
    Fill,
    Mid,
    Pts,
    Radius,
    Start,
    Stroke,
    Uuid,
    Width,
)


@dataclass
class Arc(KiCadObject):
    """Arc definition token.

    The 'arc' token defines a graphical arc in a symbol definition in the format::

        (arc
            (start X Y)
            (mid X Y)
            (end X Y)
            STROKE_DEFINITION
            FILL_DEFINITION
            (uuid UUID)
        )

    Args:
        start: Start point of the arc
        mid: Mid point of the arc (optional)
        end: End point of the arc
        stroke: Stroke definition for outline
        fill: Fill definition for filling
        uuid: Unique identifier (optional)
    """

    __token_name__ = "arc"

    start: Start = field(
        default_factory=lambda: Start(),
        metadata={"description": "Start point of the arc"},
    )
    mid: Optional[Mid] = field(
        default=None,
        metadata={"description": "Mid point of the arc", "required": False},
    )
    end: End = field(
        default_factory=lambda: End(), metadata={"description": "End point of the arc"}
    )
    stroke: Stroke = field(
        default_factory=lambda: Stroke(),
        metadata={"description": "Stroke definition for outline"},
    )
    fill: Fill = field(
        default_factory=lambda: Fill(),
        metadata={"description": "Fill definition for filling"},
    )
    uuid: Optional[Uuid] = field(
        default=None,
        metadata={"description": "Unique identifier", "required": False},
    )


@dataclass
class Bezier(KiCadObject):
    """Bezier curve definition token.

    The 'bezier' token defines a graphic Cubic Bezier curve in the format::

        (bezier
            COORDINATE_POINT_LIST
            (layer LAYER_DEFINITION)
            (width WIDTH)
            (uuid UUID)
        )

    Args:
        pts: List of X/Y coordinates of the four points of the curve
        stroke: Stroke definition for outline (optional)
        fill: Fill definition for filling (optional)
        width: Line width of the curve (optional)
        uuid: Unique identifier (optional)
    """

    __token_name__ = "bezier"

    pts: Pts = field(
        default_factory=lambda: Pts(),
        metadata={
            "description": "List of X/Y coordinates of the four points of the curve"
        },
    )
    stroke: Optional[Stroke] = field(
        default=None,
        metadata={"description": "Stroke definition for outline", "required": False},
    )
    fill: Optional[Fill] = field(
        default=None,
        metadata={"description": "Fill definition for filling", "required": False},
    )
    width: Optional[Width] = field(
        default=None,
        metadata={"description": "Line width of the curve", "required": False},
    )
    uuid: Optional[Uuid] = field(
        default=None,
        metadata={
            "description": "Unique identifier",
            "required": False,
        },
    )


@dataclass
class Circle(KiCadObject):
    """Circle definition token.

    The 'circle' token defines a graphical circle in a symbol definition in the format::

        (circle
            (center X Y)
            (radius RADIUS)
            STROKE_DEFINITION
            FILL_DEFINITION
        )

    Args:
        center: Center point of the circle
        radius: Radius length of the circle
        stroke: Stroke definition for outline
        fill: Fill definition for filling
        uuid: Unique identifier (optional)
    """

    __token_name__ = "circle"

    center: Center = field(
        default_factory=lambda: Center(),
        metadata={"description": "Center point of the circle"},
    )
    radius: Radius = field(
        default_factory=lambda: Radius(),
        metadata={"description": "Radius length of the circle"},
    )
    stroke: Stroke = field(
        default_factory=lambda: Stroke(),
        metadata={"description": "Stroke definition for outline"},
    )
    fill: Fill = field(
        default_factory=lambda: Fill(),
        metadata={"description": "Fill definition for filling"},
    )
    uuid: Optional[Uuid] = field(
        default=None,
        metadata={"description": "Unique identifier", "required": False},
    )


@dataclass
class Line(KiCadObject):
    """Line definition token.

    The 'line' token defines a basic line geometry in the format::

        (line (start X Y) (end X Y) (uuid UUID))

    Args:
        start: Start point of the line
        end: End point of the line
        uuid: Unique identifier (optional)
    """

    __token_name__ = "line"

    start: Start = field(
        default_factory=lambda: Start(),
        metadata={"description": "Start point of the line"},
    )
    end: End = field(
        default_factory=lambda: End(), metadata={"description": "End point of the line"}
    )
    uuid: Optional[Uuid] = field(
        default=None,
        metadata={"description": "Unique identifier", "required": False},
    )


@dataclass
class Polygon(KiCadObject):
    """Polygon definition token.

    The 'polygon' token defines a polygon with multiple points in the format::

        (polygon (pts (xy X Y) (xy X Y) ...) (uuid UUID))

    Args:
        pts: Polygon vertex points
        uuid: Unique identifier (optional)
    """

    __token_name__ = "polygon"

    pts: Pts = field(
        default_factory=lambda: Pts(), metadata={"description": "Polygon vertex points"}
    )
    uuid: Optional[Uuid] = field(
        default=None,
        metadata={"description": "Unique identifier", "required": False},
    )


@dataclass
class Polyline(KiCadObject):
    """Polyline definition token.

    The 'polyline' token defines a connected series of line segments in the format::

        (polyline
            (pts (xy X Y) (xy X Y) ...)
            STROKE_DEFINITION
            FILL_DEFINITION
        )

    Args:
        pts: Polyline connection points
        stroke: Stroke definition for outline (optional)
        fill: Fill definition (optional)
        uuid: Unique identifier (optional)
    """

    __token_name__ = "polyline"

    pts: Pts = field(
        default_factory=lambda: Pts(),
        metadata={"description": "Polyline connection points"},
    )
    stroke: Optional[Stroke] = field(
        default=None,
        metadata={"description": "Stroke definition for outline", "required": False},
    )
    fill: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("fill"),
        metadata={"description": "Fill definition", "required": False},
    )
    uuid: Optional[Uuid] = field(
        default=None,
        metadata={"description": "Unique identifier", "required": False},
    )


@dataclass
class Rect(KiCadObject):
    """Rectangle definition token.

    The 'rect' token defines a basic rectangle geometry in the format::

        (rect (start X Y) (end X Y))

    Args:
        start: Start corner of the rectangle
        end: End corner of the rectangle
    """

    __token_name__ = "rect"

    start: Start = field(
        default_factory=lambda: Start(),
        metadata={"description": "Start corner of the rectangle"},
    )
    end: End = field(
        default_factory=lambda: End(),
        metadata={"description": "End corner of the rectangle"},
    )


@dataclass
class Rectangle(KiCadObject):
    """Rectangle definition token (symbol form).

    The 'rectangle' token defines a graphical rectangle in a symbol definition in the format::

        (rectangle
            (start X Y)
            (end X Y)
            STROKE_DEFINITION
            FILL_DEFINITION
        )

    Args:
        start: Start point of the rectangle
        end: End point of the rectangle
        stroke: Stroke definition for outline
        fill: Fill definition for filling
        uuid: Unique identifier (optional)
    """

    __token_name__ = "rectangle"

    start: Start = field(
        default_factory=lambda: Start(),
        metadata={"description": "Start point of the rectangle"},
    )
    end: End = field(
        default_factory=lambda: End(),
        metadata={"description": "End point of the rectangle"},
    )
    stroke: Stroke = field(
        default_factory=lambda: Stroke(),
        metadata={"description": "Stroke definition for outline"},
    )
    fill: Fill = field(
        default_factory=lambda: Fill(),
        metadata={"description": "Fill definition for filling"},
    )
    uuid: Optional[Uuid] = field(
        default=None,
        metadata={"description": "Unique identifier", "required": False},
    )
