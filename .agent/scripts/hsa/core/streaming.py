# HSA v5.0 - SSE Streaming
# =============================================================================
"""
Server-Sent Events (SSE) streaming for real-time responses.

Features:
- Chunked context delivery
- Progress reporting
- Cancellation support
- Backpressure handling
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, AsyncIterator, Callable, Dict, List, Optional

logger = logging.getLogger("hsa.streaming")


class StreamEventType(Enum):
    """Types of SSE events."""
    START = "start"
    PROGRESS = "progress"
    CHUNK = "chunk"
    ERROR = "error"
    COMPLETE = "complete"
    CANCEL = "cancel"


@dataclass
class StreamEvent:
    """A single SSE event."""
    type: StreamEventType
    data: Any
    id: Optional[str] = None
    timestamp: float = field(default_factory=time.time)
    
    def to_sse(self) -> str:
        """Convert to SSE format."""
        lines = []
        
        if self.id:
            lines.append(f"id: {self.id}")
        
        lines.append(f"event: {self.type.value}")
        
        if isinstance(self.data, (dict, list)):
            data_str = json.dumps(self.data)
        else:
            data_str = str(self.data)
        
        # Handle multiline data
        for line in data_str.split("\n"):
            lines.append(f"data: {line}")
        
        lines.append("")  # Empty line to end event
        
        return "\n".join(lines) + "\n"


@dataclass
class ProgressInfo:
    """Progress information for streaming."""
    current: int
    total: int
    message: str = ""
    
    @property
    def percentage(self) -> float:
        return (self.current / self.total * 100) if self.total > 0 else 0


class StreamController:
    """
    Controller for managing SSE streams.
    
    Handles:
    - Event emission
    - Cancellation
    - Backpressure
    
    Usage:
        controller = StreamController()
        
        async for event in controller.stream():
            yield event.to_sse()
        
        # From producer
        await controller.emit_chunk(data)
        await controller.emit_progress(50, 100, "Processing...")
        await controller.complete()
    """
    
    def __init__(self, buffer_size: int = 100):
        self._queue: asyncio.Queue[StreamEvent] = asyncio.Queue(maxsize=buffer_size)
        self._cancelled = False
        self._completed = False
        self._event_id = 0
        self._start_time = time.time()
    
    def _next_id(self) -> str:
        """Generate next event ID."""
        self._event_id += 1
        return str(self._event_id)
    
    async def emit(self, event: StreamEvent) -> bool:
        """Emit an event to the stream."""
        if self._cancelled or self._completed:
            return False
        
        event.id = self._next_id()
        
        try:
            await asyncio.wait_for(
                self._queue.put(event),
                timeout=5.0
            )
            return True
        except asyncio.TimeoutError:
            logger.warning("Stream backpressure: event dropped")
            return False
    
    async def emit_start(self, metadata: Dict[str, Any] = None) -> bool:
        """Emit stream start event."""
        return await self.emit(StreamEvent(
            type=StreamEventType.START,
            data=metadata or {}
        ))
    
    async def emit_chunk(self, data: Any) -> bool:
        """Emit a data chunk."""
        return await self.emit(StreamEvent(
            type=StreamEventType.CHUNK,
            data=data
        ))
    
    async def emit_progress(
        self,
        current: int,
        total: int,
        message: str = ""
    ) -> bool:
        """Emit progress update."""
        progress = ProgressInfo(current, total, message)
        return await self.emit(StreamEvent(
            type=StreamEventType.PROGRESS,
            data={
                "current": progress.current,
                "total": progress.total,
                "percentage": progress.percentage,
                "message": progress.message,
            }
        ))
    
    async def emit_error(self, error: str, code: str = "ERROR") -> bool:
        """Emit error event."""
        return await self.emit(StreamEvent(
            type=StreamEventType.ERROR,
            data={"error": error, "code": code}
        ))
    
    async def complete(self, summary: Dict[str, Any] = None) -> bool:
        """Mark stream as complete."""
        elapsed = time.time() - self._start_time
        
        result = await self.emit(StreamEvent(
            type=StreamEventType.COMPLETE,
            data={
                "duration_ms": elapsed * 1000,
                "events": self._event_id,
                **(summary or {})
            }
        ))
        
        self._completed = True
        return result
    
    def cancel(self) -> None:
        """Cancel the stream."""
        self._cancelled = True
        
        # Put cancel event (don't await)
        try:
            self._queue.put_nowait(StreamEvent(
                type=StreamEventType.CANCEL,
                data={"reason": "Client cancelled"}
            ))
        except asyncio.QueueFull:
            pass
    
    @property
    def is_cancelled(self) -> bool:
        return self._cancelled
    
    @property
    def is_active(self) -> bool:
        return not self._cancelled and not self._completed
    
    async def stream(self) -> AsyncIterator[StreamEvent]:
        """Async iterator for consuming stream events."""
        while not self._completed or not self._queue.empty():
            if self._cancelled:
                break
            
            try:
                event = await asyncio.wait_for(
                    self._queue.get(),
                    timeout=0.5
                )
                yield event
                
                if event.type in (StreamEventType.COMPLETE, StreamEventType.CANCEL):
                    break
                    
            except asyncio.TimeoutError:
                continue


class ChunkedContextStream:
    """
    Stream context chunks with progress.
    
    Optimal for large context delivery:
    - Chunks by semantic boundaries
    - Reports progress
    - Handles cancellation
    
    Usage:
        streamer = ChunkedContextStream(controller)
        await streamer.stream_context(entities, chunk_size=10)
    """
    
    def __init__(
        self,
        controller: StreamController,
        chunk_size: int = 10
    ):
        self.controller = controller
        self.chunk_size = chunk_size
    
    async def stream_entities(
        self,
        entities: List[Dict[str, Any]],
        transform: Optional[Callable[[Dict[str, Any]], Any]] = None
    ) -> int:
        """Stream entities in chunks."""
        total = len(entities)
        sent = 0
        
        await self.controller.emit_start({
            "total_entities": total,
            "chunk_size": self.chunk_size,
        })
        
        for i in range(0, total, self.chunk_size):
            if self.controller.is_cancelled:
                break
            
            chunk = entities[i:i + self.chunk_size]
            
            if transform:
                chunk = [transform(e) for e in chunk]
            
            await self.controller.emit_chunk({
                "entities": chunk,
                "offset": i,
            })
            
            sent += len(chunk)
            await self.controller.emit_progress(sent, total, f"Sent {sent}/{total} entities")
        
        await self.controller.complete({"total_sent": sent})
        return sent
    
    async def stream_search_results(
        self,
        results_iter: AsyncIterator[Dict[str, Any]],
        max_results: int = 100
    ) -> int:
        """Stream search results as they arrive."""
        await self.controller.emit_start({
            "max_results": max_results,
        })
        
        count = 0
        
        async for result in results_iter:
            if self.controller.is_cancelled:
                break
            
            if count >= max_results:
                break
            
            await self.controller.emit_chunk(result)
            count += 1
            
            # Periodic progress
            if count % 10 == 0:
                await self.controller.emit_progress(count, max_results)
        
        await self.controller.complete({"results_count": count})
        return count


async def sse_response(
    controller: StreamController
) -> AsyncIterator[str]:
    """
    Generate SSE response from controller.
    
    Usage in FastAPI:
        @app.get("/stream")
        async def stream_endpoint():
            controller = StreamController()
            asyncio.create_task(producer(controller))
            return StreamingResponse(
                sse_response(controller),
                media_type="text/event-stream"
            )
    """
    # Send initial comment to establish connection
    yield ": HSA v5.0 SSE Stream\n\n"
    
    async for event in controller.stream():
        yield event.to_sse()
        
        # Heartbeat to keep connection alive
        if event.type == StreamEventType.PROGRESS:
            yield ": heartbeat\n\n"
