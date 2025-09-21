"""Pad and drill related elements for KiCad S-expressions."""

from dataclasses import dataclass, field
from typing import Any, Optional

from .base_element import KiCadObject
from .base_types import Anchor, At, Clearance, Locked, Offset, Size, Width
from .enums import PadShape, PadType, ZoneConnection


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

    corners: list[str] = field(
        default_factory=list, metadata={"description": "List of corners to chamfer"}
    )


@dataclass
class ChamferRatio(KiCadObject):
    """Chamfer ratio definition token for pads.

    The 'chamfer_ratio' token defines the scaling factor of the pad to chamfer size in the format::

        (chamfer_ratio RATIO)

    The scaling factor is a number between 0 and 1.

    Args:
        ratio: Chamfer scaling factor between 0 and 1
    """

    __token_name__ = "chamfer_ratio"

    ratio: float = field(
        default=0.0, metadata={"description": "Chamfer scaling factor (0-1)"}
    )


@dataclass
class Free(KiCadObject):
    """Free via/pad connection definition token.

    The 'free' token indicates that a via is free to be moved outside its assigned net in the format::

        (free)

    This is a flag token with no parameters.

    Args:
        None - This is a flag token
    """

    __token_name__ = "free"


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
        clearance: Type of clearance used for custom pad (optional)
        anchor: Anchor pad shape of custom pad (optional)
    """

    __token_name__ = "options"

    clearance: Optional[Clearance] = field(
        default=None,
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
class RoundrectRratio(KiCadObject):
    """Round rectangle ratio definition token for pads.

    The 'roundrect_rratio' token defines the scaling factor of the pad to corner radius
    for rounded rectangular and chamfered corner rectangular pads in the format::

        (roundrect_rratio RATIO)

    The scaling factor is a number between 0 and 1.

    Args:
        ratio: Corner radius scaling factor between 0 and 1
    """

    __token_name__ = "roundrect_rratio"

    ratio: float = field(
        default=0.0, metadata={"description": "Corner radius scaling factor (0-1)"}
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
class SolderPasteRatio(KiCadObject):
    """Solder paste ratio definition token.

    The 'solder_paste_ratio' token defines the percentage of the pad size used to define
    the solder paste in the format::

        (solder_paste_ratio RATIO)

    Args:
        ratio: Percentage of pad size used for solder paste
    """

    __token_name__ = "solder_paste_ratio"

    ratio: float = field(
        default=0.0, metadata={"description": "Solder paste ratio value"}
    )


@dataclass
class ThermalBridgeWidth(KiCadObject):
    """Thermal bridge width definition token.

    The 'thermal_bridge_width' token defines the width of thermal bridges in the format::

        (thermal_bridge_width WIDTH)

    Args:
        width: Thermal bridge width value
    """

    __token_name__ = "thermal_bridge_width"

    width: float = field(default=0.0, metadata={"description": "Thermal bridge width"})


@dataclass
class ThermalGap(KiCadObject):
    """Thermal gap definition token.

    The 'thermal_gap' token defines the distance from the pad to the zone of thermal relief
    connections in the format::

        (thermal_gap DISTANCE)

    Args:
        distance: Distance from pad to zone for thermal relief
    """

    __token_name__ = "thermal_gap"

    distance: float = field(
        default=0.0, metadata={"description": "Thermal gap distance"}
    )


@dataclass
class ThermalWidth(KiCadObject):
    """Thermal width definition token.

    The 'thermal_width' token defines the thermal relief spoke width used for zone
    connections in the format::

        (thermal_width WIDTH)

    Args:
        width: Thermal relief spoke width
    """

    __token_name__ = "thermal_width"

    width: float = field(
        default=0.0, metadata={"description": "Thermal relief spoke width"}
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
        connection_type: Zone connection type (0-3)
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
        number: Net ordinal number (integer that defines net order)
        name: Net name string
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
        oval: Whether the drill is oval instead of round (optional)
        diameter: Drill diameter
        width: Width of the slot for oval drills (optional)
        offset: Drill offset coordinates from the center of the pad (optional)
    """

    __token_name__ = "drill"

    oval: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Whether the drill is oval instead of round",
            "required": False,
        },
    )
    diameter: float = field(default=0.0, metadata={"description": "Drill diameter"})
    width: Optional[float] = field(
        default=None,
        metadata={
            "description": "Optional width of the slot for oval drills",
            "required": False,
        },
    )
    offset: Optional[Offset] = field(
        default=None,
        metadata={
            "description": "Optional drill offset coordinates from the center of the pad",
            "required": False,
        },
    )


