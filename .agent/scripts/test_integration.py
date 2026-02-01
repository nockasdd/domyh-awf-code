#!/usr/bin/env python3
"""
Integration tests for DOMYH Agent v4.0 Semantic Selector
Tests the semantic selection and caching functionality.
"""

import sys
import json
import os
from pathlib import Path

# Add scripts to path
AGENT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(AGENT_DIR / "scripts"))

from semantic_selector import SemanticSelector
from cache_manager import SkillCache

def test_semantic_selection():
    """Test semantic skill selection accuracy."""
    print("\n🧪 Testing Semantic Selection...")
    
    selector = SemanticSelector(str(AGENT_DIR))
    
    test_cases = [
        # (query, expected_skill, min_score)
        ("how to handle errors in golang", "go", 0.3),
        ("react hooks state management", "react", 0.5),
        ("docker container deployment", "docker", 0.4),
        ("postgresql query optimization", "database", 0.3),
        ("kubernetes pod scaling", "kubernetes", 0.4),
        ("typescript type inference", "typescript", 0.4),
        ("python async await patterns", "python", 0.4),
        ("assembly x86 registers", "asm", 0.3),
        ("SQL injection prevention", "security", 0.3),
        ("unit testing mock patterns", "testing", 0.3),
    ]
    
    passed = 0
    failed = 0
    
    for query, expected, min_score in test_cases:
        results = selector.select(query, top_k=5)
        
        if results and len(results) > 0:
            top_skill = results[0][0]
            top_score = results[0][1]
            
            # Check if expected skill is in top 3
            top_3_skills = [r[0] for r in results[:3]]
            
            if expected in top_3_skills:
                print(f"  ✅ '{query[:40]}...' → {top_skill} ({top_score:.3f})")
                passed += 1
            else:
                print(f"  ❌ '{query[:40]}...' → Expected {expected}, got {top_3_skills}")
                failed += 1
        else:
            print(f"  ❌ '{query[:40]}...' → No results")
            failed += 1
    
    print(f"\n  Results: {passed}/{passed+failed} passed")
    return failed == 0


def test_cache_management():
    """Test LRU cache functionality."""
    print("\n🧪 Testing Cache Management...")
    
    cache = SkillCache(str(AGENT_DIR), max_skills=3)
    
    # Test activation
    cache.activate("go")
    cache.activate("react")
    cache.activate("python")
    
    assert len(cache.get_active()) == 3, "Should have 3 active skills"
    print("  ✅ Basic activation works")
    
    # Test LRU eviction
    cache.activate("docker")  # Should evict oldest (go)
    active = cache.get_active()
    
    assert "docker" in active, "docker should be active"
    assert len(active) == 3, "Should still have 3 skills"
    print("  ✅ LRU eviction works")
    
    # Test MRU update
    cache.activate("react")  # Re-activate react (move to front)
    cache.activate("typescript")  # Should evict oldest non-react
    active = cache.get_active()
    
    assert "react" in active, "react should still be active (MRU)"
    assert "typescript" in active, "typescript should be active"
    print("  ✅ MRU update works")
    
    # Cleanup
    cache.save()
    print("\n  All cache tests passed!")
    return True


def test_embedding_generation():
    """Test embedding file exists and has correct format."""
    print("\n🧪 Testing Embeddings...")
    
    embeddings_path = AGENT_DIR / "core" / "embeddings.json"
    
    if not embeddings_path.exists():
        print("  ❌ embeddings.json not found")
        return False
    
    with open(embeddings_path, 'r') as f:
        data = json.load(f)
    
    # Check structure
    assert "created" in data, "Missing 'created' field"
    assert "skills" in data, "Missing 'skills' field"
    print(f"  ✅ Embeddings created: {data.get('created', 'unknown')}")
    
    # Check all skills have embeddings
    skills_dir = AGENT_DIR / "skills"
    skill_ids = [d.name for d in skills_dir.iterdir() if d.is_dir() and (d / "META.yaml").exists()]
    
    missing = []
    for skill_id in skill_ids:
        if skill_id not in data["skills"]:
            missing.append(skill_id)
    
    if missing:
        print(f"  ⚠️  Missing embeddings for: {missing}")
        return False
    
    print(f"  ✅ All {len(skill_ids)} skills have embeddings")
    return True


def test_skill_files():
    """Test all skills have required files."""
    print("\n🧪 Testing Skill Files...")
    
    skills_dir = AGENT_DIR / "skills"
    required_files = ["META.yaml", "SKILL.md"]
    optional_files = ["ADVANCED.md"]
    
    errors = []
    warnings = []
    
    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue
        
        skill_id = skill_dir.name
        
        # Check required files
        for f in required_files:
            if not (skill_dir / f).exists():
                errors.append(f"{skill_id}: missing {f}")
        
        # Check optional (ADVANCED.md)
        for f in optional_files:
            if not (skill_dir / f).exists():
                warnings.append(f"{skill_id}: missing {f}")
    
    if errors:
        for e in errors:
            print(f"  ❌ {e}")
        return False
    
    for w in warnings:
        print(f"  ⚠️  {w}")
    
    skill_count = len([d for d in skills_dir.iterdir() if d.is_dir() and (d / "META.yaml").exists()])
    print(f"  ✅ All {skill_count} skills have required files")
    return True


def main():
    """Run all integration tests."""
    print("=" * 60)
    print("DOMYH Agent v4.0 — Integration Tests")
    print("=" * 60)
    
    results = []
    
    results.append(("Skill Files", test_skill_files()))
    results.append(("Embeddings", test_embedding_generation()))
    results.append(("Semantic Selection", test_semantic_selection()))
    results.append(("Cache Management", test_cache_management()))
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {name}")
        if not passed:
            all_passed = False
    
    print("\n" + ("🎉 All tests passed!" if all_passed else "❌ Some tests failed"))
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
