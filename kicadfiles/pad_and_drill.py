"""Pad and drill related elements for KiCad S-expressions."""

from dataclasses import dataclass, field
from typing import ClassVar, List, Optional, Union

from .advanced_graphics import GrArc, GrCircle, GrCurve, GrLine, GrPoly, GrRect
from .base_element import (
    NamedFloat,
    NamedObject,
    NamedString,
    SymbolValue,
    TokenFlag,
)
from .base_types import Anchor, At, Layers, Offset, Size, Uuid
from .enums import PadShape, PadType, ZoneConnection


@dataclass
class Teardrops(NamedObject):
    """Teardrops definition token for pads.

    The 'teardrops' token defines teardrop settings in the format::

        (teardrops
            (best_length_ratio RATIO)
            (max_length LENGTH)
            (best_width_ratio RATIO)
            (max_width WIDTH)
            (curved_edges yes|no)
            (filter_ratio RATIO)
            (enabled yes|no)
            (allow_two_segments yes|no)
            (prefer_zone_connections yes|no)
        )

    Args:
        best_length_ratio: Best length ratio setting
        max_length: Maximum length setting
        best_width_ratio: Best width ratio setting
        max_width: Maximum width setting
        curved_edges: Curved edges setting (optional)
        filter_ratio: Filter ratio setting
        enabled: Enabled setting (optional)
        allow_two_segments: Allow two segments setting (optional)
        prefer_zone_connections: Prefer zone connections setting (optional)
    """

    __token_name__: ClassVar[str] = "teardrops"

    best_length_ratio: NamedFloat = field(
        default_factory=lambda: NamedFloat("best_length_ratio", 0.0),
        metadata={"description": "Best length ratio setting"},
    )
    max_length: NamedFloat = field(
        default_factory=lambda: NamedFloat("max_length", 0.0),
        metadata={"description": "Maximum length setting"},
    )
    best_width_ratio: NamedFloat = field(
        default_factory=lambda: NamedFloat("best_width_ratio", 0.0),
        metadata={"description": "Best width ratio setting"},
    )
    max_width: NamedFloat = field(
        default_factory=lambda: NamedFloat("max_width", 0.0),
        metadata={"description": "Maximum width setting"},
    )
    curved_edges: TokenFlag = field(
        default_factory=lambda: TokenFlag("curved_edges"),
        metadata={"description": "Curved edges setting", "required": False},
    )
    filter_ratio: NamedFloat = field(
        default_factory=lambda: NamedFloat("filter_ratio", 0.0),
        metadata={"description": "Filter ratio setting"},
    )
    enabled: TokenFlag = field(
        default_factory=lambda: TokenFlag("enabled"),
        metadata={"description": "Enabled setting", "required": False},
    )
    allow_two_segments: TokenFlag = field(
        default_factory=lambda: TokenFlag("allow_two_segments"),
        metadata={"description": "Allow two segments setting", "required": False},
    )
    prefer_zone_connections: TokenFlag = field(
        default_factory=lambda: TokenFlag("prefer_zone_connections"),
        metadata={"description": "Prefer zone connections setting", "required": False},
    )


@dataclass
class Chamfer(NamedObject):
    """Chamfer corner definition token for pads.

    The 'chamfer' token defines which corners of a rectangular pad get chamfered in the format::

        (chamfer CORNER_LIST)

    Valid chamfer corner attributes are top_left, top_right, bottom_left, and bottom_right.

    Args:
        corners: List of corners to chamfer
    """

    __token_name__: ClassVar[str] = "chamfer"

    corners: List[str] = field(
        default_factory=list, metadata={"description": "List of corners to chamfer"}
    )


@dataclass
class Options(NamedObject):
    """Custom pad options definition token.

    The 'options' token defines options for custom pads in the format::

        (options
            (clearance CLEARANCE_TYPE)
            (anchor PAD_SHAPE)
        )

    Valid clearance types are outline and convexhull.
    Valid anchor pad shapes are rect and circle.

    Args:
        clearance: Clearance type for custom pad (optional)
        anchor: Anchor pad shape (optional)
    """

    __token_name__: ClassVar[str] = "options"

    clearance: NamedString = field(
        default_factory=lambda: NamedString("clearance", ""),
        metadata={
            "description": "Clearance type for custom pad",
            "required": False,
        },
    )
    anchor: Optional[Anchor] = field(
        default=None,
        metadata={"description": "Anchor pad shape", "required": False},
    )


@dataclass
class Shape(NamedObject):
    """Pad shape definition token.

    The 'shape' token defines the shape of a pad in the format::

        (shape SHAPE_TYPE)

    Valid pad shapes are circle, rect, oval, trapezoid, roundrect, or custom.

    Args:
        shape: Pad shape type
    """

    __token_name__: ClassVar[str] = "shape"

    shape: PadShape = field(
        default=PadShape.CIRCLE, metadata={"description": "Pad shape type"}
    )


