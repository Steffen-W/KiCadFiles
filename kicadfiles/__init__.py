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
    GrText,
    GrTextBox,
    LeaderLength,
    OverrideValue,
    Precision,
    RenderCache,
    SuppressZeros,
    UnitsFormat,
)

# Base element
from .base_element import KiCadObject, OptionalFlag
from .base_element import ParseStrictness
from .base_element import ParseStrictness as ParseMode
from .base_element import TokenPreference

# Base types
from .base_types import (
    Anchor,
    Angle,
    At,
    Center,
    Clearance,
    Color,
    Diameter,
    Effects,
    End,
    Fill,
    Font,
    Height,
    Id,
    Justify,
    Layer,
    Layers,
    Linewidth,
    Name,
    Offset,
    Pos,
    Property,
    Pts,
    Radius,
    Rotate,
    Size,
    Start,
    Stroke,
    Style,
    Text,
    Thickness,
    Title,
    Tstamp,
    Type,
    Units,
    Uuid,
    Width,
    Xy,
    Xyz,
)

# Board layout
from .board_layout import (
    General,
    KicadPcb,
    NetName,
    Nets,
    Orientation,
    Path,
    PrivateLayers,
    Segment,
    Setup,
    Tracks,
    Via,
    Vias,
    ViaSize,
)

# Design rules
from .design_rules import (
    ConstraintMax,
    ConstraintMin,
    ConstraintOpt,
    DesignRule,
    DesignRuleCondition,
    DesignRuleConstraint,
    DesignRuleLayer,
    DesignRulePriority,
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
    AutoplaceCost90,
    AutoplaceCost180,
    Footprint,
    Footprints,
    Model,
    NetTiePadGroups,
    OnBoard,
    SolderMaskMargin,
    SolderPasteMargin,
    SolderPasteMarginRatio,
    Tags,
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
    ChamferRatio,
    DieLength,
    Drill,
    Free,
    Net,
    Options,
    Pad,
    Pads,
    Primitives,
    RoundrectRratio,
    Shape,
    SolderPasteRatio,
    ThermalBridgeWidth,
    ThermalGap,
    ThermalWidth,
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
    EmbeddedFonts,
    GlobalLabel,
    Incrx,
    Incry,
    Junction,
    KicadSch,
    Label,
    Length,
    NoConnect,
    Project,
    Repeat,
    Sheet,
    SheetInstance,
    SheetInstances,
    Wire,
)

# Symbol library
from .symbol_library import (
    ExcludeFromSim,
    Extends,
    FieldsAutoplaced,
    InBom,
    Instances,
    LibSymbols,
    Number,
    Pin,
    Pinfunction,
    PinNames,
    PinNumbers,
    Pintype,
    Prefix,
    Symbol,
    UnitName,
)

# Text and document elements
from .text_and_documents import (
    Bitmap,
    BottomMargin,
    Comment,
    Company,
    Data,
    Date,
    Descr,
    Generator,
    GeneratorVersion,
    Group,
    Image,
    KicadWks,
    LeftMargin,
    Members,
    Page,
    Paper,
    Pngdata,
    Rev,
    RightMargin,
    Scale,
    Suffix,
    Tbtext,
    Tedit,
    Textlinewidth,
    Textsize,
    TitleBlock,
    TopMargin,
    Version,
    WksLine,
    WksLinewidth,
    WksMargin,
    WksRect,
    WksSetup,
    WksTbText,
    WksTextlinewidth,
    WksTextsize,
)

# Zone system
from .zone_system import (
    ConnectPads,
    Copperpour,
    EpsilonR,
    FilledAreasThickness,
    FilledPolygon,
    FilledSegments,
    FillSegments,
    Hatch,
    HatchBorderAlgorithm,
    HatchGap,
    HatchMinHoleArea,
    HatchOrientation,
    HatchSmoothingLevel,
    HatchSmoothingValue,
    HatchThickness,
    IslandAreaMin,
    IslandRemovalMode,
    KeepEndLayers,
    Keepout,
    LossTangent,
    Material,
    MinThickness,
    Mode,
    Priority,
    RemoveUnusedLayer,
    RemoveUnusedLayers,
    Smoothing,
    Zone,
)

