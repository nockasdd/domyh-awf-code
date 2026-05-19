---
library: android-control-protocols
version: 1
latest: true
category: infra
official_docs: https://github.com/Genymobile/scrcpy
last_updated: 2026-03-26
---

# android-control-protocols v1

> Low-level Android control protocols: scrcpy sockets and binary control messages, minicap frame streaming, minitouch text protocol, pseudo-stream patterns (screenrecord, screencap loop), and host-side window capture (DXGI/PrintWindow) for emulators.

## Version Comparison
<!-- MANDATORY — helps agent disambiguate versions instantly -->
| Feature                  | v1                                | v{latest} |
|:-------------------------|:----------------------------------|:----------|
| scrcpy video socket      | H.264/H.265 elementary stream     | —         |
| scrcpy control socket    | Binary input messages             | —         |
| minitouch protocol       | `d/m/u/c` text commands           | —         |
| minicap stream           | 24-byte header + JPEG frames      | —         |
| Pseudo-stream patterns   | screenrecord pipe, screencap loop | —         |
| Host-side capture        | DXGI / PrintWindow (emulator)     | —         |

## Installation
<!-- MANDATORY — exact install commands with version pinning -->
```bash
# scrcpy (Debian/Ubuntu)
sudo apt-get install scrcpy

# scrcpy (Windows via scoop)
scoop install scrcpy

# STF tools (build from source)
git clone https://github.com/AgoraIO-Extensions/electron-agora-rtc-ng.git
# minicap and minitouch are typically bundled with STF or built per ABI
git clone https://github.com/niceplaces/minicap.git
git clone https://github.com/niceplaces/minitouch.git

# Push to device
adb push minicap /data/local/tmp/
adb push minitouch /data/local/tmp/
adb shell chmod 755 /data/local/tmp/minicap /data/local/tmp/minitouch
```

## Configuration
<!-- MANDATORY — complete config example, annotated -->
```bash
# Start scrcpy with common automation flags
scrcpy --max-size 1280 --bit-rate 8M --no-display --no-audio \
       --video-codec=h264 --max-fps 30

# Forward minicap / minitouch local sockets to host TCP ports
adb forward tcp:1313 localabstract:minicap
adb forward tcp:1111 localabstract:minitouch

# Start minicap on device (example: 1080x1920 real, 540x960 virtual, 0 rotation)
adb shell "LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P 1080x1920@540x960/0"

# Start minitouch on device
adb shell "/data/local/tmp/minitouch"
```

## Core API
<!-- MANDATORY — most-used APIs with params, types, return values -->

### scrcpy Control Protocol (Binary)

scrcpy deploys a lightweight Java server on the device. The client connects via 3 sockets:
1. **Video socket**: Raw H.264/H.265 elementary stream (NAL units).
2. **Audio socket**: Raw Opus stream (Android 11+).
3. **Control socket**: Binary control messages for input injection.

```c
// Source: scrcpy/app/src/control_msg.h
enum sc_control_msg_type {
    SC_CONTROL_MSG_TYPE_INJECT_KEYCODE       = 0,
    SC_CONTROL_MSG_TYPE_INJECT_TEXT           = 1,
    SC_CONTROL_MSG_TYPE_INJECT_TOUCH_EVENT    = 2,
    SC_CONTROL_MSG_TYPE_INJECT_SCROLL_EVENT   = 3,
    SC_CONTROL_MSG_TYPE_BACK_OR_SCREEN_ON     = 4,
    SC_CONTROL_MSG_TYPE_EXPAND_NOTIFICATION_PANEL = 5,
    SC_CONTROL_MSG_TYPE_EXPAND_SETTINGS_PANEL = 6,
    SC_CONTROL_MSG_TYPE_COLLAPSE_PANELS       = 7,
    SC_CONTROL_MSG_TYPE_GET_CLIPBOARD         = 8,
    SC_CONTROL_MSG_TYPE_SET_CLIPBOARD         = 9,
    SC_CONTROL_MSG_TYPE_SET_DISPLAY_POWER     = 10,
    SC_CONTROL_MSG_TYPE_ROTATE_DEVICE         = 11,
    SC_CONTROL_MSG_TYPE_UHID_CREATE           = 12,
    SC_CONTROL_MSG_TYPE_UHID_INPUT            = 13,
    SC_CONTROL_MSG_TYPE_OPEN_HARD_KEYBOARD_SETTINGS = 14,
    SC_CONTROL_MSG_TYPE_START_APP             = 15,
    SC_CONTROL_MSG_TYPE_RESET_VIDEO           = 16,
};

// Touch event payload structure (serialized in Big Endian on wire)
struct sc_inject_touch_event {
    uint8_t  type;        // SC_CONTROL_MSG_TYPE_INJECT_TOUCH_EVENT (2)
    uint8_t  action;      // AMOTION_EVENT_ACTION_DOWN=0, UP=1, MOVE=2
    uint64_t pointer_id;  // finger ID for multi-touch (0, 1, 2...)
    int32_t  x;           // touch X in device coordinates
    int32_t  y;           // touch Y in device coordinates
    uint16_t width;       // display width (for coordinate scaling)
    uint16_t height;      // display height
    uint16_t pressure;    // 0x0000 to 0xFFFF (0.0 to 1.0 normalized)
    uint32_t action_button; // mouse button bitmask (if applicable)
    uint32_t buttons;     // currently pressed buttons
};
```

