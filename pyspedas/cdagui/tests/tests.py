import unittest
from pyspedas import CDAWeb
from pytplot import data_exists, del_data, get_data, time_double, tplot_names, tplot


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

    def test_load_merge(self):
        del_data('*')
        # Create the CDAWeb interface object
        cdaweb_obj = CDAWeb()

        # We'll pick one of available data sets and load it into tplot variables
        dataset = 'VOYAGER2_COHO1HR_MERGED_MAG_PLASMA'
        start_time = '2009-01-01 00:00:00'
        end_time = '2010-01-01 00:00:00'

        # Get the URLs for the available data in this time range
        urllist = cdaweb_obj.get_filenames([dataset], start_time, end_time)

        # Download the data and load as tplot variables.  Setting a prefix
        # is useful if you want to work with both Voyager 1 and Voyager 2
        # data; the variable names in the archived data are the same for both
        # spacecraft.

        cdaweb_obj.cda_download(urllist, "cdaweb/", prefix='v2_')
        dat = get_data('v2_protonDensity')
        # Files are monthly; we should have over a year of data.
        self.assertTrue((dat.times[-1] - dat.times[0])/86400.0 > 395.0)

    def test_load_icon_netcdf(self):
        del_data('*')
        # Create the CDAWeb interface object
        import pyspedas

        cdaweb_obj = pyspedas.CDAWeb()

        time0 = '2021-01-15T14:05:52'
        time1 = '2021-01-15T15:08:57'

        urllist = cdaweb_obj.get_filenames(['ICON_L2-2_MIGHTI_VECTOR-WIND-GREEN (2019-12-06 to 2022-11-25)'], time0,
                                           time1)
        result = cdaweb_obj.cda_download(urllist, "cdaweb/")
        self.assertTrue(data_exists('ICON_L22_Fringe_Amplitude'))

    def test_load_goes_netcdf(self):
        del_data('*')
        # Create the CDAWeb interface object
        import pyspedas

        cdaweb_obj = pyspedas.CDAWeb()

        time0 = '2021-01-15T14:05:52'
        time1 = '2021-01-15T15:08:57'

        urllist = cdaweb_obj.get_filenames(['DN_MAGN-L2-HIRES_G17 (2018-08-01 to 2023-03-14)'], time0,
                                           time1)
        result = cdaweb_obj.cda_download(urllist, "cdaweb/")
        self.assertTrue(data_exists('b_gse'))


    def test_load_time_clip(self):
        del_data('*')
        cdaweb_obj = CDAWeb()

        dataset = 'NEW_HORIZONS_SWAP_VALIDSUM (2008-10-10 to 2023-07-31)'
        start_time = '2014-10-10 00:00:00'
        end_time = '2014-11-10 00:00:00'

        # Get the URLs for the available data in this time range
        urllist = cdaweb_obj.get_filenames([dataset], start_time, end_time)
        cdaweb_obj.cda_download(urllist, "cdaweb/", prefix='nh_', trange=[start_time, end_time], time_clip=True)

        # Verify that the times were clipped
        # Note that tplot variables with no data in the requested interval will NOT be clipped (deleted).
        dat = get_data('nh_n')
        self.assertTrue(dat.times[0] >= time_double(start_time))
        self.assertTrue(dat.times[-1] <= time_double(end_time))

    def test_load_time_clip_no_trange(self):
        del_data('*')
        cdaweb_obj = CDAWeb()

        dataset = 'NEW_HORIZONS_SWAP_VALIDSUM (2008-10-10 to 2023-07-31)'
        start_time = '2014-10-10 00:00:00'
        end_time = '2014-11-10 00:00:00'

        # Get the URLs for the available data in this time range
        urllist = cdaweb_obj.get_filenames([dataset], start_time, end_time)
        with self.assertLogs(level='WARNING') as logs:
            cdaweb_obj.cda_download(urllist, "cdaweb/", prefix='nh_', time_clip=True)
        got_trange_warning = False
        for o in logs.output:
            if "No trange specified" in o:
                got_trange_warning = True
        self.assertTrue(got_trange_warning)

    def test_load_time_clip_empty_trange(self):
        del_data('*')
        cdaweb_obj = CDAWeb()

        dataset = 'NEW_HORIZONS_SWAP_VALIDSUM (2008-10-10 to 2023-07-31)'
        start_time = '2014-10-10 00:00:00'
        end_time = '2014-11-10 00:00:00'

        # Get the URLs for the available data in this time range
        urllist = cdaweb_obj.get_filenames([dataset], start_time, end_time)
        with self.assertLogs(level='WARNING') as logs:
            cdaweb_obj.cda_download(urllist, "cdaweb/", prefix='nh_', trange=[start_time, start_time],  time_clip=True)
        got_trange_warning = False
        for o in logs.output:
            if "equal" in o:
                got_trange_warning = True
        self.assertTrue(got_trange_warning)

    def test_load_time_clip_backward_trange(self):
        del_data('*')
        cdaweb_obj = CDAWeb()

        dataset = 'NEW_HORIZONS_SWAP_VALIDSUM (2008-10-10 to 2023-07-31)'
        start_time = '2014-10-10 00:00:00'
        end_time = '2014-11-10 00:00:00'

        # Get the URLs for the available data in this time range
        urllist = cdaweb_obj.get_filenames([dataset], start_time, end_time)
        with self.assertLogs(level='WARNING') as logs:
            cdaweb_obj.cda_download(urllist, "cdaweb/", prefix='nh_', trange=[end_time, start_time],  time_clip=True)
        got_trange_warning = False
        for o in logs.output:
            if "out of order" in o:
                got_trange_warning = True
        self.assertTrue(got_trange_warning)

    def test_load_data_prefix(self):
        del_data('*')
        cdaweb_obj = CDAWeb()
        urllist = cdaweb_obj.get_filenames(['VOYAGER2_2S_MAG (1977-08-24 to 1991-01-01)'],
                                           "1979-01-01", "1979-01-02")
        cdaweb_obj.cda_download(urllist, "cdaweb/", prefix='v2_')
        self.assertTrue(data_exists('v2_B1'))


if __name__ == '__main__':
    unittest.main()
