"""Text and document related elements for KiCad S-expressions."""

from dataclasses import dataclass, field
from typing import Any, List, Optional

from .base_element import KiCadObject, OptionalFlag, ParseStrictness
from .base_types import (
    AtXY,
    End,
    Font,
    Id,
    Justify,
    Linewidth,
    Name,
    Pos,
    Size,
    Start,
    Uuid,
)


@dataclass
class Comment(KiCadObject):
    """Comment definition token.

    The 'comment' token defines document comments in the format::

        (comment N "COMMENT")

    Where N is a number from 1 to 9.

    Args:
        number: Comment number (1-9)
        text: Comment text
    """

    __token_name__ = "comment"

    number: int = field(default=1, metadata={"description": "Comment number (1-9)"})
    text: str = field(default="", metadata={"description": "Comment text"})


@dataclass
class Company(KiCadObject):
    """Company definition token.

    The 'company' token defines the document company name in the format::

        (company "COMPANY_NAME")

    Args:
        name: Company name
    """

    __token_name__ = "company"

    name: str = field(default="", metadata={"description": "Company name"})


@dataclass
class Data(KiCadObject):
    """Data definition token.

    The 'data' token defines hexadecimal byte data in the format::

        (data XX1 ... XXN)

    Where XXN represents hexadecimal bytes separated by spaces, with a maximum of 32 bytes per data token.

    Args:
        hex_bytes: Hexadecimal byte values (up to 32 bytes)
    """

    __token_name__ = "data"

    hex_bytes: List[str] = field(
        default_factory=list,
        metadata={"description": "Hexadecimal byte values (up to 32 bytes)"},
    )


@dataclass
class Date(KiCadObject):
    """Date definition token.

    The 'date' token defines the document date in the format::

        (date "DATE")

    Using YYYY-MM-DD format.

    Args:
        date: Document date (YYYY-MM-DD format)
    """

    __token_name__ = "date"

    date: str = field(
        default="", metadata={"description": "Document date (YYYY-MM-DD format)"}
    )


@dataclass
class Descr(KiCadObject):
    """Description definition token.

    The 'descr' token defines document description in the format::

        (descr "DESCRIPTION")

    Args:
        description: Description text
    """

    __token_name__ = "descr"

    description: str = field(default="", metadata={"description": "Description text"})


@dataclass
class Generator(KiCadObject):
    """Generator definition token.

    The 'generator' token defines the software generator information in the format::

        (generator GENERATOR)

    Args:
        name: Generator name
    """

    __token_name__ = "generator"

    name: str = field(default="", metadata={"description": "Generator name"})


@dataclass
class GeneratorVersion(KiCadObject):
    """Generator version definition token.

    The 'generator_version' token defines the software generator version in the format::

        (generator_version VERSION)

    Args:
        version: Generator version
    """

    __token_name__ = "generator_version"

    version: str = field(default="", metadata={"description": "Generator version"})


@dataclass
class Page(KiCadObject):
    """Page number definition token.

    The 'page' token defines the page number in the format::

        (page "NUMBER")

    Args:
        number: Page number
    """

    __token_name__ = "page"

    number: str = field(default="", metadata={"description": "Page number"})


@dataclass
class Paper(KiCadObject):
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

    __token_name__ = "paper"

    size: Optional[str] = field(
        default=None, metadata={"description": "Standard paper size", "required": False}
    )
    width: Optional[float] = field(
        default=None, metadata={"description": "Custom paper width", "required": False}
    )
    height: Optional[float] = field(
        default=None, metadata={"description": "Custom paper height", "required": False}
    )
    portrait: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("portrait"),
        metadata={
            "description": "Whether paper is in portrait mode",
            "required": False,
        },
    )


@dataclass
class Rev(KiCadObject):
    """Revision definition token.

    The 'rev' token defines the document revision in the format::

        (rev "REVISION")

    Args:
        revision: Revision string
    """

    __token_name__ = "rev"

    revision: str = field(default="", metadata={"description": "Revision string"})


