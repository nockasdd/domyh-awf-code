"""Logic tests for the Blender bridge.

Blender is not a test dependency and is not installed in CI, so `bpy` is
stubbed here and the tests cover the parts that decide what the caller sees:
the stdout cap, the framing, the auth gate, and the queue deadline.

The socket plumbing is exercised against a real loopback socket, because
"it returns the right dict" is not the claim under test — "the reply arrives
whole" is, and a mock would not notice a framing bug.

Run: python test_bridge_logic.py
"""

import json
import os
import shutil
import socket
import struct
import sys
import tempfile
import threading
import types
import unittest

ADDON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "addon")
sys.path.insert(0, ADDON_DIR)

# bpy stub: the add-on touches bpy.props at import time and bpy.app.timers when
# running. Only the surfaces used at import need to exist and behave.
bpy = types.ModuleType("bpy")


class _Prop:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


bpy.props = types.SimpleNamespace(
    IntProperty=_Prop, StringProperty=_Prop, BoolProperty=_Prop
)


class _Timers:
    def __init__(self):
        self.registered = {}
        self.ran = []

    def register(self, fn, first_interval=0.0, persistent=False):
        self.registered[fn.__name__] = fn

    def unregister(self, name):
        self.registered.pop(name, None)

    def is_registered(self, name):
        return name in self.registered


class _App:
    def __init__(self):
        self.timers = _Timers()
        self.version_string = "4.2.1"


bpy.app = _App()
bpy.types = types.SimpleNamespace(AddonPreferences=object, Operator=object)
bpy.utils = types.SimpleNamespace(register_class=lambda c: None, unregister_class=lambda c: None)
bpy.app.handlers = types.SimpleNamespace(
    persistent=lambda fn: fn,
    load_post=types.SimpleNamespace(
        append=lambda fn: None,
        is_registered=lambda fn: False,
        remove=lambda fn: None,
    )
)
bpy.context = types.SimpleNamespace(
    scene=types.SimpleNamespace(name="Scene"),
    preferences=types.SimpleNamespace(addons={}),
)
bpy.data = types.SimpleNamespace(objects=[])

sys.modules.setdefault("bpy", bpy)

import hsa_blender_addon as addon  # noqa: E402


def free_port():
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


def send_request(port, token, command, params=None, timeout=10.0):
    """One request, one reply, over a real socket with real framing."""
    payload = {"token": token, "command": command, "params": params or {}}
    body = json.dumps(payload).encode("utf-8")
    with socket.create_connection(("127.0.0.1", port), timeout=timeout) as sock:
        sock.settimeout(timeout)
        sock.sendall(struct.pack(">I", len(body)) + body)
        header = b""
        while len(header) < 4:
            chunk = sock.recv(4 - len(header))
            if not chunk:
                raise AssertionError("connection closed before the length header")
            header += chunk
        (length,) = struct.unpack(">I", header)
        buf = b""
        while len(buf) < length:
            chunk = sock.recv(length - len(buf))
            if not chunk:
                raise AssertionError("connection closed after %d of %d bytes" % (len(buf), length))
            buf += chunk
        return json.loads(buf.decode("utf-8"))


class TestBoundedWriter(unittest.TestCase):
    """The cap is the feature. A cap that does not report is a silent lie."""

    def test_short_output_passes_through_untouched(self):
        w = addon.BoundedWriter(1000)
        w.write("hello")
        self.assertEqual(w.getvalue(), "hello")
        self.assertEqual(w.dropped, 0)

    def test_output_over_the_cap_is_cut_and_the_loss_is_counted(self):
        w = addon.BoundedWriter(10)
        w.write("x" * 100)
        self.assertEqual(len(w.getvalue()), 10)
        self.assertEqual(w.dropped, 90)

    def test_accumulates_across_writes_until_the_cap(self):
        w = addon.BoundedWriter(10)
        for _ in range(5):
            w.write("xxxx")
        self.assertEqual(len(w.getvalue()), 10)
        self.assertEqual(w.dropped, 10)

    def test_multi_byte_characters_are_not_split_into_replacement_chars(self):
        # "é" is 2 bytes; a cap of 3 admits one and half of another. Emitting
        # the half would produce U+FFFD and corrupt the caller's text.
        w = addon.BoundedWriter(3)
        w.write("ééé")
        self.assertNotIn("�", w.getvalue())
        self.assertLessEqual(len(w.getvalue().encode("utf-8")), 3)

    def test_dropped_count_uses_bytes_not_characters(self):
        w = addon.BoundedWriter(4)
        w.write("é" * 10)
        self.assertEqual(w.dropped, 16)

    def test_a_cap_of_zero_writes_nothing_but_still_reports(self):
        w = addon.BoundedWriter(0)
        w.write("anything")
        self.assertEqual(w.getvalue(), "")
        self.assertEqual(w.dropped, 8)

    def test_empty_write_is_a_no_op(self):
        w = addon.BoundedWriter(10)
        self.assertEqual(w.write(""), 0)
        self.assertEqual(w.dropped, 0)


