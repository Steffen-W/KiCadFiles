"""Board layout elements for KiCad S-expressions - PCB/board design and routing."""

from dataclasses import dataclass, field
from typing import Any, Optional

from .advanced_graphics import GrText
from .base_element import KiCadObject, ParseStrictness
from .base_types import (
    At,
    Diameter,
    End,
    Layer,
    Locked,
    Property,
    Start,
    Tstamp,
    Width,
)
from .footprint_library import Footprint
from .pad_and_drill import Net
from .text_and_documents import Generator, Page, Version
from .zone_system import Zone


@dataclass
class ViaSize(KiCadObject):
    """Via size definition token.

    The 'size' token for via defines a diameter value in the format::

        (size DIAMETER)

    Args:
        diameter: The diameter value of the via
    """

    __token_name__ = "size"

    diameter: float = field(default=0.0, metadata={"description": "Via diameter value"})


@dataclass
class General(KiCadObject):
    """General board settings definition token.

    The 'general' token defines general information about the board in the format::

        (general
            (thickness THICKNESS)
        )

    Args:
        thickness: Overall board thickness
    """

    __token_name__ = "general"

    thickness: float = field(
        default=1.6, metadata={"description": "Overall board thickness"}
    )


@dataclass
class Layers(KiCadObject):
    """Board layers definition token.

    The 'layers' token defines all layers used by the board in the format::

        (layers
            (
                ORDINAL
                "CANONICAL_NAME"
                TYPE
                ["USER_NAME"]
            )
            ;; remaining layers...
        )

    Args:
        layer_definitions: List of layer definitions (ordinal, canonical_name, type, user_name)
    """

    __token_name__ = "layers"

    layer_definitions: list[tuple[Any, ...]] = field(
        default_factory=list,
        metadata={
            "description": "List of layer definitions (ordinal, canonical_name, type, user_name)"
        },
    )


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

    net_definitions: list[tuple[Any, ...]] = field(
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

    layers: list[str] = field(
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
        tstamp: Unique identifier of the line object
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
    width: Width = field(
        default_factory=lambda: Width(), metadata={"description": "Line width"}
    )
    layer: Layer = field(
        default_factory=lambda: Layer(),
        metadata={"description": "Layer the track segment resides on"},
    )
    locked: Optional[Locked] = field(
        default=None,
        metadata={
            "description": "Whether the line cannot be edited",
            "required": False,
        },
    )
    net: int = field(
        default=0, metadata={"description": "Net ordinal number from net section"}
    )
    tstamp: Tstamp = field(
        default_factory=lambda: Tstamp(),
        metadata={"description": "Unique identifier of the line object"},
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
        stackup: Stack-up settings for board manufacturing (optional)
        pad_to_mask_clearance: Clearance between footprint pads and solder mask
        solder_mask_min_width: Minimum solder mask width (optional)
        pad_to_paste_clearance: Clearance between footprint pads and solder paste (optional)
        pad_to_paste_clearance_ratio: Percentage of pad size for solder paste (optional)
        aux_axis_origin: Auxiliary axis origin coordinates (optional)
        grid_origin: Grid origin coordinates (optional)
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

    segments: list[Segment] = field(
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
        type: Via type (blind | micro) (optional, default is through hole)
        locked: Whether the line cannot be edited (optional)
        at: Coordinates of the center of the via
        size: Diameter of the via annular ring
        drill: Drill diameter of the via
        layers: Layer set the via connects
        remove_unused_layers: Remove unused layers flag (optional)
        keep_end_layers: Keep end layers flag (optional)
        free: Whether via is free to move outside assigned net (optional)
        net: Net ordinal number from net section
        tstamp: Unique identifier of the line object
    """

    __token_name__ = "via"

    type: Optional[str] = field(
        default=None,
        metadata={"description": "Via type (blind | micro)", "required": False},
    )
    locked: Optional[Locked] = field(
        default=None,
        metadata={
            "description": "Whether the line cannot be edited",
            "required": False,
        },
    )
    at: At = field(
        default_factory=lambda: At(),
        metadata={"description": "Coordinates of the center of the via"},
    )
    size: ViaSize = field(
        default_factory=lambda: ViaSize(),
        metadata={"description": "Diameter of the via annular ring"},
    )
    drill: Diameter = field(
        default_factory=lambda: Diameter(),
        metadata={"description": "Drill diameter of the via"},
    )
    layers: list[str] = field(
        default_factory=list, metadata={"description": "Layer set the via connects"}
    )
    remove_unused_layers: Optional[bool] = field(
        default=None,
        metadata={"description": "Remove unused layers flag", "required": False},
    )
    keep_end_layers: Optional[bool] = field(
        default=None,
        metadata={"description": "Keep end layers flag", "required": False},
    )
    free: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Whether via is free to move outside assigned net",
            "required": False,
        },
    )
    net: int = field(
        default=0, metadata={"description": "Net ordinal number from net section"}
    )
    tstamp: Tstamp = field(
        default_factory=lambda: Tstamp(),
        metadata={"description": "Unique identifier of the line object"},
    )


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

    vias: list[Via] = field(
        default_factory=list, metadata={"description": "List of vias"}
    )


@dataclass
class NetName(KiCadObject):
    """Net name definition token.

    The 'net_name' token defines a net name in the format::

        (net_name "NAME")

    Args:
        name: Net name
    """

    __token_name__ = "net_name"

    name: str = field(default="", metadata={"description": "Net name"})


@dataclass
class Orientation(KiCadObject):
    """Orientation definition token.

    The 'orientation' token defines an orientation angle in the format::

        (orientation ANGLE)

    Args:
        angle: Orientation angle in degrees
    """

    __token_name__ = "orientation"

    angle: float = field(
        default=0.0, metadata={"description": "Orientation angle in degrees"}
    )


@dataclass
class Path(KiCadObject):
    """Hierarchical path definition token.

    The 'path' token defines a hierarchical path in the format::

        (path "PATH_STRING")

    Args:
        path: Hierarchical path string
    """

    __token_name__ = "path"

    path: str = field(default="", metadata={"description": "Hierarchical path string"})


@dataclass
class KicadPcb(KiCadObject):
    """KiCad PCB board file definition.

    The 'kicad_pcb' token defines a complete PCB board file in the format::

        (kicad_pcb
            (version VERSION)
            (generator GENERATOR)
            (general ...)
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
        version: File format version string
        generator: Generator application name
        general: General board settings (required)
        page: Page settings (optional)
        layers: Layer definitions (optional)
        setup: Board setup parameters (optional)
        properties: Board properties list
        nets: Net definitions list
        footprints: Footprint instances list
        gr_texts: Graphical text elements list
        segments: Track segments list
        vias: Via definitions list
        zones: Zone definitions list
    """

    __token_name__ = "kicad_pcb"

    # Required header fields
    version: Version = field(
        default_factory=lambda: Version(),
        metadata={"description": "File format version"},
    )
    generator: Generator = field(
        default_factory=lambda: Generator(),
        metadata={"description": "Generator application"},
    )

    # Required sections
    general: General = field(
        default_factory=lambda: General(),
        metadata={"description": "General board settings"},
    )

    # Optional sections
    page: Optional[Page] = field(
        default=None, metadata={"description": "Page settings", "required": False}
    )
    layers: Optional[Layers] = field(
        default=None, metadata={"description": "Layer definitions", "required": False}
    )
    setup: Optional[Setup] = field(
        default=None, metadata={"description": "Board setup", "required": False}
    )

    # Multiple elements (lists)
    properties: list[Property] = field(
        default_factory=list, metadata={"description": "Board properties"}
    )
    nets: list[Net] = field(
        default_factory=list, metadata={"description": "Net definitions"}
    )
    footprints: list[Footprint] = field(
        default_factory=list, metadata={"description": "Footprint instances"}
    )
    gr_texts: list[GrText] = field(
        default_factory=list, metadata={"description": "Graphical text elements"}
    )
    segments: list[Segment] = field(
        default_factory=list, metadata={"description": "Track segments"}
    )
    vias: list[Via] = field(
        default_factory=list, metadata={"description": "Via definitions"}
    )
    zones: list[Zone] = field(
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
        content = self.to_sexpr_str(pretty_print=True)
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)
