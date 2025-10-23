"""
This is a python version of the wavelet.pro script in IDL SPEDAS.
It computes the wavelet transform as described by Torrence & Compo (1998).

Reference: Torrence, C. and G. P. Compo, 1998: A Practical Guide to
           Wavelet Analysis. <I>Bull. Amer. Meteor. Soc.</I>, 79, 61-78.
"""

import numpy as np
from scipy.special import gamma, factorial
from scipy.stats import chi2


# Morlet wavelet function (Fourier domain)
def morlet(k0, scale, k):
    """
    Morlet wavelet in the Fourier domain.

    Parameters
    ----------
    k0 : float
        Non-dimensional wavenumber of the Morlet wavelet. If set to -1,
        the function will use the default value of 6.0.
    scale : float
        Wavelet scale.
    k : array_like
        Array of angular wavenumbers (rad / time unit). Typically created
        as in wavelet98: k = [0, k_pos..., k_neg...].

    Returns
    -------
    vmorlet : ndarray
        Complex-valued Morlet wavelet evaluated in the Fourier domain at
        the frequencies given by `k`. Shape matches `k`.
    period : float
        Equivalent Fourier period corresponding to the provided `scale`.
    coi : float
        Cone-of-influence value for this scale (in same units as `period`).
    dofmin : int
        Minimum degrees of freedom for significance testing (no smoothing).
    cdelta : float
        Reconstruction factor used for inverse wavelet reconstruction.
        May be -1 if undefined for the chosen `k0`.
    psi0 : float
        Time-domain normalization constant of the mother wavelet.

    Notes
    -----
    Implementation follows Torrence & Compo (1998). The returned `vmorlet`
    is normalized such that total energy equals the signal length N (see
    inline code comment "total energy=N").
    """
    # Set default wavenumber if not provided
    if k0 == -1:
        k0 = 6.0
    n = len(k)
    # Exponent for Morlet wavelet in Fourier space
    expnt = -((scale * k - k0) ** 2) / 2.0 * (k > 0)
    # Time step in Fourier domain
    dt = 2 * np.pi / (n * k[1])
    # Normalization factor
    norm = np.sqrt(2 * np.pi * scale / dt) * (
        np.pi**-0.25
    )  # total energy=N   [Eqn (7)]
    # Morlet wavelet in Fourier space
    vmorlet = norm * np.exp(np.maximum(expnt, -100))
    vmorlet = vmorlet * (expnt > -100)  # avoid underflow errors
    vmorlet = vmorlet * (k > 0)  # Heaviside step function
    # Scale to period conversion factor
    fourier_factor = (4 * np.pi) / (k0 + np.sqrt(2 + k0**2))  # Scale-->Fourier [Sec.3h]
    period = scale * fourier_factor
    # Cone of influence
    coi = fourier_factor / np.sqrt(2)  # Cone-of-influence [Sec. 3g]
    dofmin = 2  # Degrees of freedom

    cdelta = 0.776 if k0 == 6 else -1  # Reconstruction factor
    psi0 = np.pi**-0.25

    return vmorlet, period, coi, dofmin, cdelta, psi0


