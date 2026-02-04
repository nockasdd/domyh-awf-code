# HSA v5.0 - GPU Utilities
# =============================================================================
"""
GPU utilities for Tier 1 acceleration.

Features:
- GPU memory management
- Batch optimization
- Fallback chains
- Memory profiling
"""

from __future__ import annotations

import gc
import logging
import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, TypeVar

logger = logging.getLogger("hsa.gpu")

T = TypeVar("T")


@dataclass
class MemoryStats:
    """GPU/CPU memory statistics."""
    used_mb: float = 0
    total_mb: float = 0
    free_mb: float = 0
    peak_mb: float = 0
    
    @property
    def usage_percent(self) -> float:
        if self.total_mb == 0:
            return 0
        return (self.used_mb / self.total_mb) * 100


@dataclass
class MemoryBudget:
    """Memory budget configuration."""
    max_gpu_mb: int = 4096
    max_cpu_mb: int = 4096
    gc_threshold_percent: float = 80.0
    warning_threshold_percent: float = 70.0


class GPUMemoryManager:
    """
    GPU memory management with automatic GC.
    
    Usage:
        manager = GPUMemoryManager()
        
        # Check before allocation
        if manager.can_allocate(512):
            # Allocate 512MB
            ...
        
        # Force cleanup
        manager.cleanup()
    """
    
    def __init__(self, budget: Optional[MemoryBudget] = None):
        self.budget = budget or MemoryBudget()
        self._lock = threading.Lock()
        self._peak_usage = 0
        self._allocation_count = 0
        
        # Check GPU availability
        self._has_cuda = self._check_cuda()
        self._has_mps = self._check_mps()
        
        if self._has_cuda:
            logger.info("CUDA GPU detected for memory management")
        elif self._has_mps:
            logger.info("Apple MPS detected for memory management")
        else:
            logger.info("No GPU detected, using CPU memory management")
    
    @staticmethod
    def _check_cuda() -> bool:
        try:
            import torch
            return torch.cuda.is_available()
        except:
            return False
    
    @staticmethod
    def _check_mps() -> bool:
        try:
            import torch
            return hasattr(torch.backends, 'mps') and torch.backends.mps.is_available()
        except:
            return False
    
    def get_stats(self) -> MemoryStats:
        """Get current memory statistics."""
        if self._has_cuda:
            return self._get_cuda_stats()
        elif self._has_mps:
            return self._get_mps_stats()
        else:
            return self._get_cpu_stats()
    
    def _get_cuda_stats(self) -> MemoryStats:
        """Get CUDA memory stats."""
        try:
            import torch
            
            allocated = torch.cuda.memory_allocated() / 1e6
            reserved = torch.cuda.memory_reserved() / 1e6
            total = torch.cuda.get_device_properties(0).total_memory / 1e6
            
            return MemoryStats(
                used_mb=allocated,
                total_mb=total,
                free_mb=total - allocated,
                peak_mb=max(self._peak_usage, allocated)
            )
        except Exception as e:
            logger.warning(f"Failed to get CUDA stats: {e}")
            return MemoryStats()
    
    def _get_mps_stats(self) -> MemoryStats:
        """Get Apple MPS memory stats (limited info)."""
        try:
            import torch
            
            # MPS doesn't have detailed memory tracking like CUDA
            # Use system memory as approximation
            import psutil
            mem = psutil.virtual_memory()
            
            return MemoryStats(
                used_mb=mem.used / 1e6,
                total_mb=mem.total / 1e6,
                free_mb=mem.available / 1e6,
                peak_mb=self._peak_usage
            )
        except Exception as e:
            return MemoryStats()
    
    def _get_cpu_stats(self) -> MemoryStats:
        """Get CPU memory stats."""
        try:
            import psutil
            
            process = psutil.Process()
            mem_info = process.memory_info()
            sys_mem = psutil.virtual_memory()
            
            return MemoryStats(
                used_mb=mem_info.rss / 1e6,
                total_mb=sys_mem.total / 1e6,
                free_mb=sys_mem.available / 1e6,
                peak_mb=self._peak_usage
            )
        except:
            return MemoryStats()
    
    def can_allocate(self, size_mb: float) -> bool:
        """Check if allocation is possible within budget."""
        stats = self.get_stats()
        
        if self._has_cuda:
            return (stats.used_mb + size_mb) < self.budget.max_gpu_mb
        else:
            return (stats.used_mb + size_mb) < self.budget.max_cpu_mb
    
    def should_gc(self) -> bool:
        """Check if garbage collection should run."""
        stats = self.get_stats()
        return stats.usage_percent > self.budget.gc_threshold_percent
    
    def cleanup(self, force: bool = False) -> None:
        """Clean up memory."""
        with self._lock:
            if self._has_cuda:
                self._cleanup_cuda(force)
            elif self._has_mps:
                self._cleanup_mps(force)
            
            # Python GC
            gc.collect()
    
    def _cleanup_cuda(self, force: bool) -> None:
        """Clean up CUDA memory."""
        try:
            import torch
            
            torch.cuda.empty_cache()
            
            if force:
                torch.cuda.synchronize()
                torch.cuda.reset_peak_memory_stats()
            
            logger.debug("CUDA memory cleaned")
        except Exception as e:
            logger.warning(f"CUDA cleanup failed: {e}")
    
    def _cleanup_mps(self, force: bool) -> None:
        """Clean up MPS memory."""
        try:
            import torch
            
            if hasattr(torch.mps, 'empty_cache'):
                torch.mps.empty_cache()
            
            logger.debug("MPS memory cleaned")
        except Exception as e:
            logger.warning(f"MPS cleanup failed: {e}")
    
    @contextmanager
    def memory_guard(self, size_mb: float):
        """
        Context manager for guarded memory allocation.
        
        Usage:
            with manager.memory_guard(512):
                # Allocate tensor
                tensor = torch.zeros(...)
        """
        if not self.can_allocate(size_mb):
            self.cleanup()
            
            if not self.can_allocate(size_mb):
                raise MemoryError(f"Cannot allocate {size_mb}MB, insufficient memory")
        
        self._allocation_count += 1
        try:
            yield
        finally:
            # Check if cleanup needed
            if self.should_gc():
                self.cleanup()


