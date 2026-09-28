"""Token resolution in the bridge, which is the side that was wrong.

The plugin generated its own token and wrote it beside itself; the bridge was
meant to go and collect it. It never did, because _resolve_token read the
environment first and the HSA server always populates that variable, so the
function returned before reaching the file. Both sides then held a different
credential and every call came back 401.

server.py cannot be imported the way test_token.py imports the plugin: it opens
a server and starts scanning on import. The resolution logic is therefore
exercised by reading the function out of the source and running it against a
real temporary plugin directory, which is what actually decides the answer.
"""

import ast
import os
import shutil
import tempfile
import unittest

SERVER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.py")


def load_resolve_token(plugin_dir):
    """Run server._resolve_token with IDA_PLUGIN_DIR pointed at plugin_dir."""
    with open(SERVER, "r", encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    fn = next(
        n for n in tree.body
        if isinstance(n, ast.FunctionDef) and n.name == "_resolve_token"
    )
    module = ast.Module(body=[fn], type_ignores=[])
    ns = {"os": os, "IDA_PLUGIN_DIR": plugin_dir}
    exec(compile(module, SERVER, "exec"), ns)
    return ns["_resolve_token"]


class TestServerTokenResolution(unittest.TestCase):
    def setUp(self):
        self.plugin_dir = tempfile.mkdtemp(prefix="ida-plugin-")
        self.token_file = os.path.join(self.plugin_dir, "hsa_bridge_token")
        self._saved = os.environ.get("HSA_BRIDGE_TOKEN")
        os.environ.pop("HSA_BRIDGE_TOKEN", None)

    def tearDown(self):
        shutil.rmtree(self.plugin_dir, ignore_errors=True)
        if self._saved is None:
            os.environ.pop("HSA_BRIDGE_TOKEN", None)
        else:
            os.environ["HSA_BRIDGE_TOKEN"] = self._saved

    def _write_plugin_token(self, value):
        with open(self.token_file, "w") as fh:
            fh.write(value)

    def test_the_plugin_token_wins_over_the_bridge_environment(self):
        # The regression. Both values were present and the bridge sent its own,
        # so the plugin rejected it — while the bridge believed its own was
        # authoritative and never learned otherwise.
        self._write_plugin_token("token-the-plugin-is-validating")
        os.environ["HSA_BRIDGE_TOKEN"] = "token-the-bridge-generated"

        self.assertEqual(
            load_resolve_token(self.plugin_dir)(), "token-the-plugin-is-validating"
        )

    def test_the_environment_is_used_when_the_plugin_wrote_nothing(self):
        # IDA launched after the bridge, or a plugin dir the bridge cannot read.
        # Without this the fix would trade one dead end for another.
        os.environ["HSA_BRIDGE_TOKEN"] = "token-the-bridge-generated"

        self.assertEqual(
            load_resolve_token(self.plugin_dir)(), "token-the-bridge-generated"
        )

    def test_an_empty_token_file_does_not_shadow_the_environment(self):
        # A file the plugin created but failed to write into is not a token.
        self._write_plugin_token("   \n")
        os.environ["HSA_BRIDGE_TOKEN"] = "token-the-bridge-generated"

        self.assertEqual(
            load_resolve_token(self.plugin_dir)(), "token-the-bridge-generated"
        )

    def test_no_token_anywhere_yields_an_empty_string(self):
        # The caller raises on this, and that is the right place for it: the
        # message names both places a token can be put.
        self.assertEqual(load_resolve_token(self.plugin_dir)(), "")

    def test_no_plugin_directory_falls_back_to_the_environment(self):
        os.environ["HSA_BRIDGE_TOKEN"] = "token-the-bridge-generated"

        self.assertEqual(
            load_resolve_token("")(), "token-the-bridge-generated"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
