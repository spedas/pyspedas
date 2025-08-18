"""
Python implementation of IDL SPEDAS wav_data.pro.

Uses wavelet2.py which is a wrapper for wavelet98.py.
"""

import numpy as np
import logging
from pyspedas.analysis.wavelet2 import wavelet2
from pyspedas.analysis.reduce_tres import reduce_tres
from pyspedas.analysis.roundsig import roundsig
from scipy.ndimage import uniform_filter1d
from pyspedas import get_data, store_data, options, tnames


def smooth_wavelet(wv, wid, gaussian=False):
    """
    Smooth a 3D wavelet array along the first axis using a Gaussian or boxcar kernel.

    Implementation of IDL smooth_wavelet procedure to match the exact behavior.

    Parameters
    ----------
    wv : ndarray
        Input 3D array of shape (nt, nj, nk), to be smoothed along axis 0.
        Modified in-place to match IDL behavior.
    wid : array_like
        1D array specifying smoothing width for each scale (length nj).
    gaussian : bool, optional
        If True, use a Gaussian kernel. Otherwise, use IDL's smooth function equivalent.

    Notes
    -----
    This function modifies wv in-place to match IDL behavior.
    """
    dim = list(wv.shape) + [1, 1]  # Pad dimensions
    nk = dim[2] if len(dim) > 2 else 1
    nj = dim[1] if len(dim) > 1 else 1
    nt = dim[0]

    wid = np.asarray(wid)

    if gaussian:
        # Calculate widi array for Gaussian case
        widi = np.round(wid / 2).astype(int) * 2 + 1
        # IDL behavior: width <= 1 means no smoothing
        widi = np.clip(widi, 1, nt - 1)

        for k in range(nk):
            for j in range(nj):
                if widi[j] > 1:  # Only smooth if width > 1
                    # Create Gaussian kernel using dgen equivalent
                    kernel_size = widi[j]
                    x = np.linspace(-2, 2, kernel_size)
                    kernel = np.exp(-(x**2))
                    kernel = kernel / np.sum(kernel)

                    # Apply convolution with edge truncation
                    signal = (
                        wv[:, j, k]
                        if wv.ndim >= 3
                        else wv[:, j] if wv.ndim >= 2 else wv[:]
                    )
                    # Use numpy.convolve with 'same' mode and handle edges
                    convolved = np.convolve(signal, kernel, mode="same")

                    if wv.ndim >= 3:
                        wv[:, j, k] = convolved
                    elif wv.ndim >= 2:
                        wv[:, j] = convolved
                    else:
                        wv[:] = convolved
                # If widi[j] <= 1, leave the data unchanged (IDL behavior)
        return

    # Non-Gaussian case: recalculate widi to match IDL behavior
    widi = np.round(wid).astype(int)
    # IDL smooth() with width <= 1 returns original data unchanged
    widi = np.clip(widi, 1, nt - 1)

    for k in range(nk):
        for j in range(nj):
            if widi[j] > 1:  # Only smooth if width > 1
                # Use scipy's uniform_filter1d to match IDL's smooth function

                signal = (
                    wv[:, j, k] if wv.ndim >= 3 else wv[:, j] if wv.ndim >= 2 else wv[:]
                )

                # Apply uniform filter with size widi[j], handling NaNs and edge truncation
                smoothed = uniform_filter1d(
                    signal.astype(float),
                    size=min(widi[j], nt - 1),
                    mode="nearest",  # Equivalent to IDL's /edge_truncate
                )

                if wv.ndim >= 3:
                    wv[:, j, k] = smoothed
                elif wv.ndim >= 2:
                    wv[:, j] = smoothed
                else:
                    wv[:] = smoothed
            # If widi[j] <= 1, leave the data unchanged (IDL behavior)


def cross_corr_wavelet(wa, wb, wid, gaussian=False):
    """
    Cross-correlation wavelet analysis.

    Implementation of IDL cross_corr_wavelet procedure.

    Parameters
    ----------
    wa : ndarray
        First wavelet array (complex)
    wb : ndarray
        Second wavelet array (complex)
    wid : array_like
        Smoothing width array
    gaussian : bool, optional
        Use Gaussian smoothing (default=False)

    Returns
    -------
    gam : ndarray
        Coherence array
    coinc : ndarray
        Coincidence (real part) array
    quad : ndarray
        Quadrature (imaginary part) array
    crat : ndarray
        Coincidence ratio array
    """
    # Cross-correlation
    p = wa * np.conj(wb)
    coinc = np.real(p)
    quad = np.imag(p)

    # Smooth the cross-correlation components
    smooth_wavelet(coinc, wid, gaussian=gaussian)
    smooth_wavelet(quad, wid, gaussian=gaussian)

    # Power calculations
    p = np.abs(wa) ** 2
    smooth_wavelet(p, wid, gaussian=gaussian)

    gam = np.abs(wb) ** 2
    smooth_wavelet(gam, wid, gaussian=gaussian)

    # Calculate coincidence ratio
    crat = coinc / gam

    # Calculate coherence
    p_gam = p * gam
    gam = (coinc**2 + quad**2) / p_gam

    # Normalize coincidence and quadrature
    p_sqrt = np.sqrt(p_gam)
    coinc = coinc / p_sqrt
    quad = quad / p_sqrt

    return gam, coinc, quad, crat


