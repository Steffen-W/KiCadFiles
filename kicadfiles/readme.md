# KiCadFiles - Python Library for KiCad File Formats

A comprehensive Python library for parsing and manipulating KiCad file formats with complete S-expression and JSON token support.

## File Organization

### enums.py - Common Enumeration Types

```python
clearance_type         -> enums.ClearanceType
fill_type              -> enums.FillType
footprint_text_type    -> enums.FootprintTextType
hatch_style            -> enums.HatchStyle
justify_horizontal     -> enums.JustifyHorizontal
justify_vertical       -> enums.JustifyVertical
label_shape            -> enums.LabelShape
layer_type             -> enums.LayerType
pad_shape              -> enums.PadShape
pad_type               -> enums.PadType
pin_electrical_type    -> enums.PinElectricalType
pin_graphic_style      -> enums.PinGraphicStyle
smoothing_style        -> enums.SmoothingStyle
stroke_type            -> enums.StrokeType
via_type               -> enums.ViaType
zone_connection        -> enums.ZoneConnection
zone_fill_mode         -> enums.ZoneFillMode
zone_keepout_setting   -> enums.ZoneKeepoutSetting
```

### base_element.py - Base Classes

```python
kicad_object           -> base_element.KiCadObject
optional_flag          -> base_element.OptionalFlag
parse_mode             -> base_element.ParseMode
parse_strictness       -> base_element.ParseStrictness
token_preference       -> base_element.TokenPreference
```

### advanced_graphics.py - Complex Graphics Objects

```python
dimension              -> advanced_graphics.Dimension
format                 -> advanced_graphics.Format
fp_arc                 -> advanced_graphics.FpArc
fp_circle              -> advanced_graphics.FpCircle
fp_curve               -> advanced_graphics.FpCurve
fp_line                -> advanced_graphics.FpLine
fp_poly                -> advanced_graphics.FpPoly
fp_rect                -> advanced_graphics.FpRect
fp_text                -> advanced_graphics.FpText
fp_text_box            -> advanced_graphics.FpTextBox
gr_arc                 -> advanced_graphics.GrArc
gr_bbox                -> advanced_graphics.GrBbox
gr_circle              -> advanced_graphics.GrCircle
gr_text                -> advanced_graphics.GrText
gr_text_box            -> advanced_graphics.GrTextBox
leader_length          -> advanced_graphics.LeaderLength
override_value         -> advanced_graphics.OverrideValue
precision              -> advanced_graphics.Precision
render_cache           -> advanced_graphics.RenderCache
suppress_zeros         -> advanced_graphics.SuppressZeros
units_format           -> advanced_graphics.UnitsFormat
```

### base_types.py - Fundamental Types

```python
anchor                 -> base_types.Anchor
angle                  -> base_types.Angle
at                     -> base_types.At
center                 -> base_types.Center
clearance              -> base_types.Clearance
color                  -> base_types.Color
diameter               -> base_types.Diameter
effects                -> base_types.Effects
end                    -> base_types.End
fill                   -> base_types.Fill
font                   -> base_types.Font
height                 -> base_types.Height
id                     -> base_types.Id
justify                -> base_types.Justify
layer                  -> base_types.Layer
layers                 -> base_types.Layers
linewidth              -> base_types.Linewidth
name                   -> base_types.Name
offset                 -> base_types.Offset
pos                    -> base_types.Pos
property               -> base_types.Property
pts                    -> base_types.Pts
radius                 -> base_types.Radius
rotate                 -> base_types.Rotate
size                   -> base_types.Size
start                  -> base_types.Start
stroke                 -> base_types.Stroke
style                  -> base_types.Style
text                   -> base_types.Text
thickness              -> base_types.Thickness
title                  -> base_types.Title
tstamp                 -> base_types.Tstamp
type                   -> base_types.Type
units                  -> base_types.Units
uuid                   -> base_types.Uuid
width                  -> base_types.Width
xy                     -> base_types.Xy
xyz                    -> base_types.Xyz
```

### board_layout.py - PCB Board Design

```python
general                -> board_layout.General
kicad_pcb              -> board_layout.KicadPcb
net_name               -> board_layout.NetName
nets                   -> board_layout.Nets
orientation            -> board_layout.Orientation
path                   -> board_layout.Path
private_layers         -> board_layout.PrivateLayers
segment                -> board_layout.Segment
setup                  -> board_layout.Setup
tracks                 -> board_layout.Tracks
via                    -> board_layout.Via
via_size               -> board_layout.ViaSize
vias                   -> board_layout.Vias
```