# Paul wavelet function (Fourier domain)
def paul(m, scale, k):
    """
    Paul wavelet in the Fourier domain.

    Parameters
    ----------
    m : float
        Order of the Paul wavelet. If set to -1, the function will use the
        default value of 4.0.
    scale : float
        Wavelet scale.
    k : array_like
        Array of angular wavenumbers (rad / time unit). Typically created
        as in wavelet98: k = [0, k_pos..., k_neg...].

    Returns
    -------
    vpaul : ndarray
        Complex-valued Paul wavelet evaluated in the Fourier domain at
        the frequencies given by `k`. Shape matches `k`.
    period : float
        Equivalent Fourier period corresponding to the provided `scale`.
    coi : float
        Cone-of-influence value for this scale (in same units as `period`).
    dofmin : int
        Minimum degrees of freedom for significance testing (no smoothing).
    cdelta : float
        Reconstruction factor used for inverse wavelet reconstruction.
        May be -1 if undefined for the chosen `m`.
    psi0 : float
        Time-domain normalization constant of the mother wavelet.

    Notes
    -----
    Implementation follows Torrence & Compo (1998). The returned `vpaul`
    is normalized such that total energy equals the signal length N (see
    inline code comment "total energy=N").
    """
    # Set default order if not provided
    if m == -1:
        m = 4.0
    n = len(k)
    expnt = -(scale * k) * (k > 0)
    dt = 2 * np.pi / (n * k[1])
    norm = np.sqrt(2 * np.pi * scale / dt) * (2**m / np.sqrt(m * factorial(2 * m - 1)))
    vpaul = norm * ((scale * k) ** m) * np.exp(np.maximum(expnt, -100)) * (expnt > -100)
    vpaul = vpaul * (k > 0)
    fourier_factor = 4 * np.pi / (2 * m + 1)
    period = scale * fourier_factor
    coi = fourier_factor * np.sqrt(2)
    dofmin = 2  # Degrees of freedom with no smoothing
    cdelta = 1.132 if m == 4 else -1  # Reconstruction factor
    psi0 = 2**m * factorial(m) / np.sqrt(np.pi * factorial(2 * m))

    return vpaul, period, coi, dofmin, cdelta, psi0


# Derivative of Gaussian (DOG) wavelet function (Fourier domain)
def dog(m, scale, k):
    """
    Derivative of Gaussian (DOG) wavelet in the Fourier domain.

    Parameters
    ----------
    m : int or float
        Order of the DOG wavelet (m-th derivative). If set to -1, the
        function will use the default value of 2.
    scale : float
        Wavelet scale.
    k : array_like
        Array of angular wavenumbers (rad / time unit). Typically created
        as in this module: k = [0, k_pos..., k_neg...].

    Returns
    -------
    gauss : ndarray
        Complex-valued DOG wavelet evaluated in the Fourier domain at the
        frequencies given by `k`. Shape matches `k`.
    period : float
        Equivalent Fourier period corresponding to the provided `scale`.
    coi : float
        Cone-of-influence value for this scale (in same units as `period`).
    dofmin : int
        Minimum degrees of freedom for significance testing (no smoothing).
    cdelta : float
        Reconstruction factor used for inverse wavelet reconstruction.
        May be -1 if undefined for the chosen `m`.
    psi0 : float
        Time-domain normalization constant of the mother wavelet.

    Notes
    -----
    Implementation follows Torrence & Compo (1998). Returned `gauss` is
    normalized such that total energy equals the signal length when used
    consistently with the rest of the transform implementation in this file.
    """
    # Set default order if not provided
    if m == -1:
        m = 2
    n = len(k)
    expnt = -((scale * k) ** 2) / 2.0
    dt = 2 * np.pi / (n * k[1])
    norm = np.sqrt(2 * np.pi * scale / dt) * np.sqrt(1.0 / gamma(m + 0.5))
    gauss = (
        -norm
        * (1j**m)
        * (scale * k) ** m
        * np.exp(np.maximum(expnt, -100))
        * (expnt > -100)
    )
    fourier_factor = 2 * np.pi * np.sqrt(2.0 / (2 * m + 1))
    period = scale * fourier_factor
    coi = fourier_factor / np.sqrt(2)
    dofmin = 1  # Degrees of freedom with no smoothing
    cdelta = -1
    psi0 = -1
    if m == 2:
        cdelta = 3.541  # reconstruction factor
        psi0 = 0.867325
    if m == 6:
        cdelta = 1.966  # reconstruction factor
        psi0 = 0.88406

    return gauss, period, coi, dofmin, cdelta, psi0


