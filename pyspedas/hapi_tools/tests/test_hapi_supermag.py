import unittest
import logging
from pyspedas import hapi, data_exists, del_data

class HAPITests(unittest.TestCase):

    def test_string_time(self):
        del_data()
        server = "https://supermag.jhuapl.edu/hapi"
        dataset = "ttb/baseline_all/PT1M/XYZ"
        start = "2020-05-10T00:00Z"
        stop = "2020-05-14T00:00Z"
        parameters = ""
        param_list = hapi(
            trange=[start, stop], server=server, dataset=dataset, parameters=parameters
        )
        logging.info(f"Param list from supermag: {param_list}")
        self.assertTrue("mlt" in param_list)
        self.assertTrue(data_exists("mlt"))


if __name__ == "__main__":
    unittest.main()
