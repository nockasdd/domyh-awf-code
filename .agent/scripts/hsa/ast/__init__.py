# HSA v5.0 AST Module
# =============================================================================
"""
AST parsing for HSA v5.0.

Uses tree-sitter for fast, incremental parsing.
"""

from .parser import (
    TreeSitterParser,
    ParseResult,
    CodeEntity,
    NodeType,
    LANGUAGE_EXTENSIONS,
    get_parser,
    parse_file,
)

__all__ = [
    "TreeSitterParser",
    "ParseResult",
    "CodeEntity",
    "NodeType",
    "LANGUAGE_EXTENSIONS",
    "get_parser",
    "parse_file",
]
