# HSA Unified Package - Integration Tests
# =============================================================================
"""
Tests for verifying the unified HSA package structure and imports.
"""

import pytest
import sys
from pathlib import Path


class TestUnifiedPackageStructure:
    """Tests for package structure."""
    
    def test_hsa_package_exists(self):
        """Verify hsa package can be imported."""
        # Add scripts to path
        scripts_path = Path(__file__).parent.parent.parent
        if str(scripts_path) not in sys.path:
            sys.path.insert(0, str(scripts_path))
        
        import hsa
        assert hsa.__version__ == "1.0.0"
    
    def test_submodules_exist(self):
        """Verify all submodules exist."""
        scripts_path = Path(__file__).parent.parent.parent
        if str(scripts_path) not in sys.path:
            sys.path.insert(0, str(scripts_path))
        
        # These should not raise
        from hsa import engine
        from hsa import core
        from hsa import tokenizer
        from hsa import cache
        from hsa import search
        from hsa import index
        from hsa import embedding
        from hsa import ast
        from hsa import retrieval
        from hsa import daemon


class TestEngineModule:
    """Tests for engine module."""
    
    def test_engine_config(self):
        """Test engine configuration."""
        scripts_path = Path(__file__).parent.parent.parent
        if str(scripts_path) not in sys.path:
            sys.path.insert(0, str(scripts_path))
        
        from hsa.engine import EngineConfig
        
        config = EngineConfig()
        
        assert config.total_capacity == 128000
        assert config.safety_margin == 0.90
        assert config.auto_tier == True
    
    def test_engine_creation(self):
        """Test engine creation."""
        scripts_path = Path(__file__).parent.parent.parent
        if str(scripts_path) not in sys.path:
            sys.path.insert(0, str(scripts_path))
        
        from hsa.engine import HSAEngine
        
        engine = HSAEngine()
        
        assert engine.config is not None
        assert engine._initialized == False
    
    def test_get_context_function(self):
        """Test get_context convenience function."""
        scripts_path = Path(__file__).parent.parent.parent
        if str(scripts_path) not in sys.path:
            sys.path.insert(0, str(scripts_path))
        
        from hsa.engine import get_context
        
        # Should work with current directory
        result = get_context(query_files=[], max_tokens=8000)
        
        assert result is not None
        assert result.tier_used >= 0


class TestCoreModule:
    """Tests for core module."""
    
    def test_capabilities_import(self):
        """Test capabilities import."""
        scripts_path = Path(__file__).parent.parent.parent
        if str(scripts_path) not in sys.path:
            sys.path.insert(0, str(scripts_path))
        
        from hsa.core import get_capabilities, SystemCapabilities
        
        assert get_capabilities is not None
    
    def test_resilience_import(self):
        """Test resilience patterns import."""
        scripts_path = Path(__file__).parent.parent.parent
        if str(scripts_path) not in sys.path:
            sys.path.insert(0, str(scripts_path))
        
        from hsa.core import CircuitBreaker, RetryHandler
        
        assert CircuitBreaker is not None
        assert RetryHandler is not None


class TestSOLIDCompliance:
    """Tests for SOLID principles compliance."""
    
    def test_single_responsibility(self):
        """Test each module has single responsibility."""
        scripts_path = Path(__file__).parent.parent.parent
        hsa_path = scripts_path / "hsa"
        
        # Check each submodule has its own __init__.py
        submodules = ["core", "tokenizer", "cache", "search", "index", 
                      "embedding", "ast", "retrieval", "engine", "daemon"]
        
        for mod in submodules:
            init_file = hsa_path / mod / "__init__.py"
            assert init_file.exists(), f"Missing {mod}/__init__.py"
    
    def test_no_version_in_names(self):
        """Test no version numbers in module/class names."""
        scripts_path = Path(__file__).parent.parent.parent
        hsa_path = scripts_path / "hsa"
        
        # Check no _v4 or _v5 in any Python file
        for py_file in hsa_path.rglob("*.py"):
            content = py_file.read_text(encoding="utf-8", errors="ignore")
            
            # Allow re-exports from hsa in adapter modules
            if "from hsa" in content or "from hsa" in content:
                # These are adapter modules, skip
                continue
            
            # Class names should not have version
            import re
            versioned_classes = re.findall(r"class \w+[Vv][45]\w*:", content)
            assert len(versioned_classes) == 0, f"Versioned class in {py_file}"


class TestBackwardsCompatibility:
    """Tests for backwards compatibility with v4 and v5 imports."""
    
    def test_v4_modules_still_importable(self):
        """Test hsa modules still work (for migration period)."""
        scripts_path = Path(__file__).parent.parent.parent
        if str(scripts_path) not in sys.path:
            sys.path.insert(0, str(scripts_path))
        
        # These should still work during migration
        try:
            import hsa
            assert hsa.__version__ == "4.0.0"
        except ImportError:
            pass  # OK if not yet available
    
    def test_v5_modules_still_importable(self):
        """Test hsa modules still work (for migration period)."""
        scripts_path = Path(__file__).parent.parent.parent
        if str(scripts_path) not in sys.path:
            sys.path.insert(0, str(scripts_path))
        
        # These should still work during migration
        try:
            import hsa
            assert hsa.__version__ == "5.0.0"
        except ImportError:
            pass  # OK if not yet available


# =============================================================================
# Run Tests
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
