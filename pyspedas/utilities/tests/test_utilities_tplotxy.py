"""Test plotting functions (mostly for pseudovariables)"""

import os
import unittest
import numpy as np
from pyspedas.projects import themis
from pyspedas import (
    store_data,
    get_data,
    set_coords,
    set_units,
    cotrans,
    tplotxy,
    tplotxy3,
    tplotxy3_add_mpause,
    tplotxy3_add_neutral_sheet,
    tkm2re,
    tplot_restore,
    tplot_names,
)
from pyspedas.utilities.config_testing import TESTING_CONFIG
from pyspedas import bshock_2, mpause_2, neutral_sheet

# Whether to display plots during testing
global_display = TESTING_CONFIG["global_display"]
# Directory to save testing output files
output_dir = TESTING_CONFIG["local_testing_dir"]
# Ensure output directory exists
save_dir = os.path.join(output_dir, "utilities")
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

default_trange = ["2020-01-01", "2020-01-02"]
global_display=False

class PlotTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        themis.state(trange=default_trange, probe=['a','b','c','d','e'])
        cls.bs = bshock_2()
        cls.mp = mpause_2()
        # This is time-dependent, so we'll just pick the midpoint of the first tplot variable
        d=get_data('tha_pos_gse')
        mid_time = (d.times[-1] - d.times[0])/2.0
        ns_x_re = -1.0*np.arange(0.0,375.0, 5.0)
        times=np.zeros(len(ns_x_re))
        times[:] = mid_time
        ns_gsm_pos=np.zeros((len(ns_x_re),3))
        ns_gsm_pos[:,0] = ns_x_re
        ns = neutral_sheet(times, ns_gsm_pos, model="aen", sc2NS=False)
        ns_gsm_pos[:,2] = ns
        store_data('ns_gsm_pos', data={'x':times, 'y':ns_gsm_pos})
        set_coords('ns_gsm_pos','GSM')
        set_units('ns_gsm_pos', 're')
        cotrans('ns_gsm_pos', 'ns_gse_pos',coord_in='gsm', coord_out='gse')
        cls.gse_dat = get_data('ns_gse_pos')

        tplot_restore('/tmp/ttrace_iono_t89.tplot')
        tplot_names()



    def test_themis_orbit_re(self):
        # Test a simple THEMIS orbit plot in the XY plane, plot units in re
        tplotxy('th?_pos_gse', title='THEMIS+ARTEMIS orbit plot 2020-01-01, units re', reverse_x=True, reverse_y=True, plot_units='re', display=global_display, save_png='orbits_thm_art_re.png')


    def test_themis_orbit_re_legends(self):
        # Test a simple THEMIS orbit plot in the XY plane with legends, plot units in re
        tplotxy('th?_pos_gse',title='THEMIS+ARTEMIS orbit plot 2020-01-01 with legends', legend_names=['THEMIS-A','THEMIS-B','THEMIS-C', 'THEMIS-D', 'THEMIS-E'], reverse_x=True, reverse_y=True, plot_units='re', display=global_display, save_png='orbits_thm_art_re_legends.png')

    def test_themis_orbit_re_badlegends(self):
        # Test a simple THEMIS orbit plot in the XY plane with bad legends, plot units in re
        tplotxy('th?_pos_gse', title='THEMIS+ARTEMIS orbit plot 2020-01-01 with bad legends',legend_names=['THEMIS-A','THEMIS-B'], reverse_x=True, reverse_y=True, plot_units='re', display=global_display, save_png='orbits_thm_art_re_badlegends.png')

    def test_themis_orbit_re_xz(self):
        # Test a simple THEMIS orbit plot in the XZ plane, plot units in re
         tplotxy('th?_pos_gse', title='THEMIS+ARTEMIS orbit plot 2020-01-01, XZ plane, units re',reverse_x=True, reverse_y=False, plane='xz', plot_units='re', display=global_display, save_png='orbits_thm_art_xz_re.png')

    def test_themis_orbit_re_yz(self):
        # Test a THEMIS orbit plot in the YZ plane, no X reversal, plot units in re
         tplotxy('th?_pos_gse', title='THEMIS+ARTEMIS orbit plot 2020-01-01, YZ plane, no reversal, units km', reverse_x=False, reverse_y=False, plane='yz', plot_units='re', display=global_display, save_png='orbits_thm_art_yz_noreverse_re.png')

    def test_themis_orbit_km(self):
        # Test a simple THEMIS-ARTEMIS orbit plot in the XY plane,plot units in km
        tplotxy('th?_pos_gse', title='THEMIS+ARTEMIS orbit plot 2020-01-01, units km',reverse_x=True, reverse_y=True, plot_units='km', display=global_display, save_png='orbits_thm_art_km.png')

    def test_themis_orbit_inner_mixedunits_km(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, plot units km, mixed input units
        tkm2re('the_pos_gse', km=False)
        tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse_re'],title='THEMIS inner orbit plot 2020-01-01, YZ plane, no reversal, units km', reverse_x=True, reverse_y=True, plot_units='km', display=global_display, save_png='orbits_thm_mixed_km.png')

    def test_themis_orbit_inner_mixedunits_re(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, plot units re, mixed input units
        tkm2re('the_pos_gse', km=False)
        tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse_re'],title='THEMIS inner orbit plot 2020-01-01, YZ plane, no reversal, units re', reverse_x=True, reverse_y=True, plot_units='re', display=global_display, save_png='orbits_thm_mixed_re.png')

    def test_themis_orbit_inner_linestyles(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, linestyles, plot units re, mixed input units
        tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse'],title='THEMIS inner orbit plot 2020-01-01, YZ plane, linestyle, units re', legend_names=['THEMIS-A','THEMIS-B','THEMIS-C', 'THEMIS-D', 'THEMIS-E'], reverse_x=True, reverse_y=True, plot_units='re', linestyles=['solid','dotted','dashdot'], display=global_display, save_png='orbits_thm_linestyles.png')

    def test_themis_orbit_inner_markers(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, plot units re, mixed input units
        tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse'],title='THEMIS inner orbit plot 2020-01-01, YZ plane, markers, units re', legend_names=['THEMIS-A','THEMIS-D', 'THEMIS-E'], reverse_x=True, reverse_y=True, plot_units='re', markers=['x','.','+'], markevery=60, display=global_display, save_png='orbits_thm_markers.png')

    def test_themis_orbit_inner_startendmarkers(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, plot units re, mixed input units
        tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse'],title='THEMIS inner orbit plot 2020-01-01, YZ plane, no reversal, startend markers units re', reverse_x=True, reverse_y=True, plot_units='re', startmarkers=['x','.','+'], endmarkers=['x','.','+'], markers=None, display=global_display, save_png='orbits_thm_startendmarkers.png')

    def test_themis_orbit_inner_startmarkers(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, plot units re, mixed input units
        tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse'], title='THEMIS inner orbit plot 2020-01-01, YZ plane, start markers, units re',reverse_x=True, reverse_y=True, plot_units='re', startmarkers=['x','.','+'], markers=None, display=global_display, save_png='orbits_thm_startmarkers.png')

    def test_themis_orbit_inner_linewidths(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, plot units re, mixed input units
        tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse'],title='THEMIS inner orbit plot 2020-01-01, YZ plane, linewidths, units re', reverse_x=True, reverse_y=True, plot_units='re', linewidths=[1,2,3], display=global_display, save_png='orbits_thm_linewidths.png')

    def test_themis_orbit_inner_showearth_xy(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, plot units re, mixed input units
        tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse'], title='THEMIS inner orbit plot 2020-01-01, XY plane, input km, units re',reverse_x=True, reverse_y=True, plot_units='re', show_centerbody=True, display=global_display, save_png='orbits_thm_showearth_xy.png')

    def test_themis_orbit_inner_showearth_xz(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, plot units re, mixed input units
         tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse'],title='THEMIS inner orbit plot 2020-01-01, XZ plane, input km, units re', plane='xz', reverse_x=True, reverse_y=False, plot_units='re', show_centerbody=True, display=global_display, save_png='orbits_thm_showearth_xz.png')


    def test_themis_orbit_inner_showearth_yz(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, plot units re, mixed input units
         tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse'],title='THEMIS inner orbit plot, YZ plane, no reversal, units re', plane='yz', plot_units='re', show_centerbody=True, display=global_display, save_png='orbits_thm_showearth_yz.png')

    def test_themis_orbit_inner_showearth_yz_nocenter(self):
        # Test a simple THEMIS orbit plot in the XY plane, inner probes, plot units re, mixed input units
        tplotxy(['tha_pos_gse', 'thd_pos_gse', 'the_pos_gse'],title='THEMIS inner orbit plot 2020-01-01, YZ plane, no reversal, no centering, units re', plane='yz', center_origin = False, plot_units='re', show_centerbody=True, display=global_display, save_png='orbits_thm_showearth_yz_nocenter.png')

    def test_themis_orbit_re_legends_3planes(self):
        # Test a simple THEMIS orbit plot in the XY plane, plot units in re
         tplotxy3('tha_pos_gse thd_pos_gse the_pos_gse',title='THEMIS inner orbit plot 2020-01-01, all planes, sun left, units re', legend_names=['THEMIS-A','THEMIS-D', 'THEMIS-E'], reverse_x=True, plot_units='re', display=global_display, save_png='orbits_thm_re_legends_3planes.png')

    def test_themis_art_orbit_re_legends_3planes(self):
        # Test a simple THEMIS orbit plot in the XY plane, plot units in re
         tplotxy3('th?_pos_gse',title='THEMIS_ARTEMIS orbit plot 2020-01-01, all planes, sun left, units re', legend_names=['THEMIS-A','THEMIS-D', 'THEMIS-E'], reverse_x=True, plot_units='re', display=global_display, save_png='orbits_thm_art_re_legends_3planes.png')

    def test_themis_orbit_km_legends_3planes_sunright_km(self):
        # Test a simple THEMIS orbit plot in the XY plane, plot units in re
        tplotxy3('tha_pos_gse thd_pos_gse the_pos_gse', title='THEMIS inner orbit plot 2020-01-01, all planes, sun right, units km',legend_names=['THEMIS-A','THEMIS-D', 'THEMIS-E'], plot_units='km', display=global_display, save_png='orbits_thm_re_legends_3planes_sunright_km.png')

    def test_themis_art_orbit_re_legends_extras_3planes(self):
        # Test a simple THEMIS orbit plot in the XY plane, plot units in re
        fig = tplotxy3('th?_pos_gse',title='THEMIS_ARTEMIS orbit plot 2020-01-01, all planes, extras, sun left, units re', legend_names=['THEMIS-A','THEMIS-B', 'THEMIS-C', 'THEMIS-D', 'THEMIS-E'], reverse_x=True, plot_units='re', display=False)
        # Add bow shock to figure
        tplotxy3_add_mpause(self.bs[0],self.bs[1],fig=fig,legend_name="Bow Shock",color='k',linestyle='dotted',linewidth=1,display=False)
        # Add magnetopause to figure
        tplotxy3_add_mpause(self.mp[0],self.mp[1],fig=fig,legend_name="Magnetopause",color='k',linestyle='dashed',linewidth=1,display=False)
        # Add neutral sheet to figure
        tplotxy3_add_neutral_sheet(self.gse_dat.y[:,0],self.gse_dat.y[:,2],fig=fig, legend_name="Neutral sheet",color='k',linestyle='dashdot',linewidth=1,display=global_display,save_png='orbits_thm_art_re_legends_extras_3planes.png')

    def test_themis_art_orbit_re_legends_extras_sunright_3planes(self):
        # Test a simple THEMIS orbit plot in the XY plane, plot units in re
        fig = tplotxy3('th?_pos_gse',title='THEMIS_ARTEMIS orbit plot 2020-01-01, all planes, extras, sun right, units re', legend_names=['THEMIS-A','THEMIS-B', 'THEMIS-C', 'THEMIS-D', 'THEMIS-E'], reverse_x=False, plot_units='re', display=False)
        # Add bow shock to figure
        tplotxy3_add_mpause(self.bs[0],self.bs[1],fig=fig,legend_name="Bow Shock",color='k',linestyle='dotted',linewidth=1,display=False)
        # Add magnetopause to figure
        tplotxy3_add_mpause(self.mp[0],self.mp[1],fig=fig,legend_name="Magnetopause",color='k',linestyle='dashed',linewidth=1,display=False)
        # Add neutral sheet to figure
        tplotxy3_add_neutral_sheet(self.gse_dat.y[:,0],self.gse_dat.y[:,2],fig=fig, legend_name="Neutral sheet",color='k',linestyle='dashdot',linewidth=1,display=global_display,save_png='orbits_thm_art_re_legends_extras_sunright_3planes.png')

    def test_themis_art_orbit_km_legends_extras_3planes(self):
        # Test a simple THEMIS orbit plot in the XY plane, plot units in re
        fig = tplotxy3('th?_pos_gse',title='THEMIS_ARTEMIS orbit plot 2020-01-01, all planes, extras, sun left, units km', legend_names=['THEMIS-A','THEMIS-B', 'THEMIS-C', 'THEMIS-D', 'THEMIS-E'],reverse_x=True, plot_units='km', display=False)
        # Add bow shock to figure
        tplotxy3_add_mpause(self.bs[0],self.bs[1],fig=fig,legend_name="Bow Shock",color='k',linestyle='dotted',linewidth=1,display=False)
        # Add magnetopause to figure
        tplotxy3_add_mpause(self.mp[0],self.mp[1],fig=fig,legend_name="Magnetopause",color='k',linestyle='dashed',linewidth=1,display=False)
        # Add neutral sheet to figure
        tplotxy3_add_neutral_sheet(self.gse_dat.y[:,0],self.gse_dat.y[:,2],fig=fig, legend_name="Neutral sheet",color='k',linestyle='dashdot',linewidth=1,display=global_display,save_png='orbits_thm_art_km_legends_extras_sunright_3planes.png')

    def test_plot_idl_traces(self):
        fig=tplotxy('tha_iono_t89_trace',display=global_display, plane='xy',plot_units='km',legend_names=['tha_t89_iono'],save_jpeg='flines_tha_t89_xy.jpeg')
        fig=tplotxy('tha_iono_t89_trace',display=global_display, plane='xz',plot_units='km',legend_names=['tha_t89_iono'],save_eps='flines_tha_t89_xy.eps')
        fig=tplotxy('tha_iono_t89_trace',display=global_display, plane='yz',plot_units='km',legend_names=['tha_t89_iono'],save_pdf='flines_tha_t89_yz.pdf')
        fig=tplotxy('ifoot_t89',display=global_display, plane='xy',plot_units='km',legend_names=['ifoot_t89'],save_svg='flines_ifoot_t89_xy.svg')
        fig=tplotxy('ifoot_t89',display=global_display, plane='xz',plot_units='km',legend_names=['ifoot_t89'],save_png='flines_ifoot_t89_xz.png')
        fig=tplotxy('ifoot_t89',display=global_display, plane='yz',plot_units='km',legend_names=['ifoot_t89'],save_png='flines_ifoot_t89_yz.png')

    def test_plot_idl_traces_3panels(self):
        fig=tplotxy3('tha_iono_t89_trace',display=global_display, plot_units='km',legend_names=['tha_t89_iono'],save_png='flines_tha_t89_3panel.png')
        fig=tplotxy3('ifoot_t89',display=global_display,plot_units='km',legend_names=['ifoot_t89'],save_png='flines_ifoot_t89_3panel.png')

if __name__ == "__main__":
    unittest.main()
