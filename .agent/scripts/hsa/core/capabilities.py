# HSA v5.0 - System Capabilities Detection
# =============================================================================
"""
Auto-detect system capabilities for progressive enhancement.

Phase 1.1: Detects:
- RAM size
- GPU availability (CUDA, MPS)
- VRAM size
- OS type

Used to select optimal configuration without user input.
"""

from __future__ import annotations

import logging
import platform
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

logger = logging.getLogger("hsa.capabilities")


@dataclass
class GPUInfo:
    """GPU information."""
    available: bool = False
    name: Optional[str] = None
    vram_gb: Optional[float] = None
    driver_version: Optional[str] = None
    compute_capability: Optional[Tuple[int, int]] = None
    
    @property
    def is_cuda(self) -> bool:
        """Check if CUDA GPU."""
        return self.available and self.name is not None and "NVIDIA" in (self.name or "").upper()
    
    @property
    def is_mps(self) -> bool:
        """Check if Apple MPS."""
        return self.available and self.name == "Apple MPS"
    
    @property
    def can_use_int8(self) -> bool:
        """Check if INT8 quantization is recommended (VRAM < 12GB)."""
        if self.vram_gb is None:
            return True  # Default to INT8 (safer)
        return self.vram_gb < 12
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "available": self.available,
            "name": self.name,
            "vram_gb": self.vram_gb,
            "driver_version": self.driver_version,
            "is_cuda": self.is_cuda,
            "is_mps": self.is_mps,
        }