class FallbackChain:
    """
    Fallback chain for graceful degradation.
    
    Usage:
        chain = FallbackChain()
        chain.add("gpu_large", lambda: gpu_embed(text), required_vram=12000)
        chain.add("gpu_int8", lambda: gpu_embed_int8(text), required_vram=6000)
        chain.add("cpu", lambda: cpu_embed(text))
        
        result = chain.execute()
    """
    
    @dataclass
    class Step:
        name: str
        func: Callable
        required_vram_mb: float = 0
        required_ram_mb: float = 0
        
    def __init__(self, memory_manager: Optional[GPUMemoryManager] = None):
        self._steps: List[FallbackChain.Step] = []
        self._memory_manager = memory_manager or GPUMemoryManager()
        self._last_used: Optional[str] = None
        self._fallback_count = 0
    
    def add(
        self, 
        name: str, 
        func: Callable, 
        required_vram_mb: float = 0,
        required_ram_mb: float = 0
    ) -> "FallbackChain":
        """Add a step to the chain."""
        self._steps.append(self.Step(
            name=name,
            func=func,
            required_vram_mb=required_vram_mb,
            required_ram_mb=required_ram_mb
        ))
        return self
    
    def execute(self, *args, **kwargs) -> Any:
        """
        Execute chain, falling back on failure.
        
        Returns result from first successful step.
        Raises RuntimeError if all steps fail.
        """
        errors = []
        
        for step in self._steps:
            # Check memory requirements
            if step.required_vram_mb > 0:
                if not self._memory_manager.can_allocate(step.required_vram_mb):
                    logger.debug(f"Skipping {step.name}: insufficient VRAM")
                    continue
            
            try:
                logger.debug(f"Trying {step.name}...")
                result = step.func(*args, **kwargs)
                
                self._last_used = step.name
                logger.debug(f"Success with {step.name}")
                return result
                
            except MemoryError as e:
                logger.warning(f"{step.name} OOM: {e}")
                self._memory_manager.cleanup(force=True)
                errors.append((step.name, e))
                self._fallback_count += 1
                
            except Exception as e:
                logger.warning(f"{step.name} failed: {e}")
                errors.append((step.name, e))
                self._fallback_count += 1
        
        # All steps failed
        error_msg = "; ".join(f"{name}: {err}" for name, err in errors)
        raise RuntimeError(f"All fallback steps failed: {error_msg}")
    
    @property
    def last_used(self) -> Optional[str]:
        return self._last_used
    
    @property
    def fallback_count(self) -> int:
        return self._fallback_count


