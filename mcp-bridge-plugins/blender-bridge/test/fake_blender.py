"""A stand-in Blender: the real add-on against a stubbed bpy.

The add-on needs Blender's event loop, which is the one thing a test cannot
fake, so this runs it under a thread that calls _drain the way
bpy.app.timers would. Everything else — socket, framing, auth, exec, stdout
cap — is the shipping code path.

Run: python test/fake_blender.py <port> <token> [object-count]
"""

import os
import sys
import threading
import time
import types

HERE = os.path.dirname(os.path.abspath(__file__))
BRIDGE_DIR = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(BRIDGE_DIR, "src", "addon"))


def build_fake_bpy(object_count):
    bpy = types.ModuleType("bpy")
    bpy.props = types.SimpleNamespace(
        IntProperty=lambda **k: None,
        StringProperty=lambda **k: None,
        BoolProperty=lambda **k: None,
    )

    class _Timers:
        def __init__(self):
            self.r = {}

        @staticmethod
        def _key(fn):
            return fn if isinstance(fn, str) else fn.__name__

        def register(self, fn, first_interval=0.0, persistent=False):
            self.r[self._key(fn)] = fn

        def unregister(self, fn):
            self.r.pop(self._key(fn), None)

        def is_registered(self, fn):
            return self._key(fn) in self.r

    class _App:
        def __init__(self):
            self.timers = _Timers()
            self.version_string = "4.2.1"

    bpy.app = _App()
    bpy.types = types.SimpleNamespace(AddonPreferences=object, Operator=object)
    bpy.utils = types.SimpleNamespace(register_class=lambda c: None, unregister_class=lambda c: None)
    # load_post is a list in Blender, not a namespace with methods.
    bpy.app.handlers = types.SimpleNamespace(persistent=lambda f: f, load_post=[])

    objects = []
    for i in range(object_count):
        objects.append(
            types.SimpleNamespace(
                name="Obj_%03d" % i,
                type="MESH" if i % 3 else "LIGHT",
                parent=None,
                location=(float(i), 0.0, 0.0),
                dimensions=(1.0, 1.0, 1.0),
                scale=(1.0, 1.0, 1.0),
                rotation_euler=(0.0, 0.0, 0.0),
                modifiers=[],
                hide_viewport=False,
                keys=lambda: [],
                data=None,
                children=[],
            )
        )

    class _PropCollection(list):
        """bpy_prop_collection is iterable, sized, and has .get(name).

        A plain list would pass every read the bridge does except the missing-
        object lookup, which is exactly the path that must not fall over.
        """

        def get(self, name, default=None):
            for item in self:
                if item.name == name:
                    return item
            return default

        def __contains__(self, item):
            if isinstance(item, str):
                return any(o.name == item for o in self)
            return list.__contains__(self, item)

    collection = _PropCollection(objects)

    bpy.data = types.SimpleNamespace(objects=collection)
    bpy.context = types.SimpleNamespace(
        scene=types.SimpleNamespace(name="TestScene", frame_current=1),
        preferences=types.SimpleNamespace(addons={}),
        view_layer=types.SimpleNamespace(
            objects=_PropCollection([objects[0]] if objects else []),
            active=objects[0] if objects else None,
        ),
        mode="OBJECT",
    )
    return bpy


def main():
    port = int(sys.argv[1])
    token = sys.argv[2]
    object_count = int(sys.argv[3]) if len(sys.argv) > 3 else 120

    sys.modules["bpy"] = build_fake_bpy(object_count)
    import hsa_blender_addon as addon

    if token == "":
        # The state a real Blender sits in when the IDE launched it before the
        # bridge existed: no env to read, so the port and token have to come
        # from the file the bridge publishes. _autostart is what bpy.app.timers
        # would call, so the pump calls it too rather than starting a bridge
        # that has nothing to authenticate with.
        bridge = addon._resolve_bridge()
    else:
        bridge = addon.HSABridge(port, token)
        bridge.start()

    def pump():
        while True:
            if token == "":
                addon._autostart()
            if bridge.is_running():
                bridge._drain()
            time.sleep(0.01)

    # The add-on logs through print() on a background thread, so a block-buffered
    # stdout holds those lines until the process ends — and a test waiting on
    # "listening on" would then time out on a bridge that is already up.
    sys.stdout.reconfigure(line_buffering=True)

    threading.Thread(target=pump, daemon=True).start()

    print("FAKE_BLENDER_READY port=%d objects=%d" % (port, object_count), flush=True)
    while True:
        if token != "" and not bridge.is_running():
            break
        time.sleep(0.2)


if __name__ == "__main__":
    main()
