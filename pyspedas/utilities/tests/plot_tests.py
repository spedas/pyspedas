"""Test plotting functions (mostly for pseudovariables)"""
import unittest


from pyspedas import themis
from pytplot import store_data, options, timespan, tplot

# Set this to false for Github CI tests, set to True for interactive use to see plots.
global_display = False
default_trange=['2007-03-23','2007-03-24']
class PlotTestCases(unittest.TestCase):
    """Test plot functions."""

    def test_line_pseudovariables(self):
        # Test that tplot variables with different number of traces can be combined into a pseudovariable and plotted correctly.
        # Both plots should have 4 properly labeled traces.
        themis.fgm(probe='c', trange=default_trange)
        store_data('comb_3_1',data=['thc_fge_dsl','thc_fge_btotal'])
        store_data('comb_1_3',data=['thc_fge_btotal','thc_fge_dsl'])
        tplot('comb_1_3',save_png='pseudovars_comb_1_3',display=global_display)
        tplot('comb_3_1', save_png='pseudovars_comb_3_1',display=global_display)

    def test_pseudovar_color_options(self):
        themis.fgm(probe='c',trange=default_trange)
        store_data('test_pseudo_colors',data=['thc_fge_dsl','thc_fge_btotal'])
        # Set the color option on the pseudovariable (4 traces total, so 4 colors)
        options('test_pseudo_colors','color',['k','r','g','b'])
        tplot('test_pseudo_colors', save_png='test_pseudo_colors_4color', display=global_display ) # should plot without "incorrect number of line colors" messages
        options('test_pseudo_colors','color',['k']) # All black
        tplot('test_pseudo_colors', save_png='test_pseudo_colors_allsamecolor', display=global_display)

    def test_var_line_options(self):
        themis.fgm(probe='c',trange=default_trange)
        options('thc_fgs_dsl','line_style',['solid','dot','dash'])
        tplot('thc_fgs_dsl',save_png='test_linestyle_3styles',display=global_display)
        options('thc_fgs_dsl','line_style','dot') # gets used for all lines
        tplot('thc_fgs_dsl',save_png='test_linestyle_allsame',display=global_display)

    def test_is_pseudovar(self):
        from pytplot import is_pseudovariable
        themis.fgm(probe='c',trange=default_trange)
        store_data('test_pseudo_colors',data=['thc_fge_dsl','thc_fge_btotal'])
        self.assertTrue(is_pseudovariable('test_pseudo_colors'))
        self.assertFalse(is_pseudovariable('thc_fgs_dsl'))

    def test_count_traces(self):
        from pytplot import count_traces
        themis.fgm(probe='c',trange=default_trange)
        store_data('test_pseudo_colors',data=['thc_fge_dsl','thc_fge_btotal'])
        tr_fge=count_traces('thc_fge_dsl')
        tr_btotal=count_traces('thc_fge_btotal')
        tr_pseudo=count_traces('test_pseudo_colors')
        self.assertEqual(tr_fge,3)
        self.assertEqual(tr_btotal,1)
        self.assertEqual(tr_pseudo,4)
        options('thc_fge_dsl','spec',1)
        tr_pseudo_spec=count_traces('test_pseudo_colors')
        self.assertEqual(tr_pseudo_spec,1)


    def test_pseudovar_line_options(self):
        themis.fgm(probe='c',trange=default_trange)
        store_data('test_pseudo_lineopts',data=['thc_fge_dsl','thc_fge_btotal'])
        # Set the line_style on the pseudovariable (4 traces total, so 4 styles)
        options('test_pseudo_lineopts','line_style',['dot','dash','solid','dash_dot'])
        tplot('test_pseudo_lineopts', save_png='test_pseudo_lineopts_4style',display=global_display)
        # Set all traces to the same style
        options('test_pseudo_lineopts','line_style','dot')
        tplot('test_pseudo_lineopts', save_png='test_pseudo_lineopts_allsame',display=global_display)

    def test_specplot_optimizations(self):
        ask_vars = themis.ask(trange=['2013-11-05', '2013-11-06'])
        timespan('2013-11-05',1,'days')
        # Should plot without errors, show something other than all-blue or vertical lines
        tplot(['thg_ask_atha'],save_png='thg_ask_atha',display=global_display)
        options('thg_ask_atha','y_no_resample',1)
        tplot('thg_ask_atha', save_png='thg_ask_atha_no_resample',display=global_display)
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests

    def test_elfin_specplot(self):
        import pyspedas
        # ELFIN data with V values that oscillate, the original problem that resulted in the resample, this is an angular distrubtion
        timespan('2021-07-14/11:55',10,'minutes')
        epd_var = pyspedas.elfin.epd(trange=['2021-07-14/11:55', '2021-07-14/12:05'], probe='a', level='l2', type_='nflux', fullspin=False)
        tplot('ela_pef_hs_nflux_ch0', display=global_display, save_png='ELFIN_test')
        timespan('2007-03-23',1,'days') # reset to avoid interfering with other tests

    def test_fast_specplot(self):
        import pyspedas
        # FAST TEAMS has fill values -1e31 in V, tod is an energy distribution, the bottom two are pitch angle distributions
        teams_vars = pyspedas.fast.teams(['1998-09-05', '1998-09-06'])
        timespan('1998-09-05',1,'days')
        tplot(['H+', 'H+_low', 'H+_high'], display=global_display, save_png='TEAMS_test')
        timespan('2007-03-23',1,'days') # reset to avoid interfering with other tests

    def test_themis_esa_specplot(self):
        import pyspedas
        # THEMIS ESA has monotonically decreasing energies, time varying energies, and also has fill
        esa_vars = pyspedas.themis.esa(trange=['2016-07-23', '2016-07-24'], probe='a')
        timespan('2016-07-23',1,'days')
        tplot('tha_peef_en_eflux', display=global_display, save_png='PEEF_test')
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests

    def test_erg_specplot(self):
        import pyspedas
        # ERG specplots, only vertical lines on the bottom panel for original resample...
        pyspedas.erg.hep(trange=['2017-03-27', '2017-03-28'])
        timespan('2017-03-27',1,'days')
        tplot(['erg_hep_l2_FEDO_L', 'erg_hep_l2_FEDO_H'], display=global_display, save_png='ERG_test')
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests

    def test_maven_specplot(self):
        from pyspedas.maven.spdf import load
        sta_vars = load(trange=['2020-12-30', '2020-12-31'], instrument='static', datatype='c0-64e2m')
        print(sta_vars)
        timespan('2020-12-30',1,'days')
        # This variable contains all zeroes, and is set to plot with log scaling
        tplot('bkg',display=global_display,save_png='MAVEN_test')
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests

    @unittest.skip(reason="Failing until we establish a default for spec_dim_to_plot")
    def test_maven_fluxes_specplot(self):
        from pyspedas.maven.spdf import load
        swe_vars = load(trange=['2014-10-18', '2014-10-19'], instrument='swea')
        print(swe_vars)
        tplot('diff_en_fluxes')
        timespan('2014-10-18',1,'days')
        # This variable contains all zeroes, and is set to plot with log scaling
        tplot('diff_en_fluxes',display=global_display,save_png='MAVEN_fluxes_test')
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests

    def test_pseudovars_title(self):
        import pyspedas
        from pytplot import store_data, tplot, tplot_options
        pyspedas.themis.state(probe='c',trange=default_trange)
        store_data('ps1', ['thc_spin_initial_delta_phi', 'thc_spin_idpu_spinper'])
        store_data('ps2', ['thc_spin_initial_delta_phi', 'thc_spin_idpu_spinper'])
        store_data('ps3', ['thc_spin_initial_delta_phi', 'thc_spin_idpu_spinper'])
        tplot_options('title', 'plot title')
        plotvars = ['thc_pos', 'ps1', 'thc_vel', 'ps2', 'thc_pos_gse', 'ps3']
        # Should have only one title at the top of the plot
        tplot(plotvars, save_png='test_pseudovars_title', display=global_display)

    def test_pseudovars_spectra(self):
        import pyspedas
        from pytplot import zlim, ylim, timespan

        # Load ESA and SST data
        pyspedas.themis.esa(probe='a', trange=default_trange)
        pyspedas.themis.sst(probe='a', trange=default_trange)

        # Make a combined variable with both ESA and SST spectral data (disjoint energy ranges)
        store_data('combined_spec', ['tha_peif_en_eflux', 'tha_psif_en_eflux'])
        options('tha_peif_en_eflux', 'y_no_resample', 1)
        vars = ['tha_peif_en_eflux', 'combined_spec', 'tha_psif_en_eflux']
        tplot(vars, save_png='test_pseudo_spectra_disjoint_energies', display=global_display)

        # Make a combined variable with full & burst data (same energy ranges, intermittent burst data at higher cadence)
        store_data('esa_srvy_burst', ['tha_peif_en_eflux', 'tha_peib_en_eflux'])
        zlim('tha_peif_en_eflux', 1.0e3, 1.0e7)
        options('tha_peif_en_eflux', 'y_range', [0.5, 1.0e6])

        options('tha_peib_en_eflux', 'y_no_resample', 1)
        zlim('tha_peib_en_eflux', 1.0e3, 1.0e7)
        options('tha_peib_en_eflux', 'y_range', [0.5, 1.0e6])
        options('tha_peib_en_eflux', 'data_gap', 4.0)
        vars = ['tha_peif_en_eflux', 'esa_srvy_burst', 'tha_peib_en_eflux']
        tplot(vars, save_png='test_pseudo_spectra_full_burst',display=global_display)

        # Zoom in o a burst interval
        timespan('2007-03-23/12:20', 10, 'minutes')
        tplot(vars, save_png='test_pseudo_spectra_full_burst_zoomed',display=global_display)
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests


if __name__ == '__main__':
    unittest.main()
