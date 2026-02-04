# =============================================================================
# change_detector.py — Debounced File Change Detection
# =============================================================================
# HSA v5.0 - Phase 1: Merkle Tree Indexer
# Watches filesystem and detects changes with debouncing
# =============================================================================

"""
Change Detector Module

Watches for file changes and triggers Merkle tree updates.
Uses debouncing to batch rapid changes (e.g., during git operations).

Features:
- Debounced change detection (500ms default)
- Configurable ignore patterns
- Callback-based notification
- Thread-safe operation
"""

from __future__ import annotations

import os
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional, Set, Union

from .merkle_tree import ChangeSet, MerkleCodeTracker


@dataclass
class PendingChange:
    """Represents a pending file change."""
    path: str
    change_type: str  # "added", "modified", "deleted"
    timestamp: float


class ChangeDetector:
    """
    Debounced file change detector for Merkle tree updates.
    
    Features:
    - Debounces rapid changes (500ms default)
    - Batches related changes
    - Configurable callbacks
    - Thread-safe
    
    Usage:
        tracker = MerkleCodeTracker("/path/to/project")
        tracker.build()
        
        detector = ChangeDetector(
            tracker=tracker,
            debounce_ms=500,
            on_changes=lambda changes: print(f"Changed: {changes}")
        )
        
        # Report changes as they occur
        detector.on_file_change("/path/to/project/src/main.py", "modified")
        
        # Flush pending changes manually
        changes = detector.flush()
    """
    
    def __init__(
        self,
        tracker: MerkleCodeTracker,
        debounce_ms: int = 500,
        on_changes: Optional[Callable[[ChangeSet], None]] = None,
        auto_update: bool = True
    ):
        """
        Initialize the change detector.
        
        Args:
            tracker: MerkleCodeTracker instance
            debounce_ms: Debounce window in milliseconds
            on_changes: Callback when changes are detected
            auto_update: Automatically update tracker on changes
        """
        self.tracker = tracker
        self.debounce_ms = debounce_ms
        self.on_changes = on_changes
        self.auto_update = auto_update
        
        self._pending: Dict[str, PendingChange] = {}
        self._lock = threading.RLock()
        self._timer: Optional[threading.Timer] = None
        self._last_flush: float = 0.0
    
    def on_file_change(
        self,
        path: Union[str, Path],
        change_type: str = "modified"
    ) -> None:
        """
        Report a file change.
        
        Args:
            path: Path to the changed file
            change_type: Type of change ("added", "modified", "deleted")
        """
        path_str = str(Path(path).resolve())
        
        with self._lock:
            # Check if should ignore
            if self._should_ignore(path_str):
                return
            
            # Add to pending
            self._pending[path_str] = PendingChange(
                path=path_str,
                change_type=change_type,
                timestamp=time.time()
            )
            
            # Schedule debounced flush
            self._schedule_flush()
    
    def on_file_created(self, path: Union[str, Path]) -> None:
        """Report a file creation."""
        self.on_file_change(path, "added")
    
    def on_file_modified(self, path: Union[str, Path]) -> None:
        """Report a file modification."""
        self.on_file_change(path, "modified")
    
    def on_file_deleted(self, path: Union[str, Path]) -> None:
        """Report a file deletion."""
        self.on_file_change(path, "deleted")
    
    def flush(self) -> ChangeSet:
        """
        Flush pending changes and update tracker.
        
        Returns:
            ChangeSet with all pending changes
        """
        with self._lock:
            # Cancel pending timer
            if self._timer:
                self._timer.cancel()
                self._timer = None
            
            if not self._pending:
                return ChangeSet()
            
            # Build changeset from pending
            changes = ChangeSet()
            
            for pending in self._pending.values():
                if pending.change_type == "added":
                    changes.added.append(pending.path)
                elif pending.change_type == "modified":
                    changes.modified.append(pending.path)
                elif pending.change_type == "deleted":
                    changes.deleted.append(pending.path)
            
            # Clear pending
            self._pending.clear()
            self._last_flush = time.time()
            
            # Update tracker if enabled
            if self.auto_update and changes.has_changes:
                self.tracker.update(changes)
            
            # Notify callback
            if self.on_changes and changes.has_changes:
                try:
                    self.on_changes(changes)
                except Exception:
                    pass  # Don't let callback errors break the detector
            
            return changes
    
    def detect_and_flush(self) -> ChangeSet:
        """
        Detect changes from filesystem and flush.
        
        Uses Merkle tree to detect changes rather than pending queue.
        Useful for periodic full checks.
        
        Returns:
            ChangeSet from Merkle comparison
        """
        with self._lock:
            # Clear pending (we're doing a full detect)
            self._pending.clear()
            
            # Detect from Merkle
            changes = self.tracker.detect_changes()
            
            # Update and notify
            if changes.has_changes:
                if self.auto_update:
                    self.tracker.update(changes)
                
                if self.on_changes:
                    try:
                        self.on_changes(changes)
                    except Exception:
                        pass
            
            self._last_flush = time.time()
            return changes
    
    @property
    def pending_count(self) -> int:
        """Number of pending changes."""
        with self._lock:
            return len(self._pending)
    
    @property
    def time_since_flush(self) -> float:
        """Seconds since last flush."""
        return time.time() - self._last_flush
    
    def clear_pending(self) -> None:
        """Clear pending changes without flushing."""
        with self._lock:
            if self._timer:
                self._timer.cancel()
                self._timer = None
            self._pending.clear()
    
    def _schedule_flush(self) -> None:
        """Schedule a debounced flush."""
        # Cancel existing timer
        if self._timer:
            self._timer.cancel()
        
        # Schedule new timer
        delay = self.debounce_ms / 1000.0
        self._timer = threading.Timer(delay, self._debounced_flush)
        self._timer.daemon = True
        self._timer.start()
    
    def _debounced_flush(self) -> None:
        """Called by timer to flush pending changes."""
        self.flush()
    
    def _should_ignore(self, path: str) -> bool:
        """Check if path should be ignored."""
        path_obj = Path(path)
        
        # Check against tracker's ignore patterns
        for pattern in self.tracker.ignore_patterns:
            if pattern.startswith("*"):
                if path_obj.name.endswith(pattern[1:]):
                    return True
            elif pattern in path:
                return True
        
        return False


