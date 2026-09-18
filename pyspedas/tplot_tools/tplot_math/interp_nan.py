import pyspedas
import copy
import warnings
import math
from numbers import Integral, Real

import pandas as pd


def interp_nan(tvar, newname=None, s_limit=None, *, max_gap_time=None, max_gap_samples=None):
    """
    Interpolates the tplot variable through NaNs in the data. This is basically just a wrapper for xarray's interpolate_na function.

    .. note::
        This analysis routine assumes the data is no more than 2 dimensions. If there are more, they may become flattened!

    Parameters
    ----------
    tvar : str
        Name of tplot variable.
    newname : str
        Name of new tvar for added data. If not set, then the original tvar is replaced.
    s_limit : int or float, optional
        Deprecated alias for max_gap_time, in seconds. Emits a
        DeprecationWarning. Cannot be combined with max_gap_time.
    max_gap_time : int or float, optional
        Maximum gap duration in seconds. A gap is measured between the valid
        samples immediately before and after a run of NaNs. Gaps equal to this
        limit are filled; longer gaps are left unchanged. None means no time
        limit. Must be finite and non-negative.
    max_gap_samples : int, optional
        Maximum number of consecutive NaNs to fill, following xarray's limit
        parameter. For longer runs, only the first max_gap_samples NaNs are
        filled. None means no sample limit. Must be a positive integer.
        When both limits are supplied, both apply: max_gap_time can prevent
        filling any samples in a gap, regardless of max_gap_samples.

    Returns
    -------
    None

    Examples
    --------
    >>> import pyspedas
    >>> import numpy as np
    >>> pyspedas.store_data('e', data={'x':[2,5,8,11,14,17,21], 'y':[[np.nan,1,1],[np.nan,2,3],[4,np.nan,47],[4,np.nan,5],[5,5,99],[6,6,25],[7,np.nan,-5]]})
    >>> pyspedas.interp_nan('e', 'e_nonan', max_gap_time=5)

    """

    if s_limit is not None:
        warnings.warn(
            "s_limit is deprecated; use max_gap_time (seconds) instead. "
            "Use max_gap_samples for a sample-count limit.",
            DeprecationWarning,
            stacklevel=2,
        )
        if max_gap_time is not None:
            raise ValueError("Specify only one of s_limit and max_gap_time.")
        max_gap_time = s_limit

    # Tplot stores time as datetime64; xarray requires a timedelta for max_gap.
    max_gap = None
    if max_gap_time is not None:
        if (
            not isinstance(max_gap_time, Real)
            or isinstance(max_gap_time, bool)
            or not math.isfinite(max_gap_time)
            or max_gap_time < 0
        ):
            raise ValueError("max_gap_time must be finite and non-negative.")
        max_gap = pd.to_timedelta(max_gap_time, unit="s")

    if max_gap_samples is not None:
        if (
            not isinstance(max_gap_samples, Integral)
            or isinstance(max_gap_samples, bool)
            or max_gap_samples <= 0
        ):
            raise ValueError("max_gap_samples must be a positive integer.")

    x = pyspedas.tplot_tools.data_quants[tvar].interpolate_na(
        dim="time", limit=max_gap_samples, max_gap=max_gap
    )
    x.attrs = copy.deepcopy(pyspedas.tplot_tools.data_quants[tvar].attrs)

    if newname is None:
        pyspedas.tplot_tools.data_quants[tvar] = x
        x.name = tvar
    else:
        pyspedas.tplot_tools.data_quants[newname] = x
        pyspedas.tplot_tools.data_quants[newname].name = newname
