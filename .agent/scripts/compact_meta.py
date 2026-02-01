#!/usr/bin/env python3
"""
Compact META.yaml Optimizer
DOMYH Awesome Code v4.3

Reduces META.yaml files to ~100 tokens each:
- Remove comments/headers
- Inline arrays
- Shorten descriptions
- Remove token_estimate fields
"""

import os
import yaml
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent / "skills"

# Target: ~400 bytes = ~100 tokens
TARGET_BYTES = 400

def compact_meta(skill_dir: Path) -> dict:
    """Convert META.yaml to compact format."""
    meta_path = skill_dir / "META.yaml"
    if not meta_path.exists():
        return None
    
    with open(meta_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Extract core fields
    name = data.get('name', skill_dir.name)
    display_name = data.get('display_name', name.title())
    category = data.get('category', 'language')
    priority = data.get('priority', 1)
    
    # Shorten description to ~60 chars
    desc = data.get('description', '')
    if isinstance(desc, str):
        desc = ' '.join(desc.split())[:80]
    
    # Limit keywords to 5
    keywords = data.get('keywords', [])[:5]
    
    # Simplify detection
    detect = data.get('detect', {})
    if isinstance(detect, dict):
        files = detect.get('files', [])[:3]
    else:
        files = data.get('detect_patterns', [])[:3]
    
    # Limit capabilities to 3
    capabilities = data.get('capabilities', [])[:3]
    
    # Build compact structure
    compact = {
        'name': name,
        'display': display_name,
        'category': category,
        'priority': priority,
        'desc': desc,
        'keywords': keywords,
        'detect': files,
        'caps': [c[:40] for c in capabilities]  # Truncate each
    }
    
    return compact

def write_compact_meta(skill_dir: Path, compact: dict) -> int:
    """Write compact META.yaml and return file size."""
    meta_path = skill_dir / "META.yaml"
    
    # Build compact YAML string manually for minimal tokens
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

def main():
    """Optimize all META.yaml files."""
    print("=" * 60)
    print("META.yaml Compact Optimizer")
    print("=" * 60)
    
    results = []
    total_before = 0
    total_after = 0
    
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        if skill_dir.name == '__pycache__':
            continue
            
        meta_path = skill_dir / "META.yaml"
        if not meta_path.exists():
            continue
        
        # Get original size
        original_size = meta_path.stat().st_size
        total_before += original_size
        
        # Compact
        compact = compact_meta(skill_dir)
        if compact:
            new_size = write_compact_meta(skill_dir, compact)
            total_after += new_size
            
            saved = original_size - new_size
            pct = (saved / original_size * 100) if original_size > 0 else 0
            
            results.append({
                'skill': skill_dir.name,
                'before': original_size,
                'after': new_size,
                'saved': saved,
                'pct': pct
            })
            
            status = "✅" if new_size <= TARGET_BYTES else "⚠️"
            print(f"{status} {skill_dir.name:15} {original_size:4}B → {new_size:3}B ({pct:5.1f}% saved)")
    
    print("=" * 60)
    print(f"TOTAL: {total_before:,}B → {total_after:,}B")
    print(f"SAVED: {total_before - total_after:,}B ({(total_before - total_after) / total_before * 100:.1f}%)")
    print(f"TOKEN ESTIMATE: {total_after // 4} tokens (target: 2,200)")
    print("=" * 60)

if __name__ == "__main__":
    main()
