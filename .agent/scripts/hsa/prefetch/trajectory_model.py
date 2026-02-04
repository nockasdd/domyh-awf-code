# =============================================================================
# trajectory_model.py — Markov-Based Access Pattern Predictor
# =============================================================================
# HSA v5.0 - Phase 5: Proactive Prefetching
# Implements file access trajectory prediction using Markov chains
# =============================================================================

"""
Trajectory Model Module

Implements Markov chain-based prediction for file access patterns.
Learns from user navigation history to predict next likely files.

From HSA_V4.yaml spec:
- Markov chain with decay
- Hit rate target: 60%
- Order: 1-2 (balancing accuracy vs memory)
"""

from __future__ import annotations

import json
import time
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, DefaultDict, Dict, List, Optional, Set, Tuple


@dataclass
class AccessEvent:
    """A single file access event."""
    file_id: str
    timestamp: float = field(default_factory=time.time)
    context: str = ""  # e.g., "edit", "view", "debug"
    
    def __repr__(self) -> str:
        return f"Access({self.file_id})"


@dataclass
class Prediction:
    """A predicted next file access."""
    file_id: str
    probability: float
    confidence: float
    source: str = "markov"
    
    def __repr__(self) -> str:
        return f"Pred({self.file_id}, p={self.probability:.2f})"


@dataclass
class TrajectoryStats:
    """Statistics about trajectory model performance."""
    total_predictions: int = 0
    correct_predictions: int = 0
    total_transitions: int = 0
    unique_files: int = 0
    
    @property
    def hit_rate(self) -> float:
        if self.total_predictions == 0:
            return 0.0
        return self.correct_predictions / self.total_predictions
    
    def to_dict(self) -> dict:
        return {
            "total_predictions": self.total_predictions,
            "correct_predictions": self.correct_predictions,
            "hit_rate": f"{self.hit_rate:.1%}",
            "total_transitions": self.total_transitions,
            "unique_files": self.unique_files
        }


