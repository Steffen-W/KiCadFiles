"""Board layout elements for KiCad S-expressions - PCB/board design and routing."""

from dataclasses import dataclass, field
from typing import Any, ClassVar, List, Optional, Union

from .advanced_graphics import GrArc, GrLine, GrPoly, GrText
from .base_element import (
    NamedFloat,
    NamedInt,
    NamedObject,
    NamedString,
    ParseStrictness,
    TokenFlag,
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
class Nets(NamedObject):
    """Nets section definition token.

    The 'nets' token defines nets for the board in the format::

        (net
            ORDINAL
            "NET_NAME"
        )

    Args:
        net_definitions: List of net definitions (ordinal, net_name)
    """

    __token_name__: ClassVar[str] = "nets"

    net_definitions: List[tuple[Any, ...]] = field(
        default_factory=list,
        metadata={"description": "List of net definitions (ordinal, net_name)"},
    )


@dataclass
class PrivateLayers(NamedObject):
    """Private layers definition token.

    The 'private_layers' token defines layers private to specific elements in the format::

        (private_layers "LAYER_LIST")

    Args:
        layers: List of private layer names
    """

    __token_name__: ClassVar[str] = "private_layers"

    layers: List[str] = field(
        default_factory=list, metadata={"description": "List of private layer names"}
    )


@dataclass
class Segment(NamedObject):
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

    __token_name__: ClassVar[str] = "segment"

    start: Start = field(
        default_factory=lambda: Start(),
        metadata={"description": "Coordinates of the beginning of the line"},
    )
    end: End = field(
        default_factory=lambda: End(),
        metadata={"description": "Coordinates of the end of the line"},
    )
    width: NamedFloat = field(
        default_factory=lambda: NamedFloat("width", 0.0),
        metadata={"description": "Line width"},
    )
    layer: Layer = field(
        default_factory=lambda: Layer(),
        metadata={"description": "Layer the track segment resides on"},
    )
    locked: TokenFlag = field(
        default_factory=lambda: TokenFlag("locked"),
        metadata={
            "description": "Whether the line cannot be edited",
            "required": False,
        },
    )
    net: NamedInt = field(
        default_factory=lambda: NamedInt(token="net", value=0),
        metadata={"description": "Net ordinal number from net section"},
    )
    tstamp: NamedString = field(
        default_factory=lambda: NamedString("tstamp", ""),
        metadata={
            "description": "Unique identifier of the line object",
            "required": False,
        },
    )  # NEW Variant
    uuid: Optional[Uuid] = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )  # Old Variant


@dataclass
class Tenting(NamedObject):
    """Tenting configuration for front/back sides.

    Args:
        sides: List of sides (front/back)
    """

    __token_name__: ClassVar[str] = "tenting"

    sides: List[str] = field(
        default_factory=list, metadata={"description": "List of sides (front/back)"}
    )