class TestFraming(unittest.TestCase):
    def test_round_trip(self):
        port = free_port()
        left, right = socket.socketpair()
        try:
            addon.send_frame(left, {"ok": True, "result": "héllo"})
            self.assertEqual(addon.recv_frame(right), {"ok": True, "result": "héllo"})
        finally:
            left.close()
            right.close()

    def test_a_large_reply_arrives_whole(self):
        # recv_exactly loops because recv() is free to return short; without
        # the loop a 40k reply is silently cut at whatever the buffer boundary
        # happened to be.
        port = free_port()
        left, right = socket.socketpair()
        try:
            payload = {"ok": True, "stdout": "x" * 40000}
            addon.send_frame(left, payload)
            self.assertEqual(addon.recv_frame(right), payload)
        finally:
            left.close()
            right.close()

    def test_a_reply_larger_than_the_frame_limit_is_replaced_not_truncated(self):
        left, right = socket.socketpair()
        try:
            addon.send_frame(left, {"ok": True, "stdout": "x" * (addon.MAX_FRAME_BYTES + 10)})
            reply = addon.recv_frame(right)
            self.assertFalse(reply["ok"])
            self.assertIn("frame limit", reply["error"])
        finally:
            left.close()
            right.close()

    def test_a_closed_connection_is_an_error_not_a_short_read(self):
        left, right = socket.socketpair()
        left.close()
        try:
            with self.assertRaises(addon.BridgeError) as ctx:
                addon.recv_frame(right)
            self.assertIn("connection closed", str(ctx.exception))
        finally:
            right.close()

    def test_an_oversized_declaration_is_refused_before_allocating(self):
        left, right = socket.socketpair()
        try:
            left.sendall(struct.pack(">I", addon.MAX_FRAME_BYTES + 1))
            with self.assertRaises(addon.BridgeError) as ctx:
                addon.recv_frame(right)
            self.assertIn("exceeds the limit", str(ctx.exception))
        finally:
            left.close()
            right.close()


class TestAuth(unittest.TestCase):
    """The socket is unauthenticated transport; the token is the gate."""

    def setUp(self):
        self.bridges = []
        self.pumps = []

    def tearDown(self):
        # Stop the bridges first: the pump loop exits on is_running(), and a
        # plain Thread has no stop() to interrupt a live drain.
        for b in self.bridges:
            b.stop()
        for p in self.pumps:
            p.join(timeout=2.0)

    def start(self, token="correct-horse"):
        """A real listener plus the drain timer Blender would run.

        Nothing in Blender calls _drain here, so without the pump every request
        would sit in the queue and the test would be asserting on a timeout.
        """
        port = free_port()
        bridge = addon.HSABridge(port, token)
        bridge.start()
        self.bridges.append(bridge)
        pump = threading.Thread(target=self._pump, args=(bridge,), daemon=True)
        pump.start()
        self.pumps.append(pump)
        return port

    @staticmethod
    def _pump(bridge):
        import time as _time
        while bridge.is_running():
            bridge._drain()
            _time.sleep(0.01)

    def bridge_for(self, port):
        return self.bridges[-1]

    def test_wrong_token_is_refused(self):
        port = self.start()
        reply = send_request(port, "wrong", "health")
        self.assertFalse(reply["ok"])
        self.assertEqual(reply["error"], "unauthorized")

    def test_missing_token_is_refused(self):
        port = self.start()
        reply = send_request(port, "", "health")
        self.assertEqual(reply["error"], "unauthorized")

    def test_a_refused_request_never_runs(self):
        # Otherwise an unauthenticated caller can run code on the scene.
        port = self.start()
        send_request(port, "wrong", "execute_code", {"code": "print('executed')"})
        self.assertTrue(self.bridge_for(port)._queue.empty())

    def test_a_refused_request_does_not_kill_the_listener(self):
        port = self.start()
        send_request(port, "wrong", "health")
        # The timer, not the accept thread, is what Blender's main loop runs;
        # if it returned None here the bridge would go deaf.
        self.assertIsNotNone(self.bridge_for(port)._drain())
        self.assertTrue(self.bridge_for(port).is_running())
        self.assertTrue(send_request(port, "correct-horse", "health")["ok"])

    def test_start_refuses_to_listen_without_a_token(self):
        port = free_port()
        with self.assertRaises(addon.BridgeError) as ctx:
            addon.HSABridge(port, "").start()
        self.assertIn("token", str(ctx.exception))

    def test_a_non_object_request_is_refused(self):
        port = self.start()
        body = json.dumps([1, 2, 3]).encode("utf-8")
        with socket.create_connection(("127.0.0.1", port), timeout=5) as sock:
            sock.sendall(struct.pack(">I", len(body)) + body)
            sock.settimeout(5)
            header = sock.recv(4)
            (length,) = struct.unpack(">I", header)
            reply = json.loads(sock.recv(length).decode("utf-8"))
        self.assertIn("JSON object", reply["error"])

    def test_a_request_with_no_command_is_refused(self):
        port = self.start()
        reply = send_request(port, "correct-horse", "")
        self.assertIn("missing command", reply["error"])

    def test_health_answers_over_a_real_socket(self):
        port = self.start()
        reply = send_request(port, "correct-horse", "health")
        self.assertTrue(reply["ok"])
        self.assertEqual(reply["protocol"], addon.PROTOCOL_VERSION)

    def test_execute_code_answers_over_a_real_socket(self):
        # The whole path: framing in, main-thread exec, framing out.
        port = self.start()
        reply = send_request(port, "correct-horse", "execute_code", {"code": "print('hi')"})
        self.assertTrue(reply["ok"])
        self.assertEqual(reply["stdout"].strip(), "hi")
        self.assertGreater(reply["elapsed_ms"], 0)


