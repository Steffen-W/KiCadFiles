"""Board layout elements for KiCad S-expressions - PCB/board design and routing."""

from dataclasses import dataclass, field
from typing import Any, List, Optional, Union

from .advanced_graphics import GrArc, GrLine, GrPoly, GrText
from .base_element import (
    KiCadFloat,
    KiCadInt,
    KiCadObject,
    KiCadStr,
    OptionalFlag,
    ParseStrictness,
)
from .base_types import (
    At,
    BoardLayers,
    End,
    Layer,
    Layers,
    Mid,
    Property,
    Start,
    Uuid,
)
from .footprint_library import Footprint
from .pad_and_drill import Net
from .text_and_documents import Group
from .zone_system import Zone


@dataclass
class Nets(KiCadObject):
    """Nets section definition token.

    The 'nets' token defines nets for the board in the format::

        (net
            ORDINAL
            "NET_NAME"
        )

    Args:
        net_definitions: List of net definitions (ordinal, net_name)
    """

    __token_name__ = "nets"

    net_definitions: List[tuple[Any, ...]] = field(
        default_factory=list,
        metadata={"description": "List of net definitions (ordinal, net_name)"},
    )


@dataclass
class PrivateLayers(KiCadObject):
    """Private layers definition token.

    The 'private_layers' token defines layers private to specific elements in the format::

        (private_layers "LAYER_LIST")

    Args:
        layers: List of private layer names
    """

    __token_name__ = "private_layers"

    layers: List[str] = field(
        default_factory=list, metadata={"description": "List of private layer names"}
    )


@dataclass
class Segment(KiCadObject):
    """Track segment definition token.

    The 'segment' token defines a track segment in the format::

        (segment
            (start X Y)
            (end X Y)
            (width WIDTH)
            (layer LAYER_DEFINITION)
            [(locked)]
            (net NET_NUMBER)
            (tstamp UUID)
        )

    Args:
        start: Coordinates of the beginning of the line
        end: Coordinates of the end of the line
        width: Line width
        layer: Layer the track segment resides on
        locked: Whether the line cannot be edited (optional)
        net: Net ordinal number from net section
        tstamp: Unique identifier of the line object (optional)
        uuid: Unique identifier
    """

    __token_name__ = "segment"

    start: Start = field(
        default_factory=lambda: Start(),
        metadata={"description": "Coordinates of the beginning of the line"},
    )
    end: End = field(
        default_factory=lambda: End(),
        metadata={"description": "Coordinates of the end of the line"},
    )
    width: KiCadFloat = field(
        default_factory=lambda: KiCadFloat("width", 0.0),
        metadata={"description": "Line width"},
    )
    layer: Layer = field(
        default_factory=lambda: Layer(),
        metadata={"description": "Layer the track segment resides on"},
    )
    locked: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("locked"),
        metadata={
            "description": "Whether the line cannot be edited",
            "required": False,
        },
    )
    net: int = field(
        default=0, metadata={"description": "Net ordinal number from net section"}
    )
    tstamp: KiCadStr = field(
        default_factory=lambda: KiCadStr("tstamp", "", required=False),
        metadata={
            "description": "Unique identifier of the line object",
            "required": False,
        },
    )  # NEW Variant
    uuid: Optional[Uuid] = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )  # Old Variant


@dataclass
class Tenting(KiCadObject):
    """Tenting configuration for front/back sides.

    Args:
        sides: List of sides (front/back)
    """

    __token_name__ = "tenting"

    sides: List[str] = field(
        default_factory=list, metadata={"description": "List of sides (front/back)"}
    )


