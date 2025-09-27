"""Footprint library elements for KiCad S-expressions - footprint management and properties."""

from dataclasses import dataclass, field
from typing import List, Optional

from .advanced_graphics import FpArc, FpCircle, FpLine, FpPoly, FpRect, FpText
from .base_element import KiCadObject, OptionalFlag, ParseStrictness
from .base_types import At, Clearance, Layer, Property, Uuid, Width, Xyz
from .pad_and_drill import Pad
from .text_and_documents import Descr, Generator, GeneratorVersion, Tedit, Version


@dataclass
class FileName(KiCadObject):
    """Name definition token for embedded files.

    The 'name' token defines a file name in the format::

        (name "FILENAME")

    Args:
        value: File name string
    """

    __token_name__ = "name"

    value: str = field(default="", metadata={"description": "File name string"})


@dataclass
class FileType(KiCadObject):
    """Type definition token for embedded files.

    The 'type' token defines a file type in the format::

        (type TYPE)

    Args:
        value: File type string
    """

    __token_name__ = "type"

    value: str = field(default="", metadata={"description": "File type string"})


@dataclass
class FileData(KiCadObject):
    """Data definition token for embedded files.

    The 'data' token defines base64 encoded file data in the format::

        (data |DATA_LINE1|
              |DATA_LINE2|
              ...)

    Args:
        lines: List of base64 encoded data lines
    """

    __token_name__ = "data"

    lines: List[str] = field(
        default_factory=list,
        metadata={"description": "List of base64 encoded data lines"},
    )


@dataclass
class FileChecksum(KiCadObject):
    """Checksum definition token for embedded files.

    The 'checksum' token defines a file checksum in the format::

        (checksum "CHECKSUM")

    Args:
        value: File checksum string
    """

    __token_name__ = "checksum"

    value: str = field(default="", metadata={"description": "File checksum string"})


@dataclass
class EmbeddedFile(KiCadObject):
    """Embedded file definition token.

    The 'file' token defines an embedded file in the format::

        (file
            (name "FILENAME")
            (type TYPE)
            [(data |DATA|)]
            [(checksum "CHECKSUM")]
        )

    Args:
        name: File name token
        type: File type token
        data: Base64 encoded file data token (optional)
        checksum: File checksum token (optional)
    """

    __token_name__ = "file"

    name: FileName = field(
        default_factory=lambda: FileName(), metadata={"description": "File name token"}
    )
    type: FileType = field(
        default_factory=lambda: FileType(), metadata={"description": "File type token"}
    )
    data: Optional[FileData] = field(
        default=None,
        metadata={"description": "Base64 encoded file data token", "required": False},
    )
    checksum: Optional[FileChecksum] = field(
        default=None, metadata={"description": "File checksum token", "required": False}
    )


