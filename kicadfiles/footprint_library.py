"""Footprint library elements for KiCad S-expressions - footprint management and properties."""

from dataclasses import dataclass, field
from typing import List, Optional

from .advanced_graphics import FpCircle, FpRect, FpText
from .base_element import KiCadObject, OptionalFlag, ParseStrictness
from .base_types import At, Clearance, Layer, Property, Rotate, Uuid, Width, Xyz
from .pad_and_drill import Pad
from .schematic_system import EmbeddedFonts
from .text_and_documents import Generator, GeneratorVersion, Scale, Tedit, Version


@dataclass
class Attr(KiCadObject):
    """Footprint attributes definition token.

    The 'attr' token defines footprint attributes in the format::

        (attr
            TYPE
            [board_only]
            [exclude_from_pos_files]
            [exclude_from_bom]
        )

    Args:
        type: Footprint type (smd | through_hole)
        board_only: Whether footprint is only defined in board (optional)
        exclude_from_pos_files: Whether to exclude from position files (optional)
        exclude_from_bom: Whether to exclude from BOM files (optional)
    """

    __token_name__ = "attr"

    type: str = field(
        default="", metadata={"description": "Footprint type (smd | through_hole)"}
    )
    board_only: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Whether footprint is only defined in board",
            "required": False,
        },
    )
    exclude_from_pos_files: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Whether to exclude from position files",
            "required": False,
        },
    )
    exclude_from_bom: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Whether to exclude from BOM files",
            "required": False,
        },
    )


@dataclass
class NetTiePadGroups(KiCadObject):
    """Net tie pad groups definition token.

    The 'net_tie_pad_groups' token defines groups of pads that are connected in the format::

        (net_tie_pad_groups "PAD_LIST" "PAD_LIST" ...)

    Args:
        groups: List of pad group strings with space-separated pad numbers
    """

    __token_name__ = "net_tie_pad_groups"

    groups: List[str] = field(
        default_factory=list, metadata={"description": "List of pad group strings"}
    )


@dataclass
class OnBoard(KiCadObject):
    """On board flag definition token.

    The 'on_board' token defines whether a footprint should be exported to the PCB in the format::

        (on_board yes | no)

    Args:
        value: Whether footprint is exported to PCB
    """

    __token_name__ = "on_board"

    value: bool = field(
        default=True, metadata={"description": "Whether footprint is exported to PCB"}
    )


@dataclass
class SolderMaskMargin(KiCadObject):
    """Solder mask margin definition token.

    The 'solder_mask_margin' token defines the solder mask distance from all pads in the format::

        (solder_mask_margin MARGIN)

    Args:
        margin: Solder mask margin value
    """

    __token_name__ = "solder_mask_margin"

    margin: float = field(
        default=0.0, metadata={"description": "Solder mask margin value"}
    )


@dataclass
class SolderPasteMargin(KiCadObject):
    """Solder paste margin definition token.

    The 'solder_paste_margin' token defines the solder paste distance from all pads in the format::

        (solder_paste_margin MARGIN)

    Args:
        margin: Solder paste margin value
    """

    __token_name__ = "solder_paste_margin"

    margin: float = field(
        default=0.0, metadata={"description": "Solder paste margin value"}
    )


@dataclass
class SolderPasteMarginRatio(KiCadObject):
    """Solder paste margin ratio definition token.

    The 'solder_paste_margin_ratio' token defines the percentage of pad size for solder paste in the format::

        (solder_paste_margin_ratio RATIO)

    Args:
        ratio: Solder paste margin ratio
    """

    __token_name__ = "solder_paste_margin_ratio"

    ratio: float = field(
        default=0.0, metadata={"description": "Solder paste margin ratio"}
    )


@dataclass
class Tags(KiCadObject):
    """Tags definition token.

    The 'tags' token defines search tags for the footprint in the format::

        (tags "TAG_STRING")

    Args:
        tags: Tag string
    """

    __token_name__ = "tags"

    tags: str = field(default="", metadata={"description": "Tag string"})


@dataclass
class Model(KiCadObject):
    """3D model definition token for footprints.

    The 'model' token defines a 3D model associated with a footprint in the format::

        (model
            "3D_MODEL_FILE"
            (at (xyz X Y Z))
            (scale (xyz X Y Z))
            (rotate (xyz X Y Z))
        )

    Args:
        path: Path and file name of the 3D model
        at: 3D position coordinates relative to the footprint using xyz alternative
        scale: Model scale factor for each 3D axis using xyz alternative
        rotate: Model rotation for each 3D axis relative to the footprint using xyz alternative
    """

    __token_name__ = "model"

    path: str = field(
        default="", metadata={"description": "Path and file name of the 3D model"}
    )
    at: At = field(
        default_factory=lambda: At(xyz=Xyz()),
        metadata={"description": "3D position coordinates relative to the footprint"},
    )
    scale: Scale = field(
        default_factory=lambda: Scale(xyz=Xyz()),
        metadata={"description": "Model scale factor for each 3D axis"},
    )
    rotate: Rotate = field(
        default_factory=lambda: Rotate(xyz=Xyz()),
        metadata={
            "description": "Model rotation for each 3D axis relative to the footprint"
        },
    )