class TestQueueDeadline(unittest.TestCase):
    def setUp(self):
        self.bridge = addon.HSABridge(free_port(), "t")

    def test_a_request_that_waited_too_long_is_refused(self):
        # Answering a question asked two minutes ago about a scene the caller
        # has since changed is worse than not answering.
        sent = _FakeSocket()
        self.bridge._queue.put((_ago(addon.QUEUE_DEADLINE_S + 5), {"command": "health"}, sent))
        self.bridge._drain()
        self.assertFalse(sent.payload["ok"])
        self.assertIn("refused", sent.payload["error"])

    def test_a_request_just_inside_the_deadline_is_still_served(self):
        sent = _FakeSocket()
        self.bridge._queue.put((_ago(addon.QUEUE_DEADLINE_S - 1), {"command": "health"}, sent))
        self.bridge._drain()
        self.assertTrue(sent.payload["ok"])
        self.assertEqual(sent.payload["protocol"], addon.PROTOCOL_VERSION)

    def test_a_fresh_request_is_served(self):
        sent = _FakeSocket()
        self.bridge._queue.put((_ago(0.0), {"command": "health"}, sent))
        self.bridge._drain()
        self.assertTrue(sent.payload["ok"])

    def test_a_failed_request_does_not_stop_the_next_one(self):
        # _serve absorbs failures per request; if it did not, one bad script
        # would strand everything queued behind it.
        bad = _FakeSocket()
        good = _FakeSocket()
        self.bridge._queue.put((_ago(0.0), {"command": "no_such_command"}, bad))
        self.bridge._queue.put((_ago(0.0), {"command": "health"}, good))
        self.bridge._drain()
        self.assertFalse(bad.payload["ok"])
        self.assertTrue(good.payload["ok"])


def _ago(seconds):
    import time as _time
    return _time.monotonic() - seconds


class _FakeSocket:
    def __init__(self):
        self.payload = None
        self.written = b""

    def sendall(self, data):
        self.written += data
        (length,) = struct.unpack(">I", data[:4])
        self.payload = json.loads(data[4:4 + length].decode("utf-8"))

    def shutdown(self, *args):
        pass

    def close(self):
        pass


