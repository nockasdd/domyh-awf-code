#!/usr/bin/env python3
"""
DOMYH Awesome Code v4.3 — Phase 5 Comprehensive Audit
Checks structure, scripts, configs, and token usage.
"""

import os
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
SKILLS_DIR = BASE_DIR / "skills"
CORE_DIR = BASE_DIR / "core"

class AuditReport:
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.passed = []
    
    def issue(self, msg):
        self.issues.append(msg)
        print(f"  ❌ {msg}")
    
    def warn(self, msg):
        self.warnings.append(msg)
        print(f"  ⚠️  {msg}")
    
    def ok(self, msg):
        self.passed.append(msg)
        print(f"  ✅ {msg}")


def audit_structure(report):
    """Audit 5.1: File structure consistency."""
    print("\n" + "="*60)
    print("📁 5.1 Structure Audit")
    print("="*60)
    
    # Check skills directory
    skill_dirs = [d for d in SKILLS_DIR.iterdir() if d.is_dir()]
    required_files = ["META.yaml", "SKILL.md", "ADVANCED.md"]
    
    for skill_dir in skill_dirs:
        skill_id = skill_dir.name
        missing = []
        sizes = {}
        
        for f in required_files:
            fpath = skill_dir / f
            if fpath.exists():
                sizes[f] = fpath.stat().st_size
            else:
                missing.append(f)
        
        if missing:
            report.warn(f"{skill_id}: missing {', '.join(missing)}")
        else:
            total_bytes = sum(sizes.values())
            report.ok(f"{skill_id}: all files present ({total_bytes} bytes)")
    
    # Check index.json matches filesystem
    index_path = SKILLS_DIR / "index.json"
    with open(index_path, 'r') as f:
        index = json.load(f)
    
    index_skills = {s['id'] for s in index['skills']}
    fs_skills = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir()}
    
    missing_in_index = fs_skills - index_skills
    missing_in_fs = index_skills - fs_skills
    
    if missing_in_index:
        report.issue(f"Skills in filesystem but not in index: {missing_in_index}")
    if missing_in_fs:
        report.issue(f"Skills in index but not in filesystem: {missing_in_fs}")
    if not missing_in_index and not missing_in_fs:
        report.ok(f"Index matches filesystem: {len(index_skills)} skills")


def audit_scripts(report):
    """Audit v5.5: Script functionality."""
    print("\n" + "="*60)
    print("🔧 v5.5 Script Audit")
    print("="*60)
    
    scripts_dir = BASE_DIR / "scripts"
    required_scripts = [
        "semantic_selector.py",
        "cache_manager.py",
        "regenerate_embeddings.py",
        "test_integration.py"
    ]
    
    for script in required_scripts:
        script_path = scripts_dir / script
        if script_path.exists():
            # Check for syntax errors
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                compile(content, script, 'exec')
                report.ok(f"{script}: syntax OK ({script_path.stat().st_size} bytes)")
            except SyntaxError as e:
                report.issue(f"{script}: syntax error at line {e.lineno}")
        else:
            report.issue(f"{script}: not found")


def audit_configs(report):
    """Audit 5.3: Configuration files."""
    print("\n" + "="*60)
    print("⚙️  5.3 Configuration Audit")
    print("="*60)
    
    # Check manifest.yaml
    manifest_path = BASE_DIR / "manifest.yaml"
    if manifest_path.exists():
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = yaml.safe_load(f)
            version = manifest.get('version', 'unknown')
            report.ok(f"manifest.yaml: version {version}")
        except yaml.YAMLError as e:
            report.issue(f"manifest.yaml: YAML error - {e}")
    else:
        report.issue("manifest.yaml: not found")
    
    # Check ROUTER.yaml
    router_path = CORE_DIR / "ROUTER.yaml"
    if router_path.exists():
        try:
            with open(router_path, 'r', encoding='utf-8') as f:
                router = yaml.safe_load(f)
            report.ok(f"ROUTER.yaml: strategy={router.get('strategy', 'unknown')}")
        except yaml.YAMLError as e:
            report.issue(f"ROUTER.yaml: YAML error - {e}")
    else:
        report.issue("ROUTER.yaml: not found")
    
    # Check embeddings.json
    embeddings_path = CORE_DIR / "embeddings.json"
    if embeddings_path.exists():
        with open(embeddings_path, 'r') as f:
            emb = json.load(f)
        skill_count = len(emb.get('skills', {}))
        report.ok(f"embeddings.json: {skill_count} skills indexed")
    else:
        report.issue("embeddings.json: not found")
    
    # Check core markdown files
    core_files = ["RULES.md", "STOP.md", "CACHE.md", "README.md"]
    for cf in core_files:
        path = CORE_DIR / cf
        if path.exists():
            report.ok(f"{cf}: {path.stat().st_size} bytes")
        else:
            report.warn(f"{cf}: not found")


