"""
Python implementation of IDL SPEDAS wav_data.pro.

Uses wavelet2.py which is a wrapper for wavelet98.py.
"""

import numpy as np
import logging
from pyspedas.analysis.wavelet2 import wavelet2
from pyspedas.analysis.reduce_tres import reduce_tres
from pyspedas.analysis.roundsig import roundsig
from pyspedas.analysis.interp_gap import interp_gap
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
    It does not return a new array.
    """
    dim = list(wv.shape) + [1, 1]
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
                    vx = np.linspace(-2, 2, kernel_size)
                    kernel = np.exp(-(vx**2))
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
                # smoothed = smooth(signal, width=widi[j], preserve_nans=True)

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
    gam, coinc, quad, crat : tuple

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
    wa = np.asarray(wa, dtype=complex)
    wb = np.asarray(wb, dtype=complex)
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


def rotate_wavelet2(wv, bfield, xdir=None, wid=None, rotmats=None, get_rotmats=False):
    """
    Rotate a 3D wavelet vector field into local coordinate frames defined by B and xdir.

    Implementation of IDL rotate_wavelet2 function.

    Parameters
    ----------
    wv : ndarray of shape (nt, jv+1, 3)
        Input wavelet transform data with 3 spatial components.

    bfield : ndarray of shape (nt, 3)
        Vector field that defines the "z" axis of the local coordinate system at each time.

    xdir : array-like of shape (3,), optional
        A reference direction (default: [0, 0, 1]) used to define the "y" axis with bfield.
        This should not be parallel to bfield.

    wid : array-like of shape (jv+1,), required if rotmats is not supplied
        Smoothing window width (used on field B) for each scale.

    rotmats : ndarray of shape (nt, jv+1, 3, 3), optional
        Precomputed rotation matrices.

    get_rotmats : bool, optional
        If True, return the computed rotation matrices (useful for reuse).

    Returns
    -------
    wvp, rotmats_out : tuple

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
                vwidth = min(int(wid[j]), nt - 1)
                if vwidth > 1:
                    # Use uniform_filter1d to match IDL's smooth with /edge_truncate
                    rot[:, k, 2] = uniform_filter1d(
                        bfield[:, k].astype(float), size=vwidth, mode="nearest"
                    )
                else:
                    rot[:, k, 2] = bfield[:, k]

            # Normalize z-axis (rot[*,*,2])
            z_norm = np.sqrt(np.sum(rot[:, :, 2] ** 2, axis=1))
            # Avoid division by zero
            z_norm = np.where(z_norm == 0, 1, z_norm)
            rot[:, :, 2] = rot[:, :, 2] / z_norm[:, np.newaxis]

            # Compute y-axis
            for ni in range(nt):
                rot[ni, :, 1] = np.cross(rot[ni, :, 2], xdir)

            # Normalize y-axis
            y_norm = np.sqrt(np.sum(rot[:, :, 1] ** 2, axis=1))
            y_norm = np.where(y_norm == 0, 1, y_norm)
            rot[:, :, 1] = rot[:, :, 1] / y_norm[:, np.newaxis]

            # Compute x-axis
            for ni in range(nt):
                rot[ni, :, 0] = np.cross(rot[ni, :, 1], rot[ni, :, 2])

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


