#!/usr/bin/env python3
"""
Auto-regenerate embeddings when skills change.
DOMYH Agent v4.0

Usage:
    python regenerate_embeddings.py              # Manual run
    python regenerate_embeddings.py --watch      # Watch mode (daemon)
    python regenerate_embeddings.py --check      # Check if regeneration needed
"""

import sys
import json
import hashlib
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# Configuration
AGENT_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = Path(__file__).parent


def get_skills_hash() -> str:
    """Calculate hash of all skill META.yaml files."""
    skills_dir = AGENT_DIR / "skills"
    hasher = hashlib.md5()
    
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        
        meta_file = skill_dir / "META.yaml"
        if meta_file.exists():
            content = meta_file.read_bytes()
            hasher.update(content)
    
    return hasher.hexdigest()


def get_stored_hash() -> str:
    """Get previously stored skills hash."""
    hash_file = AGENT_DIR / "core" / ".skills_hash"
    if hash_file.exists():
        return hash_file.read_text().strip()
    return ""


def save_hash(hash_value: str):
    """Save skills hash for future comparison."""
    hash_file = AGENT_DIR / "core" / ".skills_hash"
    hash_file.write_text(hash_value)


def needs_regeneration() -> bool:
    """Check if embeddings need regeneration."""
    current_hash = get_skills_hash()
    stored_hash = get_stored_hash()
    
    # Also check if embeddings.json exists
    embeddings_path = AGENT_DIR / "core" / "embeddings.json"
    if not embeddings_path.exists():
        return True
    
    return current_hash != stored_hash


def regenerate_embeddings():
    """Regenerate all skill embeddings."""
    print(f"🔄 Regenerating embeddings...")
    print(f"   Time: {datetime.now().isoformat()}")
    
    # Run semantic_selector.py --generate
    selector_script = SCRIPTS_DIR / "semantic_selector.py"
    result = subprocess.run(
        [sys.executable, str(selector_script), "--generate"],
        cwd=str(AGENT_DIR),
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        return False
    
    print(result.stdout)
    
    # Save new hash
    new_hash = get_skills_hash()
    save_hash(new_hash)
    
    # Count skills
    embeddings_path = AGENT_DIR / "core" / "embeddings.json"
    with open(embeddings_path, 'r') as f:
        data = json.load(f)
    
    skill_count = len(data.get("skills", {}))
    print(f"✅ Regenerated embeddings for {skill_count} skills")
    print(f"   Hash: {new_hash[:12]}...")
    return True


def watch_mode():
    """Watch for changes and auto-regenerate."""
    import time
    
    print("👀 Watch mode enabled. Monitoring skill changes...")
    print("   Press Ctrl+C to exit\n")
    
    last_hash = get_stored_hash()
    
    try:
        while True:
            current_hash = get_skills_hash()
            
            if current_hash != last_hash:
                print(f"\n📝 Skills changed detected!")
                regenerate_embeddings()
                last_hash = current_hash
            
            time.sleep(5)  # Check every 5 seconds
            
    except KeyboardInterrupt:
        print("\n👋 Watch mode stopped")


def main():
    parser = argparse.ArgumentParser(
        description="Auto-regenerate skill embeddings"
    )
    parser.add_argument(
        "--watch", "-w",
        action="store_true",
        help="Watch mode: monitor for changes and auto-regenerate"
    )
    parser.add_argument(
        "--check", "-c",
        action="store_true",
        help="Check if regeneration needed (exit code 0=no, 1=yes)"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force regeneration even if not needed"
    )
    
    args = parser.parse_args()
    
    if args.check:
        if needs_regeneration():
            print("⚠️  Embeddings need regeneration")
            return 1
        else:
            print("✅ Embeddings are up to date")
            return 0
    
    if args.watch:
        watch_mode()
        return 0
    
    # Normal run
    if args.force or needs_regeneration():
        regenerate_embeddings()
    else:
        print("✅ Embeddings are up to date")
        print("   Use --force to regenerate anyway")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
