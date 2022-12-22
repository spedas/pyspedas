import numpy as np
import pyspedas.utilities.time_string
from pytplot import get_data, store_data, del_data, cdf_to_tplot
from pyspedas import themis
from .spinmodel import get_spinmodel


def compare_models():
    """  Compare a set of tplot variables representing the SpinmodelSegment and interpolated data
    generated on the fly in Python, or generated elsewhere, stored in a CDF, then loaded as a test
    baseline data set.

    The maximum absolute difference for each data quantity is reported, and if the max difference is
    greater than 0.1, the times and data values associated with the discrepancies are reported.

    :return:
    """
    py_prefix = 'py_seg_'
    idl_prefix = 'seg_'
    py_t1_dat, py_t2_dat = get_data(py_prefix + 't2')
    idl_t1_t, idl_t1_dat = get_data(idl_prefix + 't1')
    all_idx = np.arange(len(py_t1_dat))
    if len(py_t1_dat) != len(idl_t1_dat):
        print("Mismatched segment counts, IDL %d, Python %d" % (len(idl_t1_dat), len(py_t1_dat)))
        return
    for var in ['t1', 't2', 'c1', 'c2', 'b', 'c', 'npts', 'maxgap', 'phaserr', 'idpu_spinper', 'initial_delta_phi',
                'segflags']:
        py_t, py_dat = get_data(py_prefix + var)
        idl_t, idl_dat = get_data(idl_prefix + var)
        diff = abs(py_dat - idl_dat)
        maxdiff = max(diff)
        print("Max %s diff: %e" % (var, maxdiff))
        cond = diff > 0.1
        fail_idx = all_idx[cond]
        if len(fail_idx) > 0:
            print("Diff exceeds tolerance at indices:")
            print(fail_idx)
            print("Segment start times:")
            print(pyspedas.utilities.time_string.time_string(py_t[fail_idx]))
            print("Python vals:")
            print(py_dat[fail_idx])
            print("IDL vals:")
            print(idl_dat[fail_idx])

    py_spinphase_t, py_spinphase_dat = get_data('py_spinphase')
    idl_spinphase_t, idl_spinphase_dat = get_data('interp_spinphase')
    all_idx2 = np.arange(len(py_spinphase_dat))
    if len(py_spinphase_dat) != len(idl_spinphase_dat):
        print("Mismatched interp counts, IDL %d, Python %d" % (len(py_spinphase_dat), len(idl_spinphase_dat)))
    for var in ['spinphase', 'spinper', 'spincount', 'segflags', 't_last', 'eclipse_delta_phi']:
        idl_t, idl_dat = get_data('interp_' + var)
        py_t, py_dat = get_data('py_' + var)
        diff = abs(py_dat - idl_dat)
        maxdiff = max(diff)
        print("Max %s diff: %e" % (var, maxdiff))
        cond = diff > 0.1
        fail_idx2 = all_idx2[cond]
        if len(fail_idx2) > 0:
            print("Diff exceeds tolerance at indices:")
            print(fail_idx2)
            print("Python vals:")
            print(py_dat[fail_idx2])
            print("IDL vals:")
            print(idl_dat[fail_idx2])


def validate_model(filename: str):
    """ Load a probe, correction level, and comparison data from a CDF, then calculate in Python and compare results.

    Args:
        filename (string): A CDF file containing test parameters and comparison results.

    """
    del_data()
    cdf_vars = cdf_to_tplot(filename, get_support_data=True)
    print(cdf_vars)
    t_dummy, trange = get_data('parm_trange')
    t_dummy, probe_idx = get_data('parm_probe')
    t_dummy, correction_level = get_data('parm_correction_level')
    print(trange)
    print(probe_idx)
    int_idx = int(probe_idx)
    probes = ['a', 'b', 'c', 'd', 'e']
    int_corr_level = int(correction_level)
    probe = probes[int_idx]
    print(probe)
    print(int_corr_level)
    thm_data = themis.state(trange=trange, probe=probe, get_support_data=True)
    model = get_spinmodel(probe, int_corr_level)
    model.make_tplot_vars('py_seg_')
    dummy_t, tst_times = get_data('interp_times')
    res = model.interp_t(tst_times)
    store_data('py_spinphase', data={'x': tst_times, 'y': res.spinphase})
    store_data('py_spinper', data={'x': tst_times, 'y': res.spinper})
    store_data('py_spincount', data={'x': tst_times, 'y': res.spincount})
    store_data('py_t_last', data={'x': tst_times, 'y': res.t_last})
    store_data('py_eclipse_delta_phi', data={'x': tst_times, 'y': res.eclipse_delta_phi})
    store_data('py_segflags', data={'x': tst_times, 'y': res.segflags})
    compare_models()
