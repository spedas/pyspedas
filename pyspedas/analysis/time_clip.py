"""
Time clip of data.

Notes
-----
Similar to tclip.pro in IDL SPEDAS.

"""

import pyspedas
import pytplot
from pytplot import data_quants


def time_clip(names, time_start, time_end, new_names=None, suffix=None,
              overwrite=None):
    """
    Clip data from time_start to time_end.

    Parameters:
    names: str/list of str
        List of pytplot names.
    time_start : float
        Start time.
    time_end : float
        End time.
    new_names: str/list of str, optional
        List of new_names for pytplot variables.
        If '', then pytplot variables are replaced.
        If not given, then a suffix is applied.
    suffix: str, optional
        A suffix to apply. Default is '-m'.
    overwrite: bool, optional
        Replace the existing tplot name.

    Returns
    -------
    None.

    """
    old_names = pyspedas.tnames(names)

    if len(old_names) < 1:
        print('Time clip error: No pytplot names were provided.')
        return

    if suffix is None:
        suffix = '-tclip'

    if overwrite is not None:
        n_names = old_names
    elif new_names is None:
        n_names = [s + suffix for s in old_names]
    else:
        n_names = new_names

    if isinstance(n_names, str):
        n_names = [n_names]

    if len(n_names) != len(old_names):
        n_names = [s + suffix for s in old_names]

    for j in range(len(old_names)):
        if old_names[j] != n_names[j]:
            pyspedas.tcopy(old_names[j], n_names[j])

        alldata = pytplot.get_data(n_names[j])

        if not isinstance(alldata, tuple): # NRV variable
            continue
            
        time = alldata[0]
        data = alldata[1]

        index_start = 0
        index_end = len(time)

        if index_end < 1:
            print('Time clip found empty list.')
            continue

        new_time = pyspedas.time_float(time)
        new_time_start = pyspedas.time_float(time_start)
        new_time_end = pyspedas.time_float(time_end)

        if new_time_start > new_time_end:
            print('Error: Start time is larger than end time.')
            continue

        if (new_time_start > new_time[-1]) or (new_time_end < new_time[0]):
            print('Time clip returns empty data.')
            continue

        if (new_time_start <= new_time[0]) and (new_time_end >= new_time[-1]):
            print('Time clip returns full data set.')
            continue

        for i in range(index_end):
            if new_time[i] >= new_time_start:
                index_start = i
                break
        found_end = index_end
        for i in range(index_start, index_end):
            if new_time[i] > new_time_end:
                found_end = i
                break
        index_end = found_end

        tmp_q = data_quants[n_names[j]]

        if 'v1' in tmp_q.coords.keys():
            if len(tmp_q.coords['v1'].values.shape) == 2:
                v1_data = tmp_q.coords['v1'].values[index_start:index_end, :]
            else:
                v1_data = tmp_q.coords['v1'].values

        if 'v2' in tmp_q.coords.keys():
            if len(tmp_q.coords['v2'].values.shape) == 2:
                v2_data = tmp_q.coords['v2'].values[index_start:index_end, :]
            else:
                v2_data = tmp_q.coords['v2'].values

        if 'v3' in tmp_q.coords.keys():
            if len(tmp_q.coords['v3'].values.shape) == 2:
                v3_data = tmp_q.coords['v3'].values[index_start:index_end, :]
            else:
                v3_data = tmp_q.coords['v3'].values

        if 'v' in tmp_q.coords.keys():
            if len(tmp_q.coords['v'].values.shape) == 2:
                v_data = tmp_q.coords['v'].values[index_start:index_end, :]
            else:
                v_data = tmp_q.coords['v'].values

        if 'spec_bins' in tmp_q.coords.keys():
            if len(tmp_q.coords['spec_bins'].values.shape) == 2:
                v_data = tmp_q.coords['spec_bins']\
                    .values[index_start:index_end, :]
            else:
                v_data = tmp_q.coords['spec_bins'].values

        try:
            if 'v1' in tmp_q.coords.keys() and\
                'v2' in tmp_q.coords.keys() and\
                    'v3' in tmp_q.coords.keys():
                pytplot.store_data(n_names[j], data={
                    'x': time[index_start:index_end],
                    'y': data[index_start:index_end, :, :, :],
                    'v1': v1_data, 'v2': v2_data, 'v3': v3_data})
            elif 'v1' in tmp_q.coords.keys() and\
                    'v2' in tmp_q.coords.keys():
                pytplot.store_data(n_names[j], data={
                    'x': time[index_start:index_end],
                    'y': data[index_start:index_end, :, :],
                    'v1': v1_data, 'v2': v2_data})
            elif 'v1' in tmp_q.coords.keys():
                pytplot.store_data(n_names[j], data={
                    'x': time[index_start:index_end],
                    'y': data[index_start:index_end, :],
                    'v1': v1_data})
            elif 'spec_bins' in tmp_q.coords.keys():
                pytplot.store_data(n_names[j], data={
                    'x': time[index_start:index_end],
                    'y': data[index_start:index_end, :],
                    'v': v_data})
            elif 'v' in tmp_q.coords.keys():
                pytplot.store_data(n_names[j], data={
                    'x': time[index_start:index_end],
                    'y': data[index_start:index_end, :],
                    'v': v_data})
            elif data.ndim == 1:
                pytplot.store_data(n_names[j], data={
                    'x': time[index_start:index_end],
                    'y': data[index_start:index_end]})
            else:
                pytplot.store_data(n_names[j], data={
                    'x': time[index_start:index_end],
                    'y': data[index_start:index_end]})
        except:
            print('Problem time clipping: ' + n_names[j])
            continue

        print('Time clip was applied to: ' + n_names[j])
