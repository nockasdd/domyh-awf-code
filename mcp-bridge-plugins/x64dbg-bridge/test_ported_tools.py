"""Logic tests for the ported x64dbg tools.

The real tools need a running x64dbg, so nothing here touches a debuggee.
What is under test is the code that decides what to send: the caps, the hex
handling, and the instruction walk that a bad address would otherwise turn
into an unbounded loop.

Run: python test_ported_tools.py
"""

import os
import re
import sys
import types
import unittest
from unittest import mock

# server.py imports X64DbgClient and FastMCP at module scope, and neither the
# real package (ctypes/zmq) nor mcp is needed to exercise the decision logic.
# Stub both so the pure code can run without a debugger or a dependency tree.
fake_pkg = types.ModuleType("x64dbg_automate")
fake_pkg.X64DbgClient = object
models = types.ModuleType("x64dbg_automate.models")


class BreakpointType:
    BpNone = 0
    BpNormal = 1
    BpHardware = 2
    BpMemory = 4


models.BreakpointType = BreakpointType
fake_pkg.models = models


class FakeFastMCP:
    """Enough of FastMCP for module import: a decorator that returns the func."""

    def __init__(self, *args, **kwargs):
        pass

    def tool(self, *args, **kwargs):
        return lambda fn: fn

    def run(self, *args, **kwargs):
        raise AssertionError("run() must not be called from a test")


fastmcp = types.ModuleType("mcp.server.fastmcp")
fastmcp.FastMCP = FakeFastMCP
mcp_pkg = types.ModuleType("mcp")
mcp_server = types.ModuleType("mcp.server")
mcp_server.fastmcp = fastmcp
mcp_pkg.server = mcp_server

for name, mod in {
    "x64dbg_automate": fake_pkg,
    "x64dbg_automate.models": models,
    "mcp": mcp_pkg,
    "mcp.server": mcp_server,
    "mcp.server.fastmcp": fastmcp,
}.items():
    sys.modules.setdefault(name, mod)

import server  # noqa: E402


class FakeArg:
    def __init__(self, mnemonic):
        self.mnemonic = mnemonic


class FakeInstr:
    def __init__(self, instruction, size, args=()):
        self.instruction = instruction
        self.instr_size = size
        self.arg = [FakeArg(a) for a in args]


class FakeBp:
    def __init__(self, addr, name=""):
        self.addr = addr
        self.enabled = True
        self.active = True
        self.hitCount = 0
        self.name = name
        self.mod = "app.exe"
        self.breakCondition = ""
        self.commandText = ""


class FakeClient:
    def __init__(self, **overrides):
        self.calls = []
        self.resolved = 0x401000
        self.eval_ok = True
        self.memory = b"\x90\x90\x48\x8b"
        self.write_result = True
        self.instructions = {}
        self.breakpoints = {}
        for k, v in overrides.items():
            setattr(self, k, v)

    def eval_sync(self, expr):
        self.calls.append(("eval", expr))
        return self.resolved, self.eval_ok

    def read_memory(self, addr, size):
        self.calls.append(("read", addr, size))
        return self.memory

    def write_memory(self, addr, data):
        self.calls.append(("write", addr, data))
        return self.write_result

    def disassemble_at(self, addr):
        self.calls.append(("disasm", addr))
        return self.instructions.get(addr)

    def get_breakpoints(self, bp_type):
        self.calls.append(("bps", bp_type))
        return self.breakpoints.get(bp_type, [])


def run(tool, client, **kwargs):
    """Call a tool with a stubbed client and return its result string."""
    with mock.patch.object(server, "ensure_attached", return_value=client):
        return tool(**kwargs)


def _repo_root():
    """The two bridge repos share a parent; the dispatcher lives in the sibling.

    __file__ is this file; three dirname calls walk out of x64dbg-bridge and
    mcp-bridge-plugins and land on the shared parent.
    """
    here = os.path.dirname(os.path.abspath(__file__))          # x64dbg-bridge
    here = os.path.dirname(here)                              # mcp-bridge-plugins
    here = os.path.dirname(here)                              # domyh-awf
    return os.path.dirname(here)                              # domyh-awesome-code-agent