@dataclass
class PcbPlotParams(NamedObject):
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

    __token_name__: ClassVar[str] = "pcbplotparams"

    layerselection: NamedString = field(
        default_factory=lambda: NamedString(
            "layerselection", "0x00000000_00000000_55555555_5755f5ff"
        ),
        metadata={"description": "Layer selection hex mask", "required": False},
    )
    plot_on_all_layers_selection: NamedString = field(
        default_factory=lambda: NamedString(
            "plot_on_all_layers_selection", "0x00000000_00000000_00000000_00000000"
        ),
        metadata={"description": "Plot on all layers selection", "required": False},
    )
    disableapertmacros: TokenFlag = field(
        default_factory=lambda: TokenFlag("disableapertmacros", "no"),
        metadata={"description": "Disable aperture macros", "required": False},
    )
    usegerberextensions: TokenFlag = field(
        default_factory=lambda: TokenFlag("usegerberextensions", "no"),
        metadata={"description": "Use gerber extensions", "required": False},
    )
    usegerberattributes: TokenFlag = field(
        default_factory=lambda: TokenFlag("usegerberattributes", "yes"),
        metadata={"description": "Use gerber attributes", "required": False},
    )
    usegerberadvancedattributes: TokenFlag = field(
        default_factory=lambda: TokenFlag("usegerberadvancedattributes", "yes"),
        metadata={"description": "Use gerber advanced attributes", "required": False},
    )
    creategerberjobfile: TokenFlag = field(
        default_factory=lambda: TokenFlag("creategerberjobfile", "yes"),
        metadata={"description": "Create gerber job file", "required": False},
    )
    dashed_line_dash_ratio: NamedFloat = field(
        default_factory=lambda: NamedFloat("dashed_line_dash_ratio", 12.0),
        metadata={"description": "Dashed line dash ratio", "required": False},
    )
    dashed_line_gap_ratio: NamedFloat = field(
        default_factory=lambda: NamedFloat("dashed_line_gap_ratio", 3.0),
        metadata={"description": "Dashed line gap ratio", "required": False},
    )
    svgprecision: NamedInt = field(
        default_factory=lambda: NamedInt("svgprecision", 4),
        metadata={"description": "SVG precision", "required": False},
    )
    plotframeref: TokenFlag = field(
        default_factory=lambda: TokenFlag("plotframeref", "no"),
        metadata={"description": "Plot frame reference", "required": False},
    )
    mode: NamedInt = field(
        default_factory=lambda: NamedInt("mode", 1),
        metadata={"description": "Plot mode", "required": False},
    )
    useauxorigin: TokenFlag = field(
        default_factory=lambda: TokenFlag("useauxorigin", "no"),
        metadata={"description": "Use auxiliary origin", "required": False},
    )
    hpglpennumber: NamedInt = field(
        default_factory=lambda: NamedInt("hpglpennumber", 1),
        metadata={"description": "HPGL pen number", "required": False},
    )
    hpglpenspeed: NamedInt = field(
        default_factory=lambda: NamedInt("hpglpenspeed", 20),
        metadata={"description": "HPGL pen speed", "required": False},
    )
    hpglpendiameter: NamedFloat = field(
        default_factory=lambda: NamedFloat("hpglpendiameter", 15.0),
        metadata={"description": "HPGL pen diameter", "required": False},
    )
    pdf_front_fp_property_popups: TokenFlag = field(
        default_factory=lambda: TokenFlag("pdf_front_fp_property_popups", "yes"),
        metadata={
            "description": "PDF front footprint property popups",
            "required": False,
        },
    )
    pdf_back_fp_property_popups: TokenFlag = field(
        default_factory=lambda: TokenFlag("pdf_back_fp_property_popups", "yes"),
        metadata={
            "description": "PDF back footprint property popups",
            "required": False,
        },
    )
    pdf_metadata: TokenFlag = field(
        default_factory=lambda: TokenFlag("pdf_metadata", "yes"),
        metadata={"description": "PDF metadata", "required": False},
    )
    pdf_single_document: TokenFlag = field(
        default_factory=lambda: TokenFlag("pdf_single_document", "no"),
        metadata={"description": "PDF single document", "required": False},
    )
    dxfpolygonmode: TokenFlag = field(
        default_factory=lambda: TokenFlag("dxfpolygonmode", "yes"),
        metadata={"description": "DXF polygon mode", "required": False},
    )
    dxfimperialunits: TokenFlag = field(
        default_factory=lambda: TokenFlag("dxfimperialunits", "yes"),
        metadata={"description": "DXF imperial units", "required": False},
    )
    dxfusepcbnewfont: TokenFlag = field(
        default_factory=lambda: TokenFlag("dxfusepcbnewfont", "yes"),
        metadata={"description": "DXF use pcbnew font", "required": False},
    )
    psnegative: TokenFlag = field(
        default_factory=lambda: TokenFlag("psnegative", "no"),
        metadata={"description": "PS negative", "required": False},
    )
    psa4output: TokenFlag = field(
        default_factory=lambda: TokenFlag("psa4output", "no"),
        metadata={"description": "PS A4 output", "required": False},
    )
    plot_black_and_white: TokenFlag = field(
        default_factory=lambda: TokenFlag("plot_black_and_white", "yes"),
        metadata={"description": "Plot black and white", "required": False},
    )
    plotinvisibletext: TokenFlag = field(
        default_factory=lambda: TokenFlag("plotinvisibletext", "no"),
        metadata={"description": "Plot invisible text", "required": False},
    )
    sketchpadsonfab: TokenFlag = field(
        default_factory=lambda: TokenFlag("sketchpadsonfab", "no"),
        metadata={"description": "Sketch pads on fab", "required": False},
    )
    plotpadnumbers: TokenFlag = field(
        default_factory=lambda: TokenFlag("plotpadnumbers", "no"),
        metadata={"description": "Plot pad numbers", "required": False},
    )
    hidednponfab: TokenFlag = field(
        default_factory=lambda: TokenFlag("hidednponfab", "no"),
        metadata={"description": "Hide DNP on fab", "required": False},
    )
    sketchdnponfab: TokenFlag = field(
        default_factory=lambda: TokenFlag("sketchdnponfab", "yes"),
        metadata={"description": "Sketch DNP on fab", "required": False},
    )
    crossoutdnponfab: TokenFlag = field(
        default_factory=lambda: TokenFlag("crossoutdnponfab", "yes"),
        metadata={"description": "Cross out DNP on fab", "required": False},
    )
    subtractmaskfromsilk: TokenFlag = field(
        default_factory=lambda: TokenFlag("subtractmaskfromsilk", "no"),
        metadata={"description": "Subtract mask from silk", "required": False},
    )
    outputformat: NamedInt = field(
        default_factory=lambda: NamedInt("outputformat", 1),
        metadata={"description": "Output format", "required": False},
    )
    mirror: TokenFlag = field(
        default_factory=lambda: TokenFlag("mirror", "no"),
        metadata={"description": "Mirror", "required": False},
    )
    drillshape: NamedInt = field(
        default_factory=lambda: NamedInt("drillshape", 1),
        metadata={"description": "Drill shape", "required": False},
    )
    scaleselection: NamedInt = field(
        default_factory=lambda: NamedInt("scaleselection", 1),
        metadata={"description": "Scale selection", "required": False},
    )
    outputdirectory: NamedString = field(
        default_factory=lambda: NamedString("outputdirectory", ""),
        metadata={"description": "Output directory", "required": False},
    )


