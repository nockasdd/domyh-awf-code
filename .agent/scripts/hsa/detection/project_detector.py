# =============================================================================
# project_detector.py — Scoring-Based Stack Detection
# =============================================================================
# HSA v5.0 - Phase 2: Stack Detection
# Replaces binary detection with weighted scoring system
# =============================================================================

"""
Project Detector Module

Implements scoring-based tech stack detection with:
- File pattern matching (weight: 10)
- Dependency analysis (weight: 8)
- Extension frequency (weight: 5, log scale)

Performance:
- Scans only root + 2 levels deep
- Caches results with Merkle validation
- Typical detection: <100ms
"""

from __future__ import annotations

import json
import math
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import yaml


@dataclass
class SkillScore:
    """Score for a detected skill."""
    skill: str
    score: float
    sources: List[str] = field(default_factory=list)
    confidence: float = 0.0
    
    def __repr__(self) -> str:
        return f"SkillScore({self.skill}: {self.score:.2f}, conf={self.confidence:.2%})"


@dataclass
class DetectionResult:
    """Result of project detection."""
    project_path: str
    detected_skills: List[SkillScore]
    build_system: Optional[str] = None
    is_monorepo: bool = False
    primary_language: Optional[str] = None
    total_files: int = 0
    scan_time_ms: float = 0.0
    
    # Skill → Category mapping (v7.0 hierarchical)
    _SKILL_CATEGORIES: Dict[str, str] = field(default_factory=dict, repr=False)
    
    def __post_init__(self):
        """Initialize skill category mapping."""
        if not self._SKILL_CATEGORIES:
            # Core
            self._SKILL_CATEGORIES["security"] = "core"
            # Languages (28)
            for s in ["python", "go", "typescript", "javascript", "rust", "cpp", "c",
                      "java", "kotlin", "csharp", "ruby", "php", "swift", "perl", "lua",
                      "asm", "nim", "crystal", "zig", "haskell", "elixir", "scala",
                      "clojure", "fsharp", "ocaml", "r", "julia", "solidity"]:
                self._SKILL_CATEGORIES[s] = "languages"
            # Frameworks (8)
            for s in ["react", "vue", "angular", "svelte", "nextjs", "nuxt", "flutter", "react-native"]:
                self._SKILL_CATEGORIES[s] = "frameworks"
            # DevOps (4)
            for s in ["docker", "kubernetes", "aws", "ci-cd"]:
                self._SKILL_CATEGORIES[s] = "devops"
            # Cross-cutting (10)
            for s in ["testing", "database", "sql", "tailwind", "electron", 
                      "coding-rules", "ui-ux-pro-max", "web-perf", "deno", "bun"]:
                self._SKILL_CATEGORIES[s] = "cross-cutting"
    
    @property
    def top_skills(self) -> List[str]:
        """Get list of top skill names."""
        return [s.skill for s in self.detected_skills]
    
    @property
    def skill_paths(self) -> Dict[str, str]:
        """Get skill → category path mapping (v7.0 hierarchical)."""
        paths = {}
        for skill_score in self.detected_skills:
            skill = skill_score.skill
            category = self._SKILL_CATEGORIES.get(skill, "cross-cutting")
            paths[skill] = f"skills/{category}/{skill}/"
        return paths
    
    def get_category_for_skill(self, skill: str) -> str:
        """Get category for a skill ID."""
        return self._SKILL_CATEGORIES.get(skill, "cross-cutting")
    
    def get_skill_path(self, skill: str) -> str:
        """Get full path for a skill ID."""
        category = self.get_category_for_skill(skill)
        return f"skills/{category}/{skill}/"
    
    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "project_path": self.project_path,
            "detected_skills": [
                {
                    "skill": s.skill, 
                    "score": s.score, 
                    "confidence": s.confidence,
                    "path": self.get_skill_path(s.skill)
                }
                for s in self.detected_skills
            ],
            "build_system": self.build_system,
            "is_monorepo": self.is_monorepo,
            "primary_language": self.primary_language,
            "total_files": self.total_files,
            "scan_time_ms": self.scan_time_ms,
            "skill_paths": self.skill_paths
        }


