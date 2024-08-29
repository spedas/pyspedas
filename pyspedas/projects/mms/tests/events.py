from pyspedas.projects.mms.mms_events import mms_brst_events

import unittest


class TestMMSBrstEvents(unittest.TestCase):
    def test_trange(self):
        # Test with trange option
        trange = ['2015-10-16', '2015-10-17']
        mms_brst_events(trange=trange)

    def test_reload(self):
        # Test with reload option
        reload = True
        mms_brst_events(reload=reload)


if __name__ == '__main__':
    unittest.main()
