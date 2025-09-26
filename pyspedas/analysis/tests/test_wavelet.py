"""Tests of waelet tool."""
import pyspedas
from pyspedas.tplot_tools import get_data, tplot, tplot_rename, ylim, zlim, options, tplot_options, split_vec, join_vec, store_data, del_data, time_double
import unittest
from numpy.testing import assert_allclose
import numpy as np
from pyspedas.analysis.wavelet import wavelet
from pyspedas.analysis.wav_data import wav_data

global_display = False

def tc_scales_from_freqs(freqs, omega0=6.0):
    """Convert desired physical frequencies [Hz] to wavelet scales using Torrence & Compo (1998)"""
    fourier_factor = (omega0 + np.sqrt(2 + omega0**2)) / (4 * np.pi)
    return 1.0 / (freqs * fourier_factor)  # No dt here!

def fracyear_to_unix(fyear: float):
    # Convert fractional years yyyy.fff from Torrence and Compo example to Unix timestamps
    iyear = int(fyear)
    ut_start = pyspedas.time_double(str(iyear))
    frac = fyear - iyear
    secs = pyspedas.time_double(str(iyear+1))-ut_start
    return ut_start + frac*secs


class TwaveletDataValidation(unittest.TestCase):
    """ Compares wavelet results between Python and IDL """

    @classmethod
    def setUpClass(cls):
        """
        IDL Data has to be downloaded to perform these tests
        The SPEDAS script that creates the file: general/tools/python_validate/wavelet_python_validate.pro
        """
        from pyspedas.utilities.download import download
        from pyspedas.projects.themis.config import CONFIG

        # Testing tolerance
        cls.tol = 1e-10

        # Download tplot files
        remote_server = 'https://github.com/spedas/test_data/raw/refs/heads/main/'
        remote_name = 'analysis_tools/wavelet_test.tplot'
        datafile = download(remote_file=remote_name,
                            remote_path=remote_server,
                            local_path=CONFIG['local_data_dir'],
                            no_download=False)
        if not datafile:
            # Skip tests
            raise unittest.SkipTest("Cannot download data validation file")
        # Load validation variables from the test file
        pyspedas.del_data('*')
        filename = datafile[0]
        #filename = "/tmp/wavelet_test.tplot"
        # pyspedas.cdf_to_tplot(filename)
        pyspedas.tplot_restore(filename)
        pyspedas.tplot_names()

        # Test 1: simple sine waves
        cls.sin_wav = pyspedas.get_data('sin_wav')
        cls.sin_wav_wv_pow = pyspedas.get_data('sin_wav_wv_pow')

        # Test 2: Vassilis homework example using THEMIS FGM data
        cls.tha_fgs_fac_bp_x = pyspedas.get_data('tha_fgs_fac_bp_x')
        cls.tha_fgs_fac_bp_y = pyspedas.get_data('tha_fgs_fac_bp_y')
        cls.tha_fgs_fac_bp_z = pyspedas.get_data('tha_fgs_fac_bp_z')
        cls.tha_fgs_fac_bp_x_wv_pow = pyspedas.get_data('tha_fgs_fac_bp_x_wv_pow')
        cls.tha_fgs_fac_bp_y_wv_pow = pyspedas.get_data('tha_fgs_fac_bp_y_wv_pow')
        cls.tha_fgs_fac_bp_z_wv_pow = pyspedas.get_data('tha_fgs_fac_bp_z_wv_pow')
        cls.wavetest_powspec = pyspedas.get_data('wavetest_powspec')

        tplot_rename('sin_wav_wv_pow', 'idl_sin_wav_wv_pow')
        tplot_rename('wavetest_powspec', 'idlwavetest_powspec')

        zlim('tha_fgs_fac_bp_?_wv_pow', 1.0e-1,1.0e2)
        ylim('tha_fgs_fac_bp_?_wv_pow', 1.0e-3,4.1e-2)
        options('tha_fgs_fac_bp_?_wv_pow', 'zlog', True)
        options('tha_fgs_fac_bp_?_wv_pow', 'ylog', False)

        tplot_rename('tha_fgs_fac_bp_x_wv_pow', 'idl_fgs_fac_bp_x_wv_pow')
        tplot_rename('tha_fgs_fac_bp_y_wv_pow', 'idl_fgs_fac_bp_y_wv_pow')
        tplot_rename('tha_fgs_fac_bp_z_wv_pow', 'idl_fgs_fac_bp_z_wv_pow')


    def setUp(self):
        """ We need to clean tplot variables before each run"""
        # pyspedas.del_data('*')

    def test_sin_wav(self):
        # The default is 'morl' rather than 'cmorl0.5-1.0, but it doesn't appear to make that much difference.
        # cmorl0.5-1.0 is what Eric used in the wiki example.
        wavelet('sin_wav',wavename='cmorl1.5-1.0')
        pvar='sin_wav_pow'
        pyspedas.options(pvar, 'colormap', 'jet')
        pyspedas.ylim(pvar, 0.001, 0.1)
        pyspedas.options(pvar, 'ylog', True)
        pyspedas.options(pvar, 'ytitle', pvar)
        pyspedas.options(pvar,'zlog',True)
        d=get_data('sin_wav_pow')
        print(f"Python frequencies: bin count {d.y.shape[1]}, min {np.min(d.v)}, max: {np.max(d.v)}" )
        print(f"Python power: min {np.min(d.y)}, max {np.max(d.y)}")
        d_idl = get_data('idl_sin_wav_wv_pow')
        print(f"IDL frequencies: bin count {d_idl.y.shape[1]}, min {np.min(d_idl.v)}, max: {np.max(d_idl.v)}" )
        print(f"IDL power: min {np.min(d_idl.y)}, max {np.max(d_idl.y)}")
        tplot(['sin_wav', 'sin_wav_pow', 'idl_sin_wav_wv_pow'],display=global_display,save_png='sin_wav_simple.png')

    def test_equiv_wav(self):

        # 54 logarithmically spaced frequencies between IDL min and max
        idl_freqs = np.logspace(np.log10(0.00051), np.log10(0.05), 54)

        scales=tc_scales_from_freqs(idl_freqs)

        wavelet('sin_wav',wavename='cmorl1.5-1.0', sampling_period=1.0)
        pvar='sin_wav_pow'
        pyspedas.options(pvar, 'colormap', 'spedas')
        #pyspedas.ylim(pvar, 0.0005, 0.05)
        pyspedas.options(pvar, 'ylog', True)
        pyspedas.options(pvar, 'zlog', True)
        pyspedas.options(pvar, 'ytitle', pvar)
        d=get_data('sin_wav_pow')
        print(f"Python frequencies: bin count {d.y.shape[1]}, min {np.min(d.v)}, max: {np.max(d.v)}" )
        print(f"Python power: min {np.min(d.y)}, max {np.max(d.y)}")
        d_idl = get_data('idl_sin_wav_wv_pow')
        print(f"IDL frequencies: bin count {d_idl.y.shape[1]}, min {np.min(d_idl.v)}, max: {np.max(d_idl.v)}" )
        print(f"IDL power: min {np.min(d_idl.y)}, max {np.max(d_idl.y)}")
        tplot(['sin_wav', 'sin_wav_pow', 'idl_sin_wav_wv_pow'], display=global_display, save_png='sin_wav_equiv.png')

    def test_themis_fgm_wavelet(self):
        pyspedas.wavelet('tha_fgs_fac_bp_x')
        pyspedas.wavelet('tha_fgs_fac_bp_y')
        pyspedas.wavelet('tha_fgs_fac_bp_z')

        zlim('tha_fgs_fac_bp_?_pow', 1.0e-1,1.0e2)
        ylim('tha_fgs_fac_bp_?_pow', 1.0e-3,4.1e-2)
        options('tha_fgs_fac_bp_?_pow', 'zlog', True)
        options('tha_fgs_fac_bp_?_pow', 'ylog', False)
        d=get_data('tha_fgs_fac_bp_x_pow')
        print(f"Python frequencies: bin count {d.y.shape[1]}, min {np.min(d.v)}, max: {np.max(d.v)}" )
        print(f"Python power: min {np.min(d.y)}, max {np.max(d.y)}")
        d_idl=get_data('idl_fgs_fac_bp_x_wv_pow')
        print(f"IDL frequencies: bin count {d_idl.y.shape[1]}, min {np.min(d_idl.v)}, max: {np.max(d_idl.v)}" )
        print(f"IDL power: min {np.min(d_idl.y)}, max {np.max(d_idl.y)}")
        tplot(['tha_fgs_fac_bp_x_pow', 'idl_fgs_fac_bp_x_wv_pow'], display=global_display, save_png='themis_fgm_wavelets.png')

    def test_nino3_tc(self):
        from pyspedas.analysis.tests.wavetest import wavetest
        output_dict = wavetest(noplot=True)
        timestamps = [fracyear_to_unix(t) for t in output_dict['time']]
        pyspedas.store_data('sst_nino3_pwr',data={'x':timestamps,'y':output_dict['power'], 'v':output_dict['period']})
        pyspedas.options('sst_nino3_pwr','spec',1)
        pyspedas.options('sst_nino3_pwr','yrange',[0.5,128.0,1])
        pyspedas.options('sst_nino3_pwr','zlog',0)

        pyspedas.options('idlwavetest_powspec', 'spec', 1)
        pyspedas.options('idlwavetest_powspec','yrange',[0.5,128.0,1])
        pyspedas.options('idlwavetest_powspec','zlog',0)

        pyspedas.tplot('sst_nino3_pwr idlwavetest_powspec', display=global_display, save_png='nino_powspec.png')
        d=pyspedas.get_data('sst_nino3_pwr')
        assert_allclose(d.times, self.wavetest_powspec.times)
        assert_allclose(d.v, self.wavetest_powspec.v)
        # Max relative difference 2.8e-06
        assert_allclose(d.y, self.wavetest_powspec.y, rtol=3e-05)


    def test_wav_data(self):
        # Compare results of wav_data.py to wav_data.pro

        # IDL results (from savefile)
        # IDL Themis data, after all transformation, but before applying wavelets
        tvars = ["tha_fgs_fac_bp_x", "tha_fgs_fac_bp_y", "tha_fgs_fac_bp_z"]
        # IDL results after applying wav_data.pro
        idl_pow = [
            "idl_fgs_fac_bp_x_wv_pow",
            "idl_fgs_fac_bp_y_wv_pow",
            "idl_fgs_fac_bp_z_wv_pow",
        ]

        # Python results (to be computed below)
        py_pow = [
            "tha_fgs_fac_bp_x_wv_pow",
            "tha_fgs_fac_bp_y_wv_pow",
            "tha_fgs_fac_bp_z_wv_pow",
        ]

        all_vars = []
        dcomp = ["time", "y", "v"]
        dxyz = ["x", "y", "z"]

        for i in range(3):
            # Compute the wavelet transform for each of x,y,z
            wav_data(tvars[i])

            # Compare python results with IDL results
            d1 = get_data(idl_pow[i])
            d2 = get_data(py_pow[i])
            print(f"IDL {idl_pow[i]}: {d1.y.shape}, {d1.v.shape}")
            print(f"Python {py_pow[i]}: {d2.y.shape}, {d2.v.shape}")
            for j in range(3):
                # Find max difference
                max_diff = np.abs(np.max(d1[j] - d2[j]))
                print(f"- Max difference for {dcomp[j]}: {max_diff}")
                assert_allclose(d1[j], d2[j], rtol=1e-3, atol=1e-3)

            # Set plotting parameters
            options(py_pow[i], "ytitle", "python " + dxyz[i])
            options(idl_pow[i], "ytitle", "idl " + dxyz[i])
            options(py_pow[i], "ztitle", "python Ptot")
            options(idl_pow[i], "ztitle", "idl Ptot")
            options(py_pow[i], "zlog", True)
            options(py_pow[i], "ylog", False)
            options(idl_pow[i], "zlog", True)
            options(idl_pow[i], "ylog", False)
            zlim(py_pow[i], 1.0e-1, 1.0e2)
            ylim(py_pow[i], 1.0e-3, 4.1e-2)
            zlim(idl_pow[i], 1.0e-1, 1.0e2)
            ylim(idl_pow[i], 1.0e-3, 4.1e-2)
            all_vars.append(idl_pow[i])
            all_vars.append(py_pow[i])

        # Plot 6 panels (x,y,z - IDL, python)
        tplot_options("title", "wav_data: IDL - Python comparison")
        tplot(all_vars, display=global_display, save_png="wav_data_test.png")        

    def test_wav_data_keywords(self):
        # Test various wav_data keywords
        # using a synthetic sine wave dataset so that the test is fast and self-contained
        
        del_data()
        t = np.arange(4000, dtype=float)
        vtime = time_double('2010-01-01') + 10 * t

        # Create a two-dimensional variable
        var = 'sin_wav'
        vdata = np.zeros((4000, 2), dtype=float)
        vdata[:, 0] = np.cos(2 * np.pi * t / 32.)
        vdata[:, 1] = np.sin(2 * np.pi * t / 64.)
        store_data(var, data={'x': vtime, 'y': vdata})

        # Test rbin, dimennum
        wav_data(var, dimennum=1, rbin=4)
        var1x = 'sin_wav(1)_wv_pow'
        var1 = 'test_rbin'
        tplot_rename(var1x, var1)
        d = get_data(var1)
        # Since rbin=4, length should be 1000
        self.assertEqual(len(d[0]), 1000)

        # Test trange
        wav_data(var, dimennum=0, trange=[vtime[1000], vtime[2000]])
        var2x = 'sin_wav(0)_wv_pow'
        var2 = 'test_trange'
        tplot_rename(var2x, var2)
        d = get_data(var2)
        # Since trange is 1001 points, length should be 1001
        self.assertEqual(len(d[0]), 1001)

        # Test resolution
        wav_data(var, dimennum=0, resolution=8)
        var3x = 'sin_wav(0)_wv_pow'
        var3 = 'test_resolution'
        tplot_rename(var3x, var3)
        d = get_data(var3)
        # Since resolution=8, length should be 500
        self.assertEqual(len(d[0]), 500)

        # Test prange
        wav_data(var, dimennum=0, prange=[8, 60])
        var4x = 'sin_wav(0)_wv_pow'
        var4 = 'test_prange'
        tplot_rename(var4x, var4)
        d = get_data(var4)
        # Period range should be within 8 to 60
        p = np.array(1. / d[2])
        print(p)
        self.assertTrue(np.min(p) >= 8.0)
        self.assertTrue(np.max(p) <= 60.0)
        # In this case, the first p should be 8.0
        self.assertAlmostEqual(np.min(p), 8.0, delta=0.01)

        # Plot all results (optional)
        vnames = pyspedas.tplot_names()
        print(vnames)
        tplot(vnames, display=global_display, save_png="wav_data_keywords.png")

    def test_store_data_singleton_v(self):
        times=[0.0,1.0,2.0]
        y=[0.0,1.0,2.0]
        v1=[1]
        v2=[0.1,0.2,0.3]

        # scalar v  (e.g. for 3-vector, or spectrogram with non-time-varying bin values
        store_data('newvar',data={'x':times,'y':y, 'v':v1})
        md=get_data('newvar',metadata=True)
        assert_allclose(md['extra_v_values'],np.array(v1))
        # array v (e.g. spectrogram with time-varying bin values)
        store_data('newvar2',data={'x':times,'y':y, 'v1':v2})
        md=get_data('newvar2',metadata=True)
        assert_allclose(md['extra_v_values'],np.array(v2))


    def test_join_vec(self):
        dat_x = get_data('tha_fgs_fac_bp_x')
        day_y = get_data('tha_fgs_fac_bp_y')
        dat_z = get_data('tha_fgs_fac_bp_z')
        join_vec(['tha_fgs_fac_bp_x','tha_fgs_fac_bp_y','tha_fgs_fac_bp_z'], newname='tha_fgs_joined')
        dat_jv = get_data('tha_fgs_joined')
        self.assertEqual(len(dat_jv),3) # Should have times, yvals, and a 'v' component

    def test_split_rejoin_non_time_varying(self):
        time=np.array([0.0, 1.0, 2.0, 3.0, 4.0])
        yvals = np.array( [[0.0, 0.0, 0.0], [1.0,1.0,1.0], [2.0, 2.0, 2.0], [3.0, 3.0, 3.0], [4.0, 4.0, 4.0]])
        const_v = np.array([11.0, 12.0, 13.0])
        store_data('newvar',data={'x':time, 'y':yvals, 'v':const_v})
        orig_data = get_data('newvar')
        split_vec('newvar')
        join_vec('newvar_*', newname='newvar_rejoined')
        joined_dat=get_data('newvar_rejoined')
        self.assertEqual(len(joined_dat), 3)
        assert_allclose(joined_dat.v, const_v)

    def test_split_rejoin_time_varying(self):
        time=np.array([0.0, 1.0, 2.0, 3.0, 4.0])
        yvals = np.array( [[0.0, 0.0, 0.0], [1.0,1.0,1.0], [2.0, 2.0, 2.0], [3.0, 3.0, 3.0], [4.0, 4.0, 4.0]])
        time_varying_v = np.array([[1.0, 2.0, 3.0], [11.0, 12.0, 13.0], [21.0, 22.0, 23.0], [31.0, 32.0, 33.0], [41.0, 42.0, 43.0]])
        store_data('newvar_tv',data={'x':time, 'y':yvals, 'v':time_varying_v})
        orig_data = get_data('newvar_tv')
        split_vec('newvar_tv')
        dx = get_data('newvar_tv_x')
        md = get_data('newvar_tv_x', metadata=True)
        join_vec('newvar_tv_*', newname='newvar_tv_rejoined')
        joined_dat=get_data('newvar_tv_rejoined')
        self.assertEqual(len(joined_dat), 3)
        assert_allclose(joined_dat.v, time_varying_v)

if __name__ == '__main__':
    unittest.main()
