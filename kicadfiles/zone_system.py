"""Zone system elements for KiCad S-expressions - copper zones and keepout areas."""

from dataclasses import dataclass, field
from typing import Any, ClassVar, List, Optional

from .base_element import NamedFloat, NamedInt, NamedObject, NamedString, TokenFlag
from .base_types import Pts, Uuid
from .enums import HatchStyle, SmoothingStyle, ZoneFillMode, ZoneKeepoutSetting
from .primitive_graphics import Polygon


@dataclass
class ConnectPads(NamedObject):
    """Connect pads definition token for zones.

    The 'connect_pads' token defines pad connection type and clearance in the format::

        (connect_pads [CONNECTION_TYPE] (clearance CLEARANCE))

    Args:
        connection_type: Pad connection type (thru_hole_only | full | no) (optional)
        clearance: Pad clearance
    """

    __token_name__: ClassVar[str] = "connect_pads"

    connection_type: Optional[str] = field(
        default=None,
        metadata={
            "description": "Pad connection type (thru_hole_only | full | no)",
            "required": False,
        },
    )
    clearance: NamedFloat = field(
        default_factory=lambda: NamedFloat("clearance", 0.0),
        metadata={"description": "Pad clearance"},
    )


@dataclass
class Copperpour(NamedObject):
    """Copper pour definition token.

    The 'copperpour' token defines copper pour properties in the format::

        (copperpour VALUE)

    where VALUE can be: not_allowed, allowed

    Args:
        value: Copper pour setting
    """

    __token_name__: ClassVar[str] = "copperpour"

    value: ZoneKeepoutSetting = field(
        default=ZoneKeepoutSetting.NOT_ALLOWED,
        metadata={"description": "Copper pour setting"},
    )


@dataclass
class ZoneFill(NamedObject):
    """Zone fill definition token.

    The 'fill' token for zones defines zone fill properties in the format::

        (fill yes
            (thermal_gap GAP)
            (thermal_bridge_width WIDTH)
            (smoothing STYLE)
            (radius RADIUS)
        )

    Args:
        enabled: Whether fill is enabled (yes|no) (optional)
        thermal_gap: Thermal gap distance (optional)
        thermal_bridge_width: Thermal bridge width (optional)
        smoothing: Smoothing style (optional)
        radius: Smoothing radius (optional)
    """

    __token_name__: ClassVar[str] = "fill"

    enabled: Optional[str] = field(
        default=None,
        metadata={"description": "Whether fill is enabled (yes|no)", "required": False},
    )
    thermal_gap: NamedFloat = field(
        default_factory=lambda: NamedFloat("thermal_gap", 0.0),
        metadata={"description": "Thermal gap distance", "required": False},
    )
    thermal_bridge_width: NamedFloat = field(
        default_factory=lambda: NamedFloat("thermal_bridge_width", 0.0),
        metadata={"description": "Thermal bridge width", "required": False},
    )
    smoothing: NamedString = field(
        default_factory=lambda: NamedString("smoothing", ""),
        metadata={"description": "Smoothing style", "required": False},
    )
    radius: NamedFloat = field(
        default_factory=lambda: NamedFloat("radius", 0.0),
        metadata={"description": "Smoothing radius", "required": False},
    )


@dataclass
class FillSegments(NamedObject):
    """Fill segments definition token.

    The 'fill_segments' token defines zone fill segments in the format::

        (fill_segments ...)

    Args:
        segments: List of fill segments
    """

    __token_name__: ClassVar[str] = "fill_segments"

    segments: List[Any] = field(
        default_factory=list, metadata={"description": "List of fill segments"}
    )


@dataclass
class FilledPolygon(NamedObject):
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

    __token_name__: ClassVar[str] = "filled_polygon"

    layer: NamedString = field(
        default_factory=lambda: NamedString(token="layer", value=""),
        metadata={"description": "Layer the zone fill resides on"},
    )
    pts: Pts = field(
        default_factory=lambda: Pts(),
        metadata={
            "description": "List of polygon X/Y coordinates used to fill the zone"
        },
    )


