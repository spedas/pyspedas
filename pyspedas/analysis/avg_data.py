"""
Creates a new pytplot variable as the time average of original.

    Notes
    -----
    Similar to avg_data.pro in IDL SPEDAS.

"""
import numpy as np
import pyspedas
import pytplot


def avg_data(names, dt=None, width=60, noremainder=False,
             new_names=None, suffix=None, overwrite=None):
    """
    Get a new tplot variable with averaged data.

    Parameters
    ----------
    names: str/list of str
        List of pytplot names.
    dt: float, optional
        Time window in seconds for averaging data. It can be less than 1 sec.
    width: int, optional
        Number of values for the averaging window.
        Default is 60 points (usually this means 60 seconds).
        If dt is set, then width is ignored.
    noremainder: boolean, optional
        If True, the remainter (last part of data) will not be included.
        If False. the remainter will be included.
    new_names: str/list of str, optional
        List of new_names for pytplot variables.
        If not given, then a suffix is applied.
    suffix: str, optional
        A suffix to apply. Default is '-avg'.
    overwrite: bool, optional
        Replace the existing tplot name.

    Returns
    -------
    None.

    """
    old_names = pyspedas.tnames(names)

    if len(old_names) < 1:
        print('avg_data error: No pytplot names were provided.')
        return

    if suffix is None:
        suffix = '-avg'

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

    for old_idx, old in enumerate(old_names):
        new = n_names[old_idx]

        d = pytplot.data_quants[old].copy()
        data = d.values
        time = d.time.values

        dim = data.shape
        dim0 = dim[0]
        if len(dim) < 2:
            dim1 = 1
        else:
            dim1 = dim[1]

        new_data = []
        new_time = []
        if dt is None:
            # Use width
            width = int(width)
            # print(dim0, width)
            for i in range(0, dim0, width):
                last = (i + width) if (i + width) < dim0 else dim0
                # idx = int(i + width/2) # redefined below before it's ever used?
                if (i + width > dim0) and noremainder:
                    continue  # Skip the last part of data.
                else:
                    idx = int((i + last - 1)/2)  # Include the last part.
                new_time.append(time[idx])

                if dim1 < 2:
                    nd0 = np.average(data[i:last])
                else:
                    nd0 = []
                    for j in range(dim1):
                        nd0.append(np.average(data[i:last, j]))
                new_data.append(nd0)
        else:
            # Use dt
            dt = float(dt)
            timedbl = np.array(pyspedas.time_float(time))
            alldt = timedbl[-1] - timedbl[0]
            if not dt > 0.0:
                print("avg_data: Time interval dt<=0.0. Exiting.")
                return
            if dt > alldt:
                print("avg_data: Time interval dt is too large. Exiting.")
                return

            # Find bins for time: equal bins of length dt.
            bincount = int(alldt/dt)
            if alldt % dt > 0.0 and not noremainder:  # residual bin
                # Include the last bin which might not be the same size.
                bincount += 1

            time0 = timedbl[0]
            maxtime = timedbl[-1]
            for i in range(bincount):
                time1 = time0 + dt
                bintime = time0 + dt/2.0
                if bintime > maxtime:
                    bintime = maxtime
                new_time.append(bintime)
                # Find all indexes between time0 and time1.
                idx = np.where((timedbl >= time0) & (timedbl < time1))

                # Check if idx is empty, ie. there is a gap in data.
                idx_is_empty = False
                if not idx:
                    idx_is_empty = True
                elif len(idx) == 1:
                    if len(idx[0]) == 0:
                        idx_is_empty = True

                if dim1 < 2:
                    if idx_is_empty:  # Empty list.
                        nd0 = np.nan
                    else:
                        nd0 = np.average(data[idx])
                else:
                    nd0 = []
                    for j in range(dim1):
                        if idx_is_empty:  # Empty list.
                            nd0.append(np.nan)
                        else:
                            nd0.append(np.average(data[idx, j]))
                new_data.append(nd0)
                time0 = time1

        pytplot.store_data(new, data={'x': new_time, 'y': new_data})
        # copy attributes
        pytplot.data_quants[new].attrs = d.attrs.copy()

        print('avg_data was applied to: ' + new)
