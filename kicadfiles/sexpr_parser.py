"""S-Expression Parser for KiCad files

This module provides a simplified approach to parsing S-expressions.
Only contains the functions actually used by the kicadfiles package.
"""

from __future__ import annotations

from typing import Any, List, cast

from .sexpdata import dumps, loads

# Type definitions
SExprValue = Any  # Can be Symbol, str, int, float, or nested list
SExpr = List[SExprValue]


def str_to_sexpr(content: str) -> SExpr:
    """Convert string content to S-expression.

    Args:
        content: String content containing S-expression data

    Returns:
        Parsed S-expression as nested lists/atoms

    Raises:
        ValueError: If content cannot be parsed as valid S-expression
    """
    try:
        return cast(SExpr, loads(content))
    except Exception as e:
        raise ValueError(f"Failed to parse S-expression: {e}") from e


def sexpr_to_str(sexpr: SExpr) -> str:
    """Convert S-expression to string representation.

    Args:
        sexpr: S-expression to serialize

    Returns:
        String representation of the S-expression

    Raises:
        ValueError: If sexpr cannot be serialized
    """
    try:
        return dumps(sexpr)
    except Exception as e:
        raise ValueError(f"Failed to serialize S-expression: {e}") from e


class SExprParser:
    """Minimal S-Expression parser with usage tracking always enabled."""

    def __init__(self, sexpr: SExpr) -> None:
        """Initialize parser with an S-expression.

        Args:
            sexpr: Parsed S-expression as nested lists/atoms
        """
        self.sexpr = sexpr
        self.used_indices: set[int] = set()

    @classmethod
    def from_string(cls, sexpr_string: str) -> "SExprParser":
        """Create parser from S-expression string.

        Args:
            sexpr_string: String containing S-expression data

        Returns:
            New parser instance
        """
        return cls(str_to_sexpr(sexpr_string))

    def mark_used(self, index: int) -> None:
        """Mark a parameter index as used.

        Args:
            index: Index in sexpr that was accessed
        """
        self.used_indices.add(index)

    def get_unused_parameters(self) -> List[Any]:
        """Get list of unused parameters.

        Returns:
            List of unused parameters (excluding token name at index 0)
        """
        unused = []
        # Skip index 0 (token name) and check remaining parameters
        for i in range(1, len(self.sexpr)):
            if i not in self.used_indices:
                unused.append(self.sexpr[i])
        return unused