@dataclass
class Primitives(KiCadObject):
    """Custom pad primitives definition token.

    The 'primitives' token defines drawing objects for custom pads in the format::

        (primitives
            GRAPHIC_ITEMS...
            (width WIDTH)
            [(fill yes)]
        )

    Args:
        elements: List of graphical items (lines, rectangles, arcs, circles, curves, polygons, annotation bounding boxes)
        width: Line width of the graphical items
        fill: Whether the geometry should be filled (optional)
    """

    __token_name__ = "primitives"

    elements: list[Any] = field(
        default_factory=list, metadata={"description": "List of primitive elements"}
    )
    width: Width = field(
        default_factory=lambda: Width(),
        metadata={"description": "Line width of graphical items"},
    )
    fill: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Whether geometry should be filled",
            "required": False,
        },
    )


@dataclass
class DieLength(KiCadObject):
    """Die length definition token.

    The 'die_length' token defines the die length between the component pad and
    physical chip inside the component package in the format::

        (die_length LENGTH)

    Args:
        length: Die length value
    """

    __token_name__ = "die_length"

    length: float = field(default=0.0, metadata={"description": "Die length value"})


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
        type: Pad type (thru_hole | smd | connect | np_thru_hole)
        shape: Pad shape (circle | rect | oval | trapezoid | roundrect | custom)
        at: Position and rotation
        size: Pad dimensions
        layers: Layer list
        drill: Drill definition (optional)
        property: Pad property (optional)
        locked: Whether pad is locked (optional)
        remove_unused_layer: Remove unused layers flag (optional)
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
    at: At = field(
        default_factory=lambda: At(), metadata={"description": "Position and rotation"}
    )
    size: Size = field(
        default_factory=lambda: Size(), metadata={"description": "Pad dimensions"}
    )
    layers: list[str] = field(
        default_factory=list, metadata={"description": "Layer list"}
    )
    drill: Optional[Drill] = field(
        default=None, metadata={"description": "Drill definition", "required": False}
    )
    property: Optional[str] = field(
        default=None, metadata={"description": "Pad property", "required": False}
    )
    locked: Optional[Locked] = field(
        default=None,
        metadata={"description": "Whether pad is locked", "required": False},
    )
    remove_unused_layer: Optional[bool] = field(
        default=None,
        metadata={"description": "Remove unused layers flag", "required": False},
    )
    keep_end_layers: Optional[bool] = field(
        default=None,
        metadata={"description": "Keep end layers flag", "required": False},
    )
    roundrect_rratio: Optional[float] = field(
        default=None,
        metadata={"description": "Round rectangle corner ratio", "required": False},
    )
    chamfer_ratio: Optional[float] = field(
        default=None, metadata={"description": "Chamfer ratio", "required": False}
    )
    chamfer: Optional[list[str]] = field(
        default_factory=list,
        metadata={"description": "Chamfer corners", "required": False},
    )
    net: Optional[Net] = field(
        default=None, metadata={"description": "Net connection", "required": False}
    )
    uuid: Optional[str] = field(
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


@dataclass
class Pads(KiCadObject):
    """Container for multiple pads.

    The 'pads' token defines a collection of pads in the format::

        (pads
            (pad ...)
            ...
        )

    Args:
        pads: List of pad objects
    """

    __token_name__ = "pads"

    pads: list[Pad] = field(
        default_factory=list, metadata={"description": "List of pads"}
    )
