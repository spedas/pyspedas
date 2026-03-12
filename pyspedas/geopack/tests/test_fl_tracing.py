import unittest

import numpy as np

import pyspedas
from pyspedas import (
    data_exists,
    time_double,
    tinterpol,
    join_vec,
    store_data,
    get_data,
    tdeflag,
    del_data,
    set_coords,
    set_units,
    tplot_restore,
    tplotxy3,
    tplotxy,
)

from pyspedas.geopack.get_tsy_params import get_tsy_params
from pyspedas.geopack.get_w_params import get_w
from pyspedas.utilities.config_testing import TESTING_CONFIG, test_data_download_file
import os


# Whether to display plots during testing
global_display = TESTING_CONFIG["global_display"]
# Directory to save testing output files
output_dir = TESTING_CONFIG["local_testing_dir"]
# Ensure output directory exists
geopack_dir = "geopack"
save_dir = os.path.join(output_dir, geopack_dir)
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
# Directory with IDL SPEDAS validation files
validation_dir = TESTING_CONFIG["remote_validation_dir"]

trange = ["2015-10-16", "2015-10-17"]
global_display = False


class LoadTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Download tplot files
        filename = test_data_download_file(
            validation_dir,
            "analysis_tools",
            "ttrace_validate_reduced.tplot",
            save_dir,
        )
        # Uncomment this if you want to use locally generated comparison data including the huge IDL trace variable.
        # filename = '/tmp/ttrace_validate_jumbo.tplot'
        del_data("*")
        tplot_restore(filename)


    def test_trace_iono_s_idl_all(self):
        from pyspedas.geopack import ttrace2endpoint
        d1=get_data('tha_state_pos')
        d2=get_data('tha_iono_t89_trace_s')
        #tplotxy3(['tha_iono_t89_trace'])
        d3=get_data('ifoot_t89_s')
        ttrace2endpoint('tha_state_pos', "t89", 'ionosphere-south', 'py_foot_s', 'py_trace_s', iopt=3, km=True)
        py_trace_data = get_data('py_trace_s')
        py_foot_data = get_data('py_foot_s')
        idl_trace_data = d2.y
        idl_foot_data = d3.y

        set_coords('py_foot_s','GSM')
        set_units('py_foot_s','km')
        set_coords('py_trace_s','GSM')
        set_units('py_trace_s','km')

        t = d1.times[0]
        pos = d1.y[0,:]
        trace_points = py_trace_data.y[0,:,:]
        foot_point = py_foot_data.y[0,:]

        n_py_trace = len(trace_points)
        n_idl_trace = d2.y.shape[1]
        py_tp_array = np.zeros((n_py_trace,3))
        py_tp_array[:,:] = trace_points
        py_time_array = np.zeros(n_py_trace)
        py_time_array[:] = t
        idl_time_array = np.zeros(n_idl_trace)
        idl_time_array[:] = t
        idl_tp_array = np.zeros((n_idl_trace,3))
        idl_tp_array[:,:]= d2.y[0,:,:]

        store_data('py_trace1_s',data={'x':py_time_array, 'y':trace_points})
        pyspedas.set_coords('py_trace1_s','gsm')
        pyspedas.set_units('py_trace1_s','km')
        store_data('idl_trace1_s',data={'x':idl_time_array, 'y':idl_tp_array})
        pyspedas.set_coords('idl_trace1_s','gsm')
        pyspedas.set_units('idl_trace1_s','km')

        max_trace_dist = 0
        max_foot_dist = 0
        max_foot_dist_idx = 0
        max_idl_foot_radius = 0
        min_idl_foot_radius = 1000000
        max_py_foot_radius = 0
        max_py_foot_idx = -1
        min_py_foot_radius = 1000000
        min_py_foot_idx = -1
        min_idl_foot_idx = -1
        max_idl_foot_idx = -1

        for i,time in enumerate(idl_time_array):
            foot_distance = np.linalg.norm(py_foot_data.y[i,:] - idl_foot_data[i,:])
            py_foot_radius = np.linalg.norm(py_foot_data.y[i,:])
            idl_foot_radius = np.linalg.norm(idl_foot_data[i,:])
            max_py_foot_radius = np.max([py_foot_radius,max_py_foot_radius])
            if max_py_foot_radius == py_foot_radius:
                max_py_foot_idx = i
            min_py_foot_radius = np.min([py_foot_radius, min_py_foot_radius])
            if min_py_foot_radius == py_foot_radius:
                min_py_foot_idx = i
            max_idl_foot_radius = np.max([idl_foot_radius, max_idl_foot_radius])
            if max_idl_foot_radius == idl_foot_radius:
                max_idl_foot_idx = i
            min_idl_foot_radius = np.min([idl_foot_radius, min_idl_foot_radius])
            if min_idl_foot_radius == idl_foot_radius:
                min_idl_foot_idx = i

            max_foot_dist = np.max([max_foot_dist,foot_distance])
            if max_foot_dist == foot_distance:
                max_foot_dist_idx = i

        print(f"Max foot distance: {max_foot_dist} at index {max_foot_dist_idx}")
        print(f"Max idl foot radius: {max_idl_foot_radius} at index {max_idl_foot_idx}")
        print(f"Min idl foot radius: {min_idl_foot_radius} at index {min_idl_foot_idx}")
        print(f"Max py foot radius: {max_py_foot_radius} at index {max_py_foot_idx}")
        print(f"Min py foot radius: {min_py_foot_radius} at index {min_py_foot_idx}")

        print(f"Foot points at max idx: py {py_foot_data.y[max_foot_dist_idx,:]} idl {idl_foot_data[max_foot_dist_idx,:]}")
        print(f"Foot radius at max idx: py {np.linalg.norm(py_foot_data.y[max_foot_dist_idx,:])}, idl {np.linalg.norm(idl_foot_data[max_foot_dist_idx,:])}")
        print(f"py foot point {foot_point}, idl foot point {d3.y[0,:]}")
        print(f"foot point distance: {np.linalg.norm(foot_point-d3.y[0,:])}")
        print(f"foot point r: python {np.linalg.norm(foot_point)} idl: {np.linalg.norm(d3.y[0,:])}")
        #tplotxy(['py_trace'], plane='xy')
        tplotxy3(['py_trace1_s', 'idl_trace1_s'], legend_names=['py','idl'], colors=['black', 'red'], markers=['+','>'], reverse_x=True,plot_units='km',show_centerbody=False, display=global_display, save_png='tha_trace_iono_s_singletrace.png')
        tplotxy3(['py_trace_s', 'tha_iono_t89_trace_s', 'tha_state_pos'], legend_names=['py','idl','orbit'], colors=['black', 'red','blue'], markers=[None, None, '+'], reverse_x=True,plot_units='km',show_centerbody=False, display=global_display, save_png='tha_trace_iono_s_full.png')
        tplotxy3(['py_foot_s', 'ifoot_t89_s'], legend_names=['py','idl'], colors=['green','red'],markers=['+',None], reverse_x=True, plot_units = 'km',show_centerbody=True, display=global_display, save_png='tha_trace_iono_s_foot.png')

    def test_trace_iono_n_idl_all(self):
        from pyspedas.geopack import ttrace2endpoint
        d1=get_data('tha_state_pos')
        d2=get_data('tha_iono_t89_trace_n')
        #tplotxy3(['tha_iono_t89_trace'])
        d3=get_data('ifoot_t89_n')
        ttrace2endpoint('tha_state_pos', "t89", 'ionosphere-north', 'py_foot_n', 'py_trace_n', iopt=3, km=True)
        py_trace_data = get_data('py_trace_n')
        py_foot_data = get_data('py_foot_n')
        idl_trace_data = d2.y
        idl_foot_data = d3.y

        set_coords('py_foot_n','GSM')
        set_units('py_foot_n','km')
        set_coords('py_trace_n','GSM')
        set_units('py_trace_n','km')

        t = d1.times[0]
        pos = d1.y[0,:]
        trace_points = py_trace_data.y[0,:,:]
        foot_point = py_foot_data.y[0,:]

        n_py_trace = len(trace_points)
        n_idl_trace = d2.y.shape[1]
        py_tp_array = np.zeros((n_py_trace,3))
        py_tp_array[:,:] = trace_points
        py_time_array = np.zeros(n_py_trace)
        py_time_array[:] = t
        idl_time_array = np.zeros(n_idl_trace)
        idl_time_array[:] = t
        idl_tp_array = np.zeros((n_idl_trace,3))
        idl_tp_array[:,:]= d2.y[0,:,:]

        store_data('py_trace1_n',data={'x':py_time_array, 'y':trace_points})
        pyspedas.set_coords('py_trace1_n','gsm')
        pyspedas.set_units('py_trace1_n','km')
        store_data('idl_trace1_n',data={'x':idl_time_array, 'y':idl_tp_array})
        pyspedas.set_coords('idl_trace1_n','gsm')
        pyspedas.set_units('idl_trace1_n','km')

        max_trace_dist = 0
        max_foot_dist = 0
        max_foot_dist_idx = 0
        max_idl_foot_radius = 0
        min_idl_foot_radius = 1000000
        max_py_foot_radius = 0
        max_py_foot_idx = -1
        min_py_foot_radius = 1000000
        min_py_foot_idx = -1
        min_idl_foot_idx = -1
        max_idl_foot_idx = -1

        for i,time in enumerate(idl_time_array):
            foot_distance = np.linalg.norm(py_foot_data.y[i,:] - idl_foot_data[i,:])
            py_foot_radius = np.linalg.norm(py_foot_data.y[i,:])
            idl_foot_radius = np.linalg.norm(idl_foot_data[i,:])
            max_py_foot_radius = np.max([py_foot_radius,max_py_foot_radius])
            if max_py_foot_radius == py_foot_radius:
                max_py_foot_idx = i
            min_py_foot_radius = np.min([py_foot_radius, min_py_foot_radius])
            if min_py_foot_radius == py_foot_radius:
                min_py_foot_idx = i
            max_idl_foot_radius = np.max([idl_foot_radius, max_idl_foot_radius])
            if max_idl_foot_radius == idl_foot_radius:
                max_idl_foot_idx = i
            min_idl_foot_radius = np.min([idl_foot_radius, min_idl_foot_radius])
            if min_idl_foot_radius == idl_foot_radius:
                min_idl_foot_idx = i

            max_foot_dist = np.max([max_foot_dist,foot_distance])
            if max_foot_dist == foot_distance:
                max_foot_dist_idx = i

        print(f"Max foot distance: {max_foot_dist} at index {max_foot_dist_idx}")
        print(f"Max idl foot radius: {max_idl_foot_radius} at index {max_idl_foot_idx}")
        print(f"Min idl foot radius: {min_idl_foot_radius} at index {min_idl_foot_idx}")
        print(f"Max py foot radius: {max_py_foot_radius} at index {max_py_foot_idx}")
        print(f"Min py foot radius: {min_py_foot_radius} at index {min_py_foot_idx}")

        print(f"Foot points at max idx: py {py_foot_data.y[max_foot_dist_idx,:]} idl {idl_foot_data[max_foot_dist_idx,:]}")
        print(f"Foot radius at max idx: py {np.linalg.norm(py_foot_data.y[max_foot_dist_idx,:])}, idl {np.linalg.norm(idl_foot_data[max_foot_dist_idx,:])}")
        print(f"py foot point {foot_point}, idl foot point {d3.y[0,:]}")
        print(f"foot point distance: {np.linalg.norm(foot_point-d3.y[0,:])}")
        print(f"foot point r: python {np.linalg.norm(foot_point)} idl: {np.linalg.norm(d3.y[0,:])}")
        #tplotxy(['py_trace'], plane='xy')
        tplotxy3(['py_trace1_n', 'idl_trace1_n'], legend_names=['py','idl'], colors=['black', 'red'], markers=['+','>'], reverse_x=True,plot_units='km',show_centerbody=False, display=global_display, save_png='tha_iono_n_singletrace.png')
        tplotxy3(['py_trace_n', 'tha_iono_t89_trace_n', 'tha_state_pos'], legend_names=['py','idl','orbit'], colors=['black', 'red','blue'], markers=[None, None, '+'], reverse_x=True,plot_units='km',show_centerbody=False, display=global_display, save_png='tha_iono_n_all.png')
        tplotxy3(['py_foot_n', 'ifoot_t89_n'], legend_names=['py','idl'], colors=['green','red'],markers=['+',None], reverse_x=True, plot_units = 'km',show_centerbody=True, display=global_display, save_png='tha_iono_n_foot.png')

    def test_t89_equ_idl_all(self):
        from pyspedas.geopack import ttrace2endpoint
        d1=get_data('tha_state_pos')
        #tplotxy3(['tha_iono_t89_trace'])
        d3=get_data('eq_foot_t89')
        ttrace2endpoint('tha_state_pos',"t89", "equator", 'py_eq_foot', 'py_eq_trace', iopt=3, km=True)
        py_trace_data = get_data('py_eq_trace')
        py_foot_data = get_data('py_eq_foot')
        idl_foot_data = d3.y

        set_coords('py_eq_foot','GSM')
        set_units('py_eq_foot','km')
        set_coords('py_eq_trace','GSM')
        set_units('py_eq_trace','km')

        t = d1.times[0]
        pos = d1.y[0,:]
        trace_points = py_trace_data.y[0,:,:]
        foot_point = py_foot_data.y[0,:]

        n_py_trace = len(trace_points)
        py_tp_array = np.zeros((n_py_trace,3))
        py_tp_array[:,:] = trace_points
        py_time_array = np.zeros(n_py_trace)
        py_time_array[:] = t

        store_data('py_eq_trace1',data={'x':py_time_array, 'y':trace_points})
        pyspedas.set_coords('py_eq_trace1','gsm')
        pyspedas.set_units('py_eq_trace1','km')

        max_trace_dist = 0
        max_foot_dist = 0
        max_foot_dist_idx = 0
        max_idl_foot_radius = 0
        min_idl_foot_radius = 1000000
        max_py_foot_radius = 0
        min_py_foot_radius = 1000000
        all_foot_distances = np.zeros(len(d1.times))
        for i, time in enumerate(d1.times):
            foot_distance = np.linalg.norm(py_foot_data.y[i,:] - idl_foot_data[i,:])
            all_foot_distances[i] = foot_distance
            py_foot_radius = np.linalg.norm(py_foot_data.y[i,:])
            idl_foot_radius = np.linalg.norm(idl_foot_data[i,:])
            max_py_foot_radius = np.max([py_foot_radius,max_py_foot_radius])
            min_py_foot_radius = np.min([py_foot_radius, min_py_foot_radius])
            max_idl_foot_radius = np.max([idl_foot_radius, max_idl_foot_radius])
            min_idl_foot_radius = np.min([idl_foot_radius, min_idl_foot_radius])
            max_foot_dist = np.max([max_foot_dist,foot_distance])
            if max_foot_dist == foot_distance:
                max_foot_dist_idx = i
        foot_dist_median = np.median(all_foot_distances)

        # This is an interesting case for the IDL ttrace2equator with /refine.
        # It returns thousands of points on top of each other, never getting more than
        # a few kilometers from the start point.  Maybe it's starting too close to the
        # equator for the initial step size?  The points on either side of it seem similarly
        # affected, but the next ones out seem to work more-or-less OK.

        n=max_foot_dist_idx
        py_single_trace = py_trace_data.y[n-3:n+4,:,:]
        orbit_single_trace = d1.y[n-3:n+4,:]
        store_data('py_eq_trace1',data={'x':d1.times[n-3:n+4], 'y':py_single_trace})
        pyspedas.set_coords('py_eq_trace1','gsm')
        pyspedas.set_units('py_eq_trace1','km')
        # The full trace data for this example is huge (350 MB), too big to store in github.  You can generate it locally with IDL, and use the 'jumbo' version of
        # the output file.
        if data_exists('tha_eq_t89_trace'):
            d2=get_data('tha_eq_t89_trace')
            idl_trace_data = d2.y
            n_idl_trace = d2.y.shape[1]
            idl_time_array = np.zeros(n_idl_trace)
            idl_time_array[:] = t
            idl_tp_array = np.zeros((n_idl_trace, 3))
            idl_tp_array[:, :] = d2.y[0, :, :]
            store_data('idl_eq_trace1',data={'x':idl_time_array, 'y':idl_tp_array})
            pyspedas.set_coords('idl_eq_trace1','gsm')
            pyspedas.set_units('idl_eq_trace1', 'km')
            idl_tp_array = np.zeros((n_idl_trace, 3))
            idl_tp_array[:, :] = d2.y[0, :, :]
            idl_single_trace = idl_trace_data[n - 3:n + 4, :, :]
            store_data('idl_eq_trace1', data={'x': d1.times[n-3:n+4], 'y':idl_single_trace})
            store_data('orbit_trace1', data={'x': d1.times[n - 3:n + 4], 'y': orbit_single_trace})
            pyspedas.set_coords('idl_eq_trace1','gsm')
            pyspedas.set_units('idl_eq_trace1','km')
            tplotxy3(['py_eq_trace1', 'idl_eq_trace1', 'orbit_trace1'], legend_names=['py', 'idl', 'orbit'],
                     colors=['black', 'red', 'blue'], markers=['+', '<', None], markevery=1, linewidths=[2, 1, 1],
                     reverse_x=True, plot_units='km', show_centerbody=False, display=global_display,
                     save_png='tha_equ_singletrace.png')
            tplotxy3(['py_eq_trace', 'tha_eq_t89_trace', 'tha_state_pos'], legend_names=['py', 'idl', 'orbit'],
                     colors=['black', 'red', 'blue'], markers=[None, None, '+'], reverse_x=True, plot_units='km',
                     show_centerbody=False, display=global_display, save_png='tha_equ_all.png')

        # print(f"Max directed trace distance: {max_trace_dist}")
        print(f"Max foot distance: {max_foot_dist} at index {max_foot_dist_idx}")
        print(f"Max idl foot radius: {max_idl_foot_radius}")
        print(f"Min idl foot radius: {min_idl_foot_radius}")
        print(f"Max py foot radius: {max_py_foot_radius}")
        print(f"Min py foot radius: {min_idl_foot_radius}")
        print(f"Median foot point distance: {foot_dist_median}")
        print(f"Python trace points at max foot distance: {len(py_trace_data.y[max_foot_dist_idx, :, :])}")
        print(f"Start point at max foot distance:{d1.y[max_foot_dist_idx,:]}")

        print(f"Foot points at max idx: py {py_foot_data.y[max_foot_dist_idx,:]} idl {idl_foot_data[max_foot_dist_idx,:]}")
        print(f"Foot radius at max idx: py {np.linalg.norm(py_foot_data.y[max_foot_dist_idx,:])}, idl {np.linalg.norm(idl_foot_data[max_foot_dist_idx,:])}")
        print(f"py foot point {foot_point}, idl foot point {d3.y[0,:]}")
        print(f"foot point distance: {np.linalg.norm(foot_point-d3.y[0,:])}")
        print(f"foot point r: python {np.linalg.norm(foot_point)} idl: {np.linalg.norm(d3.y[0,:])}")
        tplotxy3(['py_eq_foot', 'eq_foot_t89'], legend_names=['py','idl'], colors=['green','red'],markers=['+',None], reverse_x=True, plot_units = 'km',show_centerbody=True, display=global_display, save_png='tha_equ_foot.png')

    def test_calculate_lshell(self):
        from pyspedas.geopack import calculate_lshell

        calculate_lshell('tha_state_pos','py_tha_state_lshell')
        pyspedas.tplot('py_tha_state_lshell', display=global_display, save_png='tha_state_lshell.png')
        py_data = get_data('py_tha_state_lshell')
        idl_data = get_data('tha_state_pos_lshell')
        diff = np.abs(idl_data.y - py_data.y)
        max_diff = np.max(diff)
        median_diff = np.median(diff)
        print(f"Max diff: {max_diff}, median diff: {median_diff}")
        self.assertTrue(median_diff < 1.0e-05)

if __name__ == "__main__":
    unittest.main()
