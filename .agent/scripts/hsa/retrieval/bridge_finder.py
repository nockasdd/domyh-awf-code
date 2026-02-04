# =============================================================================
# bridge_finder.py — Cross-Community Bridge Detection
# =============================================================================
# HSA v5.0 - Phase 3: HiRAG Integration
# Finds shortest paths between communities for bridge context
# =============================================================================

"""
Bridge Finder Module

Implements bridge context retrieval from HiRAG research.
Bridges are entities that connect different communities.

Key insight: Bridge entities provide the "glue" between
isolated knowledge clusters, enabling coherent reasoning
across the codebase.
"""

from __future__ import annotations

import heapq
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from .community_graph import CommunityGraph, Entity


@dataclass
class Bridge:
    """Represents a bridge path between two entities."""
    source_id: str
    target_id: str
    path: List[str]  # Entity IDs in path
    distance: float
    bridge_entities: List[str]  # Entities connecting communities
    
    @property
    def length(self) -> int:
        return len(self.path)


@dataclass
class BridgeContext:
    """Context derived from bridge entities."""
    bridges: List[Bridge]
    bridge_entity_ids: Set[str]
    total_distance: float
    
    def to_dict(self) -> dict:
        return {
            "bridges": [
                {
                    "source": b.source_id,
                    "target": b.target_id,
                    "path": b.path,
                    "distance": b.distance,
                    "bridge_entities": b.bridge_entities
                }
                for b in self.bridges
            ],
            "unique_bridge_entities": list(self.bridge_entity_ids),
            "total_distance": self.total_distance
        }


