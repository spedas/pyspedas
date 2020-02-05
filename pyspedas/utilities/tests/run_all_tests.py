
import unittest

testmodules = [
    'pyspedas.mms.tests.load_routine_tests',
    'pyspedas.mms.tests.feeps',
    'pyspedas.mms.tests.eis',
    'pyspedas.mms.tests.file_filter',
    'ppyspedas.dscovr.tests.tests',
    'pyspedas.utilities.tests.download_tests',
    ]

suite = unittest.TestSuite()

for t in testmodules:
    try:
        # If the module defines a suite() function, call it to get the suite.
        mod = __import__(t, globals(), locals(), ['suite'])
        suitefn = getattr(mod, 'suite')
        suite.addTest(suitefn())
    except (ImportError, AttributeError):
        # else, just load all the test cases from the module.
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

unittest.TextTestRunner().run(suite)