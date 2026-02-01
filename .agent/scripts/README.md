# 🔧 Scripts — DOMYH Awesome Code v4.3

> Utility scripts for agent management and optimization

---

## 🚀 Installation Scripts

| Script        | Platform    | Usage            |
| ------------- | ----------- | ---------------- |
| `install.sh`  | Linux/macOS | `./install.sh`   |
| `install.ps1` | Windows     | `.\\install.ps1` |

### Quick Install

```bash
# Linux/macOS
./install.sh

# Windows PowerShell (Run as Administrator if needed)
.\install.ps1

# Direct options
./install.sh --all        # Install to all detected IDEs
./install.sh --project    # Install to current project only
.\install.ps1 -Lang vi -All  # Vietnamese, install all
```

---

## 🛠️ Utility Scripts

| Script                     | Purpose                   | Usage                                    |
| -------------------------- | ------------------------- | ---------------------------------------- |
| `validate_agent.py`        | Validate agent structure  | `python validate_agent.py [-v]`          |
| `semantic_selector.py`     | Generate/test embeddings  | `python semantic_selector.py --generate` |
| `cache_manager.py`         | Manage skill cache        | `python cache_manager.py --status`       |
| `token_tools.py`           | Token optimization        | `python token_tools.py --analyze`        |
| `compact_meta.py`          | Compact META.yaml files   | `python compact_meta.py`                 |
| `optimize_tokens.py`       | Optimize token usage      | `python optimize_tokens.py`              |
| `regenerate_embeddings.py` | Regenerate all embeddings | `python regenerate_embeddings.py`        |
| `sync_versions.py`         | Sync version numbers      | `python sync_versions.py`                |
| `audit_phase5.py`          | Audit Phase 5 (memory)    | `python audit_phase5.py`                 |
| `test_integration.py`      | Integration tests         | `python test_integration.py`             |

---

## 📦 Quick Commands

```bash
# Validate agent structure
python .agent/scripts/validate_agent.py

# Regenerate skill embeddings (after adding new skills)
python .agent/scripts/semantic_selector.py --generate

# Check cache status
python .agent/scripts/cache_manager.py --status

# Analyze token usage
python .agent/scripts/token_tools.py --analyze

# Sync all version numbers
python .agent/scripts/sync_versions.py
```

---

## 📖 Script Details

### validate_agent.py

Validates agent file structure, skills index, and manifest integrity.

```bash
python scripts/validate_agent.py        # Standard check
python scripts/validate_agent.py -v     # Verbose output
python scripts/validate_agent.py --fix  # Auto-fix issues
```

### semantic_selector.py

Generates TF-IDF embeddings for semantic skill selection.

```bash
python scripts/semantic_selector.py --generate       # Generate embeddings
python scripts/semantic_selector.py --query "go api" # Test skill matching
python scripts/semantic_selector.py --top 5          # Show top 5 matches
```

### cache_manager.py

Manages LRU cache for skill activation (performance optimization).

```bash
python scripts/cache_manager.py --init           # Initialize cache
python scripts/cache_manager.py --status         # Show cache status
python scripts/cache_manager.py --activate go    # Activate specific skill
python scripts/cache_manager.py --clear          # Clear all cache
python scripts/cache_manager.py --stats          # Show hit/miss stats
```

### token_tools.py

Analyzes and optimizes token usage across skills and rules.

```bash
python scripts/token_tools.py --analyze          # Analyze all files
python scripts/token_tools.py --report           # Generate report
python scripts/token_tools.py --optimize skills  # Optimize skills
```

---

## ⚠️ Troubleshooting

### Script không chạy được

```bash
# Kiểm tra Python version (cần 3.8+)
python --version

# Cài đặt dependencies nếu cần
pip install pyyaml tiktoken

# Quyền thực thi (Linux/macOS)
chmod +x .agent/scripts/*.sh
```

### IDE không được phát hiện

1. Đảm bảo IDE đã được cài đặt và có thư mục config
2. Chạy script với quyền Administrator (Windows) hoặc sudo (Linux)
3. Kiểm tra đường dẫn trong script có đúng với hệ thống không

---

_DOMYH Awesome Code v4.3 • Scripts v2.0.0_
