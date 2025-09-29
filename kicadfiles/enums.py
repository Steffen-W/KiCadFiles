"""Common enumeration types for KiCad S-expressions."""

from enum import Enum


class PinElectricalType(Enum):
    """Pin electrical types for symbols."""

    INPUT = "input"
    OUTPUT = "output"
    BIDIRECTIONAL = "bidirectional"
    TRI_STATE = "tri_state"
    PASSIVE = "passive"
    FREE = "free"
    UNSPECIFIED = "unspecified"
    POWER_IN = "power_in"
    POWER_OUT = "power_out"
    OPEN_COLLECTOR = "open_collector"
    OPEN_EMITTER = "open_emitter"
    NO_CONNECT = "no_connect"


class PinGraphicStyle(Enum):
    """Pin graphical styles for symbols."""

    LINE = "line"
    INVERTED = "inverted"
    CLOCK = "clock"
    INVERTED_CLOCK = "inverted_clock"
    INPUT_LOW = "input_low"
    CLOCK_LOW = "clock_low"
    OUTPUT_LOW = "output_low"
    EDGE_CLOCK_HIGH = "edge_clock_high"
    NON_LOGIC = "non_logic"


class PadType(Enum):
    """Pad types for footprints."""

    THRU_HOLE = "thru_hole"
    SMD = "smd"
    CONNECT = "connect"
    NP_THRU_HOLE = "np_thru_hole"


class PadShape(Enum):
    """Pad shapes for footprints."""

    CIRCLE = "circle"
    RECT = "rect"
    OVAL = "oval"
    TRAPEZOID = "trapezoid"
    ROUNDRECT = "roundrect"
    CUSTOM = "custom"


class StrokeType(Enum):
    """Valid stroke line styles for graphics."""

    DASH = "dash"
    DASH_DOT = "dash_dot"
    DASH_DOT_DOT = "dash_dot_dot"
    DOT = "dot"
    DEFAULT = "default"
    SOLID = "solid"


class JustifyHorizontal(Enum):
    """Horizontal text justification."""

    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"


class JustifyVertical(Enum):
    """Vertical text justification."""

    TOP = "top"
    BOTTOM = "bottom"
    CENTER = "center"


class FillType(Enum):
    """Fill types for graphical objects."""

    NONE = "none"
    OUTLINE = "outline"
    BACKGROUND = "background"
    COLOR = "color"


class LabelShape(Enum):
    """Label and pin shapes for global labels, hierarchical labels, and sheet pins."""

    INPUT = "input"
    OUTPUT = "output"
    BIDIRECTIONAL = "bidirectional"
    TRI_STATE = "tri_state"
    PASSIVE = "passive"


class FootprintTextType(Enum):
    """Footprint text types."""

    REFERENCE = "reference"
    VALUE = "value"
    USER = "user"


class LayerType(Enum):
    """PCB layer types."""

    SIGNAL = "signal"
    POWER = "power"
    MIXED = "mixed"
    JUMPER = "jumper"
    USER = "user"


class ViaType(Enum):
    """Via types for PCB."""

    THROUGH = "through"
    BLIND_BURIED = "blind_buried"
    MICRO = "micro"


class ZoneConnection(Enum):
    """Zone connection types for pads."""

    INHERITED = 0
    SOLID = 1
    THERMAL_RELIEF = 2
    NONE = 3


class ZoneFillMode(Enum):
    """Zone fill modes."""

    SOLID = "solid"
    HATCHED = "hatched"


class ZoneKeepoutSetting(Enum):
    """Zone keepout settings."""

    ALLOWED = "allowed"
    NOT_ALLOWED = "not_allowed"


class HatchStyle(Enum):
    """Zone hatch display styles."""

    NONE = "none"
    EDGE = "edge"
    FULL = "full"


class SmoothingStyle(Enum):
    """Zone corner smoothing styles."""

    NONE = "none"
    CHAMFER = "chamfer"
    FILLET = "fillet"


class ClearanceType(Enum):
    """Custom pad clearance types."""

    OUTLINE = "outline"
    CONVEXHULL = "convexhull"


class SeverityLevel(Enum):
    """Design rule severity levels."""

    ERROR = "error"
    WARNING = "warning"
    IGNORE = "ignore"
    EXCLUSION = "exclusion"


class ConstraintType(Enum):
    """Design rule constraint types."""

    # Clearance Constraints
    CLEARANCE = "clearance"
    HOLE_CLEARANCE = "hole_clearance"
    EDGE_CLEARANCE = "edge_clearance"
    SILK_CLEARANCE = "silk_clearance"
    COURTYARD_CLEARANCE = "courtyard_clearance"
    HOLE_TO_HOLE = "hole_to_hole"
    PHYSICAL_CLEARANCE = "physical_clearance"
    PHYSICAL_HOLE_CLEARANCE = "physical_hole_clearance"
    CREEPAGE = "creepage"

    # Size Constraints
    TRACK_WIDTH = "track_width"
    VIA_DIAMETER = "via_diameter"
    HOLE_SIZE = "hole_size"
    ANNULAR_WIDTH = "annular_width"
    CONNECTION_WIDTH = "connection_width"

    # Thermal Constraints
    THERMAL_RELIEF_GAP = "thermal_relief_gap"
    THERMAL_SPOKE_WIDTH = "thermal_spoke_width"
    MIN_RESOLVED_SPOKES = "min_resolved_spokes"

    # Zone Constraints
    ZONE_CONNECTION = "zone_connection"

    # Disallow Constraints
    DISALLOW = "disallow"

    # Length Constraints
    LENGTH = "length"
    SKEW = "skew"

    # Differential Pair Constraints
    DIFF_PAIR_GAP = "diff_pair_gap"
    DIFF_PAIR_UNCOUPLED = "diff_pair_uncoupled"

    # Via Constraints
    VIA_DRILL = "via_drill"
    BLIND_VIA_RATIO = "blind_via_ratio"
    MICRO_VIA_DIAMETER = "micro_via_diameter"
    MICRO_VIA_DRILL = "micro_via_drill"

    # Text Constraints
    TEXT_HEIGHT = "text_height"
    TEXT_THICKNESS = "text_thickness"

    # Assertion Constraints
    ASSERTION = "assertion"
