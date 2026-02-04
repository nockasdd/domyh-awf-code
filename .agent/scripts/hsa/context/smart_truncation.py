# =============================================================================
# smart_truncation.py — Intelligent Content Truncation
# =============================================================================
# HSA v5.0 - Phase 4: Token Budget & GC
# Implements smart content reduction when items exceed token limits
# =============================================================================

"""
Smart Truncation Module

Implements intelligent content truncation strategies:
- AST-aware truncation for code (preserve structure)
- Semantic boundary truncation for text
- Progressive detail reduction (remove examples first)

From HSA_V4.yaml spec:
- preserve_signatures: true
- preserve_docstrings: true
- remove_examples_first: true
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Callable, List, Optional, Tuple


class TruncationStrategy(Enum):
    """Available truncation strategies."""
    SIMPLE = auto()       # Basic character/line truncation
    SEMANTIC = auto()     # Preserve sentence boundaries
    CODE_AWARE = auto()   # Preserve code structure
    PROGRESSIVE = auto()  # Gradually reduce detail


@dataclass
class TruncationResult:
    """Result of truncation operation."""
    original_length: int
    truncated_length: int
    content: str
    strategy_used: TruncationStrategy
    sections_removed: List[str] = None
    
    @property
    def reduction_pct(self) -> float:
        if self.original_length == 0:
            return 0.0
        return 1 - (self.truncated_length / self.original_length)
    
    def __post_init__(self):
        if self.sections_removed is None:
            self.sections_removed = []


class Truncator(ABC):
    """Base class for truncation strategies."""
    
    @abstractmethod
    def truncate(self, content: str, max_length: int) -> TruncationResult:
        """Truncate content to max_length."""
        pass


class SimpleTruncator(Truncator):
    """Simple character-based truncation with ellipsis."""
    
    def __init__(self, preserve_end: bool = False):
        self.preserve_end = preserve_end
    
    def truncate(self, content: str, max_length: int) -> TruncationResult:
        original = len(content)
        
        if original <= max_length:
            return TruncationResult(
                original_length=original,
                truncated_length=original,
                content=content,
                strategy_used=TruncationStrategy.SIMPLE
            )
        
        ellipsis = "..."
        available = max_length - len(ellipsis)
        
        if self.preserve_end:
            # Keep start and end
            half = available // 2
            truncated = content[:half] + ellipsis + content[-half:]
        else:
            # Keep start only
            truncated = content[:available] + ellipsis
        
        return TruncationResult(
            original_length=original,
            truncated_length=len(truncated),
            content=truncated,
            strategy_used=TruncationStrategy.SIMPLE
        )


class SemanticTruncator(Truncator):
    """Truncate at sentence/paragraph boundaries."""
    
    # Sentence end patterns
    SENTENCE_END = re.compile(r'[.!?]\s+')
    PARAGRAPH_END = re.compile(r'\n\s*\n')
    
    def truncate(self, content: str, max_length: int) -> TruncationResult:
        original = len(content)
        
        if original <= max_length:
            return TruncationResult(
                original_length=original,
                truncated_length=original,
                content=content,
                strategy_used=TruncationStrategy.SEMANTIC
            )
        
        # Find the last complete sentence within limit
        truncated = content[:max_length]
        
        # Try to find paragraph boundary
        para_match = None
        for match in self.PARAGRAPH_END.finditer(truncated):
            para_match = match
        
        if para_match and para_match.end() > max_length * 0.5:
            truncated = content[:para_match.end()].rstrip() + "\n\n..."
        else:
            # Try sentence boundary
            sent_match = None
            for match in self.SENTENCE_END.finditer(truncated):
                sent_match = match
            
            if sent_match and sent_match.end() > max_length * 0.5:
                truncated = content[:sent_match.end()].rstrip() + "..."
            else:
                # Fall back to simple
                truncated = content[:max_length - 3] + "..."
        
        return TruncationResult(
            original_length=original,
            truncated_length=len(truncated),
            content=truncated,
            strategy_used=TruncationStrategy.SEMANTIC
        )


class CodeAwareTruncator(Truncator):
    """
    Truncate code while preserving structure.
    
    Preservation priority:
    1. Function/class signatures
    2. Docstrings
    3. Key logic (first lines)
    4. Examples and tests (removed first)
    """
    
    # Patterns for code structure
    FUNCTION_DEF = re.compile(r'^(\s*)(def|async def|function|fn|func)\s+\w+', re.MULTILINE)
    CLASS_DEF = re.compile(r'^(\s*)(class|struct|type|interface)\s+\w+', re.MULTILINE)
    DOCSTRING = re.compile(r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\')', re.MULTILINE)
    EXAMPLE_SECTION = re.compile(r'(^#+\s*Example|^#+\s*Usage|>>> )', re.MULTILINE | re.IGNORECASE)
    
    def __init__(
        self,
        preserve_signatures: bool = True,
        preserve_docstrings: bool = True,
        remove_examples_first: bool = True
    ):
        self.preserve_signatures = preserve_signatures
        self.preserve_docstrings = preserve_docstrings
        self.remove_examples_first = remove_examples_first
    
    def truncate(self, content: str, max_length: int) -> TruncationResult:
        original = len(content)
        removed_sections = []
        
        if original <= max_length:
            return TruncationResult(
                original_length=original,
                truncated_length=original,
                content=content,
                strategy_used=TruncationStrategy.CODE_AWARE
            )
        
        working = content
        
        # Step 1: Remove examples if enabled
        if self.remove_examples_first and len(working) > max_length:
            working, removed = self._remove_examples(working)
            if removed:
                removed_sections.append("examples")
        
        # Step 2: If still too long, truncate function bodies
        if len(working) > max_length:
            working = self._truncate_function_bodies(working, max_length)
            removed_sections.append("function_bodies")
        
        # Step 3: Final truncation if needed
        if len(working) > max_length:
            working = working[:max_length - 3] + "..."
        
        return TruncationResult(
            original_length=original,
            truncated_length=len(working),
            content=working,
            strategy_used=TruncationStrategy.CODE_AWARE,
            sections_removed=removed_sections
        )
    
    def _remove_examples(self, content: str) -> Tuple[str, bool]:
        """Remove example sections from content."""
        lines = content.split('\n')
        result_lines = []
        in_example = False
        removed = False
        
        for line in lines:
            if self.EXAMPLE_SECTION.search(line):
                in_example = True
                removed = True
                result_lines.append("# [Examples truncated]")
                continue
            
            if in_example:
                # Check if we've left the example section
                if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                    if line.startswith('#') or line.startswith('def ') or line.startswith('class '):
                        in_example = False
                        result_lines.append(line)
                continue
            
            result_lines.append(line)
        
        return '\n'.join(result_lines), removed
    
    def _truncate_function_bodies(self, content: str, max_length: int) -> str:
        """Truncate function bodies while preserving signatures."""
        lines = content.split('\n')
        result_lines = []
        current_indent = 0
        in_body = False
        body_lines_kept = 0
        max_body_lines = 3  # Keep first 3 lines of each function
        
        for line in lines:
            # Check for function/class definition
            func_match = self.FUNCTION_DEF.match(line)
            class_match = self.CLASS_DEF.match(line)
            
            if func_match or class_match:
                in_body = True
                body_lines_kept = 0
                current_indent = len(line) - len(line.lstrip())
                result_lines.append(line)
                continue
            
            if in_body:
                line_indent = len(line) - len(line.lstrip()) if line.strip() else 0
                
                # Check if we've exited the function
                if line.strip() and line_indent <= current_indent:
                    in_body = False
                    result_lines.append(line)
                    continue
                
                # Keep docstrings
                if self.preserve_docstrings and ('"""' in line or "'''" in line):
                    result_lines.append(line)
                    continue
                
                # Keep first few body lines
                if body_lines_kept < max_body_lines:
                    result_lines.append(line)
                    body_lines_kept += 1
                elif body_lines_kept == max_body_lines:
                    result_lines.append(f"{' ' * (current_indent + 4)}# ... [body truncated]")
                    body_lines_kept += 1
            else:
                result_lines.append(line)
            
            # Early exit if we're at target length
            if len('\n'.join(result_lines)) > max_length:
                break
        
        return '\n'.join(result_lines)


