"""Base types for KiCad S-expressions - fundamental elements with no cross-dependencies."""

from dataclasses import dataclass, field
from typing import Any, ClassVar, List, Optional

from .base_element import NamedFloat, NamedObject, NamedString, TokenFlag, UnquotedToken
from .enums import PadShape, StrokeType
from .sexpr_parser import SExpr


@dataclass
class Anchor(NamedObject):
    """Anchor pad shape definition for custom pads.

    The 'anchor' token defines the anchor pad shape of a custom pad in the format::

        (anchor PAD_SHAPE)

    Args:
        pad_shape: Anchor pad shape (rect or circle)
    """

    __token_name__: ClassVar[str] = "anchor"

    pad_shape: PadShape = field(
        default=PadShape.RECT,
        metadata={"description": "Anchor pad shape (rect or circle)"},
    )


@dataclass
class Xy(NamedObject):
    """2D coordinate definition token.

    The 'xy' token defines a 2D coordinate point in the format:
    (xy X Y)

    Args:
        x: Horizontal coordinate
        y: Vertical coordinate
    """

    __token_name__: ClassVar[str] = "xy"

    x: float = field(default=0.0, metadata={"description": "Horizontal coordinate"})
    y: float = field(default=0.0, metadata={"description": "Vertical coordinate"})


@dataclass
class Xyz(NamedObject):
    """3D coordinate definition token.

    The 'xyz' token defines 3D coordinates in the format:
    (xyz X Y Z)

    Args:
        x: X coordinate
        y: Y coordinate
        z: Z coordinate
    """

    __token_name__: ClassVar[str] = "xyz"

    x: float = field(default=0.0, metadata={"description": "X coordinate"})
    y: float = field(default=0.0, metadata={"description": "Y coordinate"})
    z: float = field(default=0.0, metadata={"description": "Z coordinate"})


@dataclass
class Pts(NamedObject):
    """Coordinate point list definition token.

    The 'pts' token defines a list of coordinate points in the format:
    (pts
        (xy X Y)
        ...
        (xy X Y)
    )

    Where each xy token defines a single X and Y coordinate pair.
    The number of points is determined by the object type.

    Args:
        points: List of 2D coordinate points
    """

    __token_name__: ClassVar[str] = "pts"

    points: List[Xy] = field(
        default_factory=list, metadata={"description": "List of 2D coordinate points"}
    )

    def xy(self, x: float, y: float) -> "Pts":
        """Add a coordinate point to the list.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Pts: Self (for method chaining)
        """
        self.points.append(Xy(x=x, y=y))
        return self


@dataclass
class AtXY(NamedObject):
    """Position identifier token for elements that only use X and Y coordinates.

    The 'at' token defines positional coordinates in the format:
        (at X Y)

    Used for elements like junctions that don't have rotation.

    Args:
        x: Horizontal position of the object
        y: Vertical position of the object
    """

    __token_name__: ClassVar[str] = "at"

    x: float = field(
        default=0.0,
        metadata={"description": "Horizontal position of the object"},
    )
    y: float = field(
        default=0.0, metadata={"description": "Vertical position of the object"}
    )

    def xy(self, x: float, y: float) -> "AtXY":
        """Set X and Y coordinates.

        Args:
            x: Horizontal position
            y: Vertical position

        Returns:
            AtXY: Self (for method chaining)
        """
        self.x = x
        self.y = y
        return self


@dataclass
class At(NamedObject):
    """Position identifier token that defines positional coordinates and rotation of an object.

    The 'at' token defines the positional coordinates in the format:
        (at X Y [ANGLE])

    Note:
        Symbol text ANGLEs are stored in tenth's of a degree. All other ANGLEs are stored in degrees.
        For 3D model positioning, use ModelAt class which supports (at (xyz X Y Z)) format.

    Args:
        x: Horizontal position of the object
        y: Vertical position of the object
        angle: Rotational angle of the object
    """

    __token_name__: ClassVar[str] = "at"

    x: float = field(
        default=0.0,
        metadata={"description": "Horizontal position of the object"},
    )
    y: float = field(
        default=0.0, metadata={"description": "Vertical position of the object"}
    )
    angle: Optional[float] = field(
        default=0.0,
        metadata={"description": "Rotational angle of the object"},
    )


@dataclass
class Center(NamedObject):
    """Center point definition token.

    The 'center' token defines a center point in the format::

        (center X Y)

    Args:
        x: Horizontal position of the center point
        y: Vertical position of the center point
    """

    __token_name__: ClassVar[str] = "center"

    x: float = field(
        default=0.0, metadata={"description": "Horizontal position of the center point"}
    )
    y: float = field(
        default=0.0, metadata={"description": "Vertical position of the center point"}
    )


