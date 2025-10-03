"""Zone system elements for KiCad S-expressions - copper zones and keepout areas."""

from dataclasses import dataclass, field
from typing import Any, List, Optional

from .base_element import KiCadFloat, KiCadObject, OptionalFlag
from .base_types import Fill, Pts, Uuid
from .enums import HatchStyle, SmoothingStyle, ZoneFillMode, ZoneKeepoutSetting
from .primitive_graphics import Polygon


@dataclass
class ConnectPads(KiCadObject):
    """Connect pads definition token for zones.

    The 'connect_pads' token defines pad connection type and clearance in the format::

        (connect_pads [CONNECTION_TYPE] (clearance CLEARANCE))

    Args:
        connection_type: Pad connection type (thru_hole_only | full | no) (optional)
        clearance: Pad clearance
    """

    __token_name__ = "connect_pads"

    connection_type: Optional[str] = field(
        default=None,
        metadata={
            "description": "Pad connection type (thru_hole_only | full | no)",
            "required": False,
        },
    )
    clearance: KiCadFloat = field(
        default_factory=lambda: KiCadFloat("clearance", 0.0),
        metadata={"description": "Pad clearance"},
    )


@dataclass
class Copperpour(KiCadObject):
    """Copper pour definition token.

    The 'copperpour' token defines copper pour properties in the format::

        (copperpour VALUE)

    where VALUE can be: not_allowed, allowed

    Args:
        value: Copper pour setting
    """

    __token_name__ = "copperpour"

    value: ZoneKeepoutSetting = field(
        default=ZoneKeepoutSetting.NOT_ALLOWED,
        metadata={"description": "Copper pour setting"},
    )


@dataclass
class FillSegments(KiCadObject):
    """Fill segments definition token.

    The 'fill_segments' token defines zone fill segments in the format::

        (fill_segments ...)

    Args:
        segments: List of fill segments
    """

    __token_name__ = "fill_segments"

    segments: List[Any] = field(
        default_factory=list, metadata={"description": "List of fill segments"}
    )


@dataclass
class FilledPolygon(KiCadObject):
    """Filled polygon definition token.

    The 'filled_polygon' token defines the polygons used to fill the zone in the format::

        (filled_polygon
            (layer LAYER_DEFINITION)
            COORDINATE_POINT_LIST
        )

    Args:
        layer: Layer the zone fill resides on
        pts: List of polygon X/Y coordinates used to fill the zone
    """

    __token_name__ = "filled_polygon"

    layer: str = field(
        default="", metadata={"description": "Layer the zone fill resides on"}
    )
    pts: Pts = field(
        default_factory=lambda: Pts(),
        metadata={
            "description": "List of polygon X/Y coordinates used to fill the zone"
        },
    )


@dataclass
class FilledSegments(KiCadObject):
    """Filled segments definition token.

    The 'filled_segments' token defines segments used to fill the zone in the format::

        (fill_segments
            (layer LAYER_DEFINITION)
            COORDINATED_POINT_LIST
        )

    Args:
        layer: Layer the zone fill resides on
        segments: List of X and Y coordinates of segments used to fill the zone
    """

    __token_name__ = "filled_segments"

    layer: str = field(
        default="", metadata={"description": "Layer the zone fill resides on"}
    )
    segments: List[Pts] = field(
        default_factory=list,
        metadata={
            "description": "List of X and Y coordinates of segments used to fill the zone"
        },
    )


@dataclass
class Hatch(KiCadObject):
    """Zone hatch display definition token.

    The 'hatch' token defines zone outline display style and pitch in the format::

        (hatch STYLE PITCH)

    Args:
        style: Hatch display style
        pitch: Hatch pitch distance
    """

    __token_name__ = "hatch"

    style: HatchStyle = field(
        default=HatchStyle.EDGE,
        metadata={"description": "Hatch display style"},
    )
    pitch: float = field(default=0.5, metadata={"description": "Hatch pitch distance"})


@dataclass
class HatchOrientation(KiCadObject):
    """Hatch orientation definition token.

    The 'hatch_orientation' token defines the angle for hatch lines in the format::

        (hatch_orientation ANGLE)

    Args:
        angle: Hatch line angle in degrees
    """

    __token_name__ = "hatch_orientation"

    angle: KiCadFloat = field(
        default_factory=lambda: KiCadFloat("angle", 0.0),
        metadata={"description": "Hatch line angle in degrees"},
    )


# Zone Fill Elements


