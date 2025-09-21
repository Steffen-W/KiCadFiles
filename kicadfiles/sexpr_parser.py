"""S-Expression Parser for KiCad files

This module provides a simplified approach to parsing S-expressions.
Only contains the functions actually used by the kicadfiles package.
"""

from __future__ import annotations

from typing import Any, List, cast

from .sexpdata import Symbol, dumps, loads

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


def sexpr_to_str(sexpr: SExpr, pretty_print: bool = True) -> str:
    """Convert S-expression to string representation.

    Args:
        sexpr: S-expression to serialize
        pretty_print: Whether to format output for readability

    Returns:
        String representation of the S-expression

    Raises:
        ValueError: If sexpr cannot be serialized
    """
    try:
        return dumps(sexpr, pretty_print=pretty_print)
    except Exception as e:
        raise ValueError(f"Failed to serialize S-expression: {e}") from e


class SExprParser:
    """Minimal S-Expression parser with only the methods actually used."""

    def __init__(self, sexpr: SExpr, track_usage: bool = False) -> None:
        """Initialize parser with an S-expression.

        Args:
            sexpr: Parsed S-expression as nested lists/atoms
            track_usage: Whether to track which parameters are accessed
        """
        self.sexpr = sexpr
        self.track_usage = track_usage
        self.used_indices: set[int] = set() if track_usage else set()

    @classmethod
    def from_string(cls, sexpr_string: str) -> "SExprParser":
        """Create parser from S-expression string.

        Args:
            sexpr_string: String containing S-expression data

        Returns:
            New parser instance
        """
        return cls(str_to_sexpr(sexpr_string))

    def get_list_of_tokens(self, token_name: str) -> List[SExpr]:
        """Get list of raw S-expressions for all tokens with the given name.

        Args:
            token_name: Name of the tokens to find

        Returns:
            List of S-expressions (empty list if none found)
        """
        results = []
        for item in self.sexpr:
            if (
                isinstance(item, list)
                and len(item) > 0
                and (item[0] == Symbol(token_name) or str(item[0]) == token_name)
            ):
                results.append(item)
        return results

    def mark_used(self, index: int) -> None:
        """Mark a parameter index as used.

        Args:
            index: Index in sexpr that was accessed
        """
        if self.track_usage:
            self.used_indices.add(index)

    def get_unused_parameters(self) -> List[Any]:
        """Get list of unused parameters.

        Returns:
            List of unused parameters (excluding token name at index 0)
        """
        if not self.track_usage:
            return []

        unused = []
        # Skip index 0 (token name) and check remaining parameters
        for i in range(1, len(self.sexpr)):
            if i not in self.used_indices:
                unused.append(self.sexpr[i])
        return unused

    def check_complete_usage(self, class_name: str = "") -> None:
        """Check if all parameters were used and raise error if not.

        Args:
            class_name: Name of the class for error messages

        Raises:
            ValueError: If there are unused parameters
        """
        if not self.track_usage:
            return

        unused = self.get_unused_parameters()
        if unused:
            class_info = f" in {class_name}" if class_name else ""
            raise ValueError(f"Unused parameters{class_info}: {unused}")


def parse_sexpr(sexpr: SExpr) -> SExprParser:
    """Create parser from S-expression."""
    return SExprParser(sexpr)
