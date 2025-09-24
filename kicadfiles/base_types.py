"""Base types for KiCad S-expressions - fundamental elements with no cross-dependencies."""

from dataclasses import dataclass, field
from typing import List, Optional

from .base_element import KiCadObject, OptionalFlag
from .enums import FillType, PadShape, StrokeType


@dataclass
class Anchor(KiCadObject):
    """Anchor pad shape definition for custom pads.

    The 'anchor' token defines the anchor pad shape of a custom pad in the format::

        (anchor PAD_SHAPE)

    Args:
        pad_shape: Anchor pad shape (rect or circle)
    """

    __token_name__ = "anchor"

    pad_shape: PadShape = field(
        default=PadShape.RECT,
        metadata={"description": "Anchor pad shape (rect or circle)"},
    )


@dataclass
class Angle(KiCadObject):
    """Angle definition token.

    The 'angle' token defines a rotational angle in the format::

        (angle VALUE)

    Args:
        value: Angle value in degrees
    """

    __token_name__ = "angle"

    value: float = field(
        default=0.0, metadata={"description": "Angle value in degrees"}
    )


@dataclass
class Xy(KiCadObject):
    """2D coordinate definition token.

    The 'xy' token defines a 2D coordinate point in the format:
    (xy X Y)

    Args:
        x: Horizontal coordinate
        y: Vertical coordinate
    """

    __token_name__ = "xy"

    x: float = field(default=0.0, metadata={"description": "Horizontal coordinate"})
    y: float = field(default=0.0, metadata={"description": "Vertical coordinate"})


@dataclass
class Xyz(KiCadObject):
    """3D coordinate definition token.

    The 'xyz' token defines 3D coordinates in the format:
    (xyz X Y Z)

    Args:
        x: X coordinate
        y: Y coordinate
        z: Z coordinate
    """

    __token_name__ = "xyz"

    x: float = field(default=0.0, metadata={"description": "X coordinate"})
    y: float = field(default=0.0, metadata={"description": "Y coordinate"})
    z: float = field(default=0.0, metadata={"description": "Z coordinate"})


@dataclass
class Pts(KiCadObject):
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

    __token_name__ = "pts"

    points: List[Xy] = field(
        default_factory=list, metadata={"description": "List of 2D coordinate points"}
    )


@dataclass
class At(KiCadObject):
    """Position identifier token that defines positional coordinates and rotation of an object.

    The 'at' token defines the positional coordinates in alternative formats:

    For 2D elements::
        (at X Y [ANGLE])

    Alternative for 3D models::
        (at (xyz X Y Z))

    Note:
        Symbol text ANGLEs are stored in tenth's of a degree. All other ANGLEs are stored in degrees.

    Args:
        x: Horizontal position of the object (optional)
        y: Vertical position of the object (optional)
        angle: Optional rotational angle of the object (optional)
        xyz: 3D position coordinates (optional)
    """

    __token_name__ = "at"

    x: Optional[float] = field(
        default=None,
        metadata={
            "description": "Horizontal position of the object",
            "required": False,
        },
    )
    y: Optional[float] = field(
        default=None,
        metadata={"description": "Vertical position of the object", "required": False},
    )
    angle: Optional[float] = field(
        default=None,
        metadata={
            "description": "Optional rotational angle of the object",
            "required": False,
        },
    )
    xyz: Optional[Xyz] = field(
        default=None,
        metadata={"description": "3D position coordinates", "required": False},
    )


@dataclass
class Center(KiCadObject):
    """Center point definition token.

    The 'center' token defines a center point in the format::

        (center X Y)

    Args:
        x: Horizontal position of the center point
        y: Vertical position of the center point
    """

    __token_name__ = "center"

    x: float = field(
        default=0.0, metadata={"description": "Horizontal position of the center point"}
    )
    y: float = field(
        default=0.0, metadata={"description": "Vertical position of the center point"}
    )


@dataclass
class Clearance(KiCadObject):
    """Clearance definition token.

    The 'clearance' token defines a clearance value in the format::

        (clearance VALUE)

    Args:
        value: Clearance value
    """

    __token_name__ = "clearance"

    value: float = field(default=0.0, metadata={"description": "Clearance value"})