### design_rules.py - Design Rule Check Definitions

```python
constraint_max         -> design_rules.ConstraintMax
constraint_min         -> design_rules.ConstraintMin
constraint_opt         -> design_rules.ConstraintOpt
design_rule            -> design_rules.DesignRule
design_rule_condition  -> design_rules.DesignRuleCondition
design_rule_constraint -> design_rules.DesignRuleConstraint
design_rule_layer      -> design_rules.DesignRuleLayer
design_rule_priority   -> design_rules.DesignRulePriority
design_rule_severity   -> design_rules.DesignRuleSeverity
kicad_design_rules     -> design_rules.KiCadDesignRules
```

### footprint_library.py - Footprint Management

```python
attr                   -> footprint_library.Attr
autoplace_cost180      -> footprint_library.AutoplaceCost180
autoplace_cost90       -> footprint_library.AutoplaceCost90
footprint              -> footprint_library.Footprint
footprints             -> footprint_library.Footprints
model                  -> footprint_library.Model
net_tie_pad_groups     -> footprint_library.NetTiePadGroups
on_board               -> footprint_library.OnBoard
solder_mask_margin     -> footprint_library.SolderMaskMargin
solder_paste_margin    -> footprint_library.SolderPasteMargin
solder_paste_margin_ratio -> footprint_library.SolderPasteMarginRatio
tags                   -> footprint_library.Tags
```

### pad_and_drill.py - Pad and Drill Elements

```python
chamfer                -> pad_and_drill.Chamfer
chamfer_ratio          -> pad_and_drill.ChamferRatio
die_length             -> pad_and_drill.DieLength
drill                  -> pad_and_drill.Drill
free                   -> pad_and_drill.Free
net                    -> pad_and_drill.Net
options                -> pad_and_drill.Options
pad                    -> pad_and_drill.Pad
pads                   -> pad_and_drill.Pads
primitives             -> pad_and_drill.Primitives
roundrect_rratio       -> pad_and_drill.RoundrectRratio
shape                  -> pad_and_drill.Shape
solder_paste_ratio     -> pad_and_drill.SolderPasteRatio
thermal_bridge_width   -> pad_and_drill.ThermalBridgeWidth
thermal_gap            -> pad_and_drill.ThermalGap
thermal_width          -> pad_and_drill.ThermalWidth
zone_connect           -> pad_and_drill.ZoneConnect
```

### primitive_graphics.py - Basic Graphics Primitives

```python
arc                    -> primitive_graphics.Arc
bezier                 -> primitive_graphics.Bezier
circle                 -> primitive_graphics.Circle
line                   -> primitive_graphics.Line
polygon                -> primitive_graphics.Polygon
polyline               -> primitive_graphics.Polyline
rect                   -> primitive_graphics.Rect
rectangle              -> primitive_graphics.Rectangle
```

### project_settings.py - JSON Project Settings

```python
board_defaults         -> project_settings.BoardDefaults
board_settings         -> project_settings.BoardSettings
cvpcb_settings         -> project_settings.CvpcbSettings
design_settings        -> project_settings.DesignSettings
erc_settings           -> project_settings.ERCSettings
ipc2581_settings       -> project_settings.IPC2581Settings
kicad_project          -> project_settings.KicadProject
library_settings       -> project_settings.LibrarySettings
net_class              -> project_settings.NetClass
net_settings           -> project_settings.NetSettings
pcbnew_settings        -> project_settings.PcbnewSettings
project_meta           -> project_settings.ProjectMeta
schematic_bom_settings -> project_settings.SchematicBOMSettings
schematic_settings     -> project_settings.SchematicSettings
```

### schematic_system.py - Schematic Drawing