@dataclass
class Color(NamedObject):
    """Color definition token.

    The 'color' token defines color values in the format::

        (color R G B A)

    Args:
        r: Red color component (0-255)
        g: Green color component (0-255)
        b: Blue color component (0-255)
        a: Alpha component (0-255)
    """

    __token_name__: ClassVar[str] = "color"

    r: int = field(default=0, metadata={"description": "Red color component (0-255)"})
    g: int = field(default=0, metadata={"description": "Green color component (0-255)"})
    b: int = field(default=0, metadata={"description": "Blue color component (0-255)"})
    a: int = field(default=0, metadata={"description": "Alpha component (0-255)"})


@dataclass
class End(NamedObject):
    """End point definition token.

    The 'end' token defines an end point in the format::

        (end X Y)

    Args:
        x: Horizontal position of the end point
        y: Vertical position of the end point
        corner: Corner reference (optional)
    """

    __token_name__: ClassVar[str] = "end"

    x: float = field(
        default=0.0, metadata={"description": "Horizontal position of the end point"}
    )
    y: float = field(
        default=0.0, metadata={"description": "Vertical position of the end point"}
    )
    corner: Optional[str] = field(
        default=None, metadata={"description": "Corner reference", "required": False}
    )


@dataclass
class Mid(NamedObject):
    """Mid point definition token.

    The 'mid' token defines a mid point in the format::

        (mid X Y)

    Args:
        x: Horizontal position of the mid point
        y: Vertical position of the mid point
    """

    __token_name__: ClassVar[str] = "mid"

    x: float = field(
        default=0.0, metadata={"description": "Horizontal position of the mid point"}
    )
    y: float = field(
        default=0.0, metadata={"description": "Vertical position of the mid point"}
    )


@dataclass
class Type(NamedObject):
    """Type definition token.

    The 'type' token defines a type value in the format:
    (type VALUE)

    Args:
        value: Type value
    """

    __token_name__: ClassVar[str] = "type"

    value: str = field(default="", metadata={"description": "Type value"})

    def to_sexpr(self) -> SExpr:
        """Serialize with unquoted value."""
        return [self.__token_name__, UnquotedToken(self.value)]


@dataclass
class Fill(NamedObject):
    """Fill definition token.

    The 'fill' token defines how schematic and symbol library graphical items are filled in the format:
    (fill
        (type none | outline | background)
        (color R G B A)
    )

    This represents the nested structure exactly as it appears in the S-expression files.

    Args:
        type: Fill type specification (optional)
        color: Fill color specification (optional)
    """

    __token_name__: ClassVar[str] = "fill"

    type: Optional[Type] = field(
        default=None,
        metadata={"description": "Fill type specification", "required": False},
    )
    color: Optional[Color] = field(
        default=None,
        metadata={"description": "Fill color specification", "required": False},
    )


@dataclass
class Layer(NamedObject):
    """Layer definition token.

    The 'layer' token defines layer information in the format::

        (layer "NAME" | dielectric NUMBER (type "DESCRIPTION")
               [(color "COLOR")] [(thickness THICKNESS)]
               [(material "MATERIAL")] [(epsilon_r VALUE)]
               [(loss_tangent VALUE)])

    For simple layer references:
        (layer "LAYER_NAME")

    Args:
        name: Layer name or 'dielectric'
        number: Layer stack number (optional)
        type: Layer type description (optional)
        color: Layer color as string (optional)
        thickness: Layer thickness value (optional)
        material: Material name (optional)
        epsilon_r: Dielectric constant value (optional)
        loss_tangent: Loss tangent value (optional)
    """

    __token_name__: ClassVar[str] = "layer"

    name: str = field(
        default="", metadata={"description": "Layer name or 'dielectric'"}
    )
    number: Optional[int] = field(
        default=None, metadata={"description": "Layer stack number", "required": False}
    )
    type: Optional[str] = field(
        default=None,
        metadata={"description": "Layer type description", "required": False},
    )
    color: Optional[str] = field(
        default=None,
        metadata={"description": "Layer color as string", "required": False},
    )
    thickness: Optional[float] = field(
        default=None,
        metadata={"description": "Layer thickness value", "required": False},
    )
    material: Optional[str] = field(
        default=None, metadata={"description": "Material name", "required": False}
    )
    epsilon_r: Optional[float] = field(
        default=None,  # 4,5 nomally
        metadata={"description": "Dielectric constant value", "required": False},
    )
    loss_tangent: Optional[float] = field(
        default=None, metadata={"description": "Loss tangent value", "required": False}
    )


