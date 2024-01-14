"""
Time clip of data.

Notes
-----
Similar to tclip.pro in IDL SPEDAS.

"""
import logging
import pytplot


def time_clip(names, time_start, time_end, new_names=None, suffix='-tclip',
              overwrite=False):
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
        If not given, then a suffix is applied or the variables are overwritten
    suffix: str, optional
        A suffix to apply.
        Default: '-tclip'
    overwrite: bool, optional
        If true, overwrite the existing tplot variable.
        Default: False

    Returns
    -------
    None.

    """
    if len(names) < 1:
        logging.warning('time_clip: no pytplot variables specified')
        return

    old_names = pytplot.tnames(names)

    if len(old_names) < 1:
        logging.warning('time_clip: No pytplot variables matching '+str(names))
        return

    if overwrite:
        n_names = old_names
    elif (new_names is None) or (len(new_names) < 1) or (new_names == ''):
        n_names = [s + suffix for s in old_names]
    else:
        n_names = new_names

    if isinstance(n_names, str):
        n_names = [n_names]

    if len(n_names) != len(old_names):
        logging.warning('time_clip: new_names and old_names have different lengths, using suffixes instead')
        n_names = [s + suffix for s in old_names]

    if time_start > time_end:
        logging.error('time_clip: Start time '+str(time_start)+' is larger than end time ' + str(time_end))
        return

    for j in range(len(old_names)):
        if old_names[j] != n_names[j]:
            pytplot.tplot_copy(old_names[j], n_names[j])

        alldata = pytplot.get_data(n_names[j])
        metadata = pytplot.get_data(n_names[j], metadata=True)

        if not isinstance(alldata, tuple): # NRV variable
            continue
            
        time = alldata[0]
        data = alldata[1]

        index_start = 0
        index_end = len(time)

        if index_end < 1:
            logging.info('time_clip found empty data for variable '+old_names[j])
            continue

        new_time = pytplot.time_float(time)
        new_time_start = pytplot.time_float(time_start)
        new_time_end = pytplot.time_float(time_end)

        if (new_time_start > new_time[-1]) or (new_time_end < new_time[0]):
            logging.warning('time_clip: '+ old_names[j] + ' has no data in requested range')
            continue

        if (new_time_start <= new_time[0]) and (new_time_end >= new_time[-1]):
            logging.debug('Time clip returns full data set for variable '+old_names[j])
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

        if index_start == index_end:
            logging.warning('time_clip: ' + old_names[j] + ' has no data in requested range')
            continue

        tmp_q = pytplot.data_quants[n_names[j]]

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
                    'v1': v1_data, 'v2': v2_data, 'v3': v3_data},
                    attr_dict=metadata)
            elif 'v1' in tmp_q.coords.keys() and\
                    'v2' in tmp_q.coords.keys():
                pytplot.store_data(n_names[j], data={
                    'x': time[index_start:index_end],
                    'y': data[index_start:index_end, :, :],
                    'v1': v1_data, 'v2': v2_data},
                    attr_dict=metadata)
            elif 'v1' in tmp_q.coords.keys():
                pytplot.store_data(n_names[j], data={
                    'x': time[index_start:index_end],
                    'y': data[index_start:index_end, :],
                    'v1': v1_data}, attr_dict=metadata)
            elif 'spec_bins' in tmp_q.coords.keys():
                pytplot.store_data(n_names[j], data={
                    'x': time[index_start:index_end],
                    'y': data[index_start:index_end, :],
                    'v': v_data}, attr_dict=metadata)
            elif 'v' in tmp_q.coords.keys():
                pytplot.store_data(n_names[j], data={
                    'x': time[index_start:index_end],
                    'y': data[index_start:index_end, :],
                    'v': v_data}, attr_dict=metadata)
            elif data.ndim == 1:
                pytplot.store_data(n_names[j], data={
                    'x': time[index_start:index_end],
                    'y': data[index_start:index_end]},
                    attr_dict=metadata)
            else:
                pytplot.store_data(n_names[j], data={
                    'x': time[index_start:index_end],
                    'y': data[index_start:index_end]},
                    attr_dict=metadata)
        except Exception as e:
            logging.error('Problem time clipping: ' + n_names[j])
            logging.error('Exception:'+str(e))
            continue

        logging.debug('Time clip was applied to: ' + n_names[j])