```python
bus                    -> schematic_system.Bus
bus_entry              -> schematic_system.BusEntry
embedded_fonts         -> schematic_system.EmbeddedFonts
global_label           -> schematic_system.GlobalLabel
incrx                  -> schematic_system.Incrx
incry                  -> schematic_system.Incry
junction               -> schematic_system.Junction
kicad_sch              -> schematic_system.KicadSch
label                  -> schematic_system.Label
length                 -> schematic_system.Length
no_connect             -> schematic_system.NoConnect
project                -> schematic_system.Project
repeat                 -> schematic_system.Repeat
sheet                  -> schematic_system.Sheet
sheet_instance         -> schematic_system.SheetInstance
sheet_instances        -> schematic_system.SheetInstances
wire                   -> schematic_system.Wire
```

### symbol_library.py - Symbol Management

```python
exclude_from_sim       -> symbol_library.ExcludeFromSim
extends                -> symbol_library.Extends
fields_autoplaced      -> symbol_library.FieldsAutoplaced
in_bom                 -> symbol_library.InBom
instances              -> symbol_library.Instances
lib_symbols            -> symbol_library.LibSymbols
number                 -> symbol_library.Number
pin                    -> symbol_library.Pin
pin_names              -> symbol_library.PinNames
pin_numbers            -> symbol_library.PinNumbers
pinfunction            -> symbol_library.Pinfunction
pintype                -> symbol_library.Pintype
prefix                 -> symbol_library.Prefix
symbol                 -> symbol_library.Symbol
unit_name              -> symbol_library.UnitName
```

### text_and_documents.py - Text and Document Elements

```python
bitmap                 -> text_and_documents.Bitmap
bottom_margin          -> text_and_documents.BottomMargin
comment                -> text_and_documents.Comment
company                -> text_and_documents.Company
data                   -> text_and_documents.Data
date                   -> text_and_documents.Date
descr                  -> text_and_documents.Descr
generator              -> text_and_documents.Generator
generator_version      -> text_and_documents.GeneratorVersion
group                  -> text_and_documents.Group
image                  -> text_and_documents.Image
kicad_wks              -> text_and_documents.KicadWks
left_margin            -> text_and_documents.LeftMargin
members                -> text_and_documents.Members
page                   -> text_and_documents.Page
paper                  -> text_and_documents.Paper
pngdata                -> text_and_documents.Pngdata
rev                    -> text_and_documents.Rev
right_margin           -> text_and_documents.RightMargin
scale                  -> text_and_documents.Scale
suffix                 -> text_and_documents.Suffix
tbtext                 -> text_and_documents.Tbtext
tedit                  -> text_and_documents.Tedit
textlinewidth          -> text_and_documents.Textlinewidth
textsize               -> text_and_documents.Textsize
title_block            -> text_and_documents.TitleBlock
top_margin             -> text_and_documents.TopMargin
version                -> text_and_documents.Version
wks_line               -> text_and_documents.WksLine
wks_linewidth          -> text_and_documents.WksLinewidth
wks_margin             -> text_and_documents.WksMargin
wks_rect               -> text_and_documents.WksRect
wks_setup              -> text_and_documents.WksSetup
wks_tb_text            -> text_and_documents.WksTbText
wks_textlinewidth      -> text_and_documents.WksTextlinewidth
wks_textsize           -> text_and_documents.WksTextsize
```

### zone_system.py - Zone and Copper Filling

```python
connect_pads           -> zone_system.ConnectPads
copperpour             -> zone_system.Copperpour
epsilon_r              -> zone_system.EpsilonR
fill_segments          -> zone_system.FillSegments
filled_areas_thickness -> zone_system.FilledAreasThickness
filled_polygon         -> zone_system.FilledPolygon
filled_segments        -> zone_system.FilledSegments
hatch                  -> zone_system.Hatch
hatch_border_algorithm -> zone_system.HatchBorderAlgorithm
hatch_gap              -> zone_system.HatchGap
hatch_min_hole_area    -> zone_system.HatchMinHoleArea
hatch_orientation      -> zone_system.HatchOrientation
hatch_smoothing_level  -> zone_system.HatchSmoothingLevel
hatch_smoothing_value  -> zone_system.HatchSmoothingValue
hatch_thickness        -> zone_system.HatchThickness
island_area_min        -> zone_system.IslandAreaMin
island_removal_mode    -> zone_system.IslandRemovalMode
keep_end_layers        -> zone_system.KeepEndLayers
keepout                -> zone_system.Keepout
loss_tangent           -> zone_system.LossTangent
material               -> zone_system.Material
min_thickness          -> zone_system.MinThickness
mode                   -> zone_system.Mode
priority               -> zone_system.Priority
remove_unused_layer    -> zone_system.RemoveUnusedLayer
remove_unused_layers   -> zone_system.RemoveUnusedLayers
smoothing              -> zone_system.Smoothing
zone                   -> zone_system.Zone
```

