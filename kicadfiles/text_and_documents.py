"""Text and document related elements for KiCad S-expressions."""

from dataclasses import dataclass, field
from typing import Any, ClassVar, List, Optional

from .base_element import (
    NamedFloat,
    NamedInt,
    NamedObject,
    NamedString,
    ParseStrictness,
    TokenFlag,
)
from .base_types import (
    AtXY,
    End,
    Font,
    Justify,
    Pos,
    Size,
    Start,
    Uuid,
)


@dataclass
class Comment(NamedObject):
    """Comment definition token.

    The 'comment' token defines document comments in the format::

        (comment N "COMMENT")

    Where N is a number from 1 to 9.

    Args:
        number: Comment number (1-9)
        text: Comment text
    """

    __token_name__: ClassVar[str] = "comment"

    number: int = field(default=1, metadata={"description": "Comment number (1-9)"})
    text: str = field(default="", metadata={"description": "Comment text"})


@dataclass
class Data(NamedObject):
    """Data definition token.

    The 'data' token defines hexadecimal byte data in the format::

        (data XX1 ... XXN)

    Where XXN represents hexadecimal bytes separated by spaces, with a maximum of 32 bytes per data token.

    Args:
        hex_bytes: Hexadecimal byte values (up to 32 bytes)
    """

    __token_name__: ClassVar[str] = "data"

    hex_bytes: List[str] = field(
        default_factory=list,
        metadata={"description": "Hexadecimal byte values (up to 32 bytes)"},
    )


@dataclass
class Paper(NamedObject):
    """Paper settings definition token.

    The 'paper' token defines paper size and orientation in the format::

        (paper PAPER_SIZE | WIDTH HEIGHT [portrait])

    Where PAPER_SIZE can be: A0, A1, A2, A3, A4, A5, A, B, C, D, E.

    Args:
        size: Standard paper size (optional)
        width: Custom paper width (optional)
        height: Custom paper height (optional)
        portrait: Whether paper is in portrait mode (optional)
    """

    __token_name__: ClassVar[str] = "paper"

    size: Optional[str] = field(
        default=None, metadata={"description": "Standard paper size", "required": False}
    )
    width: Optional[float] = field(
        default=None, metadata={"description": "Custom paper width", "required": False}
    )
    height: Optional[float] = field(
        default=None, metadata={"description": "Custom paper height", "required": False}
    )
    portrait: TokenFlag = field(
        default_factory=lambda: TokenFlag("portrait"),
        metadata={
            "description": "Whether paper is in portrait mode",
            "required": False,
        },
    )


@dataclass
class TitleBlock(NamedObject):
    """Title block definition token.

    The 'title_block' token defines the document title block in the format::

        (title_block
            (title "TITLE")
            (date "DATE")
            (rev "REVISION")
            (company "COMPANY_NAME")
            (comment N "COMMENT")
        )

    Args:
        title: Document title (optional)
        date: Document date (optional)
        rev: Document revision (optional)
        company: Company name (optional)
        comments: List of comments (optional)
    """

    __token_name__: ClassVar[str] = "title_block"

    title: NamedString = field(
        default_factory=lambda: NamedString("title", ""),
        metadata={"description": "Document title", "required": False},
    )
    date: NamedString = field(
        default_factory=lambda: NamedString("date", ""),
        metadata={"description": "Document date", "required": False},
    )
    rev: NamedString = field(
        default_factory=lambda: NamedString("rev", ""),
        metadata={"description": "Document revision", "required": False},
    )
    company: NamedString = field(
        default_factory=lambda: NamedString("company", ""),
        metadata={"description": "Company name", "required": False},
    )
    comments: Optional[List[Comment]] = field(
        default_factory=list,
        metadata={"description": "List of comments", "required": False},
    )