class TestDispatch(unittest.TestCase):
    def setUp(self):
        self.bridge = addon.HSABridge(free_port(), "t")

    def test_unknown_command_names_itself(self):
        with self.assertRaises(addon.BridgeError) as ctx:
            self.bridge._dispatch("rm -rf", {})
        self.assertIn("rm -rf", str(ctx.exception))

    def test_execute_code_needs_actual_code(self):
        for bad in ["", "   ", None, 42]:
            with self.subTest(code=bad):
                with self.assertRaises(addon.BridgeError):
                    self.bridge._execute_code({"code": bad})

    def test_execute_code_returns_stdout_with_its_size(self):
        reply = self.bridge._execute_code({"code": "print('hi')"})
        self.assertTrue(reply["ok"])
        self.assertEqual(reply["stdout"].strip(), "hi")
        self.assertEqual(reply["stdout_bytes"], 3)
        self.assertFalse(reply["stdout_truncated"])

    def test_stdout_over_the_cap_is_cut_and_reported(self):
        reply = self.bridge._execute_code({"code": "print('x' * 5000)", "stdout_cap_bytes": 100})
        self.assertTrue(reply["stdout_truncated"])
        self.assertEqual(reply["stdout_bytes"], 100)
        # written + dropped must account for every byte the script produced,
        # which is the only thing that makes the number trustworthy.
        self.assertEqual(
            reply["stdout_bytes"] + reply["stdout_bytes_dropped"],
            len("x" * 5000 + "\n"),
        )

    def test_the_cap_can_be_lowered_but_not_raised_by_the_caller(self):
        # A caller-supplied cap of 10MB would defeat the only bound that
        # matters, so the upper clamp is the bridge's, not the request's.
        reply = self.bridge._execute_code({"code": "print('x' * 100)", "stdout_cap_bytes": 10 ** 9})
        self.assertLessEqual(reply["stdout_bytes"], addon.MAX_FRAME_BYTES)

    def test_a_raising_script_reports_the_error_without_raising_out(self):
        reply = self.bridge._execute_code({"code": "raise ValueError('boom')"})
        self.assertFalse(reply["ok"])
        self.assertIn("ValueError", reply["error"])
        self.assertIn("boom", reply["error"])
        self.assertIn("ValueError", reply["stdout"])

    def test_stdout_is_restored_after_a_failure(self):
        # A swallowed sys.stdout would send every later print into a dead
        # buffer, and the failure would look like a Blender-side log problem.
        import sys as _sys
        before = _sys.stdout
        self.bridge._execute_code({"code": "raise RuntimeError('x')"})
        self.assertIs(_sys.stdout, before)

    def test_a_result_assignment_is_returned(self):
        reply = self.bridge._execute_code({"code": "_result = {'n': 1}"})
        self.assertEqual(reply["result"], {"n": 1})

    def test_a_bpy_object_result_is_described_not_dropped(self):
        class FakeObject:
            name = "Cube"
            bl_rna = types.SimpleNamespace(identifier="Object")
            def __repr__(self):
                return "<bpy Object>"

        reply = self.bridge._execute_code({
            "code": "_result = __import__('sys').modules['__main__']",
        })
        self.assertTrue(reply["ok"])  # a module is not encodable but must not fail
        self.assertIn("repr", reply["result"])

    def test_stdout_and_result_travel_together(self):
        reply = self.bridge._execute_code({
            "code": "print('a'); _result = [1, 2, 3]",
        })
        self.assertEqual(reply["result"], [1, 2, 3])
        self.assertEqual(reply["stdout"].strip(), "a")

    def test_bpy_is_reachable_from_executed_code(self):
        reply = self.bridge._execute_code({"code": "_result = bpy.app.version_string"})
        self.assertEqual(reply["result"], bpy.app.version_string)

    def test_verify_proves_the_main_thread(self):
        reply = self.bridge._dispatch("verify", {})
        self.assertTrue(reply["ok"])
        self.assertTrue(reply["result"]["thread_is_main"])
        self.assertEqual(reply["result"]["blender"], bpy.app.version_string)

    def test_health_does_not_need_to_run_anything(self):
        reply = self.bridge._dispatch("health", {})
        self.assertTrue(reply["ok"])
        self.assertEqual(reply["stdout_cap_bytes"], addon.STDOUT_CAP_BYTES)


class TestJsonable(unittest.TestCase):
    def test_scalars_pass_through(self):
        for value in [None, True, 3, 1.5, "s"]:
            self.assertEqual(addon._jsonable(value), value)

    def test_containers_are_walked(self):
        self.assertEqual(
            addon._jsonable({"a": [1, {"b": 2}]}),
            {"a": [1, {"b": 2}]},
        )

    def test_a_named_object_keeps_its_name(self):
        class Obj:
            name = "Suzanne"
            bl_rna = types.SimpleNamespace(identifier="Object")
        self.assertEqual(addon._jsonable(Obj())["name"], "Suzanne")

    def test_a_repr_is_bounded(self):
        class Huge:
            name = 12345  # not a str, so the name is dropped
            def __repr__(self):
                return "y" * 5000
        out = addon._jsonable(Huge())
        self.assertLessEqual(len(out["repr"]), 200)
        self.assertIsNone(out["name"])