class TestResolveAddress(unittest.TestCase):
    def test_empty_address_is_refused(self):
        with self.assertRaises(server.BridgeError) as ctx:
            server._resolve_address(FakeClient(), "  ")
        self.assertIn("address is required", str(ctx.exception))

    def test_unresolvable_address_names_the_input(self):
        with self.assertRaises(server.BridgeError) as ctx:
            server._resolve_address(FakeClient(eval_ok=False, resolved=0), "not_a_symbol")
        self.assertIn("not_a_symbol", str(ctx.exception))

    def test_symbol_name_resolves(self):
        # eval_sync is what makes symbols work; a bare int() would reject this.
        client = FakeClient(resolved=0x7FF81234)
        addr = server._resolve_address(client, "kernel32!MessageBoxA")
        self.assertEqual(addr, 0x7FF81234)
        self.assertEqual(client.calls[0], ("eval", "kernel32!MessageBoxA"))


class TestReadMemory(unittest.TestCase):
    def test_reads_and_formats(self):
        client = FakeClient()
        out = run(server.x64_read_memory, client, address="0x401000", size=4)
        self.assertIn("0x401000", out)
        self.assertIn("90 90 48 8b", out)
        self.assertIn(("read", 0x401000, 4), client.calls)

    def test_zero_size_is_refused_before_touching_the_client(self):
        client = FakeClient()
        with self.assertRaises(server.BridgeError):
            run(server.x64_read_memory, client, address="0x401000", size=0)
        self.assertEqual([c for c in client.calls if c[0] == "read"], [])

    def test_oversized_read_is_refused(self):
        with self.assertRaises(server.BridgeError) as ctx:
            run(server.x64_read_memory, FakeClient(), address="0x401000", size=server.MAX_READ_SIZE + 1)
        self.assertIn("cap", str(ctx.exception))

    def test_empty_read_is_an_error_not_an_empty_success(self):
        # Returning "" would read as "the call worked and there was nothing",
        # which is how a bad address turns into a silently wrong result.
        with self.assertRaises(server.BridgeError):
            run(server.x64_read_memory, FakeClient(memory=b""), address="0x401000", size=4)


class TestWriteMemory(unittest.TestCase):
    def test_hex_with_spaces_and_0x(self):
        client = FakeClient()
        run(server.x64_write_memory, client, address="0x401000", hex_bytes="0x90 C3")
        self.assertIn(("write", 0x401000, b"\x90\xc3"), client.calls)

    def test_invalid_hex_names_the_problem(self):
        with self.assertRaises(server.BridgeError) as ctx:
            run(server.x64_write_memory, FakeClient(), address="0x401000", hex_bytes="zzzz")
        self.assertIn("not valid hex", str(ctx.exception))

    def test_empty_payload_is_refused(self):
        with self.assertRaises(server.BridgeError):
            run(server.x64_write_memory, FakeClient(), address="0x401000", hex_bytes="   ")

    def test_rejected_write_is_an_error(self):
        # write_memory returns bool; ignoring it would report success for a
        # write x64dbg refused.
        with self.assertRaises(server.BridgeError) as ctx:
            run(server.x64_write_memory, FakeClient(write_result=False), address="0x401000", hex_bytes="90")
        self.assertIn("rejected", str(ctx.exception))


