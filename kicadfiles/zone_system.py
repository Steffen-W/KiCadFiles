"""Zone system elements for KiCad S-expressions - copper zones and keepout areas."""

from dataclasses import dataclass, field
from typing import Any, List, Optional

from .base_element import KiCadObject
from .base_types import Angle, Clearance, Fill, Pts, Uuid
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
    clearance: Clearance = field(
        default_factory=lambda: Clearance(),
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
class EpsilonR(KiCadObject):
    """Dielectric constant definition token.

    The 'epsilon_r' token defines the relative dielectric constant in the format::

        (epsilon_r VALUE)

    Args:
        value: Relative dielectric constant
    """

    __token_name__ = "epsilon_r"

    value: float = field(
        default=4.5, metadata={"description": "Relative dielectric constant"}
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
class HatchBorderAlgorithm(KiCadObject):
    """Hatch border algorithm definition token.

    The 'hatch_border_algorithm' token defines the border thickness algorithm in the format::

        (hatch_border_algorithm TYPE)

    Args:
        algorithm: Border algorithm type (0=zone thickness, 1=hatch thickness)
    """

    __token_name__ = "hatch_border_algorithm"

    algorithm: int = field(
        default=0,
        metadata={
            "description": "Border algorithm type (0=zone thickness, 1=hatch thickness)"
        },
    )


@dataclass
class HatchGap(KiCadObject):
    """Hatch gap definition token.

    The 'hatch_gap' token defines the gap between hatch lines in the format::

        (hatch_gap GAP)

    Args:
        gap: Gap distance between hatch lines
    """

    __token_name__ = "hatch_gap"

    gap: float = field(
        default=0.5, metadata={"description": "Gap distance between hatch lines"}
    )


@dataclass
class HatchMinHoleArea(KiCadObject):
    """Hatch minimum hole area definition token.

    The 'hatch_min_hole_area' token defines the minimum area for hatch holes in the format::

        (hatch_min_hole_area AREA)

    Args:
        area: Minimum hole area
    """

    __token_name__ = "hatch_min_hole_area"

    area: float = field(default=0.0, metadata={"description": "Minimum hole area"})


@dataclass
class HatchOrientation(KiCadObject):
    """Hatch orientation definition token.

    The 'hatch_orientation' token defines the angle for hatch lines in the format::

        (hatch_orientation ANGLE)

    Args:
        angle: Hatch line angle in degrees
    """

    __token_name__ = "hatch_orientation"

    angle: Angle = field(
        default_factory=lambda: Angle(),
        metadata={"description": "Hatch line angle in degrees"},
    )


@dataclass
class HatchSmoothingLevel(KiCadObject):
    """Hatch smoothing level definition token.

    The 'hatch_smoothing_level' token defines how hatch outlines are smoothed in the format::

        (hatch_smoothing_level LEVEL)

    Args:
        level: Smoothing level (0=none, 1=fillet, 2=arc min, 3=arc max)
    """

    __token_name__ = "hatch_smoothing_level"

    level: int = field(
        default=0,
        metadata={
            "description": "Smoothing level (0=none, 1=fillet, 2=arc min, 3=arc max)"
        },
    )


@dataclass
class HatchSmoothingValue(KiCadObject):
    """Hatch smoothing value definition token.

    The 'hatch_smoothing_value' token defines the smoothing ratio in the format::

        (hatch_smoothing_value VALUE)

    Args:
        value: Smoothing ratio between hole and chamfer/fillet size
    """

    __token_name__ = "hatch_smoothing_value"

    value: float = field(
        default=0.1,
        metadata={
            "description": "Smoothing ratio between hole and chamfer/fillet size"
        },
    )


@dataclass
class HatchThickness(KiCadObject):
    """Hatch thickness definition token.

    The 'hatch_thickness' token defines the thickness for hatched fills in the format::

        (hatch_thickness THICKNESS)

    Args:
        thickness: Hatch line thickness
    """

    __token_name__ = "hatch_thickness"

    thickness: float = field(
        default=0.1, metadata={"description": "Hatch line thickness"}
    )


@dataclass
class IslandAreaMin(KiCadObject):
    """Island minimum area definition token.

    The 'island_area_min' token defines the minimum allowable zone island area in the format::

        (island_area_min AREA)

    Args:
        area: Minimum island area
    """

    __token_name__ = "island_area_min"

    area: float = field(default=10.0, metadata={"description": "Minimum island area"})


@dataclass
class IslandRemovalMode(KiCadObject):
    """Island removal mode definition token.

    The 'island_removal_mode' token defines how islands are removed in the format::

        (island_removal_mode MODE)

    Args:
        mode: Island removal mode (0=always, 1=never, 2=minimum area)
    """

    __token_name__ = "island_removal_mode"

    mode: int = field(
        default=0,
        metadata={
            "description": "Island removal mode (0=always, 1=never, 2=minimum area)"
        },
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
class LossTangent(KiCadObject):
    """Loss tangent definition token.

    The 'loss_tangent' token defines the dielectric loss tangent in the format::

        (loss_tangent VALUE)

    Args:
        value: Dielectric loss tangent value
    """

    __token_name__ = "loss_tangent"

    value: float = field(
        default=0.02, metadata={"description": "Dielectric loss tangent value"}
    )


@dataclass
class Material(KiCadObject):
    """Material definition token.

    The 'material' token defines the material properties in the format::

        (material "MATERIAL_NAME")

    Args:
        name: Material name
    """

    __token_name__ = "material"

    name: str = field(default="", metadata={"description": "Material name"})


@dataclass
class MinThickness(KiCadObject):
    """Minimum thickness definition token.

    The 'min_thickness' token defines the minimum fill thickness in the format::

        (min_thickness THICKNESS)

    Args:
        thickness: Minimum thickness value
    """

    __token_name__ = "min_thickness"

    thickness: float = field(
        default=0.1, metadata={"description": "Minimum thickness value"}
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
class Priority(KiCadObject):
    """Zone priority definition token.

    The 'priority' token defines the zone priority in the format::

        (priority PRIORITY_VALUE)

    Args:
        priority: Zone priority value
    """

    __token_name__ = "priority"

    priority: int = field(default=0, metadata={"description": "Zone priority value"})


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
    filled_areas_thickness: Optional[bool] = field(
        default=None,
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
