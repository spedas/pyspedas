"""Interpolate orthogonal coordinate transformations using quaternion SLERP."""

from collections.abc import Mapping
from copy import deepcopy
import math
from numbers import Integral, Real

import numpy as np
import xarray as xr

from pyspedas.cotrans_tools.matrix_array_lib import ctv_swap_hands
from pyspedas.cotrans_tools.quaternions import mtoq, qslerp, qtom
from pyspedas.utilities.time_interpolate import _gap_mask, _interval, _times


def _prepare(values):
    """Validate whole rotations and convert usable samples to unit quaternions."""
    values = np.asarray(values)
    if values.dtype.kind not in 'biuf':
        raise TypeError('Rotations must be real numeric arrays.')
    if values.ndim == 3 and values.shape[1:] == (3, 3):
        representation = 'matrix'
    elif values.ndim == 2 and values.shape[1:] == (4,):
        representation = 'quaternion'
    else:
        raise ValueError('Rotation values must have shape (N, 3, 3) or (N, 4).')
    values = values.astype(np.float64, copy=True)
    if np.isinf(values).any():
        raise ValueError('Rotations must not contain infinity.')
    missing = np.isnan(values).reshape(len(values), -1).any(axis=1)
    good = ~missing
    quaternions = np.full((len(values), 4), np.nan)
    left = False
    if good.any():
        usable = values[good]
        if representation == 'matrix':
            determinants = np.linalg.det(usable)
            if (not np.allclose(usable @ usable.transpose(0, 2, 1), np.eye(3), rtol=0, atol=1e-5)
                    or not np.allclose(np.abs(determinants), 1, rtol=0, atol=1e-5)):
                raise ValueError('Matrices must be orthogonal with determinant +1 or -1 (tolerance 1e-5).')
            if np.any(determinants < 0) and np.any(determinants > 0):
                raise ValueError('Matrix series must have consistent handedness.')
            left = bool(determinants[0] < 0)
            usable = mtoq(ctv_swap_hands(usable) if left else usable)
        norms = np.linalg.norm(usable, axis=1)
        if not np.allclose(norms, 1, rtol=0, atol=1e-5):
            raise ValueError('Quaternions must have unit norm (tolerance 1e-5).')
        usable = usable / norms[:, None]
        # Equivalent q/-q representations must not introduce sign jumps.
        flips = np.ones(len(usable))
        flips[1:] = np.where(np.sum(usable[:-1] * usable[1:], axis=1) < 0, -1, 1)
        usable *= np.cumprod(flips)[:, None]
        quaternions[good] = usable
    return values, representation, quaternions, missing, left


def _resample(times, values, target, output, bounds, ignore_nans, max_gap_time, max_gap_samples):
    if not len(times):
        raise ValueError('Source time series must not be empty.')
    if len(values) != len(times):
        raise ValueError('The first data dimension must match the source times.')
    ticks = times.view('i8')
    if len(ticks) > 1:
        if np.all(ticks[1:] < ticks[:-1]):
            ticks, values = ticks[::-1], values[::-1]
        elif not np.all(ticks[1:] > ticks[:-1]):
            raise ValueError('Source times must be strictly increasing or decreasing (no duplicates).')
    original, representation, quaternions, missing, left = _prepare(values)
    output = representation if output == 'same' else output
    if left and output == 'quaternion':
        raise ValueError('A quaternion cannot represent a left-handed transformation.')
    query = target.view('i8')
    outside = (query < ticks[0]) | (query > ticks[-1])
    if bounds == 'raise' and outside.any():
        raise ValueError('Target times lie outside source coverage.')
    if bounds == 'trim':
        target, query = target[~outside], query[~outside]
        outside = np.zeros(len(query), dtype=bool)
    keep = ~missing if ignore_nans else np.ones(len(ticks), dtype=bool)
    x, q = ticks[keep], quaternions[keep]
    result = np.full((len(query), 4), np.nan)
    if len(x) == 1:
        result[:] = q[0]
    elif len(x) > 1:
        right = np.searchsorted(x, query, side='left')
        clipped = np.minimum(right, len(x) - 1)
        exact = (right < len(x)) & (x[clipped] == query)
        result[exact] = q[right[exact]]
        result[query < x[0]] = q[0]
        result[query > x[-1]] = q[-1]
        interpolate = np.flatnonzero(~exact & (right > 0) & (right < len(x)))
        # Group by bracketing pair, preserving arbitrary target order and duplicates.
        order = interpolate[np.argsort(right[interpolate], kind='stable')]
        if len(order):
            groups = np.split(order, np.flatnonzero(np.diff(right[order])) + 1)
            for indices in groups:
                hi = right[indices[0]]
                pair = q[hi - 1:hi + 1]
                if np.isnan(pair).any():
                    continue
                fraction = _interval(query[indices], x[hi - 1]) / _interval(x[hi], x[hi - 1])
                sorted_indices = np.argsort(fraction, kind='stable')
                interpolated = qslerp(pair, np.array([0., 1.]), fraction[sorted_indices])
                if interpolated is None or np.shape(interpolated) != (len(indices), 4):
                    raise ValueError('Quaternion interpolation failed.')
                result[indices[sorted_indices]] = interpolated
    good = np.isfinite(result).all(axis=1)
    result[good] /= np.linalg.norm(result[good], axis=1)[:, None]
    if output == 'matrix':
        matrices = np.full((len(query), 3, 3), np.nan)
        if good.any():
            matrices[good] = qtom(result[good])
            if left:
                matrices[good] = ctv_swap_hands(matrices[good])
        result = matrices
        if representation == 'matrix':
            # tvector_rotate uses matrices directly on matching grids and for
            # singleton inputs. Preserve exact matrix samples and held endpoints.
            original_keep = original[keep]
            if len(x):
                nearest = np.clip(np.searchsorted(x, query), 0, len(x) - 1)
                direct = (query == x[nearest]) | (query < x[0]) | (query > x[-1])
                valid_direct = direct & ~np.isnan(original_keep[nearest]).any(axis=(1, 2))
                result[valid_direct] = original_keep[nearest[valid_direct]]
    sample_values = np.where(missing, np.nan, 1.)
    rejected = _gap_mask(sample_values, ticks, query, max_gap_time, max_gap_samples)
    result[rejected] = np.nan
    if bounds == 'nan':
        result[outside] = np.nan
    return target, result