@dataclass
class Tedit(KiCadObject):
    """Edit timestamp definition token.

    The 'tedit' token defines the last edit timestamp in the format::

        (tedit TIMESTAMP)

    Args:
        timestamp: Edit timestamp
    """

    __token_name__ = "tedit"

    timestamp: str = field(default="0", metadata={"description": "Edit timestamp"})


@dataclass
class Title(KiCadObject):
    """Title definition token.

    The 'title' token defines a document title in the format::

        (title "TITLE_STRING")

    Args:
        value: Title string
    """

    __token_name__ = "title"

    value: str = field(default="", metadata={"description": "Title string"})


@dataclass
class TitleBlock(KiCadObject):
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

    __token_name__ = "title_block"

    title: Optional[Title] = field(
        default=None,
        metadata={"description": "Document title", "required": False},
    )
    date: Optional[Date] = field(
        default=None, metadata={"description": "Document date", "required": False}
    )
    rev: Optional[Rev] = field(
        default=None, metadata={"description": "Document revision", "required": False}
    )
    company: Optional[Company] = field(
        default=None, metadata={"description": "Company name", "required": False}
    )
    comments: Optional[List[Comment]] = field(
        default_factory=list,
        metadata={"description": "List of comments", "required": False},
    )


@dataclass
class Version(KiCadObject):
    """Version definition token.

    The 'version' token defines the file format version in the format::

        (version VERSION_NUMBER)

    Args:
        version: File format version number
    """

    __token_name__ = "version"

    version: int = field(
        default=1, metadata={"description": "File format version number"}
    )


@dataclass
class BottomMargin(KiCadObject):
    """Bottom margin definition token.

    The 'bottom_margin' token defines the bottom page margin in the format::

        (bottom_margin DISTANCE)

    Args:
        margin: Bottom margin value
    """

    __token_name__ = "bottom_margin"

    margin: float = field(default=0.0, metadata={"description": "Bottom margin value"})


@dataclass
class LeftMargin(KiCadObject):
    """Left margin definition token.

    The 'left_margin' token defines the left page margin in the format::

        (left_margin DISTANCE)

    Args:
        margin: Left margin value
    """

    __token_name__ = "left_margin"

    margin: float = field(default=0.0, metadata={"description": "Left margin value"})


@dataclass
class RightMargin(KiCadObject):
    """Right margin definition token.

    The 'right_margin' token defines the right page margin in the format::

        (right_margin DISTANCE)

    Args:
        margin: Right margin value
    """

    __token_name__ = "right_margin"

    margin: float = field(default=0.0, metadata={"description": "Right margin value"})


@dataclass
class RepeatCount(KiCadObject):
    """Repeat count definition token.

    Args:
        count: Repeat count
    """

    __token_name__ = "repeat"

    count: int = field(default=1, metadata={"description": "Repeat count"})


@dataclass
class Incrx(KiCadObject):
    """X increment definition token.

    Args:
        distance: X increment distance
    """

    __token_name__ = "incrx"

    distance: float = field(
        default=0.0, metadata={"description": "X increment distance"}
    )


@dataclass
class Incry(KiCadObject):
    """Y increment definition token.

    Args:
        distance: Y increment distance
    """

    __token_name__ = "incry"

    distance: float = field(
        default=0.0, metadata={"description": "Y increment distance"}
    )


@dataclass
class Tbtext(KiCadObject):
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

    __token_name__ = "tbtext"

    text: str = field(default="", metadata={"description": "Text content"})
    name: Name = field(
        default_factory=lambda: Name(), metadata={"description": "Text element name"}
    )
    pos: Pos = field(
        default_factory=lambda: Pos(), metadata={"description": "Position coordinates"}
    )
    font: Optional[Font] = field(
        default=None, metadata={"description": "Font settings", "required": False}
    )
    repeat: Optional[RepeatCount] = field(
        default=None,
        metadata={
            "description": "Repeat count for incremental text",
            "required": False,
        },
    )
    incrx: Optional[Incrx] = field(
        default=None,
        metadata={"description": "Repeat distance on X axis", "required": False},
    )
    incry: Optional[Incry] = field(
        default=None,
        metadata={"description": "Repeat distance on Y axis", "required": False},
    )
    comment: Optional[str] = field(
        default=None,
        metadata={"description": "Comment for the text object", "required": False},
    )


