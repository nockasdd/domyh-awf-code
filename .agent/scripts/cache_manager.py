#!/usr/bin/env python3
"""
DOMYH Awesome Code v4.3 — LRU Cache Manager
Manages session-level skill caching with LRU eviction.

Usage:
    python cache_manager.py --init      # Initialize cache
    python cache_manager.py --status    # Show cache status
    python cache_manager.py --activate go,python  # Activate skills
    python cache_manager.py --clear     # Clear cache
"""

import os
import json
import time
from pathlib import Path
from typing import List, Dict, Optional
from collections import OrderedDict

# Configuration
BASE_PATH = Path(__file__).parent.parent
CACHE_FILE = BASE_PATH / "core" / "session_cache.json"
EMBEDDINGS_FILE = BASE_PATH / "core" / "embeddings.json"
MAX_ACTIVE_SKILLS = 3
CACHE_TTL = 3600  # 1 hour


class LRUCache:
    """LRU Cache for skill management."""
    
    def __init__(self, max_size: int = MAX_ACTIVE_SKILLS):
        self.max_size = max_size
        self.cache: OrderedDict = OrderedDict()
        self.timestamps: Dict[str, float] = {}
    
    def activate(self, skill_id: str) -> Optional[str]:
        """
        Activate a skill. Returns evicted skill if any.
        """
        evicted = None
        
        # If already in cache, move to end (most recently used)
        if skill_id in self.cache:
            self.cache.move_to_end(skill_id)
            self.timestamps[skill_id] = time.time()
            return None
        
        # If cache full, evict LRU
        if len(self.cache) >= self.max_size:
            evicted, _ = self.cache.popitem(last=False)
            del self.timestamps[evicted]
        
        # Add new skill
        self.cache[skill_id] = True
        self.timestamps[skill_id] = time.time()
        
        return evicted
    
    def deactivate(self, skill_id: str) -> bool:
        """Deactivate a skill."""
        if skill_id in self.cache:
            del self.cache[skill_id]
            del self.timestamps[skill_id]
            return True
        return False
    
    def get_active(self) -> List[str]:
        """Get list of active skills in LRU order."""
        return list(self.cache.keys())
    
    def is_active(self, skill_id: str) -> bool:
        """Check if skill is active."""
        return skill_id in self.cache
    
    def touch(self, skill_id: str) -> bool:
        """Touch a skill to mark as recently used."""
        if skill_id in self.cache:
            self.cache.move_to_end(skill_id)
            self.timestamps[skill_id] = time.time()
            return True
        return False
    
    def clear_expired(self, ttl: int = CACHE_TTL) -> List[str]:
        """Clear expired entries."""
        now = time.time()
        expired = []
        for skill_id, ts in list(self.timestamps.items()):
            if now - ts > ttl:
                self.deactivate(skill_id)
                expired.append(skill_id)
        return expired
    
    def to_dict(self) -> Dict:
        """Serialize cache state."""
        return {
            'active': list(self.cache.keys()),
            'timestamps': self.timestamps,
            'max_size': self.max_size
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'LRUCache':
        """Deserialize cache state."""
        cache = cls(max_size=data.get('max_size', MAX_ACTIVE_SKILLS))
        for skill_id in data.get('active', []):
            cache.cache[skill_id] = True
        cache.timestamps = data.get('timestamps', {})
        return cache


def load_cache() -> LRUCache:
    """Load cache from file."""
    if CACHE_FILE.exists():
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return LRUCache.from_dict(data.get('cache', {}))
    return LRUCache()


def save_cache(cache: LRUCache) -> None:
    """Save cache to file."""
    os.makedirs(CACHE_FILE.parent, exist_ok=True)
    data = {
        'version': '4.0.0',
        'cache': cache.to_dict(),
        'updated_at': time.time()
    }
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def get_skill_info(skill_id: str) -> Dict:
    """Get skill info from embeddings."""
    if not EMBEDDINGS_FILE.exists():
        return {'name': skill_id, 'category': 'unknown'}
    
    with open(EMBEDDINGS_FILE, 'r', encoding='utf-8') as f:
        embeddings = json.load(f)
    
    return embeddings.get('skills', {}).get(skill_id, {'name': skill_id, 'category': 'unknown'})


def estimate_tokens(skill_ids: List[str]) -> Dict[str, int]:
    """Estimate token usage for skills."""
    # Token estimates from META.yaml
    meta_tokens = 100  # per skill
    skill_tokens = 1500  # average SKILL.md
    
    baseline = len(skill_ids) * 0  # META loaded separately
    active = len(skill_ids) * skill_tokens
    
    return {
        'baseline': 2100,  # All META.yaml
        'active': active,
        'total': 2100 + active,
        'skills_loaded': len(skill_ids)
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description='DOMYH LRU Cache Manager')
    parser.add_argument('--init', action='store_true', help='Initialize cache')
    parser.add_argument('--status', action='store_true', help='Show cache status')
    parser.add_argument('--activate', type=str, help='Activate skills (comma-separated)')
    parser.add_argument('--deactivate', type=str, help='Deactivate skill')
    parser.add_argument('--clear', action='store_true', help='Clear cache')
    args = parser.parse_args()
    
    cache = load_cache()
    
    if args.init:
        cache = LRUCache()
        save_cache(cache)
        print("✅ Cache initialized")
        print(f"   Max active skills: {cache.max_size}")
        print(f"   TTL: {CACHE_TTL}s")
    
    elif args.status:
        active = cache.get_active()
        print("📊 Cache Status\n")
        
        if not active:
            print("  No active skills")
        else:
            print("  Active skills (LRU order):")
            for i, skill_id in enumerate(active):
                info = get_skill_info(skill_id)
                ts = cache.timestamps.get(skill_id, 0)
                age = time.time() - ts
                print(f"    {i+1}. {skill_id} ({info['name']}) - {age:.0f}s ago")
        
        tokens = estimate_tokens(active)
        print(f"\n  Token usage:")
        print(f"    Baseline (META): {tokens['baseline']}")
        print(f"    Active skills: {tokens['active']}")
        print(f"    Total: {tokens['total']}")
        print(f"\n  Capacity: {len(active)}/{cache.max_size}")
    
    elif args.activate:
        skill_ids = [s.strip() for s in args.activate.split(',')]
        print(f"🔄 Activating: {', '.join(skill_ids)}\n")
        
        for skill_id in skill_ids:
            evicted = cache.activate(skill_id)
            info = get_skill_info(skill_id)
            if evicted:
                evicted_info = get_skill_info(evicted)
                print(f"  ✓ {skill_id} ({info['name']}) - evicted {evicted} ({evicted_info['name']})")
            else:
                print(f"  ✓ {skill_id} ({info['name']})")
        
        save_cache(cache)
        print(f"\n📊 Active: {', '.join(cache.get_active())}")
    
    elif args.deactivate:
        skill_id = args.deactivate
        if cache.deactivate(skill_id):
            save_cache(cache)
            print(f"✓ Deactivated: {skill_id}")
        else:
            print(f"○ Not active: {skill_id}")
    
    elif args.clear:
        cache = LRUCache()
        save_cache(cache)
        print("✅ Cache cleared")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
