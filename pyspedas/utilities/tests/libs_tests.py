import unittest
from io import StringIO
import sys
import pyspedas
import pytplot
from pyspedas.utilities.libs import libs


class LibsTestCase(unittest.TestCase):

    def setUp(self):

        # We do not need this anymore:
        # # Call function once to import all the submodules to silence the output
        # try:
        #     libs('')
        # except Exception as e:
        #     self.fail("Unexpected exception %s" % e)

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

    def test_wildcard_function_name(self):
        libs('wa*pol')
        output = sys.stdout.getvalue()
        self.assertIn('twavpol', output)

    def test_wildcard_partial_wrapper(self):
        libs('ep*ad')
        output = sys.stdout.getvalue()
        self.assertIn('epead', output)

    def test_substring_partial_wrapper(self):
        libs('epead')
        output = sys.stdout.getvalue()
        self.assertIn('epead', output)

    def test_known_function_subpackage(self):
        libs('fgm', package=pyspedas.projects.themis)
        output = sys.stdout.getvalue()
        self.assertIn('fgm', output)
        self.assertNotIn('mms', output)

    def test_known_function_pytplot(self):
        libs('get_data')
        output = sys.stdout.getvalue()
        self.assertIn('get_data', output)
        self.assertIn('Function:', output)

    def test_known_function_version_pyspeds_subpackage(self):
        libs('version', package=pyspedas)
        output = sys.stdout.getvalue()
        self.assertIn('version', output)
        self.assertNotIn('Function: pytplot', output)

    def test_known_function_version_pyspeds_themis_subpackage(self):
        libs('fgm', package=pyspedas.projects.themis)
        output = sys.stdout.getvalue()
        self.assertIn('fgm', output)

    def test_known_function_pytplot_get_data(self):
        libs('get_data')
        output = sys.stdout.getvalue()
        self.assertIn('get_data', output)
        self.assertIn('Function:', output)

    def test_known_function_data_pytplot_subpackage_only(self):
        libs('data', package=pytplot)
        output = sys.stdout.getvalue()
        self.assertIn('get_data', output)
        self.assertNotIn('Function: pyspedas', output)

    def test_qtplotter_error_exception(self):
        # This test is probably not the best way to handle this exception
        libs('qtplotter', package=pytplot)  # This can be changed to anything. qtplotter error is during pytplot import search
        output = sys.stdout.getvalue()
        self.assertNotIn('Error importing module pytplot.QtPlotter', output)

if __name__ == '__main__':
    unittest.main()
