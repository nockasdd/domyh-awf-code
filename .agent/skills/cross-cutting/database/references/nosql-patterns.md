## 🍃 MongoDB Patterns

### When to Use MongoDB

| ✅ Good For             | ❌ Not Good For               |
| ------------------------ | ----------------------------- |
| Flexible/evolving schema | Complex joins                 |
| JSON-like documents      | ACID transactions (multi-doc) |
| Rapid prototyping        | Strong consistency            |
| Content management       | Financial data                |
| IoT data ingestion       | Complex queries               |
| Real-time analytics      | Relational data               |

### MongoDB Node.js Patterns

```typescript
import { MongoClient, ObjectId } from "mongodb";

const client = new MongoClient(process.env.MONGODB_URI);
const db = client.db("myapp");

// ✅ Insert
await db.collection("users").insertOne({
  email: "alice@example.com",
  name: "Alice",
  metadata: { lastLogin: new Date(), preferences: { theme: "dark" } },
  createdAt: new Date(),
});

// ✅ Find with projection
const user = await db.collection("users").findOne(
  { email: "alice@example.com" },
  { projection: { password: 0 } }, // Exclude password
);

// ✅ Aggregation pipeline
const results = await db
  .collection("orders")
  .aggregate([
    { $match: { status: "completed" } },
    {
      $group: {
        _id: "$userId",
        totalAmount: { $sum: "$amount" },
        orderCount: { $sum: 1 },
      },
    },
    { $sort: { totalAmount: -1 } },
    { $limit: 10 },
  ])
  .toArray();

// ✅ Indexes
await db.collection("users").createIndex({ email: 1 }, { unique: true });
await db
  .collection("events")
  .createIndex({ createdAt: 1 }, { expireAfterSeconds: 86400 });
```

---

## 🔴 Redis Patterns

### Redis Use Cases

| Pattern         | Use Case             | TTL        |
| --------------- | -------------------- | ---------- |
| **Cache**       | Database query cache | 5-60 min   |
| **Session**     | User sessions        | 24h        |
| **Rate Limit**  | API throttling       | 1 min      |
| **Leaderboard** | Sorted sets          | Persistent |
| **Pub/Sub**     | Real-time events     | N/A        |
| **Queue**       | Job queue (List)     | N/A        |
| **Lock**        | Distributed lock     | 30s        |

### Redis Node.js Patterns

```typescript
import Redis from "ioredis";

const redis = new Redis(process.env.REDIS_URL);

// ✅ Cache pattern
async function getCachedUser(userId: string) {
  const cacheKey = `user:${userId}`;

  // Try cache first
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  // Cache miss - fetch from DB
  const user = await db.users.findUnique({ where: { id: userId } });

  // Store in cache with TTL
  await redis.setex(cacheKey, 3600, JSON.stringify(user));

  return user;
}

// ✅ Rate limiting (sliding window)
async function checkRateLimit(ip: string, limit = 100, windowSec = 60) {
  const key = `ratelimit:${ip}`;
  const current = await redis.incr(key);

  if (current === 1) {
    await redis.expire(key, windowSec);
  }

  return current <= limit;
}

// ✅ Session storage
await redis.hset(`session:${sessionId}`, {
  userId: user.id,
  email: user.email,
  loginAt: Date.now(),
});
await redis.expire(`session:${sessionId}`, 86400); // 24h

// ✅ Leaderboard
await redis.zadd("leaderboard", score, `user:${userId}`);
const top10 = await redis.zrevrange("leaderboard", 0, 9, "WITHSCORES");

// ✅ Pub/Sub
const subscriber = redis.duplicate();
await subscriber.subscribe("notifications");
subscriber.on("message", (channel, message) => {
  console.log(`Received: ${message}`);
});

await redis.publish("notifications", JSON.stringify({ type: "new_order" }));

// ✅ Distributed lock
async function withLock<T>(key: string, fn: () => Promise<T>, ttlMs = 30000) {
  const lockKey = `lock:${key}`;
  const lockValue = crypto.randomUUID();

  const acquired = await redis.set(lockKey, lockValue, "PX", ttlMs, "NX");
  if (!acquired) throw new Error("Failed to acquire lock");

  try {
    return await fn();
  } finally {
    // Release only if we own the lock
    const script = `
      if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
      else
        return 0
      end
    `;
    await redis.eval(script, 1, lockKey, lockValue);
  }
}
```

---

## 🛠️ Database Tools

### Migration Tools

| Tool               | Language | Database   |
| ------------------ | -------- | ---------- |
| **Prisma Migrate** | TS/JS    | Multi      |
| **Drizzle Kit**    | TS/JS    | Multi      |
| **golang-migrate** | Go       | Multi      |
| **Alembic**        | Python   | SQLAlchemy |
| **Flyway**         | Java/CLI | Multi      |
| **Atlas**          | Go       | Multi      |

### Monitoring & GUI

| Tool                | Purpose        |
| ------------------- | -------------- |
| **pgAdmin**         | PostgreSQL GUI |
| **DBeaver**         | Universal GUI  |
| **TablePlus**       | Multi-DB GUI   |
| **Prisma Studio**   | Prisma visual  |
| **RedisInsight**    | Redis GUI      |
| **MongoDB Compass** | MongoDB GUI    |

### Connection Pooling

| Tool              | Database   |
| ----------------- | ---------- |
| **PgBouncer**     | PostgreSQL |
| **PgCat**         | PostgreSQL |
| **ProxySQL**      | MySQL      |
| **Redis Cluster** | Redis      |

---

## ✅ Production Checklist
