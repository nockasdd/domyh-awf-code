# Real-time Communication — WebSocket • Socket.IO • SSE

> Full-duplex • Rooms & Namespaces • Server Push  
> Scaling • Authentication • LLM Streaming

---

## Khi Nào Dùng

- Chat applications, collaborative editing
- Live dashboards, real-time notifications
- LLM response streaming (token-by-token)
- Game state synchronization
- IoT device communication

## Protocol Selection

| Protocol      | Direction       | Reconnect | Best For                      |
| ------------- | --------------- | --------- | ----------------------------- |
| **WebSocket** | Bidirectional   | Manual    | Chat, gaming, collaboration   |
| **Socket.IO** | Bidirectional   | Auto      | Apps needing rooms/namespaces |
| **SSE**       | Server → Client | Auto      | Notifications, LLM streaming  |

## WebSocket Patterns

### Connection with Reconnection

```typescript
class ReconnectingWS {
  private retries = 0;
  connect(url: string) {
    this.ws = new WebSocket(url);
    this.ws.onopen = () => {
      this.retries = 0;
    };
    this.ws.onclose = () => {
      const delay = Math.min(1000 * 2 ** this.retries++, 30000);
      setTimeout(() => this.connect(url), delay);
    };
    this.ws.onmessage = (e) => this.handleMessage(JSON.parse(e.data));
  }
}
```

### Authentication

```typescript
// Token in URL (simple but exposed)
new WebSocket(`wss://api.example.com?token=${jwt}`);
// Token in first message (preferred)
ws.onopen = () => ws.send(JSON.stringify({ type: "auth", token: jwt }));
```

## Socket.IO Patterns

### Rooms & Namespaces

```typescript
// Server
io.on("connection", (socket) => {
  socket.join(`room:${roomId}`);
  io.to(`room:${roomId}`).emit("message", data); // to room
  socket.broadcast.to(`room:${roomId}`).emit("message", data); // except sender
});
// Namespace
const chatNs = io.of("/chat");
chatNs.on("connection", (socket) => { ... });
```

### Horizontal Scaling (Redis Adapter)

```typescript
import { createAdapter } from "@socket.io/redis-adapter";
io.adapter(createAdapter(pubClient, subClient));
// Now works across multiple server instances
```

## SSE Patterns

### LLM Streaming

```typescript
// Server: stream LLM response
app.get("/api/chat", (req, res) => {
  res.writeHead(200, {
    "Content-Type": "text/event-stream",
    "Cache-Control": "no-cache",
    Connection: "keep-alive",
  });
  for await (const chunk of llm.stream(messages)) {
    res.write(`data: ${JSON.stringify({ content: chunk })}\n\n`);
  }
  res.write("data: [DONE]\n\n");
  res.end();
});

// Client
const source = new EventSource("/api/chat");
source.onmessage = (e) => {
  if (e.data === "[DONE]") {
    source.close();
    return;
  }
  appendToUI(JSON.parse(e.data).content);
};
```

## Scaling Checklist

- ✅ Sticky sessions OR Redis adapter
- ✅ NGINX: `proxy_set_header Upgrade $http_upgrade`
- ✅ Heartbeat/ping-pong for connection health
- ✅ Connection limits per user
- ✅ Message rate limiting
- ✅ Graceful shutdown (drain connections)

## Common Traps

| Trap                                   | Fix                                       |
| -------------------------------------- | ----------------------------------------- |
| Connection drops behind proxy          | NGINX upgrade headers                     |
| Memory leak from unclosed connections  | Track + cleanup on disconnect             |
| Scaling issues                         | Redis/NATS adapter for multiple instances |
| SSE max connections (browser limit: 6) | Use HTTP/2 or single multiplexed SSE      |

---

_DOMYH Awesome Code • Real-time Communication Skill v1.0.0_
