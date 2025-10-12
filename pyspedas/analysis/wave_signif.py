"""
This is a python version of the wave_signif.pro script in IDL SPEDAS.
It computes the significance levels for a wavelet transform
as described by Torrence & Compo (1998).

Reference: Torrence, C. and G. P. Compo, 1998: A Practical Guide to
           Wavelet Analysis. <I>Bull. Amer. Meteor. Soc.</I>, 79, 61-78.

See also: wavelet98.py
"""

import numpy as np
from scipy.stats import chi2

def wave_signif(Y, dt, scale, sigtest, **kwargs):
    """
    Compute significance levels for wavelet transforms.

    Parameters:
    -----------

    Y : float or array_like
        The time series, or, the VARIANCE of the time series.
        (If this is a single number, it is assumed to be the variance...)
    dt : float
        Amount of time between each Y value, i.e. the sampling time.
    scale : array_like
        The vector of scale indices, from previous call to WAVELET.
    sigtest : int {0, 1, 2}
        Type of significance test::

            If 0 (the default), then just do a regular chi-square test,
               i.e. Eqn (18) from Torrence & Compo.
            If 1, then do a "time-average" test, i.e. Eqn (23).
                     In this case, DOF should be set to NA, the number
                     of local wavelet spectra that were averaged together.
                     For the Global Wavelet Spectrum, this would be NA=N,
                     where N is the number of points in your time series.
            If 2, then do a "scale-average" test, i.e. Eqns (25)-(28).
                     In this case, DOF should be set to a
                     two-element vector [S1,S2], which gives the scale
                     range that was averaged together.
                     e.g. if one scale-averaged scales between 2 and 8,
                         then DOF=[2,8].

    kwargs : dict
        Dictionary, containing optional additional parameters::

            lag1: Lag-1 autocorrelation (default: 0.0)
            siglvl: Significance level (default: 0.95)
            mother: Mother wavelet ('MORLET', 'PAUL', 'DOG')
            param: Mother wavelet parameter
            dof: Degrees of freedom for significance tests
            gws: Global wavelet spectrum (optional)
            confidence: If True, return confidence intervals.

    Returns:
    --------
    signif : array_like
        Significance levels for the wavelet power spectrum.
    outputs : dict
        Dictionary containing optional output parameters::

            'Cdelta': Reconstruction factor
            'period': Vector of Fourier periods corresponding to scales
            'fft_theor': Theoretical red-noise spectrum as function of period
            'Savg': Scale average (for sigtest=2 only)
            'Smid': Scale midpoint (for sigtest=2 only)
    """

    # Default parameters
    lag1 = kwargs.get("lag1", 0.0)
    siglvl = kwargs.get("siglvl", 0.95)
    mother = kwargs.get("mother", "MORLET")
    param = kwargs.get("param", -1)
    dof = kwargs.get("dof", None)
    gws = kwargs.get("gws", None)
    confidence = kwargs.get("confidence", False)

    # Calculate variance of the input time series
    if np.isscalar(Y):
        variance = Y  # If Y is a scalar, assume it's the variance
    else:
        variance = np.var(Y, ddof=0)  # Use population variance like IDL MOMENT

    # Get scale parameters
    J = len(scale) - 1
    s0 = np.min(scale)
    if len(scale) > 1:
        dj = np.log(scale[1] / scale[0]) / np.log(2)
    else:
        dj = 0.25  # Default value

    # Fourier factor and empirical values for the chosen wavelet
    if mother.upper() == "MORLET":
        k0 = 6.0 if param == -1 else param
        fourier_factor = (4 * np.pi) / (k0 + np.sqrt(2 + k0**2))
        empir = [2.0, -1, -1, -1]
        if k0 == 6:
            empir[1:4] = [0.776, 2.32, 0.60]
    elif mother.upper() == "PAUL":
        m = 4 if param == -1 else param
        fourier_factor = 4 * np.pi / (2 * m + 1)
        empir = [2.0, -1, -1, -1]
        if m == 4:
            empir[1:4] = [1.132, 1.17, 1.5]
    elif mother.upper() == "DOG":
        m = 2 if param == -1 else param
        fourier_factor = 2 * np.pi * np.sqrt(2.0 / (2 * m + 1))
        empir = [1.0, -1, -1, -1]
        if m == 2:
            empir[1:4] = [3.541, 1.43, 1.4]
        elif m == 6:
            empir[1:4] = [1.966, 1.37, 0.97]
    else:
        raise ValueError(f"Unsupported mother wavelet: {mother}")

    # Equivalent Fourier period
    period = scale * fourier_factor

    # Empirical constants
    dofmin = empir[0]  # Minimum degrees of freedom
    Cdelta = empir[1]  # Reconstruction factor
    gamma = empir[2]  # Time-decorrelation factor
    dj0 = empir[3]  # Scale-decorrelation factor

    # Compute the red-noise spectrum [Eqn(16)]
    freq = dt / period  # normalized frequency
    fft_theor = (1 - lag1**2) / (1 - 2 * lag1 * np.cos(freq * 2 * np.pi) + lag1**2)
    fft_theor = variance * fft_theor  # include time-series variance

    # Use global wavelet spectrum if provided
    if gws is not None and len(gws) == len(scale):
        fft_theor = gws

    signif = fft_theor.copy()

    # Initialize output dictionary
    outputs = {
        "Cdelta": Cdelta,
        "period": period,
        "fft_theor": fft_theor,
        "Savg": None,
        "Smid": None,
    }

    # Significance levels [Sec.4]
    if sigtest == 0:  # Local significance (no smoothing) [Eqn(18)]
        dof_local = dofmin
        signif = fft_theor * chi2.ppf(siglvl, dof_local) / dof_local
        if confidence:
            sig = (1.0 - siglvl) / 2.0
            chisqr = dof_local / np.array(
                [chi2.ppf(sig, dof_local), chi2.ppf(1.0 - sig, dof_local)]
            )
            signif = fft_theor[:, None] * chisqr

    elif sigtest == 1:  # Global significance (time-averaged) [Sec.5a]
        if gamma == -1:
            raise ValueError(
                f"Gamma (decorrelation factor) not defined for {mother} with param={param}"
            )

        if dof is None:
            dof_local = np.full(J + 1, dofmin)
        else:
            if np.isscalar(dof):
                dof_local = np.full(J + 1, dof)
            else:
                dof_local = np.array(dof)

        dof_local = np.maximum(dof_local, 1)
        dof_local = dofmin * np.sqrt(
            1 + (dof_local * dt / gamma / scale) ** 2
        )  # [Eqn(23)]
        dof_local = np.maximum(dof_local, dofmin)  # minimum DOF is dofmin

        if not confidence:
            signif = np.zeros_like(fft_theor)
            for i in range(J + 1):
                chisqr = chi2.ppf(siglvl, dof_local[i]) / dof_local[i]
                signif[i] = fft_theor[i] * chisqr
        else:
            signif = np.zeros((J + 1, 2))
            sig = (1.0 - siglvl) / 2.0
            for i in range(J + 1):
                chisqr = dof_local[i] / np.array(
                    [chi2.ppf(sig, dof_local[i]), chi2.ppf(1.0 - sig, dof_local[i])]
                )
                signif[i, :] = fft_theor[i] * chisqr

    elif sigtest == 2:  # Scale-average significance [Sec.5b]
        if dof is None or len(dof) != 2:
            raise ValueError("DOF must be set to [S1,S2], the range of scale-averages")
        if Cdelta == -1:
            raise ValueError(
                f"Cdelta & dj0 not defined for {mother} with param={param}"
            )

        s1, s2 = dof
        avg_idx = np.where((scale >= s1) & (scale <= s2))[0]
        if len(avg_idx) < 1:
            raise ValueError(f"No valid scales between {s1} and {s2}")

        s1 = np.min(scale[avg_idx])
        s2 = np.max(scale[avg_idx])
        Savg = 1.0 / np.sum(1.0 / scale[avg_idx])  # [Eqn(25)]
        Smid = np.exp((np.log(s1) + np.log(s2)) / 2.0)  # power-of-two midpoint
        navg = len(avg_idx)
        dof_eff = (dofmin * navg * Savg / Smid) * np.sqrt(
            1 + (navg * dj / dj0) ** 2
        )  # [Eqn(28)]
        fft_theor_avg = Savg * np.sum(fft_theor[avg_idx] / scale[avg_idx])  # [Eqn(27)]
        chisqr = chi2.ppf(siglvl, dof_eff) / dof_eff

        # Store scale-average outputs
        outputs["Savg"] = Savg
        outputs["Smid"] = Smid

        if confidence:
            sig = (1.0 - siglvl) / 2.0
            chisqr = dof_eff / np.array(
                [chi2.ppf(sig, dof_eff), chi2.ppf(1.0 - sig, dof_eff)]
            )

        signif = (dj * dt / Cdelta / Savg) * fft_theor_avg * chisqr  # [Eqn(26)]

    else:
        raise ValueError(f"Unsupported sigtest value: {sigtest}")

    return signif, outputs