class ProgressiveTruncator(Truncator):
    """
    Progressively reduce detail level.
    
    Levels:
    1. Full content
    2. Remove examples
    3. Remove comments
    4. Signatures only
    5. Names only
    """
    
    COMMENT_LINE = re.compile(r'^\s*(#|//|/\*|\*)', re.MULTILINE)
    
    def __init__(self, target_levels: List[int] = None):
        # Percentage targets for each level
        self.target_levels = target_levels or [1.0, 0.8, 0.6, 0.4, 0.2]
    
    def truncate(self, content: str, max_length: int) -> TruncationResult:
        original = len(content)
        
        if original <= max_length:
            return TruncationResult(
                original_length=original,
                truncated_length=original,
                content=content,
                strategy_used=TruncationStrategy.PROGRESSIVE
            )
        
        removed_sections = []
        working = content
        
        # Level 2: Remove examples
        if len(working) > max_length:
            code_truncator = CodeAwareTruncator()
            working, _ = code_truncator._remove_examples(working)
            removed_sections.append("examples")
        
        # Level 3: Remove comments
        if len(working) > max_length:
            working = self._remove_comments(working)
            removed_sections.append("comments")
        
        # Level 4: Signatures only
        if len(working) > max_length:
            working = self._extract_signatures(working)
            removed_sections.append("bodies")
        
        # Level 5: Final truncation
        if len(working) > max_length:
            working = working[:max_length - 3] + "..."
        
        return TruncationResult(
            original_length=original,
            truncated_length=len(working),
            content=working,
            strategy_used=TruncationStrategy.PROGRESSIVE,
            sections_removed=removed_sections
        )
    
    def _remove_comments(self, content: str) -> str:
        """Remove comment lines."""
        lines = content.split('\n')
        return '\n'.join(
            line for line in lines
            if not self.COMMENT_LINE.match(line)
        )
    
    def _extract_signatures(self, content: str) -> str:
        """Extract only function/class signatures."""
        lines = content.split('\n')
        result = []
        
        func_pattern = re.compile(r'^\s*(def|async def|function|fn|func|class|struct|type|interface)\s+')
        
        for line in lines:
            if func_pattern.match(line):
                result.append(line)
        
        return '\n'.join(result)


