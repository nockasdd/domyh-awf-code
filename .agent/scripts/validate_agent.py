#!/usr/bin/env python3
"""
DOMYH Agent v4.3 — Validation Utility
Validates agent structure, checks for missing files, and verifies configurations.
"""

import json
import os
import sys
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_ok(msg): print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")
def print_err(msg): print(f"{Colors.RED}✗{Colors.RESET} {msg}")
def print_warn(msg): print(f"{Colors.YELLOW}⚠{Colors.RESET} {msg}")
def print_info(msg): print(f"{Colors.BLUE}ℹ{Colors.RESET} {msg}")

# Required structure (v4.3 - modular rules)
REQUIRED_FILES = {
    "core": [
        ".agent/manifest.yaml",
        ".agent/core/ROUTER.yaml",
        ".agent/core/MEMORY_ENGINE.yaml",
    ],
    "rules": [
        ".agent/rules/README.md",
        ".agent/rules/terminal-safety.md",
        ".agent/rules/stop-conditions.md",
        ".agent/rules/evidence.md",
    ],
    "workflows": [
        ".agent/workflows/ap.md",
        ".agent/workflows/code.md",
        ".agent/workflows/debug.md",
        ".agent/workflows/plan.md",
        ".agent/workflows/test.md",
    ],
    "i18n": [
        ".agent/i18n/en.yaml",
        ".agent/i18n/vi.yaml",
    ],
    "skills": [
        ".agent/skills/index.json",
    ],
    "ide": [
        "CLAUDE.md",
        "GEMINI.md",
        "AGENTS.md",
        ".cursorrules",
    ],
}

def validate_structure(base_path: Path) -> tuple[int, int]:
    """Validate agent file structure."""
    ok, err = 0, 0
    
    for category, files in REQUIRED_FILES.items():
        print_info(f"Checking {category}...")
        for f in files:
            path = base_path / f
            if path.exists():
                print_ok(f"  {f}")
                ok += 1
            else:
                print_err(f"  {f} — MISSING")
                err += 1
    
    return ok, err

def validate_skills_index(base_path: Path) -> tuple[int, int]:
    """Validate skills/index.json and referenced skills."""
    ok, err = 0, 0
    index_path = base_path / ".agent/skills/index.json"
    
    if not index_path.exists():
        print_err("skills/index.json not found")
        return 0, 1
    
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        skills = data.get('skills', [])
        print_info(f"Validating {len(skills)} skills...")
        
        for skill in skills:
            skill_path = base_path / ".agent" / skill['path']
            if skill_path.exists():
                print_ok(f"  {skill['id']}")
                ok += 1
            else:
                print_err(f"  {skill['id']} — SKILL.md MISSING")
                err += 1
    except json.JSONDecodeError as e:
        print_err(f"Invalid JSON in skills/index.json: {e}")
        return 0, 1
    
    return ok, err

def validate_manifest(base_path: Path) -> bool:
    """Validate manifest.yaml exists and is parseable."""
    manifest_path = base_path / ".agent/manifest.yaml"
    
    if not manifest_path.exists():
        print_err("manifest.yaml not found")
        return False
    
    try:
        import yaml
        with open(manifest_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if data.get('version'):
            print_ok(f"manifest.yaml — version {data['version']}")
            return True
        else:
            print_warn("manifest.yaml — no version field")
            return True
    except ImportError:
        print_warn("PyYAML not installed, skipping YAML validation")
        return True
    except Exception as e:
        print_err(f"Invalid manifest.yaml: {e}")
        return False

def main():
    """Main validation entry point."""
    print(f"\n{Colors.BLUE}═══════════════════════════════════════════{Colors.RESET}")
    print(f"{Colors.BLUE}  DOMYH Agent v4.3 — Validation Utility{Colors.RESET}")
    print(f"{Colors.BLUE}═══════════════════════════════════════════{Colors.RESET}\n")
    
    # Find base path
    base_path = Path(__file__).parent.parent.parent
    if not (base_path / ".agent").exists():
        base_path = Path.cwd()
    
    print_info(f"Base path: {base_path}\n")
    
    total_ok, total_err = 0, 0
    
    # Structure validation
    ok, err = validate_structure(base_path)
    total_ok += ok
    total_err += err
    print()
    
    # Skills validation
    ok, err = validate_skills_index(base_path)
    total_ok += ok
    total_err += err
    print()
    
    # Manifest validation
    if validate_manifest(base_path):
        total_ok += 1
    else:
        total_err += 1
    print()
    
    # Summary
    print(f"{Colors.BLUE}═══════════════════════════════════════════{Colors.RESET}")
    if total_err == 0:
        print(f"{Colors.GREEN}✓ All {total_ok} checks passed!{Colors.RESET}")
        return 0
    else:
        print(f"{Colors.YELLOW}⚠ {total_ok} passed, {total_err} failed{Colors.RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