## Class Naming Convention

Each S-expression token gets a corresponding class with the pattern:

- Token name in lowercase -> CamelCase ClassName
- Examples: `at`       -> `At`, `fp_line`              -> `FpLine`, `zone_connect`         -> `ZoneConnect`

## Implementation Notes

1. **Dependency-Based Structure**: Classes organized by dependencies to eliminate TYPE_CHECKING
2. **Nested Elements**: When tokens contain other tokens, they reference classes from appropriate modules
3. **File Organization**: Tokens grouped by functional area and dependency level
4. **Inheritance**: All classes inherit from a base `KiCadObject` class
5. **Token Count**: Total of 241 unique tokens mapped to 241 classes across 12 Python modules

## Class Implementation Specification

### Standard Pattern

```python
from dataclasses import dataclass, field
from typing import Optional
from ..kicad_common import KiCadObject
import base_types  # Import required modules

@dataclass
class ClassName(KiCadObject):
    """S-expression token description.

    The 'token_name' token defines... in the format::

        (token_name PARAM1 [OPTIONAL_PARAM])

    Args:
        param1: Description of required parameter
        optional_param: Description of optional parameter
    """
    __token_name__ = "token_name"

    # Follow exact documentation order
    param1: type = field(metadata={"description": "Description"})
    optional_param: Optional[type] = field(default=None, metadata={"description": "Description", "required": False})
```

### Implementation Rules

**Types & Defaults:**

- Basic: `str`, `int`, `float`, `bool` with defaults `""`, `0`, `0.0`, `False`
- Optional: `Optional[type]` with `default=None` and `metadata={"required": False}`
- Nested: `module.ClassName` (import modules, no defaults for required objects)
- Lists: `List[module.Type]` with `default_factory=list` or `None` for optional

**Field Order (CRITICAL):**

- Must follow exact KiCad documentation parameter order
- If required primitives after optional fields: add `# TODO: Fix field order`

**Metadata & Documentation:**

- All fields need `metadata={"description": "..."}`
- Optional fields add `"required": False`
- Docstrings: PEP 257/287 compliant with Sphinx format
- Use `Args:` section (no `Attributes:` - dataclass fields are self-documenting)
- Code blocks with `::` for S-expression format examples

### Example: Field Order Conflicts

```python
@dataclass
class Example(KiCadObject):
    """Token with field order conflict - follows documentation order.

    Note:
        Field order follows KiCad documentation, not dataclass conventions.
        Required fields after optional fields violate dataclass ordering.

    Args:
        optional1: First parameter (optional)
        required_str: Required parameter after optional
        optional2: Last parameter (optional)
    """
    __token_name__ = "example"

    optional1: Optional[str] = field(default=None, metadata={"description": "First param", "required": False})
    required_str: str = field(default="", metadata={"description": "Required after optional"})  # TODO: Fix field order
    optional2: Optional[int] = field(default=None, metadata={"description": "Last param", "required": False})
```

### Example: Complete Implementation

```python
from dataclasses import dataclass, field
from typing import Optional
import base_types

@dataclass
class Stroke(KiCadObject):
    """Stroke definition for graphical objects.

    The 'stroke' token defines how outlines are drawn in the format::

        (stroke
            (width WIDTH)
            (type TYPE)
            [(color R G B A)]
        )

    Args:
        width: Line width specification
        type: Stroke line style (solid, dash, etc.)
        color: Line color specification (optional)
    """
    __token_name__ = "stroke"

    width: base_types.Width = field(metadata={"description": "Line width"})
    type: base_types.Type = field(metadata={"description": "Line style"})
    color: Optional[base_types.Color] = field(default=None, metadata={"description": "Line color", "required": False})
```

## Core Principles

1. **Mirror S-expression structure exactly** - nested tokens become nested objects
2. **Follow KiCad documentation parameter order** - mark dataclass conflicts with TODO
3. **Type safety** - explicit types, metadata, `mypy --strict` compatible
4. **Consistent naming** - `snake_case` → `PascalCase`, exact field names, `__token_name__`
