import os
import unittest
import numpy as np
import logging
import pyspedas
from pyspedas.tplot_tools import data_exists, del_data
from pyspedas.projects.goes.config import CONFIG

global_display = False
outputdir = os.path.join(CONFIG["local_data_dir"], "idltestfiles")
if os.path.exists(outputdir) is False:
    os.makedirs(outputdir)


class LoadTestCases(unittest.TestCase):

    def test_downloadonly(self):
        del_data()
        mag_files = pyspedas.projects.goes.fgm(datatype="1min", downloadonly=True)
        self.assertTrue(os.path.exists(mag_files[0]))

    def test_load_orbit_data(self):
        del_data()
        orbit_vars = pyspedas.projects.goes.orbit(downloadonly=True)
        filename = os.path.basename(orbit_vars[0])
        self.assertEqual(filename, "goes15_ephemeris_ssc_20130101_v01.cdf")
        orbit_vars = pyspedas.projects.goes.orbit(notplot=True, time_clip=False)
        # This should return a dict of tplot structures, but we're getting a list of names, which don't exist as tplot variables.
        self.assertTrue(isinstance(orbit_vars, dict))
        self.assertTrue("g15_orbit_XYZ_GSM" in orbit_vars.keys())
        orbit_vars = pyspedas.projects.goes.orbit(time_clip=True)
        self.assertTrue("g15_orbit_XYZ_GSM" in orbit_vars)
        self.assertTrue("g15_orbit_XYZ_GSE" in orbit_vars)
        self.assertTrue("g15_orbit_XYZ_SM" in orbit_vars)
        self.assertTrue("g15_orbit_XYZ_GEO" in orbit_vars)

        self.assertTrue(data_exists("g15_orbit_XYZ_GSM"))
        self.assertTrue(data_exists("g15_orbit_XYZ_GSE"))
        self.assertTrue(data_exists("g15_orbit_XYZ_SM"))
        self.assertTrue(data_exists("g15_orbit_XYZ_GEO"))
        del_data("*")
        # Both notplot and time_clip specified: should return dictionary, no crash, no tplot variables created
        orbit_vars = pyspedas.projects.goes.orbit(time_clip=True, notplot=True)
        self.assertTrue(isinstance(orbit_vars, dict))
        self.assertFalse(data_exists("g15_orbit_XYZ_GSM"))
        self.assertTrue("g15_orbit_XYZ_GSM" in orbit_vars.keys())

    def test_load_1min_mag_data(self):
        del_data()
        mag_vars = pyspedas.projects.goes.fgm(datatype="1min")
        self.assertTrue("g15_fgm_BX_1" in mag_vars)
        self.assertTrue("g15_fgm_BY_1" in mag_vars)
        self.assertTrue("g15_fgm_BZ_1" in mag_vars)
        self.assertTrue(data_exists("g15_fgm_BX_1"))
        self.assertTrue(data_exists("g15_fgm_BY_1"))
        self.assertTrue(data_exists("g15_fgm_BZ_1"))

    def test_load_5min_mag_data(self):
        del_data()
        mag_vars = pyspedas.projects.goes.fgm(
            datatype="5min",
            probe="10",
            trange=["2000-07-01", "2000-07-02"],
            time_clip=True,
        )
        self.assertTrue("g10_fgm_ht" in mag_vars)
        self.assertTrue(data_exists("g10_fgm_ht"))

    def test_load_full_mag_data(self):
        del_data()
        mag_vars = pyspedas.projects.goes.fgm(datatype="512ms", suffix="_512")
        self.assertTrue("g15_fgm_BX_1_512" in mag_vars)
        self.assertTrue("g15_fgm_BY_1_512" in mag_vars)
        self.assertTrue("g15_fgm_BZ_1_512" in mag_vars)
        self.assertTrue(data_exists("g15_fgm_BX_1_512"))
        self.assertTrue(data_exists("g15_fgm_BY_1_512"))
        self.assertTrue(data_exists("g15_fgm_BZ_1_512"))

    def test_load_1min_epead_data(self):
        del_data()
        epead_vars = pyspedas.projects.goes.epead()
        self.assertTrue("g15_epead_E1E_UNCOR_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_E1E_UNCOR_FLUX"))
        self.assertTrue("g15_epead_E1W_UNCOR_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_E1W_UNCOR_FLUX"))
        self.assertTrue("g15_epead_E2E_UNCOR_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_E2E_UNCOR_FLUX"))
        self.assertTrue("g15_epead_P1E_UNCOR_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_P1E_UNCOR_FLUX"))
        self.assertTrue("g15_epead_P1W_UNCOR_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_P1W_UNCOR_FLUX"))
        self.assertTrue("g15_epead_P2E_UNCOR_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_P2E_UNCOR_FLUX"))
        self.assertTrue("g15_epead_A1E_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_A1E_FLUX"))
        self.assertTrue("g15_epead_A1W_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_A1W_FLUX"))
        self.assertTrue("g15_epead_A2E_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_A2E_FLUX"))

    def test_load_full_epead_data(self):
        del_data()
        epead_vars = pyspedas.projects.goes.epead(datatype="1min")
        self.assertTrue("g15_epead_E1E_UNCOR_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_E1E_UNCOR_FLUX"))
        self.assertTrue("g15_epead_E1W_UNCOR_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_E1W_UNCOR_FLUX"))
        self.assertTrue("g15_epead_E2E_UNCOR_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_E2E_UNCOR_FLUX"))
        self.assertTrue("g15_epead_P1E_UNCOR_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_P1E_UNCOR_FLUX"))
        self.assertTrue("g15_epead_P1W_UNCOR_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_P1W_UNCOR_FLUX"))
        self.assertTrue("g15_epead_P2E_UNCOR_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_P2E_UNCOR_FLUX"))
        self.assertTrue("g15_epead_A1E_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_A1E_FLUX"))
        self.assertTrue("g15_epead_A1W_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_A1W_FLUX"))
        self.assertTrue("g15_epead_A2E_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_A2E_FLUX"))

    def test_load_5min_epead_data(self):
        del_data()
        epead_vars = pyspedas.projects.goes.epead(datatype="5min")
        self.assertTrue("g15_epead_E1E_UNCOR_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_E1E_UNCOR_FLUX"))
        self.assertTrue("g15_epead_E1W_UNCOR_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_E1W_UNCOR_FLUX"))
        self.assertTrue("g15_epead_E2E_UNCOR_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_E2E_UNCOR_FLUX"))
        self.assertTrue("g15_epead_P1E_UNCOR_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_P1E_UNCOR_FLUX"))
        self.assertTrue("g15_epead_P1W_UNCOR_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_P1W_UNCOR_FLUX"))
        self.assertTrue("g15_epead_P2E_UNCOR_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_P2E_UNCOR_FLUX"))
        self.assertTrue("g15_epead_A1E_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_A1E_FLUX"))
        self.assertTrue("g15_epead_A1W_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_A1W_FLUX"))
        self.assertTrue("g15_epead_A2E_FLUX" in epead_vars)
        self.assertTrue(data_exists("g15_epead_A2E_FLUX"))

    def test_load_full_maged_data(self):
        del_data()
        maged_vars = pyspedas.projects.goes.maged(datatype="full")
        self.assertTrue("g15_maged_M_1ME1_DTC_UNCOR_CR" in maged_vars)
        self.assertTrue(data_exists("g15_maged_M_1ME1_DTC_UNCOR_CR"))
        self.assertTrue("g15_maged_M_1ME2_DTC_UNCOR_CR" in maged_vars)
        self.assertTrue(data_exists("g15_maged_M_1ME2_DTC_UNCOR_CR"))
        self.assertTrue("g15_maged_M_1ME3_DTC_UNCOR_CR" in maged_vars)
        self.assertTrue(data_exists("g15_maged_M_1ME3_DTC_UNCOR_CR"))
        self.assertTrue("g15_maged_M_1ME4_DTC_UNCOR_CR" in maged_vars)
        self.assertTrue(data_exists("g15_maged_M_1ME4_DTC_UNCOR_CR"))
        self.assertTrue("g15_maged_M_1ME5_DTC_UNCOR_CR" in maged_vars)
        self.assertTrue(data_exists("g15_maged_M_1ME5_DTC_UNCOR_CR"))

    def test_load_1min_maged_data(self):
        del_data()
        maged_vars = pyspedas.projects.goes.maged(datatype="1min", time_clip=True)
        self.assertTrue("g15_maged_M_1ME1_DTC_UNCOR_FLUX" in maged_vars)
        self.assertTrue(data_exists("g15_maged_M_1ME1_DTC_UNCOR_FLUX"))
        self.assertTrue("g15_maged_M_1ME2_DTC_UNCOR_FLUX" in maged_vars)
        self.assertTrue(data_exists("g15_maged_M_1ME2_DTC_UNCOR_FLUX"))
        self.assertTrue("g15_maged_M_1ME3_DTC_UNCOR_FLUX" in maged_vars)
        self.assertTrue(data_exists("g15_maged_M_1ME3_DTC_UNCOR_FLUX"))
        self.assertTrue("g15_maged_M_1ME4_DTC_UNCOR_FLUX" in maged_vars)
        self.assertTrue(data_exists("g15_maged_M_1ME4_DTC_UNCOR_FLUX"))
        self.assertTrue("g15_maged_M_1ME5_DTC_UNCOR_FLUX" in maged_vars)
        self.assertTrue(data_exists("g15_maged_M_1ME5_DTC_UNCOR_FLUX"))

    def test_load_5min_maged_data(self):
        del_data()
        maged_vars = pyspedas.projects.goes.maged(datatype="5min", time_clip=True)
        self.assertTrue("g15_maged_M_2ME1_DTC_COR_FLUX" in maged_vars)
        self.assertTrue(data_exists("g15_maged_M_2ME1_DTC_COR_FLUX"))
        self.assertTrue("g15_maged_M_2ME2_DTC_COR_FLUX" in maged_vars)
        self.assertTrue(data_exists("g15_maged_M_2ME2_DTC_COR_FLUX"))
        self.assertTrue("g15_maged_M_2ME3_DTC_COR_FLUX" in maged_vars)
        self.assertTrue(data_exists("g15_maged_M_2ME3_DTC_COR_FLUX"))
        self.assertTrue("g15_maged_M_2ME4_DTC_COR_FLUX" in maged_vars)
        self.assertTrue(data_exists("g15_maged_M_2ME4_DTC_COR_FLUX"))
        self.assertTrue("g15_maged_M_2ME5_DTC_COR_FLUX" in maged_vars)
        self.assertTrue(data_exists("g15_maged_M_2ME5_DTC_COR_FLUX"))

    def test_load_full_magpd_data(self):
        del_data()
        magpd_vars = pyspedas.projects.goes.magpd(datatype="full")
        self.assertTrue("g15_magpd_M_1MP1_DTC_UNCOR_CR" in magpd_vars)
        self.assertTrue(data_exists("g15_magpd_M_1MP1_DTC_UNCOR_CR"))
        self.assertTrue("g15_magpd_M_1MP2_DTC_UNCOR_CR" in magpd_vars)
        self.assertTrue(data_exists("g15_magpd_M_1MP2_DTC_UNCOR_CR"))
        self.assertTrue("g15_magpd_M_1MP3_DTC_UNCOR_CR" in magpd_vars)
        self.assertTrue(data_exists("g15_magpd_M_1MP3_DTC_UNCOR_CR"))
        self.assertTrue("g15_magpd_M_1MP4_DTC_UNCOR_CR" in magpd_vars)
        self.assertTrue(data_exists("g15_magpd_M_1MP4_DTC_UNCOR_CR"))
        self.assertTrue("g15_magpd_M_1MP5_DTC_UNCOR_CR" in magpd_vars)
        self.assertTrue(data_exists("g15_magpd_M_1MP5_DTC_UNCOR_CR"))

    def test_load_1min_magpd_data(self):
        del_data()
        magpd_vars = pyspedas.projects.goes.magpd(datatype="1min", time_clip=True)
        self.assertTrue("g15_magpd_M_1MP1_DTC_UNCOR_FLUX" in magpd_vars)
        self.assertTrue(data_exists("g15_magpd_M_1MP1_DTC_UNCOR_FLUX"))
        self.assertTrue("g15_magpd_M_1MP2_DTC_UNCOR_FLUX" in magpd_vars)
        self.assertTrue(data_exists("g15_magpd_M_1MP2_DTC_UNCOR_FLUX"))
        self.assertTrue("g15_magpd_M_1MP3_DTC_UNCOR_FLUX" in magpd_vars)
        self.assertTrue(data_exists("g15_magpd_M_1MP3_DTC_UNCOR_FLUX"))
        self.assertTrue("g15_magpd_M_1MP4_DTC_UNCOR_FLUX" in magpd_vars)
        self.assertTrue(data_exists("g15_magpd_M_1MP4_DTC_UNCOR_FLUX"))
        self.assertTrue("g15_magpd_M_1MP5_DTC_UNCOR_FLUX" in magpd_vars)
        self.assertTrue(data_exists("g15_magpd_M_1MP5_DTC_UNCOR_FLUX"))

    def test_load_full_hepad_data(self):
        del_data()
        hepad_vars = pyspedas.projects.goes.hepad(datatype="full")
        self.assertTrue("g15_hepad_P10_FLUX" in hepad_vars)
        self.assertTrue("g15_hepad_S1_COUNT_RATE" in hepad_vars)
        self.assertTrue(data_exists("g15_hepad_P10_FLUX"))
        self.assertTrue(data_exists("g15_hepad_S1_COUNT_RATE"))

    def test_load_1min_hepad_data(self):
        del_data()
        hepad_vars = pyspedas.projects.goes.hepad(prefix="probename", time_clip=True)
        self.assertTrue("g15_hepad_P10_FLUX" in hepad_vars)
        self.assertTrue("g15_hepad_S1_COUNT_RATE" in hepad_vars)
        self.assertTrue(data_exists("g15_hepad_P10_FLUX"))
        self.assertTrue(data_exists("g15_hepad_S1_COUNT_RATE"))

    def test_load_xrs_data(self):
        del_data()
        xrs_vars = pyspedas.projects.goes.xrs(
            probe="10", datatype="full", trange=["2002-08-01", "2002-08-01"]
        )
        self.assertTrue("g10_xrs_xl" in xrs_vars)
        self.assertTrue(data_exists("g10_xrs_xl"))

    def test_load_xrs_5m_data(self):
        del_data()
        xrs_vars = pyspedas.projects.goes.xrs(
            probe="11",
            datatype="5min",
            trange=["2000-09-01", "2000-09-01"],
            time_clip=True,
        )
        self.assertTrue("g11_xrs_xl" in xrs_vars)
        self.assertTrue(data_exists("g11_xrs_xl"))

    def test_load_xrs_1m_data(self):
        del_data()
        xrs_vars = pyspedas.projects.goes.xrs(
            probe="11",
            datatype="1min",
            trange=["2000-09-01", "2000-09-01"],
            prefix="probename",
            time_clip=True,
        )
        self.assertTrue("g11_xrs_xs" in xrs_vars)
        self.assertTrue(data_exists("g11_xrs_xs"))

    def test_fillval_removal(self):
        del_data()
        trange = ["2024-05-21", "2024-05-22"]
        probe = 18

        pyspedas.projects.goes.euvs(probe=probe, trange=trange)
        pyspedas.projects.goes.xrs(probe=probe, trange=trange)
        local_png = os.path.join(outputdir, "testing_g18_xrs_euvs.png")
        pyspedas.tplot(
            ["g18_euvs_MgII_standard", "g18_xrs_xrsa_flux"],
            display=global_display,
            save_png=local_png,
        )
        d = pyspedas.get_data("g18_euvs_MgII_standard")
        datamin = np.nanmin(d.y)
        # Fillval should be -9999 for this variable, was it removed?
        self.assertTrue(datamin > -1.0)

    def test_xrs_scale(self):
        del_data()
        trange = ["2024-05-21", "2024-05-22"]
        probe = 18

        pyspedas.projects.goes.xrs(probe=probe, trange=trange)
        local_png = os.path.join(outputdir, "testing_g18_xrs_xrsa_flux.png")
        pyspedas.tplot(
            ["g18_xrs_xrsa_flux"],
            display=global_display,
            save_png=local_png,
        )
        md = pyspedas.get_data("g18_xrs_xrsa_flux", metadata=True)
        scale = md["plot_options"]["yaxis_opt"]["y_axis_type"]
        self.assertTrue(scale == "log")

    def test_load_eps_1m_data(self):
        del_data()
        eps_vars = pyspedas.projects.goes.eps(
            trange=["2000-09-01", "2000-09-01"], probe="11", time_clip=True
        )
        self.assertTrue("g11_eps_e1_flux_i" in eps_vars)
        self.assertTrue("g11_eps_e2_flux_i" in eps_vars)
        self.assertTrue("g11_eps_e3_flux_i" in eps_vars)
        self.assertTrue(data_exists("g11_eps_e1_flux_i"))
        self.assertTrue(data_exists("g11_eps_e2_flux_i"))
        self.assertTrue(data_exists("g11_eps_e3_flux_i"))

    def test_load_eps_5m_data(self):
        del_data()
        eps_vars = pyspedas.projects.goes.eps(
            trange=["2000-09-01", "2000-09-01"],
            probe="11",
            datatype="5min",
            time_clip=True,
        )
        self.assertTrue("g11_eps_p1_flux" in eps_vars)
        self.assertTrue("g11_eps_p2_flux" in eps_vars)
        self.assertTrue("g11_eps_p3_flux" in eps_vars)
        self.assertTrue("g11_eps_p4_flux" in eps_vars)
        self.assertTrue("g11_eps_p5_flux" in eps_vars)
        self.assertTrue("g11_eps_p6_flux" in eps_vars)
        self.assertTrue("g11_eps_p7_flux" in eps_vars)
        self.assertTrue(data_exists("g11_eps_p1_flux"))
        self.assertTrue(data_exists("g11_eps_p2_flux"))
        self.assertTrue(data_exists("g11_eps_p3_flux"))
        self.assertTrue(data_exists("g11_eps_p4_flux"))
        self.assertTrue(data_exists("g11_eps_p5_flux"))
        self.assertTrue(data_exists("g11_eps_p6_flux"))
        self.assertTrue(data_exists("g11_eps_p7_flux"))

    def test_load_xrs_data_16(self):
        del_data()
        xrs_vars_16 = pyspedas.projects.goes.xrs(
            probe="16", trange=["2022-09-01", "2022-09-02"]
        )
        self.assertTrue("g16_xrs_xrsa_flux" in xrs_vars_16)
        self.assertTrue(data_exists("g16_xrs_xrsa_flux"))

    def test_load_xrs_data_17_hi(self):
        del_data()
        xrs_vars_17 = pyspedas.projects.goes.xrs(
            probe="17", trange=["2022-07-01", "2022-07-02"], datatype="hi"
        )
        self.assertTrue("g17_xrs_xrsb_flux" in xrs_vars_17)
        self.assertTrue(data_exists("g17_xrs_xrsb_flux"))

    def test_load_euvs_data_17(self):
        del_data()
        euvs_vars_17 = pyspedas.projects.goes.euvs(
            probe="17", trange=["2022-09-01", "2022-09-02"]
        )
        self.assertTrue("g17_euvs_irr_256" in euvs_vars_17)
        self.assertTrue(data_exists("g17_euvs_irr_256"))

    def test_load_euvs_data_16_hi(self):
        del_data()
        euvs_vars_16 = pyspedas.projects.goes.euvs(
            probe="16",
            trange=["2022-08-01", "2022-08-02"],
            prefix="probename",
            datatype="hi",
        )
        self.assertTrue("g16_euvs_irr_256" in euvs_vars_16)
        self.assertTrue(data_exists("g16_euvs_irr_256"))

    def test_load_mag_data_16(self):
        del_data()
        mag_vars_16 = pyspedas.projects.goes.mag(
            probe="16", trange=["2023-01-30", "2023-01-31"], prefix="goes16_"
        )
        self.assertTrue("goes16_b_total" in mag_vars_16)
        self.assertTrue(data_exists("goes16_b_total"))

    def test_load_mag_data_17(self):
        del_data()
        mag_vars_17 = pyspedas.projects.goes.mag(
            probe="17",
            trange=["2022-01-30", "2022-01-31"],
            prefix="goes17_",
            datatype="hi",
        )
        self.assertTrue("goes17_b_gse" in mag_vars_17)
        self.assertTrue(data_exists("goes17_b_gse"))

    def test_load_mpsh_data_17(self):
        del_data()
        mpsh_vars_17 = pyspedas.projects.goes.mpsh(
            probe="17",
            trange=["2022-09-01", "2022-09-02"],
            prefix="probename",
            time_clip=True,
        )
        self.assertTrue("g17_mpsh_AvgDiffElectronFlux" in mpsh_vars_17)
        self.assertTrue(data_exists("g17_mpsh_AvgDiffElectronFlux"))

    def test_load_mpsh_data_16(self):
        del_data()
        mpsh_vars_16 = pyspedas.projects.goes.mpsh(
            probe="16", trange=["2022-10-01", "2022-10-02"], prefix="", datatype="hi"
        )
        self.assertTrue("g16_mpsh_AvgDiffProtonFlux" in mpsh_vars_16)
        self.assertTrue(data_exists("g16_mpsh_AvgDiffProtonFlux"))

    def test_load_sgps_data_16(self):
        del_data()
        sgps_vars_16 = pyspedas.projects.goes.sgps(
            probe="16", trange=["2023-01-30", "2023-01-31"], prefix="probename"
        )
        self.assertTrue("g16_sgps_AvgDiffAlphaFlux" in sgps_vars_16)
        self.assertTrue(data_exists("g16_sgps_AvgDiffAlphaFlux"))

    def test_load_sgps_data_18(self):
        del_data()
        sgps_vars_18 = pyspedas.projects.goes.sgps(
            probe="18",
            trange=["2023-01-30", "2023-01-31"],
            datatype="hi",
            time_clip=True,
        )
        self.assertTrue("g18_sgps_AvgIntProtonFlux" in sgps_vars_18)
        self.assertTrue(data_exists("g18_sgps_AvgIntProtonFlux"))

    def test_load_goes_reprocessed(self):
        # Load reprocessed data, GOES 8-15, GOES-R file format

        # 1. hires mag (large file, slow)
        del_data()
        mag_vars = pyspedas.projects.goes.load(
            probe="13",
            instrument="mag",
            trange=["2015-01-01 00:00:00", "2015-01-01 12:00:00"],
            time_clip=True,
            goes_r=True,
        )
        logging.info(mag_vars)
        self.assertTrue("g13_mag_b_gsm" in mag_vars)
        # tplot("g13_mag_b_gsm")

        # 2. hires xrs
        del_data()
        xrs_vars = pyspedas.projects.goes.load(
            probe="13",
            instrument="xrs",
            datatype="hi",
            trange=["2015-01-20 00:00:00", "2015-01-20 12:00:00"],
            time_clip=True,
            goes_r=True,
        )
        logging.info(xrs_vars)
        self.assertTrue("g13_xrs_a_flux" in xrs_vars)
        self.assertTrue("g13_xrs_b_flux" in xrs_vars)
        # tplot(["g13_xrs_a_flux", "g13_xrs_b_flux"])

        # 3. lowres xrs
        # del_data()
        xrs_vars2 = pyspedas.projects.goes.load(
            probe="13",
            instrument="xrs",
            trange=["2015-01-20 00:00:00", "2015-01-20 12:00:00"],
            time_clip=True,
            goes_r=True,
        )
        logging.info(xrs_vars2)
        self.assertTrue("g13_xrs_xrsa_flux" in xrs_vars2)
        self.assertTrue("g13_xrs_xrsb_flux" in xrs_vars2)
        # tplot(["g13_xrs_xrsa_flux", "g13_xrs_xrsb_flux"])

        # The following shows both hi and lowres xrs data together
        # tplot(["g13_xrs_a_flux", "g13_xrs_xrsa_flux","g13_xrs_b_flux","g13_xrs_xrsb_flux"])


if __name__ == "__main__":
    unittest.main()
