"""
HSA MCP Bridge Plugin for Ghidra
================================
This script is intended to run inside Ghidra and expose a tiny localhost HTTP
bridge for the external MCP server.
"""

import json
import os
import hmac
import threading
import traceback

from ghidra.app.plugin import GhidraPlugin
from ghidra.framework.plugintool.util import PluginException
from java.net import InetSocketAddress
from java.util.concurrent import Executors
from com.sun.net.httpserver import HttpServer, HttpHandler

PLUGIN_NAME = "HSA MCP Bridge"
PLUGIN_VERSION = "0.2.0"
HTTP_HOST = "127.0.0.1"
HTTP_PORT = int(os.environ.get("HSA_GHIDRA_HTTP_PORT", "28572"))
HTTP_PORT_RANGE = int(os.environ.get("HSA_GHIDRA_HTTP_PORT_RANGE", "32"))
ACTIVE_HTTP_PORT = HTTP_PORT

# Ghidra does not forward the launching shell's environment to the JVM, so the
# token also comes from a file next to the script. The bridge writes it; see
# server.py.
BRIDGE_TOKEN = os.environ.get("HSA_BRIDGE_TOKEN", "").strip()
if not BRIDGE_TOKEN:
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "hsa_bridge_token"), "r") as _fh:
            BRIDGE_TOKEN = _fh.read().strip()
    except Exception:
        BRIDGE_TOKEN = ""
MAX_BODY_BYTES = int(os.environ.get("HSA_GHIDRA_MAX_BODY_BYTES", str(4 * 1024 * 1024)))


def _current_program():
    return globals().get("currentProgram")


def _to_addr(addr):
    if isinstance(addr, str):
        addr = addr.strip()
        if addr.startswith("0x"):
            addr = addr[2:]
        return int(addr, 16)
    return int(addr)


def _json_ok(data):
    return {"ok": True, "data": data}


def _json_err(msg):
    return {"ok": False, "error": msg}


def cmd_get_info(_params):
    program = _current_program()
    if program is None:
        return _json_err("No active program")
    fm = program.getFunctionManager()
    listing = program.getListing()
    return _json_ok({
        "plugin": PLUGIN_NAME,
        "version": PLUGIN_VERSION,
        "name": program.getName(),
        "executable_path": program.getExecutablePath(),
        "imagebase": hex(program.getImageBase().getOffset()),
        "language_id": str(program.getLanguageID()),
        "compiler_spec_id": str(program.getCompilerSpec().getCompilerSpecID()),
        "function_count": fm.getFunctionCount(),
        "instruction_count": listing.getNumInstructions(),
        "http_port": ACTIVE_HTTP_PORT,
    })


def cmd_list_instances(_params):
    return cmd_get_info({})


def cmd_list_functions(params):
    program = _current_program()
    if program is None:
        return _json_err("No active program")
    offset = int(params.get("offset", 0))
    limit = int(params.get("limit", 50))
    fm = program.getFunctionManager()
    data = []
    count = 0
    for func in fm.getFunctions(True):
        if count < offset:
            count += 1
            continue
        if len(data) >= limit:
            break
        data.append({
            "address": hex(func.getEntryPoint().getOffset()),
            "name": func.getName(),
            "signature": str(func.getSignature()),
        })
        count += 1
    return _json_ok({"functions": data, "count": len(data), "total": fm.getFunctionCount()})


def cmd_search_functions(params):
    program = _current_program()
    if program is None:
        return _json_err("No active program")
    pattern = (params.get("pattern") or "").lower()
    max_results = int(params.get("max_results", 50))
    fm = program.getFunctionManager()
    data = []
    for func in fm.getFunctions(True):
        name = func.getName()
        if pattern and pattern not in name.lower():
            continue
        data.append({
            "address": hex(func.getEntryPoint().getOffset()),
            "name": name,
        })
        if len(data) >= max_results:
            break
    return _json_ok({"results": data, "count": len(data), "pattern": pattern})