@dataclass
class StackupLayer(NamedObject):
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

    __token_name__: ClassVar[str] = "layer"

    name: str = field(default="", metadata={"description": "Layer name"})
    type: NamedString = field(
        default_factory=lambda: NamedString("type", ""),
        metadata={"description": "Layer type", "required": False},
    )
    color: NamedString = field(
        default_factory=lambda: NamedString("color", ""),
        metadata={"description": "Layer color", "required": False},
    )
    thickness: NamedFloat = field(
        default_factory=lambda: NamedFloat("thickness", 0.0),
        metadata={"description": "Layer thickness", "required": False},
    )
    material: NamedString = field(
        default_factory=lambda: NamedString("material", ""),
        metadata={"description": "Material name", "required": False},
    )
    epsilon_r: NamedFloat = field(
        default_factory=lambda: NamedFloat("epsilon_r", 0.0),
        metadata={"description": "Relative permittivity", "required": False},
    )
    loss_tangent: NamedFloat = field(
        default_factory=lambda: NamedFloat("loss_tangent", 0.0),
        metadata={"description": "Loss tangent", "required": False},
    )


@dataclass
class Stackup(NamedObject):
    """PCB stackup configuration.

    Args:
        layers: List of stackup layers
        copper_finish: Copper finish specification (optional)
        dielectric_constraints: Dielectric constraints flag (optional)
    """

    __token_name__: ClassVar[str] = "stackup"

    layers: List[StackupLayer] = field(
        default_factory=list,
        metadata={"description": "List of stackup layers"},
    )
    copper_finish: NamedString = field(
        default_factory=lambda: NamedString("copper_finish", ""),
        metadata={"description": "Copper finish specification", "required": False},
    )
    dielectric_constraints: TokenFlag = field(
        default_factory=lambda: TokenFlag("dielectric_constraints", "no"),
        metadata={"description": "Dielectric constraints flag", "required": False},
    )


