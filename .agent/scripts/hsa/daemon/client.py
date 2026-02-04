# HSA v5.0 - IPC Client
# =============================================================================
"""
Client library for communicating with HSA daemon.

Usage:
    from hsa.daemon import HSAClient
    
    async with HSAClient() as client:
        result = await client.search("hello world")
        print(result)
    
    # Or synchronous:
    client = HSAClient.sync()
    result = client.search("hello world")
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

logger = logging.getLogger("hsa.client")


@dataclass
class ClientConfig:
    """Client configuration."""
    host: str = "127.0.0.1"
    port: int = 9527
    socket_path: Optional[str] = None
    timeout: float = 30.0
    retry_count: int = 3
    retry_delay: float = 1.0


class HSAClient:
    """
    Async client for HSA daemon.
    
    Usage:
        async with HSAClient() as client:
            # Health check
            health = await client.health()
            
            # Search
            results = await client.search("authentication")
            
            # Embed
            vectors = await client.embed(["code snippet"])
            
            # Count tokens
            count = await client.count_tokens("hello world")
    """
    
    def __init__(self, config: Optional[ClientConfig] = None):
        self.config = config or ClientConfig()
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._request_id = 0
        self._connected = False
    
    async def __aenter__(self) -> "HSAClient":
        await self.connect()
        return self
    
    async def __aexit__(self, *args) -> None:
        await self.close()
    
    async def connect(self) -> None:
        """Connect to daemon."""
        try:
            if self.config.socket_path:
                self._reader, self._writer = await asyncio.open_unix_connection(
                    self.config.socket_path
                )
            else:
                self._reader, self._writer = await asyncio.open_connection(
                    self.config.host,
                    self.config.port
                )
            
            self._connected = True
            logger.debug(f"Connected to HSA daemon")
            
        except Exception as e:
            logger.error(f"Failed to connect to daemon: {e}")
            raise ConnectionError(f"Cannot connect to HSA daemon: {e}")
    
    async def close(self) -> None:
        """Close connection."""
        if self._writer:
            self._writer.close()
            try:
                await self._writer.wait_closed()
            except:
                pass
        self._connected = False
    
    async def _request(self, method: str, params: Dict[str, Any] = None) -> Any:
        """Send request and get response."""
        try:
            import msgpack
        except ImportError:
            raise ImportError("msgpack not installed. Install with: pip install msgpack")
        
        if not self._connected:
            await self.connect()
        
        self._request_id += 1
        request = {
            "method": method,
            "params": params or {},
            "id": self._request_id
        }
        
        # Send request
        self._writer.write(msgpack.packb(request))
        await self._writer.drain()
        
        # Read response
        data = await asyncio.wait_for(
            self._reader.read(65536),
            timeout=self.config.timeout
        )
        
        if not data:
            raise ConnectionError("Connection closed by server")
        
        response = msgpack.unpackb(data, raw=False)
        
        if "error" in response and response["error"]:
            raise RuntimeError(f"Server error: {response['error']}")
        
        return response.get("result")
    
    # === API Methods ===
    
    async def health(self) -> Dict:
        """Health check."""
        return await self._request("health")
    
    async def ping(self) -> str:
        """Simple ping."""
        return await self._request("ping")
    
    async def status(self) -> Dict:
        """Get daemon status."""
        return await self._request("status")
    
    async def search(self, query: str, k: int = 10) -> Dict:
        """Search codebase."""
        return await self._request("search", {"query": query, "k": k})
    
    async def get_context(
        self, 
        query: str, 
        files: List[str] = None, 
        max_tokens: int = 8000
    ) -> Dict:
        """Get context for query."""
        return await self._request("get_context", {
            "query": query,
            "files": files or [],
            "max_tokens": max_tokens
        })
    
    async def embed(self, texts: List[str]) -> Dict:
        """Generate embeddings."""
        return await self._request("embed", {"texts": texts})
    
    async def parse(self, file_path: str, content: str = None) -> Dict:
        """Parse source file."""
        return await self._request("parse", {
            "file_path": file_path,
            "content": content
        })
    
    async def count_tokens(self, text: str, model: str = "cl100k_base") -> Dict:
        """Count tokens."""
        return await self._request("count_tokens", {
            "text": text,
            "model": model
        })
    
    async def shutdown(self) -> Dict:
        """Request daemon shutdown."""
        return await self._request("shutdown")
    
    # === Sync Wrapper ===
    
    @classmethod
    def sync(cls, config: Optional[ClientConfig] = None) -> "SyncHSAClient":
        """Create a synchronous client."""
        return SyncHSAClient(config)


class SyncHSAClient:
    """
    Synchronous wrapper for HSAClient.
    
    Usage:
        client = SyncHSAClient()
        
        health = client.health()
        results = client.search("hello")
    """
    
    def __init__(self, config: Optional[ClientConfig] = None):
        self._async_client = HSAClient(config)
        self._loop: Optional[asyncio.AbstractEventLoop] = None
    
    def _get_loop(self) -> asyncio.AbstractEventLoop:
        """Get or create event loop."""
        if self._loop is None or self._loop.is_closed():
            try:
                self._loop = asyncio.get_event_loop()
            except RuntimeError:
                self._loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self._loop)
        return self._loop
    
    def _run(self, coro):
        """Run coroutine synchronously."""
        return self._get_loop().run_until_complete(coro)
    
    def connect(self) -> None:
        """Connect to daemon."""
        self._run(self._async_client.connect())
    
    def close(self) -> None:
        """Close connection."""
        self._run(self._async_client.close())
    
    def __enter__(self) -> "SyncHSAClient":
        self.connect()
        return self
    
    def __exit__(self, *args) -> None:
        self.close()
    
    # === API Methods ===
    
    def health(self) -> Dict:
        return self._run(self._async_client.health())
    
    def ping(self) -> str:
        return self._run(self._async_client.ping())
    
    def status(self) -> Dict:
        return self._run(self._async_client.status())
    
    def search(self, query: str, k: int = 10) -> Dict:
        return self._run(self._async_client.search(query, k))
    
    def get_context(
        self, 
        query: str, 
        files: List[str] = None, 
        max_tokens: int = 8000
    ) -> Dict:
        return self._run(self._async_client.get_context(query, files, max_tokens))
    
    def embed(self, texts: List[str]) -> Dict:
        return self._run(self._async_client.embed(texts))
    
    def parse(self, file_path: str, content: str = None) -> Dict:
        return self._run(self._async_client.parse(file_path, content))
    
    def count_tokens(self, text: str, model: str = "cl100k_base") -> Dict:
        return self._run(self._async_client.count_tokens(text, model))
    
    def shutdown(self) -> Dict:
        return self._run(self._async_client.shutdown())


# Quick functions
async def connect(config: Optional[ClientConfig] = None) -> HSAClient:
    """Quick connect to daemon."""
    client = HSAClient(config)
    await client.connect()
    return client


def connect_sync(config: Optional[ClientConfig] = None) -> SyncHSAClient:
    """Quick connect to daemon (sync)."""
    client = SyncHSAClient(config)
    client.connect()
    return client
