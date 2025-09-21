# KiCad Parser v2 - Class Structure

This document outlines the complete class structure for the KiCad Parser v2, with one class per S-expression token.

## File Organization

### base_types.py - Fundamental Types (39 tokens)

**No dependencies - foundation layer**

```python
anchor                 -> base_types.Anchor  # custom_pad_options.txt
angle                  -> base_types.Angle  # graphical_polygon.txt
at                     -> base_types.At  # position_identifier.txt, footprint_3d_model.txt
center                 -> base_types.Center  # track_via.txt
clearance              -> base_types.Clearance  # setup_section.txt
color                  -> base_types.Color  # fill_definition.txt
diameter               -> base_types.Diameter  # track_via.txt
effects                -> base_types.Effects  # symbol_text.txt
end                    -> base_types.End  # graphical_line.txt
fill                   -> base_types.Fill  # fill_definition.txt
font                   -> base_types.Font  # symbol_text.txt
height                 -> base_types.Height  # dimension.txt
id                     -> base_types.Id  # group.txt
justify                -> base_types.Justify  # symbol_text.txt
layer                  -> base_types.Layer  # stack_up_layer_settings.txt
linewidth              -> base_types.Linewidth  # graphical_polygon.txt
locked                 -> base_types.Locked  # track_segment.txt
name                   -> base_types.Name  # graphical_line.txt
offset                 -> base_types.Offset  # symbols.txt
pos                    -> base_types.Pos  # graphical_polygon.txt
property               -> base_types.Property  # properties.txt, symbol_properties.txt
radius                 -> base_types.Radius  # track_arc.txt
rotate                 -> base_types.Rotate  # graphical_polygon.txt, footprint_3d_model.txt
size                   -> base_types.Size  # title_block_text.txt
start                  -> base_types.Start  # graphical_line.txt
stroke                 -> base_types.Stroke  # stroke_definition.txt
style                  -> base_types.Style  # symbol_pin.txt
text                   -> base_types.Text  # symbol_text.txt
thickness              -> base_types.Thickness  # general_section.txt
title                  -> base_types.Title  # graphical_line.txt
tstamp                 -> base_types.Tstamp  # track_arc.txt
type                   -> base_types.Type  # hierarchical_sheet_pin_definition.txt
units                  -> base_types.Units  # dimension_format.txt
uuid                   -> base_types.Uuid  # universally_unique_identifier.txt
visible                -> base_types.Visible  # conventions.txt
width                  -> base_types.Width  # setup_section.txt
xy                     -> base_types.Xy  # coordinate_point_list.txt
xyz                    -> base_types.Xyz  # footprint_3d_model.txt
pts                    -> base_types.Pts  # coordinate_point_list.txt
```

### text_and_documents.py - Text and Document Elements (27 tokens)

**Dependencies: base_types**

```python
comment                -> text_and_documents.Comment  # title_block.txt
company                -> text_and_documents.Company  # title_block.txt
data                   -> text_and_documents.Data  # image_data.txt
date                   -> text_and_documents.Date  # header_section.txt
descr                  -> text_and_documents.Descr  # footprint.txt
generator              -> text_and_documents.Generator  # header_section.txt
page                   -> text_and_documents.Page  # page_settings.txt
paper                  -> text_and_documents.Paper  # page_settings.txt
rev                    -> text_and_documents.Rev  # title_block.txt
tedit                  -> text_and_documents.Tedit  # footprint.txt
title_block            -> text_and_documents.TitleBlock  # title_block.txt
version                -> text_and_documents.Version  # header_section.txt
bottom_margin          -> text_and_documents.BottomMargin  # set_up_section.txt
left_margin            -> text_and_documents.LeftMargin  # set_up_section.txt
right_margin           -> text_and_documents.RightMargin  # set_up_section.txt
tbtext                 -> text_and_documents.Tbtext  # title_block_text.txt
textlinewidth          -> text_and_documents.Textlinewidth  # set_up_section.txt
textsize               -> text_and_documents.Textsize  # set_up_section.txt
top_margin             -> text_and_documents.TopMargin  # set_up_section.txt
suffix                 -> text_and_documents.Suffix  # dimension_format.txt
scale                  -> text_and_documents.Scale  # image.txt, footprint_3d_model.txt
group                  -> text_and_documents.Group  # group.txt
members                -> text_and_documents.Members  # group.txt
kicad_wks              -> text_and_documents.KicadWks  # header_section.txt
bitmap                 -> text_and_documents.Bitmap  # image.txt
image                  -> text_and_documents.Image  # image.txt
pngdata                -> text_and_documents.Pngdata  # image.txt
```

### pad_and_drill.py - Pad and Drill Elements (18 tokens)

**Dependencies: base_types**

