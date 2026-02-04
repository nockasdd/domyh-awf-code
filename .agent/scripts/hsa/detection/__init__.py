# HSA Detection Module
# =============================================================================
"""
Project/stack detection for HSA.

Components:
- ScoringProjectDetector: Score-based stack detection
- SkillScore: Score container
- DetectionResult: Detection result
"""

from .project_detector import (
    ScoringProjectDetector,
    SkillScore,
    DetectionResult,
    detect_project,
)

__all__ = [
    "ScoringProjectDetector",
    "SkillScore",
    "DetectionResult",
    "detect_project",
]