@dataclass
class Offset(NamedObject):
    """Offset definition token.

    The 'offset' token defines an offset position in the format:
    (offset X Y)

    Args:
        x: Horizontal offset coordinate
        y: Vertical offset coordinate
    """

    __token_name__: ClassVar[str] = "offset"

    x: float = field(
        default=0.0, metadata={"description": "Horizontal offset coordinate"}
    )
    y: float = field(
        default=0.0, metadata={"description": "Vertical offset coordinate"}
    )


@dataclass
class Pos(NamedObject):
    """Position definition token.

    The 'pos' token defines a position in the format:
    (pos X Y)

    Args:
        x: Horizontal position coordinate
        y: Vertical position coordinate
        corner: Corner reference (optional)
    """

    __token_name__: ClassVar[str] = "pos"

    x: float = field(
        default=0.0, metadata={"description": "Horizontal position coordinate"}
    )
    y: float = field(
        default=0.0, metadata={"description": "Vertical position coordinate"}
    )
    corner: Optional[str] = field(
        default=None, metadata={"description": "Corner reference", "required": False}
    )


@dataclass
class Size(NamedObject):
    """Size definition token.

    The 'size' token defines width and height dimensions in the format:
    (size WIDTH HEIGHT)

    Args:
        width: Width dimension
        height: Height dimension
    """

    __token_name__: ClassVar[str] = "size"

    width: float = field(default=0.0, metadata={"description": "Width dimension"})
    height: float = field(default=0.0, metadata={"description": "Height dimension"})


@dataclass
class Start(NamedObject):
    """Start point definition token.

    The 'start' token defines a start point in the format:
    (start X Y)

    Args:
        x: Horizontal position of the start point
        y: Vertical position of the start point
        corner: Corner reference (optional)
    """

    __token_name__: ClassVar[str] = "start"

    x: float = field(
        default=0.0, metadata={"description": "Horizontal position of the start point"}
    )
    y: float = field(
        default=0.0, metadata={"description": "Vertical position of the start point"}
    )
    corner: Optional[str] = field(
        default=None, metadata={"description": "Corner reference", "required": False}
    )


@dataclass
class Stroke(NamedObject):
    """Stroke definition token.

    The 'stroke' token defines how the outlines of graphical objects are drawn in the format:
    (stroke
        (width WIDTH)
        (type TYPE)
        (color R G B A)
    )

    This represents the nested structure exactly as it appears in the S-expression files.

    Args:
        width: Line width specification
        type: Stroke line style specification
        color: Line color specification (optional)
    """

    __token_name__: ClassVar[str] = "stroke"

    width: NamedFloat = field(
        default_factory=lambda: NamedFloat("width", 0.0),
        metadata={"description": "Line width specification"},
    )
    type: Type = field(
        default_factory=lambda: Type(value=StrokeType.SOLID.value),
        metadata={"description": "Stroke line style specification"},
    )
    color: Optional[Color] = field(
        default=None,
        metadata={"description": "Line color specification", "required": False},
    )


@dataclass
class Uuid(NamedObject):
    """UUID identifier token.

    The 'uuid' token defines a universally unique identifier in the format:
    (uuid UUID_VALUE)

    Args:
        value: UUID value
    """

    __token_name__: ClassVar[str] = "uuid"

    value: str = field(default="", metadata={"description": "UUID value"})

    def new_id(self) -> "Uuid":
        """Generate a new UUID identifier and update this instance.

        Returns:
            Uuid: Self (for method chaining)
        """
        import uuid

        self.value = str(uuid.uuid4())
        return self

    @classmethod
    def create(cls) -> "Uuid":
        """Create a new UUID identifier (factory method).

        Returns:
            Uuid: New Uuid object with a generated UUID value
        """
        import uuid

        return cls(value=str(uuid.uuid4()))


@dataclass
class Font(NamedObject):
    """Font definition token.

    The 'font' token defines font properties in the format:
    (font [face "FONT_NAME"] [size WIDTH HEIGHT] [thickness THICKNESS] [bold] [italic])

    Args:
        face: Font face specification (optional)
        size: Font size (optional)
        thickness: Font thickness (optional)
        bold: Bold flag (optional)
        italic: Italic flag (optional)
        color: Font color (optional)
    """

    __token_name__: ClassVar[str] = "font"

    face: NamedString = field(
        default_factory=lambda: NamedString("face", ""),
        metadata={"description": "Font face specification", "required": False},
    )
    size: Optional[Size] = field(
        default_factory=lambda: Size(1.27, 1.27),
        metadata={"description": "Font size", "required": False},
    )
    thickness: NamedFloat = field(
        default_factory=lambda: NamedFloat("thickness", 0.0),
        metadata={"description": "Font thickness", "required": False},
    )
    bold: TokenFlag = field(
        default_factory=lambda: TokenFlag("bold"),
        metadata={"description": "Bold flag", "required": False},
    )
    italic: TokenFlag = field(
        default_factory=lambda: TokenFlag("italic"),
        metadata={"description": "Italic flag", "required": False},
    )
    color: Optional[Color] = field(
        default=None,
        metadata={"description": "Font color", "required": False},
    )