def audit_tokens(report):
    """Audit 5.4: Token estimates vs actual."""
    print("\n" + "="*60)
    print("📊 5.4 Token Audit")
    print("="*60)
    
    # Estimate: 1 token ≈ 4 chars for English text
    CHARS_PER_TOKEN = 4
    
    skill_tokens = {}
    total_t1 = 0
    total_t2 = 0
    total_t3 = 0
    
    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        
        skill_id = skill_dir.name
        tokens = {"t1": 0, "t2": 0, "t3": 0}
        
        meta_path = skill_dir / "META.yaml"
        if meta_path.exists():
            tokens["t1"] = meta_path.stat().st_size // CHARS_PER_TOKEN
            total_t1 += tokens["t1"]
        
        skill_path = skill_dir / "SKILL.md"
        if skill_path.exists():
            tokens["t2"] = skill_path.stat().st_size // CHARS_PER_TOKEN
            total_t2 += tokens["t2"]
        
        adv_path = skill_dir / "ADVANCED.md"
        if adv_path.exists():
            tokens["t3"] = adv_path.stat().st_size // CHARS_PER_TOKEN
            total_t3 += tokens["t3"]
        
        skill_tokens[skill_id] = tokens
    
    # Summary
    print(f"\n  Token Estimates (1 token ≈ {CHARS_PER_TOKEN} chars):")
    print(f"  ─────────────────────────────────────")
    print(f"  T1 (META.yaml) total: {total_t1:,} tokens")
    print(f"  T2 (SKILL.md) total:  {total_t2:,} tokens")
    print(f"  T3 (ADVANCED.md) total: {total_t3:,} tokens")
    print(f"  ─────────────────────────────────────")
    print(f"  Baseline (all T1): {total_t1:,} tokens")
    print(f"  Peak (T1 + 3×T2): {total_t1 + 3*max(t['t2'] for t in skill_tokens.values()):,} tokens")
    
    # Check against estimates
    estimated_t1 = 22 * 100  # 2,200
    if total_t1 < estimated_t1:
        report.ok(f"T1 under budget: {total_t1} < {estimated_t1}")
    else:
        report.warn(f"T1 over budget: {total_t1} > {estimated_t1}")
    
    # Find largest skills
    print("\n  Largest skills by tier:")
    sorted_t2 = sorted(skill_tokens.items(), key=lambda x: -x[1]['t2'])[:5]
    for skill, tokens in sorted_t2:
        print(f"    {skill}: T2={tokens['t2']} T3={tokens['t3']}")


def main():
    print("="*60)
    print("DOMYH Awesome Code v4.3 — Phase 5 Comprehensive Audit")
    print(f"Date: {datetime.now().isoformat()}")
    print("="*60)
    
    report = AuditReport()
    
    audit_structure(report)
    audit_scripts(report)
    audit_configs(report)
    audit_tokens(report)
    
    # Summary
    print("\n" + "="*60)
    print("📋 AUDIT SUMMARY")
    print("="*60)
    print(f"  ✅ Passed: {len(report.passed)}")
    print(f"  ⚠️  Warnings: {len(report.warnings)}")
    print(f"  ❌ Issues: {len(report.issues)}")
    
    if report.issues:
        print("\n  Critical Issues:")
        for issue in report.issues:
            print(f"    - {issue}")
    
    return 0 if not report.issues else 1


if __name__ == "__main__":
    sys.exit(main())
