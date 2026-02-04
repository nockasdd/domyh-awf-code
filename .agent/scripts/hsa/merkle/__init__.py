# HSA Merkle Module
# =============================================================================
"""
Merkle-based change tracking for HSA.

Components:
- MerkleCodeTracker: Track file changes with Merkle tree
- FileHasher: Hash file contents
- ChangeDetector: Detect changes in codebase
"""

from .file_hasher import (
    FileHash,
    FileHasher,
    hash_content,
    hash_file,
)

from .merkle_tree import (
    ChangeSet,
    MerkleCodeTracker,
    MerkleNode,
)

from .change_detector import (
    ChangeDetector,
    PeriodicChecker,
    create_change_monitor,
)

__all__ = [
    # File Hasher
    "FileHash",
    "FileHasher",
    "hash_content",
    "hash_file",
    # Merkle Tree
    "ChangeSet",
    "MerkleCodeTracker",
    "MerkleNode",
    # Change Detector
    "ChangeDetector",
    "PeriodicChecker",
    "create_change_monitor",
]
