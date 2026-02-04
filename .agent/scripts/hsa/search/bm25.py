# HSA v5.0 - BM25 Keyword Search
# =============================================================================
"""
BM25 keyword search for code.

Tier 0: Always available, no external dependencies beyond rank_bm25.

Features:
- Optimized for code tokens (camelCase, snake_case splitting)
- Incremental index updates
- Configurable k1 and b parameters
- Hybrid search ready (for combining with vector search)
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

logger = logging.getLogger("hsa.search")


@dataclass
class SearchResult:
    """Search result with score."""
    doc_id: str
    score: float
    content: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IndexStats:
    """Index statistics."""
    total_docs: int = 0
    total_tokens: int = 0
    avg_doc_length: float = 0.0
    unique_terms: int = 0


class CodeTokenizer:
    """
    Tokenizer optimized for code.
    
    Handles:
    - camelCase → camel, case
    - snake_case → snake, case
    - PascalCase → pascal, case
    - Operators and symbols
    - Numbers
    """
    
    # Pattern to split camelCase and PascalCase
    CAMEL_PATTERN = re.compile(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])')
    
    # Pattern to split on non-alphanumeric
    SPLIT_PATTERN = re.compile(r'[^a-zA-Z0-9]+')
    
    # Common stop words for code
    STOP_WORDS: Set[str] = {
        'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'could', 'should', 'may', 'might', 'must', 'shall',
        'can', 'need', 'dare', 'ought', 'used', 'to', 'of', 'in',
        'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
        'through', 'during', 'before', 'after', 'above', 'below',
        'between', 'under', 'again', 'further', 'then', 'once',
        'and', 'but', 'or', 'nor', 'so', 'yet', 'both', 'each',
        'this', 'that', 'these', 'those', 'it', 'its'
    }
    
    def __init__(
        self, 
        min_length: int = 2,
        max_length: int = 50,
        lowercase: bool = True,
        remove_stop_words: bool = True
    ):
        self.min_length = min_length
        self.max_length = max_length
        self.lowercase = lowercase
        self.remove_stop_words = remove_stop_words
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize code text.
        
        Args:
            text: Code or text to tokenize
            
        Returns:
            List of tokens
        """
        if not text:
            return []
        
        # Split by non-alphanumeric first
        words = self.SPLIT_PATTERN.split(text)
        
        tokens = []
        for word in words:
            if not word:
                continue
            
            # Split camelCase/PascalCase
            parts = self.CAMEL_PATTERN.split(word)
            
            for part in parts:
                if not part:
                    continue
                
                # Apply lowercase
                if self.lowercase:
                    part = part.lower()
                
                # Length filter
                if len(part) < self.min_length or len(part) > self.max_length:
                    continue
                
                # Stop word filter
                if self.remove_stop_words and part in self.STOP_WORDS:
                    continue
                
                tokens.append(part)
        
        return tokens