@dataclass
class FilledSegments(NamedObject):
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

    __token_name__: ClassVar[str] = "filled_segments"

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
class Hatch(NamedObject):
    """Zone hatch display definition token.

    The 'hatch' token defines zone outline display style and pitch in the format::

        (hatch STYLE PITCH)

    Args:
        style: Hatch display style
        pitch: Hatch pitch distance
    """

    __token_name__: ClassVar[str] = "hatch"

    style: HatchStyle = field(
        default=HatchStyle.EDGE,
        metadata={"description": "Hatch display style"},
    )
    pitch: float = field(default=0.5, metadata={"description": "Hatch pitch distance"})


@dataclass
class HatchOrientation(NamedObject):
    """Hatch orientation definition token.

    The 'hatch_orientation' token defines the angle for hatch lines in the format::

        (hatch_orientation ANGLE)

    Args:
        angle: Hatch line angle in degrees
    """

    __token_name__: ClassVar[str] = "hatch_orientation"

    angle: NamedFloat = field(
        default_factory=lambda: NamedFloat("angle", 0.0),
        metadata={"description": "Hatch line angle in degrees"},
    )


# Zone Fill Elements


@dataclass
class Keepout(NamedObject):
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

    __token_name__: ClassVar[str] = "keepout"

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
class Mode(NamedObject):
    """Fill mode definition token.

    The 'mode' token defines the zone fill mode in the format::

        (mode MODE)

    Args:
        mode: Fill mode
    """

    __token_name__: ClassVar[str] = "mode"

    mode: ZoneFillMode = field(
        default=ZoneFillMode.SOLID, metadata={"description": "Fill mode"}
    )


@dataclass
class Smoothing(NamedObject):
    """Zone smoothing definition token.

    The 'smoothing' token defines corner smoothing style in the format::

        (smoothing STYLE)

    Args:
        style: Corner smoothing style
    """

    __token_name__: ClassVar[str] = "smoothing"

    style: SmoothingStyle = field(
        default=SmoothingStyle.NONE,
        metadata={"description": "Corner smoothing style"},
    )


@dataclass
class Zone(NamedObject):
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

    __token_name__: ClassVar[str] = "zone"

    # Required fields (no defaults) first
    hatch: Hatch = field(
        default_factory=lambda: Hatch(), metadata={"description": "Hatch settings"}
    )
    connect_pads: "ConnectPads" = field(
        default_factory=lambda: ConnectPads(),
        metadata={"description": "Pad connection settings"},
    )
    fill: ZoneFill = field(
        default_factory=lambda: ZoneFill(), metadata={"description": "Fill settings"}
    )
    polygon: Polygon = field(
        default_factory=lambda: Polygon(),
        metadata={"description": "Zone outline polygon"},
    )

    # Fields with defaults second
    net: NamedInt = field(
        default_factory=lambda: NamedInt(token="net", value=0),
        metadata={"description": "Net number"},
    )
    net_name: NamedString = field(
        default_factory=lambda: NamedString(token="net_name", value=""),
        metadata={"description": "Net name"},
    )
    layer: NamedString = field(
        default_factory=lambda: NamedString(token="layer", value=""),
        metadata={"description": "Layer name"},
    )
    uuid: Uuid = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )
    min_thickness: NamedFloat = field(
        default_factory=lambda: NamedFloat(token="min_thickness", value=0.0),
        metadata={"description": "Minimum thickness"},
    )

    # Optional fields (defaults to None) last
    name: Optional[str] = field(
        default=None, metadata={"description": "Zone name", "required": False}
    )
    priority: Optional[int] = field(
        default=None, metadata={"description": "Zone priority", "required": False}
    )
    filled_areas_thickness: TokenFlag = field(
        default_factory=lambda: TokenFlag("filled_areas_thickness"),
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