@dataclass
class Color(KiCadObject):
    """Color definition token.

    The 'color' token defines color values in the format::

        (color R G B A)

    Args:
        r: Red color component (0-255)
        g: Green color component (0-255)
        b: Blue color component (0-255)
        a: Alpha transparency component (0-255)
    """

    __token_name__ = "color"

    r: int = field(default=0, metadata={"description": "Red color component (0-255)"})
    g: int = field(default=0, metadata={"description": "Green color component (0-255)"})
    b: int = field(default=0, metadata={"description": "Blue color component (0-255)"})
    a: int = field(
        default=255, metadata={"description": "Alpha transparency component (0-255)"}
    )


@dataclass
class Diameter(KiCadObject):
    """Diameter definition token.

    The 'diameter' token defines a diameter value in the format::

        (diameter VALUE)

    Args:
        value: Diameter value
    """

    __token_name__ = "diameter"

    value: float = field(default=0.0, metadata={"description": "Diameter value"})


@dataclass
class End(KiCadObject):
    """End point definition token.

    The 'end' token defines an end point in the format::

        (end X Y)

    Args:
        x: Horizontal position of the end point
        y: Vertical position of the end point
        corner: Corner reference (optional)
    """

    __token_name__ = "end"

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
class Type(KiCadObject):
    """Type definition token.

    The 'type' token defines a type value in the format:
    (type VALUE)

    Args:
        value: Type value
    """

    __token_name__ = "type"

    value: str = field(default="", metadata={"description": "Type value"})


@dataclass
class Fill(KiCadObject):
    """Fill definition token.

    The 'fill' token defines how schematic and symbol library graphical items are filled in the format:
    (fill
        (type none | outline | background)
    )

    This represents the nested structure exactly as it appears in the S-expression files.

    Args:
        type: Fill type specification
    """

    __token_name__ = "fill"

    type: Type = field(
        default_factory=lambda: Type(value=FillType.NONE.value),
        metadata={"description": "Fill type specification"},
    )


@dataclass
class Height(KiCadObject):
    """Height definition token.

    The 'height' token defines a height value in the format:
    (height VALUE)

    Args:
        value: Height value
    """

    __token_name__ = "height"

    value: float = field(default=0.0, metadata={"description": "Height value"})


@dataclass
class Id(KiCadObject):
    """Identifier definition token.

    The 'id' token defines an identifier in the format::

        (id VALUE)

    Args:
        value: Identifier value
    """

    __token_name__ = "id"

    value: str = field(default="", metadata={"description": "Identifier value"})


@dataclass
class Layer(KiCadObject):
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

    __token_name__ = "layer"

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
        default=None,
        metadata={"description": "Dielectric constant value", "required": False},
    )
    loss_tangent: Optional[float] = field(
        default=None, metadata={"description": "Loss tangent value", "required": False}
    )


@dataclass
class Linewidth(KiCadObject):
    """Line width definition token.

    The 'linewidth' token defines a line width value in the format::

        (linewidth VALUE)

    Args:
        value: Line width value
    """

    __token_name__ = "linewidth"

    value: float = field(default=0.0, metadata={"description": "Line width value"})


@dataclass
class Name(KiCadObject):
    """Name definition token.

    The 'name' token defines a name in the format::

        (name "NAME_VALUE")

    Args:
        value: Name value
    """

    __token_name__ = "name"

    value: str = field(default="", metadata={"description": "Name value"})


@dataclass
class Offset(KiCadObject):
    """Offset definition token.

    The 'offset' token defines an offset position in the format:
    (offset X Y)

    Args:
        x: Horizontal offset coordinate
        y: Vertical offset coordinate
    """

    __token_name__ = "offset"

    x: float = field(
        default=0.0, metadata={"description": "Horizontal offset coordinate"}
    )
    y: float = field(
        default=0.0, metadata={"description": "Vertical offset coordinate"}
    )


@dataclass
class Pos(KiCadObject):
    """Position definition token.

    The 'pos' token defines a position in the format:
    (pos X Y)

    Args:
        x: Horizontal position coordinate
        y: Vertical position coordinate
        corner: Corner reference (optional)
    """

    __token_name__ = "pos"

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
class Radius(KiCadObject):
    """Radius definition token.

    The 'radius' token defines a radius value in the format:
    (radius VALUE)

    Args:
        value: Radius value
    """

    __token_name__ = "radius"

    value: float = field(default=0.0, metadata={"description": "Radius value"})