@dataclass
class Tbtext(NamedObject):
    """Title block text definition token.

    The 'tbtext' token defines text elements in the title block in the format::

        (tbtext
            "TEXT"
            (name "NAME")
            (pos X Y [CORNER])
            (font [(size WIDTH HEIGHT)] [bold] [italic])
            [(repeat COUNT)]
            [(incrx DISTANCE)]
            [(incry DISTANCE)]
            [(comment "COMMENT")]
        )

    Args:
        text: Text content
        name: Text element name
        pos: Position coordinates
        font: Font settings (optional)
        repeat: Repeat count for incremental text (optional)
        incrx: Repeat distance on X axis (optional)
        incry: Repeat distance on Y axis (optional)
        comment: Comment for the text object (optional)
    """

    __token_name__: ClassVar[str] = "tbtext"

    text: str = field(default="", metadata={"description": "Text content"})
    name: NamedString = field(
        default_factory=lambda: NamedString("name", ""),
        metadata={"description": "Text element name"},
    )
    pos: Pos = field(
        default_factory=lambda: Pos(), metadata={"description": "Position coordinates"}
    )
    font: Optional[Font] = field(
        default=None, metadata={"description": "Font settings", "required": False}
    )
    repeat: NamedInt = field(
        default_factory=lambda: NamedInt("repeat", 0),
        metadata={
            "description": "Repeat count for incremental text",
            "required": False,
        },
    )
    incrx: NamedFloat = field(
        default_factory=lambda: NamedFloat("incrx", 0.0),
        metadata={"description": "Repeat distance on X axis", "required": False},
    )
    incry: NamedFloat = field(
        default_factory=lambda: NamedFloat("incry", 0.0),
        metadata={"description": "Repeat distance on Y axis", "required": False},
    )
    comment: Optional[str] = field(
        default=None,
        metadata={"description": "Comment for the text object", "required": False},
    )


@dataclass
class Textsize(NamedObject):
    """Text size definition token.

    The 'textsize' token defines text size in the format::

        (textsize WIDTH HEIGHT)

    Args:
        size: Text size (width and height)
    """

    __token_name__: ClassVar[str] = "textsize"

    size: Size = field(
        default_factory=lambda: Size(),
        metadata={"description": "Text size (width and height)"},
    )


@dataclass
class Members(NamedObject):
    """Group members definition token.

    The 'members' token defines the members of a group in the format::

        (members UUID1 UUID2 ... UUIDN)

    Args:
        uuids: List of member UUIDs
    """

    __token_name__: ClassVar[str] = "members"

    uuids: List[str] = field(
        default_factory=list, metadata={"description": "List of member UUIDs"}
    )


@dataclass
class Group(NamedObject):
    """Group definition token.

    The 'group' token defines a group of objects in the format::

        (group
            "NAME"
            (uuid UUID)
            (members UUID1 ... UUIDN)
        )

    Args:
        name: Group name
        uuid: Group unique identifier (optional)
        members: List of member UUIDs (optional)
    """

    __token_name__: ClassVar[str] = "group"

    name: str = field(default="", metadata={"description": "Group name"})
    uuid: Optional[Uuid] = field(
        default=None,
        metadata={"description": "Group unique identifier", "required": False},
    )
    members: Optional[Members] = field(
        default=None,
        metadata={"description": "List of member UUIDs", "required": False},
    )


@dataclass
class WksTextsize(NamedObject):
    """Worksheet text size definition token.

    Args:
        width: Text width
        height: Text height
    """

    __token_name__: ClassVar[str] = "textsize"

    width: float = field(
        default=1.0,
        metadata={"description": "Text width"},
    )
    height: float = field(
        default=1.0,
        metadata={"description": "Text height"},
    )


