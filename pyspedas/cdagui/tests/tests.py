import unittest
from pyspedas import CDAWeb
from pytplot import data_exists, del_data


class CDAWebTests(unittest.TestCase):
    def test_get_observatories(self):
        cdaweb_obj = CDAWeb()
        obslist = cdaweb_obj.get_observatories()
        self.assertTrue('ARTEMIS' in obslist)

    def test_get_instruments(self):
        cdaweb_obj = CDAWeb()
        inst_list = cdaweb_obj.get_instruments()
        self.assertTrue('Magnetic Fields (space)' in inst_list)

    def test_get_datasets(self):
        cdaweb_obj = CDAWeb()
        ds_list = cdaweb_obj.get_datasets(['Voyager'], ['Magnetic Fields (space)'])
        self.assertTrue('VOYAGER2_2S_MAG (1977-08-24 to 1991-01-01)' in ds_list)

    def test_get_filenames(self):
        cdaweb_obj = CDAWeb()
        urllist = cdaweb_obj.get_filenames(['VOYAGER2_2S_MAG (1977-08-24 to 1991-01-01)'],
                                           "1979-01-01", "1979-01-02")
        self.assertTrue('https://cdaweb.gsfc.nasa.gov/sp_phys/data/voyager/voyager2/magnetic_fields_cdaweb/mag_2s/1979/voyager2_2s_mag_19790101_v01.cdf' in urllist)

    def test_load_data(self):
        del_data('*')
        cdaweb_obj = CDAWeb()
        urllist = cdaweb_obj.get_filenames(['VOYAGER2_2S_MAG (1977-08-24 to 1991-01-01)'],
                                           "1979-01-01", "1979-01-02")
        cdaweb_obj.cda_download(urllist, "cdaweb/")
        self.assertTrue(data_exists('B1'))

    def test_load_data_prefix(self):
        del_data('*')
        cdaweb_obj = CDAWeb()
        urllist = cdaweb_obj.get_filenames(['VOYAGER2_2S_MAG (1977-08-24 to 1991-01-01)'],
                                           "1979-01-01", "1979-01-02")
        cdaweb_obj.cda_download(urllist, "cdaweb/", prefix = 'v2_')
        self.assertTrue(data_exists('v2_B1'))


if __name__ == '__main__':
    unittest.main()
