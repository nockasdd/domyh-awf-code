#!/usr/bin/env python3
"""
DOMYH Agent v4.0 — Token Optimizer
Analyzes and optimizes META.yaml files for token reduction.
"""

import os
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
SKILLS_DIR = BASE_DIR / "skills"

# Target token count per META.yaml (4 chars = 1 token)
TARGET_BYTES = 400  # ~100 tokens
CHARS_PER_TOKEN = 4


def analyze_meta_files():
    """Analyze all META.yaml files."""
    results = []
    
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        
        meta_path = skill_dir / "META.yaml"
        if not meta_path.exists():
            continue
        
        skill_id = skill_dir.name
        size = meta_path.stat().st_size
        tokens = size // CHARS_PER_TOKEN
        
        with open(meta_path, 'r', encoding='utf-8') as f:
            content = yaml.safe_load(f)
        
        # Count fields
        keywords = len(content.get('keywords', []))
        capabilities = len(content.get('capabilities', []))
        desc_len = len(content.get('description', ''))
        
        results.append({
            'id': skill_id,
            'size': size,
            'tokens': tokens,
            'keywords': keywords,
            'capabilities': capabilities,
            'desc_len': desc_len,
            'over_target': size - TARGET_BYTES
        })
    
    return results


def print_analysis(results):
    """Print analysis report."""
    print("="*70)
    print("META.yaml Token Analysis")
    print("="*70)
    print(f"{'Skill':<15} {'Bytes':>8} {'Tokens':>8} {'Over':>8} {'KW':>4} {'Cap':>4}")
    print("-"*70)
    
    total_bytes = 0
    total_over = 0
    
    for r in sorted(results, key=lambda x: -x['size']):
        over = max(0, r['over_target'])
        total_bytes += r['size']
        total_over += over
        status = "⚠️ " if over > 100 else "  "
        print(f"{status}{r['id']:<13} {r['size']:>8} {r['tokens']:>8} {over:>8} {r['keywords']:>4} {r['capabilities']:>4}")
    
    print("-"*70)
    print(f"Total: {total_bytes} bytes (~{total_bytes//CHARS_PER_TOKEN} tokens)")
    print(f"Target: {len(results) * TARGET_BYTES} bytes (~{len(results) * (TARGET_BYTES//CHARS_PER_TOKEN)} tokens)")
    print(f"Excess: {total_over} bytes (~{total_over//CHARS_PER_TOKEN} tokens)")


def generate_compact_template():
    """Generate compact META.yaml template."""
    template = '''# {skill_name} — DOMYH v4.0
name: {id}
display_name: {display}
category: {category}
priority: {priority}

# Keep description under 60 chars
description: {short_description}

# Max 5-7 keywords
keywords: [{keywords}]

# Max 3-4 capabilities  
capabilities: [{capabilities}]

# File detection
detect: [{patterns}]
'''
    return template


def suggest_optimizations(results):
    """Suggest specific optimizations."""
    print("\n" + "="*70)
    print("Optimization Suggestions")
    print("="*70)
    
    for r in sorted(results, key=lambda x: -x['over_target'])[:5]:
        if r['over_target'] <= 0:
            continue
        
        print(f"\n📝 {r['id']} (excess: {r['over_target']} bytes)")
        
        if r['keywords'] > 7:
            print(f"   - Reduce keywords from {r['keywords']} to ≤7")
        if r['capabilities'] > 4:
            print(f"   - Reduce capabilities from {r['capabilities']} to ≤4")
        if r['desc_len'] > 100:
            print(f"   - Shorten description from {r['desc_len']} to ≤100 chars")
        
        print(f"   - Remove comments and blank lines")
        print(f"   - Use inline arrays instead of list format")


def main():
    results = analyze_meta_files()
    print_analysis(results)
    suggest_optimizations(results)
    
    print("\n" + "="*70)
    print("Compact Template")
    print("="*70)
    print(generate_compact_template())


if __name__ == "__main__":
    main()
