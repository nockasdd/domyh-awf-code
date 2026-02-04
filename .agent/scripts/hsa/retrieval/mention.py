# HSA v5.0 - @-mention Context Parser
# =============================================================================
"""
Parser for @-mention syntax in queries.

Syntax:
- @file:path/to/file.py - Reference specific file
- @folder:src/utils - Reference folder
- @function:authenticate - Reference function
- @class:UserService - Reference class
- @module:auth - Reference module
- @line:path/to/file.py#L10-L20 - Reference line range

Features:
- Parse mentions from query text
- Expand mentions to entity IDs
- Priority boost for mentioned items
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger("hsa.mention")


class MentionType(Enum):
    """Types of @-mentions."""
    FILE = "file"
    FOLDER = "folder"
    FUNCTION = "function"
    CLASS = "class"
    METHOD = "method"
    MODULE = "module"
    LINE = "line"
    SYMBOL = "symbol"  # Generic symbol
    UNKNOWN = "unknown"


@dataclass
class Mention:
    """Parsed @-mention."""
    type: MentionType
    value: str
    raw: str
    start: int
    end: int
    line_range: Optional[Tuple[int, int]] = None  # For @line mentions
    
    @property
    def file_path(self) -> Optional[str]:
        """Get file path if applicable."""
        if self.type in (MentionType.FILE, MentionType.LINE):
            # Remove line range if present
            return self.value.split("#")[0] if "#" in self.value else self.value
        return None
    
    def matches_entity(self, entity_name: str, entity_type: str) -> bool:
        """Check if mention matches an entity."""
        if self.type == MentionType.FILE:
            return entity_name.endswith(self.value) or self.value.endswith(entity_name)
        elif self.type == MentionType.FUNCTION:
            return entity_name == self.value and entity_type in ("function", "method")
        elif self.type == MentionType.CLASS:
            return entity_name == self.value and entity_type == "class"
        elif self.type == MentionType.SYMBOL:
            return self.value in entity_name
        return False


@dataclass 
class ParsedQuery:
    """Query with parsed mentions."""
    original: str
    cleaned: str  # Query with mentions removed
    mentions: List[Mention]
    
    @property
    def has_mentions(self) -> bool:
        return len(self.mentions) > 0
    
    def get_mentioned_files(self) -> List[str]:
        """Get all mentioned file paths."""
        return [
            m.file_path for m in self.mentions 
            if m.file_path is not None
        ]
    
    def get_mentioned_functions(self) -> List[str]:
        """Get all mentioned function names."""
        return [
            m.value for m in self.mentions 
            if m.type == MentionType.FUNCTION
        ]
    
    def get_mentioned_classes(self) -> List[str]:
        """Get all mentioned class names."""
        return [
            m.value for m in self.mentions 
            if m.type == MentionType.CLASS
        ]


class MentionParser:
    """
    Parser for @-mention syntax.
    
    Usage:
        parser = MentionParser()
        
        parsed = parser.parse("Show me @function:authenticate in @file:auth.py")
        
        print(parsed.mentions)
        # [Mention(type=FUNCTION, value='authenticate'), 
        #  Mention(type=FILE, value='auth.py')]
        
        print(parsed.cleaned)
        # "Show me   in  "
    """
    
    # Patterns for different mention types
    PATTERNS = {
        # Explicit type mentions
        MentionType.FILE: r'@file:([^\s]+)',
        MentionType.FOLDER: r'@folder:([^\s]+)',
        MentionType.FUNCTION: r'@function:([^\s]+)',
        MentionType.CLASS: r'@class:([^\s]+)',
        MentionType.METHOD: r'@method:([^\s]+)',
        MentionType.MODULE: r'@module:([^\s]+)',
        MentionType.LINE: r'@line:([^\s]+#L\d+(?:-L?\d+)?)',
        
        # Generic symbol (just @name)
        MentionType.SYMBOL: r'@([a-zA-Z_][a-zA-Z0-9_\.]*)',
    }
    
    # File extensions to auto-detect @file
    FILE_EXTENSIONS = {
        '.py', '.ts', '.js', '.tsx', '.jsx', '.go', '.rs', '.java', '.kt',
        '.c', '.cpp', '.h', '.hpp', '.cs', '.rb', '.php', '.swift', '.vue',
        '.svelte', '.md', '.json', '.yaml', '.yml', '.toml', '.sql'
    }
    
    def __init__(self, project_root: Optional[str] = None):
        self.project_root = Path(project_root) if project_root else None
    
    def parse(self, query: str) -> ParsedQuery:
        """Parse query for @-mentions."""
        mentions: List[Mention] = []
        
        # Parse explicit type mentions first (higher priority)
        for mention_type, pattern in self.PATTERNS.items():
            if mention_type == MentionType.SYMBOL:
                continue  # Parse symbols last
            
            for match in re.finditer(pattern, query):
                mention = self._create_mention(mention_type, match)
                mentions.append(mention)
        
        # Parse generic symbols (not already matched)
        matched_positions = {(m.start, m.end) for m in mentions}
        symbol_pattern = self.PATTERNS[MentionType.SYMBOL]
        
        for match in re.finditer(symbol_pattern, query):
            # Skip if overlaps with existing mention
            if any(
                match.start() >= start and match.start() < end
                for start, end in matched_positions
            ):
                continue
            
            value = match.group(1)
            
            # Infer type from value
            inferred_type = self._infer_type(value)
            
            mention = Mention(
                type=inferred_type,
                value=value,
                raw=match.group(0),
                start=match.start(),
                end=match.end()
            )
            mentions.append(mention)
        
        # Sort by position
        mentions.sort(key=lambda m: m.start)
        
        # Create cleaned query
        cleaned = self._remove_mentions(query, mentions)
        
        return ParsedQuery(
            original=query,
            cleaned=cleaned.strip(),
            mentions=mentions
        )
    
    def _create_mention(self, mention_type: MentionType, match: re.Match) -> Mention:
        """Create mention from regex match."""
        value = match.group(1)
        line_range = None
        
        # Parse line range for @line mentions
        if mention_type == MentionType.LINE and "#L" in value:
            line_range = self._parse_line_range(value)
        
        return Mention(
            type=mention_type,
            value=value,
            raw=match.group(0),
            start=match.start(),
            end=match.end(),
            line_range=line_range
        )
    
    def _parse_line_range(self, value: str) -> Optional[Tuple[int, int]]:
        """Parse line range from value like 'file.py#L10-L20'."""
        if "#L" not in value:
            return None
        
        try:
            _, line_part = value.split("#L")
            
            if "-" in line_part:
                # Range: L10-L20 or L10-20
                parts = line_part.replace("L", "").split("-")
                start = int(parts[0])
                end = int(parts[1])
                return (start, end)
            else:
                # Single line
                line = int(line_part)
                return (line, line)
        except:
            return None
    
    def _infer_type(self, value: str) -> MentionType:
        """Infer mention type from value."""
        # Check if looks like a file path
        if "/" in value or "\\" in value:
            return MentionType.FILE
        
        # Check file extension
        for ext in self.FILE_EXTENSIONS:
            if value.endswith(ext):
                return MentionType.FILE
        
        # Check if looks like class (PascalCase)
        if value[0].isupper() and not value.isupper():
            return MentionType.CLASS
        
        # Check if looks like function (snake_case or camelCase)
        if "_" in value or (value[0].islower() and any(c.isupper() for c in value)):
            return MentionType.FUNCTION
        
        return MentionType.SYMBOL
    
    def _remove_mentions(self, query: str, mentions: List[Mention]) -> str:
        """Remove mentions from query."""
        if not mentions:
            return query
        
        result = []
        last_end = 0
        
        for mention in sorted(mentions, key=lambda m: m.start):
            result.append(query[last_end:mention.start])
            last_end = mention.end
        
        result.append(query[last_end:])
        
        # Clean up extra whitespace
        return re.sub(r'\s+', ' ', ''.join(result))
    
    def expand_mentions(
        self, 
        mentions: List[Mention],
        entity_index: Dict[str, Any]
    ) -> List[str]:
        """
        Expand mentions to entity IDs.
        
        Args:
            mentions: List of parsed mentions
            entity_index: Dict mapping entity names to info
            
        Returns:
            List of entity IDs that match mentions
        """
        matched_ids = []
        
        for mention in mentions:
            for entity_id, entity_info in entity_index.items():
                entity_name = entity_info.get("name", entity_id.split(":")[-1])
                entity_type = entity_info.get("type", "unknown")
                
                if mention.matches_entity(entity_name, entity_type):
                    if entity_id not in matched_ids:
                        matched_ids.append(entity_id)
        
        return matched_ids


class ContextBooster:
    """
    Boost scores for mentioned entities.
    
    Usage:
        booster = ContextBooster()
        
        parsed = parser.parse("@file:auth.py login")
        boosted = booster.boost(results, parsed.mentions)
    """
    
    def __init__(
        self, 
        mention_boost: float = 2.0,
        exact_match_boost: float = 3.0
    ):
        self.mention_boost = mention_boost
        self.exact_match_boost = exact_match_boost
    
    def boost(
        self,
        results: List[Dict[str, Any]],
        mentions: List[Mention]
    ) -> List[Dict[str, Any]]:
        """
        Boost scores for results matching mentions.
        
        Args:
            results: List of search results with 'doc_id' and 'score'
            mentions: List of parsed mentions
            
        Returns:
            Results with boosted scores
        """
        if not mentions:
            return results
        
        boosted = []
        
        for result in results:
            new_result = dict(result)
            doc_id = result.get("doc_id", "")
            score = result.get("score", 0.0)
            
            boost = 1.0
            
            for mention in mentions:
                if self._matches(doc_id, mention):
                    if mention.type == MentionType.FILE:
                        boost = max(boost, self.exact_match_boost)
                    else:
                        boost = max(boost, self.mention_boost)
            
            new_result["score"] = score * boost
            new_result["boosted"] = boost > 1.0
            boosted.append(new_result)
        
        # Re-sort by score
        boosted.sort(key=lambda x: x.get("score", 0), reverse=True)
        
        return boosted
    
    def _matches(self, doc_id: str, mention: Mention) -> bool:
        """Check if doc_id matches mention."""
        if mention.type == MentionType.FILE:
            return mention.value in doc_id or doc_id.endswith(mention.value)
        elif mention.type == MentionType.FOLDER:
            return mention.value in doc_id
        elif mention.type in (MentionType.FUNCTION, MentionType.CLASS, MentionType.METHOD):
            return f":{mention.value}" in doc_id
        elif mention.type == MentionType.SYMBOL:
            return mention.value in doc_id
        
        return False


# Convenience functions
_parser: Optional[MentionParser] = None


def get_parser(project_root: Optional[str] = None) -> MentionParser:
    """Get global mention parser."""
    global _parser
    if _parser is None:
        _parser = MentionParser(project_root)
    return _parser


def parse_query(query: str) -> ParsedQuery:
    """Parse query for mentions."""
    return get_parser().parse(query)
