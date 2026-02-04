# =============================================================================
# file_hasher.py — High-Performance File Hashing with Blake3
# =============================================================================
# HSA v5.0 - Phase 1: Merkle Tree Indexer
# Uses Blake3 for fast, cryptographically secure hashing
# =============================================================================

"""
File Hasher Module

Provides fast file hashing using Blake3 algorithm.
Falls back to hashlib.sha256 if blake3 is not installed.

Performance:
- Blake3: ~3GB/s on modern CPUs
- SHA256: ~500MB/s (fallback)
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

# Try to use blake3 for better performance
try:
    import blake3
    HAS_BLAKE3 = True
except ImportError:
    HAS_BLAKE3 = False


@dataclass
class FileHash:
    """Represents a file's hash with metadata."""
    path: str
    hash: str
    size: int
    mtime: float
    algorithm: str = "blake3"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FileHash):
            return False
        return self.hash == other.hash
    
    def __hash__(self) -> int:
        return hash(self.hash)


class FileHasher:
    """
    High-performance file hasher using Blake3.
    
    Features:
    - Blake3 for speed (3GB/s)
    - Streaming for large files
    - Fallback to SHA256
    - Caching for repeated hashes
    
    Usage:
        hasher = FileHasher()
        file_hash = hasher.hash_file("path/to/file.py")
        print(file_hash.hash)
    """
    
    # 64KB chunks for streaming
    CHUNK_SIZE = 65536
    
    def __init__(self, use_blake3: bool = True):
        """
        Initialize the hasher.
        
        Args:
            use_blake3: Use Blake3 if available (default True)
        """
        self.use_blake3 = use_blake3 and HAS_BLAKE3
        self.algorithm = "blake3" if self.use_blake3 else "sha256"
        self._cache: dict[str, FileHash] = {}
    
    def hash_file(self, path: Union[str, Path], use_cache: bool = True) -> FileHash:
        """
        Hash a file and return FileHash object.
        
        Args:
            path: Path to the file
            use_cache: Use cached hash if mtime unchanged
            
        Returns:
            FileHash object with hash and metadata
            
        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file can't be read
        """
        path = Path(path).resolve()
        path_str = str(path)
        
        # Check cache
        if use_cache and path_str in self._cache:
            cached = self._cache[path_str]
            try:
                stat = path.stat()
                if stat.st_mtime == cached.mtime and stat.st_size == cached.size:
                    return cached
            except OSError:
                pass
        
        # Compute hash
        stat = path.stat()
        hash_value = self._compute_hash(path)
        
        file_hash = FileHash(
            path=path_str,
            hash=hash_value,
            size=stat.st_size,
            mtime=stat.st_mtime,
            algorithm=self.algorithm
        )
        
        # Update cache
        self._cache[path_str] = file_hash
        
        return file_hash
    
    def hash_content(self, content: Union[str, bytes]) -> str:
        """
        Hash string or bytes content directly.
        
        Args:
            content: String or bytes to hash
            
        Returns:
            Hex-encoded hash string
        """
        if isinstance(content, str):
            content = content.encode('utf-8')
        
        if self.use_blake3:
            return blake3.blake3(content).hexdigest()
        else:
            return hashlib.sha256(content).hexdigest()
    
    def hash_directory(self, path: Union[str, Path]) -> str:
        """
        Hash a directory by combining child hashes.
        
        Used for Merkle tree internal nodes.
        
        Args:
            path: Directory path
            
        Returns:
            Hex-encoded hash of combined child hashes
        """
        path = Path(path).resolve()
        
        if not path.is_dir():
            raise ValueError(f"Not a directory: {path}")
        
        # Collect child hashes (sorted for determinism)
        child_hashes = []
        
        for child in sorted(path.iterdir()):
            if child.is_file():
                try:
                    file_hash = self.hash_file(child)
                    child_hashes.append(file_hash.hash)
                except (PermissionError, OSError):
                    continue
            elif child.is_dir():
                try:
                    dir_hash = self.hash_directory(child)
                    child_hashes.append(dir_hash)
                except (PermissionError, OSError):
                    continue
        
        # Combine hashes
        combined = "".join(child_hashes)
        return self.hash_content(combined)
    
    def _compute_hash(self, path: Path) -> str:
        """Compute hash of file contents using streaming."""
        if self.use_blake3:
            hasher = blake3.blake3()
        else:
            hasher = hashlib.sha256()
        
        with open(path, 'rb') as f:
            while chunk := f.read(self.CHUNK_SIZE):
                hasher.update(chunk)
        
        return hasher.hexdigest()
    
    def clear_cache(self) -> None:
        """Clear the hash cache."""
        self._cache.clear()
    
    def invalidate(self, path: Union[str, Path]) -> None:
        """Invalidate cache for a specific path."""
        path_str = str(Path(path).resolve())
        self._cache.pop(path_str, None)
    
    @property
    def cache_size(self) -> int:
        """Return number of cached hashes."""
        return len(self._cache)


# =============================================================================
# Convenience Functions
# =============================================================================

_default_hasher: Optional[FileHasher] = None


def get_hasher() -> FileHasher:
    """Get the default FileHasher instance."""
    global _default_hasher
    if _default_hasher is None:
        _default_hasher = FileHasher()
    return _default_hasher


def hash_file(path: Union[str, Path]) -> str:
    """Quick hash of a file."""
    return get_hasher().hash_file(path).hash


def hash_content(content: Union[str, bytes]) -> str:
    """Quick hash of content."""
    return get_hasher().hash_content(content)


# =============================================================================
# _DOMYH Awesome Code v6.1.2 • HSA v5.0 • File Hasher_
# =============================================================================
