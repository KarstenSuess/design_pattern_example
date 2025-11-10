import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch, MagicMock

from design_pattern.identify.ilwrapper.ilwrapper import ILWrapper
from design_pattern.identify.ilwrapper import ILWrapperConfig, ILWrapperJobtype


class TestILWrapperIdentify(unittest.TestCase):
    def make_cfg(self):
        return ILWrapperConfig(
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

    def test_identify_remote_success_sets_response(self):
        cfg = self.make_cfg()

        # login response
        login_resp = SimpleNamespace(status_code=200, content=b"ok", text='{"token":"abc123"}')
        # identify response
        identify_payload = {"status": "queued", "jobId": "j123"}
        identify_resp = SimpleNamespace(status_code=200, content=json.dumps(identify_payload))

        session_login = self.make_context_session(login_resp)
        session_create = self.make_context_session(identify_resp)

        with patch("design_pattern.models.ilwrapper.ilwrapper.ILWrapperSession", side_effect=[session_login, session_create]):
            il = ILWrapper(cfg)  # will consume session_login
            il.identify("/path/to/file.pdf", ILWrapperJobtype.REMOTE)  # will consume session_create

        # Access the private response via name mangling
        self.assertEqual(getattr(il, "_ILWrapper__response"), identify_payload)

    def test_identify_remote_non200_raises(self):
        cfg = self.make_cfg()

        login_resp = SimpleNamespace(status_code=200, content=b"ok", text='{"token":"tkn"}')
        error_resp = SimpleNamespace(status_code=400, content=b"bad request")

        session_login = self.make_context_session(login_resp)
        session_create = self.make_context_session(error_resp)

        with patch("design_pattern.models.ilwrapper.ilwrapper.ILWrapperSession", side_effect=[session_login, session_create]):
            il = ILWrapper(cfg)
            with self.assertRaises(Exception) as ctx:
                il.identify("/path/to/file.pdf", ILWrapperJobtype.REMOTE)

        self.assertIn("400", str(ctx.exception))
        self.assertIn("bad request", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