class PeriodicChecker:
    """
    Periodically checks for changes using Merkle tree.
    
    Used as a safety net for file watchers that might miss events.
    Default interval: 5 minutes (300 seconds).
    
    Usage:
        checker = PeriodicChecker(tracker, interval_seconds=300)
        checker.start()
        
        # ... later ...
        checker.stop()
    """
    
    def __init__(
        self,
        tracker: MerkleCodeTracker,
        interval_seconds: float = 300,
        on_changes: Optional[Callable[[ChangeSet], None]] = None
    ):
        """
        Initialize the periodic checker.
        
        Args:
            tracker: MerkleCodeTracker instance
            interval_seconds: Check interval (default: 5 minutes)
            on_changes: Callback when changes detected
        """
        self.tracker = tracker
        self.interval = interval_seconds
        self.on_changes = on_changes
        
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
    
    def start(self) -> None:
        """Start periodic checking."""
        if self._running:
            return
        
        self._running = True
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
    
    def stop(self) -> None:
        """Stop periodic checking."""
        self._running = False
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2.0)
            self._thread = None
    
    def check_now(self) -> ChangeSet:
        """Perform an immediate check."""
        changes = self.tracker.detect_changes()
        
        if changes.has_changes:
            self.tracker.update(changes)
            if self.on_changes:
                try:
                    self.on_changes(changes)
                except Exception:
                    pass
        
        return changes
    
    def _run(self) -> None:
        """Background checking loop."""
        while self._running:
            # Wait for interval or stop signal
            if self._stop_event.wait(self.interval):
                break
            
            # Perform check
            try:
                self.check_now()
            except Exception:
                pass  # Don't let errors stop the checker
    
    @property
    def is_running(self) -> bool:
        """Check if periodic checker is running."""
        return self._running


# =============================================================================
# Integration Helper
# =============================================================================

def create_change_monitor(
    root_path: Union[str, Path],
    on_changes: Optional[Callable[[ChangeSet], None]] = None,
    debounce_ms: int = 500,
    check_interval: float = 300,
    cache_path: Optional[Union[str, Path]] = None
) -> tuple[MerkleCodeTracker, ChangeDetector, PeriodicChecker]:
    """
    Create a complete change monitoring setup.
    
    Args:
        root_path: Project root to monitor
        on_changes: Callback for detected changes
        debounce_ms: Debounce window for rapid changes
        check_interval: Interval for periodic full checks
        cache_path: Path to persist Merkle tree
    
    Returns:
        Tuple of (tracker, detector, checker)
    
    Example:
        tracker, detector, checker = create_change_monitor(
            "/path/to/project",
            on_changes=lambda c: print(f"Changed: {c}"),
            cache_path=".agent/memory/merkle_cache.json"
        )
        
        # Build initial tree
        tracker.build()
        
        # Start periodic checks
        checker.start()
        
        # Report file changes as they occur
        detector.on_file_modified("/path/to/project/src/main.py")
    """
    # Create tracker
    tracker = MerkleCodeTracker(
        root_path=root_path,
        cache_path=cache_path
    )
    
    # Create detector
    detector = ChangeDetector(
        tracker=tracker,
        debounce_ms=debounce_ms,
        on_changes=on_changes,
        auto_update=True
    )
    
    # Create periodic checker
    checker = PeriodicChecker(
        tracker=tracker,
        interval_seconds=check_interval,
        on_changes=on_changes
    )
    
    return tracker, detector, checker


# =============================================================================
# _DOMYH Awesome Code v6.1.2 • HSA v5.0 • Change Detector_
# =============================================================================
