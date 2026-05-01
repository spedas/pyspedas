"""
Time clip of data.

Notes
-----
Similar to tclip.pro in IDL SPEDAS.

"""
import logging
import pyspedas
from pyspedas.tplot_tools import store_data, get_data, tnames, time_float, time_string, tplot_copy
import numpy as np
import copy

def time_clip(
        names,
        time_start,
        time_end,
        newname=None,
        suffix='-tclip',
        overwrite=False,
        interior_clip=False
):
    """
    Clip data from time_start to time_end.

    Parameters
    ----------
    names: str/list of str
        List of tplot variable names to time clip (wildcards accepted)
    time_start : float or string
        Start time.
    time_end : float or string
        End time.
    newname: str/list of str, optional
        List of new names for tplot variables.
        Default: None. If not given, then a suffix is applied or the variables are overwritten
    suffix: str, optional
        A suffix to apply.
        Default: '-tclip'
    overwrite: bool, optional
        If true, overwrite the existing tplot variable.
        Default: False
    interior_clip: bool, optional
        If true, reverse sense of operation and clip out times within the start/end range, for example,
        when manually despiking data.
        Default: False

    Returns
    -------
    list of str
        Returns a list of tplot variables created or changed

    Example
    -------
        >>> # Clip time
        >>> import pyspedas
        >>> x1 = [0, 4, 8, 12, 16]
        >>> time1 = [pyspedas.time_float("2020-01-01") + i for i in x1]
        >>> pyspedas.store_data("a", data={"x": time1, "y": [[1, 2, 3],[2, 3, 4],[3, 4, 5],[4, 5, 6],[5, 6,7]]})
        >>> time_start=time1[0]
        >>> time_end=time1[2]
        >>> pyspedas.time_clip('a',time_start,time_end)
        >>> ac = pyspedas.get_data('a-tclip')
        >>> print(ac)

    """
    if len(names) < 1:
        logging.warning('time_clip: no valid tplot variables specified')
        return

    old_names = tnames(names)

    if len(old_names) < 1:
        logging.warning('time_clip: No valid tplot variables matching '+str(names))
        return

    if overwrite:
        n_names = old_names
    elif (newname is None) or (len(newname) < 1) or (newname == ''):
        n_names = [s + suffix for s in old_names]
    else:
        n_names = newname

    if isinstance(n_names, str):
        n_names = [n_names]

    if len(n_names) != len(old_names):
        logging.warning('time_clip: new names and input names have different lengths, using suffixes instead')
        n_names = [s + suffix for s in old_names]

    # We want the start/end times as both strings (for log messages) and floats (for comparisons)

    if isinstance(time_start, str):
        time_start_str = time_start
        time_start_float = time_float(time_start)
    else:
        time_start_str = time_string(time_start)
        time_start_float = time_start

    if isinstance(time_end, str):
        time_end_str = time_end
        time_end_float = time_float(time_end)
    else:
        time_end_str = time_string(time_end)
        time_end_float = time_end


    if time_start_float > time_end_float:
        logging.error('time_clip: Start time ' + time_start_str +' is larger than end time ' + time_end_str)
        return

    for j in range(len(old_names)):
        if old_names[j] != n_names[j]:
            tplot_copy(old_names[j], n_names[j])

        alldata = get_data(n_names[j])
        metadata = copy.deepcopy(get_data(n_names[j], metadata=True))

        if not isinstance(alldata, tuple): # NRV variable
            continue
            
        time = alldata[0]
        data = alldata[1]
        input_count = len(time)


        if input_count < 1:
            logging.info('time_clip found empty data for variable '+old_names[j])
            continue

        new_time = np.array(time_float(time))

        if interior_clip:
            # Invert sense of default comparison
            cond = (new_time < time_start_float) | (new_time > time_end_float)
        else:
            cond = (new_time >= time_start_float) & (new_time <= time_end_float)

        count = np.count_nonzero(cond)

        if count == 0:
            logging.warning('time_clip: '+ old_names[j] + ' has no data in requested range')
            continue

        if count == input_count:
            logging.debug('Time clip returns full data set for variable '+old_names[j])
            continue

        tmp_q = pyspedas.tplot_tools.data_quants[n_names[j]]

        if 'v1' in tmp_q.coords.keys():
            if len(tmp_q.coords['v1'].values.shape) == 2:
                v1_data = tmp_q.coords['v1'].values[cond, :]
            else:
                v1_data = tmp_q.coords['v1'].values

        if 'v2' in tmp_q.coords.keys():
            if len(tmp_q.coords['v2'].values.shape) == 2:
                v2_data = tmp_q.coords['v2'].values[cond, :]
            else:
                v2_data = tmp_q.coords['v2'].values

        if 'v3' in tmp_q.coords.keys():
            if len(tmp_q.coords['v3'].values.shape) == 2:
                v3_data = tmp_q.coords['v3'].values[cond, :]
            else:
                v3_data = tmp_q.coords['v3'].values

        if 'v' in tmp_q.coords.keys():
            if len(tmp_q.coords['v'].values.shape) == 2:
                v_data = tmp_q.coords['v'].values[cond, :]
            else:
                v_data = tmp_q.coords['v'].values

        if 'spec_bins' in tmp_q.coords.keys():
            if len(tmp_q.coords['spec_bins'].values.shape) == 2:
                v_data = tmp_q.coords['spec_bins']\
                    .values[cond, :]
            else:
                v_data = tmp_q.coords['spec_bins'].values

        try:
            if 'v1' in tmp_q.coords.keys() and\
                'v2' in tmp_q.coords.keys() and\
                    'v3' in tmp_q.coords.keys():
                store_data(n_names[j], data={
                    'x': time[cond],
                    'y': data[cond, :, :, :],
                    'v1': v1_data, 'v2': v2_data, 'v3': v3_data},
                    attr_dict=metadata)
            elif 'v1' in tmp_q.coords.keys() and\
                    'v2' in tmp_q.coords.keys():
                store_data(n_names[j], data={
                    'x': time[cond],
                    'y': data[cond, :, :],
                    'v1': v1_data, 'v2': v2_data},
                    attr_dict=metadata)
            elif 'v1' in tmp_q.coords.keys():
                store_data(n_names[j], data={
                    'x': time[cond],
                    'y': data[cond, :],
                    'v1': v1_data}, attr_dict=metadata)
            elif 'spec_bins' in tmp_q.coords.keys():
                store_data(n_names[j], data={
                    'x': time[cond],
                    'y': data[cond, :],
                    'v': v_data}, attr_dict=metadata)
            elif 'v' in tmp_q.coords.keys():
                store_data(n_names[j], data={
                    'x': time[cond],
                    'y': data[cond, :],
                    'v': v_data}, attr_dict=metadata)
            elif data.ndim == 1:
                store_data(n_names[j], data={
                    'x': time[cond],
                    'y': data[cond]},
                    attr_dict=metadata)
            else:
                store_data(n_names[j], data={
                    'x': time[cond],
                    'y': data[cond]},
                    attr_dict=metadata)
        except Exception as e:
            logging.error('Problem time clipping: ' + n_names[j])
            logging.error('Exception:'+str(e))
            continue

        logging.debug('Time clip was applied to: ' + n_names[j])

    return n_names
