import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch, MagicMock

from design_pattern.identify.ingestlist_identifier import IngestListIdentifier
from design_pattern.identify.ingestlist import IngestListIdentifierConfig, IngestListJobType


class TestILWrapperValidate(unittest.TestCase):
    def make_cfg(self):
        return IngestListIdentifierConfig(
            base_url="http://example.com/",
            username="user",
            password="pass",
            proxies=None,
        )

    def make_context_session(self, response):
        """Create a MagicMock that behaves like ILWrapperSession in a context manager returning given response on post."""
        sess = MagicMock()
        sess.__enter__.return_value = sess
        sess.__exit__.return_value = False
        sess.post.return_value = response
        return sess

    def mock_open_binary(self, data: bytes = b"DATA"):
        m = MagicMock()
        cm = MagicMock()
        m.return_value = cm
        cm.__enter__.return_value = cm
        cm.read.return_value = data
        cm.__exit__.return_value = False
        return m

    def test_validate_local_success_sets_response(self):
        cfg = self.make_cfg()

        login_resp = SimpleNamespace(status_code=200, content=b"ok", text='{"token":"abc123"}')
        payload = {"status": "ok", "jobId": "v123"}
        validate_resp = SimpleNamespace(status_code=200, content=json.dumps(payload))

        session_login = self.make_context_session(login_resp)
        session_create = self.make_context_session(validate_resp)

        with patch("builtins.open", self.mock_open_binary(b"file-bytes")):
            with patch(
                "design_pattern.identify.ingestlist_identifier.RemoteSession",
                side_effect=[session_login, session_create],
            ):
                il = IngestListIdentifier(cfg)  # consumes login session
                il.validate("/path/to/file.pdf", IngestListJobType.LOCAL)  # consumes create session

        self.assertEqual(getattr(il, "_IngestListIdentifier__response"), payload)

    def test_validate_local_non200_raises(self):
        cfg = self.make_cfg()

        login_resp = SimpleNamespace(status_code=200, content=b"ok", text='{"token":"tkn"}')
        error_resp = SimpleNamespace(status_code=422, content=b"unprocessable")

        session_login = self.make_context_session(login_resp)
        session_create = self.make_context_session(error_resp)

        with patch("builtins.open", self.mock_open_binary(b"file-bytes")):
            with patch(
                "design_pattern.identify.ingestlist_identifier.RemoteSession",
                side_effect=[session_login, session_create],
            ):
                il = IngestListIdentifier(cfg)
                with self.assertRaises(Exception) as ctx:
                    il.validate("/path/to/file.pdf", IngestListJobType.LOCAL)

        self.assertIn("422", str(ctx.exception))
        self.assertIn("unprocessable", str(ctx.exception))

    def test_validate_remote_success_sets_response(self):
        cfg = self.make_cfg()

        login_resp = SimpleNamespace(status_code=200, content=b"ok", text='{"token":"abc123"}')
        payload = {"status": "queued", "jobId": "r789"}
        validate_resp = SimpleNamespace(status_code=200, content=json.dumps(payload))

        session_login = self.make_context_session(login_resp)
        session_create = self.make_context_session(validate_resp)

        with patch(
            "design_pattern.identify.ingestlist_identifier.RemoteSession",
            side_effect=[session_login, session_create],
        ):
            il = IngestListIdentifier(cfg)
            il.validate("remote-file.pdf", IngestListJobType.REMOTE)

        self.assertEqual(getattr(il, "_IngestListIdentifier__response"), payload)

    def test_validate_remote_non200_raises(self):
        cfg = self.make_cfg()

        login_resp = SimpleNamespace(status_code=200, content=b"ok", text='{"token":"abc"}')
        error_resp = SimpleNamespace(status_code=500, content=b"server error")

        session_login = self.make_context_session(login_resp)
        session_create = self.make_context_session(error_resp)

        with patch(
            "design_pattern.identify.ingestlist_identifier.RemoteSession",
            side_effect=[session_login, session_create],
        ):
            il = IngestListIdentifier(cfg)
            with self.assertRaises(Exception) as ctx:
                il.validate("remote-file.pdf", IngestListJobType.REMOTE)

        self.assertIn("500", str(ctx.exception))
        self.assertIn("server error", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