@dataclass
class Justify(NamedObject):
    """Text justification definition token.

    The 'justify' token defines text alignment and mirroring in the format::

        (justify [left | right | center] [top | bottom | center] [mirror])

    Args:
        left: Left horizontal justification flag (optional)
        right: Right horizontal justification flag (optional)
        top: Top vertical justification flag (optional)
        bottom: Bottom vertical justification flag (optional)
        center: Center justification flag (horizontal or vertical) (optional)
        mirror: Mirror text flag (optional)
    """

    __token_name__: ClassVar[str] = "justify"

    # Horizontal justification flags
    left: TokenFlag = field(
        default_factory=lambda: TokenFlag("left"),
        metadata={
            "description": "Left horizontal justification flag",
            "required": False,
        },
    )
    right: TokenFlag = field(
        default_factory=lambda: TokenFlag("right"),
        metadata={
            "description": "Right horizontal justification flag",
            "required": False,
        },
    )

    # Vertical justification flags
    top: TokenFlag = field(
        default_factory=lambda: TokenFlag("top"),
        metadata={"description": "Top vertical justification flag", "required": False},
    )
    bottom: TokenFlag = field(
        default_factory=lambda: TokenFlag("bottom"),
        metadata={
            "description": "Bottom vertical justification flag",
            "required": False,
        },
    )

    # Center can be horizontal or vertical - ambiguous in S-expression
    center: TokenFlag = field(
        default_factory=lambda: TokenFlag("center"),
        metadata={
            "description": "Center justification flag (horizontal or vertical)",
            "required": False,
        },
    )

    # Mirror flag
    mirror: TokenFlag = field(
        default_factory=lambda: TokenFlag("mirror"),
        metadata={"description": "Mirror text flag", "required": False},
    )


@dataclass
class Effects(NamedObject):
    """Text effects definition token.

    The 'effects' token defines text formatting effects in the format::

        (effects
            (font [size SIZE] [thickness THICKNESS] [bold] [italic])
            [(justify JUSTIFY)]
            [hide]
        )

    Args:
        font: Font definition (optional)
        justify: Text justification (optional)
        hide: Whether text is hidden (optional)
        href: Hyperlink reference (optional)
    """

    __token_name__: ClassVar[str] = "effects"

    font: Optional[Font] = field(
        default=None, metadata={"description": "Font definition", "required": False}
    )
    justify: Optional[Justify] = field(
        default=None,
        metadata={"description": "Text justification", "required": False},
    )
    hide: TokenFlag = field(
        default_factory=lambda: TokenFlag("hide"),
        metadata={"description": "Whether text is hidden", "required": False},
    )
    href: NamedString = field(
        default_factory=lambda: NamedString("href", ""),
        metadata={"description": "Hyperlink reference", "required": False},
    )


@dataclass
class Text(NamedObject):
    """Text content definition token.

    The 'text' token defines text content in the format:
    (text "TEXT_CONTENT"
        (at X Y [ANGLE])
        (effects EFFECTS)
    )

    Args:
        content: Text content
        at: Position and rotation (optional)
        effects: Text effects (optional)
        exclude_from_sim: Whether to exclude from simulation (optional)
        uuid: Unique identifier (optional)
    """

    __token_name__: ClassVar[str] = "text"

    content: str = field(default="", metadata={"description": "Text content"})
    at: Optional[At] = field(
        default=None,
        metadata={"description": "Position and rotation", "required": False},
    )
    effects: Optional[Effects] = field(
        default=None, metadata={"description": "Text effects", "required": False}
    )
    exclude_from_sim: TokenFlag = field(
        default_factory=lambda: TokenFlag("exclude_from_sim"),
        metadata={
            "description": "Whether to exclude from simulation",
            "required": False,
        },
    )
    uuid: Optional[Uuid] = field(
        default=None,
        metadata={"description": "Unique identifier", "required": False},
    )


