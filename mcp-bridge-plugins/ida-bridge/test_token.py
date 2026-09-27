"""Token resolution, with the plugin's IDA imports stubbed out.

The plugin reads its token at import time, so the only way to test the cases
that matter is to import it repeatedly with a different environment each time.
Copying the file into a temp directory is what gives each case its own
__file__, which is where the plugin looks for the token.
"""

import importlib.util
import builtins
import os
import shutil
import sys
import tempfile
import types
import unittest
from unittest import mock

PLUGIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hsa_ida_plugin.py")

STUB_MODULES = [
    "idaapi", "idautils", "idc", "ida_kernwin", "ida_funcs", "ida_bytes",
    "ida_name", "ida_nalt", "ida_lines", "ida_ida", "ida_typeinf", "ida_pro",
    "ida_struct",
]


def _stub_modules():
    for name in STUB_MODULES:
        mod = types.ModuleType(name)
        mod.__getattr__ = lambda attr: mock.MagicMock()
        sys.modules[name] = mod


def _install(plugin_dir, source=PLUGIN):
    """Copy the plugin into plugin_dir and import it from there."""
    target = os.path.join(plugin_dir, "hsa_ida_plugin.py")
    shutil.copyfile(source, target)
    sys.modules.pop("hsa_ida_plugin", None)
    spec = importlib.util.spec_from_file_location("hsa_ida_plugin", target)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestTokenResolution(unittest.TestCase):
    def setUp(self):
        _stub_modules()
        self.plugin_dir = tempfile.mkdtemp(prefix="ida-plugin-")
        os.environ.pop("HSA_BRIDGE_TOKEN", None)
        self._env = mock.patch.dict(os.environ, {}, clear=False)
        self._env.start()

    def tearDown(self):
        self._env.stop()
        shutil.rmtree(self.plugin_dir, ignore_errors=True)

    def _load(self, plugin_dir=None, env_token=None, preset=None):
        if env_token is not None:
            os.environ["HSA_BRIDGE_TOKEN"] = env_token
        else:
            os.environ.pop("HSA_BRIDGE_TOKEN", None)
        if preset is not None:
            with open(os.path.join(plugin_dir or self.plugin_dir, "hsa_bridge_token"), "w") as fh:
                fh.write(preset)
        return _install(plugin_dir or self.plugin_dir)

    def test_a_missing_token_is_generated_rather_than_refused(self):
        # The regression: the plugin used to leave BRIDGE_TOKEN empty and close
        # its listener, which meant a fresh install could never start.
        mod = self._load()
        self.assertTrue(mod.BRIDGE_TOKEN)
        self.assertGreaterEqual(len(mod.BRIDGE_TOKEN), 32)

    def test_the_generated_token_is_written_where_the_bridge_looks(self):
        mod = self._load()
        with open(os.path.join(self.plugin_dir, "hsa_bridge_token")) as fh:
            self.assertEqual(fh.read().strip(), mod.BRIDGE_TOKEN)

    def test_a_second_start_reuses_the_token_it_wrote(self):
        first = self._load()
        second = self._load()
        self.assertEqual(second.BRIDGE_TOKEN, first.BRIDGE_TOKEN)

    def test_an_exported_token_wins_over_the_file(self):
        self._load(preset="from-a-previous-run")
        mod = self._load(env_token="exported")
        self.assertEqual(mod.BRIDGE_TOKEN, "exported")

    def test_generated_tokens_differ_between_installs(self):
        # Two independent installs must not share a credential, or anyone who
        # saw one machine's token could drive another.
        first = self._load()
        other = tempfile.mkdtemp(prefix="ida-plugin-")
        try:
            second = self._load(plugin_dir=other)
        finally:
            shutil.rmtree(other, ignore_errors=True)
        self.assertNotEqual(first.BRIDGE_TOKEN, second.BRIDGE_TOKEN)

    def test_an_unwritable_plugin_dir_still_yields_a_token(self):
        # Losing the file is a degraded session, not a dead one: the listener
        # still comes up and the bridge reports the mismatch on the first call.
        # Only the write is blocked — making the whole directory read-only would
        # also block the import, which is not the failure being tested.
        token_file = os.path.join(self.plugin_dir, "hsa_bridge_token")
        real_open = builtins.open

        def _open(path, *args, **kwargs):
            if str(path) == token_file and "w" in (args[0] if args else kwargs.get("mode", "r")):
                raise OSError("read-only file system")
            return real_open(path, *args, **kwargs)

        with mock.patch.object(builtins, "open", side_effect=_open):
            mod = self._load()
        self.assertTrue(mod.BRIDGE_TOKEN)
        self.assertFalse(os.path.isfile(token_file))


if __name__ == "__main__":
    unittest.main(verbosity=2)