class BridgeFinder:
    """
    Finds bridge entities connecting different communities.
    
    Architecture (from HiRAG research):
    1. Given a query, identify relevant entities
    2. Find communities those entities belong to
    3. Compute shortest paths between communities
    4. Extract bridge entities from paths
    
    Usage:
        finder = BridgeFinder(graph)
        
        # Find bridges between two entities
        bridge = finder.find_bridge("entity_a", "entity_b")
        
        # Get bridge context for multiple entities
        context = finder.get_bridge_context(["entity_a", "entity_b", "entity_c"])
    """
    
    def __init__(self, graph: CommunityGraph):
        """
        Initialize the bridge finder.
        
        Args:
            graph: CommunityGraph instance
        """
        self.graph = graph
        
        # Cache for shortest paths
        self._path_cache: Dict[Tuple[str, str], Optional[Bridge]] = {}
    
    def find_bridge(
        self,
        source_id: str,
        target_id: str,
        max_distance: float = float('inf')
    ) -> Optional[Bridge]:
        """
        Find the shortest path bridge between two entities.
        
        Uses Dijkstra's algorithm with edge weights.
        
        Args:
            source_id: Starting entity
            target_id: Destination entity
            max_distance: Maximum path distance
            
        Returns:
            Bridge object or None if no path exists
        """
        cache_key = (source_id, target_id)
        if cache_key in self._path_cache:
            return self._path_cache[cache_key]
        
        if source_id not in self.graph.entities:
            return None
        if target_id not in self.graph.entities:
            return None
        
        # Dijkstra's algorithm
        distances: Dict[str, float] = {source_id: 0}
        previous: Dict[str, Optional[str]] = {source_id: None}
        visited: Set[str] = set()
        
        # Priority queue: (distance, entity_id)
        heap = [(0.0, source_id)]
        
        while heap:
            current_dist, current_id = heapq.heappop(heap)
            
            if current_id in visited:
                continue
            
            if current_id == target_id:
                break
            
            if current_dist > max_distance:
                break
            
            visited.add(current_id)
            
            # Explore neighbors
            neighbors = self.graph.get_neighbors(current_id)
            
            for neighbor_id in neighbors:
                if neighbor_id in visited:
                    continue
                
                # Get edge weight
                weight = self._get_edge_weight(current_id, neighbor_id)
                new_dist = current_dist + weight
                
                if new_dist < distances.get(neighbor_id, float('inf')):
                    distances[neighbor_id] = new_dist
                    previous[neighbor_id] = current_id
                    heapq.heappush(heap, (new_dist, neighbor_id))
        
        # Reconstruct path
        if target_id not in distances:
            self._path_cache[cache_key] = None
            return None
        
        path = []
        current = target_id
        while current is not None:
            path.append(current)
            current = previous.get(current)
        path.reverse()
        
        # Find bridge entities (those connecting different communities)
        bridge_entities = self._find_bridge_entities(path)
        
        bridge = Bridge(
            source_id=source_id,
            target_id=target_id,
            path=path,
            distance=distances[target_id],
            bridge_entities=bridge_entities
        )
        
        self._path_cache[cache_key] = bridge
        return bridge
    
    def get_bridge_context(
        self,
        entity_ids: List[str],
        max_bridges: int = 3
    ) -> BridgeContext:
        """
        Get bridge context connecting multiple entities.
        
        Args:
            entity_ids: Entities to connect
            max_bridges: Maximum number of bridges to find
            
        Returns:
            BridgeContext with bridges and unique bridge entities
        """
        if len(entity_ids) < 2:
            return BridgeContext(
                bridges=[],
                bridge_entity_ids=set(),
                total_distance=0.0
            )
        
        bridges: List[Bridge] = []
        all_bridge_entities: Set[str] = set()
        total_distance = 0.0
        
        # Find bridges between consecutive entities
        seen_pairs: Set[Tuple[str, str]] = set()
        
        # First, connect consecutive entities
        for i in range(len(entity_ids) - 1):
            if len(bridges) >= max_bridges:
                break
            
            source = entity_ids[i]
            target = entity_ids[i + 1]
            
            pair = tuple(sorted([source, target]))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            
            bridge = self.find_bridge(source, target)
            if bridge:
                bridges.append(bridge)
                all_bridge_entities.update(bridge.bridge_entities)
                total_distance += bridge.distance
        
        # If we have capacity, also try to connect first and last
        if len(bridges) < max_bridges and len(entity_ids) > 2:
            source = entity_ids[0]
            target = entity_ids[-1]
            
            pair = tuple(sorted([source, target]))
            if pair not in seen_pairs:
                bridge = self.find_bridge(source, target)
                if bridge:
                    bridges.append(bridge)
                    all_bridge_entities.update(bridge.bridge_entities)
                    total_distance += bridge.distance
        
        return BridgeContext(
            bridges=bridges,
            bridge_entity_ids=all_bridge_entities,
            total_distance=total_distance
        )
    
    def find_cross_community_bridges(
        self,
        community_a: str,
        community_b: str,
        max_bridges: int = 3
    ) -> List[Bridge]:
        """
        Find bridges between two communities.
        
        Args:
            community_a: First community ID
            community_b: Second community ID
            max_bridges: Maximum bridges to find
            
        Returns:
            List of bridges connecting the communities
        """
        comm_a = self.graph.communities.get(community_a)
        comm_b = self.graph.communities.get(community_b)
        
        if not comm_a or not comm_b:
            return []
        
        bridges: List[Bridge] = []
        
        # Sample entities from each community
        sample_a = list(comm_a.entity_ids)[:5]
        sample_b = list(comm_b.entity_ids)[:5]
        
        for source in sample_a:
            if len(bridges) >= max_bridges:
                break
            
            for target in sample_b:
                if len(bridges) >= max_bridges:
                    break
                
                bridge = self.find_bridge(source, target)
                if bridge and bridge.length > 1:
                    bridges.append(bridge)
        
        # Sort by distance
        bridges.sort(key=lambda b: b.distance)
        return bridges[:max_bridges]
    
    def clear_cache(self) -> None:
        """Clear the path cache."""
        self._path_cache.clear()
    
    def _get_edge_weight(self, source_id: str, target_id: str) -> float:
        """Get the weight of an edge (lower = stronger connection)."""
        # Check for direct relation
        for rel_type in ["imports", "calls", "extends", "tests", "types"]:
            key = (source_id, target_id, rel_type)
            if key in self.graph.relations:
                # Invert weight (higher relation weight = lower distance)
                return 1.0 / self.graph.relations[key].weight
            
            # Check reverse
            key = (target_id, source_id, rel_type)
            if key in self.graph.relations:
                return 1.0 / self.graph.relations[key].weight
        
        return 1.0  # Default weight
    
    def _find_bridge_entities(self, path: List[str]) -> List[str]:
        """
        Find entities in path that bridge different communities.
        
        A bridge entity is one whose neighbors belong to
        different communities than itself.
        """
        bridge_entities = []
        
        for i, entity_id in enumerate(path):
            entity_comm = self.graph.entity_to_community.get(entity_id)
            
            # Check if it connects different communities
            is_bridge = False
            
            # Check previous in path
            if i > 0:
                prev_comm = self.graph.entity_to_community.get(path[i - 1])
                if prev_comm and prev_comm != entity_comm:
                    is_bridge = True
            
            # Check next in path
            if i < len(path) - 1:
                next_comm = self.graph.entity_to_community.get(path[i + 1])
                if next_comm and next_comm != entity_comm:
                    is_bridge = True
            
            if is_bridge:
                bridge_entities.append(entity_id)
        
        return bridge_entities


# =============================================================================
# Convenience Functions
# =============================================================================

def find_bridges_between(
    graph: CommunityGraph,
    source_ids: List[str],
    target_ids: List[str],
    max_bridges: int = 3
) -> List[Bridge]:
    """
    Find bridges between two sets of entities.
    
    Args:
        graph: CommunityGraph instance
        source_ids: Source entities
        target_ids: Target entities
        max_bridges: Maximum bridges to find
        
    Returns:
        List of bridges
    """
    finder = BridgeFinder(graph)
    bridges = []
    
    for source in source_ids[:3]:
        for target in target_ids[:3]:
            if len(bridges) >= max_bridges:
                break
            
            bridge = finder.find_bridge(source, target)
            if bridge:
                bridges.append(bridge)
        
        if len(bridges) >= max_bridges:
            break
    
    return bridges[:max_bridges]


# =============================================================================
# _DOMYH Awesome Code v6.1.2 • HSA v5.0 • Bridge Finder_
# =============================================================================
