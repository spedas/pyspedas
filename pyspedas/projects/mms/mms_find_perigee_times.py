import logging

import numpy as np

from pyspedas.tplot_tools import time_double, time_float_one

from .mec_tools.mec import mms_load_mec

logger = logging.getLogger(__name__)


def mms_find_perigee_times(time, probe: str | int = '1'):
    """Find the MMS perigees bracketing an input time using MEC positions.

    Parameters
    ----------
    time : str or float
        Time of interest, as a time string or Unix time in seconds.
    probe : str or int, optional
        Spacecraft number (1, 2, 3 or 4). Default: '1'.

    Returns
    -------
    numpy.ndarray or None
        Two Unix times in seconds: the last perigee at or before ``time``
        and the first perigee after it. Returns None and logs an error if
        the MEC data do not contain both perigees.

    Raises
    ------
    ValueError
        If time is not a single finite time or probe is not a spacecraft number.

    Notes
    -----
    Port of IDL SPEDAS ``mms_find_perigee_times``, created by Naritoshi Kitamura.
    Uses survey L2 ``epht89d`` ECI positions. A perigee is the first sample
    where geocentric distance stops decreasing; times are limited to the
    resolution of the MEC samples. The search extends one day on either side
    before 2017-02-01, and four days on either side from that date onward,
    matching the IDL routine's search windows.

    Unlike IDL, this routine loads both sides in one request with
    ``notplot=True``, creates no tplot variables, and returns None if either
    perigee cannot be found. It explicitly brackets the input time: IDL's
    preceding search includes a 60-second look-ahead, which can select a
    perigee slightly after the input time.

    Examples
    --------
    >>> from pyspedas.projects.mms import mms_find_perigee_times
    >>> trange = mms_find_perigee_times('2015-09-02/00:00:00', probe='1')
    """
    probe = str(probe).strip()
    if probe not in ('1', '2', '3', '4'):
        raise ValueError('probe must be a single MMS spacecraft number (1, 2, 3 or 4)')
    if time is None:
        raise ValueError('time must be a single finite time')
    try:
        input_time = time_double(time)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError('time must be a single finite time') from exc
    if not isinstance(input_time, float) or not np.isfinite(input_time):
        raise ValueError('time must be a single finite time')

    days = 1 if input_time < time_float_one('2017-02-01') else 4
    trange = [input_time - days * 86400.0, input_time + days * 86400.0]
    data = mms_load_mec(trange=trange.copy(), probe=probe, data_rate='srvy', level='l2',
                        datatype='epht89d', varformat='*_r_eci', notplot=True)
    name = f'mms{probe}_mec_r_eci'
    if not isinstance(data, dict) or name not in data:
        logger.error('No MEC ECI position data found for MMS%s', probe)
        return None

    times = np.asarray(data[name]['x'])
    if np.issubdtype(times.dtype, np.datetime64):
        times = (times - np.datetime64('1970-01-01T00:00:00')) / np.timedelta64(1, 's')
    positions = np.asarray(data[name]['y'])
    # notplot data are not time-clipped by mms_load_mec.
    in_range = (times >= trange[0]) & (times <= trange[1])
    times = times[in_range]
    positions = positions[in_range]
    if times.size < 3:
        logger.error('Insufficient MEC ECI position data for MMS%s', probe)
        return None
    radius = np.linalg.norm(positions, axis=1)
    change = np.diff(radius)
    # Require three adjacent finite samples; do not bridge missing positions.
    finite = np.isfinite(radius[:-2]) & np.isfinite(radius[1:-1]) & np.isfinite(radius[2:])
    perigees = times[1:-1][finite & (change[:-1] < 0) & (change[1:] >= 0)]
    before = perigees[perigees <= input_time]
    after = perigees[perigees > input_time]
    if before.size == 0 or after.size == 0:
        logger.error('Could not find both perigees bracketing the input time for MMS%s', probe)
        return None
    return np.array([before[-1], after[0]])
