# =============================================================================
# community_graph.py — Community Detection with Leiden Algorithm
# =============================================================================
# HSA v5.0 - Phase 3: HiRAG Integration
# Implements hierarchical community detection for knowledge graphs
# =============================================================================

"""
Community Graph Module

Implements community detection for hierarchical context organization.
Uses simplified Leiden algorithm (or fallback to label propagation).

Key concepts from HiRAG research:
- Global context: Community summaries (high-level abstractions)
- Bridge context: Cross-community connections (shortest paths)
- Local context: Individual entity descriptions
"""

from __future__ import annotations

import hashlib
import json
import random
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, Iterator, List, Optional, Set, Tuple, Union


@dataclass
class Entity:
    """Represents an entity (file, function, class) in the graph."""
    id: str
    name: str
    entity_type: str  # "file", "function", "class", "module"
    description: str = ""
    content_hash: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.id == other.id


@dataclass
class Relation:
    """Represents a relationship between entities."""
    source_id: str
    target_id: str
    relation_type: str  # "imports", "calls", "extends", "tests", "types"
    weight: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def key(self) -> Tuple[str, str, str]:
        return (self.source_id, self.target_id, self.relation_type)


@dataclass
class Community:
    """Represents a cluster of related entities."""
    id: str
    name: str
    entity_ids: Set[str] = field(default_factory=set)
    summary: str = ""
    level: int = 0  # Hierarchy level (0 = leaf, higher = more abstract)
    parent_id: Optional[str] = None
    child_ids: Set[str] = field(default_factory=set)
    
    @property
    def size(self) -> int:
        return len(self.entity_ids)


