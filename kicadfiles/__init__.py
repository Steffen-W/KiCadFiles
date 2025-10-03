"""KiCadFiles - A comprehensive Python library for parsing and manipulating KiCad file formats.

This library provides a complete set of dataclasses representing all KiCad
S-expression tokens. Each class corresponds exactly to one S-expression token
and follows a consistent structure for parsing and serialization.

The classes are organized into logical modules based on dependencies:
- base_element: Base KiCadObject class with simplified strictness modes
- enums: Common enumeration types for type safety
- base_types: Fundamental types with no dependencies (37 classes)
- text_and_documents: Text and document elements (35 classes)
- pad_and_drill: Pad and drill elements (17 classes)
- primitive_graphics: Basic graphics primitives (8 classes)
- advanced_graphics: Complex graphics objects (20 classes)
- symbol_library: Symbol management (15 classes)
- footprint_library: Footprint management (12 classes)
- zone_system: Zone and copper filling (28 classes)
- board_layout: PCB board design (15 classes)
- schematic_system: Schematic drawing (17 classes)
- design_rules: Design rule check definitions (10 classes)
- project_settings: JSON project settings (14 classes)

Total: 241 classes representing all KiCad S-expression and JSON tokens.

Key Features:
- Simplified parser strictness modes: STRICT, FAILSAFE, SILENT
- Comprehensive type safety with Python type hints
- Round-trip parsing: parse KiCad files and convert back to S-expressions
- Zero external dependencies
- Extensive test coverage

Usage:
    from kicadfiles import At, Layer, Footprint, ParseStrictness

    # Create objects using dataclass syntax
    position = At(x=10.0, y=20.0, angle=90.0)
    layer = Layer(name="F.Cu")

    # Parse from S-expression with different strictness levels
    at_obj = At.from_sexpr("(at 10.0 20.0 90.0)", ParseStrictness.STRICT)

    # Convert back to S-expression
    sexpr_str = at_obj.to_sexpr_str()
"""

# Version information
from .__version__ import __version__, __version_info__  # noqa: F401

# Advanced graphics
from .advanced_graphics import (
    Dimension,
    Format,
    FpArc,
    FpCircle,
    FpCurve,
    FpLine,
    FpPoly,
    FpRect,
    FpText,
    FpTextBox,
    GrArc,
    GrBbox,
    GrCircle,
    GrCurve,
    GrLine,
    GrPoly,
    GrRect,
    GrText,
    GrTextBox,
)

# Base element
from .base_element import (
    KiCadFloat,
    KiCadInt,
    KiCadObject,
    KiCadStr,
    OptionalFlag,
    OptionalSimpleFlag,
    ParseStrictness,
)

# Base types
from .base_types import (
    Anchor,
    At,
    AtXY,
    BoardLayers,
    Center,
    Color,
    Effects,
    End,
    Fill,
    Font,
    Justify,
    Layer,
    LayerDefinition,
    Layers,
    Offset,
    Pos,
    Property,
    Pts,
    Size,
    Start,
    Stroke,
    Text,
    Type,
    Uuid,
    Xy,
    Xyz,
)

# Board layout
from .board_layout import (
    BoardArc,
    KicadPcb,
    Nets,
    PcbPlotParams,
    PrivateLayers,
    Segment,
    Setup,
    Stackup,
    StackupLayer,
    Tenting,
    Tracks,
    Via,
    Vias,
)

# Design rules
from .design_rules import (
    DesignRule,
    DesignRuleConstraint,
    DesignRuleSeverity,
    KiCadDesignRules,
)

# Enums
from .enums import (
    ClearanceType,
    FillType,
    FootprintTextType,
    HatchStyle,
    JustifyHorizontal,
    JustifyVertical,
    LabelShape,
    LayerType,
    PadShape,
    PadType,
    PinElectricalType,
    PinGraphicStyle,
    SmoothingStyle,
    StrokeType,
    ViaType,
    ZoneConnection,
    ZoneFillMode,
    ZoneKeepoutSetting,
)

# Footprint library
from .footprint_library import (
    Attr,
    Footprint,
    Footprints,
    Model,
    NetTiePadGroups,
)

# Library tables
from .library_tables import (
    FpLibTable,
    LibraryEntry,
    SymLibTable,
)

# Pad and drill elements
from .pad_and_drill import (
    Chamfer,
    Drill,
    Net,
    Options,
    Pad,
    Pads,
    Primitives,
    Shape,
    ZoneConnect,
)

# Primitive graphics
from .primitive_graphics import (
    Arc,
    Bezier,
    Circle,
    Line,
    Polygon,
    Polyline,
    Rect,
    Rectangle,
)

# Project settings
from .project_settings import (
    BoardDefaults,
    BoardSettings,
    CvpcbSettings,
    DesignSettings,
    ERCSettings,
    IPC2581Settings,
    KicadProject,
    LibrarySettings,
    NetClass,
    NetSettings,
    PcbnewSettings,
    ProjectMeta,
    SchematicBOMSettings,
    SchematicSettings,
)

# Schematic system
from .schematic_system import (
    Bus,
    BusEntry,
    GlobalLabel,
    HierarchicalLabel,
    Junction,
    KicadSch,
    Label,
    NetclassFlag,
    NoConnect,
    Project,
    RuleArea,
    Sheet,
    SheetInstance,
    SheetInstances,
    Table,
    Wire,
)

