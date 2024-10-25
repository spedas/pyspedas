import unittest
from unittest.mock import patch, MagicMock

class TestImportErrorHandling(unittest.TestCase):
    def setUp(self):

        # Mocking only the logging part of pyspedas to capture logging outputs
        self.logging_patch = patch('pyspedas.logging.error', new_callable=MagicMock)
        self.mock_logging_error = self.logging_patch.start()

    def tearDown(self):
        self.logging_patch.stop()

    def test_pyspedas_mth5_import_error(self):
        import sys

        # Patch 'mth5' to raise ImportError
        with patch.dict('sys.modules', {'mth5': None}):
            if 'pyspedas.mth5' in sys.modules:
                del sys.modules['pyspedas.mth5']

            # Attempt to import 'pyspedas.mth5' which should raise ImportError due to 'mth5' not being available
            with self.assertRaises((ImportError, ModuleNotFoundError)):
                import pyspedas.mth5

            # Verify the error log was called with the expected message
            self.mock_logging_error.assert_any_call('MTH5 must be installed to use module pyspedas.mth5.')
            self.mock_logging_error.assert_any_call("Please install it using: pip install mth5")


if __name__ == '__main__':
    unittest.main()
