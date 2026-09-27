"""HSA Blender Bridge add-on.

Listens on localhost, runs commands on Blender's main thread, and caps what it
hands back. Three things here are deliberate and are the reason this add-on
exists rather than a `exec` over a raw socket:

1. `bpy` is not thread-safe. Socket threads only enqueue; the timer registered
   with `bpy.app.timers` is the only thing that touches the scene. A handler that
   reads `bpy.data` from the socket thread corrupts state in ways that only show
   up later, and blaming the bridge then costs hours.
2. stdout is bounded where it is produced. A print loop cannot be stopped after
   the fact without first paying for the string, so the cap sits in the writer.
3. Every response is framed (4-byte big-endian length + JSON) and carries
   truncation metadata. A reader that guesses where a message ends cannot tell a
   partial reply from a slow one, and will sit on a dead socket until its own
   timeout.
"""

bl_info = {
    "name": "HSA Blender Bridge",
    "author": "NockDev",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > HSA",
    "description": "Command queue for the HSA MCP bridge",
    "category": "Development",
}

import bpy
import hmac
import io
import json
import os
import queue
import secrets
import socket
import struct
import sys
import threading
import time
import traceback

PROTOCOL_VERSION = 1
DEFAULT_PORT = 28782
MAX_FRAME_BYTES = 32 * 1024 * 1024
STDOUT_CAP_BYTES = 24_000
QUEUE_DEADLINE_S = 120.0
POLL_INTERVAL_S = 0.05
TIMER_NAME = "hsa_bridge_drain"


class BridgeError(RuntimeError):
    """A failure the caller can see and act on, not a socket reset."""


# ─── framing ─────────────────────────────────────────────────────────────────
# 4-byte big-endian length then UTF-8 JSON. Length framing is what makes a slow
# reply distinguishable from a truncated one.

def send_frame(sock, payload):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    if len(body) > MAX_FRAME_BYTES:
        body = json.dumps({
            "ok": False,
            "error": "response exceeds the %d-byte frame limit" % MAX_FRAME_BYTES,
        }).encode("utf-8")
    sock.sendall(struct.pack(">I", len(body)) + body)


def recv_exactly(sock, count):
    chunks = []
    remaining = count
    while remaining > 0:
        chunk = sock.recv(min(remaining, 65536))
        if not chunk:
            raise BridgeError("connection closed after %d of %d bytes" % (count - remaining, count))
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def recv_frame(sock):
    header = recv_exactly(sock, 4)
    (length,) = struct.unpack(">I", header)
    if length > MAX_FRAME_BYTES:
        raise BridgeError("declared frame of %d bytes exceeds the limit" % length)
    return json.loads(recv_exactly(sock, length).decode("utf-8"))


# ─── bounded stdout ──────────────────────────────────────────────────────────

class BoundedWriter(io.TextIOBase):
    """Counts what it drops, because "we cut it off" and "it printed nothing"
    are the same string to the caller and must not be."""

    def __init__(self, limit_bytes):
        self._parts = []
        self._bytes = 0
        self._limit = limit_bytes
        self.dropped = 0

    def write(self, text):
        if not text:
            return 0
        chunk = text.encode("utf-8", "replace")
        if self._bytes + len(chunk) <= self._limit:
            self._parts.append(text)
            self._bytes += len(chunk)
            return len(text)
        room = self._limit - self._bytes
        if room > 0:
            # "ignore" drops a partial trailing character rather than emitting
            # a replacement char for it.
            head = chunk[:room].decode("utf-8", "ignore")
            if head:
                self._parts.append(head)
                self._bytes += len(head.encode("utf-8"))
        self.dropped += len(chunk) - min(room, len(chunk))
        return len(text)

    def getvalue(self):
        return "".join(self._parts)


# ─── the bridge ──────────────────────────────────────────────────────────────