@dataclass
class ZoneConnect(NamedObject):
    """Zone connection definition token.

    The 'zone_connect' token defines how a pad connects to filled zones in the format::

        (zone_connect CONNECTION_TYPE)

    Valid connection types are integer values from 0 to 3:
    - 0: Pad not connected to zone
    - 1: Pad connected using thermal relief
    - 2: Pad connected using solid fill

    Args:
        connection_type: Zone connection type
    """

    __token_name__: ClassVar[str] = "zone_connect"

    connection_type: ZoneConnection = field(
        default=ZoneConnection.INHERITED,
        metadata={"description": "Zone connection type"},
    )


@dataclass
class Net(NamedObject):
    """Net connection definition token.

    The 'net' token defines the net connection in the format::

        (net ORDINAL "NET_NAME")

    Args:
        number: Net number
        name: Net name
    """

    __token_name__: ClassVar[str] = "net"

    number: int = field(default=0, metadata={"description": "Net number"})
    name: str = field(default="", metadata={"description": "Net name"})


@dataclass
class Drill(NamedObject):
    """Drill definition token for pads.

    The 'drill' token defines the drill attributes for a footprint pad in the format::

        (drill
            [oval]
            DIAMETER
            [WIDTH]
            [(offset X Y)]
        )

    Args:
        oval: Whether the drill is oval instead of round (optional)
        diameter: Drill diameter
        width: Width of the slot for oval drills (optional)
        offset: Drill offset coordinates from the center of the pad (optional)
    """

    __token_name__: ClassVar[str] = "drill"

    oval: Optional[SymbolValue] = field(
        default_factory=lambda: SymbolValue(token="oval"),
        metadata={
            "description": "Whether the drill is oval instead of round",
            "required": False,
        },
    )
    diameter: float = field(
        default=0.0,
        metadata={
            "description": "Drill diameter",
            "position": 2,  # Position after oval (or at 1 if no oval)
        },
    )
    width: Optional[float] = field(
        default=None,
        metadata={
            "description": "Width of the slot for oval drills",
            "required": False,
            "position": 3,
        },
    )
    offset: Optional[Offset] = field(
        default=None,
        metadata={
            "description": "Drill offset coordinates from the center of the pad",
            "required": False,
        },
    )


@dataclass
class Primitives(NamedObject):
    """Custom pad primitives definition token.

    The 'primitives' token defines drawing objects for custom pads in the format::

        (primitives
            (gr_poly ...)
            (gr_line ...)
            (gr_circle ...)
            (gr_arc ...)
            (gr_rect ...)
            (gr_curve ...)
            ...
        )

    Args:
        elements: List of primitive graphical elements (optional)
        width: Line width of graphical items (optional)
        fill: Whether geometry should be filled (optional)
    """

    __token_name__: ClassVar[str] = "primitives"

    elements: Optional[
        List[Union[GrArc, GrCircle, GrCurve, GrLine, GrPoly, GrRect]]
    ] = field(
        default_factory=list,
        metadata={
            "description": "List of primitive graphical elements",
            "required": False,
        },
    )
    width: NamedFloat = field(
        default_factory=lambda: NamedFloat("width", 0.0),
        metadata={"description": "Line width of graphical items", "required": False},
    )
    fill: TokenFlag = field(
        default_factory=lambda: TokenFlag("fill"),
        metadata={
            "description": "Whether geometry should be filled",
            "required": False,
        },
    )