@dataclass
class SystemCapabilities:
    """
    Detected system capabilities.
    
    Usage:
        caps = SystemCapabilities.detect()
        print(f"RAM: {caps.ram_gb:.1f}GB")
        print(f"GPU: {caps.gpu.name if caps.gpu.available else 'None'}")
        
        config_name, config = caps.recommend_config()
        print(f"Recommended: {config_name}")
    """
    
    ram_gb: float
    os_type: str  # "windows", "darwin", "linux"
    os_version: str
    python_version: str
    cpu_count: int
    gpu: GPUInfo
    
    @classmethod
    def detect(cls) -> "SystemCapabilities":
        """
        Detect all system capabilities.
        
        Returns:
            SystemCapabilities with all detected info
        """
        import sys
        
        # RAM detection
        ram_gb = cls._detect_ram()
        
        # OS detection
        os_type = platform.system().lower()
        if os_type == "darwin":
            os_type = "macos"
        os_version = platform.release()
        
        # Python version
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        
        # CPU count
        try:
            import os
            cpu_count = os.cpu_count() or 1
        except:
            cpu_count = 1
        
        # GPU detection
        gpu = cls._detect_gpu()
        
        caps = cls(
            ram_gb=ram_gb,
            os_type=os_type,
            os_version=os_version,
            python_version=python_version,
            cpu_count=cpu_count,
            gpu=gpu
        )
        
        caps.log_summary()
        return caps
    
    @staticmethod
    def _detect_ram() -> float:
        """Detect available RAM in GB."""
        try:
            import psutil
            return psutil.virtual_memory().total / 1e9
        except ImportError:
            logger.warning("psutil not installed, assuming 8GB RAM")
            return 8.0
    
    @staticmethod
    def _detect_gpu() -> GPUInfo:
        """Detect GPU availability and specs."""
        try:
            import torch
            
            # CUDA detection
            if torch.cuda.is_available():
                props = torch.cuda.get_device_properties(0)
                return GPUInfo(
                    available=True,
                    name=props.name,
                    vram_gb=props.total_memory / 1e9,
                    driver_version=torch._C._cuda_getDriverVersion() if hasattr(torch._C, '_cuda_getDriverVersion') else None,
                    compute_capability=(props.major, props.minor)
                )
            
            # MPS detection (Apple Silicon)
            if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                return GPUInfo(
                    available=True,
                    name="Apple MPS",
                    vram_gb=None,  # MPS uses shared memory
                )
            
        except ImportError:
            logger.debug("PyTorch not installed, GPU detection skipped")
        except Exception as e:
            logger.debug(f"GPU detection error: {e}")
        
        return GPUInfo(available=False)
    
    def recommend_config(self) -> Tuple[str, Dict[str, Any]]:
        """
        Recommend optimal configuration based on capabilities.
        
        Returns:
            Tuple of (config_name, config_dict)
        """
        if self.gpu.available and self.gpu.vram_gb and self.gpu.vram_gb >= 12:
            # High-end GPU
            return "gpu_large", {
                "model": "codesage-v2-large",
                "precision": "fp16",
                "batch_size": 32,
                "use_gpu": True,
                "description": "High-end GPU with 12GB+ VRAM"
            }
        elif self.gpu.available:
            # GPU with limited VRAM (or MPS)
            return "gpu_int8", {
                "model": "codesage-v2-large",
                "precision": "int8",
                "batch_size": 16,
                "use_gpu": True,
                "description": "GPU with INT8 quantization"
            }
        elif self.ram_gb >= 16:
            # No GPU but good RAM
            return "cpu_large", {
                "model": "codesage-v2-base",
                "precision": "fp32",
                "batch_size": 8,
                "use_gpu": False,
                "description": "CPU with 16GB+ RAM"
            }
        else:
            # Limited resources
            return "cpu_minimal", {
                "model": "bm25_only",
                "precision": None,
                "batch_size": 4,
                "use_gpu": False,
                "description": "CPU with limited RAM"
            }
    
    def get_memory_budgets(self) -> Dict[str, int]:
        """
        Get recommended memory budgets based on available RAM.
        
        Returns:
            Dict with memory budgets in MB
        """
        if self.ram_gb >= 32:
            return {
                "embedding_cache_mb": 2048,
                "vector_index_mb": 4096,
                "max_concurrent_files": 500
            }
        elif self.ram_gb >= 16:
            return {
                "embedding_cache_mb": 1024,
                "vector_index_mb": 2048,
                "max_concurrent_files": 200
            }
        elif self.ram_gb >= 8:
            return {
                "embedding_cache_mb": 512,
                "vector_index_mb": 1024,
                "max_concurrent_files": 100
            }
        else:
            return {
                "embedding_cache_mb": 256,
                "vector_index_mb": 512,
                "max_concurrent_files": 50
            }
    
    def log_summary(self) -> None:
        """Log detection summary."""
        logger.info(f"System: {self.os_type} {self.os_version}, Python {self.python_version}")
        logger.info(f"RAM: {self.ram_gb:.1f}GB, CPUs: {self.cpu_count}")
        
        if self.gpu.available:
            if self.gpu.vram_gb:
                logger.info(f"GPU: {self.gpu.name} ({self.gpu.vram_gb:.1f}GB VRAM)")
            else:
                logger.info(f"GPU: {self.gpu.name} (shared memory)")
        else:
            logger.info("GPU: Not detected (using CPU)")
        
        config_name, _ = self.recommend_config()
        logger.info(f"Recommended config: {config_name}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "ram_gb": self.ram_gb,
            "os_type": self.os_type,
            "os_version": self.os_version,
            "python_version": self.python_version,
            "cpu_count": self.cpu_count,
            "gpu": self.gpu.to_dict(),
            "recommended_config": self.recommend_config()[0],
            "memory_budgets": self.get_memory_budgets()
        }


# Global cached capabilities
_cached_capabilities: Optional[SystemCapabilities] = None


def get_capabilities() -> SystemCapabilities:
    """
    Get cached system capabilities.
    
    Detects on first call, returns cached on subsequent calls.
    """
    global _cached_capabilities
    if _cached_capabilities is None:
        _cached_capabilities = SystemCapabilities.detect()
    return _cached_capabilities


def refresh_capabilities() -> SystemCapabilities:
    """Force re-detection of capabilities."""
    global _cached_capabilities
    _cached_capabilities = SystemCapabilities.detect()
    return _cached_capabilities