@dataclass
class Rotate(KiCadObject):
    """Rotation definition token for various elements.

    The 'rotate' token defines rotation in alternative formats:

    For polygons and 2D elements::
        (rotate ANGLE)

    Alternative for 3D models::
        (rotate (xyz X Y Z))

    Args:
        angle: Rotation angle in degrees (optional)
        xyz: 3D rotation angles (optional)
    """

    __token_name__ = "rotate"

    angle: Optional[float] = field(
        default=None,
        metadata={"description": "Rotation angle in degrees", "required": False},
    )
    xyz: Optional[Xyz] = field(
        default=None, metadata={"description": "3D rotation angles", "required": False}
    )


@dataclass
class Size(KiCadObject):
    """Size definition token.

    The 'size' token defines width and height dimensions in the format:
    (size WIDTH HEIGHT)

    Args:
        width: Width dimension
        height: Height dimension
    """

    __token_name__ = "size"

    width: float = field(default=0.0, metadata={"description": "Width dimension"})
    height: float = field(default=0.0, metadata={"description": "Height dimension"})


@dataclass
class Start(KiCadObject):
    """Start point definition token.

    The 'start' token defines a start point in the format:
    (start X Y)

    Args:
        x: Horizontal position of the start point
        y: Vertical position of the start point
        corner: Corner reference (optional)
    """

    __token_name__ = "start"

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
class Width(KiCadObject):
    """Width definition token.

    The 'width' token defines a width value in the format:
    (width VALUE)

    Args:
        value: Width value
    """

    __token_name__ = "width"

    value: float = field(default=0.0, metadata={"description": "Width value"})


@dataclass
class Stroke(KiCadObject):
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

    __token_name__ = "stroke"

    width: Width = field(
        default_factory=lambda: Width(),
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
class Style(KiCadObject):
    """Style definition token.

    The 'style' token defines a style value in the format:
    (style VALUE)

    Args:
        value: Style value
    """

    __token_name__ = "style"

    value: str = field(default="", metadata={"description": "Style value"})


@dataclass
class Text(KiCadObject):
    """Text content definition token.

    The 'text' token defines text content in the format:
    (text "TEXT_CONTENT")

    Args:
        content: Text content
    """

    __token_name__ = "text"

    content: str = field(default="", metadata={"description": "Text content"})


@dataclass
class Thickness(KiCadObject):
    """Thickness definition token.

    The 'thickness' token defines a thickness value in the format:
    (thickness VALUE)

    Args:
        value: Thickness value
    """

    __token_name__ = "thickness"

    value: float = field(default=0.0, metadata={"description": "Thickness value"})


@dataclass
class Title(KiCadObject):
    """Title definition token.

    The 'title' token defines a title in the format:
    (title "TITLE_VALUE")

    Args:
        value: Title value
    """

    __token_name__ = "title"

    value: str = field(default="", metadata={"description": "Title value"})


@dataclass
class Tstamp(KiCadObject):
    """Timestamp identifier token.

    The 'tstamp' token defines a timestamp identifier in the format:
    (tstamp UUID)

    Args:
        value: Timestamp UUID
    """

    __token_name__ = "tstamp"

    value: str = field(default="", metadata={"description": "Timestamp UUID"})


@dataclass
class Units(KiCadObject):
    """Units definition token.

    The 'units' token defines measurement units in the format:
    (units VALUE)

    Args:
        value: Units value (mm | inches)
    """

    __token_name__ = "units"

    value: str = field(
        default="mm", metadata={"description": "Units value (mm | inches)"}
    )


@dataclass
class Uuid(KiCadObject):
    """UUID identifier token.

    The 'uuid' token defines a universally unique identifier in the format:
    (uuid UUID_VALUE)

    Args:
        value: UUID value
    """

    __token_name__ = "uuid"

    value: str = field(default="", metadata={"description": "UUID value"})


@dataclass
class Font(KiCadObject):
    """Font definition token.

    The 'font' token defines font properties in the format:
    (font [size WIDTH HEIGHT] [thickness THICKNESS] [bold] [italic])

    Args:
        size: Font size (optional)
        thickness: Font thickness (optional)
        bold: Bold flag (optional)
        italic: Italic flag (optional)
    """

    __token_name__ = "font"

    size: Optional[Size] = field(
        default=None, metadata={"description": "Font size", "required": False}
    )
    thickness: Optional[Thickness] = field(
        default=None, metadata={"description": "Font thickness", "required": False}
    )
    bold: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("bold"),
        metadata={"description": "Bold flag", "required": False},
    )
    italic: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("italic"),
        metadata={"description": "Italic flag", "required": False},
    )


