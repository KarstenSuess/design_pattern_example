import unittest
from types import SimpleNamespace
from unittest.mock import patch, MagicMock

from design_pattern.identify.ingestlist_identifier import IngestListIdentifier, IngestListIdentifierConfig


class TestILWrapperLogin(unittest.TestCase):
    def make_cfg(self):
        return IngestListIdentifierConfig(
            base_url="http://example.com/",
            username="user",
            password="pass",
            proxies=None,
        )

    def test_login_success_sets_token(self):
        cfg = self.make_cfg()
        il = IngestListIdentifier(cfg)
        # Work around private attribute name and reference to self.proxies in implementation
        il.proxies = None

        # Prepare a fake Response-like object
        resp = SimpleNamespace(status_code=200, content=b"ok", text='{"token":"abc123"}')

        # Prepare a fake session that behaves as a context manager and returns our response
        fake_session = MagicMock()
        fake_session.__enter__.return_value = fake_session
        fake_session.__exit__.return_value = False
        fake_session.post.return_value = resp

        with patch("design_pattern.models.ilwrapper.ilwrapper.ILWrapperSession", return_value=fake_session):
            il._ILWrapper__login()

        self.assertEqual(il.token, "abc123")

    def test_login_failure_raises_exception(self):
        cfg = self.make_cfg()
        il = IngestListIdentifier(cfg)
        il.proxies = None

        resp = SimpleNamespace(status_code=401, content=b"unauthorized", text="")

        fake_session = MagicMock()
        fake_session.__enter__.return_value = fake_session
        fake_session.__exit__.return_value = False
        fake_session.post.return_value = resp

        with patch("design_pattern.models.ilwrapper.ilwrapper.ILWrapperSession", return_value=fake_session):
            with self.assertRaises(Exception) as ctx:
                il._ILWrapper__login()

        self.assertIn("401", str(ctx.exception))
        self.assertIn("unauthorized", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
