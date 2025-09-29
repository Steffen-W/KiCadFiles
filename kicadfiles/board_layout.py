"""Board layout elements for KiCad S-expressions - PCB/board design and routing."""

from dataclasses import dataclass, field
from typing import Any, List, Optional

from .advanced_graphics import GrText
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
    End,
    Layer,
    Layers,
    Property,
    Start,
    Uuid,
)
from .footprint_library import Footprint
from .pad_and_drill import Net
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
    locked: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("locked"),
        metadata={
            "description": "Whether the line cannot be edited",
            "required": False,
        },
    )
    net: int = field(
        default=0, metadata={"description": "Net ordinal number from net section"}
    )
    tstamp: Optional[KiCadStr] = field(
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
        stackup: Stackup definition (optional)
        pad_to_mask_clearance: Pad to mask clearance
        solder_mask_min_width: Minimum solder mask width (optional)
        pad_to_paste_clearance: Pad to paste clearance (optional)
        pad_to_paste_clearance_ratio: Pad to paste clearance ratio (0-100%) (optional)
        aux_axis_origin: Auxiliary axis origin (X, Y) (optional)
        grid_origin: Grid origin (X, Y) (optional)
        plot_settings: Plot settings (optional)
    """

    __token_name__ = "setup"

    stackup: Optional[dict[Any, Any]] = field(
        default=None, metadata={"description": "Stackup definition", "required": False}
    )
    pad_to_mask_clearance: float = field(
        default=0.0, metadata={"description": "Pad to mask clearance"}
    )
    solder_mask_min_width: Optional[float] = field(
        default=None,
        metadata={"description": "Minimum solder mask width", "required": False},
    )
    pad_to_paste_clearance: Optional[float] = field(
        default=None,
        metadata={"description": "Pad to paste clearance", "required": False},
    )
    pad_to_paste_clearance_ratio: Optional[float] = field(
        default=None,
        metadata={
            "description": "Pad to paste clearance ratio (0-100%)",
            "required": False,
        },
    )
    aux_axis_origin: Optional[tuple[float, float]] = field(
        default=None,
        metadata={"description": "Auxiliary axis origin (X, Y)", "required": False},
    )
    grid_origin: Optional[tuple[float, float]] = field(
        default=None,
        metadata={"description": "Grid origin (X, Y)", "required": False},
    )
    plot_settings: Optional[dict[Any, Any]] = field(
        default=None, metadata={"description": "Plot settings", "required": False}
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
    legacy_teardrops: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("legacy_teardrops"),
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
    locked: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("locked"),
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
    remove_unused_layers: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("remove_unused_layers"),
        metadata={"description": "Remove unused layers flag", "required": False},
    )
    keep_end_layers: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("keep_end_layers"),
        metadata={"description": "Keep end layers flag", "required": False},
    )
    free: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("free"),
        metadata={
            "description": "Whether via is free to move outside assigned net",
            "required": False,
        },
    )
    net: int = field(
        default=0, metadata={"description": "Net ordinal number from net section"}
    )
    tstamp: Optional[KiCadStr] = field(
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
        properties: Board properties
        nets: Net definitions
        footprints: Footprint instances
        gr_texts: Graphical text elements
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
    generator_version: Optional[KiCadStr] = field(
        default_factory=lambda: KiCadStr("generator_version", "", required=False),
        metadata={"description": "Generator version", "required": False},
    )

    # Optional sections
    general: Optional[General] = field(
        default=None,
        metadata={"description": "General board settings", "required": False},
    )

    page: Optional[KiCadStr] = field(
        default_factory=lambda: KiCadStr("page", "", required=False),
        metadata={"description": "Page settings", "required": False},
    )
    paper: Optional[KiCadStr] = field(
        default_factory=lambda: KiCadStr("paper", "A4", required=False),
        metadata={"description": "Paper size specification", "required": False},
    )
    layers: Optional[Layers] = field(
        default=None, metadata={"description": "Layer definitions", "required": False}
    )
    setup: Optional[Setup] = field(
        default=None, metadata={"description": "Board setup", "required": False}
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
    gr_texts: List[GrText] = field(
        default_factory=list, metadata={"description": "Graphical text elements"}
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