class TestDisassemble(unittest.TestCase):
    def test_walks_by_instr_size(self):
        client = FakeClient(instructions={
            0x401000: FakeInstr("mov", 5, ["rax", "rbx"]),
            0x401005: FakeInstr("ret", 1),
        })
        out = run(server.x64_disassemble, client, address="0x401000", count=2)
        self.assertIn("mov rax rbx", out)
        self.assertIn("ret", out)
        # The second call must be at the first instruction's end, not addr+1.
        self.assertIn(("disasm", 0x401005), client.calls)

    def test_undecodable_first_instruction_is_an_error(self):
        with self.assertRaises(server.BridgeError) as ctx:
            run(server.x64_disassemble, FakeClient(), address="0x401000", count=1)
        self.assertIn("could not disassemble", str(ctx.exception))

    def test_undecodable_mid_walk_ends_rather_than_raising(self):
        # Some instructions decoded is a result; none decoded is an error.
        client = FakeClient(instructions={0x401000: FakeInstr("nop", 1)})
        out = run(server.x64_disassemble, client, address="0x401000", count=5)
        self.assertIn("end of decodable range", out)

    def test_zero_length_instruction_cannot_loop_forever(self):
        # count has to clear the 64-instruction cap to reach the walk at all;
        # with a zero-length instruction at the cursor, every remaining
        # iteration would otherwise re-request the same address.
        client = FakeClient(instructions={0x401000: FakeInstr("bad", 0)})
        out = run(server.x64_disassemble, client, address="0x401000", count=64)
        self.assertIn("zero-length", out)
        self.assertEqual(len([c for c in client.calls if c[0] == "disasm"]), 1)

    def test_count_cap(self):
        with self.assertRaises(server.BridgeError):
            run(server.x64_disassemble, FakeClient(), address="0x401000", count=65)


class TestValidateCommand(unittest.TestCase):
    """The bridge's own copy of the dispatcher's allowlist.

    The dispatcher screens the string first, but this process is reachable
    directly over MCP, so the check cannot live only there.
    """

    def test_allows_the_documented_read_only_verbs(self):
        for cmd in [
            "bp MessageBoxA", "bpc 0x401000", "bphws LoadLibraryA, rcx",
            "lm", "lmv", "trace", "dasm 0x401000:40", "sym info, 401000",
        ]:
            with self.subTest(cmd=cmd):
                server.validate_command(cmd)  # must not raise

    def test_refuses_verbs_that_change_the_debuggee(self):
        for cmd in [
            "bc *", "erun", "run", "rtr", "rte", "go", "dd",
            "kill", "init", "attach", "dlgcmd", "setcmd", "savedata",
            "writemem", "patch",
        ]:
            with self.subTest(cmd=cmd):
                with self.assertRaises(server.BridgeError) as ctx:
                    server.validate_command(cmd)
                self.assertIn("allowlist", str(ctx.exception))

    def test_refuses_verbs_that_write_a_file(self):
        # d/dump read the target and then write to disk, TraceSetLogFile
        # redirects trace output. All three are "reads" in the casual sense and
        # none of them is read-only.
        for cmd in ["d dump C:\\out.bin", "TraceSetLogFile C:\\t.log", "TraceSetDir C:\\t"]:
            with self.subTest(cmd=cmd):
                with self.assertRaises(server.BridgeError) as ctx:
                    server.validate_command(cmd)
                self.assertIn("allowlist", str(ctx.exception))

    def test_refuses_chained_commands_with_and_without_spaces(self):
        for cmd in [
            "bp X; erun", "bp X;erun", "bp X && erun", "lm | dd C:\\d",
            "lm|dd C:\\out.bin", "bc * || erun", "bpc 401000\nerun",
        ]:
            with self.subTest(cmd=cmd):
                with self.assertRaises(server.BridgeError) as ctx:
                    server.validate_command(cmd)
                self.assertIn("chained", str(ctx.exception))

    def test_chained_refusal_reports_the_separator_not_the_verb(self):
        # 'lm|dd' is a single whitespace token, so a verb-scoped check rejects
        # it for the wrong reason. The message has to name the chain.
        with self.assertRaises(server.BridgeError) as ctx:
            server.validate_command("lm|dd C:\\out.bin")
        self.assertIn("chained", str(ctx.exception))

    def test_refuses_empty(self):
        for cmd in ["", "   ", "\t\n"]:
            with self.subTest(cmd=repr(cmd)):
                with self.assertRaises(server.BridgeError):
                    server.validate_command(cmd)

    def test_verb_case_does_not_decide(self):
        # x64dbg verbs are case-insensitive; an allowlist that is not is a
        # bypass.
        server.validate_command("LM")
        with self.assertRaises(server.BridgeError):
            server.validate_command("ERUN")

    def test_the_tool_itself_refuses_before_touching_the_client(self):
        # The predicate existing proves nothing if the tool does not call it.
        # This is the wiring assertion, and it is the one that would have caught
        # the gap.
        client = FakeClient()
        with self.assertRaises(server.BridgeError):
            run(server.x64_search_command, client, command="erun")
        self.assertEqual(client.calls, [])


