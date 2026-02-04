# HSA Prefetch Module
# =============================================================================
"""
Proactive prefetching for HSA.

Components:
- MarkovTrajectoryModel: Predict next file access
- Prefetcher: Prefetch files before they're needed
"""

from .trajectory_model import (
    MarkovTrajectoryModel,
    Prediction,
    AccessEvent,
    TrajectoryStats,
)

from .prefetcher import (
    Prefetcher,
    AsyncPrefetcher,
    PrefetchedFile,
    PrefetchStats,
    prefetch_file,
)

__all__ = [
    # Trajectory Model
    "MarkovTrajectoryModel",
    "Prediction",
    "AccessEvent",
    "TrajectoryStats",
    # Prefetcher
    "Prefetcher",
    "AsyncPrefetcher",
    "PrefetchedFile",
    "PrefetchStats",
    "prefetch_file",
]
