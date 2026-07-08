import os
import pickle
import tempfile
import unittest
from unittest.mock import Mock, patch

from pyspedas.projects.mms.mms_login_lasp import mms_login_lasp


class MMSLoginLaspTestCases(unittest.TestCase):
    def _write_saved_auth(self, home, payload):
        with open(os.path.join(home, "mms_auth_info.pkl"), "wb") as auth_file:
            pickle.dump(payload, auth_file)

    @patch("pyspedas.projects.mms.mms_login_lasp.readsav", side_effect=FileNotFoundError)
    @patch("requests.Session.get")
    def test_invalid_saved_credentials_fall_back_to_public_access(self, mock_get, _mock_readsav):
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        with tempfile.TemporaryDirectory() as home:
            self._write_saved_auth(home, {"user": "stale-user", "passwd": "stale-pass"})

            with patch("pyspedas.projects.mms.mms_login_lasp.os.path.expanduser", return_value=home):
                with self.assertLogs(level="ERROR") as log:
                    session, user = mms_login_lasp()

        self.assertIsNone(user)
        self.assertIsNone(session.auth)
        self.assertIn("using public access", "\n".join(log.output))
        self.assertIn("mms_auth_info.pkl", "\n".join(log.output))
        self.assertIn("mms_auth_info.sav", "\n".join(log.output))
        self.assertIn("mms_auth_info.sav", "\n".join(log.output))

    @patch("pyspedas.projects.mms.mms_login_lasp.readsav", side_effect=FileNotFoundError)
    @patch("requests.Session.get")
    def test_none_saved_user_is_treated_as_public_access(self, mock_get, _mock_readsav):
        with tempfile.TemporaryDirectory() as home:
            self._write_saved_auth(home, {"user": None, "passwd": "stale-pass"})

            with patch("pyspedas.projects.mms.mms_login_lasp.os.path.expanduser", return_value=home):
                session, user = mms_login_lasp()

        self.assertIsNone(user)
        self.assertIsNone(session.auth)
        mock_get.assert_not_called()

    @patch("pyspedas.projects.mms.mms_login_lasp.readsav", side_effect=FileNotFoundError)
    @patch("requests.Session.get", side_effect=TimeoutError("network timeout"))
    def test_credential_check_exception_falls_back_to_public_access(self, _mock_get, _mock_readsav):
        with tempfile.TemporaryDirectory() as home:
            self._write_saved_auth(home, {"user": "saved-user", "passwd": "saved-pass"})

            with patch("pyspedas.projects.mms.mms_login_lasp.os.path.expanduser", return_value=home):
                with self.assertLogs(level="WARNING") as log:
                    session, user = mms_login_lasp()

        self.assertIsNone(user)
        self.assertIsNone(session.auth)
        self.assertIn("Unable to verify MMS SDC credentials", "\n".join(log.output))
        self.assertIn("mms_auth_info.pkl", "\n".join(log.output))


if __name__ == "__main__":
    unittest.main()