# Main wavelet transform function (Torrence & Compo 1998 style)
def wavelet98(
    y1,
    dt,
    s0=None,
    dj=None,
    j_scales=None,
    pad=0,
    mother="MORLET",
    param=-1,
    lag1=0.0,
    siglvl=0.95,
    recon=False,
    fft_theor=None,
    do_wave=True,
    do_daughter=False,
):
    """
    Compute the wavelet transform of a 1D time series
    using the Torrence & Compo (1998) algorithm.

    Parameters
    ----------
    y1 : array_like
        Time series to be analyzed.
    dt : float
        Time step of the time series (sampling time).
    s0 : float, optional
        Smallest scale of the wavelet transform. Default is 2 * dt.
    dj : float, optional
        Spacing between discrete scales of the wavelet transform. Default is 0.125.
        A smaller value will give better scale resolution, but it will be slower.
    j_scales : int, optional
        Number of scales minus one to use in the wavelet transform.
        Scales range from s0 to s0 * 2^(j_scales * dj).
        Default is int(np.floor(np.log2(n * dt / s0) / dj)).
    pad : int {0, 1, 2}, optional::

            pad = 0, no padding (default)
            pad = 1, pad the time series to the next power of 2
            pad = 2, pad the time series to the next power of 4

    mother : string {'MORLET', 'PAUL', 'DOG'}, optional
        A string giving the mother wavelet to use. Default is 'MORLET'.
    param : float, optional
        Parameter for the mother wavelet. Default is -1::

                For 'Morlet' this is k0 (wavenumber), default is 6.
                For 'Paul' this is m (order), default is 4.
                For 'DOG' this is m (m-th derivative), default is 2.

    lag1 : float, optional
        Lag-1 autocorrelation of the time series used for SIGNIF levels.
        Default is 0.0.
    siglvl : float, optional
        Significance level to use for the wavelet transform. Default is 0.95.
    recon : bool, optional
        If True, reconstruct the time series from the wavelet transform.
        Default is False.
    fft_theor : array_like, optional
        Theoretical background spectrum as a function of
        Fourier frequency. This will be smoothed by the
        wavelet function.
    do_wave: bool, optional
        If True, return the wavelet transform. Default is True.
    do_daughter: bool, optional
        If True, return the wavelet transform of the mother wavelet.
        Default is False.

    Returns
    -------
    wave : array_like
        Wavelet transform of the time series.
        This is a complex array of dimensions (N,j_scales+1).
    scale : array_like
        Scales of the wavelet transform.
    period : array_like
        Periods of the wavelet transform.
    signif : array_like
        Significance levels of the wavelet transform.
    daughter: array_like
        Wavelet wavelets, if do_daughter is True. Else, an empty array.
    y2 : array_like
        Reconstructed time series, if recon is True. Else, -1.
    fft_theor_out : array_like
        Output theoretical background spectrum (smoothed by the
        wavelet function) that was used in the wavelet transform.

    References
    ----------
    Torrence, C. and G. P. Compo, 1998: A Practical Guide to Wavelet Analysis.
    <I>Bull. Amer. Meteor. Soc.</I>, 79, 61-78.
    """
    y1 = np.asarray(y1)
    n = len(y1)
    n1 = n
    y2 = -1  # This will become the reconstructed time series, if recon is True
    y1_orig = y1.copy()

    # Set default parameters if not provided
    if s0 is None:
        s0 = 2 * dt
    if dj is None:
        dj = 1.0 / 8
    if j_scales is None:
        j_scales = int(np.trunc(np.log2(n * dt / s0) / dj))  # [Eqn (10)]
    if mother is None:
        mother = "MORLET"
    if param is None:
        param = -1

    # Remove mean from input
    ypad = y1 - np.sum(y1) / n

    # Pad to next power of 2 for FFT speed, if requested
    if pad is not None and pad != 0:
        n = len(ypad)
        if pad == 1:
            base2 = int(np.trunc(np.log2(n) + 0.4999))  # for "nearest power of 2"
        elif pad == 2:
            base2 = int(np.trunc(np.log2(n)))  # for "next lowest integer power of 2"
        else:
            raise ValueError("pad must be 1 or 2")
        num_pad = 2 ** (base2 + 1) - n

        # Pad the input
        if num_pad > 0:
            ypad = np.concatenate([ypad, np.zeros(num_pad, dtype=np.float32)])
        n = len(ypad)

    # Construct scale array (logarithmic spacing)
    na = int(j_scales + 1)  # Cast na as an integer, this is the number of scales
    scale = np.arange(na) * dj  # array of j values
    scale = (2.0**scale) * s0  # array of scales 2^j, [Eqn (9)]
    period = np.empty(na, dtype=np.float32)  # uninitialized (empty) float array
    wave = np.empty((n, na), dtype=np.complex64)  # uninitialized (empty) complex array
    daughter = np.empty(
        (n, na), dtype=np.complex64
    )  # uninitialized (empty) complex array

    # Construct wavenumber array used in transform [Eqn (5)]
    k_pos = (np.arange(n // 2, dtype=np.float64) + 1) * (2 * np.pi) / (n * dt)
    k_reversed = -k_pos[: ((n - 1) // 2)][::-1]
    k = np.concatenate(([0.0], k_pos, k_reversed))

    # FFT of the (possibly padded) input, normalize it similarly to IDL
    yfft = np.fft.fft(ypad, norm="forward")  # [Eqn (3)]

    # Theoretical background spectrum for significance
    if fft_theor is not None and len(fft_theor) == n:
        # If fft_theor exists and has length n, use it
        fft_theor_k = fft_theor
    else:
        fft_theor_k = (1 - lag1**2) / (
            1 - 2 * lag1 * np.cos(k * dt) + lag1**2
        )  # [Eqn(16)]
    fft_theor_out = np.zeros(na)

    # Main loop over all scales
    for a1 in range(na):
        if mother.upper() == "MORLET":
            psi_fft, period1, coi, dofmin, cdelta, psi0 = morlet(param, scale[a1], k)
        elif mother.upper() == "PAUL":
            psi_fft, period1, coi, dofmin, cdelta, psi0 = paul(param, scale[a1], k)
        elif mother.upper() == "DOG":
            psi_fft, period1, coi, dofmin, cdelta, psi0 = dog(param, scale[a1], k)
        else:
            raise ValueError(
                "Unknown mother wavelet; accepted values: MORLET, PAUL, DOG"
            )
        # Inverse FFT to get wavelet transform at this scale
        if do_wave:
            wave[:, a1] = np.fft.ifft(yfft * psi_fft) * n  # wavelet transform [Eqn (4)]
        if do_daughter:
            daughter[:, a1] = np.fft.ifft(psi_fft) * n

        period[a1] = period1
        # Theoretical spectrum for significance
        fft_theor_out[a1] = np.sum(np.abs(psi_fft) ** 2 * fft_theor_k) / n

    #  ; COI [Sec.3g]
    idx = np.concatenate(
        [
            np.arange((n1 + 1) // 2, dtype=np.float32),  # FINDGEN((n1+1)/2)
            np.arange(n1 // 2 - 1, -1, -1, dtype=np.float32),  # REVERSE(FINDGEN(n1/2))
        ]
    )
    # Elementwise multiply and scale by dt
    coi = coi * idx * dt

    # shift so DAUGHTERs are in middle of array
    if do_daughter:
        half_n1 = n1 // 2
        daughter = np.concatenate(
            (daughter[n - half_n1 :, ...], daughter[: n - half_n1, ...]), axis=0
        )

    # Significance levels (chi-squared test) [Sec.4]
    sdev = np.var(y1_orig)
    fft_theor_out = sdev * fft_theor_out
    dof = dofmin
    # IDL uses the chisqr_csf function, the equivalent in python is scipy.stats.chi2.ppf
    signif = fft_theor_out * chi2.isf(1.0 - siglvl, dof) / dof  # [Eqn (18)]

    # Optional: reconstruct the time series from the wavelet transform [Eqn (11)]
    if recon:
        if cdelta == -1:
            y2 = -1
            print("cdelta undefined, cannot reconstruct with this wavelet")
        else:
            wave_float = (
                wave.astype(np.float32)
                if not np.issubdtype(wave.dtype, np.floating)
                else wave
            )

            # Refine reconstruction logic to match IDL
            scale_factor = 1.0 / np.sqrt(scale)
            y2 = (
                dj
                * np.sqrt(dt)
                / (cdelta * psi0)
                * np.sum(wave_float * scale_factor[None, :], axis=1)
            )
            y2 = y2[:n1]  # Ensure the reconstructed array matches the original length

    # Return wavelet transform, scales, periods, and significance
    return wave[:n1, :], scale, period, signif, daughter, y2, fft_theor_out