@dataclass
class PcbPlotParams(KiCadObject):
    """PCB plot parameters - stores all plotting settings.

    Args:
        layerselection: Layer selection hex mask (optional)
        plot_on_all_layers_selection: Plot on all layers selection (optional)
        disableapertmacros: Disable aperture macros (optional)
        usegerberextensions: Use gerber extensions (optional)
        usegerberattributes: Use gerber attributes (optional)
        usegerberadvancedattributes: Use gerber advanced attributes (optional)
        creategerberjobfile: Create gerber job file (optional)
        dashed_line_dash_ratio: Dashed line dash ratio (optional)
        dashed_line_gap_ratio: Dashed line gap ratio (optional)
        svgprecision: SVG precision (optional)
        plotframeref: Plot frame reference (optional)
        mode: Plot mode (optional)
        useauxorigin: Use auxiliary origin (optional)
        hpglpennumber: HPGL pen number (optional)
        hpglpenspeed: HPGL pen speed (optional)
        hpglpendiameter: HPGL pen diameter (optional)
        pdf_front_fp_property_popups: PDF front footprint property popups (optional)
        pdf_back_fp_property_popups: PDF back footprint property popups (optional)
        pdf_metadata: PDF metadata (optional)
        pdf_single_document: PDF single document (optional)
        dxfpolygonmode: DXF polygon mode (optional)
        dxfimperialunits: DXF imperial units (optional)
        dxfusepcbnewfont: DXF use pcbnew font (optional)
        psnegative: PS negative (optional)
        psa4output: PS A4 output (optional)
        plot_black_and_white: Plot black and white (optional)
        plotinvisibletext: Plot invisible text (optional)
        sketchpadsonfab: Sketch pads on fab (optional)
        plotpadnumbers: Plot pad numbers (optional)
        hidednponfab: Hide DNP on fab (optional)
        sketchdnponfab: Sketch DNP on fab (optional)
        crossoutdnponfab: Cross out DNP on fab (optional)
        subtractmaskfromsilk: Subtract mask from silk (optional)
        outputformat: Output format (optional)
        mirror: Mirror (optional)
        drillshape: Drill shape (optional)
        scaleselection: Scale selection (optional)
        outputdirectory: Output directory (optional)
    """

    __token_name__ = "pcbplotparams"

    layerselection: KiCadStr = field(
        default_factory=lambda: KiCadStr(
            "layerselection", "0x00000000_00000000_55555555_5755f5ff", required=False
        ),
        metadata={"description": "Layer selection hex mask", "required": False},
    )
    plot_on_all_layers_selection: KiCadStr = field(
        default_factory=lambda: KiCadStr(
            "plot_on_all_layers_selection",
            "0x00000000_00000000_00000000_00000000",
            required=False,
        ),
        metadata={"description": "Plot on all layers selection", "required": False},
    )
    disableapertmacros: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("disableapertmacros", "no"),
        metadata={"description": "Disable aperture macros", "required": False},
    )
    usegerberextensions: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("usegerberextensions", "no"),
        metadata={"description": "Use gerber extensions", "required": False},
    )
    usegerberattributes: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("usegerberattributes", "yes"),
        metadata={"description": "Use gerber attributes", "required": False},
    )
    usegerberadvancedattributes: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("usegerberadvancedattributes", "yes"),
        metadata={"description": "Use gerber advanced attributes", "required": False},
    )
    creategerberjobfile: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("creategerberjobfile", "yes"),
        metadata={"description": "Create gerber job file", "required": False},
    )
    dashed_line_dash_ratio: KiCadFloat = field(
        default_factory=lambda: KiCadFloat(
            "dashed_line_dash_ratio", 12.0, required=False
        ),
        metadata={"description": "Dashed line dash ratio", "required": False},
    )
    dashed_line_gap_ratio: KiCadFloat = field(
        default_factory=lambda: KiCadFloat(
            "dashed_line_gap_ratio", 3.0, required=False
        ),
        metadata={"description": "Dashed line gap ratio", "required": False},
    )
    svgprecision: KiCadInt = field(
        default_factory=lambda: KiCadInt("svgprecision", 4, required=False),
        metadata={"description": "SVG precision", "required": False},
    )
    plotframeref: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("plotframeref", "no"),
        metadata={"description": "Plot frame reference", "required": False},
    )
    mode: KiCadInt = field(
        default_factory=lambda: KiCadInt("mode", 1, required=False),
        metadata={"description": "Plot mode", "required": False},
    )
    useauxorigin: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("useauxorigin", "no"),
        metadata={"description": "Use auxiliary origin", "required": False},
    )
    hpglpennumber: KiCadInt = field(
        default_factory=lambda: KiCadInt("hpglpennumber", 1, required=False),
        metadata={"description": "HPGL pen number", "required": False},
    )
    hpglpenspeed: KiCadInt = field(
        default_factory=lambda: KiCadInt("hpglpenspeed", 20, required=False),
        metadata={"description": "HPGL pen speed", "required": False},
    )
    hpglpendiameter: KiCadFloat = field(
        default_factory=lambda: KiCadFloat("hpglpendiameter", 15.0, required=False),
        metadata={"description": "HPGL pen diameter", "required": False},
    )
    pdf_front_fp_property_popups: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("pdf_front_fp_property_popups", "yes"),
        metadata={
            "description": "PDF front footprint property popups",
            "required": False,
        },
    )
    pdf_back_fp_property_popups: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("pdf_back_fp_property_popups", "yes"),
        metadata={
            "description": "PDF back footprint property popups",
            "required": False,
        },
    )
    pdf_metadata: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("pdf_metadata", "yes"),
        metadata={"description": "PDF metadata", "required": False},
    )
    pdf_single_document: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("pdf_single_document", "no"),
        metadata={"description": "PDF single document", "required": False},
    )
    dxfpolygonmode: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("dxfpolygonmode", "yes"),
        metadata={"description": "DXF polygon mode", "required": False},
    )
    dxfimperialunits: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("dxfimperialunits", "yes"),
        metadata={"description": "DXF imperial units", "required": False},
    )
    dxfusepcbnewfont: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("dxfusepcbnewfont", "yes"),
        metadata={"description": "DXF use pcbnew font", "required": False},
    )
    psnegative: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("psnegative", "no"),
        metadata={"description": "PS negative", "required": False},
    )
    psa4output: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("psa4output", "no"),
        metadata={"description": "PS A4 output", "required": False},
    )
    plot_black_and_white: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("plot_black_and_white", "yes"),
        metadata={"description": "Plot black and white", "required": False},
    )
    plotinvisibletext: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("plotinvisibletext", "no"),
        metadata={"description": "Plot invisible text", "required": False},
    )
    sketchpadsonfab: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("sketchpadsonfab", "no"),
        metadata={"description": "Sketch pads on fab", "required": False},
    )
    plotpadnumbers: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("plotpadnumbers", "no"),
        metadata={"description": "Plot pad numbers", "required": False},
    )
    hidednponfab: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("hidednponfab", "no"),
        metadata={"description": "Hide DNP on fab", "required": False},
    )
    sketchdnponfab: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("sketchdnponfab", "yes"),
        metadata={"description": "Sketch DNP on fab", "required": False},
    )
    crossoutdnponfab: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("crossoutdnponfab", "yes"),
        metadata={"description": "Cross out DNP on fab", "required": False},
    )
    subtractmaskfromsilk: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("subtractmaskfromsilk", "no"),
        metadata={"description": "Subtract mask from silk", "required": False},
    )
    outputformat: KiCadInt = field(
        default_factory=lambda: KiCadInt("outputformat", 1, required=False),
        metadata={"description": "Output format", "required": False},
    )
    mirror: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("mirror", "no"),
        metadata={"description": "Mirror", "required": False},
    )
    drillshape: KiCadInt = field(
        default_factory=lambda: KiCadInt("drillshape", 1, required=False),
        metadata={"description": "Drill shape", "required": False},
    )
    scaleselection: KiCadInt = field(
        default_factory=lambda: KiCadInt("scaleselection", 1, required=False),
        metadata={"description": "Scale selection", "required": False},
    )
    outputdirectory: KiCadStr = field(
        default_factory=lambda: KiCadStr("outputdirectory", "", required=False),
        metadata={"description": "Output directory", "required": False},
    )