@dataclass
class Keepout(KiCadObject):
    """Keepout zone definition token.

    The 'keepout' token defines which objects should be kept out of the zone in the format::

        (keepout
            (tracks KEEPOUT)
            (vias KEEPOUT)
            (pads KEEPOUT)
            (copperpour KEEPOUT)
            (footprints KEEPOUT)
        )

    Args:
        tracks: Whether tracks should be excluded (allowed | not_allowed)
        vias: Whether vias should be excluded (allowed | not_allowed)
        pads: Whether pads should be excluded (allowed | not_allowed)
        copperpour: Whether copper pours should be excluded (allowed | not_allowed)
        footprints: Whether footprints should be excluded (allowed | not_allowed)
    """

    __token_name__ = "keepout"

    tracks: ZoneKeepoutSetting = field(
        default=ZoneKeepoutSetting.NOT_ALLOWED,
        metadata={
            "description": "Whether tracks should be excluded (allowed | not_allowed)"
        },
    )
    vias: ZoneKeepoutSetting = field(
        default=ZoneKeepoutSetting.NOT_ALLOWED,
        metadata={
            "description": "Whether vias should be excluded (allowed | not_allowed)"
        },
    )
    pads: ZoneKeepoutSetting = field(
        default=ZoneKeepoutSetting.NOT_ALLOWED,
        metadata={
            "description": "Whether pads should be excluded (allowed | not_allowed)"
        },
    )
    copperpour: ZoneKeepoutSetting = field(
        default=ZoneKeepoutSetting.NOT_ALLOWED,
        metadata={
            "description": "Whether copper pours should be excluded (allowed | not_allowed)"
        },
    )
    footprints: ZoneKeepoutSetting = field(
        default=ZoneKeepoutSetting.NOT_ALLOWED,
        metadata={
            "description": "Whether footprints should be excluded (allowed | not_allowed)"
        },
    )


@dataclass
class Mode(KiCadObject):
    """Fill mode definition token.

    The 'mode' token defines the zone fill mode in the format::

        (mode MODE)

    Args:
        mode: Fill mode
    """

    __token_name__ = "mode"

    mode: ZoneFillMode = field(
        default=ZoneFillMode.SOLID, metadata={"description": "Fill mode"}
    )


@dataclass
class Smoothing(KiCadObject):
    """Zone smoothing definition token.

    The 'smoothing' token defines corner smoothing style in the format::

        (smoothing STYLE)

    Args:
        style: Corner smoothing style
    """

    __token_name__ = "smoothing"

    style: SmoothingStyle = field(
        default=SmoothingStyle.NONE,
        metadata={"description": "Corner smoothing style"},
    )


@dataclass
class Zone(KiCadObject):
    """Zone definition token.

    The 'zone' token defines a zone on the board or footprint in the format::

        (zone
            (net NET_NUMBER)
            (net_name "NET_NAME")
            (layer LAYER_DEFINITION)
            (uuid UUID)
            [(name "NAME")]
            (hatch STYLE PITCH)
            [(priority PRIORITY)]
            (connect_pads [CONNECTION_TYPE] (clearance CLEARANCE))
            (min_thickness THICKNESS)
            [(filled_areas_thickness no)]
            [ZONE_KEEPOUT_SETTINGS]
            ZONE_FILL_SETTINGS
            (polygon COORDINATE_POINT_LIST)
            [ZONE_FILL_POLYGONS...]
            [ZONE_FILL_SEGMENTS...]
        )

    Args:
        hatch: Hatch settings
        connect_pads: Pad connection settings
        fill: Fill settings
        polygon: Zone outline polygon
        net: Net number
        net_name: Net name
        layer: Layer name
        uuid: Unique identifier
        min_thickness: Minimum thickness
        name: Zone name (optional)
        priority: Zone priority (optional)
        filled_areas_thickness: Filled areas thickness flag (optional)
        keepout: Keepout settings (optional)
        filled_polygons: List of fill polygons (optional)
        filled_segments: List of fill segments (optional)
    """

    __token_name__ = "zone"

    # Required fields (no defaults) first
    hatch: Hatch = field(
        default_factory=lambda: Hatch(), metadata={"description": "Hatch settings"}
    )
    connect_pads: "ConnectPads" = field(
        default_factory=lambda: ConnectPads(),
        metadata={"description": "Pad connection settings"},
    )
    fill: Fill = field(
        default_factory=lambda: Fill(), metadata={"description": "Fill settings"}
    )
    polygon: Polygon = field(
        default_factory=lambda: Polygon(),
        metadata={"description": "Zone outline polygon"},
    )

    # Fields with defaults second
    net: int = field(default=0, metadata={"description": "Net number"})
    net_name: str = field(default="", metadata={"description": "Net name"})
    layer: str = field(default="", metadata={"description": "Layer name"})
    uuid: Uuid = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )
    min_thickness: float = field(
        default=0.0, metadata={"description": "Minimum thickness"}
    )

    # Optional fields (defaults to None) last
    name: Optional[str] = field(
        default=None, metadata={"description": "Zone name", "required": False}
    )
    priority: Optional[int] = field(
        default=None, metadata={"description": "Zone priority", "required": False}
    )
    filled_areas_thickness: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("filled_areas_thickness"),
        metadata={"description": "Filled areas thickness flag", "required": False},
    )
    keepout: Optional[Keepout] = field(
        default=None, metadata={"description": "Keepout settings", "required": False}
    )
    filled_polygons: Optional[List[FilledPolygon]] = field(
        default_factory=list,
        metadata={"description": "List of fill polygons", "required": False},
    )
    filled_segments: Optional[List[FilledSegments]] = field(
        default_factory=list,
        metadata={"description": "List of fill segments", "required": False},
    )
