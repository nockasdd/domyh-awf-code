#!/usr/bin/env python3
"""
DOMYH Agent - Version Synchronization Script v1.0
Updates all version strings to target version (4.3.0)
"""

import os
import re
import json
from pathlib import Path

TARGET_VERSION = "4.3.0"
TARGET_VERSION_SHORT = "4.3"

BASE_DIR = Path(__file__).parent.parent  # .agent directory

# Files to update with their patterns
UPDATE_PATTERNS = [
    # YAML frontmatter: version: "X.X" or version: "X.X.X"
    {
        "glob": "**/*.yaml",
        "pattern": r'^(version:\s*["\'])[\d.]+(["\'])',
        "replacement": rf'\g<1>{TARGET_VERSION}\g<2>',
        "line_range": (1, 20)  # Only check first 20 lines
    },
    {
        "glob": "skills/**/SKILL.md",
        "pattern": r'^(version:\s*["\'])[\d.]+(["\'])',
        "replacement": rf'\g<1>{TARGET_VERSION_SHORT}\g<2>',
        "line_range": (1, 20)
    },
    {
        "glob": "templates/*.md",
        "pattern": r'^(version:\s*["\'])[\d.]+(["\'])',
        "replacement": rf'\g<1>{TARGET_VERSION}\g<2>',
        "line_range": (1, 20)
    },
    {
        "glob": "personas/README.md",
        "pattern": r'^(version:\s*["\'])[\d.]+(["\'])',
        "replacement": rf'\g<1>{TARGET_VERSION}\g<2>',
        "line_range": (1, 50)
    },
]

# JSON files
JSON_FILES = [
    "skills/index.json",
    "core/embeddings.json",
    "core/session_cache.json",
]

def update_yaml_version(file_path: Path, pattern: str, replacement: str, line_range: tuple) -> bool:
    """Update version in YAML/MD file frontmatter."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        modified = False
        start, end = line_range
        
        for i in range(min(start - 1, 0), min(end, len(lines))):
            if re.match(pattern, lines[i], re.MULTILINE):
                new_line = re.sub(pattern, replacement, lines[i])
                if new_line != lines[i]:
                    lines[i] = new_line
                    modified = True
                    break
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return True
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def update_json_version(file_path: Path) -> bool:
    """Update version in JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'version' in data and data['version'] != TARGET_VERSION:
            data['version'] = TARGET_VERSION
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    print(f"🔄 DOMYH Version Sync → {TARGET_VERSION}")
    print("=" * 50)
    
    updated = 0
    skipped = 0
    errors = 0
    
    # Update YAML/MD files
    for config in UPDATE_PATTERNS:
        print(f"\n📁 Pattern: {config['glob']}")
        for file_path in BASE_DIR.glob(config['glob']):
            relative = file_path.relative_to(BASE_DIR)
            result = update_yaml_version(
                file_path, 
                config['pattern'], 
                config['replacement'],
                config['line_range']
            )
            if result:
                print(f"  ✅ {relative}")
                updated += 1
            else:
                skipped += 1
    
    # Update JSON files
    print(f"\n📁 JSON Files")
    for json_file in JSON_FILES:
        file_path = BASE_DIR / json_file
        if file_path.exists():
            result = update_json_version(file_path)
            if result:
                print(f"  ✅ {json_file}")
                updated += 1
            else:
                skipped += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Summary: {updated} updated, {skipped} skipped, {errors} errors")
    print(f"✅ All versions synchronized to {TARGET_VERSION}")

if __name__ == "__main__":
    main()