def interpolate_rotation(source, target, *, output='same', newname=None,
                         suffix=None, overwrite=False, return_data=False,
                         bounds='repeat', ignore_nans=False,
                         max_gap_time=None, max_gap_samples=None):
    """Interpolate matrices or quaternions using shortest-path quaternion SLERP.

    Parameters
    ----------
    source : str, list of str, or dict
        Tplot names/wildcards, or a dictionary with ``x`` times and ``y`` values.
        Values have shape (N, 3, 3) for orthogonal transformation matrices or
        (N, 4) for scalar-first [w, x, y, z] PySPEDAS quaternions.
        A single rotation uses N=1. Optional ``metadata`` is copied.
    target : str or array_like
        Tplot name whose times are used, or timestamps. Numeric times are Unix
        seconds; strings and datetimes are accepted. Order and duplicates remain.
    output : {'same', 'matrix', 'quaternion'}, optional
        Output representation, default 'same'. Left-handed matrices cannot be
        returned as quaternions because a quaternion cannot encode a reflection.
    newname : str or list of str, optional
        One output name per source. A dictionary requires newname for storage.
    suffix : str, optional
        Output suffix, default '_rot_interp'.
    overwrite : bool, optional
        Replace source tplot variables. Mutually exclusive with newname/suffix.
    return_data : bool, optional
        Return a dictionary for one source without storing a variable. A source
        dictionary without newname also returns data. Cannot combine with naming.
    bounds : {'repeat', 'nan', 'trim', 'raise'}, optional
        Outside original source coverage, hold endpoints (default, matching
        tvector_rotate), fill NaNs, discard targets, or raise ValueError.
        No angular-velocity extrapolation is performed.
    ignore_nans : bool, optional
        Skip whole missing rotations. Default False: a NaN anywhere in a sample
        makes it missing, and intervals needing that sample remain entirely NaN.
        With True, endpoint holding extends the first/last usable rotation even
        inside leading/trailing missing runs. Bounds use original coverage.
    max_gap_time : float, optional
        Maximum seconds between usable rotations. Targets strictly inside longer
        intervals become NaN, including outages without explicit missing values.
        Finite and non-negative; None is unlimited. Equality is allowed.
    max_gap_samples : int, optional
        Maximum missing source rotations between usable rotations. Reject the
        entire gap if exceeded. Positive integer; None is unlimited. Both limits
        apply together, preserving exact usable samples. Unbounded missing runs
        and singletons retain the endpoint policy. Limits do not enable NaN removal.

    Returns
    -------
    list of str or dict
        Names stored, or x/y/metadata with datetime64[ns] times and float64 values.
        Empty trimmed results are returned as arrays or skipped during storage.

    Notes
    -----
    Matches tvector_rotate's conversion convention: left-handed matrices have
    their first row negated before mtoq/qslerp/qtom, then negated again afterward.
    Usable matrices must have a consistent determinant sign and be orthogonal
    with determinant +/-1 within absolute tolerance 1e-5. Mixed handedness,
    nonfinite infinities, invalid shapes and invalid rotations raise exceptions.
    Quaternions within 1e-5 of unit norm are normalized; others are rejected.
    Quaternion signs may change for continuity without changing the rotation.
    At exactly 180 degrees between orientations the shortest path is ambiguous;
    the PySPEDAS quaternion convention determines the selected path.

    Source times must be strictly monotonic, without duplicates; descending
    sources are reversed. Matching matrix samples and held matrix endpoints are
    copied exactly. A singleton orientation is held constant. Matrix input/output
    coordinate-system and other scientific metadata is retained. Plot options
    are rebuilt; representation-specific bin axes and error bars are not carried
    over to the new rotation variable.

    Examples
    --------
    >>> import pyspedas
    >>> data = pyspedas.interpolate_rotation(
    ...     {'x': [0, 2], 'y': [[1, 0, 0, 0], [0, 0, 0, 1]]},
    ...     [1], output='matrix')
    """
    from pyspedas.tplot_tools import data_quants, store_data, tnames

    if output not in ('same', 'matrix', 'quaternion'):
        raise ValueError("output must be 'same', 'matrix', or 'quaternion'.")
    if bounds not in ('repeat', 'nan', 'trim', 'raise'):
        raise ValueError("bounds must be 'repeat', 'nan', 'trim', or 'raise'.")
    if max_gap_time is not None and (
            not isinstance(max_gap_time, Real) or isinstance(max_gap_time, bool)
            or not math.isfinite(max_gap_time) or max_gap_time < 0):
        raise ValueError('max_gap_time must be finite and non-negative.')
    if max_gap_samples is not None and (
            not isinstance(max_gap_samples, Integral) or isinstance(max_gap_samples, bool)
            or max_gap_samples <= 0):
        raise ValueError('max_gap_samples must be a positive integer.')
    if sum((newname is not None, suffix is not None, bool(overwrite))) > 1:
        raise ValueError('Specify only one of newname, suffix, or overwrite.')
    if return_data and (newname is not None or suffix is not None or overwrite):
        raise ValueError('return_data cannot be combined with output naming options.')
    if isinstance(source, Mapping):
        if suffix is not None or overwrite:
            raise ValueError('A dictionary source requires newname for stored output.')
        sources = [deepcopy(source)]
        names = []
        return_data = return_data or newname is None
    else:
        if not isinstance(source, (str, list, tuple)):
            raise TypeError('source must be tplot names or a data dictionary.')
        names = list(dict.fromkeys(tnames(list(source) if isinstance(source, tuple) else source)))
        if not names:
            raise ValueError('No source tplot variables matched.')
        sources = []
        for name in names:
            array = data_quants[name]
            if not isinstance(array, xr.DataArray) or not array.dims or array.dims[0] != 'time':
                raise ValueError('Sources must be time-dependent tplot variables.')
            sources.append({'x': array.time.values.copy(), 'y': array.values.copy(),
                            'metadata': deepcopy(array.attrs)})
    if return_data and len(sources) != 1:
        raise ValueError('return_data requires exactly one source.')
    if isinstance(target, str):
        array = data_quants.get(target)
        if not isinstance(array, xr.DataArray) or 'time' not in array.coords:
            raise ValueError('Target must name a time-dependent tplot variable.')
        target = array.time.values.copy()
    target = _times(target)
    if newname is not None:
        output_names = [newname] if isinstance(newname, str) else list(newname)
    else:
        output_names = names if overwrite else [n + ('_rot_interp' if suffix is None else suffix) for n in names]
    if not return_data and (len(output_names) != len(sources)
                           or any(not isinstance(n, str) or not n for n in output_names)
                           or len(set(output_names)) != len(output_names)):
        raise ValueError('Provide one distinct non-empty output name per source.')
    results = []
    for item in sources:
        if 'x' not in item or 'y' not in item:
            raise ValueError('Source dictionaries require x and y.')
        times = _times(item['x'])
        values = np.asarray(item['y'])
        if values.ndim == 0:
            raise ValueError('Rotation values must include the sample dimension.')
        x, y = _resample(times, values, target, output, bounds, ignore_nans,
                         max_gap_time, max_gap_samples)
        result = {'x': x.copy(), 'y': y}
        if 'metadata' in item:
            metadata = deepcopy(item['metadata'])
            # Plot settings describe the old representation and time grid.
            # Recreate them on storage, retaining scientific metadata separately.
            metadata.pop('plot_options', None)
            result['metadata'] = metadata
        results.append(result)
    if return_data:
        return results[0]
    stored = []
    for name, result in zip(output_names, results):
        if not len(result['x']):
            continue
        data = {'x': result['x'], 'y': result['y']}
        if result['y'].ndim == 3:
            data.update(v1=np.arange(3), v2=np.arange(3))
        if not store_data(name, data=data, attr_dict=result.get('metadata', {})):
            raise ValueError(f'Could not store {name}.')
        stored.append(name)
    return stored