@dataclass
class Textlinewidth(KiCadObject):
    """Text line width definition token.

    The 'textlinewidth' token defines the line width for text outlines in the format::

        (textlinewidth WIDTH)

    Args:
        width: Text line width
    """

    __token_name__ = "textlinewidth"

    width: float = field(default=0.0, metadata={"description": "Text line width"})


@dataclass
class Textsize(KiCadObject):
    """Text size definition token.

    The 'textsize' token defines text size in the format::

        (textsize WIDTH HEIGHT)

    Args:
        size: Text size (width and height)
    """

    __token_name__ = "textsize"

    size: Size = field(
        default_factory=lambda: Size(),
        metadata={"description": "Text size (width and height)"},
    )


@dataclass
class TopMargin(KiCadObject):
    """Top margin definition token.

    The 'top_margin' token defines the top page margin in the format::

        (top_margin DISTANCE)

    Args:
        margin: Top margin value
    """

    __token_name__ = "top_margin"

    margin: float = field(default=0.0, metadata={"description": "Top margin value"})


@dataclass
class Suffix(KiCadObject):
    """Suffix definition token.

    The 'suffix' token defines a suffix string in the format::

        (suffix "SUFFIX")

    Args:
        suffix: Suffix string
    """

    __token_name__ = "suffix"

    suffix: str = field(default="", metadata={"description": "Suffix string"})


@dataclass
class Scale(KiCadObject):
    """Scale definition token for 2D elements.

    The 'scale' token defines scaling factor in the format:
        (scale SCALAR)

    For 3D model scaling, use ModelScale class which supports (scale (xyz X Y Z)) format.

    Args:
        factor: Scale factor for 2D elements
    """

    __token_name__ = "scale"

    factor: float = field(
        default=1.0,
        metadata={"description": "Scale factor for 2D elements"},
    )


@dataclass
class Members(KiCadObject):
    """Group members definition token.

    The 'members' token defines the members of a group in the format::

        (members UUID1 UUID2 ... UUIDN)

    Args:
        uuids: List of member UUIDs
    """

    __token_name__ = "members"

    uuids: List[Uuid] = field(
        default_factory=list, metadata={"description": "List of member UUIDs"}
    )


@dataclass
class Group(KiCadObject):
    """Group definition token.

    The 'group' token defines a group of objects in the format::

        (group
            "NAME"
            (id UUID)
            (members UUID1 ... UUIDN)
        )

    Args:
        name: Group name
        id: Group unique identifier
        members: List of member UUIDs (optional)
    """

    __token_name__ = "group"

    name: str = field(default="", metadata={"description": "Group name"})
    id: Id = field(
        default_factory=lambda: Id(),
        metadata={"description": "Group unique identifier"},
    )
    members: Optional[Members] = field(
        default=None,
        metadata={"description": "List of member UUIDs", "required": False},
    )


@dataclass
class WksTextsize(KiCadObject):
    """Worksheet text size definition token.

    Args:
        width: Text width
        height: Text height
    """

    __token_name__ = "textsize"

    width: float = field(
        default=1.0,
        metadata={"description": "Text width"},
    )
    height: float = field(
        default=1.0,
        metadata={"description": "Text height"},
    )


@dataclass
class WksLinewidth(KiCadObject):
    """Worksheet line width definition token.

    Args:
        value: Line width value
    """

    __token_name__ = "linewidth"

    value: float = field(
        default=0.15,
        metadata={"description": "Line width value"},
    )


@dataclass
class WksTextlinewidth(KiCadObject):
    """Worksheet text line width definition token.

    Args:
        value: Text line width value
    """

    __token_name__ = "textlinewidth"

    value: float = field(
        default=0.15,
        metadata={"description": "Text line width value"},
    )


@dataclass
class WksMargin(KiCadObject):
    """Worksheet margin definition token.

    Args:
        value: Margin value
    """

    __token_name__ = "margin"

    value: float = field(
        default=10.0,
        metadata={"description": "Margin value"},
    )