# Symbol library
from .symbol_library import (
    Instances,
    KicadSymbolLib,
    LibSymbols,
    Number,
    Pin,
    PinName,
    PinNames,
    PinNumbers,
    Pintype,
    Symbol,
)

# Templates (convenience helpers)
from .templates import (
    KiCadTemplates,
)

# Text and document elements
from .text_and_documents import (
    Bitmap,
    Comment,
    Data,
    Group,
    Image,
    KicadWks,
    Members,
    Paper,
    Pngdata,
    Tbtext,
    Textsize,
    TitleBlock,
    WksLine,
    WksRect,
    WksSetup,
    WksTbText,
    WksTextsize,
)

# Zone system
from .zone_system import (
    ConnectPads,
    Copperpour,
    FilledPolygon,
    FilledSegments,
    FillSegments,
    Hatch,
    HatchOrientation,
    Keepout,
    Mode,
    Smoothing,
    Zone,
    ZoneFill,
)

# Grid helper constants
GRID = 1.27  # KiCad schematic default grid in mm (50 mil)

__all__ = [
    # Grid helpers
    "GRID",
    # Base
    "KiCadFloat",
    "KiCadInt",
    "KiCadObject",
    "KiCadStr",
    "ParseStrictness",
    "OptionalFlag",
    "OptionalSimpleFlag",
    # Enums
    "ClearanceType",
    "FillType",
    "FootprintTextType",
    "HatchStyle",
    "JustifyHorizontal",
    "JustifyVertical",
    "LabelShape",
    "LayerType",
    "PadShape",
    "PadType",
    "PinElectricalType",
    "PinGraphicStyle",
    "SmoothingStyle",
    "StrokeType",
    "ViaType",
    "ZoneConnection",
    "ZoneFillMode",
    "ZoneKeepoutSetting",
    # Base types
    "Anchor",
    "At",
    "AtXY",
    "BoardLayers",
    "Center",
    "Color",
    "Effects",
    "End",
    "Fill",
    "Font",
    "Justify",
    "Layer",
    "LayerDefinition",
    "Layers",
    "Offset",
    "Pos",
    "Property",
    "Pts",
    "Size",
    "Start",
    "Stroke",
    "Text",
    "Type",
    "Uuid",
    "Xy",
    "Xyz",
    # Design rules
    "DesignRule",
    "DesignRuleConstraint",
    "DesignRuleSeverity",
    "KiCadDesignRules",
    # Text and documents
    "Bitmap",
    "Comment",
    "Data",
    "Group",
    "Image",
    "KicadWks",
    "Members",
    "Paper",
    "Pngdata",
    "Tbtext",
    "Textsize",
    "TitleBlock",
    "WksLine",
    "WksRect",
    "WksSetup",
    "WksTbText",
    "WksTextsize",
    # Pad and drill
    "Chamfer",
    "Drill",
    "Net",
    "Options",
    "Pad",
    "Pads",
    "Primitives",
    "Shape",
    "ZoneConnect",
    # Primitive graphics
    "Arc",
    "Bezier",
    "Circle",
    "Line",
    "Polygon",
    "Polyline",
    "Rect",
    "Rectangle",
    # Advanced graphics
    "Dimension",
    "Format",
    "FpArc",
    "FpCircle",
    "FpCurve",
    "FpLine",
    "FpPoly",
    "FpRect",
    "FpText",
    "FpTextBox",
    "GrArc",
    "GrBbox",
    "GrCircle",
    "GrCurve",
    "GrLine",
    "GrPoly",
    "GrRect",
    "GrText",
    "GrTextBox",
    # Symbol library
    "Instances",
    "KicadSymbolLib",
    "LibSymbols",
    "PinName",
    "Number",
    "Pin",
    "PinNames",
    "PinNumbers",
    "Pintype",
    "Symbol",
    # Footprint library
    "Attr",
    "Footprint",
    "Footprints",
    "Model",
    "NetTiePadGroups",
    # Library tables
    "FpLibTable",
    "LibraryEntry",
    "SymLibTable",
    # Project settings
    "BoardDefaults",
    "BoardSettings",
    "CvpcbSettings",
    "DesignSettings",
    "ERCSettings",
    "IPC2581Settings",
    "KicadProject",
    "LibrarySettings",
    "NetClass",
    "NetSettings",
    "PcbnewSettings",
    "ProjectMeta",
    "SchematicBOMSettings",
    "SchematicSettings",
    # Zone system
    "ConnectPads",
    "Copperpour",
    "FillSegments",
    "FilledPolygon",
    "FilledSegments",
    "Hatch",
    "HatchOrientation",
    "Keepout",
    "Mode",
    "Smoothing",
    "Zone",
    "ZoneFill",
    # Board layout
    "BoardArc",
    "KicadPcb",
    "Nets",
    "PcbPlotParams",
    "PrivateLayers",
    "Segment",
    "Setup",
    "Stackup",
    "StackupLayer",
    "Tenting",
    "Tracks",
    "Via",
    "Vias",
    # Schematic system
    "Bus",
    "BusEntry",
    "GlobalLabel",
    "HierarchicalLabel",
    "Junction",
    "KicadSch",
    "Label",
    "NetclassFlag",
    "NoConnect",
    "Project",
    "RuleArea",
    "Sheet",
    "SheetInstance",
    "SheetInstances",
    "Table",
    "Wire",
    # Templates
    "KiCadTemplates",
]