class HSABridge:
    def __init__(self, port, token):
        self.port = port
        self.token = token
        self._server = None
        self._thread = None
        self._queue = queue.Queue()
        self._stop = threading.Event()
        self._timer_registered = False
        self._log = io.StringIO()

    # -- lifecycle --

    def start(self):
        if self._server is not None:
            raise BridgeError("bridge already listening on port %d" % self.port)
        if not self.token:
            raise BridgeError("no token configured")

        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # SO_REUSEADDR only: on Windows this also allows a hijack of the port by
        # another process, and the token is what actually authenticates.
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            srv.bind(("127.0.0.1", self.port))
        except OSError as exc:
            srv.close()
            raise BridgeError("cannot bind port %d: %s" % (self.port, exc))
        srv.listen(8)
        srv.settimeout(0.5)

        self._server = srv
        self._stop.clear()
        self._thread = threading.Thread(target=self._accept_loop, name="hsa-bridge-accept", daemon=True)
        self._thread.start()
        self._ensure_timer()
        self._write_log("listening on 127.0.0.1:%d" % self.port)

    def stop(self):
        self._stop.set()
        if self._server is not None:
            try:
                self._server.close()
            except OSError:
                pass
            self._server = None
        if bpy.app.timers.is_registered(TIMER_NAME):
            bpy.app.timers.unregister(TIMER_NAME)
        self._timer_registered = False
        self._write_log("stopped")

    def is_running(self):
        return self._server is not None

    def _write_log(self, line):
        stamp = time.strftime("%H:%M:%S")
        self._log.write("%s %s\n" % (stamp, line))
        print("[HSA Bridge] %s" % line)

    def _ensure_timer(self):
        # persistent=True: the timer must survive a file load, otherwise the
        # bridge goes deaf after the first Save and the caller sees timeouts
        # that look like a Blender hang.
        if not bpy.app.timers.is_registered(TIMER_NAME):
            bpy.app.timers.register(self._drain, first_interval=POLL_INTERVAL_S, persistent=True)
        self._timer_registered = True

    # -- accept thread: enqueue only, never touch bpy --

    def _accept_loop(self):
        while not self._stop.is_set():
            try:
                conn, _addr = self._server.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            threading.Thread(
                target=self._read_loop, args=(conn,), name="hsa-bridge-conn", daemon=True
            ).start()
        self._write_log("accept loop exited")

    def _read_loop(self, conn):
        conn.settimeout(10.0)
        try:
            request = recv_frame(conn)
        except (BridgeError, OSError, ValueError) as exc:
            _safe_send(conn, {"ok": False, "error": str(exc)})
            _close(conn)
            return

        refusal = self._refuse_reason(request)
        if refusal:
            # A rejected connection gets no queue slot: an unauthenticated
            # caller must not be able to occupy the main thread.
            _safe_send(conn, {"ok": False, "error": refusal})
            _close(conn)
            return

        conn.settimeout(300.0)
        self._queue.put((time.monotonic(), request, conn))

    def _refuse_reason(self, request):
        """The reason to turn this request away, or '' to accept it.

        Truthy-means-reject so the call site cannot invert the gate by accident:
        the previous shape returned an error dict on failure and None on
        success, and reading it backwards let every wrong token through.
        """
        if not isinstance(request, dict):
            return "request must be a JSON object"
        if not hmac.compare_digest(str(request.get("token", "")), self.token):
            return "unauthorized"
        if not request.get("command"):
            return "missing command"
        return ""

    # -- main thread: the only place bpy is touched --

    def _drain(self):
        try:
            deadline = time.monotonic() + 1.0
            while time.monotonic() < deadline:
                try:
                    queued = self._queue.get_nowait()
                except queue.Empty:
                    break
                self._serve(queued)
        except Exception as exc:
            # _serve already absorbs per-request failures, so reaching here means
            # the transport itself misbehaved. Tearing the listener down would
            # turn one bad frame into a dead bridge, so the listener stays up
            # and the fault is reported instead.
            self._write_log("drain error: %r" % (exc,))
        return POLL_INTERVAL_S if self.is_running() else None

    def _serve(self, queued):
        enqueued_at, request, conn = queued
        if self._stop.is_set():
            _close(conn)
            return
        waited = time.monotonic() - enqueued_at
        if waited > QUEUE_DEADLINE_S:
            # Refuse rather than answer a question asked 2 minutes ago about a
            # scene the caller has since changed.
            _safe_send(conn, {
                "ok": False,
                "error": "request waited %.1fs in the queue and was refused" % waited,
            })
            _close(conn)
            return

        command = request.get("command")
        params = request.get("params") or {}
        try:
            result = self._dispatch(command, params)
        except BridgeError as exc:
            result = {"ok": False, "error": str(exc)}
        except Exception:
            result = {"ok": False, "error": "unhandled", "traceback": traceback.format_exc()[-2000:]}

        result["elapsed_ms"] = int((time.monotonic() - enqueued_at) * 1000)
        _safe_send(conn, result)
        _close(conn)

    def _dispatch(self, command, params):
        # Health is answered without exec so a caller can prove the link is
        # alive without being able to run anything.
        if command == "health":
            return {"ok": True, "protocol": PROTOCOL_VERSION, "stdout_cap_bytes": STDOUT_CAP_BYTES}
        if command == "verify":
            # Reports the four things every later call depends on: version,
            # main-thread identity, the exec path, and the stdout cap. Without
            # it a misconfigured add-on looks identical to an empty scene until
            # something is built on top of it.
            probe = self._execute_code({
                "code": "import threading\n"
                        "_result = {\n"
                        "  'blender': bpy.app.version_string,\n"
                        "  'thread_is_main': threading.current_thread() is threading.main_thread(),\n"
                        "  'objects': len(bpy.data.objects),\n"
                        "  'scene': bpy.context.scene.name,\n"
                        "}\n"
                        "print('hsa bridge verify')",
                "stdout_cap_bytes": 4096,
            })
            probe["ok"] = bool(probe.get("ok"))
            return probe
        if command == "execute_code":
            return self._execute_code(params)
        raise BridgeError("unknown command %r" % (command,))

    def _execute_code(self, params):
        code = params.get("code")
        if not isinstance(code, str) or not code.strip():
            raise BridgeError("code must be a non-empty string")

        cap = params.get("stdout_cap_bytes", STDOUT_CAP_BYTES)
        cap = max(0, min(int(cap), MAX_FRAME_BYTES))

        buffer = BoundedWriter(cap)
        namespace = {
            "bpy": bpy,
            "__name__": "hsa_bridge_exec",
        }

        stdout_fd, stderr_fd = sys.stdout, sys.stderr
        sys.stdout = sys.stderr = buffer
        returned = None
        try:
            exec(compile(code, "<hsa-bridge>", "exec"), namespace)
            returned = namespace.get("_result")
        except Exception as exc:
            # The exception text goes through the same bounded writer, so a
            # traceback referencing a 1MB string cannot escape the cap.
            traceback.print_exc(file=buffer)
            result = {
                "ok": False,
                "error": "%s: %s" % (type(exc).__name__, exc),
                "stdout": buffer.getvalue(),
                "stdout_bytes": buffer._bytes,
                "stdout_truncated": buffer.dropped > 0,
                "stdout_bytes_dropped": buffer.dropped,
            }
            return result
        finally:
            sys.stdout, sys.stderr = stdout_fd, stderr_fd

        text = buffer.getvalue()
        return {
            "ok": True,
            "result": _jsonable(returned),
            "stdout": text,
            "stdout_bytes": buffer._bytes,
            "stdout_truncated": buffer.dropped > 0,
            "stdout_bytes_dropped": buffer.dropped,
        }