```python
chamfer                -> pad_and_drill.Chamfer  # footprint_pad.txt
chamfer_ratio          -> pad_and_drill.ChamferRatio  # footprint_pad.txt
free                   -> pad_and_drill.Free  # track_via.txt
options                -> pad_and_drill.Options  # custom_pad_options.txt
roundrect_rratio       -> pad_and_drill.RoundrectRratio  # footprint_pad.txt
shape                  -> pad_and_drill.Shape  # custom_pad_options.txt
solder_paste_ratio     -> pad_and_drill.SolderPasteRatio  # footprint_pad.txt
thermal_bridge_widh    -> pad_and_drill.ThermalBridgeWidth  # footprint.txt
thermal_gap            -> pad_and_drill.ThermalGap  # footprint.txt
thermal_width          -> pad_and_drill.ThermalWidth  # footprint.txt
zone_connect           -> pad_and_drill.ZoneConnect  # footprint_pad.txt
net                    -> pad_and_drill.Net  # nets_section.txt
options_clearance      -> pad_and_drill.OptionsClearance  # custom_pad_options.txt
drill                  -> pad_and_drill.Drill  # pad_drill_definition.txt
pad                    -> pad_and_drill.Pad  # footprint_pad.txt
pads                   -> pad_and_drill.Pads  # footprint.txt
primitives             -> pad_and_drill.Primitives  # custom_pad_primitives.txt
die_length             -> pad_and_drill.DieLength  # footprint_pad.txt
```

### primitive_graphics.py - Basic Graphics Primitives (8 tokens)

**Dependencies: base_types**

```python
arc                    -> primitive_graphics.Arc  # symbol_arc.txt
bezier                 -> primitive_graphics.Bezier  # graphical_curve.txt
circle                 -> primitive_graphics.Circle  # symbol_circle.txt
line                   -> primitive_graphics.Line  # graphical_line.txt
polygon                -> primitive_graphics.Polygon  # graphical_polygon.txt
polyline               -> primitive_graphics.Polyline  # graphical_line_section.txt
rect                   -> primitive_graphics.Rect  # graphical_rectangle.txt
rectangle              -> primitive_graphics.Rectangle  # symbol_rectangle.txt
```

### advanced_graphics.py - Complex Graphics Objects (20 tokens)

**Dependencies: base_types, text_and_documents**

```python
gr_arc                 -> advanced_graphics.GrArc  # graphical_arc.txt
gr_bbox                -> advanced_graphics.GrBbox  # annotation_bounding_box.txt
gr_circle              -> advanced_graphics.GrCircle  # graphical_circle.txt
gr_text                -> advanced_graphics.GrText  # graphical_text.txt
gr_text_box            -> advanced_graphics.GrTextBox  # graphical_text_box.txt
dimension              -> advanced_graphics.Dimension  # dimension.txt
format                 -> advanced_graphics.Format  # dimension_format.txt
leader_length          -> advanced_graphics.LeaderLength  # dimension.txt
precision              -> advanced_graphics.Precision  # dimension_format.txt
suppress_zeros         -> advanced_graphics.SuppressZeros  # dimension_format.txt
units_format           -> advanced_graphics.UnitsFormat  # dimension_format.txt
fp_arc                 -> advanced_graphics.FpArc  # footprint_arc.txt
fp_circle              -> advanced_graphics.FpCircle  # footprint_circle.txt
fp_curve               -> advanced_graphics.FpCurve  # footprint_curve.txt
fp_line                -> advanced_graphics.FpLine  # footprint_line.txt
fp_poly                -> advanced_graphics.FpPoly  # footprint_polygon.txt
fp_rect                -> advanced_graphics.FpRect  # footprint_rectangle.txt
fp_text                -> advanced_graphics.FpText  # footprint_text.txt
fp_text_box            -> advanced_graphics.FpTextBox  # footprint_text_box.txt
render_cache           -> advanced_graphics.RenderCache  # graphical_text_box.txt
```

### symbol_library.py - Symbol Management (14 tokens)

**Dependencies: base_types**

```python
symbol                 -> symbol_library.Symbol  # symbols.txt
lib_symbols            -> symbol_library.LibSymbols  # library_symbol_section.txt
extends                -> symbol_library.Extends  # symbols.txt
fields_autoplaced      -> symbol_library.FieldsAutoplaced  # global_label_section.txt
in_bom                 -> symbol_library.InBom  # symbols.txt
instances              -> symbol_library.Instances  # hierarchical_sheet_section.txt
number                 -> symbol_library.Number  # hierarchical_sheet_section.txt
pin                    -> symbol_library.Pin  # symbol_pin.txt
pin_names              -> symbol_library.PinNames  # symbols.txt
pin_numbers            -> symbol_library.PinNumbers  # symbols.txt
pinfunction            -> symbol_library.Pinfunction  # footprint_pad.txt
pintype                -> symbol_library.Pintype  # footprint_pad.txt
prefix                 -> symbol_library.Prefix  # dimension_format.txt
unit_name              -> symbol_library.UnitName  # symbols.txt
```

### footprint_library.py - Footprint Management (12 tokens)

**Dependencies: base_types, symbol_library, pad_and_drill, text_and_documents, board_layout**

