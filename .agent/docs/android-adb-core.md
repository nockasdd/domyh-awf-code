---
library: android-adb-core
version: 1
latest: true
category: infra
official_docs: https://android.googlesource.com/platform/system/core/+/master/adb/PROTOCOL.txt
last_updated: 2026-03-26
---

# android-adb-core v1

> ADB core transport protocol, 24-byte header, server text protocol, auth handshake, and essential CLI surfaces for device orchestration.

## Version Comparison
<!-- MANDATORY — helps agent disambiguate versions instantly -->
| Feature                    | v1                    | v{latest} |
|:---------------------------|:----------------------|:----------|
| 24-byte transport header   | struct `adb_msg` in C | —         |
| AUTH & RSA keys            | Host/daemon handshake | —         |
| Server text protocol 5037  | `host:*`, `shell:`    | —         |
| MAX_PAYLOAD                | 256KB (old) / 1MB     | —         |

## Installation
<!-- MANDATORY — exact install commands with version pinning -->
```bash
# Linux
sudo apt-get install android-tools-adb
adb version

# Windows (via scoop)
scoop install adb

# macOS (via homebrew)
brew install android-platform-tools
```

## Configuration
<!-- MANDATORY — complete config example, annotated -->
```bash
# Enable ADB over TCP on device (lab / CI environments only)
adb tcpip 5555
adb connect 192.168.0.10:5555

# Start ADB server on a custom port (advanced, avoid port conflicts)
set ADB_SERVER_PORT=5038   # Windows
export ADB_SERVER_PORT=5038 # Linux/macOS
adb start-server

# List all connected devices with extended info
adb devices -l
# Output: <serial> device product:<name> model:<name> device:<name> transport_id:<N>
```

## Core API
<!-- MANDATORY — most-used APIs with params, types, return values -->

### 24-byte Transport Header (C struct)

Every message between ADB server (host) and daemon (device) over TCP/USB is wrapped in a fixed 24-byte header.

```c
// Source: AOSP system/core/adb/adb.h
typedef struct adb_msg {
    uint32_t command;      // 4B — command ID: 'CNXN', 'AUTH', 'OPEN', 'WRTE', 'OKAY', 'CLSE'
    uint32_t arg0;         // 4B — command-specific argument
    uint32_t arg1;         // 4B — command-specific argument
    uint32_t data_length;  // 4B — payload byte count following this header
    uint32_t data_crc32;   // 4B — CRC32 of payload (or 0 on some builds)
    uint32_t magic;        // 4B — must equal command ^ 0xffffffff
} adb_msg_t;

// Command constants (little-endian encoded ASCII)
#define A_CNXN 0x4e584e43  // 'CNXN' — connection request
#define A_AUTH 0x48545541  // 'AUTH' — authentication challenge/response
#define A_OPEN 0x4e45504f  // 'OPEN' — open a new stream
#define A_WRTE 0x45545257  // 'WRTE' — write data to stream
#define A_OKAY 0x59414b4f  // 'OKAY' — ready for next WRTE
#define A_CLSE 0x45534c43  // 'CLSE' — close stream
```

### Header Validation Logic
```c
bool adb_msg_is_valid(const adb_msg_t* msg) {
    // Magic MUST be command XOR 0xffffffff
    if ((msg->command ^ 0xffffffffu) != msg->magic) return false;
    if (msg->data_length > MAX_PAYLOAD) return false;
    // CRC32 check on payload buffer (optional on some builds)
    return true;
}
```

### Connection Handshake (CNXN & AUTH)

```text
Step 1: Client sends CNXN
  command=A_CNXN  arg0=version(0x01000001)  arg1=MAX_PAYLOAD
  payload="host::features=stat_v2,cmd,shell_v2,..."

Step 2: Daemon replies AUTH type=TOKEN
  command=A_AUTH  arg0=1(TOKEN)
  payload=<20-byte random challenge token>

Step 3: Client replies AUTH type=SIGNATURE
  command=A_AUTH  arg0=2(SIGNATURE)
  payload=RSA_sign(private_key, token)  // ~/.android/adbkey

Step 4a: Daemon accepts → replies CNXN
  command=A_CNXN  arg0=version  arg1=MAX_PAYLOAD
  payload="device::ro.product.model=Pixel_6;..."

Step 4b: Daemon rejects (unknown key) → AUTH type=RSAPUBLICKEY
  command=A_AUTH  arg0=3(RSAPUBLICKEY)
  payload=<public key data>
  // Triggers "Allow USB debugging?" dialog on device
```

### Server Text Protocol (Port 5037)

