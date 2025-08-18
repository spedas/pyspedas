"""Tests of waelet tool."""
import pyspedas
from pyspedas.tplot_tools import get_data, tplot, tplot_rename, ylim, zlim, options, tplot_options
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
        The SPEDAS script that creates the file: general/tools/tplot/wvlt/wavelet_python_validate.pro
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

if __name__ == '__main__':
    unittest.main()
