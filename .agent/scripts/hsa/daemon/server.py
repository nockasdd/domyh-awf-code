# HSA v5.0 - Python Daemon Server
# =============================================================================
"""
Standalone Python daemon for HSA v5.0.

Features:
- msgpack IPC protocol over Unix socket / TCP
- Graceful shutdown (SIGTERM/SIGINT)
- Health check endpoint
- Structured logging with rotation
- Request routing to HSA components

Protocol:
    Request:  {"method": "...", "params": {...}, "id": 1}
    Response: {"result": {...}, "id": 1} or {"error": {...}, "id": 1}
"""

from __future__ import annotations

import asyncio
import logging
import os
import signal
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger("hsa.daemon")


@dataclass
class DaemonConfig:
    """Daemon configuration."""
    host: str = "127.0.0.1"
    port: int = 9527
    socket_path: Optional[str] = None  # Use Unix socket if specified
    max_connections: int = 10
    request_timeout: float = 30.0
    shutdown_timeout: float = 5.0
    log_level: str = "INFO"
    log_file: Optional[str] = None
    log_max_bytes: int = 10 * 1024 * 1024  # 10MB
    log_backup_count: int = 5
    
    @classmethod
    def from_env(cls) -> "DaemonConfig":
        """Create config from environment variables."""
        return cls(
            host=os.getenv("HSA_DAEMON_HOST", "127.0.0.1"),
            port=int(os.getenv("HSA_DAEMON_PORT", "9527")),
            socket_path=os.getenv("HSA_DAEMON_SOCKET"),
            max_connections=int(os.getenv("HSA_MAX_CONNECTIONS", "10")),
            request_timeout=float(os.getenv("HSA_REQUEST_TIMEOUT", "30")),
            log_level=os.getenv("HSA_LOG_LEVEL", "INFO"),
            log_file=os.getenv("HSA_LOG_FILE"),
        )


@dataclass
class Request:
    """IPC request."""
    method: str
    params: Dict[str, Any] = field(default_factory=dict)
    id: Optional[int] = None


@dataclass
class Response:
    """IPC response."""
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        if self.error:
            return {"error": self.error, "id": self.id}
        return {"result": self.result, "id": self.id}