def rotate_wavelet2(wv, B, xdir=None, wid=None, rotmats=None, get_rotmats=False):
    """
    Rotate a 3D wavelet vector field into local coordinate frames defined by B and xdir.

    Implementation of IDL rotate_wavelet2 function.

    Parameters
    ----------
    wv : ndarray of shape (nt, jv+1, 3)
        Input wavelet transform data with 3 spatial components.

    B : ndarray of shape (nt, 3)
        Vector field that defines the "z" axis of the local coordinate system at each time.

    xdir : array-like of shape (3,), optional
        A reference direction (default: [0, 0, 1]) used to define the "y" axis with B.
        This should not be parallel to B.

    wid : array-like of shape (jv+1,), required if rotmats is not supplied
        Smoothing window width (used on field B) for each scale.

    rotmats : ndarray of shape (nt, jv+1, 3, 3), optional
        Precomputed rotation matrices.

    get_rotmats : bool, optional
        If True, return the computed rotation matrices (useful for reuse).

    Returns
    -------
    wvp : ndarray of shape (nt, jv+1, 3)
        Wavelet transform rotated into local coordinates.

    rotmats_out : ndarray
        If True, return the computed rotation matrices. Shape (nt, jv+1, 3, 3).
        If False, return None.
    """
    # Get dimensions like IDL
    dim = list(wv.shape)
    nt = dim[0]
    jv = dim[1] - 1  # IDL uses jv = dim[1] - 1

    if dim[2] != 3:
        raise ValueError("Must have 3 dimensions")

    # Set default xdir
    if xdir is None or len(xdir) != 3:
        xdir = np.array([0.0, 0.0, 1.0])
    else:
        xdir = np.asarray(xdir)

    # Initialize rotation matrix and output wavelet
    rot = np.zeros((nt, 3, 3), dtype=np.float32)
    wvp = np.zeros_like(wv, dtype=wv.dtype)

    # Check if using precomputed rotmats
    use_rotmat = (rotmats is not None) and (not get_rotmats)

    # Initialize rotmats for output if requested
    if get_rotmats:
        rotmats_out = np.zeros((nt, dim[1], 3, 3), dtype=np.float32)

    # Main loop over scales (j=0 to jv, inclusive)
    for j in range(jv + 1):
        if use_rotmat:
            # Use precomputed rotation matrices
            rot = rotmats[:, j, :, :]
        else:
            if wid is None:
                raise ValueError("wid must be provided if rotmats are not used.")

            # Smooth B field components
            for k in range(3):
                width = min(int(wid[j]), nt - 1)
                if width > 1:
                    # Use uniform_filter1d to match IDL's smooth with /edge_truncate
                    rot[:, k, 2] = uniform_filter1d(
                        B[:, k].astype(float), size=width, mode="nearest"
                    )
                else:
                    rot[:, k, 2] = B[:, k]

            # Normalize z-axis (rot[*,*,2])
            z_norm = np.sqrt(np.sum(rot[:, :, 2] ** 2, axis=1))
            # Avoid division by zero
            z_norm = np.where(z_norm == 0, 1, z_norm)
            rot[:, :, 2] = rot[:, :, 2] / z_norm[:, np.newaxis]

            # Compute y-axis
            for i in range(nt):
                rot[i, :, 1] = np.cross(rot[i, :, 2], xdir)

            # Normalize y-axis
            y_norm = np.sqrt(np.sum(rot[:, :, 1] ** 2, axis=1))
            y_norm = np.where(y_norm == 0, 1, y_norm)
            rot[:, :, 1] = rot[:, :, 1] / y_norm[:, np.newaxis]

            # Compute x-axis
            for i in range(nt):
                rot[i, :, 0] = np.cross(rot[i, :, 1], rot[i, :, 2])

            # Store rotation matrices if requested
            if get_rotmats:
                rotmats_out[:, j, :, :] = rot

        # Apply rotation to wavelet components
        wvp[:, j, 2] = (
            wv[:, j, 0] * rot[:, 0, 2]
            + wv[:, j, 1] * rot[:, 1, 2]
            + wv[:, j, 2] * rot[:, 2, 2]
        )
        wvp[:, j, 1] = (
            wv[:, j, 0] * rot[:, 0, 1]
            + wv[:, j, 1] * rot[:, 1, 1]
            + wv[:, j, 2] * rot[:, 2, 1]
        )
        wvp[:, j, 0] = (
            wv[:, j, 0] * rot[:, 0, 0]
            + wv[:, j, 1] * rot[:, 1, 0]
            + wv[:, j, 2] * rot[:, 2, 0]
        )

    if get_rotmats:
        return wvp, rotmats_out
    else:
        return wvp, None


