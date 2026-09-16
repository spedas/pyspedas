"""Component-wise interpolation of time series, following IDL SPEDAS."""

from collections.abc import Mapping
from copy import deepcopy
import logging
import re

import numpy as np
import pandas as pd
import xarray as xr
from scipy.interpolate import CubicSpline


def _times(values):
    """Normalize time to nanosecond ticks without a float epoch round-trip."""
    values = np.asarray(values)
    if values.ndim != 1:
        raise ValueError("Times must be one-dimensional.")
    if not len(values):
        return np.empty(0, dtype='datetime64[ns]')
    if values.dtype.kind == 'M' and np.isnat(values).any():
        raise ValueError("Times must not contain NaT.")
    if values.dtype.kind in 'iuf':
        if not np.isfinite(values).all():
            raise ValueError("Times must be finite.")
        converted = pd.to_datetime(values, unit='s', utc=True)
    else:
        converted = pd.to_datetime(values, utc=True, format='mixed')
    result = converted.tz_localize(None).as_unit('ns').to_numpy()
    if np.isnat(result).any():
        raise ValueError("Times must not contain NaT.")
    return result


def _interval(a, b):
    """Subtract integer ns ticks without overflow or rounding absolute epochs."""
    return ((a // 10**9 - b // 10**9).astype(np.float64) * 1e9
            + (a % 10**9 - b % 10**9))


def _local_polynomial(x, v, target, method):
    """IDL INTERPOL neighborhoods: three-point quadratic or local natural spline.

    Select the neighborhood from the interval's left endpoint, clamping at
    either edge. Extrapolation evaluates that same endpoint neighborhood.
    Use relative times to preserve subsecond precision at modern epochs.
    """
    left = np.searchsorted(x, target, side='right') - 1
    width = 3 if method == 'quadratic' else 4
    start = np.clip(left, 1, len(x) - width + 1) - 1
    result = np.full(len(target), np.nan, dtype=v.dtype)
    if method == 'quadratic':
        result[:] = 0
        for j in range(3):
            weight = np.ones(len(target))
            for k in range(3):
                if k != j:
                    weight *= (_interval(target, x[start + k])
                               / _interval(x[start + j], x[start + k]))
            result += weight * v[start + j]
    elif len(target):
        # Group targets by neighborhood, fitting each local spline only once.
        order = np.argsort(start, kind='stable')
        groups = np.split(order, np.flatnonzero(np.diff(start[order])) + 1)
        for indices in groups:
            first = start[indices[0]]
            ys = v[first:first + 4]
            # A missing value contaminates its entire four-point stencil.
            # CubicSpline rejects nonfinite values; leave those results NaN.
            if not np.isfinite(ys).all():
                continue
            xs = _interval(x[first:first + 4], x[first]) / 1e9
            ts = _interval(target[indices], x[first]) / 1e9
            result[indices] = CubicSpline(xs, ys, bc_type='natural')(ts)
    return result


def _interpolate_values(values, times, target, ignore_nans=False, bounds='extrapolate',
                        method='linear'):
    """Interpolate each flattened component; ticks are ordered integer ns."""
    values = np.asarray(values)
    if values.dtype.kind not in 'biufc':
        raise TypeError("Time-dependent values must be numeric.")
    if values.ndim == 0:
        values = values.reshape(1)
    if values.shape[0] != len(times):
        raise ValueError("The first data dimension must match the source times.")
    dtype = np.result_type(values.dtype, np.float64)
    flat = values.reshape(len(times), -1).astype(dtype, copy=False)
    result = np.full((len(target), flat.shape[1]), np.nan, dtype=dtype)
    outside = (target < times[0]) | (target > times[-1])
    for component in range(flat.shape[1]):
        y = flat[:, component]
        valid = ~np.isnan(y) if ignore_nans else np.ones(len(y), dtype=bool)
        x, v = times[valid], y[valid]
        column = result[:, component]
        if len(x) == 1:
            column[:] = v[0]
        elif len(x) > 1:
            right = np.searchsorted(x, target, side='left')
            exact = (right < len(x)) & (x[np.minimum(right, len(x) - 1)] == target)
            column[exact] = v[right[exact]]
            evaluate = ~exact
            t = target[evaluate]
            hi = np.clip(right[evaluate], 1, len(x) - 1)
            lo = hi - 1
            with np.errstate(invalid='ignore', over='ignore'):
                if method == 'previous':
                    index = np.clip(np.searchsorted(x, t, side='right') - 1, 0, len(x) - 1)
                    column[evaluate] = v[index]
                elif method == 'nearest':
                    # Strict comparison resolves midpoint ties to the earlier time.
                    index = np.where(_interval(t, x[lo]) > _interval(x[hi], t), hi, lo)
                    column[evaluate] = v[index]
                elif ((method == 'quadratic' and len(x) >= 3)
                      or (method == 'spline' and len(x) >= 4)):
                    column[evaluate] = _local_polynomial(x, v, t, method)
                else:
                    # Too few samples for the requested polynomial: use linear.
                    fraction = _interval(t, x[lo]) / _interval(x[hi], x[lo])
                    column[evaluate] = (1 - fraction) * v[lo] + fraction * v[hi]
        if bounds == 'nan':
            column[outside] = np.nan
        elif bounds == 'repeat':
            finite = y[np.isfinite(y)]
            if len(finite):
                column[target < times[0]] = finite[0]
                column[target > times[-1]] = finite[-1]
    return result.reshape((len(target),) + values.shape[1:])


def _previous_bins(values, times, target, bounds):
    """Select complete bin maps; never blend maps or fill their missing bins."""
    index = np.clip(np.searchsorted(times, target, side='right') - 1, 0, len(times) - 1)
    result = values[index].copy()
    if bounds == 'nan':
        outside = (target < times[0]) | (target > times[-1])
        if outside.any():
            dtype = np.result_type(result.dtype, np.float64) if result.dtype.kind in 'biufc' else object
            result = result.astype(dtype)
            result[outside] = np.nan
    return result


def _from_mapping(source):
    """Interpret conventional static (K,) and time-dependent (N,K) bins."""
    if 'x' not in source or 'y' not in source:
        raise ValueError("A source dictionary must contain x and y.")
    times = _times(source['x'])
    values = np.asarray(source['y'])
    if values.ndim == 0:
        values = values.reshape(1)
    dims = ['time'] + [f'v{i}_dim' for i in range(1, values.ndim)]
    coords = {'time': ('time', times)}
    for key, value in source.items():
        if not re.fullmatch(r'v(?:[1-9][0-9]*)?', key) or value is None:
            continue
        axis = 1 if key == 'v' else int(key[1:])
        if axis >= values.ndim:
            raise ValueError(f"{key} does not correspond to a data dimension.")
        coord = np.asarray(value)
        if coord.shape == (values.shape[axis],):
            coord_dims = (dims[axis],)
        elif coord.shape == (len(times), values.shape[axis]):
            coord_dims = ('time', dims[axis])
        else:
            raise ValueError(f"{key} must have shape (K,) or (N, K).")
        coords[key] = (coord_dims, coord)
    return xr.DataArray(values, dims=dims, coords=coords,
                        attrs=deepcopy(source.get('metadata', {})))


def _interpolate(source, target, bounds, ignore_nans, method):
    if not isinstance(source, xr.DataArray) or not source.dims or source.dims[0] != 'time':
        raise ValueError("Source must be a time series with time as its first dimension.")
    times = _times(source.coords['time'].values).view('i8')
    if not len(times):
        raise ValueError("Source time series must not be empty.")
    descending = False
    if len(times) > 1:
        if np.all(times[1:] < times[:-1]):
            source = source.isel(time=slice(None, None, -1))
            times = times[::-1]
            descending = True
        elif not np.all(times[1:] > times[:-1]):
            raise ValueError("Source times must be strictly increasing or decreasing (no duplicates).")
    ticks = target.view('i8')
    if bounds == 'trim':
        target = target[(ticks >= times[0]) & (ticks <= times[-1])]
        ticks = target.view('i8')
    values = _interpolate_values(source.values, times, ticks, ignore_nans, bounds, method)
    coords = {'time': xr.Variable('time', target, attrs=deepcopy(source.time.attrs))}
    for name, coord in source.coords.items():
        if name == 'time':
            continue
        if 'time' in coord.dims:
            axis = coord.dims.index('time')
            data = np.moveaxis(coord.values, axis, 0)
            if name in ('v', 'v1', 'v2', 'v3', 'spec_bins'):
                data = _previous_bins(data, times, ticks, bounds)
            else:
                data = _interpolate_values(data, times, ticks, ignore_nans, bounds, method)
            data = np.moveaxis(data, 0, axis)
            coords[name] = xr.Variable(coord.dims, data, attrs=deepcopy(coord.attrs))
        else:
            coords[name] = coord.copy(deep=True)
    attrs = deepcopy(source.attrs)
    plot = attrs.get('plot_options')
    if plot is not None:
        plot['trange'] = ([float(ticks.min()) / 1e9, float(ticks.max()) / 1e9]
                          if len(ticks) else [])
        # Error bars are stored as a time-dependent array outside xarray coords.
        if plot.get('error') is not None:
            error = np.asarray(plot['error'])
            if descending:
                error = error[::-1]
            plot['error'] = _interpolate_values(error, times, ticks, ignore_nans, bounds, method)
    return xr.DataArray(values, dims=source.dims, coords=coords, attrs=attrs)


def _as_dict(result):
    data = {'x': result.time.values.copy(), 'y': result.values.copy()}
    for name, coord in result.coords.items():
        if re.fullmatch(r'v(?:[1-9][0-9]*)?', name):
            data[name] = coord.values.copy()
    if 'spec_bins' in result.coords and not any(k.startswith('v') for k in data):
        data['v'] = result.coords['spec_bins'].values.copy()
    if result.attrs:
        data['metadata'] = deepcopy(result.attrs)
    return data


def time_interpolate(source, target, *, method='linear', newname=None,
                 suffix=None, overwrite=False, return_data=False,
                 no_extrapolate=False, nan_extrapolate=False,
                 repeat_extrapolate=False, ignore_nans=False):
    """Interpolate a time series, independently for every component.

    Parameters
    ----------
    source : str, list of str, or dict
        Tplot names/wildcards, or a dictionary with ``x`` times and ``y`` values.
        The first data dimension is time; any number of trailing dimensions is
        supported. Dictionaries may include static ``v``, ``v1``, ``v2``, ``v3``
        arrays of shape (K,), time-dependent bins of shape (N, K), and metadata.
    target : str or array_like
        One tplot name (only its times are used), or a one-dimensional time
        array. Numeric times are Unix seconds; strings and datetime values are
        also accepted. Times are normalized to datetime64[ns]. Target ordering
        and duplicates are preserved.
    method : str, optional
        'linear' (default), 'quadratic', 'spline', 'nearest', or 'previous'.
        Quadratic uses IDL's local three-point polynomial. Spline uses a natural
        cubic spline over each local four-point neighborhood, not a global fit.
        Nearest selects the earlier sample at midpoint ties. Previous selects
        the latest sample at or before the target (exact matches included).
    newname : str or list of str, optional
        Output names, one per expanded source. Cannot be combined with suffix
        or overwrite. A dictionary source requires one name to create output.
    suffix : str, optional
        Output suffix; defaults to '_interp' for tplot sources.
    overwrite : bool, optional
        Replace source tplot variables. Default False.
    return_data : bool, optional
        Return one dictionary containing x, y, dependencies and metadata without
        storing a variable. Requires exactly one source and no naming options.
        A dictionary source with no newname also returns data automatically.
    no_extrapolate : bool, optional
        Trim target times to source coverage, independently for each source.
        Empty results are returned as arrays, or skipped when storing variables.
    nan_extrapolate : bool, optional
        Keep target times but fill values outside source coverage with NaNs.
    repeat_extrapolate : bool, optional
        Repeat each component's first/last finite value outside source coverage.
        Only one boundary option may be enabled. With none enabled, extend
        the selected interpolant outside coverage: linear uses two endpoint
        samples, quadratic/spline use their endpoint neighborhoods, and
        nearest/previous repeat endpoint values.
    ignore_nans : bool, optional
        Remove NaNs per Y component before interpolation. Bin-map NaNs are
        retained regardless of this option. Default False: NaNs propagate through
        the selected interpolation neighborhood (nearest/previous copy only the
        selected sample). Exact source samples are copied for every method.
        Boundary options refer to the ORIGINAL source time coverage, as in IDL;
        ignoring NaNs can extrapolate inside that coverage beyond valid samples.

    Returns
    -------
    list of str or dict
        Names stored, or returned data with datetime64[ns] times. Existing valid
        samples are copied exactly (subject to output dtype conversion). Numeric
        Y outputs are promoted to at least float64; complex data remain complex.

    Notes
    -----
    Source times must be strictly monotonic; descending data are reversed.
    Duplicate times, empty sources, incompatible shapes and conflicting options
    raise exceptions. All-NaN components stay NaN. A singleton component is
    extended as a constant, then the selected boundary policy is applied.
    Quadratic requires three samples and spline requires four, counted after
    NaN removal when ignore_nans=True. With fewer samples, use linear; with
    one sample, use a constant; with none, return NaNs. Without NaN removal,
    a missing neighborhood value produces NaN rather than triggering fallback.
    No gap-duration restriction is imposed. Unlike IDL's
    arithmetic at some interval boundaries, an exact valid source sample remains
    valid even when its neighbor is NaN. Matrix elements are interpolated
    independently; rotation-matrix orthogonality is not enforced.

    Time-dependent v/v1/v2/v3 bins (including the spec_bins alias) use the map at
    the latest source time less than or equal to each target time. Exact source
    times select the new map. Static bins are copied. Outside source coverage,
    default extrapolation and repeat_extrapolate retain the endpoint maps,
    including their NaNs; nan_extrapolate fills with NaNs, and no_extrapolate
    trims the grid. Unlike IDL, bin maps are never linearly interpolated.
    Y uses the selected method across bin changes, without rebinning.
    Unlike IDL tinterpol_mxn's nearest-neighbor branch, ignore_nans applies to
    nearest as well as the other methods. Descending sources are normalized to
    increasing time, so nearest ties always choose the earlier time.


    Examples
    --------
    >>> import pyspedas
    >>> result = pyspedas.time_interpolate({'x': [0, 2], 'y': [0, 4]}, [0, 1, 2])
    >>> result['y']
    array([0., 2., 4.])
    """
    from pyspedas.tplot_tools import data_quants, tnames, store_data, get_y_range

    if method not in ('linear', 'quadratic', 'spline', 'nearest', 'previous'):
        raise ValueError("method must be 'linear', 'quadratic', 'spline', 'nearest', or 'previous'.")
    if sum(bool(v) for v in (no_extrapolate, nan_extrapolate, repeat_extrapolate)) > 1:
        raise ValueError("Specify only one extrapolation option.")
    if sum((newname is not None, suffix is not None, bool(overwrite))) > 1:
        raise ValueError("Specify only one of newname, suffix, or overwrite.")
    if return_data and (newname is not None or suffix is not None or overwrite):
        raise ValueError("return_data cannot be combined with output naming options.")
    bounds = ('trim' if no_extrapolate else 'nan' if nan_extrapolate else
              'repeat' if repeat_extrapolate else 'extrapolate')
    mapping = isinstance(source, Mapping)
    if mapping:
        if suffix is not None or overwrite:
            raise ValueError("A dictionary source requires newname for stored output.")
        sources = [_from_mapping(source)]
        names = []
        return_data = return_data or newname is None
    else:
        if not isinstance(source, (str, list, tuple)):
            raise TypeError("source must contain tplot names or be a data dictionary.")
        names = list(dict.fromkeys(tnames(list(source) if isinstance(source, tuple) else source)))
        if not names:
            raise ValueError("No source tplot variables matched.")
        if any(not isinstance(data_quants[name], xr.DataArray) for name in names):
            raise ValueError("Sources must be time-dependent tplot variables.")
        sources = [data_quants[name].copy(deep=True) for name in names]
    if return_data and len(sources) != 1:
        raise ValueError("return_data requires exactly one source.")
    if isinstance(target, str):
        if target not in data_quants or not isinstance(data_quants[target], xr.DataArray):
            raise ValueError("Target must name a time-dependent tplot variable.")
        target = data_quants[target].coords['time'].values
    target = _times(target)
    if newname is not None:
        output_names = [newname] if isinstance(newname, str) else list(newname)
    else:
        output_names = names if overwrite else [n + ('_interp' if suffix is None else suffix) for n in names]
    if not return_data:
        if len(output_names) != len(sources) or any(not isinstance(n, str) or not n for n in output_names):
            raise ValueError("Provide one non-empty output name per source.")
        if len(set(output_names)) != len(output_names):
            raise ValueError("Output names must be distinct.")
    # Compute every result before changing the registry, including overwrite mode.
    results = [_interpolate(s, target, bounds, ignore_nans, method) for s in sources]
    if return_data:
        return _as_dict(results[0])
    stored = []
    for name, result in zip(output_names, results):
        if not result.sizes['time']:
            logging.info("time_interpolate: empty result for %s; skipping storage", name)
            continue
        if 'plot_options' not in result.attrs:
            data = _as_dict(result)
            data.pop('metadata', None)
            for axis in range(1, result.ndim):
                if axis == 1 and 'v' in data:
                    continue
                key = 'v' if result.ndim == 2 else f'v{axis}'
                if key not in data and f'v{axis}' not in data:
                    data[key] = np.arange(result.shape[axis])
            if not store_data(name, data=data, attr_dict=deepcopy(result.attrs)):
                raise ValueError(f"Could not store {name}.")
        else:
            result.name = name
            result.attrs['plot_options']['yaxis_opt']['y_range'] = get_y_range(result)
            data_quants[name] = result
        stored.append(name)
    return stored
