Interpolation
=============

There are several routines for performing interpolation in PySPEDAS, each designed
for slightly different use cases.

pyspedas.time_interpolate() interpolates along time independently for each component
of a scalar, vector, matrix, or higher-dimensional series. It accepts tplot names
(including lists and wildcards) or dictionaries containing ``x`` and ``y``.
Select the interpolation with ``method`` (default ``'linear'``):

* ``'linear'``: interpolate between adjacent samples.
* ``'quadratic'``: fit a polynomial through the local three-point neighborhood,
  matching IDL ``INTERPOL, /QUADRATIC``.
* ``'spline'``: fit a natural cubic spline over each local four-point neighborhood,
  matching IDL ``INTERPOL, /SPLINE``. This is not a single global spline fit.
* ``'nearest'``: copy the closest sample, choosing the earlier time at midpoint ties.
* ``'previous'``: copy the latest sample at or before the target time. At an exact
  source time, select that sample.

Quadratic requires three samples and spline requires four. With fewer samples,
these methods fall back to linear interpolation; a single sample is repeated,
and a component with no remaining samples produces NaNs. Counts are per
component after NaN removal when ``ignore_nans=True``. Without NaN removal,
missing values propagate through the local neighborhood; they do not trigger
fallback. Exact source samples are copied for all methods.
Existing interpolation routines remain unchanged.

Like IDL SPEDAS, the default is to extrapolate using the selected method.
Quadratic and spline extend their endpoint neighborhoods; nearest and previous
repeat endpoint values. Use ``nan_extrapolate=True`` to
keep the target grid and fill outside source coverage with NaNs,
``no_extrapolate=True`` to trim it, or ``repeat_extrapolate=True`` to repeat
first/last finite values per component. These options are mutually exclusive.
``ignore_nans=True`` removes NaNs independently for each component; this may
extrapolate beyond that component's valid samples even inside the original
source time coverage.

.. rubric:: Gap limits

``max_gap_time`` limits the elapsed seconds between the non-NaN samples
surrounding each target time, independently for each component. Targets strictly
inside longer intervals become NaN, including acquisition outages with no
recorded NaNs. Gaps exactly equal to the limit are allowed. The value must be
finite and non-negative; zero permits only exact samples within the usable
source span.

``max_gap_samples`` limits the number of consecutive NaNs between surrounding
non-NaN source samples. It must be a positive integer. If a gap contains more
missing samples, its entire interior is rejected. Unlike ``interp_nan``, it does
not partially fill longer runs. This count uses the source grid, so changing the
number or order of target times does not change which gaps qualify.

Both options default to ``None`` (unlimited). When both are supplied, exceeding
either limit rejects the gap. Use ``ignore_nans=True`` to interpolate through
missing values; the limits alone do not enable NaN removal.

Exact non-NaN source samples are preserved. Rejected targets remain in the
output with NaN values, rather than being removed. Gap limits apply only between
non-NaN samples: extrapolation beyond those samples, including leading/trailing
NaN runs and singleton components, retains the existing behavior and boundary
options. The limits mask results without changing quadratic/spline fitting
neighborhoods; an allowed result may still use samples across a neighboring
rejected gap. Numeric time-dependent auxiliary coordinates and error bars also
respect the limits independently. Time-dependent bin maps remain repeat-previous.

For example::

    import numpy as np
    import pyspedas

    source = {'x': [0, 1, 2, 3, 4, 5, 6],
              'y': [0, np.nan, np.nan, 3, 4, np.nan, 6]}
    result = pyspedas.time_interpolate(
        source, source['x'], ignore_nans=True,
        max_gap_samples=1, max_gap_time=3)
    # result['y'] is [0, NaN, NaN, 3, 4, 5, 6].
    # The two-sample gap is rejected in full; the one-sample gap is filled.

.. rubric:: Examples

For example::

    import numpy as np
    import pyspedas

    # Three matrix-valued samples; interpolate each matrix element in time.
    matrices = np.arange(27).reshape(3, 3, 3)
    result = pyspedas.time_interpolate(
        {'x': [0, 2, 4], 'y': matrices}, [1, 3])
    assert result['y'].shape == (2, 3, 3)

    pyspedas.store_data('input', data={'x': [0, 2], 'y': [0, 4]})
    names = pyspedas.time_interpolate(
        'input', [-1, 1, 3], nan_extrapolate=True)
    # Creates input_interp with values [NaN, 2, NaN].
    data = pyspedas.time_interpolate('input', [1], return_data=True)
    # Returns a dictionary without creating a tplot variable.

    data = pyspedas.time_interpolate('input', [0.5, 1.5], method='previous',
                                    return_data=True)
    # Both target times use the sample at time 0.

