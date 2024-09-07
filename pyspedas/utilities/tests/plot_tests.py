"""Test plotting functions (mostly for pseudovariables)"""
import unittest
import numpy as np

from pyspedas import themis
from pytplot import store_data, options, timespan, tplot, tplot_options, degap, tplot_names, del_data, ylim
import pytplot

# Set this to false for Github CI tests, set to True for interactive use to see plots.
global_display = False
default_trange=['2007-03-23','2007-03-24']
class PlotTestCases(unittest.TestCase):
    """Test plot functions."""

    def test_markers_and_symbols(self):
        # Regression test for lineplot crash when marker sizes are set
        # Taken from pytplot markers and symbols notebook in pyspedas_examples
        store_data('data', data={'x': [1, 2, 3, 4, 5, 6], 'y': [1, 1, 1, 1, 1, 1]})
        tplot('data', display=global_display, save_png='simple_lineplot.png')
        options('data', 'marker', 'X')
        tplot('data', display=global_display, save_png='markers_lineplot.png')
        options('data', 'symbols', True)
        tplot('data', display=global_display, save_png='symbols_lineplot.png')
        options('data', 'marker_size', 200)
        tplot('data', display=global_display, save_png='markersize_lineplot.png')
        options('data', 'symbols', False)
        tplot('data', display=global_display, save_png='markersize_nosymbols_lineplot.png')
        options('data', 'marker_size', 20)
        tplot('data', display=global_display, save_png='markersize20_nosymbols_lineplot.png')
        options('data', 'markevery', 2)
        tplot('data', display=global_display, save_png='markevery_lineplot.png')
        options('data', 'marker', 'H')
        tplot('data', display=global_display, save_png='hexagons_lineplot.png')




    def test_line_pseudovariables(self):
        del_data("*")
        # Test that tplot variables with different number of traces can be combined into a pseudovariable and plotted correctly.
        # Both plots should have 4 properly labeled traces.
        themis.fgm(probe='c', trange=default_trange)
        store_data('comb_3_1',data=['thc_fge_dsl','thc_fge_btotal'])
        store_data('comb_1_3',data=['thc_fge_btotal','thc_fge_dsl'])
        tplot_options('title', 'Pseudovariable with one+three line traces')
        tplot('comb_1_3',save_png='pseudovars_comb_1_3',display=global_display)
        tplot_options('title', 'Pseudovariable with three+one line traces')
        tplot('comb_3_1', save_png='pseudovars_comb_3_1',display=global_display)
        tplot_options('title', '')
        timespan('2007-03-23',1,'days') # reset to avoid interfering with other tests



    def test_pseudovar_color_options(self):
        del_data("*")
        themis.fgm(probe='c',trange=default_trange)
        timespan('2007-03-23', 1, 'days')
        store_data('test_pseudo_colors',data=['thc_fge_dsl','thc_fge_btotal'])
        # Set the color option on the pseudovariable (4 traces total, so 4 colors)
        options('test_pseudo_colors','color',['k','r','g','b'])
        tplot_options('title', 'Trace colors should be black, red, green, blue')
        tplot('test_pseudo_colors', save_png='test_pseudo_colors_4color', display=global_display ) # should plot without "incorrect number of line colors" messages
        options('test_pseudo_colors','color',['k']) # All black
        tplot_options('title', 'Trace colors all black')
        tplot('test_pseudo_colors', save_png='test_pseudo_colors_allsamecolor', display=global_display)
        tplot_options('title', '')
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests

    def test_var_line_options(self):
        del_data("*")
        themis.fgm(probe='c',trange=default_trange)
        timespan('2007-03-23', 1, 'days')
        options('thc_fgs_dsl','line_style',['solid','dot','dash'])
        tplot_options('title', 'Line styles solid, dot, dash')
        tplot('thc_fgs_dsl',save_png='test_linestyle_3styles',display=global_display)
        options('thc_fgs_dsl','line_style','dot') # gets used for all lines
        tplot_options('title', 'Line styles all dot')
        tplot('thc_fgs_dsl',save_png='test_linestyle_allsame',display=global_display)
        tplot_options('title', '')
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests

    def test_ylim(self):
        del_data("*")
        themis.fgm(probe='c',trange=default_trange)
        timespan('2007-03-23', 1, 'days')
        ylim('thc_fgs_dsl',-100, 100)
        tplot_options('title', 'Y limit [-100, 100]')
        tplot('thc_fgs_dsl',save_png='test_ylim',display=global_display)
        tplot_options('title', '')
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests

    def test_is_pseudovar(self):
        del_data("*")
        from pytplot import is_pseudovariable
        themis.fgm(probe='c',trange=default_trange)
        timespan('2007-03-23', 1, 'days')
        store_data('test_pseudo_colors',data=['thc_fge_dsl','thc_fge_btotal'])
        self.assertTrue(is_pseudovariable('test_pseudo_colors'))
        self.assertFalse(is_pseudovariable('thc_fgs_dsl'))
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests

    def test_count_traces(self):
        del_data("*")
        from pytplot import count_traces
        themis.fgm(probe='c',trange=default_trange)
        store_data('test_pseudo_colors',data=['thc_fge_dsl','thc_fge_btotal'])
        tr_fge=count_traces('thc_fge_dsl')
        tr_btotal=count_traces('thc_fge_btotal')
        tr_pseudo=count_traces('test_pseudo_colors')
        self.assertEqual(tr_fge,3)
        self.assertEqual(tr_btotal,1)
        self.assertEqual(tr_pseudo,4)
        # We need to ensure thc_fge_dsl has a 'v' component, so we can pretend this variable is a spectrogram
        fgs_data = pytplot.get_data('thc_fge_dsl')
        fgs_meta = pytplot.get_data('thc_fge_dsl', metadata=True)
        store_data('thc_fge_dsl',data={'x':fgs_data.times, 'y':fgs_data.y, 'v':[0, 1, 2]})
        options('thc_fge_dsl','spec',1)
        tr_pseudo_spec=count_traces('test_pseudo_colors')
        self.assertEqual(tr_pseudo_spec,1)
        tplot_options('title', '')
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests


    def test_pseudovar_line_options(self):
        del_data("*")
        themis.fgm(probe='c',trange=default_trange)
        timespan('2007-03-23', 1, 'days')
        store_data('test_pseudo_lineopts',data=['thc_fge_dsl','thc_fge_btotal'])
        # Set the line_style on the pseudovariable (4 traces total, so 4 styles)
        options('test_pseudo_lineopts','line_style',['dot','dash','solid','dash_dot'])
        tplot_options('title', 'Pseudovar line styles dot, dash, solid, dash_dot')
        tplot('test_pseudo_lineopts', save_png='test_pseudo_lineopts_4style',display=global_display)
        # Set all traces to the same style
        options('test_pseudo_lineopts','line_style','dot')
        tplot_options('title', 'Pseudovar line styles all dot')
        tplot('test_pseudo_lineopts', save_png='test_pseudo_lineopts_allsame',display=global_display)
        tplot_options('title', '')
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests

    def test_specplot_optimizations(self):
        del_data("*")
        ask_vars = themis.ask(trange=['2013-11-05', '2013-11-06'])
        timespan('2013-11-05',1,'days')
        # Should plot without errors, show something other than all-blue or vertical lines
        tplot_options('title', 'Should be mostly dark with a few lighter features')
        tplot(['thg_ask_atha'],save_png='thg_ask_atha',display=global_display)
        options('thg_ask_atha','y_no_resample',1)
        tplot_options('title', 'Should be mostly dark with a few lighter features')
        tplot('thg_ask_atha', save_png='thg_ask_atha_no_resample',display=global_display)
        tplot_options('title', 'Should be somewhat lighter now with logarithmic z scale')
        options('thg_ask_atha','zlog',"log")
        tplot('thg_ask_atha', save_png='thg_ask_atha_no_resample_zlog',display=global_display)
        tplot_options('title', '')
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests

    def test_themis_peef_bins(self):
        del_data("*")
        themis.esa(probe='a',trange=['2016-12-11','2016-12-12'])
        timespan('2016-12-11',1,'days')
        options('tha_peef_en_eflux','yrange', [1000,3000])
        tplot_options('title', 'Logarithmic bin boundaries: should be a boundary at y~=1947 eV, just below the tick mark at y=2000')
        tplot('tha_peef_en_eflux',save_png='tha_peef_en_eflux',display=global_display)
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests

    def test_themis_peef_bins_interp_x(self):
        del_data("*")
        themis.esa(probe='a',trange=['2016-12-11','2016-12-12'])
        timespan('2016-12-11',1,'hours')
        options('tha_peef_en_eflux','yrange', [1000,3000])
        options('tha_peef_en_eflux', 'x_interp',1)
        options('tha_peef_en_eflux', 'x_interp_points', 500)
        tplot_options('title', 'Interpolated along time axis')
        tplot('tha_peef_en_eflux',save_png='tha_peef_en_eflux_interp_x',display=global_display)
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests
        options('tha_peef_en_eflux', 'x_interp',0) # reset for other tests


    def test_themis_peef_bins_interp_y(self):
        del_data("*")
        themis.esa(probe='a',trange=['2016-12-11','2016-12-12'])
        timespan('2016-12-11',1,'hours')
        options('tha_peef_en_eflux','yrange', [1000,3000])
        options('tha_peef_en_eflux', 'y_interp',1)
        options('tha_peef_en_eflux', 'y_interp_points', 200)
        tplot_options('title', 'Interpolated along y axis')
        tplot('tha_peef_en_eflux',save_png='tha_peef_en_eflux_interp_y',display=global_display)
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests
        options('tha_peef_en_eflux', 'y_interp',0) # reset for other tests

    def test_themis_peef_bins_interp_both(self):
        del_data("*")
        themis.esa(probe='a',trange=['2016-12-11','2016-12-12'])
        timespan('2016-12-11',1,'hours')
        options('tha_peef_en_eflux','yrange', [1000,3000])
        options('tha_peef_en_eflux', 'x_interp',1)
        options('tha_peef_en_eflux', 'x_interp_points', 500)
        options('tha_peef_en_eflux', 'y_interp',1)
        options('tha_peef_en_eflux', 'y_interp_points', 200)
        tplot_options('title', 'Interpolated along both x and y axes')
        tplot('tha_peef_en_eflux',save_png='tha_peef_en_eflux_interp_both',display=global_display)
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests
        options('tha_peef_en_eflux', '_interp',0) # reset for other tests
        options('tha_peef_en_eflux', 'y_interp',0) # reset for other tests

    def test_mms_epsd_specplot(self):
        del_data("*")
        from pytplot import options
        from pyspedas import mms_load_dsp
        timespan('2015-08-01',1,'days')
        # Logarithmic Y scale with lowest bin boundary = 0.0 by linear extrapolation from bin centers
        data = mms_load_dsp(trange=['2015-08-01','2015-08-02'], datatype=['epsd', 'bpsd'], level='l2', data_rate='fast')
        # options('mms1_dsp_epsd_omni','yrange',[8.0,130000.0])
        tplot(['mms1_dsp_epsd_omni', 'mms1_dsp_bpsd_omni'], save_png='mms1_epsd_omni', display=global_display)
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests

    def test_elfin_specplot(self):
        del_data("*")
        import pyspedas
        # ELFIN data with V values that oscillate, the original problem that resulted in the resample, this is an angular distrubtion
        timespan('2021-07-14/11:55',10,'minutes')
        epd_var = pyspedas.elfin.epd(trange=['2021-07-14/11:55', '2021-07-14/12:05'], probe='a', level='l2', type_='nflux', fullspin=False)
        tplot_options('title', 'ELFIN data with time-varying bins, should render accurately')
        tplot('ela_pef_hs_nflux_ch0', display=global_display, save_png='ELFIN_test')
        tplot_options('title', '')
        timespan('2007-03-23',1,'days') # reset to avoid interfering with other tests

    def test_fast_specplot(self):
        del_data("*")
        import pyspedas
        # FAST TEAMS has fill values -1e31 in V, top is an energy distribution, the bottom two are pitch angle distributions
        teams_vars = pyspedas.fast.teams(['1998-09-05', '1998-09-06'])
        timespan('1998-09-05',1,'days')
        tplot_options('title', 'Fill should be removed, bottom two panels should go to Y=-90 deg')
        tplot(['H+', 'H+_low', 'H+_high'], display=global_display, save_png='TEAMS_test')
        tplot_options('title', '')
        timespan('2007-03-23',1,'days') # reset to avoid interfering with other tests

    def test_themis_esa_specplot(self):
        del_data("*")
        import pyspedas
        # THEMIS ESA has monotonically decreasing energies, time varying energies, and also has fill
        esa_vars = pyspedas.themis.esa(trange=['2016-07-23', '2016-07-24'], probe='a')
        timespan('2016-07-23',1,'days')
        tplot_options('title', 'Decreasing and time-varying energies, fillvals, should render correctly')
        tplot('tha_peef_en_eflux', display=global_display, save_png='PEEF_test')
        tplot_options('title', '')
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests

    def test_themis_esa_copy_specplot(self):
        del_data("*")
        import pyspedas
        # THEMIS ESA has monotonically decreasing energies, time varying energies, and also has fill
        esa_vars = pyspedas.themis.esa(trange=['2016-07-23', '2016-07-24'], probe='a')
        timespan('2016-07-23',1,'days')
        tplot_options('title', 'Decreasing and time-varying energies, fillvals, should render correctly')
        pyspedas.tplot_copy('tha_peef_en_eflux',new_name='tha_peef_copy')
        tplot('tha_peef_copy', display=global_display, save_png='PEEF_copy_test')
        tplot_options('title', '')
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests

    def test_erg_specplot(self):
        del_data("*")
        import pyspedas
        # ERG specplots, only vertical lines on the bottom panel for original resample...
        pyspedas.erg.hep(trange=['2017-03-27', '2017-03-28'])
        timespan('2017-03-27',1,'days')
        tplot_options('title', 'Time varying spectral bins, should render correctly')
        tplot(['erg_hep_l2_FEDO_L', 'erg_hep_l2_FEDO_H'], display=global_display, save_png='ERG_test')
        tplot_options('title', '')
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests

    def test_maven_specplot(self):
        del_data("*")
        from pyspedas.projects.maven.spdf import load
        sta_vars = load(trange=['2020-12-30', '2020-12-31'], instrument='static', datatype='c0-64e2m')
        print(sta_vars)
        timespan('2020-12-30',1,'days')
        # This variable contains all zeroes, and is set to plot with log scaling
        tplot_options('title', 'Should be all the same color')
        tplot('bkg',display=global_display,save_png='MAVEN_test')
        tplot_options('title', '')
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests

    #@unittest.skip(reason="Failing until we establish a default for spec_dim_to_plot")
    def test_maven_fluxes_specplot(self):
        del_data("*")
        from pyspedas.projects.maven.spdf import load
        swe_vars = load(trange=['2014-10-18', '2014-10-19'], instrument='swea')
        print(swe_vars)
        timespan('2014-10-18',1,'days')
        # This variable has 3 dimensions but is not marked in the CDF as being a specplot.
        # This used to crash in reduce_spec_dataset because the spec_dim_to_plot option was missing.
        tplot_options('title', 'Spec data plotted as lines')
        tplot('diff_en_fluxes', display=global_display, save_png='MAVEN_fluxes_test_nospec')
        options('diff_en_fluxes',"spec",1)
        # Setting the "spec" option also sets the spec_dim_to_plot option to v2 in this case
        tplot_options('title', 'Plotting as spectrum with default spec_dim_to_plot (v2)')
        tplot('diff_en_fluxes',display=global_display,save_png='MAVEN_fluxes_test_v2')
        # Test that the "v1" option also works (it used to crash looking for "v" and not checking "v1")
        options('diff_en_fluxes','spec_dim_to_plot',"v1")
        tplot_options('title', 'Plotting as spectrum with spec_dim_to_plot=v1')
        tplot('diff_en_fluxes',display=global_display,save_png='MAVEN_fluxes_test_v1')
        tplot_options('title', '')
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests

    def test_pseudovars_title(self):
        del_data("*")
        import pyspedas
        from pytplot import store_data
        pyspedas.themis.state(probe='c',trange=default_trange)
        store_data('ps1', ['thc_spin_initial_delta_phi', 'thc_spin_idpu_spinper'])
        store_data('ps2', ['thc_spin_initial_delta_phi', 'thc_spin_idpu_spinper'])
        store_data('ps3', ['thc_spin_initial_delta_phi', 'thc_spin_idpu_spinper'])
        tplot_options('title', 'Plot title should only appear once at top of plot')
        plotvars = ['thc_pos', 'ps1', 'thc_vel', 'ps2', 'thc_pos_gse', 'ps3']
        # Should have only one title at the top of the plot
        tplot(plotvars, save_png='test_pseudovars_title', display=global_display)
        tplot_options('title', '')
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests

    def test_pseudovars_spectra(self):
        del_data("*")
        import pyspedas
        from pytplot import zlim, ylim, timespan

        # Load ESA and SST data
        pyspedas.themis.esa(probe='a', trange=default_trange)
        pyspedas.themis.sst(probe='a', trange=default_trange)

        # Make a combined variable with both ESA and SST spectral data (disjoint energy ranges)
        store_data('combined_spec', ['tha_peif_en_eflux', 'tha_psif_en_eflux'])
        options('tha_peif_en_eflux', 'y_no_resample', 1)
        options('combined_spec','y_range',[5.0, 7e+06])
        vars = ['tha_peif_en_eflux', 'combined_spec', 'tha_psif_en_eflux']
        tplot_options('title', 'Pseudovar with two spectra, disjoint energies: top=ESA, middle=combined, bottom=SST')
        tplot(vars, save_png='test_pseudo_spectra_disjoint_energies', display=global_display)

        tplot_options('title','Original burst variable')
        tplot('tha_peib_en_eflux',display=global_display)
        degap('tha_peib_en_eflux',dt=4.0)
        tplot_options('title','Degapped burst variable')
        tplot('tha_peib_en_eflux',display=global_display)
        # Make a combined variable with full & burst data (same energy ranges, intermittent burst data at higher cadence)
        store_data('esa_srvy_burst', ['tha_peif_en_eflux', 'tha_peib_en_eflux'])
        zlim('tha_peif_en_eflux', 1.0e3, 1.0e7)
        options('tha_peif_en_eflux', 'y_range', [0.5, 1.0e6])

        options('tha_peib_en_eflux', 'y_no_resample', 1)
        zlim('tha_peib_en_eflux', 1.0e3, 1.0e7)
        options('tha_peib_en_eflux', 'y_range', [0.5, 1.0e6])
        options('tha_peib_en_eflux', 'data_gap', 4.0)
        vars = ['tha_peif_en_eflux', 'esa_srvy_burst', 'tha_peib_en_eflux']
        tplot_options('title', 'Combining full & burst cadence with same energies: top=fast, middle=combined, bot=burst')
        tplot(vars, save_png='test_pseudo_spectra_full_burst',display=global_display)
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests

        # Zoom in o a burst interval
        timespan('2007-03-23/12:20', 10, 'minutes')
        tplot_options('title', 'Combined full and burst cadence with same energies (zoomed in) top=fast, mid=combined, bot=burst')
        tplot(vars, save_png='test_pseudo_spectra_full_burst_zoomed',display=global_display)
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests
        tplot_options('title', '')

    def test_pseudo_spectra_plus_line(self):
        del_data("*")
        import pyspedas
        pyspedas.mms.fpi(datatype='des-moms', trange=['2015-10-16', '2015-10-17'])
        pyspedas.mms.edp(trange=['2015-10-16', '2015-10-17'], datatype='scpot')
        # Create a pseudovariable with an energy spectrum plus a line plot of spacecraft potential
        store_data('spec', data=['mms1_des_energyspectr_omni_fast', 'mms1_edp_scpot_fast_l2', 'mms1_edp_scpot_fast_l2'])
        # Set some options so that the spectrum, trace, and y axes are legible
        options('mms1_edp_scpot_fast_l2', 'yrange', [10, 100])
        #options('mms2_edp_scpot_fast_l2', 'right_axis', True)
        options('spec','right_axis','True')
        tplot_options('xmargin', [0.1, 0.2])
        timespan('2015-10-16',1,'days')
        tplot_options('title', 'Pseudovar with energy spectrum plus line plot of s/c potential')
        tplot('spec', xsize=12, display=global_display,save_png='MMS_pseudo_spec_plus_line')
        tplot_options('title', '')
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests

    def test_pseudo_spectra_plus_line_copy(self):
        del_data("*")
        import pyspedas
        pyspedas.mms.fpi(datatype='des-moms', trange=['2015-10-16', '2015-10-17'])
        pyspedas.mms.edp(trange=['2015-10-16', '2015-10-17'], datatype='scpot')
        # Create a pseudovariable with an energy spectrum plus a line plot of spacecraft potential
        store_data('spec', data=['mms1_des_energyspectr_omni_fast', 'mms1_edp_scpot_fast_l2', 'mms1_edp_scpot_fast_l2'])
        # Set some options so that the spectrum, trace, and y axes are legible
        options('mms1_edp_scpot_fast_l2', 'yrange', [10, 100])
        #options('mms2_edp_scpot_fast_l2', 'right_axis', True)
        options('spec','right_axis','True')
        tplot_options('xmargin', [0.1, 0.2])
        timespan('2015-10-16',1,'days')
        tplot_options('title', 'Pseudovar with energy spectrum plus line plot of s/c potential')
        pyspedas.tplot_copy('spec', 'spec_copy')
        tplot('spec_copy', xsize=12, display=global_display,save_png='MMS_pseudo_spec_plus_line')
        tplot_options('title', '')
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests

    def test_psp_flux_plot(self):
        del_data("*")
        import pyspedas
        import pytplot
        import numpy as np
        # import matplotlib.pyplot as plt
        from pytplot import tplot
        spi_vars = pyspedas.psp.spi(trange=['2022-12-12/00:00', '2022-12-12/23:59'], datatype='sf00_l3_mom', level='l3',
                                    time_clip=True)
        time = pytplot.data_quants['psp_spi_EFLUX_VS_ENERGY'].coords['time'].values
        # print(time)
        energy_channel = pytplot.data_quants['psp_spi_EFLUX_VS_ENERGY'].coords['spec_bins'].values
        # print(energy_channel)
        ec = energy_channel[0, :]
        energy_flux = pytplot.data_quants['psp_spi_EFLUX_VS_ENERGY'].values
        # print(energy_flux)
        e_flux = pytplot.data_quants['psp_spi_EFLUX_VS_ENERGY'].coords['v'].values
        energy_flux[energy_flux == 0] = np.nan
        pytplot.store_data('E_Flux', data={'x': time.T, 'y': energy_flux, 'v': energy_channel})
        pytplot.options('E_Flux', opt_dict={'Spec': 1, 'zlog': 1, 'Colormap': 'jet', 'ylog': 1})
        timespan('2022-12-12',1,'days')
        tplot_options('title', 'Parker Solar Probe E_flux')
        tplot('E_Flux',display=global_display, save_png='psp_E_Flux')
        timespan('2007-03-23',1,'days') # Reset to avoid interfering with other tests


if __name__ == '__main__':
    unittest.main()