class BatchProcessor:
    """
    Optimized batch processor for GPU.
    
    Features:
    - Dynamic batch sizing based on memory
    - Async queue for background processing
    - Progress reporting
    
    Usage:
        processor = BatchProcessor(batch_size=32)
        
        results = processor.process(items, embed_func)
    """
    
    def __init__(
        self,
        batch_size: int = 16,
        max_batch_size: int = 64,
        memory_manager: Optional[GPUMemoryManager] = None
    ):
        self.batch_size = batch_size
        self.max_batch_size = max_batch_size
        self._memory_manager = memory_manager or GPUMemoryManager()
        self._processed = 0
        self._total_time = 0.0
    
    def process(
        self, 
        items: List[T], 
        func: Callable[[List[T]], List[Any]],
        on_progress: Optional[Callable[[int, int], None]] = None
    ) -> List[Any]:
        """
        Process items in optimized batches.
        
        Args:
            items: Items to process
            func: Function that takes a batch and returns results
            on_progress: Optional progress callback(done, total)
            
        Returns:
            List of results
        """
        if not items:
            return []
        
        results = []
        total = len(items)
        batch_size = self._get_optimal_batch_size()
        
        for i in range(0, total, batch_size):
            batch = items[i:i + batch_size]
            
            start = time.time()
            try:
                batch_results = func(batch)
                results.extend(batch_results)
            except MemoryError:
                # Reduce batch size and retry
                logger.warning("OOM, reducing batch size")
                self._memory_manager.cleanup(force=True)
                batch_size = max(1, batch_size // 2)
                
                # Retry with smaller batch
                for j in range(0, len(batch), batch_size):
                    mini_batch = batch[j:j + batch_size]
                    batch_results = func(mini_batch)
                    results.extend(batch_results)
            
            self._total_time += time.time() - start
            self._processed += len(batch)
            
            if on_progress:
                on_progress(len(results), total)
        
        return results
    
    def _get_optimal_batch_size(self) -> int:
        """Determine optimal batch size based on memory."""
        stats = self._memory_manager.get_stats()
        
        # If memory pressure is high, reduce batch size
        if stats.usage_percent > 70:
            return max(1, self.batch_size // 2)
        elif stats.usage_percent < 30:
            return min(self.max_batch_size, self.batch_size * 2)
        
        return self.batch_size
    
    @property
    def avg_time_per_item(self) -> float:
        """Average processing time per item."""
        if self._processed == 0:
            return 0
        return self._total_time / self._processed


class MemoryProfiler:
    """
    Memory profiler for detecting leaks.
    
    Usage:
        profiler = MemoryProfiler()
        
        with profiler.track("embedding"):
            # Do work
            ...
        
        profiler.report()
    """
    
    @dataclass
    class Snapshot:
        name: str
        start_mb: float
        end_mb: float
        peak_mb: float
        duration_s: float
        
        @property
        def delta_mb(self) -> float:
            return self.end_mb - self.start_mb
    
    def __init__(self, memory_manager: Optional[GPUMemoryManager] = None):
        self._memory_manager = memory_manager or GPUMemoryManager()
        self._snapshots: List[MemoryProfiler.Snapshot] = []
        self._baseline_mb: Optional[float] = None
    
    @contextmanager
    def track(self, name: str):
        """Track memory usage for a block."""
        stats_before = self._memory_manager.get_stats()
        start_time = time.time()
        peak_mb = stats_before.used_mb
        
        try:
            yield
        finally:
            stats_after = self._memory_manager.get_stats()
            duration = time.time() - start_time
            
            snapshot = self.Snapshot(
                name=name,
                start_mb=stats_before.used_mb,
                end_mb=stats_after.used_mb,
                peak_mb=max(peak_mb, stats_after.peak_mb),
                duration_s=duration
            )
            self._snapshots.append(snapshot)
    
    def set_baseline(self) -> None:
        """Set current memory as baseline."""
        stats = self._memory_manager.get_stats()
        self._baseline_mb = stats.used_mb
    
    def check_leak(self, threshold_mb: float = 100) -> bool:
        """Check if there's a potential memory leak."""
        if self._baseline_mb is None:
            return False
        
        stats = self._memory_manager.get_stats()
        delta = stats.used_mb - self._baseline_mb
        
        return delta > threshold_mb
    
    def report(self) -> Dict[str, Any]:
        """Generate profiling report."""
        if not self._snapshots:
            return {"snapshots": [], "total_delta_mb": 0}
        
        total_delta = sum(s.delta_mb for s in self._snapshots)
        
        return {
            "snapshots": [
                {
                    "name": s.name,
                    "start_mb": round(s.start_mb, 2),
                    "end_mb": round(s.end_mb, 2),
                    "delta_mb": round(s.delta_mb, 2),
                    "peak_mb": round(s.peak_mb, 2),
                    "duration_s": round(s.duration_s, 3)
                }
                for s in self._snapshots
            ],
            "total_delta_mb": round(total_delta, 2),
            "potential_leak": self.check_leak()
        }
    
    def clear(self) -> None:
        """Clear snapshots."""
        self._snapshots.clear()


# Global instances
_memory_manager: Optional[GPUMemoryManager] = None


def get_memory_manager() -> GPUMemoryManager:
    """Get global memory manager."""
    global _memory_manager
    if _memory_manager is None:
        _memory_manager = GPUMemoryManager()
    return _memory_manager