@dataclass
class StackupLayer(KiCadObject):
    """A single layer in the stackup configuration.

    Args:
        name: Layer name
        type: Layer type (optional)
        color: Layer color (optional)
        thickness: Layer thickness (optional)
        material: Material name (optional)
        epsilon_r: Relative permittivity (optional)
        loss_tangent: Loss tangent (optional)
    """

    __token_name__ = "layer"

    name: str = field(default="", metadata={"description": "Layer name"})
    type: KiCadStr = field(
        default_factory=lambda: KiCadStr("type", "", required=False),
        metadata={"description": "Layer type", "required": False},
    )
    color: KiCadStr = field(
        default_factory=lambda: KiCadStr("color", "", required=False),
        metadata={"description": "Layer color", "required": False},
    )
    thickness: KiCadFloat = field(
        default_factory=lambda: KiCadFloat("thickness", 0.0, required=False),
        metadata={"description": "Layer thickness", "required": False},
    )
    material: KiCadStr = field(
        default_factory=lambda: KiCadStr("material", "", required=False),
        metadata={"description": "Material name", "required": False},
    )
    epsilon_r: KiCadFloat = field(
        default_factory=lambda: KiCadFloat("epsilon_r", 0.0, required=False),
        metadata={"description": "Relative permittivity", "required": False},
    )
    loss_tangent: KiCadFloat = field(
        default_factory=lambda: KiCadFloat("loss_tangent", 0.0, required=False),
        metadata={"description": "Loss tangent", "required": False},
    )