@dataclass
class WksSetup(NamedObject):
    """Worksheet setup definition token.

    Args:
        textsize: Text size (optional)
        linewidth: Line width (optional)
        textlinewidth: Text line width (optional)
        left_margin: Left margin (optional)
        right_margin: Right margin (optional)
        top_margin: Top margin (optional)
        bottom_margin: Bottom margin (optional)
    """

    __token_name__: ClassVar[str] = "setup"

    textsize: Optional[WksTextsize] = field(
        default=None,
        metadata={"description": "Text size", "required": False},
    )
    linewidth: NamedFloat = field(
        default_factory=lambda: NamedFloat("linewidth", 0.0),
        metadata={"description": "Line width", "required": False},
    )
    textlinewidth: NamedFloat = field(
        default_factory=lambda: NamedFloat("textlinewidth", 0.0),
        metadata={"description": "Text line width", "required": False},
    )
    left_margin: NamedFloat = field(
        default_factory=lambda: NamedFloat("left_margin", 0.0),
        metadata={"description": "Left margin", "required": False},
    )
    right_margin: NamedFloat = field(
        default_factory=lambda: NamedFloat("right_margin", 0.0),
        metadata={"description": "Right margin", "required": False},
    )
    top_margin: NamedFloat = field(
        default_factory=lambda: NamedFloat("top_margin", 0.0),
        metadata={"description": "Top margin", "required": False},
    )
    bottom_margin: NamedFloat = field(
        default_factory=lambda: NamedFloat("bottom_margin", 0.0),
        metadata={"description": "Bottom margin", "required": False},
    )


@dataclass
class WksRect(NamedObject):
    """Worksheet rectangle definition token.

    Args:
        name: Rectangle name (optional)
        start: Start position
        end: End position
        comment: Comment (optional)
        repeat: Repeat count (optional)
        incrx: X increment (optional)
        incry: Y increment (optional)
        linewidth: Line width (optional)
    """

    __token_name__: ClassVar[str] = "rect"

    name: Optional[str] = field(
        default=None, metadata={"description": "Rectangle name", "required": False}
    )
    start: Start = field(
        default_factory=lambda: Start(), metadata={"description": "Start position"}
    )
    end: End = field(
        default_factory=lambda: End(), metadata={"description": "End position"}
    )
    comment: NamedString = field(
        default_factory=lambda: NamedString("comment", ""),
        metadata={"description": "Comment", "required": False},
    )
    repeat: NamedInt = field(
        default_factory=lambda: NamedInt("repeat", 0),
        metadata={"description": "Repeat count", "required": False},
    )
    incrx: NamedFloat = field(
        default_factory=lambda: NamedFloat("incrx", 0.0),
        metadata={"description": "X increment", "required": False},
    )
    incry: NamedFloat = field(
        default_factory=lambda: NamedFloat("incry", 0.0),
        metadata={"description": "Y increment", "required": False},
    )
    linewidth: NamedFloat = field(
        default_factory=lambda: NamedFloat("linewidth", 0.0),
        metadata={"description": "Line width", "required": False},
    )


@dataclass
class WksLine(NamedObject):
    """Worksheet line definition token.

    Args:
        name: Line name (optional)
        start: Start position
        end: End position
        repeat: Repeat count (optional)
        incrx: X increment (optional)
        incry: Y increment (optional)
    """

    __token_name__: ClassVar[str] = "line"

    name: Optional[str] = field(
        default=None, metadata={"description": "Line name", "required": False}
    )
    start: Start = field(
        default_factory=lambda: Start(), metadata={"description": "Start position"}
    )
    end: End = field(
        default_factory=lambda: End(), metadata={"description": "End position"}
    )
    repeat: NamedInt = field(
        default_factory=lambda: NamedInt("repeat", 0),
        metadata={"description": "Repeat count", "required": False},
    )
    incrx: NamedFloat = field(
        default_factory=lambda: NamedFloat("incrx", 0.0),
        metadata={"description": "X increment", "required": False},
    )
    incry: NamedFloat = field(
        default_factory=lambda: NamedFloat("incry", 0.0),
        metadata={"description": "Y increment", "required": False},
    )