class TestAllowlistParityWithDispatcher(unittest.TestCase):
    """The two allowlists are two copies of one policy.

    A second copy that drifts is how the hole reopens, so the shared entries are
    pinned from both sides rather than from one file's opinion of the other.
    """

    def _dispatcher_allowlist(self):
        path = os.path.join(
            _repo_root(), "domyh-hsa-mcp", "src", "tools", "t17_bridge.ts"
        )
        # Not a skipTest: a missing sibling repo means the two lists can no
        # longer be compared, and a skipped parity check is how a second copy
        # drifts unnoticed. Fail so it cannot go quiet.
        if not os.path.exists(path):
            raise AssertionError(f"dispatcher source not present at {path}")
        with open(path, encoding="utf-8") as fh:
            source = fh.read()
        start = source.index("X64DBG_COMMAND_ALLOWLIST = new Set([")
        end = source.index("]);", start)
        return set(re.findall(r"'([^']+)'", source[start:end]))

    def test_the_two_lists_agree(self):
        dispatcher = {v.lower() for v in self._dispatcher_allowlist()}
        self.assertEqual(
            dispatcher,
            {v.lower() for v in server.X64DBG_COMMAND_ALLOWLIST},
            "the bridge and the dispatcher must allow the same verbs",
        )

    def test_neither_list_carries_a_known_writer(self):
        forbidden = {"d", "dump", "dd", "savedata", "erun", "run", "rtr", "rte",
                     "go", "writemem", "patch", "tracesetlogfile", "tracesetdir"}
        overlap = {v.lower() for v in server.X64DBG_COMMAND_ALLOWLIST} & forbidden
        self.assertEqual(overlap, set(), f"allowlist must not contain {overlap}")


class TestListBreakpoints(unittest.TestCase):
    def test_all_queries_the_three_real_types(self):
        # BpNone is 0 and returns nothing while looking valid, so it is not
        # part of "all".
        client = FakeClient(breakpoints={
            BreakpointType.BpNormal: [FakeBp(0x401000, "bp1")],
            BreakpointType.BpHardware: [FakeBp(0x7FFE0000, "hw")],
        })
        out = run(server.x64_list_breakpoints, client, bp_type="bp_type_all")
        types_queried = {c[1] for c in client.calls if c[0] == "bps"}
        self.assertEqual(types_queried, {BreakpointType.BpNormal, BreakpointType.BpHardware, BreakpointType.BpMemory})
        self.assertIn("bp1", out)

    def test_single_type(self):
        client = FakeClient()
        run(server.x64_list_breakpoints, client, bp_type="bp_type_hardware")
        self.assertEqual([c for c in client.calls if c[0] == "bps"], [("bps", BreakpointType.BpHardware)])

    def test_unknown_type_lists_the_valid_ones(self):
        with self.assertRaises(server.BridgeError) as ctx:
            run(server.x64_list_breakpoints, FakeClient(), bp_type="bp_type_none")
        self.assertIn("bp_type_memory", str(ctx.exception))

    def test_results_are_sorted_by_address(self):
        client = FakeClient(breakpoints={
            BreakpointType.BpNormal: [FakeBp(0x402000), FakeBp(0x401000)],
        })
        out = run(server.x64_list_breakpoints, client, bp_type="bp_type_normal")
        self.assertLess(out.index("0x401000"), out.index("0x402000"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