### minicap Frame Stream Protocol

minicap streams JPEG frames over a local abstract Unix socket. The first 24 bytes are a one-time global header (banner).

```text
minicap Banner Header (24 bytes, Little Endian):
| Offset | Type         | Field                 |
|:-------|:-------------|:----------------------|
| 0      | uint8        | Version (1)           |
| 1      | uint8        | Banner size (24)      |
| 2-5    | uint32 (LE)  | Process ID            |
| 6-9    | uint32 (LE)  | Real display width    |
| 10-13  | uint32 (LE)  | Real display height   |
| 14-17  | uint32 (LE)  | Virtual display width |
| 18-21  | uint32 (LE)  | Virtual display height|
| 22     | uint8        | Display orientation   |
| 23     | uint8        | Quirk bitflags        |

After banner, continuous frame loop:
  [4 bytes uint32 LE: JPEG frame size] [N bytes: raw JPEG data]
  [4 bytes uint32 LE: JPEG frame size] [N bytes: raw JPEG data]
  ...
```

```python
import socket, struct
from PIL import Image
import io

def read_minicap_stream(host: str = "127.0.0.1", port: int = 1313):
    """Read minicap banner then yield JPEG frames."""
    sock = socket.create_connection((host, port))

    # Read 24-byte banner
    banner = sock.recv(24)
    version = banner[0]
    banner_size = banner[1]
    pid = struct.unpack_from("<I", banner, 2)[0]
    real_w = struct.unpack_from("<I", banner, 6)[0]
    real_h = struct.unpack_from("<I", banner, 10)[0]
    virt_w = struct.unpack_from("<I", banner, 14)[0]
    virt_h = struct.unpack_from("<I", banner, 18)[0]
    orient = banner[22]
    print(f"minicap: {real_w}x{real_h} → {virt_w}x{virt_h}, orient={orient}")

    # Frame loop
    while True:
        frame_len_bytes = _recv_exact(sock, 4)
        frame_len = struct.unpack("<I", frame_len_bytes)[0]
        jpeg_data = _recv_exact(sock, frame_len)
        yield jpeg_data  # raw JPEG bytes

def _recv_exact(sock, n: int) -> bytes:
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("minicap socket closed")
        buf += chunk
    return buf
```

### minitouch Multitouch Command Protocol

minitouch listens on a local abstract Unix socket and accepts line-based text commands for high-performance input injection.

```text
Protocol commands (each terminated by \n):
  d <contact_id> <x> <y> <pressure>   — finger DOWN
  m <contact_id> <x> <y> <pressure>   — finger MOVE
  u <contact_id>                       — finger UP
  c                                    — COMMIT (flush buffered events)
  r                                    — RESET (release all contacts)

Coordinates are in the device's real display resolution.
Pressure is typically 50 (range: 0-255 on most devices).
```

```python
import socket

def minitouch_tap(host: str, port: int, x: int, y: int, pressure: int = 50):
    """Send a single tap via minitouch protocol."""
    sock = socket.create_connection((host, port))
    commands = f"d 0 {x} {y} {pressure}\nc\nu 0\nc\n"
    sock.sendall(commands.encode("ascii"))
    sock.close()

def minitouch_swipe(host, port, x1, y1, x2, y2, steps=10, pressure=50):
    """Send a swipe gesture with interpolated move events."""
    sock = socket.create_connection((host, port))
    sock.sendall(f"d 0 {x1} {y1} {pressure}\nc\n".encode())
    for i in range(1, steps + 1):
        t = i / steps
        cx = int(x1 + (x2 - x1) * t)
        cy = int(y1 + (y2 - y1) * t)
        sock.sendall(f"m 0 {cx} {cy} {pressure}\nc\n".encode())
    sock.sendall(b"u 0\nc\n")
    sock.close()

def minitouch_pinch_zoom(host, port, cx, cy, start_dist, end_dist, steps=10):
    """Two-finger pinch zoom centered on (cx, cy)."""
    sock = socket.create_connection((host, port))
    for i in range(steps + 1):
        t = i / steps
        dist = int(start_dist + (end_dist - start_dist) * t)
        action = "d" if i == 0 else "m"
        # Finger 0: above center
        sock.sendall(f"{action} 0 {cx} {cy - dist} 50\n".encode())
        # Finger 1: below center
        sock.sendall(f"{action} 1 {cx} {cy + dist} 50\n".encode())
        sock.sendall(b"c\n")
    sock.sendall(b"u 0\nu 1\nc\n")
    sock.close()
```

