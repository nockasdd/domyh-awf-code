import unreal
import base64
import hmac
import json
import os
import queue
import sys
import threading
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import StringIO

def _load_bridge_config():
    """The bridge server writes this before the editor starts, because this
    script runs inside the editor process and os.environ here is the editor's,
    not the server's. Saved/ is gitignored by Unreal, so the token stays out of
    commits the way a file under Content/Python would not."""
    try:
        saved_dir = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_saved_dir())
        with open(os.path.join(saved_dir, "HSA", "bridge_config.json"), "r") as fh:
            config = json.load(fh)
        return config if isinstance(config, dict) else {}
    except Exception as e:
        unreal.log_warning("[HSA Bridge] No bridge config read (%s). Falling back to environment." % e)
        return {}


_BRIDGE_CONFIG = _load_bridge_config()


def _setting(key, env_name, default, cast):
    raw = os.environ.get(env_name)
    if not raw:
        raw = _BRIDGE_CONFIG.get(key)
    if not raw:
        return default
    try:
        return cast(raw)
    except (TypeError, ValueError):
        unreal.log_warning("[HSA Bridge] Bad value for %s: %r. Using default." % (env_name, raw))
        return default


BRIDGE_HOST = _setting("host", "HSA_UE_BRIDGE_HOST", "127.0.0.1", str)
BRIDGE_PORT = _setting("port", "HSA_UE_BRIDGE_PORT", 30011, int)
BRIDGE_TOKEN = _setting("token", "HSA_BRIDGE_TOKEN", "", str)
MAX_CODE_BYTES = _setting("max_code_bytes", "HSA_UE_MAX_CODE_BYTES", 1024 * 1024, int)
EXEC_TIMEOUT_S = _setting("exec_timeout_s", "HSA_UE_EXEC_TIMEOUT_S", 30.0, float)
PLUGIN_VERSION = "2.2.0"

# Captured before any task can replace sys.stdout. A task that never returns
# leaves the replacement in place, because the restore lives in a finally on the
# thread that is now stuck — which would silently divert the whole editor's
# output into a StringIO that is never flushed. The HTTP threads still run, so
# they are the only ones able to put it back.
_REAL_STDOUT = sys.stdout
_REAL_STDERR = sys.stderr

# Command queue for thread-safe Game Thread execution
request_queue = queue.Queue()

# A user block that never returns takes the Game Thread with it, and no thread in
# this process can preempt it. The recovery is a real timeout in the calling HTTP
# thread, not a flag on the bridge: a flag could only be set from the tick that a
# wedge prevents from ever running again.
WEDGE_CLEAR_FRAMES = _setting("wedge_clear_frames", "HSA_UE_WEDGE_CLEAR_FRAMES", 300, int)
WEDGED = (
    "The Game Thread is still running an execution that exceeded %.0fs and could not "
    "be interrupted, so the editor is unresponsive and this call was abandoned. It is "
    "queued behind that one and will not run. Restart the editor; this cannot be "
    "recovered from inside the process."
    % EXEC_TIMEOUT_S
)


def _deny(detail):
    """Body for a rejected call. Returning it rather than raising keeps the
    reason in the response the agent reads, instead of a bare 401."""
    return {"ok": False, "output": "", "error": detail}


def _restore_std_streams():
    """Put the process streams back from any thread.

    Called at every HTTP entry rather than only when a wedge was detected: a task
    that replaced the streams and then never returns cannot run its own restore,
    and the flag that would tell us so is set on the same stuck thread. The HTTP
    threads keep running, so they are the only place this can be recovered, and
    the identity check makes it a no-op in the normal case.
    """
    if sys.stdout is not _REAL_STDOUT:
        sys.stdout = _REAL_STDOUT
    if sys.stderr is not _REAL_STDERR:
        sys.stderr = _REAL_STDERR


class PythonExecutorHTTPHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress default logging

    def _authorized(self):
        if not BRIDGE_TOKEN:
            return False, "HSA_BRIDGE_TOKEN is not set on the bridge, so no call can be authenticated. Set it on both the editor and the bridge server."
        header = self.headers.get("Authorization", "")
        prefix = "Bearer "
        if not header.startswith(prefix):
            return False, "Missing Authorization: Bearer <HSA_BRIDGE_TOKEN> header"
        # hmac.compare_digest, not ==: a byte-by-byte compare returns early on the
        # first mismatch, which leaks the length of the matching prefix.
        if not hmac.compare_digest(header[len(prefix):], BRIDGE_TOKEN):
            return False, "Invalid HSA_BRIDGE_TOKEN"
        return True, None

    def _respond(self, status, payload):
        body = json.dumps(payload, default=str).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        _restore_std_streams()
        if self.path == '/health':
            # Unauthenticated on purpose: the bridge only has to learn whether the
            # listener is up, and answering this leaks nothing an attacker can act
            # on. It also keeps the liveness probe from counting as an exec.
            self._respond(200, {
                "ok": True,
                "status": "running",
                "version": PLUGIN_VERSION,
                "auth_required": bool(BRIDGE_TOKEN),
                "max_code_bytes": MAX_CODE_BYTES,
                "exec_timeout_s": EXEC_TIMEOUT_S,
                "queue_depth": request_queue.qsize(),
            })
        else:
            self._respond(404, _deny("Unknown path: %s" % self.path))

    def do_POST(self):
        _restore_std_streams()
        if self.path != '/execute':
            self._respond(404, _deny("Unknown path: %s" % self.path))
            return

        authorized, reason = self._authorized()
        if not authorized:
            unreal.log_warning("[HSA Bridge] Rejected unauthenticated /execute: %s" % reason)
            self._respond(401, _deny(reason))
            return

        try:
            content_length = int(self.headers.get('Content-Length', '0'))
        except ValueError:
            self._respond(400, _deny("Invalid Content-Length"))
            return

        # Checked before the body is read so an oversized request is refused
        # without ever buffering it.
        if content_length > MAX_CODE_BYTES:
            self._respond(413, _deny(
                "Request body is %d bytes, limit is %d. Raise HSA_UE_MAX_CODE_BYTES if this is expected."
                % (content_length, MAX_CODE_BYTES)
            ))
            return

        post_data = self.rfile.read(content_length).decode('utf-8')

        try:
            req = json.loads(post_data)
            code_base64 = req.get("code_base64", "")
        except Exception as e:
            self._respond(400, _deny("Malformed JSON: %s" % e))
            return

        if not code_base64:
            self._respond(400, _deny("Missing code_base64"))
            return

        # Create event and result placeholder
        event = threading.Event()
        task = {
            "code_base64": code_base64,
            "event": event,
            "result": None
        }

        # Push to Game Thread
        request_queue.put(task)

        # Wait for Game Thread to process
        if not event.wait(timeout=EXEC_TIMEOUT_S):
            # Only the handler's wait is abandoned. The task stays queued and the
            # tick loop still owns it, so a late result finds an event nobody is
            # listening to and is dropped. WEDGED rather than a bare timeout: if
            # the Game Thread was blocked before this call rather than by it, the
            # queue is where the call now waits forever.
            self._respond(200, _deny(WEDGED))
            return

        result = task["result"]
        if result is None:
            result = _deny("Execution timed out")

        self._respond(200, result)