def _jsonable(value):
    """Reduce a returned value to something JSON can carry.

    A bpy object is the usual thing a script returns and JSON cannot encode one,
    so describe it rather than failing the whole call.
    """
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    name = getattr(value, "name", None)
    rna_type = getattr(value, "bl_rna", None)
    return {
        "repr": repr(value)[:200],
        "name": str(name) if isinstance(name, str) else None,
        "rna_type": rna_type.identifier if rna_type is not None else None,
    }


def _safe_send(conn, payload):
    try:
        send_frame(conn, payload)
    except OSError:
        pass


def _close(conn):
    # close() only. shutdown() before it discards the receive buffer and makes
    # Windows reset the connection, which loses a response that sendall already
    # handed to the kernel — the caller then sees a truncated frame, not a
    # closed one, and blames the wrong process.
    try:
        conn.close()
    except OSError:
        pass


# ─── preferences + operators ─────────────────────────────────────────────────

class HSAAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    port: bpy.props.IntProperty(
        name="Port", default=DEFAULT_PORT, min=1024, max=65535
    )
    token: bpy.props.StringProperty(
        name="Token", default="", subtype="PASSWORD",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "port")
        layout.prop(self, "token")
        layout.label(text="Generate: python -c \"import secrets;print(secrets.token_urlsafe(24))\"")


def _prefs(context):
    return context.preferences.addons[__name__].preferences


class HSA_OT_start(bpy.types.Operator):
    bl_idname = "hsa_bridge.start"
    bl_label = "Start HSA Bridge"
    bl_description = "Listen for HSA MCP bridge connections"

    def execute(self, context):
        prefs = _prefs(context)
        if not prefs.token:
            # A default shared secret would make the port effectively public to
            # anything running on this machine, so there is no default.
            self.report({"ERROR"}, "Set a token in the add-on preferences first")
            return {"CANCELLED"}
        bridge = _resolve_bridge()
        if not bridge.token:
            bridge.token = prefs.token
        try:
            bridge.start()
        except BridgeError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        return {"FINISHED"}


