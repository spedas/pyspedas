import unittest
import sys
from unittest.mock import patch, MagicMock


class TestImportErrorHandling(unittest.TestCase):

    def setUp(self):
        # Mocking only the logging part of pyspedas to capture logging outputs
        self.logging_patch = patch('pyspedas.logging.error', new_callable=MagicMock)
        self.mock_logging_error = self.logging_patch.start()

        # Clear any existing modules
        if 'pyspedas' in sys.modules:
            del sys.modules['pyspedas']

        if 'mth5' in sys.modules:
            del sys.modules['mth5']

    def tearDown(self):
        self.logging_patch.stop()

    def test_pyspedas_mth5_import_error(self):
        # Patch 'mth5' to raise ImportError
        with patch.dict('sys.modules', {'mth5': None}):
            # Attempt to import 'pyspedas.mth5' which should raise ImportError due to 'mth5' not being available
            with self.assertRaises(ImportError):
                import pyspedas.mth5

            # Verify the error log was called with the expected message
            self.mock_logging_error.assert_any_call('MTH5 must be installed to use module pyspedas.mth5.')
            self.mock_logging_error.assert_any_call('Please install it using: pip install mth5')


if __name__ == '__main__':
    unittest.main()