def cmd_decompile(params):
    program = _current_program()
    if program is None:
        return _json_err("No active program")
    try:
        from ghidra.app.decompiler import DecompInterface
    except Exception as e:
        return _json_err("Decompiler unavailable: %s" % e)
    ea = _to_addr(params.get("address"))
    func = program.getFunctionManager().getFunctionAt(program.getAddressFactory().getAddress("%x" % ea))
    if func is None:
        return _json_err("No function at %s" % hex(ea))
    di = DecompInterface()
    di.openProgram(program)
    res = di.decompileFunction(func, 120, None)
    if not res.decompileCompleted():
        return _json_err("Decompile failed")
    return _json_ok({"address": hex(ea), "name": func.getName(), "pseudocode": str(res.getDecompiledFunction().getC())})


def cmd_get_disasm(params):
    program = _current_program()
    if program is None:
        return _json_err("No active program")
    ea = _to_addr(params.get("address"))
    count = int(params.get("count", 20))
    listing = program.getListing()
    addr = program.getAddressFactory().getAddress("%x" % ea)
    inst = listing.getInstructionAt(addr)
    data = []
    while inst is not None and len(data) < count:
        data.append({
            "address": hex(inst.getAddress().getOffset()),
            "text": str(inst),
        })
        inst = inst.getNext()
    return _json_ok({"lines": data, "count": len(data)})


def cmd_get_xrefs(params):
    program = _current_program()
    if program is None:
        return _json_err("No active program")
    ea = _to_addr(params.get("address"))
    direction = params.get("direction", "to")
    rm = program.getReferenceManager()
    addr = program.getAddressFactory().getAddress("%x" % ea)
    refs = rm.getReferencesTo(addr) if direction == "to" else rm.getReferencesFrom(addr)
    data = []
    for ref in refs:
        data.append({
            "from": hex(ref.getFromAddress().getOffset()),
            "to": hex(ref.getToAddress().getOffset()),
            "type": str(ref.getReferenceType()),
        })
    return _json_ok({"xrefs": data, "count": len(data), "direction": direction})


def cmd_get_symbols(params):
    program = _current_program()
    if program is None:
        return _json_err("No active program")
    pattern = (params.get("pattern") or "").lower()
    max_results = int(params.get("max_results", 100))
    table = program.getSymbolTable()
    data = []
    it = table.getAllSymbols(True)
    while it.hasNext() and len(data) < max_results:
        sym = it.next()
        name = sym.getName()
        if pattern and pattern not in name.lower():
            continue
        data.append({
            "address": hex(sym.getAddress().getOffset()),
            "name": name,
            "namespace": str(sym.getParentNamespace().getName()),
        })
    return _json_ok({"results": data, "count": len(data)})


def cmd_get_data_types(params):
    program = _current_program()
    if program is None:
        return _json_err("No active program")
    pattern = (params.get("pattern") or "").lower()
    max_results = int(params.get("max_results", 100))
    dtm = program.getDataTypeManager()
    data = []
    for dt in dtm.getAllDataTypes():
        name = dt.getName()
        if pattern and pattern not in name.lower():
            continue
        data.append({
            "name": name,
            "category": str(dt.getCategoryPath()),
            "length": dt.getLength(),
        })
        if len(data) >= max_results:
            break
    return _json_ok({"results": data, "count": len(data)})


def cmd_rename_symbol(params):
    program = _current_program()
    if program is None:
        return _json_err("No active program")
    from ghidra.program.model.symbol import SourceType
    ea = _to_addr(params.get("address"))
    name = params.get("name")
    if not name:
        return _json_err("Missing name")
    addr = program.getAddressFactory().getAddress("%x" % ea)
    sym = program.getSymbolTable().getPrimarySymbol(addr)
    if sym is not None:
        sym.setName(name, SourceType.USER_DEFINED)
        return _json_ok({"ok": True, "address": hex(ea), "name": name})
    func = program.getFunctionManager().getFunctionAt(addr)
    if func is not None:
        func.setName(name, SourceType.USER_DEFINED)
        return _json_ok({"ok": True, "address": hex(ea), "name": name})
    return _json_err("No symbol or function at %s" % hex(ea))


def cmd_set_function_signature(params):
    program = _current_program()
    if program is None:
        return _json_err("No active program")
    ea = _to_addr(params.get("address"))
    signature = params.get("signature")
    if not signature:
        return _json_err("Missing signature")
    addr = program.getAddressFactory().getAddress("%x" % ea)
    func = program.getFunctionManager().getFunctionAt(addr)
    if func is None:
        return _json_err("No function at %s" % hex(ea))
    try:
        func.setSignature(signature)
        return _json_ok({"ok": True, "address": hex(ea), "signature": signature})
    except Exception as e:
        return _json_err(str(e))