@dataclass
class Setup(NamedObject):
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

    __token_name__: ClassVar[str] = "setup"

    stackup: Optional["Stackup"] = field(
        default=None,
        metadata={"description": "Stackup configuration", "required": False},
    )
    pad_to_mask_clearance: NamedFloat = field(
        default_factory=lambda: NamedFloat("pad_to_mask_clearance", 0.0),
        metadata={"description": "Pad to mask clearance", "required": False},
    )
    allow_soldermask_bridges_in_footprints: TokenFlag = field(
        default_factory=lambda: TokenFlag(
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
class General(NamedObject):
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

    __token_name__: ClassVar[str] = "general"

    thickness: NamedFloat = field(
        default_factory=lambda: NamedFloat("thickness", 1.6),
        metadata={"description": "Board thickness"},
    )
    legacy_teardrops: TokenFlag = field(
        default_factory=lambda: TokenFlag("legacy_teardrops"),
        metadata={
            "description": "Whether to use legacy teardrops",
            "required": False,
        },
    )


@dataclass
class Tracks(NamedObject):
    """Tracks container definition token.

    The 'tracks' token defines a container for track segments in the format::

        (tracks
            (segment ...)
            ...
        )

    Args:
        segments: List of track segments
    """

    __token_name__: ClassVar[str] = "tracks"

    segments: List[Segment] = field(
        default_factory=list, metadata={"description": "List of track segments"}
    )


@dataclass
class Via(NamedObject):
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

    __token_name__: ClassVar[str] = "via"

    type: Optional[str] = field(
        default=None,
        metadata={"description": "Via type (blind | micro)", "required": False},
    )
    locked: TokenFlag = field(
        default_factory=lambda: TokenFlag("locked"),
        metadata={
            "description": "Whether the line cannot be edited",
            "required": False,
        },
    )
    at: At = field(
        default_factory=lambda: At(),
        metadata={"description": "Coordinates of the center of the via"},
    )
    size: NamedFloat = field(
        default_factory=lambda: NamedFloat("size", 0.0),
        metadata={"description": "Diameter of the via annular ring"},
    )
    drill: NamedFloat = field(
        default_factory=lambda: NamedFloat("drill", 0.0),
        metadata={"description": "Drill diameter of the via"},
    )
    layers: Layers = field(
        default_factory=lambda: Layers(),
        metadata={"description": "Layer set the via connects"},
    )
    remove_unused_layers: TokenFlag = field(
        default_factory=lambda: TokenFlag("remove_unused_layers"),
        metadata={"description": "Remove unused layers flag", "required": False},
    )
    keep_end_layers: TokenFlag = field(
        default_factory=lambda: TokenFlag("keep_end_layers"),
        metadata={"description": "Keep end layers flag", "required": False},
    )
    free: TokenFlag = field(
        default_factory=lambda: TokenFlag("free"),
        metadata={
            "description": "Whether via is free to move outside assigned net",
            "required": False,
        },
    )
    net: NamedInt = field(
        default_factory=lambda: NamedInt(token="net", value=0),
        metadata={"description": "Net ordinal number from net section"},
    )
    tstamp: NamedString = field(
        default_factory=lambda: NamedString("tstamp", ""),
        metadata={
            "description": "Unique identifier of the line object",
            "required": False,
        },
    )  # NEW Variant
    uuid: Optional[Uuid] = field(
        default_factory=lambda: Uuid(), metadata={"description": "Unique identifier"}
    )  # Old Variant


@dataclass
class Vias(NamedObject):
    """Vias container definition token.

    The 'vias' token defines a container for vias in the format::

        (vias
            (via ...)
            ...
        )

    Args:
        vias: List of vias
    """

    __token_name__: ClassVar[str] = "vias"

    vias: List[Via] = field(
        default_factory=list, metadata={"description": "List of vias"}
    )


@dataclass
class BoardArc(NamedObject):
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

    __token_name__: ClassVar[str] = "arc"

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
    width: NamedFloat = field(
        default_factory=lambda: NamedFloat("width", 0.0),
        metadata={"description": "Track width"},
    )
    layer: NamedString = field(
        default_factory=lambda: NamedString("layer", ""),
        metadata={"description": "Layer name"},
    )
    net: NamedInt = field(
        default_factory=lambda: NamedInt("net", 0),
        metadata={"description": "Net number"},
    )
    uuid: Optional[Uuid] = field(
        default_factory=lambda: Uuid(),
        metadata={"description": "Unique identifier", "required": False},
    )


@dataclass
class KicadPcb(NamedObject):
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

    __token_name__: ClassVar[str] = "kicad_pcb"

    # Required header fields
    version: NamedInt = field(
        default_factory=lambda: NamedInt("version", 20240101),
        metadata={"description": "File format version"},
    )
    generator: NamedString = field(
        default_factory=lambda: NamedString("generator", ""),
        metadata={"description": "Generator application"},
    )
    generator_version: NamedString = field(
        default_factory=lambda: NamedString("generator_version", ""),
        metadata={"description": "Generator version", "required": False},
    )

    # Optional sections
    general: Optional[General] = field(
        default=None,
        metadata={"description": "General board settings", "required": False},
    )

    page: NamedString = field(
        default_factory=lambda: NamedString("page", ""),
        metadata={"description": "Page settings", "required": False},
    )
    paper: NamedString = field(
        default_factory=lambda: NamedString("paper", "A4"),
        metadata={"description": "Paper size specification", "required": False},
    )
    layers: Optional[BoardLayers] = field(
        default=None, metadata={"description": "Layer definitions", "required": False}
    )
    setup: Optional[Setup] = field(
        default=None, metadata={"description": "Board setup", "required": False}
    )
    embedded_fonts: NamedString = field(
        default_factory=lambda: NamedString("embedded_fonts", ""),
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