@dataclass
class EmbeddedFiles(KiCadObject):
    """Embedded files container definition token.

    The 'embedded_files' token defines a container for embedded files in the format::

        (embedded_files
            (file ...)
            ...
        )

    Args:
        files: List of embedded files
    """

    __token_name__ = "embedded_files"

    files: List[EmbeddedFile] = field(
        default_factory=list, metadata={"description": "List of embedded files"}
    )


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
    board_only: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("board_only"),
        metadata={
            "description": "Whether footprint is only defined in board",
            "required": False,
        },
    )
    exclude_from_pos_files: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("exclude_from_pos_files"),
        metadata={
            "description": "Whether to exclude from position files",
            "required": False,
        },
    )
    exclude_from_bom: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("exclude_from_bom"),
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
        groups: List of pad group strings
    """

    __token_name__ = "net_tie_pad_groups"

    groups: List[str] = field(
        default_factory=list, metadata={"description": "List of pad group strings"}
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
class ModelAt(KiCadObject):
    """3D model position definition token.

    The 'at' token for 3D models in the format:
    (at (xyz X Y Z))

    Args:
        xyz: 3D coordinates for model position
    """

    __token_name__ = "at"

    xyz: Xyz = field(
        default_factory=lambda: Xyz(),
        metadata={"description": "3D coordinates for model position"},
    )


@dataclass
class ModelScale(KiCadObject):
    """3D model scale definition token.

    The 'scale' token for 3D models in the format:
    (scale (xyz X Y Z))

    Args:
        xyz: 3D scale factors for model
    """

    __token_name__ = "scale"

    xyz: Xyz = field(
        default_factory=lambda: Xyz(x=1.0, y=1.0, z=1.0),
        metadata={"description": "3D scale factors for model"},
    )


@dataclass
class ModelRotate(KiCadObject):
    """3D model rotation definition token.

    The 'rotate' token for 3D models in the format:
    (rotate (xyz X Y Z))

    Args:
        xyz: 3D rotation angles for model
    """

    __token_name__ = "rotate"

    xyz: Xyz = field(
        default_factory=lambda: Xyz(),
        metadata={"description": "3D rotation angles for model"},
    )


@dataclass
class ModelOffset(KiCadObject):
    """3D model offset definition token.

    The 'offset' token for 3D models in the format:
    (offset (xyz X Y Z))

    Args:
        xyz: 3D offset coordinates for model
    """

    __token_name__ = "offset"

    xyz: Xyz = field(
        default_factory=lambda: Xyz(),
        metadata={"description": "3D offset coordinates for model"},
    )


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
        at: 3D position coordinates relative to the footprint (optional)
        scale: Model scale factor for each 3D axis (optional)
        rotate: Model rotation for each 3D axis relative to the footprint (optional)
        offset: Model offset coordinates (optional)
    """

    __token_name__ = "model"

    path: str = field(
        default="", metadata={"description": "Path and file name of the 3D model"}
    )
    at: Optional[ModelAt] = field(
        default=None,
        metadata={
            "description": "3D position coordinates relative to the footprint",
            "required": False,
        },
    )
    scale: Optional[ModelScale] = field(
        default=None,
        metadata={
            "description": "Model scale factor for each 3D axis",
            "required": False,
        },
    )
    rotate: Optional[ModelRotate] = field(
        default=None,
        metadata={
            "description": "Model rotation for each 3D axis relative to the footprint",
            "required": False,
        },
    )
    offset: Optional[ModelOffset] = field(
        default=None,
        metadata={"description": "Model offset coordinates", "required": False},
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
        version: File format version (optional)
        generator: Generator application (optional)
        generator_version: Generator version (optional)
        locked: Whether the footprint cannot be edited (optional)
        placed: Whether the footprint has been placed (optional)
        layer: Layer the footprint is placed on
        tedit: Last edit timestamp (optional)
        uuid: Unique identifier for board footprints (optional)
        at: Position and rotation coordinates (optional)
        descr: Description of the footprint (optional)
        tags: Search tags for the footprint (optional)
        properties: List of footprint properties (optional)
        path: Hierarchical path of linked schematic symbol (optional)
        attr: Footprint attributes (optional)
        autoplace_cost90: Vertical cost for automatic placement (optional)
        autoplace_cost180: Horizontal cost for automatic placement (optional)
        solder_mask_margin: Solder mask distance from pads (optional)
        solder_paste_margin: Solder paste distance from pads (optional)
        solder_paste_ratio: Percentage of pad size for solder paste (optional)
        clearance: Clearance to board copper objects (optional)
        zone_connect: How pads connect to filled zones (optional)
        thermal_width: Thermal relief spoke width (optional)
        thermal_gap: Distance from pad to zone for thermal relief (optional)
        private_layers: List of private layers (optional)
        net_tie_pad_groups: Net tie pad groups (optional)
        pads: List of pads (optional)
        models: List of 3D models (optional)
        fp_rects: List of footprint rectangles (optional)
        fp_circles: List of footprint circles (optional)
        fp_texts: List of footprint texts (optional)
        fp_lines: List of footprint lines (optional)
        fp_arcs: List of footprint arcs (optional)
        fp_polys: List of footprint polygons (optional)
        embedded_fonts: Embedded fonts settings (optional)
        embedded_files: Embedded files container (optional)
    """

    __token_name__ = "footprint"
    __legacy_token_names__ = ["module"]

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
    placed: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("placed"),
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
    descr: Optional[Descr] = field(
        default=None,
        metadata={"description": "Description of the footprint", "required": False},
    )
    tags: Optional[Tags] = field(
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
    fp_lines: Optional[List[FpLine]] = field(
        default_factory=list,
        metadata={"description": "List of footprint lines", "required": False},
    )
    fp_arcs: Optional[List[FpArc]] = field(
        default_factory=list,
        metadata={"description": "List of footprint arcs", "required": False},
    )
    fp_polys: Optional[List[FpPoly]] = field(
        default_factory=list,
        metadata={"description": "List of footprint polygons", "required": False},
    )
    embedded_fonts: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("embedded_fonts"),
        metadata={"description": "Embedded fonts settings", "required": False},
    )
    embedded_files: Optional[EmbeddedFiles] = field(
        default=None,
        metadata={"description": "Embedded files container", "required": False},
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
        content = self.to_sexpr_str()
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
        cost: 180 degree rotation cost
    """

    __token_name__ = "autoplace_cost180"

    cost: int = field(default=0, metadata={"description": "180 degree rotation cost"})


@dataclass
class AutoplaceCost90(KiCadObject):
    """Autoplace cost 90 definition token.

    The 'autoplace_cost90' token defines the vertical cost for automatic placement in the format::

        (autoplace_cost90 COST)

    Args:
        cost: 90 degree rotation cost
    """

    __token_name__ = "autoplace_cost90"

    cost: int = field(default=0, metadata={"description": "90 degree rotation cost"})
