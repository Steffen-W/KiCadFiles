"""Pad and drill related elements for KiCad S-expressions."""

from dataclasses import dataclass, field
from typing import List, Optional, Union

from .advanced_graphics import GrArc, GrCircle, GrCurve, GrLine, GrPoly, GrRect
from .base_element import KiCadFloat, KiCadObject, KiCadStr, OptionalFlag
from .base_types import Anchor, AtXY, Layers, Offset, Size, Uuid
from .enums import PadShape, PadType, ZoneConnection


@dataclass
class CurvedEdges(KiCadObject):
    """Curved edges definition token for teardrops.

    The 'curved_edges' token defines whether edges are curved in the format::

        (curved_edges yes|no)

    Args:
        value: Whether edges are curved
    """

    __token_name__ = "curved_edges"

    value: bool = field(
        default=False, metadata={"description": "Whether edges are curved"}
    )


@dataclass
class Enabled(KiCadObject):
    """Enabled definition token for teardrops.

    The 'enabled' token defines whether teardrops are enabled in the format::

        (enabled yes|no)

    Args:
        value: Whether teardrops are enabled
    """

    __token_name__ = "enabled"

    value: bool = field(
        default=True, metadata={"description": "Whether teardrops are enabled"}
    )


@dataclass
class AllowTwoSegments(KiCadObject):
    """Allow two segments definition token for teardrops.

    The 'allow_two_segments' token defines whether two segments are allowed in the format::

        (allow_two_segments yes|no)

    Args:
        value: Whether two segments are allowed
    """

    __token_name__ = "allow_two_segments"

    value: bool = field(
        default=True, metadata={"description": "Whether two segments are allowed"}
    )


@dataclass
class PreferZoneConnections(KiCadObject):
    """Prefer zone connections definition token for teardrops.

    The 'prefer_zone_connections' token defines whether zone connections are preferred in the format::

        (prefer_zone_connections yes|no)

    Args:
        value: Whether zone connections are preferred
    """

    __token_name__ = "prefer_zone_connections"

    value: bool = field(
        default=True, metadata={"description": "Whether zone connections are preferred"}
    )