class RequestHandler:
    """Handles incoming requests by routing to appropriate handlers."""
    
    def __init__(self):
        self._handlers: Dict[str, Callable] = {}
        self._start_time = time.time()
        self._request_count = 0
        
        # Register built-in handlers
        self._register_builtins()
    
    def _register_builtins(self) -> None:
        """Register built-in handlers."""
        self.register("health", self._handle_health)
        self.register("ping", self._handle_ping)
        self.register("status", self._handle_status)
        self.register("shutdown", self._handle_shutdown)
        
        # HSA methods
        self.register("get_context", self._handle_get_context)
        self.register("search", self._handle_search)
        self.register("embed", self._handle_embed)
        self.register("parse", self._handle_parse)
        self.register("count_tokens", self._handle_count_tokens)
    
    def register(self, method: str, handler: Callable) -> None:
        """Register a method handler."""
        self._handlers[method] = handler
        logger.debug(f"Registered handler: {method}")
    
    async def handle(self, request: Request) -> Response:
        """Handle a request."""
        self._request_count += 1
        
        handler = self._handlers.get(request.method)
        if handler is None:
            return Response(
                error={"code": -32601, "message": f"Method not found: {request.method}"},
                id=request.id
            )
        
        try:
            if asyncio.iscoroutinefunction(handler):
                result = await handler(request.params)
            else:
                result = handler(request.params)
            
            return Response(result=result, id=request.id)
            
        except Exception as e:
            logger.exception(f"Handler error for {request.method}")
            return Response(
                error={"code": -32000, "message": str(e)},
                id=request.id
            )
    
    # === Built-in Handlers ===
    
    def _handle_health(self, params: Dict) -> Dict:
        """Health check."""
        return {
            "status": "healthy",
            "uptime_seconds": time.time() - self._start_time,
            "version": "5.0.0"
        }
    
    def _handle_ping(self, params: Dict) -> str:
        """Simple ping."""
        return "pong"
    
    def _handle_status(self, params: Dict) -> Dict:
        """Daemon status."""
        from ..core import get_config, get_capabilities
        
        config = get_config()
        caps = get_capabilities()
        
        return {
            "uptime_seconds": time.time() - self._start_time,
            "request_count": self._request_count,
            "tier": config.get_tier().name,
            "tier_name": config.get_tier_name(),
            "gpu_available": caps.gpu.available,
            "ram_gb": caps.ram_gb,
            "embedding_model": config.get_embedding_model(),
            "vector_store": config.get_vector_store(),
        }
    
    def _handle_shutdown(self, params: Dict) -> Dict:
        """Request graceful shutdown."""
        logger.info("Shutdown requested via IPC")
        # Signal main loop to shutdown
        asyncio.get_event_loop().call_soon(lambda: os.kill(os.getpid(), signal.SIGTERM))
        return {"status": "shutting_down"}
    
    # === HSA Handlers ===
    
    async def _handle_get_context(self, params: Dict) -> Dict:
        """Get context for files."""
        from ..search import get_index
        from ..embedding import get_embedder
        
        query = params.get("query", "")
        files = params.get("files", [])
        max_tokens = params.get("max_tokens", 8000)
        
        # Combine BM25 + vector search
        bm25_results = get_index().search(query, k=10)
        
        # Get embeddings if available
        try:
            embedder = get_embedder()
            query_vec = embedder.embed_single(query)
            
            from ..index import get_store
            vector_results = get_store().search(query_vec, k=10)
        except Exception:
            vector_results = []
        
        return {
            "bm25_results": [{"doc_id": r.doc_id, "score": r.score} for r in bm25_results],
            "vector_results": [{"doc_id": r.doc_id, "score": r.score} for r in vector_results],
            "query": query,
            "max_tokens": max_tokens,
        }
    
    async def _handle_search(self, params: Dict) -> Dict:
        """Search codebase."""
        from ..search import get_index
        
        query = params.get("query", "")
        k = params.get("k", 10)
        
        results = get_index().search(query, k=k, include_content=True)
        
        return {
            "results": [
                {"doc_id": r.doc_id, "score": r.score, "content": r.content[:500] if r.content else None}
                for r in results
            ],
            "total": len(results)
        }
    
    async def _handle_embed(self, params: Dict) -> Dict:
        """Generate embeddings."""
        from ..embedding import get_embedder
        
        texts = params.get("texts", [])
        if isinstance(texts, str):
            texts = [texts]
        
        embedder = get_embedder()
        vectors = embedder.embed(texts)
        
        return {
            "vectors": vectors,
            "dimension": embedder.get_dimension(),
            "model": embedder.get_active_embedder(),
        }
    
    async def _handle_parse(self, params: Dict) -> Dict:
        """Parse source file."""
        from ..ast import parse_file
        
        file_path = params.get("file_path", "")
        content = params.get("content")
        
        result = parse_file(file_path, content)
        
        return {
            "language": result.language,
            "entities": [e.to_dict() for e in result.entities],
            "imports": result.imports[:20],  # Limit imports
            "exports": result.exports[:20],
            "parse_time_ms": result.parse_time_ms,
        }
    
    def _handle_count_tokens(self, params: Dict) -> Dict:
        """Count tokens in text."""
        from ..tokenizer import count_tokens, AccurateTokenCounter
        
        text = params.get("text", "")
        model = params.get("model", "cl100k_base")
        
        counter = AccurateTokenCounter(model=model)
        count = counter.count(text)
        stats = counter.get_stats()
        
        return {
            "count": count,
            "model": model,
            "cache_hit_rate": stats.get("hit_rate", 0),
        }


