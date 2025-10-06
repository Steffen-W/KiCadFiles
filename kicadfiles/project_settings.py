"""Project settings elements for KiCad JSON project files - .kicad_pro format."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .base_element import ParseStrictness
from .json_base_element import JsonObject


@dataclass
class BoardDefaults(JsonObject):
    """Board design defaults settings.

    In the standard KiCad.kicad_pro file, this is an empty object {},
    so all fields are optional and represent extended configurations.
    """

    # All fields are optional since standard file has empty defaults {}
    apply_defaults_to_fp_fields: Optional[bool] = field(default=None)
    apply_defaults_to_fp_shapes: Optional[bool] = field(default=None)
    apply_defaults_to_fp_text: Optional[bool] = field(default=None)
    board_outline_line_width: Optional[float] = field(default=None)
    copper_line_width: Optional[float] = field(default=None)
    copper_text_italic: Optional[bool] = field(default=None)
    copper_text_size_h: Optional[float] = field(default=None)
    copper_text_size_v: Optional[float] = field(default=None)
    copper_text_thickness: Optional[float] = field(default=None)
    copper_text_upright: Optional[bool] = field(default=None)
    courtyard_line_width: Optional[float] = field(default=None)
    dimension_precision: Optional[int] = field(default=None)
    dimension_units: Optional[int] = field(default=None)
    dimensions: Optional[Dict[str, Any]] = field(default=None)
    fab_line_width: Optional[float] = field(default=None)
    fab_text_italic: Optional[bool] = field(default=None)
    fab_text_size_h: Optional[float] = field(default=None)
    fab_text_size_v: Optional[float] = field(default=None)
    fab_text_thickness: Optional[float] = field(default=None)
    fab_text_upright: Optional[bool] = field(default=None)
    other_line_width: Optional[float] = field(default=None)
    other_text_italic: Optional[bool] = field(default=None)
    other_text_size_h: Optional[float] = field(default=None)
    other_text_size_v: Optional[float] = field(default=None)
    other_text_thickness: Optional[float] = field(default=None)
    other_text_upright: Optional[bool] = field(default=None)
    pads: Optional[Dict[str, Any]] = field(default=None)
    silk_line_width: Optional[float] = field(default=None)
    silk_text_italic: Optional[bool] = field(default=None)
    silk_text_size_h: Optional[float] = field(default=None)
    silk_text_size_v: Optional[float] = field(default=None)
    silk_text_thickness: Optional[float] = field(default=None)
    silk_text_upright: Optional[bool] = field(default=None)
    zones: Optional[Dict[str, Any]] = field(default=None)


@dataclass
class DesignSettings(JsonObject):
    """Board design settings.

    Based on standard KiCad.kicad_pro structure.
    """

    defaults: BoardDefaults = field(default_factory=lambda: BoardDefaults())
    diff_pair_dimensions: List[Dict[str, Any]] = field(default_factory=list)
    drc_exclusions: List[Dict[str, Any]] = field(default_factory=list)
    rules: Dict[str, Any] = field(default_factory=dict)
    track_widths: List[float] = field(default_factory=list)
    via_dimensions: List[Dict[str, Any]] = field(default_factory=list)

    # Extended fields not in standard file - all optional
    meta: Optional[Dict[str, Any]] = field(default=None)
    rule_severities: Optional[Dict[str, str]] = field(default=None)
    teardrop_options: Optional[List[Dict[str, Any]]] = field(default=None)
    teardrop_parameters: Optional[List[Dict[str, Any]]] = field(default=None)
    tuning_pattern_settings: Optional[Dict[str, Any]] = field(default=None)
    zones_allow_external_fillets: Optional[bool] = field(default=None)
    zones_use_no_outline: Optional[bool] = field(default=None)


@dataclass
class IPC2581Settings(JsonObject):
    """IPC2581 export settings."""

    dist: str = field(default="")
    distpn: str = field(default="")
    internal_id: str = field(default="")
    mfg: str = field(default="")
    mpn: str = field(default="")


@dataclass
class BoardSettings(JsonObject):
    """Board-specific settings.

    Based on standard KiCad.kicad_pro structure.
    """

    design_settings: DesignSettings = field(default_factory=lambda: DesignSettings())
    ipc2581: IPC2581Settings = field(default_factory=lambda: IPC2581Settings())
    layer_pairs: List[Dict[str, Any]] = field(default_factory=list)
    layer_presets: List[Dict[str, Any]] = field(default_factory=list)
    viewports: List[Dict[str, Any]] = field(default_factory=list)
    threeD_viewports: List[Dict[str, Any]] = field(
        default_factory=list, metadata={"json_key": "3dviewports"}
    )


@dataclass
class NetClass(JsonObject):
    """Network class definition.

    Values from standard KiCad.kicad_pro file.
    """

    name: str = field(default="Default")
    bus_width: float = field(default=12.0)
    clearance: float = field(default=0.2)
    diff_pair_gap: float = field(default=0.25)
    diff_pair_via_gap: float = field(default=0.25)
    diff_pair_width: float = field(default=0.2)
    line_style: int = field(default=0)
    microvia_diameter: float = field(default=0.3)
    microvia_drill: float = field(default=0.1)
    pcb_color: str = field(default="rgba(0, 0, 0, 0.000)")
    priority: int = field(default=2147483647)
    schematic_color: str = field(default="rgba(0, 0, 0, 0.000)")
    track_width: float = field(default=0.2)
    via_diameter: float = field(default=0.6)
    via_drill: float = field(default=0.3)
    wire_width: float = field(default=6.0)


@dataclass
class NetSettings(JsonObject):
    """Network settings configuration.

    Based on standard KiCad.kicad_pro structure.
    """

    classes: List[NetClass] = field(default_factory=lambda: [NetClass()])
    meta: Dict[str, Any] = field(default_factory=lambda: {"version": 4})
    net_colors: Optional[Dict[str, Any]] = field(default=None)
    netclass_assignments: Optional[Dict[str, Any]] = field(default=None)
    netclass_patterns: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class LibrarySettings(JsonObject):
    """Library settings configuration."""

    pinned_footprint_libs: List[str] = field(default_factory=list)
    pinned_symbol_libs: List[str] = field(default_factory=list)


@dataclass
class ERCSettings(JsonObject):
    """ERC (Electrical Rules Check) settings.

    Not present in standard KiCad.kicad_pro, so all fields are optional.
    """

    erc_exclusions: Optional[List[Dict[str, Any]]] = field(default=None)
    meta: Optional[Dict[str, Any]] = field(default=None)
    pin_map: Optional[List[List[int]]] = field(default=None)
    rule_severities: Optional[Dict[str, str]] = field(default=None)


@dataclass
class SchematicBOMSettings(JsonObject):
    """BOM (Bill of Materials) settings.

    Not present in standard KiCad.kicad_pro, so all fields are optional.
    """

    annotate_start_num: Optional[int] = field(default=None)
    bom_export_filename: Optional[str] = field(default=None)
    bom_fmt_presets: Optional[List[Dict[str, Any]]] = field(default=None)
    bom_fmt_settings: Optional[Dict[str, Any]] = field(default=None)
    bom_presets: Optional[List[Dict[str, Any]]] = field(default=None)
    bom_settings: Optional[Dict[str, Any]] = field(default=None)
    connection_grid_size: Optional[float] = field(default=None)
    drawing: Optional[Dict[str, Any]] = field(default=None)
    net_format_name: Optional[str] = field(default=None)
    ngspice: Optional[Dict[str, Any]] = field(default=None)
    page_layout_descr_file: Optional[str] = field(default=None)
    plot_directory: Optional[str] = field(default=None)
    space_save_all_events: Optional[bool] = field(default=None)
    spice_adjust_passive_values: Optional[bool] = field(default=None)
    spice_current_sheet_as_root: Optional[bool] = field(default=None)
    spice_external_command: Optional[str] = field(default=None)
    spice_model_current_sheet_as_root: Optional[bool] = field(default=None)
    spice_save_all_currents: Optional[bool] = field(default=None)
    spice_save_all_dissipations: Optional[bool] = field(default=None)
    spice_save_all_voltages: Optional[bool] = field(default=None)
    subpart_first_id: Optional[int] = field(default=None)
    subpart_id_separator: Optional[int] = field(default=None)


@dataclass
class SchematicSettings(JsonObject):
    """Schematic-specific settings.

    Based on standard KiCad.kicad_pro structure.
    """

    legacy_lib_dir: str = field(default="")
    legacy_lib_list: List[str] = field(default_factory=list)

    # Extended BOM/drawing settings - not in standard file
    meta: Optional[Dict[str, Any]] = field(default=None)


@dataclass
class PcbnewSettings(JsonObject):
    """PCB editor specific settings.

    Based on standard KiCad.kicad_pro structure.
    """

    last_paths: Dict[str, str] = field(
        default_factory=lambda: {
            "gencad": "",
            "idf": "",
            "netlist": "",
            "plot": "",
            "pos_files": "",
            "specctra_dsn": "",
            "step": "",
            "svg": "",
            "vrml": "",
        }
    )
    page_layout_descr_file: str = field(default="")


@dataclass
class CvpcbSettings(JsonObject):
    """Component-Footprint assignment tool settings."""

    equivalence_files: List[str] = field(default_factory=list)


@dataclass
class ProjectMeta(JsonObject):
    """Project metadata.

    Based on standard KiCad.kicad_pro values.
    """

    filename: str = field(default="KiCad.kicad_pro")
    version: int = field(default=3)


@dataclass
class KicadProject(JsonObject):
    """KiCad project file definition (.kicad_pro format).

    The .kicad_pro file is a JSON format file that contains project configuration
    and settings for KiCad projects.

    Based on the standard KiCad.kicad_pro structure with all standard fields
    and optional extended fields for more complex projects.

    Args:
        board: Board-specific settings
        boards: List of board files in project
        cvpcb: Component-Footprint assignment settings
        libraries: Library configuration
        meta: Project metadata
        net_settings: Network classes and settings
        pcbnew: PCB editor settings
        schematic: Schematic-specific settings
        sheets: List of schematic sheets
        text_variables: Project text variables
        erc: ERC settings (optional, not in standard file)
        _original_data: Internal storage of original input data for exact round-trip
    """

    board: BoardSettings = field(default_factory=lambda: BoardSettings())
    boards: List[str] = field(default_factory=list)
    cvpcb: CvpcbSettings = field(default_factory=lambda: CvpcbSettings())
    libraries: LibrarySettings = field(default_factory=lambda: LibrarySettings())
    meta: ProjectMeta = field(
        default_factory=lambda: ProjectMeta(filename="KiCad.kicad_pro", version=3)
    )
    net_settings: NetSettings = field(default_factory=lambda: NetSettings())
    pcbnew: PcbnewSettings = field(default_factory=lambda: PcbnewSettings())
    schematic: SchematicSettings = field(default_factory=lambda: SchematicSettings())
    sheets: List[Dict[str, Any]] = field(default_factory=list)
    text_variables: Dict[str, str] = field(default_factory=dict)

    # Extended fields not in standard file - all optional
    erc: Optional[ERCSettings] = field(default_factory=lambda: ERCSettings())

    @classmethod
    def from_file(
        cls,
        file_path: str,
        strictness: ParseStrictness = ParseStrictness.STRICT,
        encoding: str = "utf-8",
    ) -> "KicadProject":
        """Parse from JSON file - convenience method for project operations.

        Args:
            file_path: Path to .kicad_pro file
            strictness: Parse strictness level (not used for JSON)
            encoding: File encoding (default: utf-8)

        Returns:
            KicadProject instance
        """
        if not file_path.endswith(".kicad_pro"):
            raise ValueError("Unsupported file extension. Expected: .kicad_pro")

        return super().from_file(file_path, strictness, encoding)

    def save_to_file(
        self, file_path: str, encoding: str = "utf-8", preserve_original: bool = False
    ) -> None:
        """Save to .kicad_pro file format.

        Args:
            file_path: Path to write the .kicad_pro file
            encoding: File encoding (default: utf-8)
            preserve_original: Whether to preserve original structure
        """
        if not file_path.endswith(".kicad_pro"):
            raise ValueError("Unsupported file extension. Expected: .kicad_pro")

        super().save_to_file(file_path, encoding, preserve_original)