class CommunityGraph:
    """
    Graph structure with community detection for hierarchical retrieval.
    
    Architecture (from HiRAG research):
    1. Build entity graph with relations
    2. Detect communities using Leiden/Label Propagation
    3. Generate community summaries (global context)
    4. Find bridge entities between communities
    
    Usage:
        graph = CommunityGraph()
        
        # Add entities
        graph.add_entity(Entity(id="main.py", name="main", entity_type="file"))
        graph.add_entity(Entity(id="utils.py", name="utils", entity_type="file"))
        
        # Add relations
        graph.add_relation(Relation(
            source_id="main.py",
            target_id="utils.py",
            relation_type="imports"
        ))
        
        # Detect communities
        graph.detect_communities()
        
        # Get global context (community summaries)
        global_ctx = graph.get_global_context(k=3)
    """
    
    def __init__(self, resolution: float = 1.0, min_community_size: int = 3):
        """
        Initialize the community graph.
        
        Args:
            resolution: Leiden resolution parameter (higher = smaller communities)
            min_community_size: Minimum entities per community
        """
        self.resolution = resolution
        self.min_community_size = min_community_size
        
        # Graph storage
        self.entities: Dict[str, Entity] = {}
        self.relations: Dict[Tuple[str, str, str], Relation] = {}
        self.adjacency: Dict[str, Set[str]] = defaultdict(set)
        self.reverse_adjacency: Dict[str, Set[str]] = defaultdict(set)
        
        # Community storage
        self.communities: Dict[str, Community] = {}
        self.entity_to_community: Dict[str, str] = {}
        
        # Cache
        self._dirty = True
    
    # =========================================================================
    # Graph Building
    # =========================================================================
    
    def add_entity(self, entity: Entity) -> None:
        """Add an entity to the graph."""
        self.entities[entity.id] = entity
        self._dirty = True
    
    def add_relation(self, relation: Relation) -> None:
        """Add a relation between entities."""
        if relation.source_id not in self.entities:
            raise ValueError(f"Source entity not found: {relation.source_id}")
        if relation.target_id not in self.entities:
            raise ValueError(f"Target entity not found: {relation.target_id}")
        
        self.relations[relation.key] = relation
        self.adjacency[relation.source_id].add(relation.target_id)
        self.reverse_adjacency[relation.target_id].add(relation.source_id)
        self._dirty = True
    
    def remove_entity(self, entity_id: str) -> None:
        """Remove an entity and its relations."""
        if entity_id not in self.entities:
            return
        
        # Remove relations
        to_remove = [
            key for key in self.relations
            if key[0] == entity_id or key[1] == entity_id
        ]
        for key in to_remove:
            del self.relations[key]
        
        # Update adjacency
        self.adjacency.pop(entity_id, None)
        self.reverse_adjacency.pop(entity_id, None)
        
        for neighbors in self.adjacency.values():
            neighbors.discard(entity_id)
        for neighbors in self.reverse_adjacency.values():
            neighbors.discard(entity_id)
        
        # Remove entity
        del self.entities[entity_id]
        self._dirty = True
    
    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """Get an entity by ID."""
        return self.entities.get(entity_id)
    
    def get_neighbors(self, entity_id: str, direction: str = "both") -> Set[str]:
        """
        Get neighboring entities.
        
        Args:
            entity_id: Entity to get neighbors for
            direction: "outgoing", "incoming", or "both"
        """
        neighbors = set()
        
        if direction in ("outgoing", "both"):
            neighbors |= self.adjacency.get(entity_id, set())
        
        if direction in ("incoming", "both"):
            neighbors |= self.reverse_adjacency.get(entity_id, set())
        
        return neighbors
    
    # =========================================================================
    # Community Detection
    # =========================================================================
    
    def detect_communities(
        self,
        algorithm: str = "label_propagation",
        max_iterations: int = 100
    ) -> int:
        """
        Detect communities in the graph.
        
        Args:
            algorithm: "label_propagation" or "leiden" (fallback to LP)
            max_iterations: Maximum iterations for convergence
            
        Returns:
            Number of communities detected
        """
        if not self.entities:
            return 0
        
        # Use label propagation (simpler, no external deps)
        labels = self._label_propagation(max_iterations)
        
        # Build communities from labels
        self.communities.clear()
        self.entity_to_community.clear()
        
        label_to_entities: Dict[int, Set[str]] = defaultdict(set)
        for entity_id, label in labels.items():
            label_to_entities[label].add(entity_id)
        
        # Create community objects
        for label, entity_ids in label_to_entities.items():
            if len(entity_ids) < self.min_community_size:
                continue
            
            community_id = f"community_{label}"
            
            # Generate community name from common patterns
            name = self._generate_community_name(entity_ids)
            
            community = Community(
                id=community_id,
                name=name,
                entity_ids=entity_ids,
                level=0
            )
            
            self.communities[community_id] = community
            
            for entity_id in entity_ids:
                self.entity_to_community[entity_id] = community_id
        
        self._dirty = False
        return len(self.communities)
    
    def _label_propagation(self, max_iterations: int) -> Dict[str, int]:
        """
        Simple label propagation for community detection.
        
        Each node adopts the most frequent label among neighbors.
        """
        # Initialize each node with unique label
        labels: Dict[str, int] = {
            entity_id: i for i, entity_id in enumerate(self.entities)
        }
        
        entity_list = list(self.entities.keys())
        
        for iteration in range(max_iterations):
            changed = False
            random.shuffle(entity_list)
            
            for entity_id in entity_list:
                neighbors = self.get_neighbors(entity_id)
                if not neighbors:
                    continue
                
                # Count neighbor labels
                label_counts: Dict[int, float] = defaultdict(float)
                for neighbor_id in neighbors:
                    neighbor_label = labels[neighbor_id]
                    
                    # Weight by relation strength
                    for key in self.relations:
                        if (key[0] == entity_id and key[1] == neighbor_id) or \
                           (key[0] == neighbor_id and key[1] == entity_id):
                            label_counts[neighbor_label] += self.relations[key].weight
                            break
                    else:
                        label_counts[neighbor_label] += 1.0
                
                # Adopt most common label
                if label_counts:
                    best_label = max(label_counts, key=label_counts.get)
                    if labels[entity_id] != best_label:
                        labels[entity_id] = best_label
                        changed = True
            
            if not changed:
                break
        
        return labels
    
    def _generate_community_name(self, entity_ids: Set[str]) -> str:
        """Generate a descriptive name for a community."""
        entities = [self.entities[eid] for eid in entity_ids if eid in self.entities]
        
        if not entities:
            return "Unknown"
        
        # Find common type
        types = [e.entity_type for e in entities]
        common_type = max(set(types), key=types.count)
        
        # Find common path prefix
        names = [e.name for e in entities]
        if len(names) > 1:
            # Find common prefix
            prefix = names[0]
            for name in names[1:]:
                while prefix and not name.startswith(prefix):
                    prefix = prefix[:-1]
            
            if prefix and len(prefix) > 2:
                return f"{prefix}* ({common_type}s)"
        
        # Use first entity name
        return f"{entities[0].name} group"
    
    # =========================================================================
    # Context Retrieval (HiRAG 3-Level)
    # =========================================================================
    
    def get_global_context(self, k: int = 3) -> List[Dict[str, Any]]:
        """
        Get global context: top-k community summaries.
        
        Args:
            k: Number of communities to return
            
        Returns:
            List of community summaries
        """
        if self._dirty:
            self.detect_communities()
        
        # Sort by size (largest first)
        sorted_communities = sorted(
            self.communities.values(),
            key=lambda c: c.size,
            reverse=True
        )[:k]
        
        return [
            {
                "community_id": c.id,
                "name": c.name,
                "size": c.size,
                "summary": c.summary or f"Group of {c.size} related {c.name}",
                "entity_ids": list(c.entity_ids)[:5]  # Sample
            }
            for c in sorted_communities
        ]
    
    def get_local_context(
        self,
        entity_ids: List[str],
        k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get local context: entity descriptions.
        
        Args:
            entity_ids: Entities to retrieve
            k: Maximum entities to return
            
        Returns:
            List of entity details
        """
        results = []
        
        for entity_id in entity_ids[:k]:
            entity = self.entities.get(entity_id)
            if not entity:
                continue
            
            # Get relations
            outgoing = []
            incoming = []
            
            for key, rel in self.relations.items():
                if rel.source_id == entity_id:
                    outgoing.append({
                        "target": rel.target_id,
                        "type": rel.relation_type
                    })
                elif rel.target_id == entity_id:
                    incoming.append({
                        "source": rel.source_id,
                        "type": rel.relation_type
                    })
            
            results.append({
                "id": entity.id,
                "name": entity.name,
                "type": entity.entity_type,
                "description": entity.description,
                "community": self.entity_to_community.get(entity_id),
                "outgoing": outgoing[:5],
                "incoming": incoming[:5]
            })
        
        return results
    
    # =========================================================================
    # Serialization
    # =========================================================================
    
    def to_dict(self) -> dict:
        """Serialize graph to dictionary."""
        return {
            "entities": {
                eid: {
                    "id": e.id,
                    "name": e.name,
                    "entity_type": e.entity_type,
                    "description": e.description,
                    "content_hash": e.content_hash,
                    "metadata": e.metadata
                }
                for eid, e in self.entities.items()
            },
            "relations": [
                {
                    "source_id": r.source_id,
                    "target_id": r.target_id,
                    "relation_type": r.relation_type,
                    "weight": r.weight,
                    "metadata": r.metadata
                }
                for r in self.relations.values()
            ],
            "communities": {
                cid: {
                    "id": c.id,
                    "name": c.name,
                    "entity_ids": list(c.entity_ids),
                    "summary": c.summary,
                    "level": c.level
                }
                for cid, c in self.communities.items()
            }
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "CommunityGraph":
        """Deserialize graph from dictionary."""
        graph = cls()
        
        # Load entities
        for eid, edata in data.get("entities", {}).items():
            graph.add_entity(Entity(
                id=edata["id"],
                name=edata["name"],
                entity_type=edata["entity_type"],
                description=edata.get("description", ""),
                content_hash=edata.get("content_hash", ""),
                metadata=edata.get("metadata", {})
            ))
        
        # Load relations
        for rdata in data.get("relations", []):
            try:
                graph.add_relation(Relation(
                    source_id=rdata["source_id"],
                    target_id=rdata["target_id"],
                    relation_type=rdata["relation_type"],
                    weight=rdata.get("weight", 1.0),
                    metadata=rdata.get("metadata", {})
                ))
            except ValueError:
                continue  # Skip invalid relations
        
        # Load communities
        for cid, cdata in data.get("communities", {}).items():
            graph.communities[cid] = Community(
                id=cdata["id"],
                name=cdata["name"],
                entity_ids=set(cdata.get("entity_ids", [])),
                summary=cdata.get("summary", ""),
                level=cdata.get("level", 0)
            )
            
            for eid in cdata.get("entity_ids", []):
                graph.entity_to_community[eid] = cid
        
        graph._dirty = False
        return graph
    
    def save(self, path: Union[str, Path]) -> None:
        """Save graph to JSON file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, path: Union[str, Path]) -> "CommunityGraph":
        """Load graph from JSON file."""
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    # =========================================================================
    # Stats
    # =========================================================================
    
    @property
    def entity_count(self) -> int:
        return len(self.entities)
    
    @property
    def relation_count(self) -> int:
        return len(self.relations)
    
    @property
    def community_count(self) -> int:
        return len(self.communities)


# =============================================================================
# _DOMYH Awesome Code v6.1.2 • HSA v5.0 • Community Graph_
# =============================================================================
