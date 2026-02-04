#!/usr/bin/env python3
"""
DOMYH Awesome Code — Version Synchronization Script v2.0
Syncs version and branding across all agent files from manifest.yaml (single source of truth).

Usage:
    python sync_versions.py              # Preview changes
    python sync_versions.py --apply      # Apply changes
    python sync_versions.py --check      # Check for inconsistencies only
"""

import os
import re
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

@dataclass
class BrandConfig:
    """Brand configuration loaded from manifest.yaml"""
    name: str = "DOMYH Awesome Code"
    version: str = "6.1.2"
    short_version: str = "4.3"
    author: str = "NockDev"
    
    # Legacy names to replace
    legacy_names: Tuple[str, ...] = (
        "DOMYH Awesome Code",
        "Domyh Agent", 
        "domyh agent",
    )

# File patterns to process
FILE_PATTERNS = [
    "**/*.md",
    "**/*.yaml",
    "**/*.yml", 
    "**/*.json",
    "**/*.py",
    "**/*.sh",
    "**/*.ps1",
]

# Directories to skip
SKIP_DIRS = [
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
]

# ═══════════════════════════════════════════════════════════════
# VERSION PATTERNS
# ═══════════════════════════════════════════════════════════════

class VersionPatterns:
    """Regex patterns for version detection and replacement"""
    
    @staticmethod
    def get_patterns(config: BrandConfig) -> List[Tuple[str, str, str]]:
        """
        Returns list of (pattern, replacement, description) tuples.
        Order matters - more specific patterns first.
        """
        name = config.name
        ver = config.short_version
        
        return [
            # Footer patterns (most common)
            (
                r'_DOMYH Awesome Code v[\d.]+',
                f'_{name} v{ver}',
                "Footer version"
            ),
            (
                r'_DOMYH Awesome Code v[\d.]+',
                f'_{name} v{ver}',
                "Footer version (already branded)"
            ),
            
            # Header patterns
            (
                r'# DOMYH Awesome Code v[\d.]+',
                f'# {name} v{ver}',
                "Header version"
            ),
            (
                r'# DOMYH Awesome Code v[\d.]+',
                f'# {name} v{ver}',
                "Header version (already branded)"
            ),
            
            # Inline mentions with version
            (
                r'DOMYH Awesome Code v[\d.]+',
                f'{name} v{ver}',
                "Inline version reference"
            ),
            
            # Title patterns (skill files)
            (
                r'— DOMYH Awesome Code v[\d.]+',
                f'— {name} v{ver}',
                "Title version"
            ),
            (
                r'— DOMYH Awesome Code v[\d.]+',
                f'— {name} v{ver}',
                "Title version (already branded)"
            ),
            
            # Python/script headers
            (
                r'DOMYH Awesome Code — (\w+)',
                f'{name} — \\1',
                "Script header"
            ),
            
            # YAML comments
            (
                r'# DOMYH Awesome Code —',
                f'# {name} —',
                "YAML comment"
            ),
            
            # Generic name replacement (last, catches remaining)
            (
                r'DOMYH Awesome Code(?! Library)',  # Don't match "DOMYH Awesome Code Library" yet
                name,
                "Generic name"
            ),
            
            # Library references
            (
                r'DOMYH Awesome Code Library',
                f'{name} Library',
                "Library name"
            ),
        ]


# ═══════════════════════════════════════════════════════════════
# CORE SYNC ENGINE
# ═══════════════════════════════════════════════════════════════

