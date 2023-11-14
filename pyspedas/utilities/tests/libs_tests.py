import unittest
from io import StringIO
import sys
import pyspedas
from pyspedas.utilities.libs import libs


class LibsTestCase(unittest.TestCase):

    def setUp(self):
        # Call function once to import all the submodules to silence the output
        try:
            libs('')
        except Exception as e:
            self.fail("Unexpected exception %s" % e)

        # Redirect stdout to capture print statements
        self.held_stdout = sys.stdout
        sys.stdout = StringIO()


    def tearDown(self):
        # Reset stdout
        sys.stdout = self.held_stdout

    def test_known_function_fgm(self):
        libs('fgm')
        output = sys.stdout.getvalue()
        self.assertIn('fgm', output)
        self.assertIn('Function:', output)

    def test_non_existent_function(self):
        libs('non_existent_function')
        output = sys.stdout.getvalue()
        self.assertEqual(output, '')  # Assuming no output for non-existent functions

    def test_partial_function_name(self):
        libs('mms_')
        output = sys.stdout.getvalue()
        self.assertIn('mms_', output)

    def test_different_package(self):
        libs('fgm', package=pyspedas.themis)
        output = sys.stdout.getvalue()
        self.assertIn('fgm', output)
        self.assertNotIn('mms', output)


if __name__ == '__main__':
    unittest.main()