@dataclass
class Teardrops(KiCadObject):
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
        curved_edges: Curved edges setting
        filter_ratio: Filter ratio setting
        enabled: Enabled setting
        allow_two_segments: Allow two segments setting
        prefer_zone_connections: Prefer zone connections setting
    """

    __token_name__ = "teardrops"

    best_length_ratio: KiCadFloat = field(
        default_factory=lambda: KiCadFloat("best_length_ratio", 0.0),
        metadata={"description": "Best length ratio setting"},
    )
    max_length: KiCadFloat = field(
        default_factory=lambda: KiCadFloat("max_length", 0.0),
        metadata={"description": "Maximum length setting"},
    )
    best_width_ratio: KiCadFloat = field(
        default_factory=lambda: KiCadFloat("best_width_ratio", 0.0),
        metadata={"description": "Best width ratio setting"},
    )
    max_width: KiCadFloat = field(
        default_factory=lambda: KiCadFloat("max_width", 0.0),
        metadata={"description": "Maximum width setting"},
    )
    curved_edges: CurvedEdges = field(
        default_factory=lambda: CurvedEdges(),
        metadata={"description": "Curved edges setting"},
    )
    filter_ratio: KiCadFloat = field(
        default_factory=lambda: KiCadFloat("filter_ratio", 0.0),
        metadata={"description": "Filter ratio setting"},
    )
    enabled: Enabled = field(
        default_factory=lambda: Enabled(),
        metadata={"description": "Enabled setting"},
    )
    allow_two_segments: AllowTwoSegments = field(
        default_factory=lambda: AllowTwoSegments(),
        metadata={"description": "Allow two segments setting"},
    )
    prefer_zone_connections: PreferZoneConnections = field(
        default_factory=lambda: PreferZoneConnections(),
        metadata={"description": "Prefer zone connections setting"},
    )


@dataclass
class Chamfer(KiCadObject):
    """Chamfer corner definition token for pads.

    The 'chamfer' token defines which corners of a rectangular pad get chamfered in the format::

        (chamfer CORNER_LIST)

    Valid chamfer corner attributes are top_left, top_right, bottom_left, and bottom_right.

    Args:
        corners: List of corners to chamfer
    """

    __token_name__ = "chamfer"

    corners: List[str] = field(
        default_factory=list, metadata={"description": "List of corners to chamfer"}
    )


@dataclass
class Options(KiCadObject):
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

    __token_name__ = "options"

    clearance: Optional[KiCadStr] = field(
        default_factory=lambda: KiCadStr("clearance", "", required=False),
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
class Shape(KiCadObject):
    """Pad shape definition token.

    The 'shape' token defines the shape of a pad in the format::

        (shape SHAPE_TYPE)

    Valid pad shapes are circle, rect, oval, trapezoid, roundrect, or custom.

    Args:
        shape: Pad shape type
    """

    __token_name__ = "shape"

    shape: PadShape = field(
        default=PadShape.CIRCLE, metadata={"description": "Pad shape type"}
    )


@dataclass
class ZoneConnect(KiCadObject):
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

    __token_name__ = "zone_connect"

    connection_type: ZoneConnection = field(
        default=ZoneConnection.INHERITED,
        metadata={"description": "Zone connection type"},
    )


@dataclass
class Net(KiCadObject):
    """Net connection definition token.

    The 'net' token defines the net connection in the format::

        (net ORDINAL "NET_NAME")

    Args:
        number: Net number
        name: Net name
    """

    __token_name__ = "net"

    number: int = field(default=0, metadata={"description": "Net number"})
    name: str = field(default="", metadata={"description": "Net name"})


@dataclass
class Drill(KiCadObject):
    """Drill definition token for pads.

    The 'drill' token defines the drill attributes for a footprint pad in the format::

        (drill
            [oval]
            DIAMETER
            [WIDTH]
            [(offset X Y)]
        )

    Args:
        diameter: Drill diameter
        oval: Whether the drill is oval instead of round (optional)
        width: Width of the slot for oval drills (optional)
        offset: Drill offset coordinates from the center of the pad (optional)
    """

    __token_name__ = "drill"

    diameter: float = field(default=0.0, metadata={"description": "Drill diameter"})
    oval: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("oval"),
        metadata={
            "description": "Whether the drill is oval instead of round",
            "required": False,
        },
    )
    width: Optional[float] = field(
        default=None,
        metadata={
            "description": "Width of the slot for oval drills",
            "required": False,
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
class Primitives(KiCadObject):
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

    __token_name__ = "primitives"

    elements: Optional[
        List[Union[GrArc, GrCircle, GrCurve, GrLine, GrPoly, GrRect]]
    ] = field(
        default_factory=list,
        metadata={
            "description": "List of primitive graphical elements",
            "required": False,
        },
    )
    width: Optional[KiCadFloat] = field(
        default_factory=lambda: KiCadFloat("width", 0.0),
        metadata={"description": "Line width of graphical items", "required": False},
    )
    fill: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("fill"),
        metadata={
            "description": "Whether geometry should be filled",
            "required": False,
        },
    )


@dataclass
class Pad(KiCadObject):
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
        thermal_gap: Thermal gap (optional)
        options: Custom pad options (optional)
        primitives: Custom pad primitives (optional)
        teardrops: Teardrop settings (optional)
    """

    __token_name__ = "pad"

    number: str = field(default="", metadata={"description": "Pad number or name"})
    type: PadType = field(
        default=PadType.THRU_HOLE,
        metadata={"description": "Pad type"},
    )
    shape: PadShape = field(
        default=PadShape.CIRCLE,
        metadata={"description": "Pad shape"},
    )
    at: AtXY = field(
        default_factory=lambda: AtXY(),
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
    locked: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("locked"),
        metadata={"description": "Whether pad is locked", "required": False},
    )
    remove_unused_layer: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("remove_unused_layer"),
        metadata={"description": "Remove unused layers flag", "required": False},
    )
    remove_unused_layers: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("remove_unused_layers"),
        metadata={
            "description": "Remove unused layers flag (newer format)",
            "required": False,
        },
    )
    keep_end_layers: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("keep_end_layers"),
        metadata={"description": "Keep end layers flag", "required": False},
    )
    roundrect_rratio: Optional[KiCadFloat] = field(
        default_factory=lambda: KiCadFloat("roundrect_rratio", 0.0, required=False),
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
class Pads(KiCadObject):
    """Container for multiple pads.

    The 'pads' token defines a collection of pads in the format::

        (pads
            (pad ...)
            ...
        )

    Args:
        pads: List of pads
    """

    __token_name__ = "pads"

    pads: List[Pad] = field(
        default_factory=list, metadata={"description": "List of pads"}
    )