@dataclass
class WksTbText(NamedObject):
    """Worksheet text block definition token.

    Args:
        text: Text content
        name: Text name (optional)
        pos: Text position
        font: Font settings (optional)
        justify: Text justification (optional)
        repeat: Repeat count (optional)
        incrx: X increment (optional)
        incry: Y increment (optional)
        comment: Comment (optional)
    """

    __token_name__: ClassVar[str] = "tbtext"

    text: str = field(default="", metadata={"description": "Text content"})
    name: NamedString = field(
        default_factory=lambda: NamedString("name", ""),
        metadata={"description": "Text name", "required": False},
    )
    pos: Pos = field(
        default_factory=lambda: Pos(), metadata={"description": "Text position"}
    )
    font: Optional[Font] = field(
        default=None, metadata={"description": "Font settings", "required": False}
    )
    justify: Optional[Justify] = field(
        default=None, metadata={"description": "Text justification", "required": False}
    )
    repeat: NamedInt = field(
        default_factory=lambda: NamedInt("repeat", 0),
        metadata={"description": "Repeat count", "required": False},
    )
    incrx: NamedFloat = field(
        default_factory=lambda: NamedFloat("incrx", 0.0),
        metadata={"description": "X increment", "required": False},
    )
    incry: NamedFloat = field(
        default_factory=lambda: NamedFloat("incry", 0.0),
        metadata={"description": "Y increment", "required": False},
    )
    comment: NamedString = field(
        default_factory=lambda: NamedString("comment", ""),
        metadata={"description": "Comment", "required": False},
    )


@dataclass
class KicadWks(NamedObject):
    """KiCad worksheet definition token.

    The 'kicad_wks' token defines worksheet format information in the format::

        (kicad_wks
            (version VERSION)
            (generator GENERATOR)
            ;; contents of the schematic file...
        )

    Args:
        version: Format version (optional)
        generator: Generator name (optional)
        generator_version: Generator version (optional)
        page: Page settings (optional)
        title_block: Title block (optional)
        setup: Worksheet setup (optional)
        rect: List of rectangles (optional)
        line: List of lines (optional)
        tbtext: List of text blocks (optional)
        elements: List of worksheet elements (optional)
    """

    __token_name__: ClassVar[str] = "kicad_wks"
    __legacy_token_names__ = ["page_layout"]

    version: NamedInt = field(
        default_factory=lambda: NamedInt("version", 0),
        metadata={"description": "Format version", "required": False},
    )
    generator: NamedString = field(
        default_factory=lambda: NamedString("generator", ""),
        metadata={"description": "Generator name", "required": False},
    )
    generator_version: NamedString = field(
        default_factory=lambda: NamedString("generator_version", ""),
        metadata={"description": "Generator version", "required": False},
    )
    page: NamedString = field(
        default_factory=lambda: NamedString("page", ""),
        metadata={"description": "Page settings", "required": False},
    )
    title_block: Optional[TitleBlock] = field(
        default=None, metadata={"description": "Title block", "required": False}
    )
    setup: Optional[WksSetup] = field(
        default=None, metadata={"description": "Worksheet setup", "required": False}
    )
    rect: Optional[List[WksRect]] = field(
        default_factory=list,
        metadata={"description": "List of rectangles", "required": False},
    )
    line: Optional[List[WksLine]] = field(
        default_factory=list,
        metadata={"description": "List of lines", "required": False},
    )
    tbtext: Optional[List[WksTbText]] = field(
        default_factory=list,
        metadata={"description": "List of text blocks", "required": False},
    )
    elements: Optional[List[Any]] = field(
        default_factory=list,
        metadata={"description": "List of worksheet elements", "required": False},
    )

    @classmethod
    def from_file(
        cls,
        file_path: str,
        strictness: ParseStrictness = ParseStrictness.STRICT,
        encoding: str = "utf-8",
    ) -> "KicadWks":
        """Parse from S-expression file - convenience method for worksheet operations."""
        if not file_path.endswith(".kicad_wks"):
            raise ValueError("Unsupported file extension. Expected: .kicad_wks")
        with open(file_path, "r", encoding=encoding) as f:
            content = f.read()
        return cls.from_str(content, strictness)

    def save_to_file(self, file_path: str, encoding: str = "utf-8") -> None:
        """Save to .kicad_wks file format.

        Args:
            file_path: Path to write the .kicad_wks file
            encoding: File encoding (default: utf-8)
        """
        if not file_path.endswith(".kicad_wks"):
            raise ValueError("Unsupported file extension. Expected: .kicad_wks")
        content = self.to_sexpr_str()
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)