@dataclass
class Stackup(KiCadObject):
    """PCB stackup configuration.

    Args:
        layers: List of stackup layers
        copper_finish: Copper finish specification (optional)
        dielectric_constraints: Dielectric constraints flag (optional)
    """

    __token_name__ = "stackup"

    layers: List[StackupLayer] = field(
        default_factory=list,
        metadata={"description": "List of stackup layers"},
    )
    copper_finish: KiCadStr = field(
        default_factory=lambda: KiCadStr("copper_finish", "", required=False),
        metadata={"description": "Copper finish specification", "required": False},
    )
    dielectric_constraints: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("dielectric_constraints", "no"),
        metadata={"description": "Dielectric constraints flag", "required": False},
    )


@dataclass
class Setup(KiCadObject):
    """Board setup definition token.

    The 'setup' token stores current settings and options used by the board in the format::

        (setup
            [(STACK_UP_SETTINGS)]
            (pad_to_mask_clearance CLEARANCE)
            [(solder_mask_min_width MINIMUM_WIDTH)]
            [(pad_to_paste_clearance CLEARANCE)]
            [(pad_to_paste_clearance_ratio RATIO)]
            [(aux_axis_origin X Y)]
            [(grid_origin X Y)]
            (PLOT_SETTINGS)
        )

    Args:
        stackup: Stackup configuration (optional)
        pad_to_mask_clearance: Pad to mask clearance (optional)
        allow_soldermask_bridges_in_footprints: Allow soldermask bridges in footprints (optional)
        tenting: Tenting configuration (optional)
        pcbplotparams: PCB plot parameters (optional)
    """

    __token_name__ = "setup"

    stackup: Optional["Stackup"] = field(
        default=None,
        metadata={"description": "Stackup configuration", "required": False},
    )
    pad_to_mask_clearance: KiCadFloat = field(
        default_factory=lambda: KiCadFloat(
            "pad_to_mask_clearance", 0.0, required=False
        ),
        metadata={"description": "Pad to mask clearance", "required": False},
    )
    allow_soldermask_bridges_in_footprints: OptionalFlag = field(
        default_factory=lambda: OptionalFlag(
            "allow_soldermask_bridges_in_footprints", "no"
        ),
        metadata={
            "description": "Allow soldermask bridges in footprints",
            "required": False,
        },
    )
    tenting: Optional[Tenting] = field(
        default=None,
        metadata={"description": "Tenting configuration", "required": False},
    )
    pcbplotparams: Optional[PcbPlotParams] = field(
        default=None,
        metadata={"description": "PCB plot parameters", "required": False},
    )


@dataclass
class General(KiCadObject):
    """General board settings definition token.

    The 'general' token defines general board settings in the format::

        (general
            (thickness THICKNESS)
            [(legacy_teardrops yes|no)]
        )

    Args:
        thickness: Board thickness
        legacy_teardrops: Whether to use legacy teardrops (optional)
    """

    __token_name__ = "general"

    thickness: KiCadFloat = field(
        default_factory=lambda: KiCadFloat("thickness", 1.6),
        metadata={"description": "Board thickness"},
    )
    legacy_teardrops: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("legacy_teardrops"),
        metadata={
            "description": "Whether to use legacy teardrops",
            "required": False,
        },
    )


@dataclass
class Tracks(KiCadObject):
    """Tracks container definition token.

    The 'tracks' token defines a container for track segments in the format::

        (tracks
            (segment ...)
            ...
        )

    Args:
        segments: List of track segments
    """

    __token_name__ = "tracks"

    segments: List[Segment] = field(
        default_factory=list, metadata={"description": "List of track segments"}
    )