Language bindings (Python, C#, Go) communicate with the ADB server via local TCP port 5037 using a length-prefixed ASCII text protocol.

```text
# Format: <4-hex-digit-length><payload>
# Response: "OKAY"<4-hex-digit-length><data> or "FAIL"<4-hex-digit-length><error>

# Query server version
Client → Server: "000Chost:version"
Server → Client: "OKAY00040029"

# List devices with extended info
Client → Server: "000Ehost:devices-l"
Server → Client: "OKAY004Aemulator-5554 device product:sdk_gphone64..."

# Select transport (device) by serial
Client → Server: "001Ahost:transport:emulator-5554"
Server → Client: "OKAY"

# Open shell stream on selected transport
Client → Server: "0006shell:"
Server → Client: "OKAY"
# Now enters WRTE/OKAY binary streaming loop
```

```python
# Python: raw ADB server text protocol client
import socket

def adb_server_request(host: str, port: int, payload: str) -> bytes:
    """Send a text-protocol request to ADB server and return response."""
    sock = socket.create_connection((host, port))
    length_prefix = f"{len(payload):04x}".encode("ascii")
    sock.sendall(length_prefix + payload.encode("ascii"))
    status = sock.recv(4)  # b'OKAY' or b'FAIL'
    if status == b"OKAY":
        resp_len = int(sock.recv(4).decode("ascii"), 16)
        data = sock.recv(resp_len)
        sock.close()
        return data
    else:
        resp_len = int(sock.recv(4).decode("ascii"), 16)
        error = sock.recv(resp_len)
        sock.close()
        raise RuntimeError(f"ADB FAIL: {error.decode()}")

# Usage
version = adb_server_request("127.0.0.1", 5037, "host:version")
devices = adb_server_request("127.0.0.1", 5037, "host:devices-l")
```

### Stream Lifecycle (OPEN → WRTE → OKAY → CLSE)

```text
# After transport selection, open a service stream:
Client → Daemon: OPEN(local_id=1, remote_id=0, "shell:ls /sdcard")
Daemon → Client: OKAY(remote_id=42, local_id=1)

# Data flows via WRTE/OKAY pairs (flow control):
Daemon → Client: WRTE(remote_id=42, local_id=1, payload="file1.txt\nfile2.jpg\n")
Client → Daemon: OKAY(local_id=1, remote_id=42)  # ACK: ready for more

# Stream close:
Daemon → Client: CLSE(remote_id=42, local_id=1)
Client → Daemon: CLSE(local_id=1, remote_id=42)
```

## Common Patterns
<!-- RECOMMENDED — real-world usage examples -->

```bash
# Activity Manager (am): launch app without UI click
adb -s <serial> shell am start -n com.example.app/.MainActivity

# Broadcast intent for automation trigger
adb -s <serial> shell am broadcast -a com.example.ACTION_START_BOT

# Package Manager (pm): disable / enable app
adb -s <serial> shell pm disable-user --user 0 com.facebook.katana
adb -s <serial> shell pm clear com.example.app

# Window Manager (wm): query / set display size and density
adb -s <serial> shell wm size
adb -s <serial> shell wm size 1080x1920
adb -s <serial> shell wm density 420

# Settings: toggle developer options
adb -s <serial> shell settings put global animator_duration_scale 0
adb -s <serial> shell settings put global debug_view_attributes 1

# Input: raw touch/key events
adb -s <serial> shell input tap 500 700
adb -s <serial> shell input swipe 300 1000 300 300 200
adb -s <serial> shell input keyevent KEYCODE_HOME
```

```python
# Pattern: multi-device round-robin via host:devices-l
def get_all_serials() -> list[str]:
    raw = adb_server_request("127.0.0.1", 5037, "host:devices-l")
    lines = raw.decode().strip().split("\n")
    return [line.split()[0] for line in lines if "device" in line]

def run_on_all(cmd: str):
    for serial in get_all_serials():
        adb_server_request("127.0.0.1", 5037, f"host:transport:{serial}")
        # then open shell stream with cmd...
```

## Gotchas & Breaking Changes
<!-- CRITICAL — things that trip up agents and humans -->
<!-- Use ⚠️ markers for version-specific warnings -->

- ⚠️ **data_crc32 may be zero** on some older builds — agent must NOT hard-fail if CRC32 is unused. Validate magic field first instead.
- ⚠️ **Magic field is mandatory**: `command ^ 0xffffffff`. Wrong magic → immediate connection drop causing desync.
- ⚠️ **MAX_PAYLOAD varies**: 4KB on very old ADB, 256KB on Android 5-6, 1MB on modern ADB. Always buffer-slice when pushing large files via `sync:`.
- ⚠️ **`host:transport-any`** may pick a random device when multiple are connected. Always use `host:transport:<serial>` explicitly for deterministic targeting.
- ⚠️ **Line ending differences**: `adb shell` translates `\n` to `\r\n` on older ADB. Use `adb exec-out` for binary-safe output or `shell,v2,raw:` for shell v2.

## Migration
<!-- MANDATORY if not latest — checklist to upgrade to next version -->

- [ ] Audit all places that parse the 24-byte header — ensure they handle new fields without breaking alignment.
- [ ] Standardize error handling: when receiving `FAIL` from server port 5037, log the full payload error string.
- [ ] Add metrics for OPEN/WRTE/CLSE stream counts to debug connection leaks.
- [ ] Migrate from `adb shell` to `adb exec-out` for binary-safe screencap / file pull pipelines.

<!--
BM25 DESIGN RULES:
- H1 = library name (root search anchor)
- H2 = feature category, add (vN) suffix for version matching
- Code:prose ratio >= 70:30
- Use ⚠️ diff notes for version disambiguation
- Keep 5-30KB per file, H2 sections ~50 lines each
-->