@dataclass
class Property(NamedObject):
    """Property definition token.

    The 'property' token defines properties in two formats:

    General properties::
        (property "KEY" "VALUE")

    Symbol properties::
        (property
            "KEY"
            "VALUE"
            (id N)
            POSITION_IDENTIFIER
            TEXT_EFFECTS
        )

    Args:
        key: Property key name (must be unique)
        value: Property value
        id: Property ID (optional)
        at: Position and rotation (optional)
        effects: Text effects (optional)
        unlocked: Whether property is unlocked (optional)
        layer: Layer assignment (optional)
        uuid: Unique identifier (optional)
        hide: Hide property flag (optional)
    """

    __token_name__: ClassVar[str] = "property"

    key: str = field(
        default="", metadata={"description": "Property key name (must be unique)"}
    )
    value: str = field(default="", metadata={"description": "Property value"})
    id: NamedString = field(
        default_factory=lambda: NamedString("id", ""),
        metadata={"description": "Property ID", "required": False},
    )
    at: Optional[At] = field(
        default=None,
        metadata={"description": "Position and rotation", "required": False},
    )
    effects: Optional[Effects] = field(
        default=None, metadata={"description": "Text effects", "required": False}
    )
    unlocked: TokenFlag = field(
        default_factory=lambda: TokenFlag("unlocked"),
        metadata={"description": "Whether property is unlocked", "required": False},
    )
    layer: Optional[Layer] = field(
        default=None, metadata={"description": "Layer assignment", "required": False}
    )
    uuid: Optional[Uuid] = field(
        default=None, metadata={"description": "Unique identifier", "required": False}
    )
    hide: TokenFlag = field(
        default_factory=lambda: TokenFlag("hide"),
        metadata={"description": "Hide property flag", "required": False},
    )


@dataclass
class LayerDefinition:
    """Board layer definition entry (no token name).

    Individual layer definition within a 'layers' token in PCB files::

        (0 "F.Cu" signal)
        (9 "F.Adhes" user "F.Adhesive")
        (31 "F.CrtYd" user "F.Courtyard")

    Stores the raw list internally and provides properties for access.

    Args:
        data: Raw layer data as list [ordinal, name, type, user_name?]
    """

    data: List[Any] = field(default_factory=list)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize from list or individual parameters."""
        if len(args) == 1 and isinstance(args[0], list):
            self.data = args[0]
        elif args:
            self.data = list(args)
        else:
            self.data = []

    @property
    def ordinal(self) -> int:
        """Layer ordinal number."""
        return int(self.data[0]) if len(self.data) > 0 else 0

    @property
    def canonical_name(self) -> str:
        """Canonical layer name."""
        return self.data[1] if len(self.data) > 1 else ""

    @property
    def layer_type(self) -> str:
        """Layer type (signal, user, power, mixed, jumper)."""
        return self.data[2] if len(self.data) > 2 else "signal"

    @property
    def user_name(self) -> Optional[str]:
        """User-defined layer name (optional)."""
        return self.data[3] if len(self.data) > 3 else None


@dataclass
class BoardLayers(NamedObject):
    """Board layer definitions for kicad_pcb files.

    Stores layer definitions as raw lists::

        (layers (0 "F.Cu" signal) (2 "B.Cu" signal) ...)

    Use get_layer(index) to parse a specific layer as LayerDefinition if needed.
    """

    __token_name__: ClassVar[str] = "layers"
    layer_defs: List[LayerDefinition] = field(default_factory=list)

    @classmethod
    def _parse_recursive(cls, cursor: Any) -> "BoardLayers":
        """Parse and store layer definitions as LayerDefinition objects."""
        layer_defs = [
            LayerDefinition([str(v) for v in item])
            for item in cursor.sexpr[1:]
            if isinstance(item, list)
        ]
        for i in range(1, len(cursor.sexpr)):
            cursor.parser.mark_used(i)
        return cls(layer_defs=layer_defs)

    def to_sexpr(self) -> SExpr:
        """Convert to S-expression format."""
        return [self.__token_name__] + [ld.data for ld in self.layer_defs]


@dataclass
class Layers(NamedObject):
    """Layer list definition token.

    The 'layers' token defines a list of layer names in the format::

        (layers "F.Cu" "F.Paste" "F.Mask")
        (layers "*.Cu" "*.Mask" "F.SilkS")

    Used for pad layers, via layers, and other layer specifications.

    Attributes:
        layers (List[str]): List of layer names

    Args:
        layers: List of layer names
    """

    __token_name__: ClassVar[str] = "layers"

    layers: List[str] = field(
        default_factory=list, metadata={"description": "List of layer names"}
    )