class HSA_OT_stop(bpy.types.Operator):
    bl_idname = "hsa_bridge.stop"
    bl_label = "Stop HSA Bridge"
    bl_description = "Stop listening for HSA MCP bridge connections"

    def execute(self, context):
        _get_bridge().stop()
        return {"FINISHED"}


_BRIDGE = None


CONFIG_PATH = os.path.join(
    os.environ.get("HSA_NOCKDEV_HOME", os.path.expanduser("~")),
    ".nockdev",
    "blender-bridge.json",
)


def _config_file_bridge():
    """The port and token the Node bridge published, or None.

    The bridge writes this file on startup precisely so a Blender that was
    already open can pick the values up without being relaunched. Reading it is
    what makes that work: without a reader, the bridge generates a token, writes
    it here, and then rejects an add-on holding a different one — the two never
    agree and the handshake cannot complete on its own.
    """
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as handle:
            parsed = json.load(handle)
    except (OSError, ValueError):
        return None
    port = parsed.get("port")
    token = parsed.get("token")
    if not isinstance(port, int) or not isinstance(token, str) or not token:
        return None
    return port, token


def _resolve_bridge():
    """Build the bridge from the environment on first use.

    Env rather than UI preferences: the MCP side launches Blender with a port
    and token already exported, and an operator that has to be clicked cannot
    be part of an automated handshake.
    """
    global _BRIDGE
    if _BRIDGE is None:
        _BRIDGE = HSABridge(int(os.environ.get("HSA_BLENDER_PORT", DEFAULT_PORT)), "")

    # A bridge built before the config file existed holds no token, so the
    # values are looked up again — but they are adopted into the same object
    # rather than a new one. Replacing it would leave every existing holder
    # (the autostart timer, a caller's _on_load_post) pointing at a bridge that
    # is not the one listening, and nothing would ever drain its queue.
    if _BRIDGE.token:
        return _BRIDGE

    env_token = os.environ.get("HSA_BLENDER_TOKEN", "")
    if env_token:
        _BRIDGE.port = int(os.environ.get("HSA_BLENDER_PORT", _BRIDGE.port))
        _BRIDGE.token = env_token
        return _BRIDGE

    published = _config_file_bridge()
    if published is not None:
        _BRIDGE.port, _BRIDGE.token = published
        return _BRIDGE

    return _BRIDGE


def _autostart():
    """Start listening as soon as there is a token, however it turned up.

    Blender is usually already open when the bridge starts, so the config file
    the bridge publishes does not exist yet at register() time. Polling is what
    closes that gap; it stops on the first token rather than running forever,
    because a bridge with no token is a deliberate configuration, not a state
    worth watching for.
    """
    try:
        bridge = _resolve_bridge()
        if not bridge.token:
            return 2.0
        if not bridge.is_running():
            bridge.start()
        return None
    except BridgeError as exc:
        print("[HSA Bridge] autostart failed: %s" % exc)
        return None


@bpy.app.handlers.persistent
def _on_load_post(_dummy):
    # bpy.app.timers registrations are cleared by some load paths; re-register
    # so a bridge started before a Save is still answering afterwards.
    bridge = _resolve_bridge()
    if bridge.is_running():
        bridge._ensure_timer()


_CLASSES = (HSAAddonPreferences, HSA_OT_start, HSA_OT_stop)


def register():
    for cls in _CLASSES:
        bpy.utils.register_class(cls)
    if _on_load_post not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(_on_load_post)

    # A bridge with a token starts itself: an IDE harness that launches Blender
    # has no way to click "Start", and a token is what proves one is there. The
    # token can come from the env or from the file the bridge publishes, and the
    # file usually lands after register(), so this keeps retrying until one does.
    bpy.app.timers.register(_autostart, first_interval=0.5, persistent=True)


def unregister():
    if _BRIDGE is not None:
        _BRIDGE.stop()
    for cls in reversed(_CLASSES):
        bpy.utils.unregister_class(cls)
    if _on_load_post in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(_on_load_post)
    # _autostart outliving unregister() means a disabled add-on still polls for
    # a token and re-opens the socket, and a re-enable registers it a second
    # time. Blender keeps firing it either way, so the stop has to be explicit.
    if bpy.app.timers.is_registered(_autostart):
        bpy.app.timers.unregister(_autostart)


if __name__ == "__main__":
    register()