__all__ = [
    # Base
    "KiCadObject",
    "ParseMode",
    "ParseStrictness",
    "OptionalFlag",
    "TokenPreference",
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
    "Angle",
    "At",
    "Center",
    "Clearance",
    "Color",
    "Diameter",
    "Effects",
    "End",
    "Fill",
    "Font",
    "Height",
    "Id",
    "Justify",
    "Layer",
    "Layers",
    "Linewidth",
    "Name",
    "Offset",
    "Pos",
    "Property",
    "Pts",
    "Radius",
    "Rotate",
    "Size",
    "Start",
    "Stroke",
    "Style",
    "Text",
    "Thickness",
    "Title",
    "Tstamp",
    "Type",
    "Units",
    "Uuid",
    "Width",
    "Xy",
    "Xyz",
    # Design rules
    "ConstraintMax",
    "ConstraintMin",
    "ConstraintOpt",
    "DesignRule",
    "DesignRuleCondition",
    "DesignRuleConstraint",
    "DesignRuleLayer",
    "DesignRulePriority",
    "DesignRuleSeverity",
    "KiCadDesignRules",
    # Text and documents
    "Bitmap",
    "BottomMargin",
    "Comment",
    "Company",
    "Data",
    "Date",
    "Descr",
    "Generator",
    "GeneratorVersion",
    "Group",
    "Image",
    "KicadWks",
    "LeftMargin",
    "Members",
    "Page",
    "Paper",
    "Pngdata",
    "Rev",
    "RightMargin",
    "Scale",
    "Suffix",
    "Tbtext",
    "Tedit",
    "Textlinewidth",
    "Textsize",
    "TitleBlock",
    "TopMargin",
    "Version",
    "WksLine",
    "WksLinewidth",
    "WksMargin",
    "WksRect",
    "WksSetup",
    "WksTbText",
    "WksTextlinewidth",
    "WksTextsize",
    # Pad and drill
    "Chamfer",
    "ChamferRatio",
    "DieLength",
    "Drill",
    "Free",
    "Net",
    "Options",
    "Pad",
    "Pads",
    "Primitives",
    "RoundrectRratio",
    "Shape",
    "SolderPasteRatio",
    "ThermalBridgeWidth",
    "ThermalGap",
    "ThermalWidth",
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
    "GrText",
    "GrTextBox",
    "LeaderLength",
    "OverrideValue",
    "Precision",
    "RenderCache",
    "SuppressZeros",
    "UnitsFormat",
    # Symbol library
    "ExcludeFromSim",
    "Extends",
    "FieldsAutoplaced",
    "InBom",
    "Instances",
    "LibSymbols",
    "Number",
    "Pin",
    "Pinfunction",
    "PinNames",
    "PinNumbers",
    "Pintype",
    "Prefix",
    "Symbol",
    "UnitName",
    # Footprint library
    "Attr",
    "AutoplaceCost180",
    "AutoplaceCost90",
    "Footprint",
    "Footprints",
    "Model",
    "NetTiePadGroups",
    "OnBoard",
    "SolderMaskMargin",
    "SolderPasteMargin",
    "SolderPasteMarginRatio",
    "Tags",
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
    "EpsilonR",
    "FillSegments",
    "FilledAreasThickness",
    "FilledPolygon",
    "FilledSegments",
    "Hatch",
    "HatchBorderAlgorithm",
    "HatchGap",
    "HatchMinHoleArea",
    "HatchOrientation",
    "HatchSmoothingLevel",
    "HatchSmoothingValue",
    "HatchThickness",
    "IslandAreaMin",
    "IslandRemovalMode",
    "KeepEndLayers",
    "Keepout",
    "LossTangent",
    "Material",
    "MinThickness",
    "Mode",
    "Priority",
    "RemoveUnusedLayer",
    "RemoveUnusedLayers",
    "Smoothing",
    "Zone",
    # Board layout
    "General",
    "KicadPcb",
    "NetName",
    "Nets",
    "Orientation",
    "Path",
    "PrivateLayers",
    "Segment",
    "Setup",
    "Tracks",
    "Via",
    "ViaSize",
    "Vias",
    # Schematic system
    "Bus",
    "BusEntry",
    "EmbeddedFonts",
    "GlobalLabel",
    "Incrx",
    "Incry",
    "Junction",
    "KicadSch",
    "Label",
    "Length",
    "NoConnect",
    "Project",
    "Repeat",
    "Sheet",
    "SheetInstance",
    "SheetInstances",
    "Wire",
]