@dataclass
class WksLeftMargin(KiCadObject):
    """Worksheet left margin definition token.

    Args:
        value: Left margin distance value
    """

    __token_name__ = "left_margin"

    value: float = field(
        default=10.0,
        metadata={"description": "Left margin distance value"},
    )


@dataclass
class WksRightMargin(KiCadObject):
    """Worksheet right margin definition token.

    Args:
        value: Right margin distance value
    """

    __token_name__ = "right_margin"

    value: float = field(
        default=10.0,
        metadata={"description": "Right margin distance value"},
    )


@dataclass
class WksTopMargin(KiCadObject):
    """Worksheet top margin definition token.

    Args:
        value: Top margin distance value
    """

    __token_name__ = "top_margin"

    value: float = field(
        default=10.0,
        metadata={"description": "Top margin distance value"},
    )


@dataclass
class WksBottomMargin(KiCadObject):
    """Worksheet bottom margin definition token.

    Args:
        value: Bottom margin distance value
    """

    __token_name__ = "bottom_margin"

    value: float = field(
        default=10.0,
        metadata={"description": "Bottom margin distance value"},
    )


@dataclass
class WksSetup(KiCadObject):
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

    __token_name__ = "setup"

    textsize: Optional[WksTextsize] = field(
        default=None,
        metadata={"description": "Text size", "required": False},
    )
    linewidth: Optional[WksLinewidth] = field(
        default=None,
        metadata={"description": "Line width", "required": False},
    )
    textlinewidth: Optional[WksTextlinewidth] = field(
        default=None,
        metadata={"description": "Text line width", "required": False},
    )
    left_margin: Optional[WksLeftMargin] = field(
        default=None,
        metadata={"description": "Left margin", "required": False},
    )
    right_margin: Optional[WksRightMargin] = field(
        default=None,
        metadata={"description": "Right margin", "required": False},
    )
    top_margin: Optional[WksTopMargin] = field(
        default=None,
        metadata={"description": "Top margin", "required": False},
    )
    bottom_margin: Optional[WksBottomMargin] = field(
        default=None,
        metadata={"description": "Bottom margin", "required": False},
    )


@dataclass
class WksComment(KiCadObject):
    """Worksheet comment definition token.

    Args:
        value: Comment text
    """

    __token_name__ = "comment"

    value: str = field(default="", metadata={"description": "Comment text"})


@dataclass
class WksRect(KiCadObject):
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

    __token_name__ = "rect"

    name: Optional[str] = field(
        default=None, metadata={"description": "Rectangle name", "required": False}
    )
    start: Start = field(
        default_factory=lambda: Start(), metadata={"description": "Start position"}
    )
    end: End = field(
        default_factory=lambda: End(), metadata={"description": "End position"}
    )
    comment: Optional[WksComment] = field(
        default=None, metadata={"description": "Comment", "required": False}
    )
    repeat: Optional[RepeatCount] = field(
        default=None, metadata={"description": "Repeat count", "required": False}
    )
    incrx: Optional[Incrx] = field(
        default=None, metadata={"description": "X increment", "required": False}
    )
    incry: Optional[Incry] = field(
        default=None, metadata={"description": "Y increment", "required": False}
    )
    linewidth: Optional[Linewidth] = field(
        default=None, metadata={"description": "Line width", "required": False}
    )


@dataclass
class WksLine(KiCadObject):
    """Worksheet line definition token.

    Args:
        name: Line name (optional)
        start: Start position
        end: End position
        repeat: Repeat count (optional)
        incrx: X increment (optional)
        incry: Y increment (optional)
    """

    __token_name__ = "line"

    name: Optional[str] = field(
        default=None, metadata={"description": "Line name", "required": False}
    )
    start: Start = field(
        default_factory=lambda: Start(), metadata={"description": "Start position"}
    )
    end: End = field(
        default_factory=lambda: End(), metadata={"description": "End position"}
    )
    repeat: Optional[RepeatCount] = field(
        default=None, metadata={"description": "Repeat count", "required": False}
    )
    incrx: Optional[Incrx] = field(
        default=None, metadata={"description": "X increment", "required": False}
    )
    incry: Optional[Incry] = field(
        default=None, metadata={"description": "Y increment", "required": False}
    )