def cmd_create_struct(params):
    program = _current_program()
    if program is None:
        return _json_err("No active program")
    try:
        from ghidra.program.model.data import StructureDataType, CategoryPath, ByteDataType, DataTypeConflictHandler
    except Exception as e:
        return _json_err("Struct API unavailable: %s" % e)
    name = params.get("name")
    members = params.get("members") or []
    if not name:
        return _json_err("Missing name")
    dtm = program.getDataTypeManager()
    struct = StructureDataType(name, 0)
    applied = []
    for member in members:
        if not isinstance(member, dict):
            continue
        member_name = member.get("name")
        offset = int(member.get("offset", 0))
        size = int(member.get("size", 1))
        if not member_name:
            continue
        while struct.getLength() < offset:
            struct.add(ByteDataType.dataType, 1, "__pad")
        struct.add(ByteDataType.dataType, size, member_name, None)
        applied.append({"name": member_name, "offset": offset, "size": size})
    try:
        dtm.addDataType(struct, DataTypeConflictHandler.DEFAULT_HANDLER)
    except Exception:
        pass
    return _json_ok({"ok": True, "name": name, "members": applied})


def cmd_apply_data_type(params):
    program = _current_program()
    if program is None:
        return _json_err("No active program")
    type_name = params.get("type_name")
    if not type_name:
        return _json_err("Missing type_name")
    dtm = program.getDataTypeManager()
    dt = dtm.getDataType(type_name)
    if dt is None:
        return _json_err("Data type not found: %s" % type_name)
    ea = _to_addr(params.get("address"))
    addr = program.getAddressFactory().getAddress("%x" % ea)
    length = int(params.get("length", 0)) or dt.getLength()
    try:
        listing = program.getListing()
        listing.clearCodeUnits(addr, addr.add(max(1, length) - 1), False)
        created = listing.createData(addr, dt)
        if created is None:
            return _json_err("Ghidra refused the data type at %s" % hex(ea))
        return _json_ok({
            "address": hex(ea),
            "type_name": type_name,
            "length": created.getLength(),
        })
    except Exception as e:
        return _json_err(str(e))


def cmd_create_class_layout(params):
    return cmd_create_struct(params)


COMMANDS = {
    "get_info": cmd_get_info,
    "list_instances": cmd_list_instances,
    "list_functions": cmd_list_functions,
    "search_functions": cmd_search_functions,
    "decompile": cmd_decompile,
    "get_disasm": cmd_get_disasm,
    "get_xrefs": cmd_get_xrefs,
    "get_symbols": cmd_get_symbols,
    "get_data_types": cmd_get_data_types,
    "rename_symbol": cmd_rename_symbol,
    "set_function_signature": cmd_set_function_signature,
    "create_struct": cmd_create_struct,
    "apply_data_type": cmd_apply_data_type,
    "create_class_layout": cmd_create_class_layout,
}