@dataclass
class Via(KiCadObject):
    """Via definition token.

    The 'via' token defines a track via in the format::

        (via
            [TYPE]
            [(locked)]
            (at X Y)
            (size DIAMETER)
            (drill DIAMETER)
            (layers LAYER1 LAYER2)
            [(remove_unused_layers)]
            [(keep_end_layers)]
            [(free)]
            (net NET_NUMBER)
            (tstamp UUID)
        )

    Args:
        type: Via type (blind | micro) (optional)
        locked: Whether the line cannot be edited (optional)
        at: Coordinates of the center of the via
        size: Diameter of the via annular ring
        drill: Drill diameter of the via
        layers: Layer set the via connects
        remove_unused_layers: Remove unused layers flag (optional)
        keep_end_layers: Keep end layers flag (optional)
        free: Whether via is free to move outside assigned net (optional)
        net: Net ordinal number from net section
        tstamp: Unique identifier of the line object (optional)
        uuid: Unique identifier
    """

    __token_name__ = "via"

    type: Optional[str] = field(
        default=None,
        metadata={"description": "Via type (blind | micro)", "required": False},
    )
    locked: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("locked"),
        metadata={
            "description": "Whether the line cannot be edited",
            "required": False,
        },
    )
    at: At = field(
        default_factory=lambda: At(),
        metadata={"description": "Coordinates of the center of the via"},
    )
    size: KiCadFloat = field(
        default_factory=lambda: KiCadFloat("size", 0.0),
        metadata={"description": "Diameter of the via annular ring"},
    )
    drill: KiCadFloat = field(
        default_factory=lambda: KiCadFloat("drill", 0.0),
        metadata={"description": "Drill diameter of the via"},
    )
    layers: Layers = field(
        default_factory=lambda: Layers(),
        metadata={"description": "Layer set the via connects"},
    )
    remove_unused_layers: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("remove_unused_layers"),
        metadata={"description": "Remove unused layers flag", "required": False},
    )
    keep_end_layers: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("keep_end_layers"),
        metadata={"description": "Keep end layers flag", "required": False},
    )
    free: OptionalFlag = field(
        default_factory=lambda: OptionalFlag("free"),
        metadata={
            "description": "Whether via is free to move outside assigned net",
            "required": False,
        },
    )
    net: int = field(
        default=0, metadata={"description": "Net ordinal number from net section"}
    )
    tstamp: KiCadStr = field(
        default_factory=lambda: KiCadStr("tstamp", "", required=False),
        metadata={
            "description": "Unique identifier of the line object",
            "required": False,
        },
    )  # NEW Variant
    uuid: Optional[Uuid] = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )  # Old Variant


@dataclass
class Vias(KiCadObject):
    """Vias container definition token.

    The 'vias' token defines a container for vias in the format::

        (vias
            (via ...)
            ...
        )

    Args:
        vias: List of vias
    """

    __token_name__ = "vias"

    vias: List[Via] = field(
        default_factory=list, metadata={"description": "List of vias"}
    )


@dataclass
class BoardArc(KiCadObject):
    """Board arc track segment definition.

    The 'arc' token defines an arc-shaped track segment in the format::

        (arc
            (start X Y)
            (mid X Y)
            (end X Y)
            (width WIDTH)
            (layer LAYER)
            (net NET_NUMBER)
            (uuid UUID)
        )

    Args:
        start: Start point of the arc
        mid: Mid point of the arc
        end: End point of the arc
        width: Track width
        layer: Layer name
        net: Net number
        uuid: Unique identifier (optional)
    """

    __token_name__ = "arc"

    start: Start = field(
        default_factory=lambda: Start(),
        metadata={"description": "Start point of the arc"},
    )
    mid: Mid = field(
        default_factory=lambda: Mid(),
        metadata={"description": "Mid point of the arc"},
    )
    end: End = field(
        default_factory=lambda: End(),
        metadata={"description": "End point of the arc"},
    )
    width: KiCadFloat = field(
        default_factory=lambda: KiCadFloat("width", 0.0),
        metadata={"description": "Track width"},
    )
    layer: KiCadStr = field(
        default_factory=lambda: KiCadStr("layer", ""),
        metadata={"description": "Layer name"},
    )
    net: KiCadInt = field(
        default_factory=lambda: KiCadInt("net", 0),
        metadata={"description": "Net number"},
    )
    uuid: Optional[Uuid] = field(
        default_factory=lambda: Uuid(),
        metadata={"description": "Unique identifier", "required": False},
    )