```python
footprint              -> footprint_library.Footprint  # footprint.txt
footprints             -> footprint_library.Footprints  # footprint.txt
attr                   -> footprint_library.Attr  # footprint_attributes.txt
autoplace_cost180      -> footprint_library.AutoplaceCost180  # footprint.txt
autoplace_cost90       -> footprint_library.AutoplaceCost90  # footprint.txt
model                  -> footprint_library.Model  # footprint_3d_model.txt
net_tie_pad_groups     -> footprint_library.NetTiePadGroups  # footprint.txt
on_board               -> footprint_library.OnBoard  # symbols.txt
solder_mask_margin     -> footprint_library.SolderMaskMargin  # footprint.txt
solder_paste_margin    -> footprint_library.SolderPasteMargin  # footprint.txt
solder_paste_marginio  -> footprint_library.SolderPasteMarginRatio  # footprint_pad.txt
tags                   -> footprint_library.Tags  # footprint.txt
```

### zone_system.py - Zone and Copper Filling (28 tokens)

**Dependencies: base_types, primitive_graphics**

```python
zone                   -> zone_system.Zone  # zone.txt
connect_pads           -> zone_system.ConnectPads  # zone.txt
copperpour             -> zone_system.Copperpour  # zone_keep_out_settings.txt
epsilon_r              -> zone_system.EpsilonR  # stack_up_layer_settings.txt
fill_segments          -> zone_system.FillSegments  # zone_fill_segments.txt
filled_areas_thicknss  -> zone_system.FilledAreasThickness  # zone.txt
filled_polygon         -> zone_system.FilledPolygon  # zone_fill_polygons.txt
filled_segments        -> zone_system.FilledSegments  # zone_fill_segments.txt
hatch                  -> zone_system.Hatch  # zone.txt
hatch_border_algorihm  -> zone_system.HatchBorderAlgorithm  # zone.txt
hatch_gap              -> zone_system.HatchGap  # zone.txt
hatch_min_hole_area    -> zone_system.HatchMinHoleArea  # zone.txt
hatch_orientation      -> zone_system.HatchOrientation  # zone.txt
hatch_smoothing_leel   -> zone_system.HatchSmoothingLevel  # zone.txt
hatch_smoothing_vaue   -> zone_system.HatchSmoothingValue  # zone.txt
hatch_thickness        -> zone_system.HatchThickness  # zone.txt
island_area_min        -> zone_system.IslandAreaMin  # zone.txt
island_removal_mode    -> zone_system.IslandRemovalMode  # zone.txt
keep_end_layers        -> zone_system.KeepEndLayers  # zone.txt
keepout                -> zone_system.Keepout  # zone_keep_out_settings.txt
loss_tangent           -> zone_system.LossTangent  # stack_up_layer_settings.txt
material               -> zone_system.Material  # stack_up_layer_settings.txt
min_thickness          -> zone_system.MinThickness  # zone.txt
mode                   -> zone_system.Mode  # zone.txt
priority               -> zone_system.Priority  # zone.txt
remove_unused_layer    -> zone_system.RemoveUnusedLayer  # zone.txt
remove_unused_layes    -> zone_system.RemoveUnusedLayers  # zone.txt
smoothing              -> zone_system.Smoothing  # zone.txt
```

### board_layout.py - PCB Board Design (13 tokens)

**Dependencies: base_types**

```python
general                -> board_layout.General  # general_section.txt
layers                 -> board_layout.Layers  # layers_section.txt
nets                   -> board_layout.Nets  # nets_section.txt
private_layers         -> board_layout.PrivateLayers  # setup_section.txt
segment                -> board_layout.Segment  # track_segment.txt
setup                  -> board_layout.Setup  # setup_section.txt
tracks                 -> board_layout.Tracks  # setup_section.txt
via                    -> board_layout.Via  # track_via.txt
vias                   -> board_layout.Vias  # setup_section.txt
net_name               -> board_layout.NetName  # track_segment.txt
orientation            -> board_layout.Orientation  # footprint.txt
override_value         -> board_layout.OverrideValue  # dimension_format.txt
path                   -> board_layout.Path  # hierarchical_sheet_section.txt
```

### schematic_system.py - Schematic Drawing (13 tokens)

**Dependencies: base_types, symbol_library**

```python
bus                    -> schematic_system.Bus  # wire_and_bus_section.txt
bus_entry              -> schematic_system.BusEntry  # bus_entry_section.txt
global_label           -> schematic_system.GlobalLabel  # global_label_section.txt
junction               -> schematic_system.Junction  # junction_section.txt
label                  -> schematic_system.Label  # local_label_section.txt
no_connect             -> schematic_system.NoConnect  # no_connect_section.txt
sheet                  -> schematic_system.Sheet  # hierarchical_sheet_section.txt
wire                   -> schematic_system.Wire  # wire_and_bus_section.txt
project                -> schematic_system.Project  # hierarchical_sheet_section.txt
incrx                  -> schematic_system.Incrx  # graphical_line.txt
incry                  -> schematic_system.Incry  # graphical_line.txt
length                 -> schematic_system.Length  # symbol_circle.txt
repeat                 -> schematic_system.Repeat  # graphical_line.txt
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
5. **Token Count**: Total of 207 unique tokens mapped to 207 classes across 10 Python modules

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
- Lists: `list[module.Type]` with `default_factory=list` or `None` for optional

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