class TestPublishedConfig(unittest.TestCase):
    """The add-on has to read what the Node bridge publishes.

    Without a reader the two sides each hold a token the other does not have:
    the bridge generates one and writes it to the config file, the add-on falls
    back to an empty token, and every request is refused. Nothing in the
    handshake says why, so the failure reads as a dead port rather than a
    mismatch that a single file read would have fixed.
    """

    def setUp(self):
        self._env = {k: os.environ.pop(k, None) for k in
                     ("HSA_BLENDER_TOKEN", "HSA_BLENDER_PORT", "HSA_NOCKDEV_HOME")}
        for key, value in self._env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        self._home = tempfile.mkdtemp()
        os.environ["HSA_NOCKDEV_HOME"] = self._home
        self._original_config = addon.CONFIG_PATH
        self._original_bridge = addon._BRIDGE
        addon.CONFIG_PATH = os.path.join(self._home, ".nockdev", "blender-bridge.json")

    def tearDown(self):
        addon.CONFIG_PATH = self._original_config
        addon._BRIDGE = self._original_bridge
        if addon._BRIDGE is not None:
            addon._BRIDGE.stop()
        shutil.rmtree(self._home, ignore_errors=True)
        for key, value in self._env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def publish(self, payload):
        os.makedirs(os.path.dirname(addon.CONFIG_PATH), exist_ok=True)
        with open(addon.CONFIG_PATH, "w", encoding="utf-8") as handle:
            json.dump(payload, handle)

    def test_a_published_config_supplies_the_token(self):
        self.publish({"port": 29123, "token": "published-token"})
        bridge = addon._resolve_bridge()
        self.assertEqual(bridge.port, 29123)
        self.assertEqual(bridge.token, "published-token")

    def test_the_env_still_wins_over_the_file(self):
        self.publish({"port": 29123, "token": "published-token"})
        os.environ["HSA_BLENDER_TOKEN"] = "env-token"
        os.environ["HSA_BLENDER_PORT"] = "29222"
        bridge = addon._resolve_bridge()
        self.assertEqual(bridge.port, 29222)
        self.assertEqual(bridge.token, "env-token")

    def test_no_config_leaves_the_token_empty_rather_than_guessing(self):
        bridge = addon._resolve_bridge()
        self.assertEqual(bridge.token, "")
        self.assertEqual(bridge.port, addon.DEFAULT_PORT)

    def test_a_corrupt_config_is_ignored_not_fatal(self):
        os.makedirs(os.path.dirname(addon.CONFIG_PATH), exist_ok=True)
        with open(addon.CONFIG_PATH, "w", encoding="utf-8") as handle:
            handle.write("{not json")
        self.assertIsNone(addon._config_file_bridge())
        self.assertEqual(addon._resolve_bridge().token, "")

    def test_a_config_missing_its_token_is_rejected(self):
        self.publish({"port": 29123})
        self.assertIsNone(addon._config_file_bridge())

    def test_a_non_numeric_port_is_rejected(self):
        self.publish({"port": "28782", "token": "t"})
        self.assertIsNone(addon._config_file_bridge())

    def test_resolve_is_stable_within_a_session(self):
        self.publish({"port": 29123, "token": "first"})
        first = addon._resolve_bridge()
        self.publish({"port": 29444, "token": "second"})
        # A republish must not retune a running bridge out from under the
        # bridge: the add-on is already listening on the first port.
        self.assertIs(addon._resolve_bridge(), first)
        self.assertEqual(first.token, "first")

    def test_a_bridge_held_before_the_file_appeared_is_adopted_in_place(self):
        # The holder captures the bridge at register() time, long before the
        # bridge process publishes anything. Rebuilding it on the second lookup
        # would leave that holder pumping a queue nothing ever drains.
        held = addon._resolve_bridge()
        self.assertEqual(held.token, "")
        self.publish({"port": 29123, "token": "late"})
        later = addon._resolve_bridge()
        self.assertIs(later, held)
        self.assertEqual(held.token, "late")
        self.assertEqual(held.port, 29123)

    def test_autostart_polls_until_a_token_appears(self):
        bridge = addon._resolve_bridge()
        self.assertEqual(addon._autostart(), 2.0)  # nothing to start with
        self.assertFalse(bridge.is_running())

        self.publish({"port": 0, "token": "appeared"})  # 0 lets the OS pick a free port
        try:
            self.assertIsNone(addon._autostart())  # started; stop polling
            self.assertTrue(bridge.is_running())
        finally:
            bridge.stop()
        self.assertFalse(bridge.is_running())


if __name__ == "__main__":
    unittest.main(verbosity=2)