class VersionSyncEngine:
    """Main synchronization engine"""
    
    def __init__(self, base_path: Path, config: BrandConfig):
        self.base_path = base_path
        self.config = config
        self.patterns = VersionPatterns.get_patterns(config)
        self.changes: List[Dict] = []
        self.errors: List[str] = []
        
    def scan_files(self) -> List[Path]:
        """Find all files to process"""
        files = []
        for pattern in FILE_PATTERNS:
            for file_path in self.base_path.glob(pattern):
                # Skip directories in SKIP_DIRS
                if any(skip in str(file_path) for skip in SKIP_DIRS):
                    continue
                if file_path.is_file():
                    files.append(file_path)
        return sorted(set(files))
    
    def analyze_file(self, file_path: Path) -> List[Dict]:
        """Analyze a single file for version inconsistencies"""
        changes = []
        try:
            content = file_path.read_text(encoding='utf-8')
            
            for pattern, replacement, description in self.patterns:
                matches = list(re.finditer(pattern, content))
                for match in matches:
                    # Check if replacement is different
                    if match.group(0) != re.sub(pattern, replacement, match.group(0)):
                        changes.append({
                            'file': file_path,
                            'line': content[:match.start()].count('\n') + 1,
                            'original': match.group(0),
                            'replacement': re.sub(pattern, replacement, match.group(0)),
                            'description': description,
                        })
        except Exception as e:
            self.errors.append(f"{file_path}: {e}")
        
        return changes
    
    def apply_changes(self, file_path: Path, dry_run: bool = True) -> int:
        """Apply changes to a single file"""
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            for pattern, replacement, _ in self.patterns:
                content = re.sub(pattern, replacement, content)
            
            if content != original_content:
                if not dry_run:
                    file_path.write_text(content, encoding='utf-8')
                return 1
            return 0
        except Exception as e:
            self.errors.append(f"{file_path}: {e}")
            return 0
    
    def run(self, mode: str = 'preview') -> Dict:
        """
        Run synchronization.
        mode: 'preview' | 'apply' | 'check'
        """
        files = self.scan_files()
        total_changes = 0
        files_changed = 0
        
        print(f"\n{'═' * 50}")
        print(f"  {self.config.name} v{self.config.version}")
        print(f"  Version Sync Engine v2.0")
        print(f"{'═' * 50}\n")
        print(f"📂 Base path: {self.base_path}")
        print(f"📄 Files to scan: {len(files)}")
        print(f"🔄 Mode: {mode.upper()}\n")
        
        for file_path in files:
            changes = self.analyze_file(file_path)
            if changes:
                self.changes.extend(changes)
                
                if mode == 'apply':
                    result = self.apply_changes(file_path, dry_run=False)
                    if result:
                        files_changed += 1
                        print(f"✅ {file_path.relative_to(self.base_path)}")
                elif mode == 'preview':
                    files_changed += 1
                    rel_path = file_path.relative_to(self.base_path)
                    print(f"\n📄 {rel_path}")
                    for change in changes:
                        print(f"   L{change['line']:4d}: {change['original']}")
                        print(f"       → {change['replacement']}")
        
        total_changes = len(self.changes)
        
        # Summary
        print(f"\n{'─' * 50}")
        print(f"📊 SUMMARY")
        print(f"{'─' * 50}")
        print(f"   Files scanned:  {len(files)}")
        print(f"   Files affected: {files_changed}")
        print(f"   Total changes:  {total_changes}")
        
        if self.errors:
            print(f"\n⚠️  Errors: {len(self.errors)}")
            for err in self.errors[:5]:
                print(f"   {err}")
        
        if mode == 'preview' and total_changes > 0:
            print(f"\n💡 Run with --apply to apply changes")
        elif mode == 'apply':
            print(f"\n✅ Changes applied successfully!")
        
        return {
            'files_scanned': len(files),
            'files_changed': files_changed,
            'total_changes': total_changes,
            'errors': len(self.errors),
        }


# ═══════════════════════════════════════════════════════════════
# MANIFEST LOADER
# ═══════════════════════════════════════════════════════════════

def load_config_from_manifest(base_path: Path) -> BrandConfig:
    """Load brand configuration from manifest.yaml (single source of truth)"""
    manifest_path = base_path / '.agent' / 'manifest.yaml'
    
    config = BrandConfig()
    
    if manifest_path.exists():
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = yaml.safe_load(f)
            
            # Update from manifest
            config.version = manifest.get('version', config.version)
            config.short_version = '.'.join(config.version.split('.')[:2])
            
            # Name should be updated in manifest first
            if 'name' in manifest:
                config.name = manifest['name']
            
            print(f"📋 Loaded from manifest.yaml:")
            print(f"   Name: {config.name}")
            print(f"   Version: {config.version}")
            
        except Exception as e:
            print(f"⚠️  Could not load manifest: {e}")
            print(f"   Using defaults")
    
    return config


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    # Determine base path
    script_dir = Path(__file__).parent
    base_path = script_dir.parent.parent  # .agent/scripts -> project root
    
    # Check if we're in the right place
    if not (base_path / '.agent').exists():
        # Try current directory
        base_path = Path.cwd()
        if not (base_path / '.agent').exists():
            print("❌ Error: Could not find .agent directory")
            print("   Run this script from the project root or .agent/scripts/")
            sys.exit(1)
    
    # Parse arguments
    mode = 'preview'
    if '--apply' in sys.argv:
        mode = 'apply'
    elif '--check' in sys.argv:
        mode = 'check'
    
    # Load configuration
    config = load_config_from_manifest(base_path)
    
    # Run sync
    engine = VersionSyncEngine(base_path, config)
    result = engine.run(mode)
    
    # Exit code
    if result['errors'] > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
