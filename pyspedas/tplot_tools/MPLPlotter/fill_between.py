"""Configure filled regions for tplot panels."""

from copy import deepcopy
from numbers import Real

import numpy as np
import pyspedas
from pyspedas.tplot_tools import tplot_wildcard_expand


def fill_between(variables, y1=None, y2=0, color="gray", alpha=0.2,
                 hatch=None, label=None, zorder=1, delete=False):
    """Store a filled region between two bounds on tplot variables.

    Parameters
    ----------
    variables : str or list of str
        Target panel variables. Wildcards are accepted. A pseudovariable can
        be used to display the two bound variables in the same panel.
    y1 : str or real scalar, optional
        First bound: an exact name of a scalar time-series variable, or a
        finite constant. Defaults to the target variable for each panel.
        Specify an explicit bound when targeting a pseudovariable.
    y2 : str or real scalar, optional
        Second bound, in the same format as y1. Defaults to zero.
        At least one bound must be a time-series variable. Two variable
        bounds must have identical timestamps; no interpolation is performed.
    color : matplotlib color, optional
        Fill color. Defaults to gray.
    alpha : float, optional
        Fill opacity between zero and one. Defaults to 0.2.
    hatch : str, optional
        Matplotlib hatch pattern.
    label : str, optional
        Legend label for the region.
    zorder : real scalar, optional
        Drawing order. Defaults to 1, beneath ordinary Matplotlib lines.
    delete : bool, optional
        Clear all fill regions on the target variables. Other arguments are
        ignored when True.

    Returns
    -------
    list of str
        Names of the target variables whose metadata was updated.

    Raises
    ------
    ValueError
        If targets or bounds are invalid, timestamps differ, or opacity or
        drawing order is invalid. Validation completes before any updates.

    Notes
    -----
    This helper only stores configuration in
    ``attrs['plot_options']['fill_between']``. Rendering support in tplot is
    still required before these settings produce shading.

    Each call appends a region. Bounds are stored as variable references,
    so their data should be resolved and revalidated at draw time. A renderer
    must preserve NaNs and data gaps, apply the requested time range, mask
    nonpositive bounds on logarithmic axes, and respect explicit axis limits.
    Numeric bounds use the same units as the panel.

    Examples
    --------
    >>> from pyspedas.tplot_tools.MPLPlotter.fill_between import fill_between
    >>> pyspedas.store_data('lower', data={'x': [1, 2, 3], 'y': [1, 2, 1]})
    True
    >>> pyspedas.store_data('upper', data={'x': [1, 2, 3], 'y': [3, 4, 3]})
    True
    >>> pyspedas.store_data('bounds', data=['lower', 'upper'])
    True
    >>> fill_between('bounds', y1='lower', y2='upper', color='steelblue')
    ['bounds']
    >>> fill_between('lower', y2=0)
    ['lower']
    >>> fill_between('bounds', delete=True)
    ['bounds']
    """
    names = tplot_wildcard_expand(variables)
    if not names:
        raise ValueError("fill_between: No valid target variables specified.")

    for name in names:
        quant = pyspedas.tplot_tools.data_quants[name]
        if isinstance(quant, dict) or "time" not in quant.dims:
            raise ValueError(f"fill_between: Target {name!r} must be time-varying.")

    if delete:
        for name in names:
            pyspedas.tplot_tools.data_quants[name].attrs["plot_options"].pop(
                "fill_between", None)
        return names

    if not isinstance(alpha, Real) or not np.isfinite(alpha) or not 0 <= alpha <= 1:
        raise ValueError("fill_between: alpha must be between zero and one.")
    if not isinstance(zorder, Real) or not np.isfinite(zorder):
        raise ValueError("fill_between: zorder must be a finite real scalar.")

    def validate_bound(bound):
        if isinstance(bound, str):
            quant = pyspedas.tplot_tools.data_quants.get(bound)
            if quant is None or isinstance(quant, dict):
                raise ValueError(f"fill_between: Bound {bound!r} must be time-varying.")
            opts = quant.attrs.get("plot_options", {})
            if opts.get("overplots_mpl") or opts.get("extras", {}).get("spec"):
                raise ValueError(f"fill_between: Bound {bound!r} must be a scalar time series.")
            if ("time" not in quant.dims or quant.dims[0] != "time"
                    or quant.ndim not in (1, 2)
                    or (quant.ndim == 2 and quant.shape[1] != 1)
                    or not np.issubdtype(quant.dtype, np.number)
                    or np.issubdtype(quant.dtype, np.complexfloating)):
                raise ValueError(f"fill_between: Bound {bound!r} must be a scalar time series.")
            times = quant.time.values
            if times.size == 0 or np.isnat(times).any():
                raise ValueError(f"fill_between: Bound {bound!r} has empty or invalid timestamps.")
            return times
        if not isinstance(bound, Real) or not np.isfinite(bound):
            raise ValueError("fill_between: Bounds must be variable names or finite real scalars.")
        return None

    regions = []
    for name in names:
        first_bound = name if y1 is None else y1
        first_times = validate_bound(first_bound)
        second_times = validate_bound(y2)
        if first_times is None and second_times is None:
            raise ValueError("fill_between: At least one bound must be a time-series variable.")
        if (first_times is not None and second_times is not None
                and not np.array_equal(first_times, second_times)):
            raise ValueError("fill_between: Variable bounds must have identical timestamps.")
        regions.append({
            "y1": first_bound, "y2": y2,
            "color": color, "alpha": alpha, "hatch": hatch,
            "label": label, "zorder": zorder,
        })

    for name, region in zip(names, regions):
        opts = pyspedas.tplot_tools.data_quants[name].attrs["plot_options"]
        if opts.get("fill_between") is None:
            opts["fill_between"] = []
        opts["fill_between"].append(deepcopy(region))
    return names