@dataclass
class WksTbText(KiCadObject):
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

    __token_name__ = "tbtext"

    text: str = field(default="", metadata={"description": "Text content"})
    name: Optional[Name] = field(
        default=None, metadata={"description": "Text name", "required": False}
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
    repeat: Optional[RepeatCount] = field(
        default=None, metadata={"description": "Repeat count", "required": False}
    )
    incrx: Optional[Incrx] = field(
        default=None, metadata={"description": "X increment", "required": False}
    )
    incry: Optional[Incry] = field(
        default=None, metadata={"description": "Y increment", "required": False}
    )
    comment: Optional[WksComment] = field(
        default=None, metadata={"description": "Comment", "required": False}
    )


@dataclass
class KicadWks(KiCadObject):
    """KiCad worksheet definition token.

    The 'kicad_wks' token defines worksheet format information in the format::

        (kicad_wks
            (version VERSION)
            (generator GENERATOR)
            ;; contents of the schematic file...
        )

    Args:
        version: Format version
        generator: Generator name
        generator_version: Generator version (optional)
        page: Page settings (optional)
        title_block: Title block (optional)
        setup: Worksheet setup (optional)
        rect: List of rectangles (optional)
        line: List of lines (optional)
        tbtext: List of text blocks (optional)
        elements: List of worksheet elements (optional)
    """

    __token_name__ = "kicad_wks"
    __legacy_token_names__ = ["page_layout"]

    version: Optional[Version] = field(
        default=None, metadata={"description": "Format version"}
    )
    generator: Optional[Generator] = field(
        default=None, metadata={"description": "Generator name"}
    )
    generator_version: Optional[GeneratorVersion] = field(
        default=None,
        metadata={"description": "Generator version", "required": False},
    )
    page: Optional[Page] = field(
        default=None, metadata={"description": "Page settings", "required": False}
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
class Bitmap(KiCadObject):
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

    __token_name__ = "bitmap"

    name: Name = field(
        default_factory=lambda: Name(), metadata={"description": "Image name"}
    )
    pos: Pos = field(
        default_factory=lambda: Pos(), metadata={"description": "Position coordinates"}
    )
    scale: Scale = field(
        default_factory=lambda: Scale(), metadata={"description": "Scale factor"}
    )
    repeat: Optional[RepeatCount] = field(
        default=None, metadata={"description": "Repeat count", "required": False}
    )
    incrx: Optional[Incrx] = field(
        default=None,
        metadata={"description": "X increment distance", "required": False},
    )
    incry: Optional[Incry] = field(
        default=None,
        metadata={"description": "Y increment distance", "required": False},
    )
    comment: Optional[str] = field(
        default=None, metadata={"description": "Image comment", "required": False}
    )
    pngdata: "Pngdata" = field(
        default_factory=lambda: Pngdata(), metadata={"description": "PNG image data"}
    )


@dataclass
class Image(KiCadObject):
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

    __token_name__ = "image"

    at: AtXY = field(
        default_factory=lambda: AtXY(), metadata={"description": "Position"}
    )
    scale: Optional[Scale] = field(
        default=None, metadata={"description": "Scale factor", "required": False}
    )
    uuid: Optional[Uuid] = field(
        default=None, metadata={"description": "Unique identifier", "required": False}
    )
    data: Optional[Data] = field(
        default=None, metadata={"description": "Image data", "required": False}
    )
    locked: Optional[OptionalFlag] = field(
        default_factory=lambda: OptionalFlag.create_bool_flag("locked"),
        metadata={"description": "Whether image is locked", "required": False},
    )


@dataclass
class Pngdata(KiCadObject):
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

    __token_name__ = "pngdata"

    data_lines: List[Data] = field(
        default_factory=list,
        metadata={
            "description": "List of data token objects containing hexadecimal bytes"
        },
    )