class MarkovTrajectoryModel:
    """
    Markov chain model for predicting file access patterns.
    
    Uses transition probabilities to predict likely next files
    based on current file and optionally previous files (order-2).
    
    Features:
    - Order-1 and Order-2 Markov chain
    - Time-based decay for old transitions
    - Co-occurrence boosting for related files
    - Session-aware learning
    
    Usage:
        model = MarkovTrajectoryModel()
        
        # Record accesses
        model.record_access("main.py")
        model.record_access("utils.py")
        model.record_access("main.py")
        
        # Get predictions
        predictions = model.predict("main.py", k=3)
        for pred in predictions:
            print(f"{pred.file_id}: {pred.probability:.2%}")
    """
    
    # Decay half-life in seconds (1 hour)
    DECAY_HALFLIFE = 3600
    
    # Minimum probability to return
    MIN_PROBABILITY = 0.05
    
    def __init__(
        self,
        order: int = 2,
        decay_enabled: bool = True,
        co_occurrence_boost: float = 0.1
    ):
        """
        Initialize the trajectory model.
        
        Args:
            order: Markov chain order (1 or 2)
            decay_enabled: Enable time-based decay
            co_occurrence_boost: Boost for co-occurring files
        """
        self.order = min(order, 2)
        self.decay_enabled = decay_enabled
        self.co_occurrence_boost = co_occurrence_boost
        
        # Transition counts: from_state -> to_file -> (count, last_time)
        self._transitions: DefaultDict[str, DefaultDict[str, Tuple[float, float]]] = \
            defaultdict(lambda: defaultdict(lambda: (0.0, 0.0)))
        
        # Order-2 transitions: (prev, current) -> next -> (count, last_time)
        self._transitions_order2: DefaultDict[Tuple[str, str], DefaultDict[str, Tuple[float, float]]] = \
            defaultdict(lambda: defaultdict(lambda: (0.0, 0.0)))
        
        # Co-occurrence within sessions
        self._co_occurrence: DefaultDict[str, DefaultDict[str, float]] = \
            defaultdict(lambda: defaultdict(float))
        
        # Access history for current session
        self._session_history: List[AccessEvent] = []
        self._session_files: Set[str] = set()
        
        # Stats
        self._stats = TrajectoryStats()
        self._all_files: Set[str] = set()
        
        # Last prediction for hit tracking
        self._last_predictions: List[str] = []
    
    def record_access(self, file_id: str, context: str = "") -> None:
        """
        Record a file access.
        
        Updates transition probabilities and co-occurrence.
        """
        now = time.time()
        event = AccessEvent(file_id=file_id, timestamp=now, context=context)
        
        # Track hit rate
        if file_id in self._last_predictions:
            self._stats.correct_predictions += 1
        if self._last_predictions:
            self._stats.total_predictions += 1
        self._last_predictions = []
        
        # Update stats
        self._all_files.add(file_id)
        self._stats.unique_files = len(self._all_files)
        
        # Update order-1 transitions
        if self._session_history:
            prev = self._session_history[-1].file_id
            count, _ = self._transitions[prev][file_id]
            self._transitions[prev][file_id] = (count + 1, now)
            self._stats.total_transitions += 1
        
        # Update order-2 transitions
        if len(self._session_history) >= 2 and self.order >= 2:
            prev2 = self._session_history[-2].file_id
            prev1 = self._session_history[-1].file_id
            key = (prev2, prev1)
            count, _ = self._transitions_order2[key][file_id]
            self._transitions_order2[key][file_id] = (count + 1, now)
        
        # Update co-occurrence
        for session_file in self._session_files:
            if session_file != file_id:
                self._co_occurrence[session_file][file_id] += 1
                self._co_occurrence[file_id][session_file] += 1
        
        # Add to session
        self._session_history.append(event)
        self._session_files.add(file_id)
        
        # Limit session history
        if len(self._session_history) > 100:
            self._session_history = self._session_history[-50:]
    
    def predict(
        self,
        current_file: str,
        k: int = 3,
        exclude: Optional[Set[str]] = None
    ) -> List[Prediction]:
        """
        Predict next likely file accesses.
        
        Args:
            current_file: Current file being accessed
            k: Number of predictions to return
            exclude: Files to exclude from predictions
            
        Returns:
            List of Predictions sorted by probability
        """
        exclude = exclude or set()
        exclude.add(current_file)  # Don't predict current file
        
        now = time.time()
        candidates: Dict[str, float] = {}
        
        # Order-1 predictions
        for next_file, (count, last_time) in self._transitions[current_file].items():
            if next_file in exclude:
                continue
            
            prob = self._calculate_probability(count, last_time, now)
            candidates[next_file] = prob
        
        # Order-2 predictions (if available)
        if self.order >= 2 and len(self._session_history) >= 1:
            prev_file = self._session_history[-1].file_id
            key = (prev_file, current_file)
            
            for next_file, (count, last_time) in self._transitions_order2[key].items():
                if next_file in exclude:
                    continue
                
                prob = self._calculate_probability(count, last_time, now)
                # Order-2 gets 50% boost
                prob *= 1.5
                
                if next_file in candidates:
                    candidates[next_file] = max(candidates[next_file], prob)
                else:
                    candidates[next_file] = prob
        
        # Add co-occurrence boost
        for co_file, boost_count in self._co_occurrence[current_file].items():
            if co_file in exclude:
                continue
            
            boost = min(self.co_occurrence_boost * boost_count, 0.3)
            if co_file in candidates:
                candidates[co_file] += boost
            elif boost > self.MIN_PROBABILITY:
                candidates[co_file] = boost
        
        # Normalize and filter
        total = sum(candidates.values()) or 1.0
        predictions = []
        
        for file_id, score in sorted(candidates.items(), key=lambda x: -x[1])[:k]:
            prob = score / total
            if prob >= self.MIN_PROBABILITY:
                predictions.append(Prediction(
                    file_id=file_id,
                    probability=prob,
                    confidence=min(score / 5, 1.0),  # Confidence based on raw score
                    source="markov"
                ))
        
        # Track for hit rate
        self._last_predictions = [p.file_id for p in predictions]
        
        return predictions
    
    def _calculate_probability(
        self,
        count: float,
        last_time: float,
        now: float
    ) -> float:
        """Calculate probability with optional decay."""
        if not self.decay_enabled:
            return count
        
        # Apply exponential decay
        age = now - last_time
        decay_factor = 0.5 ** (age / self.DECAY_HALFLIFE)
        
        return count * decay_factor
    
    def new_session(self) -> None:
        """Start a new session (clears session history)."""
        self._session_history = []
        self._session_files = set()
    
    def get_stats(self) -> TrajectoryStats:
        """Get model statistics."""
        return self._stats
    
    def get_related_files(self, file_id: str, k: int = 5) -> List[Tuple[str, float]]:
        """
        Get files related to a given file via co-occurrence.
        
        Returns list of (file_id, score) tuples.
        """
        co_files = self._co_occurrence.get(file_id, {})
        sorted_files = sorted(co_files.items(), key=lambda x: -x[1])
        return sorted_files[:k]
    
    def save(self, path: Path) -> None:
        """Save model to disk."""
        data = {
            "order": self.order,
            "transitions": {
                k: dict(v) for k, v in self._transitions.items()
            },
            "transitions_order2": {
                f"{k[0]}|||{k[1]}": dict(v)
                for k, v in self._transitions_order2.items()
            },
            "co_occurrence": {
                k: dict(v) for k, v in self._co_occurrence.items()
            },
            "stats": self._stats.to_dict(),
            "all_files": list(self._all_files)
        }
        
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2))
    
    def load(self, path: Path) -> bool:
        """Load model from disk."""
        if not path.exists():
            return False
        
        try:
            data = json.loads(path.read_text())
            
            self.order = data.get("order", 2)
            
            # Load transitions
            for from_file, targets in data.get("transitions", {}).items():
                for to_file, value in targets.items():
                    if isinstance(value, (list, tuple)):
                        self._transitions[from_file][to_file] = tuple(value)
                    else:
                        self._transitions[from_file][to_file] = (value, 0.0)
            
            # Load order-2 transitions
            for key_str, targets in data.get("transitions_order2", {}).items():
                parts = key_str.split("|||")
                if len(parts) == 2:
                    key = (parts[0], parts[1])
                    for to_file, value in targets.items():
                        if isinstance(value, (list, tuple)):
                            self._transitions_order2[key][to_file] = tuple(value)
                        else:
                            self._transitions_order2[key][to_file] = (value, 0.0)
            
            # Load co-occurrence
            for file1, related in data.get("co_occurrence", {}).items():
                for file2, count in related.items():
                    self._co_occurrence[file1][file2] = count
            
            self._all_files = set(data.get("all_files", []))
            
            return True
        except Exception:
            return False


# =============================================================================
# _DOMYH Awesome Code v6.1.2 • HSA v5.0 • Trajectory Model_
# =============================================================================
