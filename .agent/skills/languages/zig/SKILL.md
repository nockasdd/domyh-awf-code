---
name: zig
detect: ["*.zig", "build.zig", "build.zig.zon"]
version: "6.4.0"
category: systems
tier: 2
---

# Zig Patterns — DOMYH Awesome Code

> **Version**: Zig 0.13+ (2025-2026)
> **Focus**: Systems programming, C interop, WebAssembly
> **Philosophy**: Simple, explicit, no hidden control flow

---

## 🎯 When to Use This Skill

Use for: Systems programming, game engines, embedded, C replacement.
**NOT for**: Web APIs (→ go), ML (→ python), mobile (→ flutter).

---

## 📦 Why Zig?

| Feature        | Zig            | C          | Rust           |
| -------------- | -------------- | ---------- | -------------- |
| Memory safety  | Runtime checks | None       | Compile-time   |
| C interop      | Native 🏆      | N/A        | FFI            |
| Compile time   | Comptime 🏆    | Macros     | Const generics |
| Build system   | Built-in 🏆    | Make/CMake | Cargo          |
| Learning curve | Low            | Low        | High           |

---

## 🔧 Project Setup

```bash
# Create new project
mkdir my-project && cd my-project
zig init

# Project structure
my-project/
├── build.zig         # Build configuration
├── build.zig.zon     # Dependencies
└── src/
    └── main.zig      # Entry point
```

### build.zig

```zig
const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const exe = b.addExecutable(.{
        .name = "myapp",
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });

    b.installArtifact(exe);

    // Run step
    const run_cmd = b.addRunArtifact(exe);
    run_cmd.step.dependOn(b.getInstallStep());

    const run_step = b.step("run", "Run the app");
    run_step.dependOn(&run_cmd.step);

    // Test step
    const tests = b.addTest(.{
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });

    const test_step = b.step("test", "Run tests");
    test_step.dependOn(&b.addRunArtifact(tests).step);
}
```

---

## 🔄 Core Patterns

### Error Handling

```zig
const std = @import("std");

// ✅ Error union return type
fn readFile(path: []const u8) ![]u8 {
    const file = try std.fs.cwd().openFile(path, .{});
    defer file.close();

    return try file.readToEndAlloc(std.heap.page_allocator, 1024 * 1024);
}

// ✅ Custom error sets
const FileError = error{
    NotFound,
    PermissionDenied,
    TooBig,
};

fn processFile(path: []const u8) FileError!void {
    const stat = std.fs.cwd().statFile(path) catch |err| {
        return switch (err) {
            error.FileNotFound => error.NotFound,
            error.AccessDenied => error.PermissionDenied,
            else => error.NotFound,
        };
    };

    if (stat.size > 100 * 1024 * 1024) {
        return error.TooBig;
    }
}

// ✅ Error handling patterns
pub fn main() !void {
    // Try with fallback
    const data = readFile("config.json") catch |err| {
        std.debug.print("Error: {}\n", .{err});
        return;
    };
    defer std.heap.page_allocator.free(data);

    // Propagate error
    const result = try processFile("input.txt");
    _ = result;
}
```

### Memory Management

```zig
const std = @import("std");
const Allocator = std.mem.Allocator;

// ✅ Explicit allocator pattern
const User = struct {
    name: []const u8,
    email: []const u8,
    allocator: Allocator,

    pub fn init(allocator: Allocator, name: []const u8, email: []const u8) !User {
        return User{
            .name = try allocator.dupe(u8, name),
            .email = try allocator.dupe(u8, email),
            .allocator = allocator,
        };
    }

    pub fn deinit(self: *User) void {
        self.allocator.free(self.name);
        self.allocator.free(self.email);
    }
};

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    var user = try User.init(allocator, "John", "john@example.com");
    defer user.deinit();

    std.debug.print("User: {s}\n", .{user.name});
}
```

### Comptime (Compile-Time Execution)

```zig
const std = @import("std");

// ✅ Compile-time type generation
fn Matrix(comptime T: type, comptime rows: usize, comptime cols: usize) type {
    return struct {
        data: [rows][cols]T,

        const Self = @This();

        pub fn init() Self {
            return .{ .data = std.mem.zeroes([rows][cols]T) };
        }

        pub fn get(self: Self, row: usize, col: usize) T {
            return self.data[row][col];
        }

        pub fn set(self: *Self, row: usize, col: usize, value: T) void {
            self.data[row][col] = value;
        }
    };
}

// ✅ Compile-time string processing
fn parseFormatString(comptime fmt: []const u8) usize {
    var count: usize = 0;
    var i: usize = 0;
    while (i < fmt.len) : (i += 1) {
        if (fmt[i] == '{' and i + 1 < fmt.len and fmt[i + 1] == '}') {
            count += 1;
            i += 1;
        }
    }
    return count;
}

// Usage
const Mat3x3 = Matrix(f32, 3, 3);
const arg_count = parseFormatString("Hello {} from {}!");  // 2 at compile time

pub fn main() void {
    var m = Mat3x3.init();
    m.set(1, 1, 5.0);
    std.debug.print("Value: {}\n", .{m.get(1, 1)});
    std.debug.print("Args: {}\n", .{arg_count});
}
```

---

## 🔗 C Interop

```zig
const std = @import("std");
const c = @cImport({
    @cInclude("stdio.h");
    @cInclude("stdlib.h");
});

pub fn main() void {
    // ✅ Call C functions directly
    _ = c.printf("Hello from C!\n");

    // ✅ Use C types
    const ptr: [*c]c.char = c.malloc(100);
    defer c.free(ptr);

    // ✅ Pass Zig strings to C
    const message = "Zig to C";
    _ = c.printf("%s\n", message.ptr);
}
```

### Linking C Libraries

```zig
// build.zig
exe.linkLibC();
exe.linkSystemLibrary("sqlite3");
exe.addIncludePath("/usr/include");
```

---

## 🌐 WebAssembly

```zig
// src/wasm.zig

// Export function to JavaScript
export fn add(a: i32, b: i32) i32 {
    return a + b;
}

export fn greet(name_ptr: [*]const u8, name_len: usize) void {
    const name = name_ptr[0..name_len];
    // Process name...
}

// Import from JavaScript
extern fn consoleLog(ptr: [*]const u8, len: usize) void;

fn log(message: []const u8) void {
    consoleLog(message.ptr, message.len);
}
```

```bash
# Build for WASM
zig build-lib src/wasm.zig -target wasm32-freestanding -O ReleaseSmall
```

---

## 🧪 Testing

```zig
const std = @import("std");
const testing = std.testing;

fn add(a: i32, b: i32) i32 {
    return a + b;
}

test "add positive numbers" {
    try testing.expectEqual(@as(i32, 5), add(2, 3));
}

test "add negative numbers" {
    try testing.expectEqual(@as(i32, -1), add(1, -2));
}

test "memory allocation" {
    const allocator = testing.allocator;
    const list = try allocator.alloc(u8, 100);
    defer allocator.free(list);

    try testing.expect(list.len == 100);
}
```

```bash
# Run tests
zig build test
```

---

## ✅ Production Checklist

### Code Quality

- [ ] No undefined behavior
- [ ] All allocations paired with free
- [ ] Error handling complete
- [ ] Comptime where possible

### Performance

- [ ] Release build optimized
- [ ] No debug allocator in prod
- [ ] Profile with `-O ReleaseFast`
- [ ] SIMD for hot paths

### Safety

- [ ] Bounds checks appropriate
- [ ] No use-after-free
- [ ] Null checks on optionals

---

_DOMYH Awesome Code • Zig 0.13+_