class _Handler(HttpHandler):
    def __init__(self, server):
        self.server = server

    def _send(self, exchange, status, body):
        exchange.getResponseHeaders().add("Content-Type", "application/json")
        exchange.sendResponseHeaders(status, len(body))
        exchange.getResponseBody().write(body)
        exchange.getResponseBody().close()

    def _authorized(self, exchange):
        if not BRIDGE_TOKEN:
            return False, "HSA_BRIDGE_TOKEN is not set, so no call can be authenticated."
        header = exchange.getRequestHeaders().getFirst("Authorization") or ""
        prefix = "Bearer "
        if not header.startswith(prefix):
            return False, "Missing Authorization: Bearer <HSA_BRIDGE_TOKEN> header"
        # compare_digest rather than ==, which returns on the first mismatched
        # byte and so leaks the length of the matching prefix.
        if not hmac.compare_digest(header[len(prefix):], BRIDGE_TOKEN):
            return False, "Invalid HSA_BRIDGE_TOKEN"
        return True, None

    def handle(self, exchange):
        try:
            method = exchange.getRequestMethod()
            if method == "GET":
                # Liveness only. Unauthenticated because it discloses nothing
                # actionable and keeps discovery from needing the token.
                body = json.dumps({
                    "status": "ok",
                    "plugin": PLUGIN_NAME,
                    "version": PLUGIN_VERSION,
                    "port": ACTIVE_HTTP_PORT,
                    "auth_required": bool(BRIDGE_TOKEN),
                    "commands": list(COMMANDS.keys()),
                }).encode("utf-8")
            else:
                authorized, reason = self._authorized(exchange)
                if not authorized:
                    self._send(exchange, 401, json.dumps({"ok": False, "error": reason}).encode("utf-8"))
                    return
                raw_length = exchange.getRequestHeaders().getFirst("Content-Length")
                length = int(raw_length or "0")
                # Refused before the body is read, so an oversized request is
                # never buffered.
                if length > MAX_BODY_BYTES:
                    self._send(exchange, 413, json.dumps({
                        "ok": False,
                        "error": "Request body is %d bytes, limit is %d" % (length, MAX_BODY_BYTES),
                    }).encode("utf-8"))
                    return
                data = exchange.getRequestBody().read(length).decode("utf-8")
                req = json.loads(data or "{}")
                name = req.get("command") or req.get("cmd")
                params = req.get("params", {})
                handler = COMMANDS.get(name)
                if handler is None:
                    self._send(exchange, 404, json.dumps({"ok": False, "error": "Unknown command: %s" % name}).encode("utf-8"))
                    return
                body = json.dumps(handler(params), default=str).encode("utf-8")
                exchange.getResponseHeaders().add("Content-Type", "application/json")
                exchange.sendResponseHeaders(200, len(body))
                exchange.getResponseBody().write(body)
                exchange.getResponseBody().close()
                return

            self._send(exchange, 200, body)
        except Exception as e:
            self._send(exchange, 500, json.dumps({
                "ok": False,
                "error": "%s\n%s" % (e, traceback.format_exc()),
            }).encode("utf-8"))


class HsaGhidraBridgePlugin(GhidraPlugin):
    """Ghidra loads this through the plugin manager, which instantiates the
    class named in Module.manifest and drives initialize()/dispose()."""

    def __init__(self):
        super(HsaGhidraBridgePlugin, self).__init__()
        self._server = None
        self._thread = None

    def initialize(self):
        """Called by Ghidra once the tool is available. Starting the listener
        here rather than on demand means the agent finds the bridge as soon as
        Ghidra is up."""
        self.start()

    def dispose(self):
        self.stop()

    def start(self):
        global ACTIVE_HTTP_PORT
        if self._server is not None:
            return
        if not BRIDGE_TOKEN:
            # rename_symbol and create_struct write to the program. On an open
            # localhost socket any local process could reach them.
            raise PluginException(
                "HSA bridge: no HSA_BRIDGE_TOKEN, so the server was not started. Set it in "
                "the environment Ghidra sees, or write it next to this script as "
                "hsa_bridge_token."
            )
        last_error = None
        for port in range(HTTP_PORT, HTTP_PORT + max(1, HTTP_PORT_RANGE)):
            try:
                server = HttpServer.create(InetSocketAddress(HTTP_HOST, port), 0)
                server.createContext("/", _Handler(server))
                # A null executor serves requests on the dispatcher thread, so one
                # 120s decompile blocks every other call. Ghidra decompiles are
                # slow by nature, so the bridge has to stay concurrent.
                server.setExecutor(Executors.newFixedThreadPool(4))
                self._server = server
                ACTIVE_HTTP_PORT = port
                break
            except Exception as e:
                last_error = e
                self._server = None
        if self._server is None:
            # PluginException's two-argument form wants a Python BaseException as
            # the cause, and the failures here are Java BindExceptions, so the
            # last error has to be folded into the message instead.
            raise PluginException(
                "HSA bridge: no free port in %d-%d (last error: %s)"
                % (HTTP_PORT, HTTP_PORT + HTTP_PORT_RANGE - 1, last_error)
            )
        self._thread = threading.Thread(target=self._server.start)
        # The daemon flag is a property on both Jython 2.7 and Python 3, whereas
        # setDaemon() was removed in 3.10, so this form works either way.
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        if self._server is not None:
            self._server.stop(0)
            self._server = None
            self._thread = None


PLUGIN = HsaGhidraBridgePlugin()


if __name__ == "__main__":
    PLUGIN.start()
