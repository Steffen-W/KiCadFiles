"""Design rules elements for KiCad S-expressions - design rule constraint system."""

from dataclasses import dataclass, field
from typing import ClassVar, List, Optional

from .base_element import NamedInt, NamedObject, NamedString, ParseStrictness
from .enums import ConstraintType, SeverityLevel
from .sexpr_parser import sexpr_to_str


@dataclass
class DesignRuleConstraint(NamedObject):
    """Design rule constraint definition token.

    The 'constraint' token defines a constraint with optional min/opt/max values in the format::

        (constraint CONSTRAINT_TYPE [(min VALUE)] [(opt VALUE)] [(max VALUE)])
        (constraint disallow ITEM_TYPE)

    Args:
        constraint_type: Type of constraint
        min_constraint: Minimum value constraint (optional)
        opt_constraint: Optimal value constraint (optional)
        max_constraint: Maximum value constraint (optional)
        disallow_item: Item type to disallow (optional)
    """

    __token_name__: ClassVar[str] = "constraint"

    constraint_type: ConstraintType = field(
        default=ConstraintType.CLEARANCE, metadata={"description": "Type of constraint"}
    )
    min_constraint: NamedString = field(
        default_factory=lambda: NamedString("min", "0.0"),
        metadata={"description": "Minimum value constraint", "required": False},
    )
    opt_constraint: NamedString = field(
        default_factory=lambda: NamedString("opt", "0.0"),
        metadata={"description": "Optimal value constraint", "required": False},
    )
    max_constraint: NamedString = field(
        default_factory=lambda: NamedString("max", "0.0"),
        metadata={"description": "Maximum value constraint", "required": False},
    )
    disallow_item: Optional[str] = field(
        default=None,
        metadata={"description": "Item type to disallow", "required": False},
    )


@dataclass
class DesignRuleSeverity(NamedObject):
    """Design rule severity level token.

    The 'severity' token defines the severity level for rule violations in the format::

        (severity error | warning | ignore)

    Args:
        level: Severity level
    """

    __token_name__: ClassVar[str] = "severity"

    level: SeverityLevel = field(
        default=SeverityLevel.ERROR, metadata={"description": "Severity level"}
    )


@dataclass
class DesignRule(NamedObject):
    """Design rule definition token.

    The 'rule' token defines a complete design rule in the format::

        (rule NAME
            [(severity SEVERITY)]
            [(layer LAYER_NAME)]
            [(condition EXPRESSION)]
            [(priority PRIORITY_NUMBER)]
            (constraint CONSTRAINT_TYPE [CONSTRAINT_ARGUMENTS])
            [(constraint CONSTRAINT_TYPE [CONSTRAINT_ARGUMENTS])]...
        )

    Args:
        name: Rule name
        severity: Severity level (optional)
        layer: Layer specification (optional)
        condition: Conditional expression (optional)
        priority: Rule priority (optional)
        constraints: List of constraint definitions
    """

    __token_name__: ClassVar[str] = "rule"

    name: str = field(default="", metadata={"description": "Rule name"})
    severity: DesignRuleSeverity = field(
        default_factory=lambda: DesignRuleSeverity(),
        metadata={"description": "Severity level", "required": False},
    )
    layer: NamedString = field(
        default_factory=lambda: NamedString("layer", ""),
        metadata={"description": "Layer specification", "required": False},
    )
    condition: NamedString = field(
        default_factory=lambda: NamedString("condition", ""),
        metadata={"description": "Conditional expression", "required": False},
    )
    priority: NamedInt = field(
        default_factory=lambda: NamedInt("priority", 0),
        metadata={"description": "Rule priority", "required": False},
    )
    constraints: List[DesignRuleConstraint] = field(
        default_factory=list,
        metadata={"description": "List of constraint definitions"},
    )


@dataclass
class KiCadDesignRules(NamedObject):
    """KiCad design rules file definition.

    The design rules file contains version information and a list of rules in the format::

        (version VERSION)
        RULES...

    Note: This is different from other KiCad files - it doesn't have a root token like 'kicad_dru',
    instead it starts directly with version and rules.

    Args:
        version: File format version
        rules: List of design rules (optional)
    """

    __token_name__: ClassVar[str] = (
        "kicad_dru"  # Using this as placeholder, but file format is different
    )

    version: NamedInt = field(
        default_factory=lambda: NamedInt("version", 1),
        metadata={"description": "File format version"},
    )
    rules: Optional[List[DesignRule]] = field(
        default_factory=list,
        metadata={"description": "List of design rules", "required": False},
    )

    @classmethod
    def from_str(
        cls,
        sexpr_string: str,
        strictness: ParseStrictness = ParseStrictness.STRICT,
    ) -> "KiCadDesignRules":
        """Parse from S-expression string - convenience method for design rules.

        This method automatically handles .kicad_dru format preprocessing.
        """
        # Check if content looks like raw .kicad_dru format (no root token)
        stripped_content = sexpr_string.strip()
        if not stripped_content.startswith("(kicad_dru"):
            # Preprocess as raw .kicad_dru content
            processed_content = cls._preprocess_dru_content(sexpr_string)
        else:
            # Already wrapped, use as-is
            processed_content = sexpr_string

        return super().from_str(processed_content, strictness)

    @classmethod
    def from_file(
        cls,
        file_path: str,
        strictness: ParseStrictness = ParseStrictness.STRICT,
        encoding: str = "utf-8",
    ) -> "KiCadDesignRules":
        """Parse from S-expression file - convenience method for design rules operations.

        Design rules files (.kicad_dru) have a special format without root token wrapping.
        This method handles the preprocessing needed for the parser.
        """
        if not file_path.endswith(".kicad_dru"):
            raise ValueError("Unsupported file extension. Expected: .kicad_dru")

        with open(file_path, "r", encoding=encoding) as f:
            raw_content = f.read()

        return cls.from_str(raw_content, strictness)

    @classmethod
    def _preprocess_dru_content(cls, content: str) -> str:
        """Preprocess .kicad_dru file content for parsing.

        Design rules files don't have a root token wrapper, so we need to:
        1. Filter out comment lines that might have parsing issues
        2. Wrap content in a root token for the parser
        """
        lines = content.split("\n")
        filtered_lines = []

        for line in lines:
            stripped = line.strip()
            # Skip empty lines and comment lines
            if not stripped or stripped.startswith("#"):
                continue
            filtered_lines.append(line)

        # Join the filtered content and wrap in root token
        filtered_content = "\n".join(filtered_lines)
        wrapped_content = f"(kicad_dru\n{filtered_content}\n)"

        return wrapped_content

    def to_dru_str(self) -> str:
        """Convert to .kicad_dru format string (without root token wrapper).

        This method produces the native .kicad_dru file format.
        """

        lines = []

        # Add version
        version_sexpr = ["version", self.version.value]
        lines.append(sexpr_to_str(version_sexpr))

        # Add rules
        if self.rules:
            for rule in self.rules:
                rule_sexpr = rule.to_sexpr()
                lines.append(sexpr_to_str(rule_sexpr))

        return "\n".join(lines)

    def save_to_file(self, file_path: str, encoding: str = "utf-8") -> None:
        """Save to .kicad_dru file format.

        Args:
            file_path: Path to write the .kicad_dru file
            encoding: File encoding (default: utf-8)
        """
        content = self.to_dru_str()
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)