@dataclass
class Justify(KiCadObject):
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

    __token_name__ = "justify"

    # Horizontal justification flags
    left: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("left"),
        metadata={
            "description": "Left horizontal justification flag",
            "required": False,
        },
    )
    right: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("right"),
        metadata={
            "description": "Right horizontal justification flag",
            "required": False,
        },
    )

    # Vertical justification flags
    top: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("top"),
        metadata={"description": "Top vertical justification flag", "required": False},
    )
    bottom: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("bottom"),
        metadata={
            "description": "Bottom vertical justification flag",
            "required": False,
        },
    )

    # Center can be horizontal or vertical - ambiguous in S-expression
    center: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("center"),
        metadata={
            "description": "Center justification flag (horizontal or vertical)",
            "required": False,
        },
    )

    # Mirror flag
    mirror: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("mirror"),
        metadata={"description": "Mirror text flag", "required": False},
    )


@dataclass
class Effects(KiCadObject):
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
    """

    __token_name__ = "effects"

    font: Optional[Font] = field(
        default=None, metadata={"description": "Font definition", "required": False}
    )
    justify: Optional[Justify] = field(
        default=None,
        metadata={"description": "Text justification", "required": False},
    )
    hide: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("hide"),
        metadata={"description": "Whether text is hidden", "required": False},
    )


@dataclass
class Property(KiCadObject):
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

    __token_name__ = "property"

    key: str = field(
        default="", metadata={"description": "Property key name (must be unique)"}
    )
    value: str = field(default="", metadata={"description": "Property value"})
    id: Optional[Id] = field(
        default=None, metadata={"description": "Property ID", "required": False}
    )
    at: Optional[At] = field(
        default=None,
        metadata={"description": "Position and rotation", "required": False},
    )
    effects: Optional[Effects] = field(
        default=None, metadata={"description": "Text effects", "required": False}
    )
    unlocked: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("unlocked"),
        metadata={"description": "Whether property is unlocked", "required": False},
    )
    layer: Optional[Layer] = field(
        default=None, metadata={"description": "Layer assignment", "required": False}
    )
    uuid: Optional[Uuid] = field(
        default=None, metadata={"description": "Unique identifier", "required": False}
    )
    hide: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("hide"),
        metadata={"description": "Hide property flag", "required": False},
    )


@dataclass
class Layers(KiCadObject):
    """Layer list definition token.

    The 'layers' token defines a list of layer names in the format::

        (layers "F.Cu" "F.Paste" "F.Mask")
        (layers "*.Cu" "*.Mask" "F.SilkS")

    Used for pad layers, via layers, and other layer specifications.

    TODO: Implement proper list parsing for direct parameters format.
    Currently using individual fields as workaround.

    Args:
        layer1: First layer name (optional)
        layer2: Second layer name (optional)
        layer3: Third layer name (optional)
        layer4: Fourth layer name (optional)
        layer5: Fifth layer name (optional)
    """

    __token_name__ = "layers"

    # TODO: Replace with proper list parsing - temporary workaround with individual fields
    layer1: Optional[str] = field(
        default=None, metadata={"description": "First layer name", "required": False}
    )
    layer2: Optional[str] = field(
        default=None, metadata={"description": "Second layer name", "required": False}
    )
    layer3: Optional[str] = field(
        default=None, metadata={"description": "Third layer name", "required": False}
    )
    layer4: Optional[str] = field(
        default=None, metadata={"description": "Fourth layer name", "required": False}
    )
    layer5: Optional[str] = field(
        default=None, metadata={"description": "Fifth layer name", "required": False}
    )

    @property
    def layers(self) -> List[str]:
        """Get all non-None layer names as a list."""
        return [
            layer
            for layer in [
                self.layer1,
                self.layer2,
                self.layer3,
                self.layer4,
                self.layer5,
            ]
            if layer is not None
        ]
