
import numpy as np
import pandas as pd
import zipfile
from tempfile import mkdtemp
from pyspedas import time_double
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import store_data

def get_w(trange=None, create_tvar=False, newname=None):
    """
    This routine downloads the 6 Tsygeneko (TS05) model 
    driving variables W1, W2, W3, W4, W5, W6; from:

    http://geo.phys.spbu.ru/~tsyganenko/TS05_data_and_stuff
    """

    if trange is None:
        print('trange keyword must be specified.')
        return

    years = dailynames(trange=trange, file_format='%Y')
    tmpdir = mkdtemp()

    if newname is None:
        newname = 'Tsy_W_vars_' + '-'.join(years)

    ut_out = np.empty(0)
    w1_out = np.empty(0)
    w2_out = np.empty(0)
    w3_out = np.empty(0)
    w4_out = np.empty(0)
    w5_out = np.empty(0)
    w6_out = np.empty(0)

    for year in years:
        file = download(remote_path='http://geo.phys.spbu.ru/~tsyganenko/TS05_data_and_stuff/',
                        remote_file=year+'_OMNI_5m_with_TS05_variables.???',
                        local_path=tmpdir)

        if file[0][-3:] == 'zip':
            with zipfile.ZipFile(file[0], 'r') as zip_ref:
                zip_ref.extractall(tmpdir)

        rows = pd.read_csv(tmpdir + '/' + year + '_OMNI_5m_with_TS05_variables.dat', delim_whitespace=True, header=None)

        # extract the W variables
        w1 = rows.to_numpy()[:, -6]
        w2 = rows.to_numpy()[:, -5]
        w3 = rows.to_numpy()[:, -4]
        w4 = rows.to_numpy()[:, -3]
        w5 = rows.to_numpy()[:, -2]
        w6 = rows.to_numpy()[:, -1]

        # extract the times
        years = rows.to_numpy()[:, 0]
        doys = rows.to_numpy()[:, 1]
        hours = rows.to_numpy()[:, 2]
        minutes = rows.to_numpy()[:, 3]
        time_strings = [str(int(year)) + '-' + str(int(doy)).zfill(3) + ' ' + str(int(hour)).zfill(2) + ':' + str(int(minute)).zfill(2) for year, doy, hour, minute in zip(years, doys, hours, minutes)]
        unix_times = np.array(time_double(time_strings))

        ut_out = np.append(ut_out, unix_times)
        w1_out = np.append(w1_out, w1)
        w2_out = np.append(w2_out, w2)
        w3_out = np.append(w3_out, w3)
        w4_out = np.append(w4_out, w4)
        w5_out = np.append(w5_out, w5)
        w6_out = np.append(w6_out, w6)

    in_range = np.argwhere((ut_out >= time_double(trange[0])) & (ut_out < time_double(trange[1]))).squeeze()

    if len(in_range) == 0:
        print('No data found in the trange.')
        return

    if create_tvar:
        out = np.array((w1_out[in_range], w2_out[in_range], w3_out[in_range], w4_out[in_range], w5_out[in_range], w6_out[in_range]))
        store_data(newname, data={'x': ut_out[in_range], 'y': out.T})
        return newname

    return {'times': ut_out[in_range], 
            'w1': w1_out[in_range], 
            'w2': w2_out[in_range], 
            'w3': w3_out[in_range], 
            'w4': w4_out[in_range], 
            'w5': w5_out[in_range], 
            'w6': w6_out[in_range]}