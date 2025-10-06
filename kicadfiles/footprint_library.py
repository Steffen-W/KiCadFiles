"""Footprint library elements for KiCad S-expressions - footprint management and properties."""

from dataclasses import dataclass, field
from typing import ClassVar, List, Optional, Union

from .advanced_graphics import FpArc, FpCircle, FpCurve, FpLine, FpPoly, FpRect, FpText
from .base_element import (
    NamedFloat,
    NamedInt,
    NamedObject,
    NamedString,
    ParseStrictness,
    TokenFlag,
)
from .base_types import At, Layer, Property, Uuid, Xyz
from .pad_and_drill import Pad


@dataclass
class FileData(NamedObject):
    """Data definition token for embedded files.

    The 'data' token defines base64 encoded file data in the format::

        (data |DATA_LINE1|
              |DATA_LINE2|
              ...)

    Args:
        lines: List of base64 encoded data lines
    """

    __token_name__: ClassVar[str] = "data"

    lines: List[str] = field(
        default_factory=list,
        metadata={"description": "List of base64 encoded data lines"},
    )


@dataclass
class EmbeddedFile(NamedObject):
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

    __token_name__: ClassVar[str] = "file"

    name: NamedString = field(
        default_factory=lambda: NamedString("name", ""),
        metadata={"description": "File name token"},
    )
    type: NamedString = field(
        default_factory=lambda: NamedString("type", ""),
        metadata={"description": "File type token"},
    )
    data: Optional[FileData] = field(
        default=None,
        metadata={"description": "Base64 encoded file data token", "required": False},
    )
    checksum: NamedString = field(
        default_factory=lambda: NamedString("checksum", ""),
        metadata={"description": "File checksum token", "required": False},
    )


@dataclass
class EmbeddedFiles(NamedObject):
    """Embedded files container definition token.

    The 'embedded_files' token defines a container for embedded files in the format::

        (embedded_files
            (file ...)
            ...
        )

    Args:
        files: List of embedded files
    """

    __token_name__: ClassVar[str] = "embedded_files"

    files: List[EmbeddedFile] = field(
        default_factory=list, metadata={"description": "List of embedded files"}
    )


@dataclass
class Attr(NamedObject):
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
        allow_soldermask_bridges: Whether to allow soldermask bridges (optional)
    """

    __token_name__: ClassVar[str] = "attr"

    type: str = field(
        default="", metadata={"description": "Footprint type (smd | through_hole)"}
    )
    board_only: TokenFlag = field(
        default_factory=lambda: TokenFlag("board_only"),
        metadata={
            "description": "Whether footprint is only defined in board",
            "required": False,
        },
    )
    exclude_from_pos_files: TokenFlag = field(
        default_factory=lambda: TokenFlag("exclude_from_pos_files"),
        metadata={
            "description": "Whether to exclude from position files",
            "required": False,
        },
    )
    exclude_from_bom: TokenFlag = field(
        default_factory=lambda: TokenFlag("exclude_from_bom"),
        metadata={
            "description": "Whether to exclude from BOM files",
            "required": False,
        },
    )
    allow_soldermask_bridges: TokenFlag = field(
        default_factory=lambda: TokenFlag("allow_soldermask_bridges"),
        metadata={
            "description": "Whether to allow soldermask bridges",
            "required": False,
        },
    )


@dataclass
class NetTiePadGroups(NamedObject):
    """Net tie pad groups definition token.

    The 'net_tie_pad_groups' token defines groups of pads that are connected in the format::

        (net_tie_pad_groups "PAD_LIST" "PAD_LIST" ...)

    Args:
        groups: List of pad group strings
    """

    __token_name__: ClassVar[str] = "net_tie_pad_groups"

    groups: List[str] = field(
        default_factory=list, metadata={"description": "List of pad group strings"}
    )


@dataclass
class ModelAt(NamedObject):
    """3D model position definition token.

    The 'at' token for 3D models in the format:
    (at (xyz X Y Z))

    Args:
        xyz: 3D coordinates for model position
    """

    __token_name__: ClassVar[str] = "at"

    xyz: Xyz = field(
        default_factory=lambda: Xyz(),
        metadata={"description": "3D coordinates for model position"},
    )


@dataclass
class ModelScale(NamedObject):
    """3D model scale definition token.

    The 'scale' token for 3D models in the format:
    (scale (xyz X Y Z))

    Args:
        xyz: 3D scale factors for model
    """

    __token_name__: ClassVar[str] = "scale"

    xyz: Xyz = field(
        default_factory=lambda: Xyz(x=1.0, y=1.0, z=1.0),
        metadata={"description": "3D scale factors for model"},
    )


@dataclass
class ModelRotate(NamedObject):
    """3D model rotation definition token.

    The 'rotate' token for 3D models in the format:
    (rotate (xyz X Y Z))

    Args:
        xyz: 3D rotation angles for model
    """

    __token_name__: ClassVar[str] = "rotate"

    xyz: Xyz = field(
        default_factory=lambda: Xyz(),
        metadata={"description": "3D rotation angles for model"},
    )


@dataclass
class ModelOffset(NamedObject):
    """3D model offset definition token.

    The 'offset' token for 3D models in the format:
    (offset (xyz X Y Z))

    Args:
        xyz: 3D offset coordinates for model
    """

    __token_name__: ClassVar[str] = "offset"

    xyz: Xyz = field(
        default_factory=lambda: Xyz(),
        metadata={"description": "3D offset coordinates for model"},
    )


@dataclass
class Model(NamedObject):
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
        hide: Whether the 3D model is hidden (optional)
    """

    __token_name__: ClassVar[str] = "model"

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
    hide: TokenFlag = field(
        default_factory=lambda: TokenFlag("hide"),
        metadata={"description": "Whether the 3D model is hidden", "required": False},
    )