def wav_data(
    varname,
    period=None,
    prange=None,
    frange=None,
    param=None,
    avg_period=6.0,
    nmorlet=None,
    tplot_prefix=None,
    magrat=False,
    per_axis=False,
    kolom=None,
    normval=None,
    normconst=1.0,
    normname=None,
    get_components=False,
    tint_pow=None,
    fraction=False,
    rotmats=None,
    get_rotmats=False,
    wid=None,
    hermition_k=None,
    dimennum=None,
    rotate_pow=False,
    maxpoints=32768,  # 2^15 like IDL
    rbin=None,
    cross1=False,
    cross2=False,
    trange=None,
    resolution=0,  # Add resolution parameter like IDL
):
    """
    Python implementation of wav_data.pro. Computes wavelet transform of tplot variable,
    using the Torrence & Compo (1998) algorithm.

    Stores results in pytplot variables with normalization, masking, smoothing, and options.

    This function calls wavelet2.pro which sets various parameters for the wavelet transform in wavelet98.py.

    Parameters
    ----------
    varname : str
        Name of tplot variable to analyze
    period : array-like, optional
        Array of periods to use for wavelet analysis
    prange : array-like, optional
        Period range [min_period, max_period] in same units as time
    frange : array-like, optional
        Frequency range [min_freq, max_freq] - converted to prange
    param : float, optional
        Wavelet parameter (default=6 for Morlet wavelet)
    avg_period : float, optional
        Averaging period for smoothing (default=6.0)
    nmorlet : float, optional
        Number of Morlet wavelets, converted to param
    tplot_prefix : str, optional
        Prefix for output tplot variable names
    magrat : bool, optional
        Compute magnitude ratio analysis
    per_axis : bool, optional
        Use period (True) or frequency (False) for y-axis
    kolom : array-like, optional
        Kolmogorov spectrum for normalization
    normval : array-like or float, optional
        Normalization values
    normconst : float, optional
        Normalization constant (default=1.0)
    normname : str, optional
        Name of tplot variable for normalization
        TODO: not implemented yet, depends on function data_cut
    get_components : bool, optional
        Store individual component power spectra
    tint_pow : float, optional
        Power law for frequency normalization
    fraction : bool, optional
        Normalize by total power fraction
    rotmats : array-like, optional
        Precomputed rotation matrices for rotate_pow
    get_rotmats : bool, optional
        Return rotation matrices
    wid : array-like, optional
        Smoothing width array
    hermition_k : int, optional
        Hermitian analysis at specific frequency index
    dimennum : int, optional
        Select specific component of input variable
    rotate_pow : bool, optional
        Perform field-aligned coordinate analysis
    maxpoints : int, optional
        Maximum number of time points (default=32768)
    rbin : int, optional
        Rebinning factor
    cross1 : bool, optional
        Cross-correlation analysis type 1
    cross2 : bool, optional
        Cross-correlation analysis type 2
    trange : array-like, optional
        Time range for analysis
    resolution : int, optional
        Time resolution reduction factor. If > 0, reduces time resolution
        of output data using reduce_tres function (default=0, no reduction)

    Returns
    -------
    dict
        Dictionary with the following keys:
        - 'wave': ndarray, wavelet transform data
        - 'power': ndarray, power spectral data
        - 'period': ndarray, period/frequency scale values
        - 'yax': ndarray, y-axis values (period or frequency)
        - 'time': ndarray, time values
        - 'returned_rotmats': ndarray or None, rotation matrices if get_rotmats=True and rotate_pow=True
    """
    # Get tplot variable name
    name = tplot_prefix if tplot_prefix else varname
    if tnames(name) is None:
        logging.info(f"Variable: {name} not found.")
        return

    # Initialize output
    returned_rotmats = None

    # Handle nmorlet parameter
    if nmorlet is not None:
        param = nmorlet * 2 * np.pi

    # Get data
    d = get_data(name)
    time = d[0]
    B = d[1]
    if time is None or len(time) == 0:
        logging.info(f"Variable: {name} has no data.")
        return

    # Select component if requested
    if dimennum is not None:
        B = B[:, dimennum]
        name = f"{name}({dimennum})"

    # Frequency/period range
    if frange is not None and len(frange) == 2:
        prange = [1.0 / frange[1], 1.0 / frange[0]]

    # Rebin if requested
    if rbin is not None:
        n = len(time)
        nrbin = n // rbin
        time = time[: nrbin * rbin].reshape(nrbin, rbin).mean(axis=1)
        B = B[: nrbin * rbin]
        if B.ndim == 2:
            B = B.reshape(nrbin, rbin, B.shape[1]).mean(axis=1)
        else:
            B = B.reshape(nrbin, rbin).mean(axis=1)

    # Limit maxpoints
    if len(time) > maxpoints and trange is None:
        msg = f"Too many time samples, (Pts:{len(time)},Limit:{maxpoints}). Please select a different time range"
        logging.info(msg)
        return

    # Apply trange
    if trange is not None:
        if len(trange) == 1:
            idx = np.argmin(np.abs(time - trange[0]))
            rr = np.arange(
                max(0, idx - maxpoints // 2), min(len(time), idx + maxpoints // 2)
            )
            time = time[rr[0] : rr[-1] + 1]
            B = B[rr[0] : rr[-1] + 1]
        else:
            t0, t1 = min(trange), max(trange)
            w = np.where((time >= t0) & (time <= t1))[0]
            if len(w) == 0:
                logging.info("No data in that time range")
                return
            if len(w) > maxpoints:
                logging.info(
                    f"Too many time samples. (Pts:{len(w)},Limit:{maxpoints}). Please select a different time range"
                )
                return
            time = time[w]
            B = B[w]

    # Remove nans
    mask = np.isfinite(B).all(axis=-1) if B.ndim > 1 else np.isfinite(B)
    bad_index = np.where(~mask)[0]
    B = B[mask]
    time = time[mask]

    # dt and check sampling like IDL
    dtime = np.diff(time)
    dt = np.mean(dtime)

    # Check for uniform sampling and resample if needed (IDL logic)
    tgap_threshold = 0.1
    # Fix resampling threshold to match IDL: total(abs(minmax(dtime)/dt-1)) gt tgap_threshold
    if (
        np.sum(np.abs(np.array([np.min(dtime), np.max(dtime)]) / dt - 1))
        > tgap_threshold
    ):
        resample = True
    else:
        resample = False

    if resample:
        logging.info("Warning!!! Resampling data onto a uniform period")
        # IDL resampling logic
        dsample = np.round(dtime / np.median(dtime)).astype(int)
        samples = np.concatenate([[0], np.cumsum(dsample)])

        # Create new time array filled with NaNs
        re_time = np.full(np.max(samples) + 1, np.nan)
        re_time[samples] = time
        time = re_time

        # Interpolate gaps in time
        valid_mask = np.isfinite(time)
        if np.any(valid_mask):
            time_indices = np.arange(len(time))
            time[~valid_mask] = np.interp(
                time_indices[~valid_mask], time_indices[valid_mask], time[valid_mask]
            )

        # Create new B array filled with NaNs
        dim = list(B.shape)
        dim[0] = np.max(samples) + 1
        if B.ndim == 2:
            re_B = np.full((dim[0], dim[1]), np.nan)
            re_B[samples, :] = B
        else:
            re_B = np.full(dim[0], np.nan)
            re_B[samples] = B
        B = re_B

        # Interpolate gaps in B data
        if B.ndim == 2:
            for i in range(B.shape[1]):
                valid_mask = np.isfinite(B[:, i])
                if np.any(valid_mask):
                    B_indices = np.arange(len(B))
                    B[~valid_mask, i] = np.interp(
                        B_indices[~valid_mask], B_indices[valid_mask], B[valid_mask, i]
                    )
        else:
            valid_mask = np.isfinite(B)
            if np.any(valid_mask):
                B_indices = np.arange(len(B))
                B[~valid_mask] = np.interp(
                    B_indices[~valid_mask], B_indices[valid_mask], B[valid_mask]
                )

        # Recalculate dt
        dtime = np.diff(time)
        dt = np.mean(dtime)

    # Pad for FFT
    pad = 2

    # Compute wavelet
    wave, period = wavelet2(B, dt, pad=pad, period=period, prange=prange, param=param)

    if isinstance(wave, int) and wave == -1:
        logging.info("Time interval too short, Returning")
        return

    nt, jv1 = wave.shape[:2]
    nk = wave.shape[2] if wave.ndim == 3 else 1

    # IDL-style masking implementation - properly define badtime
    badtime = np.zeros(nt, dtype=bool)

    # Mark bad times from original bad_index mapping to new time array
    if len(bad_index) > 0:
        # Map original bad indices to new time indices after resampling
        original_length = len(mask)
        for bad_idx in bad_index:
            # Proportional mapping to new time array
            if original_length > 0:
                mapped_idx = int((bad_idx / original_length) * nt)
                if 0 <= mapped_idx < nt:
                    badtime[mapped_idx] = True

    # Axis labels
    yax = period if per_axis else 1.0 / period
    ysubtitle = "Seconds" if per_axis else "f (Hz)"
    mm = [np.min(yax), np.max(yax)]

    # Width used in smoothing - add IDL upper bound
    if wid is None:
        wid = (period / 2 / dt * avg_period) * 2 + 1
    # IDL: wid = 3 > round(period/2/dt*avg_period)*2+1 < (nt-1)
    wid = np.clip(np.maximum(wid, 3).astype(int), 3, nt - 1)

    # Create mask array like IDL (now with badtime properly defined)
    if np.any(badtime):
        # IDL logic: create mask with NaN for bad times, 1 for good times
        mask_array = np.ones(nt, dtype=float)
        mask_array[badtime] = np.nan

        # Smooth the mask like IDL
        mask_2d = mask_array[:, None] * np.ones(jv1)
        smooth_wavelet(mask_2d, wid)

        # IDL sets mask = ([1.,!values.f_nan])[msk]
        # Where msk is boolean array of mask validity
        msk = np.isfinite(mask_2d)
        mask_final = np.ones_like(mask_2d)
        mask_final[~msk] = np.nan
    else:
        # No bad times - mask is all ones like IDL
        mask_final = 1.0

    # Magnitude wavelet (if requested)
    wvmag = None
    if magrat:
        wvmag, _ = wavelet2(
            np.sqrt(np.sum(B**2, axis=-1)),
            dt,
            pad=pad,
            period=period,
            prange=prange,
            param=param,
        )

    # Normalization
    normpow = normconst
    if normval is not None:
        if np.isscalar(normval):
            normpow = normval * normconst
        elif hasattr(normval, "__len__") and len(normval) == nt:
            # Reshape normval for smoothing
            normpow = (normval * normconst)[:, None] * np.ones(jv1)
            smooth_wavelet(normpow, wid)
        else:
            normpow = normval * normconst

    tsfx = ""
    if fraction:
        # Handle 1D case properly like IDL
        if nk > 1:
            normpow = (np.sum(B**2, axis=-1))[:, None] * np.ones(jv1)
        else:
            normpow = (B**2)[:, None] * np.ones(jv1)
        smooth_wavelet(normpow, wid)
        normpow = 1.0 / normpow
        tsfx += "/<B^2>"

    if kolom is not None:
        # Ensure proper broadcasting
        if np.isscalar(normpow):
            normpow = normpow / (kolom * period ** (5.0 / 3.0))
        else:
            normpow = normpow / (np.ones(nt)[:, None] * (kolom * period ** (5.0 / 3.0)))
        tsfx += "/P_K"
    elif tint_pow is not None:
        # Ensure proper broadcasting
        if np.isscalar(normpow):
            normpow = normpow / (period**tint_pow)
        else:
            normpow = normpow / (np.ones(nt)[:, None] * (period**tint_pow))
        tsfx += "*f"
        if tint_pow != 1:
            tsfx += f"^{tint_pow:.2f}"

    # Apply normalization - handle scalar and array cases
    if np.isscalar(normpow):
        wave = wave * np.sqrt(normpow)
        if wvmag is not None:
            wvmag = wvmag * np.sqrt(normpow)
    else:
        for k in range(nk):
            wave[..., k] *= np.sqrt(normpow)
        if wvmag is not None:
            wvmag *= np.sqrt(normpow)

    # Power - match IDL exactly
    if nk == 1:
        pow = np.abs(wave) ** 2  # IDL: pow = abs(wv)^2
    else:
        pow = np.sum(np.abs(wave) ** 2, axis=2)

    # zrange - match IDL calculation exactly using roundsig
    if np.all(pow > 0):
        # IDL: roundsig(10^(average(alog(pow*mask),/nan)/alog(10)),sigfi=.2) * [.1,10]
        if np.isscalar(mask_final):
            pow_masked = pow * mask_final
        else:
            pow_masked = pow * mask_final
        valid_pow = pow_masked[np.isfinite(pow_masked) & (pow_masked > 0)]
        if len(valid_pow) > 0:
            # Calculate average of log10(pow*mask) ignoring NaN
            log_pow_mean = np.mean(np.log10(valid_pow))
            # Apply roundsig with sigfig=0.2 like IDL
            rounded_val = roundsig(10**log_pow_mean, sigfig=0.2)
            zrange = rounded_val * np.array([0.1, 10])
        else:
            zrange = np.array([1e-6, 1e-3])
    else:
        if tint_pow is not None:
            zrange = np.array([0.0001, 0.1])  # IDL default for tint_pow
        else:
            zrange = np.array([1e-6, 1e-3])

    # Store main power with nmorlet suffix like IDL
    wvs = "_wv"
    if nmorlet is not None:
        wvs += str(int(nmorlet))

    # Use reduce_tres like IDL
    r = resolution if resolution else 0
    rdtime = reduce_tres(time, r) if r > 0 else time

    polopts = {
        "spec": 1,
        "yrange": mm,
        "ylog": 1,
        "ystyle": 1,
        "no_interp": 1,
        "zrange": [-1, 1],
        "zlog": 0,
        "zstyle": 1,
        "ztitle": "",
        "ysubtitle": ysubtitle,
    }

    powopts = {
        "spec": 1,
        "yrange": mm,
        "ylog": 1,
        "ystyle": 1,
        "no_interp": 1,
        "zlog": 1,
        "zstyle": 1,
        "zrange": zrange,
        "ztitle": f"P_Tot{tsfx}",
        "ysubtitle": ysubtitle,
    }

    # Apply mask like IDL - remove the duplicate mask=1.0 line
    powname = name + wvs + "_pow"
    if np.isscalar(mask_final):
        reduced_pow = reduce_tres(pow * mask_final, r) if r > 0 else pow * mask_final
    else:
        reduced_pow = reduce_tres(pow * mask_final, r) if r > 0 else pow * mask_final
    store_data(
        powname, data={"x": rdtime, "y": reduced_pow, "v": yax}, attr_dict=powopts
    )
    options(powname, "spec", 1)
    options(powname, "ylog", 1)
    options(powname, "zlog", 1)

    if nk == 1:
        return {"wave": wave, "power": pow, "period": period, "yax": yax, "time": time}

    # Store components if requested (with proper masking)
    if get_components and nk > 1:
        cstr = ["x", "y", "z", "4"]
        for i in range(nk):
            powi = np.abs(wave[..., i]) ** 2
            if np.isscalar(mask_final):
                reduced_powi = (
                    reduce_tres(powi * mask_final, r) if r > 0 else powi * mask_final
                )
            else:
                reduced_powi = (
                    reduce_tres(powi * mask_final, r) if r > 0 else powi * mask_final
                )
            store_data(
                f"{name}_{cstr[i]}{wvs}_pow",
                data={"x": rdtime, "y": reduced_powi, "v": yax},
            )

    # Magnitude ratio (with proper masking)
    if magrat and wvmag is not None:
        powb = np.abs(wvmag) ** 2
        pol = powb / pow
        smooth_wavelet(pol, wid)
        ratopts = polopts.copy()
        ratopts["ztitle"] = "P_mag/P_tot"
        ratopts["zrange"] = [0, 1]
        if np.isscalar(mask_final):
            reduced_pol = (
                reduce_tres(pol * mask_final, r) if r > 0 else pol * mask_final
            )
        else:
            reduced_pol = (
                reduce_tres(pol * mask_final, r) if r > 0 else pol * mask_final
            )
        store_data(
            name + wvs + "_rat_par",
            data={"x": rdtime, "y": reduced_pol, "v": yax},
            attr_dict=ratopts,
        )

    # Update all other stored data to use mask_final instead of mask
    # Polarization for nk==2 (with proper masking)
    if nk == 2:
        i = 1j
        powr = np.abs(wave[..., 0] + i * wave[..., 1]) ** 2
        powl = np.abs(wave[..., 0] - i * wave[..., 1]) ** 2
        pol = (powr - powl) / (powl + powr)
        smooth_wavelet(pol, wid)
        pol_opts = polopts.copy()
        pol_opts["ztitle"] = "<σ_p>"
        if np.isscalar(mask_final):
            reduced_pol = (
                reduce_tres(pol * mask_final, r) if r > 0 else pol * mask_final
            )
        else:
            reduced_pol = (
                reduce_tres(pol * mask_final, r) if r > 0 else pol * mask_final
            )
        store_data(
            name + wvs + "_pol_perp",
            data={"x": rdtime, "y": reduced_pol, "v": yax},
            attr_dict=pol_opts,
        )

    # Update rotation section to use mask_final
    if rotate_pow:
        wv_rot, returned_rotmats = rotate_wavelet2(
            wave, B, wid=wid, rotmats=rotmats, get_rotmats=get_rotmats
        )
        i = 1j
        powr = np.abs(wv_rot[..., 0] + i * wv_rot[..., 1]) ** 2
        powl = np.abs(wv_rot[..., 0] - i * wv_rot[..., 1]) ** 2
        powb = np.abs(wv_rot[..., 2]) ** 2

        pol = powb / (powb + powl + powr)
        smooth_wavelet(pol, wid)
        ratopts = polopts.copy()
        ratopts["ztitle"] = "<P_||/P_tot>"
        ratopts["zrange"] = [0, 1]
        if np.isscalar(mask_final):
            reduced_pol = (
                reduce_tres(pol * mask_final, r) if r > 0 else pol * mask_final
            )
        else:
            reduced_pol = (
                reduce_tres(pol * mask_final, r) if r > 0 else pol * mask_final
            )
        store_data(
            name + wvs + "_pol_par",
            data={"x": rdtime, "y": reduced_pol, "v": yax},
            attr_dict=ratopts,
        )

        pol = (powr - powl) / (powl + powr)
        smooth_wavelet(pol, wid)
        pol_opts = polopts.copy()
        pol_opts["ztitle"] = "<σ_p>"
        if np.isscalar(mask_final):
            reduced_pol = (
                reduce_tres(pol * mask_final, r) if r > 0 else pol * mask_final
            )
        else:
            reduced_pol = (
                reduce_tres(pol * mask_final, r) if r > 0 else pol * mask_final
            )
        store_data(
            name + wvs + "_pol_perp",
            data={"x": rdtime, "y": reduced_pol, "v": yax},
            attr_dict=pol_opts,
        )

    # Hermitian analysis - add the missing section
    if hermition_k is not None and nk == 3:
        wv_hm = (
            np.conj(wave[:, hermition_k, :])[:, None] * wave[:, hermition_k, :][:, None]
        )
        wv_pow = wv_hm[:, 0, 0] + wv_hm[:, 1, 1] + wv_hm[:, 2, 2]
        if np.isscalar(mask_final):
            reduced_wv_pow = (
                reduce_tres(wv_pow * mask_final, r) if r > 0 else wv_pow * mask_final
            )
        else:
            reduced_wv_pow = (
                reduce_tres(wv_pow * mask_final[:, 0], r)
                if r > 0
                else wv_pow * mask_final[:, 0]
            )
        store_data(name + wvs + "_H_pow", data={"x": rdtime, "y": reduced_wv_pow})

        dbb = wv_hm.reshape(nt, 9)[:, [0, 4, 8, 1, 2, 5]]
        if np.isscalar(mask_final):
            dbb_normalized = dbb / (wv_pow[:, None]) * mask_final
        else:
            dbb_normalized = dbb / (wv_pow[:, None]) * mask_final[:, 0:1]

        reduced_dbb_real = (
            reduce_tres(dbb_normalized.real, r) if r > 0 else dbb_normalized.real
        )
        reduced_dbb_imag = (
            reduce_tres(dbb_normalized.imag, r) if r > 0 else dbb_normalized.imag
        )
        store_data(name + wvs + "_HN_real", data={"x": rdtime, "y": reduced_dbb_real})
        store_data(name + wvs + "_HN_imag", data={"x": rdtime, "y": reduced_dbb_imag})

        # Eigenvalue calculation (replaces IDL LA_ELMHES/LA_HQR)
        eigenvalues = np.zeros((nt, 3), dtype=float)
        for n in range(nt):
            # Extract 3x3 Hermitian matrix at time n
            herm_matrix = wv_hm[n, :, :]
            # Compute eigenvalues using numpy (equivalent to IDL LA_ELMHES+LA_HQR)
            evals = np.linalg.eigvals(herm_matrix)
            # Sort eigenvalues in descending order like IDL
            eigenvalues[n, :] = np.sort(np.real(evals))[::-1]

        # Normalize eigenvalues by trace like IDL
        trace = np.sum(eigenvalues, axis=1)
        eigenvalues_norm = eigenvalues / trace[:, None]

        # Store eigenvalues like IDL
        if np.isscalar(mask_final):
            reduced_eigenvalues = (
                reduce_tres(eigenvalues_norm * mask_final, r)
                if r > 0
                else eigenvalues_norm * mask_final
            )
        else:
            reduced_eigenvalues = (
                reduce_tres(eigenvalues_norm * mask_final[:, 0:1], r)
                if r > 0
                else eigenvalues_norm * mask_final[:, 0:1]
            )
        store_data(name + wvs + "_H_eval", data={"x": rdtime, "y": reduced_eigenvalues})

    # Update cross-correlation sections to use mask_final
    if cross1 and nk >= 2:
        # Linear polarization cross-correlation
        i = 1j
        wa = wave[..., 0] + i * wave[..., 1]
        wb = wave[..., 0] - i * wave[..., 1]

        gam, coinc, quad, crat = cross_corr_wavelet(wa, wb, wid, gaussian=True)

        ratopts_gam = polopts.copy()
        ratopts_gam["ztitle"] = "γ_l"
        if np.isscalar(mask_final):
            reduced_gam = (
                reduce_tres(gam * mask_final, r) if r > 0 else gam * mask_final
            )
        else:
            reduced_gam = (
                reduce_tres(gam * mask_final, r) if r > 0 else gam * mask_final
            )
        store_data(
            name + wvs + "_gam_lin",
            data={"x": rdtime, "y": reduced_gam, "v": yax},
            attr_dict=ratopts_gam,
        )

        pol_opts_coin = polopts.copy()
        pol_opts_coin["ztitle"] = "C_l"
        reduced_coinc = (
            reduce_tres(coinc * mask_final, r) if r > 0 else coinc * mask_final
        )
        store_data(
            name + wvs + "_coin_lin",
            data={"x": rdtime, "y": reduced_coinc, "v": yax},
            attr_dict=pol_opts_coin,
        )

        pol_opts_quad = polopts.copy()
        pol_opts_quad["ztitle"] = "Q_l"
        reduced_quad = reduce_tres(quad * mask_final, r) if r > 0 else quad * mask_final
        store_data(
            name + wvs + "_quad_lin",
            data={"x": rdtime, "y": reduced_quad, "v": yax},
            attr_dict=pol_opts_quad,
        )

        # Circular polarization cross-correlation
        wa = wave[..., 0]
        wb = wave[..., 1]

        gam, coinc, quad, crat = cross_corr_wavelet(wa, wb, wid, gaussian=True)

        ratopts_gam["ztitle"] = "γ_p"
        reduced_gam = reduce_tres(gam * mask_final, r) if r > 0 else gam * mask_final
        store_data(
            name + wvs + "_gam_cir",
            data={"x": rdtime, "y": reduced_gam, "v": yax},
            attr_dict=ratopts_gam,
        )

        pol_opts_coin["ztitle"] = "C_p"
        reduced_coinc = (
            reduce_tres(coinc * mask_final, r) if r > 0 else coinc * mask_final
        )
        store_data(
            name + wvs + "_coin_cir",
            data={"x": rdtime, "y": reduced_coinc, "v": yax},
            attr_dict=pol_opts_coin,
        )

        pol_opts_quad["ztitle"] = "Q_p"
        reduced_quad = reduce_tres(quad * mask_final, r) if r > 0 else quad * mask_final
        store_data(
            name + wvs + "_quad_cir",
            data={"x": rdtime, "y": reduced_quad, "v": yax},
            attr_dict=pol_opts_quad,
        )

    if cross2 and nk >= 3:
        # Parallel-perpendicular cross-correlation
        i = 1j
        wa = wave[..., 2]  # parallel component
        wb = wave[..., 0] + i * wave[..., 1]  # right-handed

        gam, coinc, quad, crat = cross_corr_wavelet(wa, wb, wid, gaussian=False)

        ratopts_gam = polopts.copy()
        ratopts_gam["ztitle"] = "γ_pr"
        reduced_gam = reduce_tres(gam * mask_final, r) if r > 0 else gam * mask_final
        store_data(
            name + wvs + "_gam_pr",
            data={"x": rdtime, "y": reduced_gam, "v": yax},
            attr_dict=ratopts_gam,
        )

        pol_opts_coin = polopts.copy()
        pol_opts_coin["ztitle"] = "C_pr"
        reduced_coinc = (
            reduce_tres(coinc * mask_final, r) if r > 0 else coinc * mask_final
        )
        store_data(
            name + wvs + "_coin_pr",
            data={"x": rdtime, "y": reduced_coinc, "v": yax},
            attr_dict=pol_opts_coin,
        )

        pol_opts_quad = polopts.copy()
        pol_opts_quad["ztitle"] = "Q_pr"
        reduced_quad = reduce_tres(quad * mask_final, r) if r > 0 else quad * mask_final
        store_data(
            name + wvs + "_quad_pr",
            data={"x": rdtime, "y": reduced_quad, "v": yax},
            attr_dict=pol_opts_quad,
        )

        # Left-handed
        wb = wave[..., 0] - i * wave[..., 1]
        gam, coinc, quad, crat = cross_corr_wavelet(wa, wb, wid, gaussian=False)

        ratopts_gam["ztitle"] = "γ_pl"
        reduced_gam = reduce_tres(gam * mask_final, r) if r > 0 else gam * mask_final
        store_data(
            name + wvs + "_gam_pl",
            data={"x": rdtime, "y": reduced_gam, "v": yax},
            attr_dict=ratopts_gam,
        )

        pol_opts_coin["ztitle"] = "C_pl"
        reduced_coinc = (
            reduce_tres(coinc * mask_final, r) if r > 0 else coinc * mask_final
        )
        store_data(
            name + wvs + "_coin_pl",
            data={"x": rdtime, "y": reduced_coinc, "v": yax},
            attr_dict=pol_opts_coin,
        )

        pol_opts_quad["ztitle"] = "Q_pl"
        reduced_quad = reduce_tres(quad * mask_final, r) if r > 0 else quad * mask_final
        store_data(
            name + wvs + "_quad_pl",
            data={"x": rdtime, "y": reduced_quad, "v": yax},
            attr_dict=pol_opts_quad,
        )

    logging.info(f"Finished wav_data for {name}")

    # Return dictionary with results
    result = {
        "wave": wave,
        "power": pow,
        "period": period,
        "yax": yax,
        "time": time,
        "returned_rotmats": returned_rotmats,
    }

    return result