class SmartTruncator:
    """
    Unified smart truncator with auto-detection.
    
    Automatically selects the best strategy based on content type.
    
    Usage:
        truncator = SmartTruncator()
        
        result = truncator.truncate(
            content=code_content,
            max_length=5000,
            content_type="python"
        )
        
        print(f"Reduced by {result.reduction_pct:.0%}")
    """
    
    # Content type to truncator mapping
    CODE_TYPES = {"python", "javascript", "typescript", "go", "rust", "java", "csharp"}
    
    def __init__(self):
        self.simple = SimpleTruncator()
        self.semantic = SemanticTruncator()
        self.code_aware = CodeAwareTruncator()
        self.progressive = ProgressiveTruncator()
    
    def truncate(
        self,
        content: str,
        max_length: int,
        content_type: Optional[str] = None,
        strategy: Optional[TruncationStrategy] = None
    ) -> TruncationResult:
        """
        Truncate content using the best strategy.
        
        Args:
            content: Content to truncate
            max_length: Maximum allowed length
            content_type: Type hint for strategy selection
            strategy: Force specific strategy
            
        Returns:
            TruncationResult
        """
        # Select strategy
        if strategy:
            truncator = self._get_truncator(strategy)
        elif content_type and content_type.lower() in self.CODE_TYPES:
            truncator = self.code_aware
        elif self._looks_like_code(content):
            truncator = self.code_aware
        elif self._looks_like_prose(content):
            truncator = self.semantic
        else:
            truncator = self.simple
        
        return truncator.truncate(content, max_length)
    
    def _get_truncator(self, strategy: TruncationStrategy) -> Truncator:
        """Get truncator for strategy."""
        return {
            TruncationStrategy.SIMPLE: self.simple,
            TruncationStrategy.SEMANTIC: self.semantic,
            TruncationStrategy.CODE_AWARE: self.code_aware,
            TruncationStrategy.PROGRESSIVE: self.progressive,
        }.get(strategy, self.simple)
    
    def _looks_like_code(self, content: str) -> bool:
        """Heuristic check if content looks like code."""
        indicators = [
            'def ', 'class ', 'function ', 'import ', 'from ',
            'const ', 'let ', 'var ', 'fn ', 'func ',
            '{ }', '();', '=>', '->', '::'
        ]
        return any(ind in content for ind in indicators)
    
    def _looks_like_prose(self, content: str) -> bool:
        """Heuristic check if content looks like prose."""
        # Has sentence-like structure
        return '. ' in content and len(content) > 100


# =============================================================================
# Convenience Functions
# =============================================================================

_default_truncator: Optional[SmartTruncator] = None


def truncate_smart(
    content: str,
    max_length: int,
    content_type: Optional[str] = None
) -> str:
    """Quick smart truncation."""
    global _default_truncator
    if _default_truncator is None:
        _default_truncator = SmartTruncator()
    
    result = _default_truncator.truncate(content, max_length, content_type)
    return result.content


# =============================================================================
# _DOMYH Awesome Code v6.1.2 • HSA v5.0 • Smart Truncation_
# =============================================================================
