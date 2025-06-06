import datetime
import logging
import numpy as np
from pytplot import time_double
from pyspedas.utilities.interpol import interpol


def time_ephemeris(t, et2ut=False):
    """
    Convert between unix time and ephemeris time, based on the IDL routine by Davin Larson

    Parameters
    ==========

    t: float
        Input time to convert, by default unix time (seconds since 1970-01-01)
    et2ut: bool
        If True, convert ephemeris time (seconds since 2000-01-01/11:58:55 UTC) to unix time (Default: False)

    Examples
    ========

    >>> strdate='2025-01-01/00:00:00'
    >>> ut = pyspedas.time_double(strdate)
    >>> et = pyspedas.time_ephemeris(ut)
    >>> print(et)
    788961669.184
    """
    if not isinstance(t, float):
        t = time_double(t)

    ls_utimes = time_double(
        ['0200-1-1', '1972-1-1', '1972-7-1', '1973-1-1', '1974-1-1', '1975-1-1', '1976-1-1', '1977-1-1', '1978-1-1',
         '1979-1-1', '1980-1-1', '1981-7-1', '1982-7-1', '1983-7-1', '1985-7-1', '1988-1-1', '1990-1-1', '1991-1-1', '1992-7-1', '1993-7-1', '1994-7-1',
         '1996-1-1', '1997-7-1', '1999-1-1', '2006-1-1', '2009-1-1', '2012-7-1', '2015-7-1', '2017-1-1', '3000-1-1'])

    ls_num = np.arange(len(ls_utimes)) + 9
    utc_et_diff = time_double('2000-1-1/12:00:00') - 32.184
    ls_etimes = ls_utimes + ls_num - utc_et_diff
    disable_time = time_double('2026-01-01')  # time of next possible leap second

    if time_double() > disable_time - 30*86400.0:
        logging.warning('Warning: This procedure must be modified before ' + str(disable_time) + ' to account for potential leap second')

    if time_double() > disable_time:
        raise ValueError('Sorry!  This procedure has been disabled because it was not modified to account for a possible leap second on ' + str(disable_time))

    if time_double() > disable_time - 7*86400.0:
        logging.warning('Warning: This procedure must be modified before ' + str(disable_time) + ' to account for potential leap second at that time.')

    if et2ut:
        return t - np.floor(interpol(ls_num, ls_etimes, t)) + utc_et_diff

    ut = time_double(t)

    return ut + np.floor(interpol(ls_num, ls_utimes, ut)) - utc_et_diff