Returned dictionary times use ``datetime64[ns]``. Static dependency coordinates
are copied. Time-dependent ``v``, ``v1``, ``v2``, and ``v3`` bins (including the
``spec_bins`` alias) repeat the bin map at the latest source time at or before
each target time. Exact transition times select the new map. Bin-map NaNs are
retained even with ``ignore_nans=True``. Outside coverage, default extrapolation
and repeat extrapolation retain endpoint maps; NaN extrapolation fills with NaNs
and no extrapolation trims the grid. Y values use the selected interpolation method across
bin changes, without rebinning or suppressing interpolation at mode transitions.
Tplot output preserves coordinate attributes, data metadata and plot options, while updating
time and value ranges. Matrix interpolation is component-wise and does not
preserve special constraints such as rotation-matrix orthogonality.

Intentional differences from IDL include preserving exact valid samples next to
NaNs, trimming each source independently in a batch, consistently applying
repeat filling to tensors, and using previous bin maps instead of interpolating
them linearly. Python also honors ``ignore_nans=True`` for nearest-neighbor
interpolation, whereas the IDL wrapper bypasses NaN filtering for that method.
The insufficient-sample fallback avoids IDL failures for undersized quadratic
and spline neighborhoods. Invalid options and inputs raise Python exceptions. Stored results return a list of names; empty trimmed
results are skipped, while returned-data mode returns empty arrays.

.. autofunction:: pyspedas.time_interpolate

``pyspedas.tinterpol_mxn()`` is an IDL SPEDAS compatibility wrapper around
``time_interpolate``, with identical arguments, defaults and return values.
Use ``time_interpolate`` in new Python code.

.. autofunction:: pyspedas.tinterpol_mxn

.. rubric:: Rotation matrices and quaternions

Use ``pyspedas.interpolate_rotation`` for orthogonal coordinate-transformation
matrices or unit quaternions. Component-wise ``time_interpolate`` does not
preserve matrix orthogonality; quaternion spherical linear interpolation (SLERP)
follows the shortest rotation path between samples.

The routine accepts the same source/target conventions as ``time_interpolate``:
tplot names (including lists and wildcards), or a source dictionary containing
``x`` and ``y``. Matrix values have shape ``(N, 3, 3)`` and quaternion values have
shape ``(N, 4)`` with scalar-first components ``[w, x, y, z]``. Output defaults to
the input representation; use ``output='matrix'`` or ``output='quaternion'`` to
convert. It uses the existing PySPEDAS quaternion convention, matching
``tvector_rotate``.

Both consistently right-handed and consistently left-handed orthogonal matrices
are supported. Following ``tvector_rotate``, left-handed matrices have their
first row negated before quaternion interpolation, then restored afterward.
Mixed-handed series are rejected. Left-handed transformations cannot be returned
as quaternions because a quaternion alone cannot encode a reflection.

``bounds='repeat'`` holds endpoint orientations, matching ``tvector_rotate``.
Other choices are ``'nan'``, ``'trim'``, and ``'raise'``. A singleton matrix is
applied unchanged, and exact matrix samples are preserved. Quaternions may be
normalized or have signs changed without changing their orientation. Matrices
must be orthogonal with determinant +/-1 within absolute tolerance ``1e-5``;
quaternion norms must be within ``1e-5`` of one. Infinity and materially invalid
rotations raise exceptions.

A NaN anywhere in a rotation marks the entire sample as missing. Set
``ignore_nans=True`` to skip such samples. ``max_gap_time`` and
``max_gap_samples`` have the same whole-gap semantics as ``time_interpolate``,
but count missing rotations rather than components. Coordinate-system and other
scientific metadata are copied; plot options are rebuilt for the output
representation. The default suffix is ``'_rot_interp'``.

For example::

    # Transform matrices to the times of a measurement variable.
    pyspedas.interpolate_rotation(
        'attitude_matrix', 'measurements', newname='attitude_at_measurements')

    # Return matrices from a quaternion series, without storing a tplot variable.
    result = pyspedas.interpolate_rotation(
        {'x': [0, 2], 'y': [[1, 0, 0, 0], [0, 0, 0, 1]]},
        [0.5, 1, 1.5], output='matrix', bounds='nan')

.. autofunction:: pyspedas.interpolate_rotation

pyspedas.interpol() operates directly on arrays, not tplot variables. It is a wrapper around scipy.interpolate.interp1d().

.. autofunction:: pyspedas.interpol

pyspedas.tinterpol() operates on tplot variables, and uses the xarray interp() method (which itself uses scipy.interp1d) internally.  It can take a list of
tplot variables and perform the interpolation on all of them.

.. autofunction:: pyspedas.tinterpol

pyspedas.interp_nan() operates on single tplot variables, and uses the xarray interpolate_na() method to perform
interpolation through NaN values. Use ``max_gap_time`` to limit the duration of
filled gaps in seconds, or ``max_gap_samples`` to limit the number of consecutive
NaNs filled. Both limits can be used together. The deprecated ``s_limit`` argument
now follows its documented meaning in seconds and is an alias for ``max_gap_time``;
use ``max_gap_samples`` to retain the previous sample-count behavior.

.. autofunction:: pyspedas.interp_nan

pyspedas.tinterp() operates on single tplot variables, using the xarray interp_like() method internally.

.. autofunction:: pyspedas.tinterp