@dataclass
class Pad(NamedObject):
    """Footprint pad definition token.

    The 'pad' token defines a pad in a footprint with comprehensive properties in the format::

        (pad "NUMBER" TYPE SHAPE POSITION_IDENTIFIER [(locked)] (size X Y)
             [(drill DRILL_DEFINITION)] (layers "CANONICAL_LAYER_LIST") ...)

    Note:
        Field order follows KiCad documentation, not dataclass conventions.
        Required fields after optional fields violate dataclass ordering.

    Args:
        number: Pad number or name
        type: Pad type
        shape: Pad shape
        at: Position and rotation
        size: Pad dimensions
        layers: Layer list
        drill: Drill definition (optional)
        property: Pad property (optional)
        locked: Whether pad is locked (optional)
        remove_unused_layer: Remove unused layers flag (optional)
        remove_unused_layers: Remove unused layers flag (newer format) (optional)
        keep_end_layers: Keep end layers flag (optional)
        roundrect_rratio: Round rectangle corner ratio (optional)
        chamfer_ratio: Chamfer ratio (optional)
        chamfer: Chamfer corners (optional)
        net: Net connection (optional)
        uuid: Unique identifier (optional)
        pinfunction: Pin function name (optional)
        pintype: Pin type (optional)
        die_length: Die length (optional)
        solder_mask_margin: Solder mask margin (optional)
        solder_paste_margin: Solder paste margin (optional)
        solder_paste_margin_ratio: Solder paste margin ratio (optional)
        clearance: Clearance value (optional)
        zone_connect: Zone connection type (optional)
        thermal_width: Thermal width (optional)
        thermal_bridge_width: Thermal bridge width (optional)
        thermal_gap: Thermal gap (optional)
        options: Custom pad options (optional)
        primitives: Custom pad primitives (optional)
        teardrops: Teardrop settings (optional)
    """

    __token_name__: ClassVar[str] = "pad"

    number: str = field(default="", metadata={"description": "Pad number or name"})
    type: PadType = field(
        default=PadType.THRU_HOLE,
        metadata={"description": "Pad type"},
    )
    shape: PadShape = field(
        default=PadShape.CIRCLE,
        metadata={"description": "Pad shape"},
    )
    at: At = field(
        default_factory=lambda: At(),
        metadata={"description": "Position and rotation"},
    )
    size: Size = field(
        default_factory=lambda: Size(), metadata={"description": "Pad dimensions"}
    )
    layers: Layers = field(
        default_factory=lambda: Layers(),
        metadata={"description": "Layer list"},
    )
    drill: Optional[Drill] = field(
        default=None, metadata={"description": "Drill definition", "required": False}
    )
    property: Optional[str] = field(
        default=None, metadata={"description": "Pad property", "required": False}
    )
    locked: TokenFlag = field(
        default_factory=lambda: TokenFlag("locked"),
        metadata={"description": "Whether pad is locked", "required": False},
    )
    remove_unused_layer: TokenFlag = field(
        default_factory=lambda: TokenFlag("remove_unused_layer"),
        metadata={"description": "Remove unused layers flag", "required": False},
    )
    remove_unused_layers: TokenFlag = field(
        default_factory=lambda: TokenFlag("remove_unused_layers"),
        metadata={
            "description": "Remove unused layers flag (newer format)",
            "required": False,
        },
    )
    keep_end_layers: TokenFlag = field(
        default_factory=lambda: TokenFlag("keep_end_layers"),
        metadata={"description": "Keep end layers flag", "required": False},
    )
    roundrect_rratio: NamedFloat = field(
        default_factory=lambda: NamedFloat("roundrect_rratio", 0.0),
        metadata={"description": "Round rectangle corner ratio", "required": False},
    )
    chamfer_ratio: Optional[float] = field(
        default=None, metadata={"description": "Chamfer ratio", "required": False}
    )
    chamfer: Optional[List[str]] = field(
        default_factory=list,
        metadata={"description": "Chamfer corners", "required": False},
    )
    net: Optional[Net] = field(
        default=None, metadata={"description": "Net connection", "required": False}
    )
    uuid: Optional[Uuid] = field(
        default=None, metadata={"description": "Unique identifier", "required": False}
    )
    pinfunction: Optional[str] = field(
        default=None, metadata={"description": "Pin function name", "required": False}
    )
    pintype: Optional[str] = field(
        default=None, metadata={"description": "Pin type", "required": False}
    )
    die_length: Optional[float] = field(
        default=None, metadata={"description": "Die length", "required": False}
    )
    solder_mask_margin: Optional[float] = field(
        default=None, metadata={"description": "Solder mask margin", "required": False}
    )
    solder_paste_margin: Optional[float] = field(
        default=None, metadata={"description": "Solder paste margin", "required": False}
    )
    solder_paste_margin_ratio: Optional[float] = field(
        default=None,
        metadata={"description": "Solder paste margin ratio", "required": False},
    )
    clearance: Optional[float] = field(
        default=None, metadata={"description": "Clearance value", "required": False}
    )
    zone_connect: Optional[ZoneConnection] = field(
        default=None,
        metadata={"description": "Zone connection type", "required": False},
    )
    thermal_width: Optional[float] = field(
        default=None, metadata={"description": "Thermal width", "required": False}
    )
    thermal_bridge_width: NamedFloat = field(
        default_factory=lambda: NamedFloat("thermal_bridge_width", 0.0),
        metadata={"description": "Thermal bridge width", "required": False},
    )
    thermal_gap: Optional[float] = field(
        default=None, metadata={"description": "Thermal gap", "required": False}
    )
    options: Optional[Options] = field(
        default=None, metadata={"description": "Custom pad options", "required": False}
    )
    primitives: Optional[Primitives] = field(
        default=None,
        metadata={"description": "Custom pad primitives", "required": False},
    )
    teardrops: Optional[Teardrops] = field(
        default=None,
        metadata={"description": "Teardrop settings", "required": False},
    )


@dataclass
class Pads(NamedObject):
    """Container for multiple pads.

    The 'pads' token defines a collection of pads in the format::

        (pads
            (pad ...)
            ...
        )

    Args:
        pads: List of pads
    """

    __token_name__: ClassVar[str] = "pads"

    pads: List[Pad] = field(
        default_factory=list, metadata={"description": "List of pads"}
    )