# Image related elements
@dataclass
class Bitmap(NamedObject):
    """Bitmap image definition token.

    The 'bitmap' token defines a bitmap image in the format::

        (bitmap
            (name "NAME")
            (pos X Y)
            (scale SCALAR)
            [(repeat COUNT)]
            [(incrx DISTANCE)]
            [(incry DISTANCE)]
            [(comment "COMMENT")]
            (pngdata IMAGE_DATA)
        )

    Args:
        name: Image name
        pos: Position coordinates
        scale: Scale factor
        repeat: Repeat count (optional)
        incrx: X increment distance (optional)
        incry: Y increment distance (optional)
        comment: Image comment (optional)
        pngdata: PNG image data
    """

    __token_name__: ClassVar[str] = "bitmap"

    name: NamedString = field(
        default_factory=lambda: NamedString("name", ""),
        metadata={"description": "Image name"},
    )
    pos: Pos = field(
        default_factory=lambda: Pos(), metadata={"description": "Position coordinates"}
    )
    scale: NamedFloat = field(
        default_factory=lambda: NamedFloat("factor", 0.0),
        metadata={"description": "Scale factor"},
    )
    repeat: NamedInt = field(
        default_factory=lambda: NamedInt("repeat", 0),
        metadata={"description": "Repeat count", "required": False},
    )
    incrx: NamedFloat = field(
        default_factory=lambda: NamedFloat("incrx", 0.0),
        metadata={"description": "X increment distance", "required": False},
    )
    incry: NamedFloat = field(
        default_factory=lambda: NamedFloat("incry", 0.0),
        metadata={"description": "Y increment distance", "required": False},
    )
    comment: Optional[str] = field(
        default=None, metadata={"description": "Image comment", "required": False}
    )
    pngdata: "Pngdata" = field(
        default_factory=lambda: Pngdata(), metadata={"description": "PNG image data"}
    )


@dataclass
class Image(NamedObject):
    """Image definition token.

    The 'image' token defines an image object in PCB files in the format::

        (image (at X Y) (scale FACTOR) (uuid UUID) (data ...))

    Args:
        at: Position
        scale: Scale factor (optional)
        uuid: Unique identifier (optional)
        data: Image data (optional)
        locked: Whether image is locked (optional)
    """

    __token_name__: ClassVar[str] = "image"

    at: AtXY = field(
        default_factory=lambda: AtXY(), metadata={"description": "Position"}
    )
    scale: NamedFloat = field(
        default_factory=lambda: NamedFloat("scale", 1.0),
        metadata={"description": "Scale factor", "required": False},
    )
    uuid: Optional[Uuid] = field(
        default=None, metadata={"description": "Unique identifier", "required": False}
    )
    data: Optional[Data] = field(
        default=None, metadata={"description": "Image data", "required": False}
    )
    locked: TokenFlag = field(
        default_factory=lambda: TokenFlag("locked"),
        metadata={"description": "Whether image is locked", "required": False},
    )


@dataclass
class Pngdata(NamedObject):
    """PNG data definition token.

    The 'pngdata' token defines PNG image data in the format::

        (pngdata
            (data XX1 ... XXN)
            (data XX1 ... XXN)
            ...
        )

    Where each data line contains up to 32 hexadecimal bytes.

    Args:
        data_lines: List of data token objects containing hexadecimal bytes
    """

    __token_name__: ClassVar[str] = "pngdata"

    data_lines: List[Data] = field(
        default_factory=list,
        metadata={
            "description": "List of data token objects containing hexadecimal bytes"
        },
    )