class BM25Index:
    """
    BM25 search index for code.
    
    Usage:
        index = BM25Index()
        
        # Add documents
        index.add_document("file1.py", "def hello_world(): pass")
        index.add_document("file2.py", "class UserService: ...")
        
        # Search
        results = index.search("hello world", k=10)
        for result in results:
            print(f"{result.doc_id}: {result.score}")
    """
    
    def __init__(
        self,
        k1: float = 1.5,
        b: float = 0.75,
        tokenizer: Optional[CodeTokenizer] = None
    ):
        """
        Initialize BM25 index.
        
        Args:
            k1: BM25 k1 parameter (term frequency saturation)
            b: BM25 b parameter (document length normalization)
            tokenizer: Custom tokenizer (defaults to CodeTokenizer)
        """
        self.k1 = k1
        self.b = b
        self.tokenizer = tokenizer or CodeTokenizer()
        
        # Index state
        self._doc_ids: List[str] = []
        self._doc_contents: Dict[str, str] = {}
        self._doc_metadata: Dict[str, Dict[str, Any]] = {}
        self._corpus: List[List[str]] = []
        self._bm25 = None
        self._needs_rebuild = True
        
        logger.debug(f"BM25 index initialized: k1={k1}, b={b}")
    
    def add_document(
        self,
        doc_id: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add document to index.
        
        Args:
            doc_id: Unique document identifier
            content: Document content
            metadata: Optional metadata
        """
        tokens = self.tokenizer.tokenize(content)
        
        if doc_id in self._doc_contents:
            # Update existing
            idx = self._doc_ids.index(doc_id)
            self._corpus[idx] = tokens
            self._doc_contents[doc_id] = content
        else:
            # Add new
            self._doc_ids.append(doc_id)
            self._corpus.append(tokens)
            self._doc_contents[doc_id] = content
        
        if metadata:
            self._doc_metadata[doc_id] = metadata
        
        self._needs_rebuild = True
    
    def remove_document(self, doc_id: str) -> bool:
        """
        Remove document from index.
        
        Args:
            doc_id: Document ID to remove
            
        Returns:
            True if removed, False if not found
        """
        if doc_id not in self._doc_contents:
            return False
        
        idx = self._doc_ids.index(doc_id)
        self._doc_ids.pop(idx)
        self._corpus.pop(idx)
        del self._doc_contents[doc_id]
        self._doc_metadata.pop(doc_id, None)
        
        self._needs_rebuild = True
        return True
    
    def _rebuild_if_needed(self) -> None:
        """Rebuild BM25 index if documents changed."""
        if not self._needs_rebuild:
            return
        
        if not self._corpus:
            self._bm25 = None
            return
        
        try:
            from rank_bm25 import BM25Okapi
            self._bm25 = BM25Okapi(self._corpus, k1=self.k1, b=self.b)
            self._needs_rebuild = False
            logger.debug(f"BM25 index rebuilt: {len(self._doc_ids)} documents")
        except ImportError:
            logger.error(
                "rank_bm25 not installed. Install with: pip install rank-bm25"
            )
            raise
    
    def search(
        self,
        query: str,
        k: int = 10,
        min_score: float = 0.0,
        include_content: bool = False
    ) -> List[SearchResult]:
        """
        Search for documents.
        
        Args:
            query: Search query
            k: Maximum results to return
            min_score: Minimum score threshold
            include_content: Include document content in results
            
        Returns:
            List of SearchResult sorted by score
        """
        self._rebuild_if_needed()
        
        if not self._bm25 or not self._doc_ids:
            return []
        
        # Tokenize query
        query_tokens = self.tokenizer.tokenize(query)
        
        if not query_tokens:
            return []
        
        # Get scores
        scores = self._bm25.get_scores(query_tokens)
        
        # Create results
        results = []
        for idx, score in enumerate(scores):
            if score < min_score:
                continue
            
            doc_id = self._doc_ids[idx]
            result = SearchResult(
                doc_id=doc_id,
                score=float(score),
                content=self._doc_contents[doc_id] if include_content else None,
                metadata=self._doc_metadata.get(doc_id, {})
            )
            results.append(result)
        
        # Sort by score descending
        results.sort(key=lambda x: x.score, reverse=True)
        
        return results[:k]
    
    def search_with_context(
        self,
        query: str,
        k: int = 10,
        context_lines: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Search with context snippets.
        
        Args:
            query: Search query
            k: Maximum results
            context_lines: Lines of context around matches
            
        Returns:
            Results with context snippets
        """
        results = self.search(query, k=k, include_content=True)
        query_tokens = set(self.tokenizer.tokenize(query))
        
        enriched = []
        for result in results:
            if not result.content:
                continue
            
            lines = result.content.split('\n')
            snippets = []
            
            for i, line in enumerate(lines):
                line_tokens = set(self.tokenizer.tokenize(line))
                if line_tokens & query_tokens:
                    # Found matching line
                    start = max(0, i - context_lines)
                    end = min(len(lines), i + context_lines + 1)
                    snippet = '\n'.join(lines[start:end])
                    snippets.append({
                        "line": i + 1,
                        "content": snippet
                    })
            
            enriched.append({
                "doc_id": result.doc_id,
                "score": result.score,
                "snippets": snippets[:3],  # Limit snippets
                "metadata": result.metadata
            })
        
        return enriched
    
    def get_stats(self) -> IndexStats:
        """Get index statistics."""
        self._rebuild_if_needed()
        
        total_tokens = sum(len(tokens) for tokens in self._corpus)
        unique_terms = len(set(
            token 
            for tokens in self._corpus 
            for token in tokens
        ))
        
        return IndexStats(
            total_docs=len(self._doc_ids),
            total_tokens=total_tokens,
            avg_doc_length=total_tokens / len(self._doc_ids) if self._doc_ids else 0,
            unique_terms=unique_terms
        )
    
    def clear(self) -> None:
        """Clear all documents from index."""
        self._doc_ids.clear()
        self._doc_contents.clear()
        self._doc_metadata.clear()
        self._corpus.clear()
        self._bm25 = None
        self._needs_rebuild = True
    
    def __len__(self) -> int:
        return len(self._doc_ids)
    
    def __contains__(self, doc_id: str) -> bool:
        return doc_id in self._doc_contents


# Global index instance
_global_index: Optional[BM25Index] = None


def get_index() -> BM25Index:
    """Get global BM25 index."""
    global _global_index
    if _global_index is None:
        _global_index = BM25Index()
    return _global_index


def search(query: str, k: int = 10) -> List[SearchResult]:
    """Quick search using global index."""
    return get_index().search(query, k=k)
