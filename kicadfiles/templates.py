"""KiCad File Templates.

Provides helper functions to create empty/minimal KiCad files with proper defaults.
Useful for testing, programmatic generation, or starting new designs.
"""

from __future__ import annotations

from .base_types import BoardLayers, LayerDefinition
from .board_layout import (
    General,
    KicadPcb,
    PcbPlotParams,
    Setup,
    Tenting,
)
from .footprint_library import Footprint
from .pad_and_drill import Net
from .project_settings import KicadProject
from .schematic_system import KicadSch, LibSymbols, Paper, SheetInstance, SheetInstances
from .symbol_library import KicadSymbolLib
from .text_and_documents import KicadWks

__all__ = ["KiCadTemplates"]


def _default_pcb_layers() -> list[LayerDefinition]:
    """Create default PCB layer stack (24 layers)."""
    return [
        LayerDefinition(0, "F.Cu", "signal"),
        LayerDefinition(2, "B.Cu", "signal"),
        LayerDefinition(9, "F.Adhes", "user", "F.Adhesive"),
        LayerDefinition(11, "B.Adhes", "user", "B.Adhesive"),
        LayerDefinition(13, "F.Paste", "user"),
        LayerDefinition(15, "B.Paste", "user"),
        LayerDefinition(5, "F.SilkS", "user", "F.Silkscreen"),
        LayerDefinition(7, "B.SilkS", "user", "B.Silkscreen"),
        LayerDefinition(1, "F.Mask", "user"),
        LayerDefinition(3, "B.Mask", "user"),
        LayerDefinition(17, "Dwgs.User", "user", "User.Drawings"),
        LayerDefinition(19, "Cmts.User", "user", "User.Comments"),
        LayerDefinition(21, "Eco1.User", "user", "User.Eco1"),
        LayerDefinition(23, "Eco2.User", "user", "User.Eco2"),
        LayerDefinition(25, "Edge.Cuts", "user"),
        LayerDefinition(27, "Margin", "user"),
        LayerDefinition(31, "F.CrtYd", "user", "F.Courtyard"),
        LayerDefinition(29, "B.CrtYd", "user", "B.Courtyard"),
        LayerDefinition(35, "F.Fab", "user"),
        LayerDefinition(33, "B.Fab", "user"),
        LayerDefinition(39, "User.1", "user"),
        LayerDefinition(41, "User.2", "user"),
        LayerDefinition(43, "User.3", "user"),
        LayerDefinition(45, "User.4", "user"),
    ]


class KiCadTemplates:
    """Helper class for creating empty/minimal KiCad files.

    All methods return objects with minimal required fields set to sensible defaults.
    You can then modify these objects before saving.

    Example:
        >>> from kicadfiles.templates import KiCadTemplates
        >>> pcb = KiCadTemplates.pcb()
        >>> pcb.save_to_file("my_board.kicad_pcb")
    """

    @staticmethod
    def pcb(
        version: int = 20241229,
        generator: str = "pcbnew",
        generator_version: str = "9.0",
    ) -> KicadPcb:
        """Create an empty PCB file.

        Args:
            version: KiCad format version (default: 20241229 for KiCad 9.0).
            generator: Generator name (default: "pcbnew").
            generator_version: Generator version (default: "9.0").

        Returns:
            Minimal KicadPcb object.

        Example:
            >>> pcb = KiCadTemplates.pcb()
            >>> pcb.footprints = []  # Add footprints
            >>> pcb.save_to_file("board.kicad_pcb")
        """
        pcb = KicadPcb()
        pcb.general = General()
        pcb.layers = BoardLayers(layer_defs=_default_pcb_layers())
        pcb.setup = Setup()
        pcb.setup.tenting = Tenting(sides=["front", "back"])
        pcb.setup.pcbplotparams = PcbPlotParams()
        pcb.nets = [Net(number=0, name="")]

        pcb.version(version)
        pcb.generator(generator)
        pcb.generator_version(generator_version)
        pcb.paper("A4")
        pcb.embedded_fonts("no")
        pcb.general.thickness(1.6)
        pcb.general.legacy_teardrops("no")
        pcb.setup.pad_to_mask_clearance(0.0)
        pcb.setup.allow_soldermask_bridges_in_footprints("no")

        return pcb

    @staticmethod
    def schematic(
        version: int = 20250114,
        generator: str = "eeschema",
        generator_version: str = "9.0",
    ) -> KicadSch:
        """Create an empty schematic file.

        Args:
            version: KiCad format version (default: 20250114 for KiCad 9.0).
            generator: Generator name (default: "eeschema").
            generator_version: Generator version (default: "9.0").

        Returns:
            Minimal KicadSch object with new UUID.

        Example:
            >>> sch = KiCadTemplates.schematic()
            >>> sch.symbols = []  # Add symbols
            >>> sch.save_to_file("schematic.kicad_sch")
        """
        sch = KicadSch()
        sch.uuid.new_id()
        sch.paper = Paper(size="A4")
        sch.lib_symbols = LibSymbols(symbols=[])
        sch.sheet_instances = SheetInstances(sheet_instances=[SheetInstance(path="/")])

        sch.version(version)
        sch.generator(generator)
        sch.generator_version(generator_version)
        sch.embedded_fonts("no")
        sch.sheet_instances.sheet_instances[0].page("1")

        return sch

    @staticmethod
    def footprint(
        library_link: str = "Empty",
        version: int = 20240108,
        generator: str = "kicadfiles",
    ) -> Footprint:
        """Create an empty footprint file.

        Args:
            library_link: Footprint identifier (default: "Empty").
            version: KiCad format version (default: 20240108).
            generator: Generator name (default: "kicadfiles").

        Returns:
            Minimal Footprint object.

        Example:
            >>> fp = KiCadTemplates.footprint("MyComponent")
            >>> fp.pads = []  # Add pads
            >>> fp.save_to_file("component.kicad_mod")
        """
        fp = Footprint(library_link=library_link)
        fp.version(version)
        fp.generator(generator)
        return fp

    @staticmethod
    def symbol_library(
        version: int = 20241209,
        generator: str = "kicadfiles",
    ) -> KicadSymbolLib:
        """Create an empty symbol library file.

        Args:
            version: KiCad format version (default: 20241209 for KiCad 9.0).
            generator: Generator name (default: "kicadfiles").

        Returns:
            Minimal KicadSymbolLib object.

        Example:
            >>> lib = KiCadTemplates.symbol_library()
            >>> lib.symbols = []  # Add symbols
            >>> lib.save_to_file("library.kicad_sym")
        """
        lib = KicadSymbolLib()
        lib.version(version)
        lib.generator(generator)
        return lib

    @staticmethod
    def worksheet(
        version: int = 20231003,
        generator: str = "kicadfiles",
    ) -> KicadWks:
        """Create an empty worksheet/drawing sheet file.

        Args:
            version: KiCad format version (default: 20231003).
            generator: Generator name (default: "kicadfiles").

        Returns:
            Minimal KicadWks object.

        Example:
            >>> wks = KiCadTemplates.worksheet()
            >>> wks.save_to_file("template.kicad_wks")
        """
        wks = KicadWks()
        wks.version(version)
        wks.generator(generator)
        return wks

    @staticmethod
    def project() -> KicadProject:
        """Create an empty project file (JSON format).

        Returns:
            Minimal KicadProject object.

        Example:
            >>> proj = KiCadTemplates.project()
            >>> proj.save_to_file("project.kicad_pro")
        """
        return KicadProject()
