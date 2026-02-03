#!/usr/bin/env python3
"""
DOMYH Awesome Code v4.3 — Token Tools
Unified tool for META.yaml analysis and optimization.

Usage:
    python token_tools.py --analyze     # Analyze token usage
    python token_tools.py --compact     # Compact META files
    python token_tools.py --template    # Generate template
    python token_tools.py --version     # Show version
"""

import os
import sys
import yaml
import argparse
from pathlib import Path

VERSION = "4.0.0"
BASE_DIR = Path(__file__).parent.parent
SKILLS_DIR = BASE_DIR / "skills"

# Target: ~400 bytes = ~100 tokens
TARGET_BYTES = 400
CHARS_PER_TOKEN = 4


def analyze_meta_files():
    """Analyze all META.yaml files and return results."""
    results = []
    
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name == '__pycache__':
            continue
        
        meta_path = skill_dir / "META.yaml"
        if not meta_path.exists():
            continue
        
        skill_id = skill_dir.name
        size = meta_path.stat().st_size
        tokens = size // CHARS_PER_TOKEN
        
        with open(meta_path, 'r', encoding='utf-8') as f:
            content = yaml.safe_load(f)
        
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
    print("=" * 70)
    print("META.yaml Token Analysis — DOMYH Awesome Code v4.3")
    print("=" * 70)
    print(f"{'Skill':<15} {'Bytes':>8} {'Tokens':>8} {'Over':>8} {'KW':>4} {'Cap':>4}")
    print("-" * 70)
    
    total_bytes = 0
    total_over = 0
    over_count = 0
    
    for r in sorted(results, key=lambda x: -x['size']):
        over = max(0, r['over_target'])
        total_bytes += r['size']
        total_over += over
        if over > 100:
            over_count += 1
        status = "⚠️ " if over > 100 else "  "
        print(f"{status}{r['id']:<13} {r['size']:>8} {r['tokens']:>8} {over:>8} {r['keywords']:>4} {r['capabilities']:>4}")
    
    print("-" * 70)
    print(f"Total: {total_bytes:,} bytes (~{total_bytes//CHARS_PER_TOKEN:,} tokens)")
    print(f"Target: {len(results) * TARGET_BYTES:,} bytes")
    print(f"Over target: {over_count}/{len(results)} skills need optimization")


def compact_meta(skill_dir: Path) -> dict:
    """Convert META.yaml to compact format."""
    meta_path = skill_dir / "META.yaml"
    if not meta_path.exists():
        return None
    
    with open(meta_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    name = data.get('name', skill_dir.name)
    display_name = data.get('display_name', name.title())
    category = data.get('category', 'language')
    priority = data.get('priority', 1)
    
    desc = data.get('description', '')
    if isinstance(desc, str):
        desc = ' '.join(desc.split())[:80]
    
    keywords = data.get('keywords', [])[:5]
    
    detect = data.get('detect', {})
    if isinstance(detect, dict):
        files = detect.get('files', [])[:3]
    else:
        files = data.get('detect_patterns', [])[:3]
    
    capabilities = data.get('capabilities', [])[:3]
    
    return {
        'name': name,
        'display': display_name,
        'category': category,
        'priority': priority,
        'desc': desc,
        'keywords': keywords,
        'detect': files,
        'caps': [c[:40] for c in capabilities]
    }


def write_compact_meta(skill_dir: Path, compact: dict) -> int:
    """Write compact META.yaml and return file size."""
    meta_path = skill_dir / "META.yaml"
    
    lines = [
        f"name: {compact['name']}",
        f"display: {compact['display']}",
        f"category: {compact['category']}",
        f"priority: {compact['priority']}",
        f"desc: \"{compact['desc']}\"",
        f"keywords: {compact['keywords']}",
        f"detect: {compact['detect']}",
        f"caps: {compact['caps']}"
    ]
    
    content = '\n'.join(lines) + '\n'
    
    with open(meta_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return len(content.encode('utf-8'))


def run_compact():
    """Compact all META.yaml files."""
    print("=" * 60)
    print("META.yaml Compact Optimizer — DOMYH Awesome Code v4.3")
    print("=" * 60)
    
    total_before = 0
    total_after = 0
    
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name == '__pycache__':
            continue
        
        meta_path = skill_dir / "META.yaml"
        if not meta_path.exists():
            continue
        
        original_size = meta_path.stat().st_size
        total_before += original_size
        
        compact = compact_meta(skill_dir)
        if compact:
            new_size = write_compact_meta(skill_dir, compact)
            total_after += new_size
            
            saved = original_size - new_size
            pct = (saved / original_size * 100) if original_size > 0 else 0
            
            status = "✅" if new_size <= TARGET_BYTES else "⚠️"
            print(f"{status} {skill_dir.name:15} {original_size:4}B → {new_size:3}B ({pct:5.1f}% saved)")
    
    print("=" * 60)
    print(f"TOTAL: {total_before:,}B → {total_after:,}B")
    print(f"SAVED: {total_before - total_after:,}B ({(total_before - total_after) / total_before * 100:.1f}%)")


def print_template():
    """Print compact META.yaml template."""
    template = '''# {skill_name} — DOMYH v5.5
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
    print("=" * 60)
    print("Compact META.yaml Template")
    print("=" * 60)
    print(template)


def main():
    parser = argparse.ArgumentParser(
        description='DOMYH Awesome Code Token Tools v5.5',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--analyze', '-a', action='store_true', help='Analyze token usage')
    parser.add_argument('--compact', '-c', action='store_true', help='Compact all META files')
    parser.add_argument('--template', '-t', action='store_true', help='Show template')
    parser.add_argument('--version', '-v', action='store_true', help='Show version')
    
    args = parser.parse_args()
    
    if args.version:
        print(f"DOMYH Token Tools v{VERSION}")
        return 0
    
    if args.compact:
        run_compact()
        return 0
    
    if args.template:
        print_template()
        return 0
    
    if args.analyze or len(sys.argv) == 1:
        results = analyze_meta_files()
        print_analysis(results)
        return 0
    
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