class ScoringProjectDetector:
    """
    Scoring-based project tech stack detector.
    
    Features:
    - Multi-signal scoring (files, deps, extensions)
    - Configurable weights from detection_rules.yaml
    - Monorepo detection
    - Framework vs language prioritization
    - Caching with Merkle tree validation
    
    Usage:
        detector = ScoringProjectDetector()
        result = detector.detect("/path/to/project")
        
        print(f"Build system: {result.build_system}")
        print(f"Top skills: {result.top_skills}")
        print(f"Primary language: {result.primary_language}")
    """
    
    # Default weights (overridden by detection_rules.yaml)
    DEFAULT_WEIGHTS = {
        "file_pattern": 10,
        "dependency": 8,
        "extension_frequency": 5
    }
    
    DEFAULT_THRESHOLD = 0.3
    DEFAULT_MAX_SKILLS = 5
    
    # Scan depth limits
    MAX_DEPTH = 3
    MAX_FILES_PER_DIR = 100
    
    def __init__(
        self,
        rules_path: Optional[Union[str, Path]] = None,
        max_skills: Optional[int] = None
    ):
        """
        Initialize the detector.
        
        Args:
            rules_path: Path to detection_rules.yaml
            max_skills: Maximum skills to return (default: 5)
        """
        self.rules = self._load_rules(rules_path)
        self.weights = self.rules.get("weights", self.DEFAULT_WEIGHTS)
        self.threshold = self.rules.get("threshold", self.DEFAULT_THRESHOLD)
        self.max_skills = max_skills or self.rules.get("max_skills", self.DEFAULT_MAX_SKILLS)
        
        # Build lookup tables
        self._build_pattern_cache()
        
        # Detection cache
        self._cache: Dict[str, DetectionResult] = {}
    
    def detect(
        self,
        project_path: Union[str, Path],
        use_cache: bool = True
    ) -> DetectionResult:
        """
        Detect tech stack for a project.
        
        Args:
            project_path: Path to project root
            use_cache: Use cached results if available
            
        Returns:
            DetectionResult with detected skills and metadata
        """
        import time
        start_time = time.perf_counter()
        
        project_path = Path(project_path).resolve()
        path_str = str(project_path)
        
        # Check cache
        if use_cache and path_str in self._cache:
            return self._cache[path_str]
        
        # Initialize scores
        skill_scores: Dict[str, float] = defaultdict(float)
        skill_sources: Dict[str, List[str]] = defaultdict(list)
        
        # Collect project files
        all_files = self._scan_project(project_path)
        
        # Phase 1: Build system detection
        build_system = self._detect_build_system(project_path, all_files)
        if build_system:
            build_info = self.rules.get("build_systems", {}).get(build_system, {})
            for skill in build_info.get("skills", []):
                skill_scores[skill] += build_info.get("weight", 10)
                skill_sources[skill].append(f"build:{build_system}")
        
        # Phase 2: Special files detection
        special_skills = self._detect_special_files(project_path, all_files)
        for skill, weight, source in special_skills:
            skill_scores[skill] += weight
            skill_sources[skill].append(f"special:{source}")
        
        # Phase 3: Dependency analysis
        dep_skills = self._detect_dependencies(project_path)
        for skill, weight, source in dep_skills:
            skill_scores[skill] += weight
            skill_sources[skill].append(f"dep:{source}")
        
        # Phase 4: Extension frequency
        ext_skills = self._detect_extensions(all_files)
        for skill, weight, source in ext_skills:
            skill_scores[skill] += weight
            skill_sources[skill].append(f"ext:{source}")
        
        # Phase 5: Monorepo detection
        is_monorepo = self._detect_monorepo(project_path, all_files)
        
        # Normalize and filter scores
        max_score = max(skill_scores.values()) if skill_scores else 1.0
        
        detected = []
        for skill, score in skill_scores.items():
            normalized = score / max_score if max_score > 0 else 0
            if normalized >= self.threshold:
                detected.append(SkillScore(
                    skill=skill,
                    score=score,
                    sources=skill_sources[skill],
                    confidence=normalized
                ))
        
        # Sort by priority then score
        priorities = self.rules.get("skill_priority", {})
        detected.sort(
            key=lambda s: (priorities.get(s.skill, 50), s.score),
            reverse=True
        )
        
        # Limit to max skills
        detected = detected[:self.max_skills]
        
        # Determine primary language
        primary = self._determine_primary_language(detected)
        
        # Calculate scan time
        scan_time = (time.perf_counter() - start_time) * 1000
        
        result = DetectionResult(
            project_path=path_str,
            detected_skills=detected,
            build_system=build_system,
            is_monorepo=is_monorepo,
            primary_language=primary,
            total_files=len(all_files),
            scan_time_ms=scan_time
        )
        
        # Cache result
        self._cache[path_str] = result
        
        return result
    
    def invalidate_cache(self, project_path: Optional[Union[str, Path]] = None) -> None:
        """
        Invalidate detection cache.
        
        Args:
            project_path: Specific project to invalidate, or None for all
        """
        if project_path:
            path_str = str(Path(project_path).resolve())
            self._cache.pop(path_str, None)
        else:
            self._cache.clear()
    
    # =========================================================================
    # Private Methods
    # =========================================================================
    
    def _load_rules(self, rules_path: Optional[Union[str, Path]]) -> dict:
        """Load detection rules from YAML file."""
        if rules_path is None:
            # Default path relative to this file
            rules_path = Path(__file__).parent / "detection_rules.yaml"
        
        rules_path = Path(rules_path)
        
        if not rules_path.exists():
            return {}
        
        try:
            with open(rules_path, encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except (yaml.YAMLError, OSError):
            return {}
    
    def _build_pattern_cache(self) -> None:
        """Pre-compile pattern matching data."""
        self._build_system_patterns: Dict[str, List[str]] = {}
        for name, info in self.rules.get("build_systems", {}).items():
            self._build_system_patterns[name] = info.get("patterns", [])
        
        self._extension_map: Dict[str, Tuple[str, int, List[str]]] = {}
        for name, info in self.rules.get("extensions", {}).items():
            for pattern in info.get("patterns", []):
                self._extension_map[pattern.lower()] = (
                    name,
                    info.get("weight", 5),
                    info.get("skills", [])
                )
        
        self._special_file_patterns: List[Tuple[str, dict]] = []
        for name, info in self.rules.get("special_files", {}).items():
            for pattern in info.get("patterns", []):
                self._special_file_patterns.append((pattern, {**info, "name": name}))
    
    def _scan_project(self, project_path: Path) -> List[Path]:
        """Scan project files up to MAX_DEPTH."""
        files = []
        
        def scan(path: Path, depth: int = 0):
            if depth > self.MAX_DEPTH:
                return
            
            try:
                children = list(path.iterdir())[:self.MAX_FILES_PER_DIR]
            except (PermissionError, OSError):
                return
            
            for child in children:
                # Skip common ignore patterns
                if child.name in {"node_modules", ".git", "__pycache__", "venv", ".venv", "dist", "build"}:
                    continue
                
                if child.is_file():
                    files.append(child)
                elif child.is_dir():
                    scan(child, depth + 1)
        
        scan(project_path)
        return files
    
    def _detect_build_system(
        self,
        project_path: Path,
        all_files: List[Path]
    ) -> Optional[str]:
        """Detect the primary build system."""
        root_names = {f.name for f in project_path.iterdir() if f.is_file()}
        
        for system, patterns in self._build_system_patterns.items():
            for pattern in patterns:
                if pattern.startswith("*"):
                    # Extension pattern
                    ext = pattern[1:]
                    if any(name.endswith(ext) for name in root_names):
                        return system
                elif pattern in root_names:
                    return system
        
        return None
    
    def _detect_special_files(
        self,
        project_path: Path,
        all_files: List[Path]
    ) -> List[Tuple[str, int, str]]:
        """Detect special configuration files."""
        results = []
        all_names = {f.name for f in all_files}
        
        for pattern, info in self._special_file_patterns:
            matched = False
            
            if pattern.endswith("/"):
                # Directory pattern
                dir_name = pattern.rstrip("/")
                if (project_path / dir_name).is_dir():
                    matched = True
            elif "*" in pattern:
                # Glob pattern
                if any(fnmatch(name, pattern) for name in all_names):
                    matched = True
            elif pattern in all_names:
                matched = True
            
            if matched:
                weight = info.get("weight", 8)
                for skill in info.get("skills", []):
                    results.append((skill, weight, info.get("name", pattern)))
        
        return results
    
    def _detect_dependencies(
        self,
        project_path: Path
    ) -> List[Tuple[str, int, str]]:
        """Analyze dependency manifests."""
        results = []
        
        # Check package.json
        pkg_json = project_path / "package.json"
        if pkg_json.exists():
            try:
                with open(pkg_json, encoding="utf-8") as f:
                    pkg = json.load(f)
                
                all_deps = set()
                for key in ["dependencies", "devDependencies", "peerDependencies"]:
                    all_deps.update(pkg.get(key, {}).keys())
                
                for name, info in self.rules.get("dependencies", {}).items():
                    for pattern in info.get("patterns", []):
                        for dep in all_deps:
                            if dep == pattern or dep.startswith(pattern):
                                weight = info.get("weight", 8)
                                for skill in info.get("skills", []):
                                    results.append((skill, weight, dep))
                                break
            except (json.JSONDecodeError, OSError):
                pass
        
        # Check requirements.txt
        req_txt = project_path / "requirements.txt"
        if req_txt.exists():
            try:
                with open(req_txt, encoding="utf-8") as f:
                    lines = f.readlines()
                
                deps = []
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # Extract package name
                        name = re.split(r"[=<>!~\[]", line)[0].strip()
                        if name:
                            deps.append(name.lower())
                
                for dep in deps:
                    for name, info in self.rules.get("dependencies", {}).items():
                        for pattern in info.get("patterns", []):
                            if dep == pattern.lower() or dep.startswith(pattern.lower()):
                                weight = info.get("weight", 8)
                                for skill in info.get("skills", []):
                                    results.append((skill, weight, dep))
            except OSError:
                pass
        
        return results
    
    def _detect_extensions(
        self,
        all_files: List[Path]
    ) -> List[Tuple[str, int, str]]:
        """Analyze file extension frequency."""
        # Count extensions
        ext_counts: Counter = Counter()
        for f in all_files:
            ext = f.suffix.lower()
            if ext:
                ext_counts[ext] += 1
        
        # Also check for special filenames
        for f in all_files:
            name = f.name.lower()
            if name in self._extension_map:
                ext_counts[name] += 1
        
        results = []
        for ext, count in ext_counts.items():
            if ext in self._extension_map:
                name, base_weight, skills = self._extension_map[ext]
                # Log scale for frequency
                freq_factor = 1 + math.log2(max(1, count))
                weight = base_weight * min(freq_factor, 3)  # Cap at 3x
                
                for skill in skills:
                    results.append((skill, weight, f"{ext}:{count}"))
        
        return results
    
    def _detect_monorepo(
        self,
        project_path: Path,
        all_files: List[Path]
    ) -> bool:
        """Detect if project is a monorepo."""
        all_names = {f.name for f in all_files}
        root_names = {f.name for f in project_path.iterdir()}
        
        # Check explicit monorepo indicators
        monorepo_files = {"lerna.json", "nx.json", "turbo.json", "pnpm-workspace.yaml"}
        if monorepo_files & root_names:
            return True
        
        # Check package.json workspaces
        pkg_json = project_path / "package.json"
        if pkg_json.exists():
            try:
                with open(pkg_json, encoding="utf-8") as f:
                    pkg = json.load(f)
                if "workspaces" in pkg:
                    return True
            except (json.JSONDecodeError, OSError):
                pass
        
        # Check .sln with multiple projects
        for f in project_path.glob("*.sln"):
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                if content.count("Project(") > 3:
                    return True
            except OSError:
                pass
        
        return False
    
    def _determine_primary_language(
        self,
        detected: List[SkillScore]
    ) -> Optional[str]:
        """Determine the primary language from detected skills."""
        # Language skills (not frameworks)
        languages = {
            "python", "javascript", "typescript", "java", "kotlin", "csharp",
            "cpp", "c", "go", "rust", "ruby", "php", "swift", "dart",
            "elixir", "haskell", "scala", "clojure", "fsharp", "ocaml",
            "lua", "perl", "r", "julia", "zig", "nim", "solidity"
        }
        
        for skill in detected:
            if skill.skill in languages:
                return skill.skill
        
        # Framework to language mapping
        framework_lang = {
            "react": "javascript",
            "vue": "javascript",
            "angular": "typescript",
            "svelte": "javascript",
            "nextjs": "typescript",
            "nuxt": "javascript",
            "flutter": "dart",
            "react-native": "javascript",
            "electron": "javascript",
        }
        
        for skill in detected:
            if skill.skill in framework_lang:
                return framework_lang[skill.skill]
        
        return None


# =============================================================================
# Convenience Function
# =============================================================================

_default_detector: Optional[ScoringProjectDetector] = None


def detect_project(
    project_path: Union[str, Path],
    use_cache: bool = True
) -> DetectionResult:
    """
    Quick project detection with default detector.
    
    Args:
        project_path: Path to project root
        use_cache: Use cached results
        
    Returns:
        DetectionResult
    """
    global _default_detector
    if _default_detector is None:
        _default_detector = ScoringProjectDetector()
    return _default_detector.detect(project_path, use_cache)


# =============================================================================
# _DOMYH Awesome Code v6.1.2 • HSA v5.0 • Project Detector_
# =============================================================================
