# HSA v5.0 - Tree-sitter AST Parser
# =============================================================================
"""
Fast AST parsing using tree-sitter.

Tier 0: Always available for supported languages.

Features:
- Incremental parsing (<1ms for small changes)
- Extract: functions, classes, imports, exports
- Support: Python, TypeScript, JavaScript, Go, Rust, C/C++
- Entity extraction for HiRAG integration
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger("hsa.ast")


class NodeType(Enum):
    """Types of code entities."""
    FILE = "file"
    CLASS = "class"
    FUNCTION = "function"
    METHOD = "method"
    VARIABLE = "variable"
    IMPORT = "import"
    EXPORT = "export"
    CONSTANT = "constant"
    INTERFACE = "interface"
    TYPE = "type"
    DECORATOR = "decorator"


@dataclass
class CodeEntity:
    """Code entity extracted from AST."""
    name: str
    type: NodeType
    file_path: str
    start_line: int
    end_line: int
    start_col: int = 0
    end_col: int = 0
    
    # Optional metadata
    docstring: Optional[str] = None
    parent: Optional[str] = None
    decorators: List[str] = field(default_factory=list)
    parameters: List[str] = field(default_factory=list)
    return_type: Optional[str] = None
    
    @property
    def qualified_name(self) -> str:
        """Get fully qualified name."""
        if self.parent:
            return f"{self.parent}.{self.name}"
        return self.name
    
    @property
    def line_count(self) -> int:
        """Number of lines."""
        return self.end_line - self.start_line + 1
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type.value,
            "file_path": self.file_path,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "parent": self.parent,
            "qualified_name": self.qualified_name,
        }


@dataclass
class ParseResult:
    """Result of parsing a file."""
    file_path: str
    language: str
    entities: List[CodeEntity]
    imports: List[str]
    exports: List[str]
    parse_time_ms: float
    
    @property
    def functions(self) -> List[CodeEntity]:
        return [e for e in self.entities if e.type in (NodeType.FUNCTION, NodeType.METHOD)]
    
    @property
    def classes(self) -> List[CodeEntity]:
        return [e for e in self.entities if e.type == NodeType.CLASS]


# Language extensions mapping
LANGUAGE_EXTENSIONS: Dict[str, str] = {
    ".py": "python",
    ".pyi": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".go": "go",
    ".rs": "rust",
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".hpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
}


class TreeSitterParser:
    """
    Tree-sitter based AST parser.
    
    Usage:
        parser = TreeSitterParser()
        result = parser.parse_file("src/main.py")
        
        for entity in result.entities:
            print(f"{entity.type.value}: {entity.name}")
    """
    
    def __init__(self):
        """Initialize parser with supported languages."""
        self._parsers: Dict[str, Any] = {}
        self._languages: Dict[str, Any] = {}
        
        # Try to load tree-sitter
        try:
            import tree_sitter
            self._tree_sitter = tree_sitter
            logger.debug("tree-sitter loaded successfully")
        except ImportError:
            logger.warning(
                "tree-sitter not installed. "
                "Install with: pip install tree-sitter"
            )
            self._tree_sitter = None
    
    def _get_parser(self, language: str) -> Optional[Any]:
        """Get or create parser for language."""
        if self._tree_sitter is None:
            return None
        
        if language in self._parsers:
            return self._parsers[language]
        
        try:
            # Try loading language-specific tree-sitter package
            language_module = __import__(f"tree_sitter_{language}")
            parser = self._tree_sitter.Parser(language_module.language())
            
            self._parsers[language] = parser
            logger.debug(f"Loaded tree-sitter parser for {language}")
            return parser
            
        except ImportError:
            logger.debug(f"tree-sitter-{language} not installed")
            return None
        except Exception as e:
            logger.warning(f"Failed to load tree-sitter for {language}: {e}")
            return None
    
    def detect_language(self, file_path: str) -> Optional[str]:
        """Detect language from file extension."""
        ext = Path(file_path).suffix.lower()
        return LANGUAGE_EXTENSIONS.get(ext)
    
    def parse_file(self, file_path: str, content: Optional[str] = None) -> ParseResult:
        """
        Parse a source file.
        
        Args:
            file_path: Path to file
            content: Optional file content (reads from disk if not provided)
            
        Returns:
            ParseResult with extracted entities
        """
        import time
        start_time = time.time()
        
        # Detect language
        language = self.detect_language(file_path)
        if language is None:
            return ParseResult(
                file_path=file_path,
                language="unknown",
                entities=[],
                imports=[],
                exports=[],
                parse_time_ms=0
            )
        
        # Read content if not provided
        if content is None:
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
            except Exception as e:
                logger.error(f"Failed to read file {file_path}: {e}")
                return ParseResult(
                    file_path=file_path,
                    language=language,
                    entities=[],
                    imports=[],
                    exports=[],
                    parse_time_ms=0
                )
        
        # Get parser
        parser = self._get_parser(language)
        
        if parser is None:
            # Fallback to regex-based parsing
            result = self._parse_with_regex(file_path, content, language)
        else:
            # Use tree-sitter
            result = self._parse_with_tree_sitter(file_path, content, language, parser)
        
        parse_time_ms = (time.time() - start_time) * 1000
        result.parse_time_ms = parse_time_ms
        
        logger.debug(f"Parsed {file_path}: {len(result.entities)} entities in {parse_time_ms:.1f}ms")
        
        return result
    
    def _parse_with_tree_sitter(
        self, 
        file_path: str, 
        content: str, 
        language: str,
        parser: Any
    ) -> ParseResult:
        """Parse using tree-sitter."""
        entities = []
        imports = []
        exports = []
        
        try:
            tree = parser.parse(content.encode("utf-8"))
            root = tree.root_node
            
            # Extract entities based on language
            if language == "python":
                self._extract_python_entities(root, file_path, content, entities, imports)
            elif language in ("javascript", "typescript"):
                self._extract_js_entities(root, file_path, content, entities, imports, exports)
            elif language == "go":
                self._extract_go_entities(root, file_path, content, entities, imports)
            else:
                # Generic extraction
                self._extract_generic_entities(root, file_path, content, entities)
                
        except Exception as e:
            logger.warning(f"Tree-sitter parsing failed for {file_path}: {e}")
        
        return ParseResult(
            file_path=file_path,
            language=language,
            entities=entities,
            imports=imports,
            exports=exports,
            parse_time_ms=0
        )
    
    def _extract_python_entities(
        self,
        root: Any,
        file_path: str,
        content: str,
        entities: List[CodeEntity],
        imports: List[str]
    ) -> None:
        """Extract entities from Python AST."""
        lines = content.split("\n")
        
        def visit(node, parent_name: Optional[str] = None):
            node_type = node.type
            
            if node_type == "function_definition":
                name_node = node.child_by_field_name("name")
                if name_node:
                    entity_type = NodeType.METHOD if parent_name else NodeType.FUNCTION
                    entity = CodeEntity(
                        name=name_node.text.decode("utf-8"),
                        type=entity_type,
                        file_path=file_path,
                        start_line=node.start_point[0] + 1,
                        end_line=node.end_point[0] + 1,
                        parent=parent_name
                    )
                    entities.append(entity)
            
            elif node_type == "class_definition":
                name_node = node.child_by_field_name("name")
                if name_node:
                    class_name = name_node.text.decode("utf-8")
                    entity = CodeEntity(
                        name=class_name,
                        type=NodeType.CLASS,
                        file_path=file_path,
                        start_line=node.start_point[0] + 1,
                        end_line=node.end_point[0] + 1
                    )
                    entities.append(entity)
                    
                    # Visit children with class as parent
                    for child in node.children:
                        visit(child, class_name)
                    return  # Don't recurse again
            
            elif node_type in ("import_statement", "import_from_statement"):
                imports.append(node.text.decode("utf-8"))
            
            # Recurse
            for child in node.children:
                visit(child, parent_name)
        
        visit(root)
    
    def _extract_js_entities(
        self,
        root: Any,
        file_path: str,
        content: str,
        entities: List[CodeEntity],
        imports: List[str],
        exports: List[str]
    ) -> None:
        """Extract entities from JavaScript/TypeScript AST."""
        
        def visit(node, parent_name: Optional[str] = None):
            node_type = node.type
            
            if node_type in ("function_declaration", "arrow_function", "method_definition"):
                name_node = node.child_by_field_name("name")
                if name_node:
                    entity_type = NodeType.METHOD if parent_name else NodeType.FUNCTION
                    entity = CodeEntity(
                        name=name_node.text.decode("utf-8"),
                        type=entity_type,
                        file_path=file_path,
                        start_line=node.start_point[0] + 1,
                        end_line=node.end_point[0] + 1,
                        parent=parent_name
                    )
                    entities.append(entity)
            
            elif node_type == "class_declaration":
                name_node = node.child_by_field_name("name")
                if name_node:
                    class_name = name_node.text.decode("utf-8")
                    entity = CodeEntity(
                        name=class_name,
                        type=NodeType.CLASS,
                        file_path=file_path,
                        start_line=node.start_point[0] + 1,
                        end_line=node.end_point[0] + 1
                    )
                    entities.append(entity)
                    
                    for child in node.children:
                        visit(child, class_name)
                    return
            
            elif node_type == "interface_declaration":
                name_node = node.child_by_field_name("name")
                if name_node:
                    entity = CodeEntity(
                        name=name_node.text.decode("utf-8"),
                        type=NodeType.INTERFACE,
                        file_path=file_path,
                        start_line=node.start_point[0] + 1,
                        end_line=node.end_point[0] + 1
                    )
                    entities.append(entity)
            
            elif node_type == "import_statement":
                imports.append(node.text.decode("utf-8"))
            
            elif node_type == "export_statement":
                exports.append(node.text.decode("utf-8")[:100])  # Truncate
            
            for child in node.children:
                visit(child, parent_name)
        
        visit(root)
    
    def _extract_go_entities(
        self,
        root: Any,
        file_path: str,
        content: str,
        entities: List[CodeEntity],
        imports: List[str]
    ) -> None:
        """Extract entities from Go AST."""
        
        def visit(node):
            node_type = node.type
            
            if node_type == "function_declaration":
                name_node = node.child_by_field_name("name")
                if name_node:
                    entity = CodeEntity(
                        name=name_node.text.decode("utf-8"),
                        type=NodeType.FUNCTION,
                        file_path=file_path,
                        start_line=node.start_point[0] + 1,
                        end_line=node.end_point[0] + 1
                    )
                    entities.append(entity)
            
            elif node_type == "method_declaration":
                name_node = node.child_by_field_name("name")
                receiver_node = node.child_by_field_name("receiver")
                if name_node:
                    parent = None
                    if receiver_node:
                        parent = receiver_node.text.decode("utf-8")
                    entity = CodeEntity(
                        name=name_node.text.decode("utf-8"),
                        type=NodeType.METHOD,
                        file_path=file_path,
                        start_line=node.start_point[0] + 1,
                        end_line=node.end_point[0] + 1,
                        parent=parent
                    )
                    entities.append(entity)
            
            elif node_type == "type_declaration":
                for child in node.children:
                    if child.type == "type_spec":
                        name_node = child.child_by_field_name("name")
                        if name_node:
                            entity = CodeEntity(
                                name=name_node.text.decode("utf-8"),
                                type=NodeType.TYPE,
                                file_path=file_path,
                                start_line=child.start_point[0] + 1,
                                end_line=child.end_point[0] + 1
                            )
                            entities.append(entity)
            
            elif node_type == "import_declaration":
                imports.append(node.text.decode("utf-8"))
            
            for child in node.children:
                visit(child)
        
        visit(root)
    
    def _extract_generic_entities(
        self,
        root: Any,
        file_path: str,
        content: str,
        entities: List[CodeEntity]
    ) -> None:
        """Generic entity extraction for other languages."""
        
        def visit(node, depth: int = 0):
            if depth > 20:  # Prevent too deep recursion
                return
            
            node_type = node.type
            
            # Look for common function/class patterns
            if "function" in node_type or "method" in node_type:
                name_node = node.child_by_field_name("name")
                if name_node:
                    entity = CodeEntity(
                        name=name_node.text.decode("utf-8"),
                        type=NodeType.FUNCTION,
                        file_path=file_path,
                        start_line=node.start_point[0] + 1,
                        end_line=node.end_point[0] + 1
                    )
                    entities.append(entity)
            
            elif "class" in node_type or "struct" in node_type:
                name_node = node.child_by_field_name("name")
                if name_node:
                    entity = CodeEntity(
                        name=name_node.text.decode("utf-8"),
                        type=NodeType.CLASS,
                        file_path=file_path,
                        start_line=node.start_point[0] + 1,
                        end_line=node.end_point[0] + 1
                    )
                    entities.append(entity)
            
            for child in node.children:
                visit(child, depth + 1)
        
        visit(root)
    
    def _parse_with_regex(
        self, 
        file_path: str, 
        content: str, 
        language: str
    ) -> ParseResult:
        """Fallback regex-based parsing when tree-sitter unavailable."""
        import re
        
        entities = []
        imports = []
        exports = []
        lines = content.split("\n")
        
        # Language-specific patterns
        patterns = {
            "python": {
                "function": r"^\s*def\s+(\w+)\s*\(",
                "class": r"^\s*class\s+(\w+)\s*[\(:]",
                "import": r"^\s*(?:from\s+\S+\s+)?import\s+.+",
            },
            "javascript": {
                "function": r"(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:\([^)]*\)\s*=>|\function))",
                "class": r"^\s*class\s+(\w+)",
                "import": r"^\s*import\s+",
                "export": r"^\s*export\s+",
            },
            "typescript": {
                "function": r"(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:\([^)]*\)\s*=>|\function))",
                "class": r"^\s*(?:export\s+)?class\s+(\w+)",
                "interface": r"^\s*(?:export\s+)?interface\s+(\w+)",
                "import": r"^\s*import\s+",
                "export": r"^\s*export\s+",
            },
            "go": {
                "function": r"^\s*func\s+(?:\([^)]+\)\s+)?(\w+)\s*\(",
                "type": r"^\s*type\s+(\w+)\s+",
                "import": r"^\s*import\s+",
            },
        }
        
        lang_patterns = patterns.get(language, patterns.get("python", {}))
        
        for i, line in enumerate(lines, 1):
            # Check function patterns
            if "function" in lang_patterns:
                match = re.search(lang_patterns["function"], line)
                if match:
                    name = match.group(1) or (match.group(2) if len(match.groups()) > 1 else None)
                    if name:
                        entities.append(CodeEntity(
                            name=name,
                            type=NodeType.FUNCTION,
                            file_path=file_path,
                            start_line=i,
                            end_line=i  # Can't determine end without more parsing
                        ))
            
            # Check class patterns
            if "class" in lang_patterns:
                match = re.search(lang_patterns["class"], line)
                if match:
                    entities.append(CodeEntity(
                        name=match.group(1),
                        type=NodeType.CLASS,
                        file_path=file_path,
                        start_line=i,
                        end_line=i
                    ))
            
            # Check interface patterns (TypeScript)
            if "interface" in lang_patterns:
                match = re.search(lang_patterns["interface"], line)
                if match:
                    entities.append(CodeEntity(
                        name=match.group(1),
                        type=NodeType.INTERFACE,
                        file_path=file_path,
                        start_line=i,
                        end_line=i
                    ))
            
            # Check imports
            if "import" in lang_patterns:
                if re.search(lang_patterns["import"], line):
                    imports.append(line.strip())
            
            # Check exports
            if "export" in lang_patterns:
                if re.search(lang_patterns["export"], line):
                    exports.append(line.strip()[:100])
        
        return ParseResult(
            file_path=file_path,
            language=language,
            entities=entities,
            imports=imports,
            exports=exports,
            parse_time_ms=0
        )


# Global parser instance
_global_parser: Optional[TreeSitterParser] = None


def get_parser() -> TreeSitterParser:
    """Get global parser."""
    global _global_parser
    if _global_parser is None:
        _global_parser = TreeSitterParser()
    return _global_parser


def parse_file(file_path: str, content: Optional[str] = None) -> ParseResult:
    """Quick parse using global parser."""
    return get_parser().parse_file(file_path, content)