class HSADaemon:
    """
    HSA v5.0 Daemon Server.
    
    Usage:
        daemon = HSADaemon()
        await daemon.start()
    
    Or from command line:
        python -m hsa.daemon
    """
    
    def __init__(self, config: Optional[DaemonConfig] = None):
        self.config = config or DaemonConfig.from_env()
        self.handler = RequestHandler()
        self._server: Optional[asyncio.AbstractServer] = None
        self._shutdown_event = asyncio.Event()
        self._connections: List[asyncio.Task] = []
        
        self._setup_logging()
        self._setup_signals()
    
    def _setup_logging(self) -> None:
        """Setup logging with optional rotation."""
        import logging.handlers
        
        log_level = getattr(logging, self.config.log_level.upper(), logging.INFO)
        
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # Root logger for HSA
        hsa_logger = logging.getLogger("hsa")
        hsa_logger.setLevel(log_level)
        hsa_logger.addHandler(console_handler)
        
        # File handler with rotation
        if self.config.log_file:
            file_handler = logging.handlers.RotatingFileHandler(
                self.config.log_file,
                maxBytes=self.config.log_max_bytes,
                backupCount=self.config.log_backup_count
            )
            file_handler.setFormatter(formatter)
            hsa_logger.addHandler(file_handler)
    
    def _setup_signals(self) -> None:
        """Setup signal handlers for graceful shutdown."""
        if sys.platform != "win32":
            loop = asyncio.get_event_loop()
            for sig in (signal.SIGTERM, signal.SIGINT):
                loop.add_signal_handler(sig, self._signal_handler, sig)
        else:
            # Windows doesn't support add_signal_handler
            signal.signal(signal.SIGTERM, lambda s, f: self._signal_handler(s))
            signal.signal(signal.SIGINT, lambda s, f: self._signal_handler(s))
    
    def _signal_handler(self, sig: signal.Signals) -> None:
        """Handle shutdown signals."""
        logger.info(f"Received signal {sig.name}, initiating shutdown...")
        self._shutdown_event.set()
    
    async def start(self) -> None:
        """Start the daemon server."""
        try:
            import msgpack
        except ImportError:
            raise ImportError("msgpack not installed. Install with: pip install msgpack")
        
        logger.info(f"Starting HSA v5.0 Daemon on {self.config.host}:{self.config.port}")
        
        # Log system info
        from ..core import get_config, get_capabilities
        config = get_config()
        caps = get_capabilities()
        
        logger.info(f"System: {caps.os_type}, RAM: {caps.ram_gb:.1f}GB, GPU: {caps.gpu.name if caps.gpu.available else 'None'}")
        logger.info(f"Tier: {config.get_tier_name()}")
        
        # Start server
        if self.config.socket_path:
            # Unix socket
            self._server = await asyncio.start_unix_server(
                self._handle_connection,
                path=self.config.socket_path
            )
            logger.info(f"Listening on Unix socket: {self.config.socket_path}")
        else:
            # TCP
            self._server = await asyncio.start_server(
                self._handle_connection,
                self.config.host,
                self.config.port
            )
            logger.info(f"Listening on TCP: {self.config.host}:{self.config.port}")
        
        # Wait for shutdown
        await self._shutdown_event.wait()
        
        # Graceful shutdown
        await self._shutdown()
    
    async def _handle_connection(
        self, 
        reader: asyncio.StreamReader, 
        writer: asyncio.StreamWriter
    ) -> None:
        """Handle a client connection."""
        import msgpack
        
        addr = writer.get_extra_info("peername")
        logger.debug(f"New connection from {addr}")
        
        unpacker = msgpack.Unpacker(raw=False)
        
        try:
            while not self._shutdown_event.is_set():
                # Read data
                try:
                    data = await asyncio.wait_for(
                        reader.read(4096),
                        timeout=self.config.request_timeout
                    )
                except asyncio.TimeoutError:
                    break
                
                if not data:
                    break
                
                unpacker.feed(data)
                
                for msg in unpacker:
                    # Parse request
                    try:
                        request = Request(
                            method=msg.get("method", ""),
                            params=msg.get("params", {}),
                            id=msg.get("id")
                        )
                    except Exception as e:
                        response = Response(
                            error={"code": -32600, "message": f"Invalid request: {e}"},
                            id=msg.get("id") if isinstance(msg, dict) else None
                        )
                        writer.write(msgpack.packb(response.to_dict()))
                        await writer.drain()
                        continue
                    
                    # Handle request
                    response = await self.handler.handle(request)
                    
                    # Send response
                    writer.write(msgpack.packb(response.to_dict()))
                    await writer.drain()
                    
        except Exception as e:
            logger.exception(f"Connection error: {e}")
        finally:
            writer.close()
            try:
                await writer.wait_closed()
            except:
                pass
            logger.debug(f"Connection closed: {addr}")
    
    async def _shutdown(self) -> None:
        """Graceful shutdown."""
        logger.info("Shutting down daemon...")
        
        # Stop accepting new connections
        if self._server:
            self._server.close()
            await self._server.wait_closed()
        
        # Cancel existing connections with timeout
        if self._connections:
            for task in self._connections:
                task.cancel()
            
            await asyncio.wait(
                self._connections,
                timeout=self.config.shutdown_timeout
            )
        
        # Cleanup Unix socket
        if self.config.socket_path and os.path.exists(self.config.socket_path):
            os.unlink(self.config.socket_path)
        
        # Persist any state
        try:
            from ..index import get_store
            store = get_store()
            # Save index if it has save method
            if hasattr(store, '_store') and hasattr(store._store, 'save'):
                data_dir = Path.home() / ".hsa" / "data"
                data_dir.mkdir(parents=True, exist_ok=True)
                store._store.save(str(data_dir / "index.faiss"))
                logger.info("Saved FAISS index")
        except Exception as e:
            logger.warning(f"Failed to save state: {e}")
        
        logger.info("Daemon shutdown complete")


async def run_daemon(config: Optional[DaemonConfig] = None) -> None:
    """Run the daemon."""
    daemon = HSADaemon(config)
    await daemon.start()


def main():
    """Entry point for daemon."""
    import argparse
    
    parser = argparse.ArgumentParser(description="HSA v5.0 Daemon")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind")
    parser.add_argument("--port", type=int, default=9527, help="Port to bind")
    parser.add_argument("--socket", help="Unix socket path (overrides host/port)")
    parser.add_argument("--log-level", default="INFO", help="Log level")
    parser.add_argument("--log-file", help="Log file path")
    
    args = parser.parse_args()
    
    config = DaemonConfig(
        host=args.host,
        port=args.port,
        socket_path=args.socket,
        log_level=args.log_level,
        log_file=args.log_file
    )
    
    asyncio.run(run_daemon(config))


if __name__ == "__main__":
    main()