def wav_data_set_options(varname, vdict):
    """Set pyspedas options for wavelet data visualization."""
    for key, value in vdict.items():
        options(varname, key, value)


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
    get_components=False,
    tint_pow=None,
    fraction=False,
    rotmats=None,
    get_rotmats=False,
    wid=None,
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

            'wave': ndarray, wavelet transform data
            'power': ndarray, power spectral data
            'period': ndarray, period/frequency scale values
            'yax': ndarray, y-axis values (period or frequency)
            'time': ndarray, time values
            'returned_rotmats': ndarray or None, rotation matrices if get_rotmats=True and rotate_pow=True
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
    bfield = d[1]
    if time is None or len(time) == 0:
        logging.info(f"Variable: {name} has no data.")
        return

    # Select component if requested
    if dimennum is not None:
        bfield = bfield[:, dimennum]
        name = f"{name}({dimennum})"

    # Frequency/period range
    if frange is not None and len(frange) == 2:
        prange = [1.0 / frange[1], 1.0 / frange[0]]

    # Rebin if requested
    if rbin is not None:
        nn = len(time)
        nrbin = nn // rbin
        time = time[: nrbin * rbin].reshape(nrbin, rbin).mean(axis=1)
        bfield = bfield[: nrbin * rbin]
        if bfield.ndim == 2:
            bfield = bfield.reshape(nrbin, rbin, bfield.shape[1]).mean(axis=1)
        else:
            bfield = bfield.reshape(nrbin, rbin).mean(axis=1)

    # Limit maxpoints
    if len(time) > maxpoints and trange is None:
        msg = f"Too many time samples, (Pts:{len(time)},Limit:{maxpoints}). Please select a different time range"
        logging.info(msg)
        return

    # Apply trange
    if trange is not None:
        if len(trange) == 1:
            idxn = np.argmin(np.abs(time - trange[0]))
            rr = np.arange(
                max(0, idxn - maxpoints // 2), min(len(time), idxn + maxpoints // 2)
            )
            time = time[rr[0] : rr[-1] + 1]
            bfield = bfield[rr[0] : rr[-1] + 1]
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
            bfield = bfield[w]

    # dt and check sampling like IDL
    dtime = np.diff(time)
    dt = np.mean(dtime)

    # Check for uniform sampling and resample if needed
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
        # This part fixes any time axis non-uniformity by resampling onto a uniform grid
        logging.warning("Warning!!! Resampling data onto a uniform period")
        dsample = np.round(dtime / np.median(dtime)).astype(int)
        samples = np.concatenate(([0], np.cumsum(dsample, dtype=int)))
        grid_len = samples[-1] + 1

        re_time = np.full(grid_len, np.nan, dtype=float)
        re_time[samples] = time
        time = interp_gap(np.arange(grid_len, dtype=float), re_time)["y"]

        # Initialize re_B with the appropriate shape and data type
        if bfield.ndim == 1:
            re_b = np.full(grid_len, np.nan, dtype=bfield.dtype)
            re_b[samples] = bfield
        elif bfield.ndim == 2:
            re_b = np.full((grid_len, bfield.shape[1]), np.nan, dtype=bfield.dtype)
            re_b[samples, :] = bfield
        elif bfield.ndim == 3:
            re_b = np.full(
                (grid_len, bfield.shape[1], bfield.shape[2]), np.nan, dtype=bfield.dtype
            )
            re_b[samples, :, :] = bfield
        else:
            re_b = np.full((grid_len,) + bfield.shape[1:], np.nan, dtype=bfield.dtype)
            src = (slice(None),) * (bfield.ndim - 1)
            re_b[(samples,) + src] = bfield

        bfield = re_b

        dtime = np.diff(time)
        dt = np.mean(dtime)

    # Interpolate gaps in bfield to match IDL
    interp_out = interp_gap(time, bfield)
    nbad_count = interp_out["count"]
    if nbad_count > 0:
        logging.info(f"Warning!!! Interpolating {nbad_count} bad points in data")
        bfield = interp_out["y"]
        # bad_index = interp_out["index"] # not used

    # Pad for FFT
    pad = 2

    # Compute wavelet
    wave, period = wavelet2(
        bfield, dt, pad=pad, period=period, prange=prange, param=param
    )

    if isinstance(wave, int) and wave == -1:
        logging.info("Time interval too short, Returning")
        return

    nt, jv1 = wave.shape[:2]
    nk = wave.shape[2] if wave.ndim == 3 else 1

    # Magnitude wavelet
    wvmag = None
    if magrat:
        logging.info("Computing magnitude now")
        wvmag, _ = wavelet2(
            np.sqrt(np.sum(bfield**2, axis=-1)),
            dt,
            pad=pad,
            period=period,
            prange=prange,
            param=param,
        )

    # Axis labels
    yax = period if per_axis else 1.0 / period
    ysubtitle = "Seconds" if per_axis else "f (Hz)"
    mm = [np.min(yax), np.max(yax)]

    # Width used in smoothing
    if wid is None:
        wid = (period / 2 / dt * avg_period) * 2 + 1
    wid = np.maximum(wid, 3).astype(int)

    # Normalization
    normpow = normconst
    if normval is not None:
        normval_arr = np.asarray(normval, dtype=float)
        if normval_arr.size == nt:
            logging.info("Calculating Normalization")
            normpow = normval_arr[:, None] * np.full((1, jv1), normconst, dtype=float)
            smooth_wavelet(normpow, wid)
        elif normval_arr.size == 1:
            normpow = float(normval_arr.ravel()[0])

    tsfx = ""
    if fraction:
        # Fractional normalization
        logging.info("Calculating Fractional Power")
        if nk > 1:
            normpow = (np.sum(bfield**2, axis=-1))[:, None] * np.ones(jv1)
        else:
            normpow = (bfield**2)[:, None] * np.ones(jv1)
        smooth_wavelet(normpow, wid)
        normpow = 1.0 / normpow
        tsfx += "$<B^2>$"

    zrangetmp = None  # temp zrange
    if kolom is not None:
        # Kolmogorov normalization
        logging.info("Calculating Kolmogorov Normalization")
        if np.isscalar(normpow):
            normpow = normpow / (kolom * period ** (5.0 / 3.0))
        else:
            normpow = normpow / (np.ones(nt)[:, None] * (kolom * period ** (5.0 / 3.0)))
        tsfx += "$P_{K}$"
        zrangetmp = [0.1, 10.0]
    elif tint_pow is not None:
        # Power-law normalization
        logging.info("Calculating Power-Law Normalization")
        if np.isscalar(normpow):
            normpow = normpow / (period**tint_pow)
        else:
            normpow = normpow / (np.ones(nt)[:, None] * (period**tint_pow))
        tsfx += "*f"
        if tint_pow != 1:
            vsub = f"{tint_pow:4.2f}"
            tsfx += f"$_{{{vsub}}}$"
        zrangetmp = [0.0001, 1.0]

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

    # Power
    if nk == 1:
        wpow = np.abs(wave) ** 2
    else:
        wpow = np.sum(np.abs(wave) ** 2, axis=2)

    # zrange
    mask_final = 1.0
    zrange = [-1.0, 1.0]
    if zrangetmp is not None:
        zrange = zrangetmp
    else:
        zrange = roundsig(
            10 ** np.nanmean(np.log10(wpow * mask_final)), sigfig=0.2
        ) * np.array([0.1, 10.0])

    # Store main power with nmorlet suffix
    wvs = "_wv"
    if nmorlet is not None:
        wvs += str(int(nmorlet))

    # Use reduce_tres
    r = resolution if resolution else 0
    rdtime = reduce_tres(time, r)
    ztitle = ""  # ztitle changes for each tplot variable

    polopts = {
        "spec": 1,
        "yrange": mm,
        "ylog": 1,
        "ystyle": 1,
        "no_interp": 1,
        "zrange": [-1.0, 1.0],
        "zlog": 0,
        "zstyle": 1,
        "ztitle": ztitle,
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
        "ztitle": ztitle,
        "ysubtitle": ysubtitle,
    }

    # Apply mask
    powname = name + wvs + "_pow"
    reduced_pow = reduce_tres(wpow * mask_final, r)
    powopts["ztitle"] = "$P_{Tot}$" + tsfx
    store_data(
        powname, data={"x": rdtime, "y": reduced_pow, "v": yax}, attr_dict=powopts
    )
    wav_data_set_options(powname, powopts)

    if nk == 1:
        # Single component ends here
        return {"wave": wave, "power": wpow, "period": period, "yax": yax, "time": time}

    # Store components if requested
    if get_components and nk > 1:
        cstr = ["x", "y", "z", "4"]
        for ni in range(nk):
            powi = np.abs(wave[..., ni]) ** 2
            nistr = cstr[ni]
            varname = name + "_" + nistr + wvs + "_pow"
            powopts["ztitle"] = "$P_{" + nistr + "}$" + tsfx
            store_data(
                varname,
                data={"x": rdtime, "y": reduce_tres(powi * mask_final, r), "v": yax},
                attr_dict=powopts,
            )
            wav_data_set_options(varname, powopts)

    # Magnitude ratio
    if magrat and wvmag is not None:
        varname = name + wvs + "_rat_par"
        powb = np.abs(wvmag) ** 2
        pol = powb / wpow
        smooth_wavelet(pol, wid)
        ztitle = "$P_{mag}/P_{tot}$"
        ratopts = polopts.copy()
        ratopts["ztitle"] = ztitle
        ratopts["zrange"] = [0.0, 1.0]
        store_data(
            varname,
            data={"x": rdtime, "y": reduce_tres(pol * mask_final, r), "v": yax},
            attr_dict=ratopts,
        )
        wav_data_set_options(varname, ratopts)

    ratopts = polopts.copy()
    ratopts["ztitle"] = "$P_{\\parallel}/P_{tot}$"
    ratopts["zrange"] = [0, 1]

    if nk == 2:
        # Form right/left circular powers powr / powl
        powr = np.abs(wave[..., 0] + 1j * wave[..., 1]) ** 2
        powl = np.abs(wave[..., 0] - 1j * wave[..., 1]) ** 2
        pol = (powr - powl) / (powl + powr)
        smooth_wavelet(pol, wid)
        reduced_pol = reduce_tres(pol * mask_final, r)
        varname = name + wvs + "_pol_perp"
        polopts["ztitle"] = "$P_{\\perp}$"
        store_data(
            varname,
            data={"x": rdtime, "y": reduced_pol, "v": yax},
            attr_dict=polopts,
        )
        wav_data_set_options(varname, polopts)

    # Rotate wavelet
    if rotate_pow:
        logging.info("Computing power and polarization for TPLOT")
        wv_rot, returned_rotmats = rotate_wavelet2(
            wave, bfield, wid=wid, rotmats=rotmats, get_rotmats=get_rotmats
        )
        powr = np.abs(wv_rot[..., 0] + 1j * wv_rot[..., 1]) ** 2
        powl = np.abs(wv_rot[..., 0] - 1j * wv_rot[..., 1]) ** 2
        powb = np.abs(wv_rot[..., 2]) ** 2

        pol = powb / (powb + powl + powr)
        smooth_wavelet(pol, wid)
        varname = name + wvs + "_pol_par"
        store_data(
            varname,
            data={"x": rdtime, "y": reduce_tres(pol * mask_final, r), "v": yax},
            attr_dict=ratopts,
        )
        wav_data_set_options(varname, ratopts)

        pol = (powr - powl) / (powl + powr)
        smooth_wavelet(pol, wid)
        varname = name + wvs + "_pol_perp"
        polopts["ztitle"] = "$P_{\\perp}$"
        store_data(
            varname,
            data={"x": rdtime, "y": reduce_tres(pol * mask_final, r), "v": yax},
            attr_dict=polopts,
        )
        wav_data_set_options(varname, polopts)

    # Hermitian analysis - hermition_k
    # Removed because IDL code uses the function 'polyroots' which is not defined

    if cross1 and nk >= 2:
        logging.info("Computing cross-correlation cross1")
        # Linear polarization cross-correlation
        wa = wave[..., 0] + 1j * wave[..., 1]
        wb = wave[..., 0] - 1j * wave[..., 1]

        cpol, cpow, cpowb, _ = cross_corr_wavelet(wa, wb, wid, gaussian=True)

        vname = name + wvs + "_gam_lin"
        ratopts["ztitle"] = "$g_l$"
        store_data(
            vname,
            data={"x": rdtime, "y": reduce_tres(cpol * mask_final, r), "v": yax},
            attr_dict=ratopts,
        )
        wav_data_set_options(vname, ratopts)

        vname = name + wvs + "_coin_lin"
        polopts["ztitle"] = "$C_l$"
        store_data(
            vname,
            data={"x": rdtime, "y": reduce_tres(cpow * mask_final, r), "v": yax},
            attr_dict=polopts,
        )
        wav_data_set_options(vname, polopts)

        vname = name + wvs + "_quad_lin"
        polopts["ztitle"] = "$Q_l$"
        store_data(
            vname,
            data={"x": rdtime, "y": reduce_tres(cpowb * mask_final, r), "v": yax},
            attr_dict=polopts,
        )
        wav_data_set_options(vname, polopts)

        # Circular polarization cross-correlation
        wa = wave[..., 0]
        wb = wave[..., 1]
        cpol, cpow, cpowb, _ = cross_corr_wavelet(wa, wb, wid, gaussian=True)

        vname = name + wvs + "_gam_cir"
        ratopts["ztitle"] = "$g_p$"
        store_data(
            vname,
            data={"x": rdtime, "y": reduce_tres(cpol * mask_final, r), "v": yax},
            attr_dict=ratopts,
        )
        wav_data_set_options(vname, ratopts)

        vname = name + wvs + "_coin_cir"
        polopts["ztitle"] = "$C_p$"
        store_data(
            vname,
            data={"x": rdtime, "y": reduce_tres(cpow * mask_final, r), "v": yax},
            attr_dict=polopts,
        )
        wav_data_set_options(vname, polopts)

        vname = name + wvs + "_quad_cir"
        polopts["ztitle"] = "$Q_p$"
        store_data(
            vname,
            data={"x": rdtime, "y": reduce_tres(cpowb * mask_final, r), "v": yax},
            attr_dict=polopts,
        )
        wav_data_set_options(vname, polopts)

    if cross2 and nk >= 3:
        logging.info("Computing cross-correlation cross2")
        # Parallel-perpendicular cross-correlation
        wa = wave[..., 2]  # parallel component
        wb = wave[..., 0] + 1j * wave[..., 1]  # right-handed

        c2pol, c2pow, c2powb, _ = cross_corr_wavelet(wa, wb, wid, gaussian=False)

        vname = name + wvs + "_gam_pr"
        ratopts["ztitle"] = "$g_{pr}$"
        store_data(
            vname,
            data={"x": rdtime, "y": reduce_tres(c2pol * mask_final, r), "v": yax},
            attr_dict=ratopts,
        )
        wav_data_set_options(vname, ratopts)

        vname = name + wvs + "_coin_pr"
        polopts["ztitle"] = "$C_{pr}$"
        store_data(
            vname,
            data={"x": rdtime, "y": reduce_tres(c2pow * mask_final, r), "v": yax},
            attr_dict=polopts,
        )
        wav_data_set_options(vname, polopts)

        vname = name + wvs + "_quad_pr"
        polopts["ztitle"] = "$Q_{pr}$"
        store_data(
            vname,
            data={"x": rdtime, "y": reduce_tres(c2powb * mask_final, r), "v": yax},
            attr_dict=polopts,
        )
        wav_data_set_options(vname, polopts)

        # Left-handed
        wb = wave[..., 0] - 1j * wave[..., 1]
        c2pol, c2pow, c2powb, _ = cross_corr_wavelet(wa, wb, wid, gaussian=False)

        vname = name + wvs + "_gam_pl"
        ratopts["ztitle"] = "$g_{pl}$"
        store_data(
            vname,
            data={"x": rdtime, "y": reduce_tres(c2pol * mask_final, r), "v": yax},
            attr_dict=ratopts,
        )
        wav_data_set_options(vname, ratopts)

        vname = name + wvs + "_coin_pl"
        polopts["ztitle"] = "$C_{pl}$"
        store_data(
            vname,
            data={"x": rdtime, "y": reduce_tres(c2pow * mask_final, r), "v": yax},
            attr_dict=polopts,
        )
        wav_data_set_options(vname, polopts)

        vname = name + wvs + "_quad_pl"
        polopts["ztitle"] = "$Q_{pl}$"
        store_data(
            vname,
            data={"x": rdtime, "y": reduce_tres(c2powb * mask_final, r), "v": yax},
            attr_dict=polopts,
        )
        wav_data_set_options(vname, polopts)

    logging.info(f"Finished wav_data for {name}")

    # Return dictionary with results
    result = {
        "wave": wave,
        "power": wpow,
        "period": period,
        "yax": yax,
        "time": time,
        "returned_rotmats": returned_rotmats,
    }

    return result