@dataclass
class Footprint(NamedObject):
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
        sheetname: Schematic sheet name (optional)
        sheetfile: Schematic sheet file (optional)
        attr: Footprint attributes (optional)
        autoplace_cost90: Vertical cost for automatic placement (optional)
        autoplace_cost180: Horizontal cost for automatic placement (optional)
        solder_mask_margin: Solder mask distance from pads (optional)
        solder_paste_margin: Solder paste distance from pads (optional)
        solder_paste_margin_ratio: Solder paste margin ratio (optional)
        solder_paste_ratio: Percentage of pad size for solder paste (optional)
        clearance: Clearance to board copper objects (optional)
        zone_connect: How pads connect to filled zones (optional)
        thermal_width: Thermal relief spoke width (optional)
        thermal_gap: Distance from pad to zone for thermal relief (optional)
        private_layers: List of private layers (optional)
        net_tie_pad_groups: Net tie pad groups (optional)
        pads: List of pads (optional)
        models: List of 3D models (optional)
        fp_elements: List of footprint graphical elements (optional)
        embedded_fonts: Embedded fonts settings (optional)
        embedded_files: Embedded files container (optional)
    """

    __token_name__: ClassVar[str] = "footprint"
    __legacy_token_names__ = ["module"]

    library_link: Optional[str] = field(
        default=None,
        metadata={"description": "Link to footprint library", "required": False},
    )
    version: NamedInt = field(
        default_factory=lambda: NamedInt("version", 0),
        metadata={"description": "File format version", "required": False},
    )
    generator: NamedString = field(
        default_factory=lambda: NamedString("generator", ""),
        metadata={"description": "Generator application", "required": False},
    )
    generator_version: NamedString = field(
        default_factory=lambda: NamedString("generator_version", ""),
        metadata={"description": "Generator version", "required": False},
    )
    locked: TokenFlag = field(
        default_factory=lambda: TokenFlag("locked"),
        metadata={
            "description": "Whether the footprint cannot be edited",
            "required": False,
        },
    )
    placed: TokenFlag = field(
        default_factory=lambda: TokenFlag("placed"),
        metadata={
            "description": "Whether the footprint has been placed",
            "required": False,
        },
    )
    layer: Layer = field(
        default_factory=lambda: Layer(),
        metadata={"description": "Layer the footprint is placed on"},
    )
    tedit: NamedString = field(
        default_factory=lambda: NamedString("tedit", "0"),
        metadata={"description": "Last edit timestamp", "required": False},
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
    descr: NamedString = field(
        default_factory=lambda: NamedString("descr", ""),
        metadata={"description": "Description of the footprint", "required": False},
    )
    tags: NamedString = field(
        default_factory=lambda: NamedString("tags", ""),
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
    sheetname: NamedString = field(
        default_factory=lambda: NamedString("sheetname", ""),
        metadata={"description": "Schematic sheet name", "required": False},
    )
    sheetfile: NamedString = field(
        default_factory=lambda: NamedString("sheetfile", ""),
        metadata={"description": "Schematic sheet file", "required": False},
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
    solder_paste_margin_ratio: NamedFloat = field(
        default_factory=lambda: NamedFloat("solder_paste_margin_ratio", 0.0),
        metadata={"description": "Solder paste margin ratio", "required": False},
    )
    solder_paste_ratio: Optional[float] = field(
        default=None,
        metadata={
            "description": "Percentage of pad size for solder paste",
            "required": False,
        },
    )
    clearance: NamedFloat = field(
        default_factory=lambda: NamedFloat("clearance", 0.0),
        metadata={
            "description": "Clearance to board copper objects",
            "required": False,
        },
    )
    zone_connect: Optional[int] = field(
        default=None,
        metadata={"description": "How pads connect to filled zones", "required": False},
    )
    thermal_width: NamedFloat = field(
        default_factory=lambda: NamedFloat("thermal_width", 0.0),
        metadata={"description": "Thermal relief spoke width", "required": False},
    )
    thermal_gap: NamedFloat = field(
        default_factory=lambda: NamedFloat("thermal_gap", 0.0),
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
    fp_elements: Optional[
        List[Union[FpArc, FpCircle, FpCurve, FpLine, FpPoly, FpRect, FpText]]
    ] = field(
        default_factory=list,
        metadata={
            "description": "List of footprint graphical elements",
            "required": False,
        },
    )
    embedded_fonts: TokenFlag = field(
        default_factory=lambda: TokenFlag("embedded_fonts"),
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
class Footprints(NamedObject):
    """Footprints container token.

    The 'footprints' token defines a container for multiple footprints in the format::

        (footprints
            (footprint ...)
            ...
        )

    Args:
        footprints: List of footprints
    """

    __token_name__: ClassVar[str] = "footprints"

    footprints: List[Footprint] = field(
        default_factory=list, metadata={"description": "List of footprints"}
    )