@dataclass
class KicadPcb(KiCadObject):
    """KiCad PCB board file definition.

    The 'kicad_pcb' token defines a complete PCB board file in the format::

        (kicad_pcb
            (version VERSION)
            (generator GENERATOR)
            (general ...)
            (paper "SIZE")
            (page ...)
            (layers ...)
            (setup ...)
            [(property ...)]
            [(net ...)]
            [(footprint ...)]
            [(gr_text ...)]
            [(segment ...)]
            [(via ...)]
            [(zone ...)]
        )

    Args:
        version: File format version
        generator: Generator application
        generator_version: Generator version (optional)
        general: General board settings (optional)
        page: Page settings (optional)
        paper: Paper size specification (optional)
        layers: Layer definitions (optional)
        setup: Board setup (optional)
        embedded_fonts: Whether fonts are embedded (yes/no) (optional)
        properties: Board properties
        nets: Net definitions
        footprints: Footprint instances
        gr_elements: List of board graphical elements (optional)
        arcs: Arc track segments
        groups: Group definitions
        segments: Track segments
        vias: Via definitions
        zones: Zone definitions
    """

    __token_name__ = "kicad_pcb"

    # Required header fields
    version: KiCadInt = field(
        default_factory=lambda: KiCadInt("version", 20240101),
        metadata={"description": "File format version"},
    )
    generator: KiCadStr = field(
        default_factory=lambda: KiCadStr("generator", ""),
        metadata={"description": "Generator application"},
    )
    generator_version: KiCadStr = field(
        default_factory=lambda: KiCadStr("generator_version", "", required=False),
        metadata={"description": "Generator version", "required": False},
    )

    # Optional sections
    general: Optional[General] = field(
        default=None,
        metadata={"description": "General board settings", "required": False},
    )

    page: KiCadStr = field(
        default_factory=lambda: KiCadStr("page", "", required=False),
        metadata={"description": "Page settings", "required": False},
    )
    paper: KiCadStr = field(
        default_factory=lambda: KiCadStr("paper", "A4", required=False),
        metadata={"description": "Paper size specification", "required": False},
    )
    layers: Optional[BoardLayers] = field(
        default=None, metadata={"description": "Layer definitions", "required": False}
    )
    setup: Optional[Setup] = field(
        default=None, metadata={"description": "Board setup", "required": False}
    )
    embedded_fonts: KiCadStr = field(
        default_factory=lambda: KiCadStr("embedded_fonts", "", required=False),
        metadata={
            "description": "Whether fonts are embedded (yes/no)",
            "required": False,
        },
    )

    # Multiple elements (lists)
    properties: List[Property] = field(
        default_factory=list, metadata={"description": "Board properties"}
    )
    nets: List[Net] = field(
        default_factory=list, metadata={"description": "Net definitions"}
    )
    footprints: List[Footprint] = field(
        default_factory=list, metadata={"description": "Footprint instances"}
    )
    gr_elements: Optional[List[Union[GrText, GrLine, GrArc, GrPoly]]] = field(
        default_factory=list,
        metadata={
            "description": "List of board graphical elements",
            "required": False,
        },
    )
    arcs: List[BoardArc] = field(
        default_factory=list, metadata={"description": "Arc track segments"}
    )
    groups: List[Group] = field(
        default_factory=list, metadata={"description": "Group definitions"}
    )
    segments: List[Segment] = field(
        default_factory=list, metadata={"description": "Track segments"}
    )
    vias: List[Via] = field(
        default_factory=list, metadata={"description": "Via definitions"}
    )
    zones: List[Zone] = field(
        default_factory=list, metadata={"description": "Zone definitions"}
    )

    @classmethod
    def from_file(
        cls,
        file_path: str,
        strictness: ParseStrictness = ParseStrictness.STRICT,
        encoding: str = "utf-8",
    ) -> "KicadPcb":
        """Parse from S-expression file - convenience method for PCB operations."""
        if not file_path.endswith(".kicad_pcb"):
            raise ValueError("Unsupported file extension. Expected: .kicad_pcb")
        with open(file_path, "r", encoding=encoding) as f:
            content = f.read()
        return cls.from_str(content, strictness)

    def save_to_file(self, file_path: str, encoding: str = "utf-8") -> None:
        """Save to .kicad_pcb file format.

        Args:
            file_path: Path to write the .kicad_pcb file
            encoding: File encoding (default: utf-8)
        """
        if not file_path.endswith(".kicad_pcb"):
            raise ValueError("Unsupported file extension. Expected: .kicad_pcb")
        content = self.to_sexpr_str()
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)
