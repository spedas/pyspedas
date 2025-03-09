"""
Creates a new tplot variable as the time average of original.

    Notes
    -----
    Similar to avg_data.pro in IDL SPEDAS.

"""
import logging
import numpy as np
from pytplot import store_data, get_data, tnames, time_float


def avg_data(names, trange=[], res=None, width=None,
             newname=None, new_names=None, suffix=None, overwrite=False):
    """
    Get a new tplot variable with averaged data.

    Parameters
    ----------
    names: str/list of str
        List of pytplot names.
    trange: list of float, optional
        Start time, end time.
        If empty, the data start and end time will be used.
    res: float, optional
        Time resolution in seconds for averaging data.
        It can be less than 1 sec.
        Default is 60 sec.
    width: int, optional
        Number of values for the averaging window.
        If res is set, then width is ignored.
    newname: str/list of str, optional
        List of new names for tplot variables.
        If not given, then a suffix is applied.
    new_names: str/list of str, optional (Deprecated)
        List of new names for tplot variables.
        If not given, then a suffix is applied.
    suffix: str, optional
        A suffix to apply.
        Default is '-avg'.
    overwrite: bool, optional
        Replace the existing tplot name.
        Default is False.

    Returns
    -------
    n_names: str/list of str
        List of new pytplot names.

    """

    # new_tvar is deprecated in favor of newname
    if new_names is not None:
        logging.info("avg_data: The new_names parameter is deprecated. Please use newname instead.")
        newname = new_names

    old_names = tnames(names)

    if names is None or len(old_names) < 1:
        logging.error('avg_data: No valid tplot names were provided.')
        return

    if suffix is None:
        suffix = '-avg'

    if overwrite:
        n_names = old_names
    elif newname is None:
        n_names = [s + suffix for s in old_names]
    else:
        n_names = newname

    if isinstance(n_names, str):
        n_names = [n_names]

    if len(n_names) != len(old_names):
        n_names = [s + suffix for s in old_names]

    for old_idx, old in enumerate(old_names):
        new = n_names[old_idx]

        # Get times and data
        d = get_data(old)
        metadata = get_data(old, metadata=True)

        time = d[0]
        time = np.array(time_float(time))
        time_len = len(time)

        data = np.array(d[1])
        dim = data.shape
        dim0 = dim[0]
        if dim0 != time_len:
            logging.error('avg_data: Data and time length mismatch.')
            continue
        if len(dim) < 2:
            dim1 = 1
        else:
            dim1 = dim[1]

        # Data may also contain v, v1, v2, v3
        process_energies = []
        retain_energies = []
        for i in range(len(d)):
            if i > 1:
                if len(d[i]) == len(time):
                    process_energies.append(i)
                else:
                    # These will retained in the results as-is
                    retain_energies.append(i)
        process_v = {}
        for i in process_energies:
            process_v[d._fields[i]] = []

        # Find start and end times
        if trange is not None:
            trange = time_float(trange)
        if len(trange) == 2 and trange[0] < trange[1]:
            time_start = trange[0]
            time_end = trange[1]
        else:
            time_start = time[0]
            time_end = time[-1]

        if time_start < time[0]:
            time_start = time[0]
        if time_end > time[-1]:
            time_end = time[-1]

        # Check for empty set
        count_in_range = len(time[(time >= time_start) & (time <= time_end)])
        if time_end <= time_start or count_in_range < 2:
            logging.error('avg_data: No time values in provided time range.')
            continue

        # Find time bins

        time_duration = time_end - time_start
        if res is None and width is None:
            res = 60  # Default is 60 sec

        if res is not None:
            # Given the resolution, compute bins
            dt = res
            bin_count = int(time_duration/dt)
            ind = np.floor((time-time_start)/dt)
        else:
            # Given the width, compute bins
            bins = np.arange(count_in_range)
            ind = np.floor(bins/width)
            bin_count = int(count_in_range/width)
            dt = time_duration/bin_count

        if bin_count < 2:
            msg = 'avg_data: too few bins. Bins=' + str(bin_count) \
                + ', Data points=' + str(count_in_range)
            logging.error(msg)
            continue

        # Split time into bins
        mdt = (time_end-time_start)/dt
        if (mdt-int(mdt) >= 0.5):
            max_ind = np.ceil(mdt)
        else:
            max_ind = np.floor(mdt)
        w1 = np.asarray(ind < 0).nonzero()
        ind[w1] = -1
        w2 = np.asarray(ind >= max_ind).nonzero()
        ind[w2] = -1

        # Find new times
        mx = np.max(ind)+1
        new_times = (np.arange(mx)+0.5)*dt + time_start

        # Find new data
        new_data = []
        for i in range(int(max_ind)):
            if i < 0:
                continue

            idx0 = np.asarray(ind == i).nonzero()
            isempty = True if len(idx0) < 1 else False

            if dim1 < 2:
                nd0 = np.nan if isempty else np.average(data[idx0])
            else:
                nd0 = []
                for j in range(dim1):
                    nd0.append(np.nan) if isempty else nd0.append(np.average(data[idx0, j]))
            new_data.append(nd0)

            for i in process_energies:
                # The following processes v, v1, v2, v3
                dime1 = len(d[i][0])
                if dime1 < 2:
                    nd1 = np.nan if isempty else np.average(d[i][idx0])
                else:
                    nd1 = []
                    for j in range(dime1):
                        nd1.append(np.nan) if isempty else nd1.append(np.average(d[i][idx0, j]))
                process_v[d._fields[i]].append(nd1)

        # Create the new tplot variable
        data_dict = {'x': new_times, 'y': new_data}
        for i in retain_energies:
            data_dict[d._fields[i]] = d[i]
        for i in process_energies:
            data_dict[d._fields[i]] = process_v[d._fields[i]]

        store_data(new, data=data_dict, attr_dict=metadata)

        logging.info('avg_data was applied to: ' + new)

    return n_names