@dataclass
class Footprint(KiCadObject):
    """Footprint definition token that defines a complete footprint.

    The 'footprint' token defines a footprint with all its elements in the format::

        (footprint
            ["LIBRARY_LINK"]
            [locked]
            [placed]
            (layer LAYER_DEFINITIONS)
            (tedit TIME_STAMP)
            [(uuid UUID)]
            [POSITION_IDENTIFIER]
            [(descr "DESCRIPTION")]
            [(tags "NAME")]
            [(property "KEY" "VALUE") ...]
            (path "PATH")
            [(autoplace_cost90 COST)]
            [(autoplace_cost180 COST)]
            [(solder_mask_margin MARGIN)]
            [(solder_paste_margin MARGIN)]
            [(solder_paste_ratio RATIO)]
            [(clearance CLEARANCE)]
            [(zone_connect CONNECTION_TYPE)]
            [(thermal_width WIDTH)]
            [(thermal_gap DISTANCE)]
            [ATTRIBUTES]
            [(private_layers LAYER_DEFINITIONS)]
            [(net_tie_pad_groups PAD_GROUP_DEFINITIONS)]
            GRAPHIC_ITEMS...
            PADS...
            ZONES...
            GROUPS...
            3D_MODEL
        )

    Args:
        library_link: Link to footprint library (optional)
        locked: Whether the footprint cannot be edited (optional)
        placed: Whether the footprint has been placed (optional)
        layer: Layer the footprint is placed on
        tedit: Last edit timestamp
        uuid: Unique identifier for board footprints (optional)
        at: Position and rotation coordinates (optional)
        descr: Description of the footprint (optional)
        tags: Search tags for the footprint (optional)
        properties: List of footprint properties (optional)
        path: Hierarchical path of linked schematic symbol
        autoplace_cost90: Vertical cost for automatic placement (optional)
        autoplace_cost180: Horizontal cost for automatic placement (optional)
        solder_mask_margin: Solder mask distance from pads (optional)
        solder_paste_margin: Solder paste distance from pads (optional)
        solder_paste_ratio: Percentage of pad size for solder paste (optional)
        clearance: Clearance to board copper objects (optional)
        zone_connect: How pads connect to filled zones (optional)
        thermal_width: Thermal relief spoke width (optional)
        thermal_gap: Distance from pad to zone for thermal relief (optional)
        attr: Footprint attributes (optional)
        private_layers: List of private layers (optional)
        net_tie_pad_groups: Net tie pad groups (optional)
        pads: List of pads (optional)
        models: List of 3D models (optional)
    """

    __token_name__ = "footprint"

    library_link: Optional[str] = field(
        default=None,
        metadata={"description": "Link to footprint library", "required": False},
    )
    version: Optional[Version] = field(
        default=None, metadata={"description": "File format version", "required": False}
    )
    generator: Optional[Generator] = field(
        default=None,
        metadata={"description": "Generator application", "required": False},
    )
    generator_version: Optional[GeneratorVersion] = field(
        default=None, metadata={"description": "Generator version", "required": False}
    )
    locked: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("locked"),
        metadata={
            "description": "Whether the footprint cannot be edited",
            "required": False,
        },
    )
    placed: Optional[bool] = field(
        default=None,
        metadata={
            "description": "Whether the footprint has been placed",
            "required": False,
        },
    )
    layer: Layer = field(
        default_factory=lambda: Layer(),
        metadata={"description": "Layer the footprint is placed on"},
    )
    tedit: Optional[Tedit] = field(
        default=None, metadata={"description": "Last edit timestamp", "required": False}
    )
    uuid: Optional[Uuid] = field(
        default=None,
        metadata={
            "description": "Unique identifier for board footprints",
            "required": False,
        },
    )
    at: Optional[At] = field(
        default=None,
        metadata={
            "description": "Position and rotation coordinates",
            "required": False,
        },
    )
    descr: Optional[str] = field(
        default=None,
        metadata={"description": "Description of the footprint", "required": False},
    )
    tags: Optional[str] = field(
        default=None,
        metadata={"description": "Search tags for the footprint", "required": False},
    )
    properties: Optional[List[Property]] = field(
        default_factory=list,
        metadata={"description": "List of footprint properties", "required": False},
    )
    path: Optional[str] = field(
        default=None,
        metadata={
            "description": "Hierarchical path of linked schematic symbol",
            "required": False,
        },
    )
    attr: Optional[Attr] = field(
        default=None,
        metadata={"description": "Footprint attributes", "required": False},
    )
    autoplace_cost90: Optional[int] = field(
        default=None,
        metadata={
            "description": "Vertical cost for automatic placement",
            "required": False,
        },
    )
    autoplace_cost180: Optional[int] = field(
        default=None,
        metadata={
            "description": "Horizontal cost for automatic placement",
            "required": False,
        },
    )
    solder_mask_margin: Optional[float] = field(
        default=None,
        metadata={"description": "Solder mask distance from pads", "required": False},
    )
    solder_paste_margin: Optional[float] = field(
        default=None,
        metadata={"description": "Solder paste distance from pads", "required": False},
    )
    solder_paste_ratio: Optional[float] = field(
        default=None,
        metadata={
            "description": "Percentage of pad size for solder paste",
            "required": False,
        },
    )
    clearance: Optional[Clearance] = field(
        default=None,
        metadata={
            "description": "Clearance to board copper objects",
            "required": False,
        },
    )
    zone_connect: Optional[int] = field(
        default=None,
        metadata={"description": "How pads connect to filled zones", "required": False},
    )
    thermal_width: Optional[Width] = field(
        default=None,
        metadata={"description": "Thermal relief spoke width", "required": False},
    )
    thermal_gap: Optional[Clearance] = field(
        default=None,
        metadata={
            "description": "Distance from pad to zone for thermal relief",
            "required": False,
        },
    )
    private_layers: Optional[List[str]] = field(
        default_factory=list,
        metadata={"description": "List of private layers", "required": False},
    )
    net_tie_pad_groups: Optional[NetTiePadGroups] = field(
        default=None, metadata={"description": "Net tie pad groups", "required": False}
    )
    pads: Optional[List[Pad]] = field(
        default_factory=list,
        metadata={"description": "List of pads", "required": False},
    )
    models: Optional[List[Model]] = field(
        default_factory=list,
        metadata={"description": "List of 3D models", "required": False},
    )
    fp_rects: Optional[List[FpRect]] = field(
        default_factory=list,
        metadata={"description": "List of footprint rectangles", "required": False},
    )
    fp_circles: Optional[List[FpCircle]] = field(
        default_factory=list,
        metadata={"description": "List of footprint circles", "required": False},
    )
    fp_texts: Optional[List[FpText]] = field(
        default_factory=list,
        metadata={"description": "List of footprint texts", "required": False},
    )
    embedded_fonts: Optional[EmbeddedFonts] = field(
        default=None,
        metadata={"description": "Embedded fonts settings", "required": False},
    )

    @classmethod
    def from_file(
        cls,
        file_path: str,
        strictness: ParseStrictness = ParseStrictness.STRICT,
        encoding: str = "utf-8",
    ) -> "Footprint":
        """Parse from S-expression file - convenience method for footprint operations."""
        if not file_path.endswith(".kicad_mod"):
            raise ValueError("Unsupported file extension. Expected: .kicad_mod")
        with open(file_path, "r", encoding=encoding) as f:
            content = f.read()
        return cls.from_str(content, strictness)

    def save_to_file(self, file_path: str, encoding: str = "utf-8") -> None:
        """Save to .kicad_mod file format.

        Args:
            file_path: Path to write the .kicad_mod file
            encoding: File encoding (default: utf-8)
        """
        if not file_path.endswith(".kicad_mod"):
            raise ValueError("Unsupported file extension. Expected: .kicad_mod")
        content = self.to_sexpr_str(pretty_print=True)
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)


@dataclass
class Footprints(KiCadObject):
    """Footprints container token.

    The 'footprints' token defines a container for multiple footprints in the format::

        (footprints
            (footprint ...)
            ...
        )

    Args:
        footprints: List of footprints
    """

    __token_name__ = "footprints"

    footprints: List[Footprint] = field(
        default_factory=list, metadata={"description": "List of footprints"}
    )


@dataclass
class AutoplaceCost180(KiCadObject):
    """Autoplace cost 180 definition token.

    The 'autoplace_cost180' token defines the horizontal cost for automatic placement in the format::

        (autoplace_cost180 COST)

    Args:
        cost: Horizontal cost for automatic placement (1-10)
    """

    __token_name__ = "autoplace_cost180"

    cost: int = field(default=0, metadata={"description": "180 degree rotation cost"})


@dataclass
class AutoplaceCost90(KiCadObject):
    """Autoplace cost 90 definition token.

    The 'autoplace_cost90' token defines the vertical cost for automatic placement in the format::

        (autoplace_cost90 COST)

    Args:
        cost: Vertical cost for automatic placement (1-10)
    """

    __token_name__ = "autoplace_cost90"

    cost: int = field(default=0, metadata={"description": "90 degree rotation cost"})