### Pseudo-Stream Patterns (Non-server Alternative)

These patterns avoid deploying server APKs (scrcpy/minicap), using only built-in ADB tools.

#### screenrecord + pipe (H.264 pseudo-stream)

```bash
# Output H.264 elementary stream to stdout (requires Android 5+)
adb exec-out screenrecord --output-format=h264 --size 720x1280 --bit-rate 4000000 -
# Can pipe to FFmpeg for decoding:
# adb exec-out screenrecord --output-format=h264 - | ffmpeg -i - -f rawvideo -pix_fmt bgr24 pipe:1
```

```python
import subprocess, numpy as np, cv2

def screenrecord_stream(serial: str, width=720, height=1280, bitrate=4_000_000):
    """
    Pseudo-stream frames via screenrecord H.264 output piped through FFmpeg.
    Latency: ~100-300ms depending on device encoder.
    Session max: 180s (screenrecord limit), auto-restart required.
    """
    adb_cmd = [
        "adb", "-s", serial, "exec-out",
        "screenrecord", "--output-format=h264",
        f"--size={width}x{height}", f"--bit-rate={bitrate}", "-"
    ]
    ffmpeg_cmd = [
        "ffmpeg", "-y", "-i", "pipe:0",
        "-f", "rawvideo", "-pix_fmt", "bgr24", "pipe:1"
    ]
    adb_proc = subprocess.Popen(adb_cmd, stdout=subprocess.PIPE)
    ff_proc = subprocess.Popen(ffmpeg_cmd, stdin=adb_proc.stdout, stdout=subprocess.PIPE)
    frame_size = width * height * 3
    while True:
        raw = ff_proc.stdout.read(frame_size)
        if len(raw) < frame_size:
            break
        frame = np.frombuffer(raw, dtype=np.uint8).reshape((height, width, 3))
        yield frame
```

#### screencap loop (PNG/gzip pseudo-stream)

```bash
# Fast single screenshot (PNG)
adb exec-out screencap -p > frame.png

# Faster: gzip-compressed raw (less CPU on encode, faster transfer)
adb exec-out "screencap | gzip -1" > frame.gz
# On host: gunzip frame.gz → decode raw screencap format
```

```python
import subprocess, cv2, numpy as np, gzip, time

def screencap_loop(serial: str, fps_limit: float = 5.0, use_gzip: bool = True):
    """
    Pseudo-stream via exec-out screencap loop.
    Latency: ~150-500ms per frame. Good for turn-based / QA / menu automation.
    """
    interval = 1.0 / fps_limit
    while True:
        t0 = time.monotonic()
        if use_gzip:
            raw = subprocess.run(
                ["adb", "-s", serial, "exec-out", "screencap | gzip -1"],
                capture_output=True, shell=False
            ).stdout
            raw = gzip.decompress(raw)
        else:
            raw = subprocess.run(
                ["adb", "-s", serial, "exec-out", "screencap", "-p"],
                capture_output=True
            ).stdout
        frame = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
        yield frame
        elapsed = time.monotonic() - t0
        if elapsed < interval:
            time.sleep(interval - elapsed)
```

### Host-Side Window Capture (Emulators Only)

For emulators running on Windows hosts with GPU mode `host` or `angle`, you can capture the emulator window directly using OS-level APIs, completely bypassing ADB.

```text
Architecture:
  Emulator (BlueStacks/AVD/LDPlayer) renders to host GPU
  → DXGI Desktop Duplication API captures surface buffer (DirectX 11+)
  → Or PrintWindow/BitBlt Win32 API captures window bitmap
  → Frame delivered to OpenCV/EmguCV for processing
  → Agent sends input back via ADB / minitouch

Advantages:
  - Ultra-low latency (~10-30ms capture time)
  - No server deployment on device
  - No ADB port forwarding for capture

Limitations:
  - Windows only (DXGI, PrintWindow)
  - Only works for emulators / desktop mirrors (scrcpy window)
  - Not applicable to physical devices over USB/WiFi
  - GPU mode must be 'host' or 'angle' (not swiftshader)
```