def start_http_server():
    if not BRIDGE_TOKEN:
        unreal.log_error(
            "[HSA Bridge] Refusing to start without HSA_BRIDGE_TOKEN. Any local process could "
            "otherwise execute arbitrary Python in this editor. Set the same token on the bridge server."
        )
        return
    # Each POST blocks for up to EXEC_TIMEOUT_S waiting on the Game Thread, so a
    # single serving thread would serialise every call and the second one would
    # time out behind the first. The queue is what orders the work, not the server.
    server = ThreadingHTTPServer((BRIDGE_HOST, BRIDGE_PORT), PythonExecutorHTTPHandler)
    server.serve_forever()


# Start background HTTP server
server_thread = threading.Thread(target=start_http_server, daemon=True)
server_thread.start()


def game_thread_tick(delta_time):
    frames = 0
    while not request_queue.empty():
        task = request_queue.get()
        code_base64 = task["code_base64"]

        result = {"ok": False, "output": "", "error": ""}

        started = time.time()
        try:
            code = base64.b64decode(code_base64).decode("utf-8")

            captured_out = StringIO()
            captured_err = StringIO()
            sys.stdout = captured_out
            sys.stderr = captured_err

            try:
                exec_globals = {
                    "__builtins__": __builtins__,
                    "unreal": unreal,
                }
                exec(code, exec_globals)

                result["ok"] = True
                result["output"] = captured_out.getvalue()
                stderr_val = captured_err.getvalue()
                if stderr_val:
                    result["error"] = stderr_val
            finally:
                # Restored via the captured originals rather than the values read
                # at entry: a previous wedged task may have left the replacement
                # in place, and then restoring that would capture it forever.
                sys.stdout = _REAL_STDOUT
                sys.stderr = _REAL_STDERR

        # BaseException, not Exception: SystemExit derives from BaseException, so
        # a bare `sys.exit()` in a user block used to escape this tick entirely
        # and take the editor down with it. The code is untrusted by construction,
        # so the base class is the only one wide enough to hold it.
        except BaseException as e:
            result["ok"] = False
            result["error"] = "%s: %s\n%s" % (type(e).__name__, str(e), traceback.format_exc())

        elapsed = time.time() - started
        # Only reachable if the block returned, so this never fires for the task
        # that actually wedged the thread — nothing reports that one from here,
        # because the thread it would report from is the stuck one.
        if result["ok"] and elapsed > EXEC_TIMEOUT_S:
            unreal.log_warning(
                "[HSA Bridge] execution took %.1fs, over the %.1fs timeout. The tick loop "
                "keeps draining, so a single slow block is survivable, but a block that "
                "never returns is not." % (elapsed, EXEC_TIMEOUT_S)
            )

        # Logged here rather than in the handler: a request that timed out is no
        # longer waiting, but the work still ran, and that is the call worth seeing.
        unreal.log("[HSA Bridge] execute %s %d b64 chars in %.2fs" % (
            "ok" if result["ok"] else "err", len(code_base64), elapsed))
        task["result"] = result
        task["event"].set()
        request_queue.task_done()

        frames += 1
        if frames >= WEDGE_CLEAR_FRAMES:
            # A long queue would otherwise block every frame of a level-open, so
            # the remainder is left for the next tick. Ordering survives because
            # the queue is FIFO.
            return

# Register the Slate Tick to run on Game Thread
unreal.register_slate_post_tick_callback(game_thread_tick)

unreal.log(
    "[HSA Bridge] Python Native HTTP Server v%s on %s:%d - auth=token, cap=%d bytes, timeout=%ss"
    % (PLUGIN_VERSION, BRIDGE_HOST, BRIDGE_PORT, MAX_CODE_BYTES, EXEC_TIMEOUT_S)
    if BRIDGE_TOKEN
    else "[HSA Bridge] Python Native HTTP Server v%s NOT started - no HSA_BRIDGE_TOKEN"
    % PLUGIN_VERSION
)