```csharp
// C# skeleton: DXGI Desktop Duplication capture interface
public interface IFrameProvider : IDisposable
{
    bool TryGetFrame(out byte[] bgra, out int width, out int height);
}

// DXGI implementation (Windows 8+, DirectX 11)
public class DxgiFrameProvider : IFrameProvider
{
    // Uses SharpDX.DXGI.OutputDuplication to capture GPU surface
    // Typical capture latency: 5-15ms per frame
    public bool TryGetFrame(out byte[] bgra, out int w, out int h) { /* ... */ }
    public void Dispose() { /* release DXGI resources */ }
}

// PrintWindow fallback (older Windows / non-DX apps)
public class PrintWindowProvider : IFrameProvider
{
    // Uses User32.PrintWindow() + GDI BitBlt
    // Captures even minimized windows, but slower (~30-50ms)
    public bool TryGetFrame(out byte[] bgra, out int w, out int h) { /* ... */ }
    public void Dispose() { /* release GDI handles */ }
}
```

## Common Patterns
<!-- RECOMMENDED — real-world usage examples -->

```python
# Coordinate normalization: virtual → real display
def normalize_coords(virt_x, virt_y, virt_w, virt_h, real_w, real_h):
    """Convert virtual display coords to real device coords for minitouch."""
    real_x = int(virt_x * real_w / virt_w)
    real_y = int(virt_y * real_w / virt_h)
    return real_x, real_y

# scrcpy headless H.264 → OpenCV (high-fps pattern)
import subprocess
proc = subprocess.Popen(
    ["scrcpy", "--no-display", "--no-audio", "--max-fps=30", "--max-size=720"],
    stdout=subprocess.PIPE
)
# Decode H.264 stream with FFmpeg or hardware decoder...
```

```text
Capture Method Comparison:

| Method          | Latency   | FPS   | Server? | Multi-device | Notes                          |
|:----------------|:----------|:------|:--------|:-------------|:-------------------------------|
| scrcpy          | 30-80ms   | 30-60 | Yes     | Yes          | Best overall, needs server jar |
| minicap         | 30-60ms   | 20-40 | Yes     | Yes          | JPEG stream, Android 5-9      |
| screenrecord    | 100-300ms | 10-30 | No      | Yes          | H.264 pipe, 180s limit        |
| screencap loop  | 150-500ms | 2-5   | No      | Yes          | Simplest, high latency        |
| DXGI capture    | 5-15ms    | 60+   | No      | No (emu)     | Windows only, ultra-fast       |
| PrintWindow     | 30-50ms   | 20-30 | No      | No (emu)     | Win32 fallback                 |
```

## Gotchas & Breaking Changes
<!-- CRITICAL — things that trip up agents and humans -->

- ⚠️ **scrcpy protocol versioning**: The binary control protocol may change between scrcpy versions. Always pin server/client version when integrating directly.
- ⚠️ **minitouch single-connection**: minitouch only allows one socket connection at a time. Agent must implement a mutex/lock to avoid conflicts in multi-threaded setups.
- ⚠️ **minicap Android 10+ deprecation**: minicap relies on internal SurfaceFlinger APIs that are restricted since Android 10. Use scrcpy or screenrecord for Android 10+.
- ⚠️ **screenrecord 180s limit**: `screenrecord` has a hard 3-minute limit. Agent must implement auto-restart with seamless reconnection.
- ⚠️ **screencap LF/CRLF**: Use `adb exec-out` instead of `adb shell` for screencap to avoid `\r\n` corruption on binary PNG data.
- ⚠️ **DXGI requires DX11**: DXGI Desktop Duplication is only available on Windows 8+ with DirectX 11. Emulators using software rendering (swiftshader) may not expose capturable surfaces.
- ⚠️ **Backpressure on H.264 stream**: Without frame skipping, the decode queue fills up, increasing total latency linearly. Implement ring buffer + skip-frame policy.

## Migration
<!-- MANDATORY if not latest — checklist to upgrade to next version -->

- [ ] Create abstraction `IFrameSource` (scrcpy / minicap / screencap / DXGI) and `IInputSink` (minitouch / adb input / scrcpy control) for swappable backends.
- [ ] Add rate-limit configuration for control events to prevent flooding the control socket.
- [ ] Implement auto-restart for `screenrecord` pseudo-stream with session counter.
- [ ] Add double-buffer or lock-free queue between capture thread and inference thread.

<!--
BM25 DESIGN RULES:
- H1 = library name (root search anchor)
- H2 = feature category
- Code:prose ratio >= 70:30
- Keep 5-30KB per file
-->
