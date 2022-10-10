"""
Perform polarisation analysis of three orthogonal component time series data.

Assumes data are in righthanded fieldaligned coordinate system
with Z pointing the direction of the ambient magnetic field.

The program outputs five spectral results derived from the
fourier transform of the covariance matrix (spectral matrix).

Similar to wavpol.pro in SPEDAS.

Notes:
-----
The program outputs five spectral results derived from the
  fourier transform of the covariance matrix (spectral matrix)

These are follows:

1. Wave power: On a linear scale
    (units of nT^2/Hz if input Bx, By, Bz are in nT)

2. Degree of Polarisation:
    This is similar to a measure of coherency between the input
    signals, however unlike coherency it is invariant under
    coordinate transformation and can detect pure state waves
    which may exist in one channel only.100% indicates a pure
    state wave. Less than 70% indicates noise. For more
    information see J. C. Samson and J. V. Olson 'Some comments
    on the description of the polarization states
    of waves' Geophys. J. R. Astr. Soc. (1980) v61 115-130

3. Wavenormal Angle:
    The angle between the direction of minimum variance
    calculated from the complex off diagonal elements of the
    spectral matrix and the Z direction of the input ac field data.
    for magnetic field data in field aligned coordinates this is the
    wavenormal angle assuming a plane wave. See:
    Means, J. D. (1972), Use of the three-dimensional covariance
    matrix in analyzing the polarization properties of plane waves,
    J. Geophys. Res., 77(28), 5551-5559, doi:10.1029/JA077i028p05551.

4. Ellipticity:
    The ratio (minor axis)/(major axis) of the ellipse transcribed
    by the field variations of the components transverse to the
    Z direction (Samson and Olson, 1980). The sign indicates
    the direction of rotation of the field vector in the plane (cf.
    Means, (1972)).
    Negative signs refer to left-handed rotation about the Z
    direction. In the field aligned coordinate system these signs
    refer to plasma waves of left and right handed polarization.

5. Helicity:
    Similar to Ellipticity except defined in terms of the
    direction of minimum variance instead of Z. Stricltly the Helicity
    is defined in terms of the wavenormal direction or k.
    However since from single point observations the
    sense of k cannot be determined,  helicity here is
    simply the ratio of the minor to major axis transverse to the
    minimum variance direction without sign.

Restrictions:
    If one component is an order of magnitude or more  greater than
    the other two then the polarisation results saturate and erroneously
    indicate high degrees of polarisation at all times and
    frequencies. Time series should be eyeballed before running the program.
    For time series containing very rapid changes or spikes
    the usual problems with Fourier analysis arise.
    Care should be taken in evaluating degree of polarisation results.
    For meaningful results there should be significant wave power at the
    frequency where the polarisation approaches
    100%. Remembercomparing two straight lines yields 100% polarisation.

"""
import logging
import warnings
import numpy as np
from pytplot import get_data, store_data, options
from pyspedas import tnames

# these routines require numpy v1.20.0 or later
if np.__version__ < '1.20':
    logging.error('Error: numpy 1.20.0 or later is required for wave polarization calculations. ')
    logging.error('Please update numpy with: pip install numpy --upgrade')
    breakpoint()


def atan2c(zx, zy):
    """Define arctan2 with complex numbers."""
    if np.isreal(zx) and np.isreal(zy):
        res = np.arctan2(zx, zy)
    else:
        res = -1j * np.log((zx + 1j*zy)/np.sqrt(zx**2 + zy**2))
    return res


def wpol_ematspec(i1, i2, i3, i4, aa, nosmbins, matspec):
    """Calculate ematspec array."""
    id0 = (i2 - int((nosmbins-1)/2))
    id1 = (i2 + int((nosmbins-1)/2)) + 1
    res = np.sum(aa[0:nosmbins] * matspec[i1, id0:id1, i3, i4])
    return res


def wpol_matsqrd(i1, i2, i3, ematspec):
    """Calculate matsqrd array."""
    res = (ematspec[i1, :, i2, 0] * ematspec[i1, :, 0, i3] +
           ematspec[i1, :, i2, 1] * ematspec[i1, :, 1, i3] +
           ematspec[i1, :, i2, 2] * ematspec[i1, :, 2, i3])
    return res


def wpol_helicity(nosteps, nopfft, KK, ematspec, waveangle):
    """Calculate helicity, ellipticity."""
    # Avoid warnings.
    warnings.simplefilter("ignore", np.ComplexWarning)

    # Define arrays.
    helicity = np.empty((nosteps, int(nopfft/2), 3))
    ellip = np.empty((nosteps, int(nopfft/2), 3))
    alphax = np.empty((nosteps, int(nopfft/2)))
    alphasin2x = np.empty((nosteps, int(nopfft/2)))
    alphacos2x = np.empty((nosteps, int(nopfft/2)))
    alphasin3x = np.empty((nosteps, int(nopfft/2)))
    alphacos3x = np.empty((nosteps, int(nopfft/2)))
    alphay = np.empty((nosteps, int(nopfft/2)))
    alphasin2y = np.empty((nosteps, int(nopfft/2)))
    alphacos2y = np.empty((nosteps, int(nopfft/2)))
    alphasin3y = np.empty((nosteps, int(nopfft/2)))
    alphacos3y = np.empty((nosteps, int(nopfft/2)))
    alphaz = np.empty((nosteps, int(nopfft/2)))
    alphasin2z = np.empty((nosteps, int(nopfft/2)))
    alphacos2z = np.empty((nosteps, int(nopfft/2)))
    alphasin3z = np.empty((nosteps, int(nopfft/2)))
    alphacos3z = np.empty((nosteps, int(nopfft/2)))
    lambdau = np.empty((nosteps, int(nopfft/2), 3, 3), dtype=complex)
    lambday = np.empty((nosteps, int(nopfft/2), 3, 3), dtype=complex)
    lambdaurot = np.empty((nosteps, int(nopfft/2), 2), dtype=complex)

    alphax[KK, :] = np.sqrt(ematspec[KK, :, 0, 0])
    alphacos2x[KK, :] = (np.real(ematspec[KK, :, 0, 1]) /
                         np.sqrt(ematspec[KK, :, 0, 0]))
    alphasin2x[KK, :] = (-np.imag(ematspec[KK, :, 0, 1]) /
                         np.sqrt(ematspec[KK, :, 0, 0]))
    alphacos3x[KK, :] = (np.real(ematspec[KK, :, 0, 2]) /
                         np.sqrt(ematspec[KK, :, 0, 0]))
    alphasin3x[KK, :] = (-np.imag(ematspec[KK, :, 0, 2]) /
                         np.sqrt(ematspec[KK, :, 0, 0]))
    lambdau[KK, :, 0, 0] = alphax[KK, :]
    lambdau[KK, :, 0, 1] = (alphacos2x[KK, :] +
                            1j * alphasin2x[KK, :])
    lambdau[KK, :, 0, 2] = (alphacos3x[KK, :] +
                            1j * alphasin3x[KK, :])

    alphay[KK, :] = np.sqrt(ematspec[KK, :, 1, 1])
    alphacos2y[KK, :] = (np.real(ematspec[KK, :, 1, 0]) /
                         np.sqrt(ematspec[KK, :, 1, 1]))
    alphasin2y[KK, :] = (-np.imag(ematspec[KK, :, 1, 0]) /
                         np.sqrt(ematspec[KK, :, 1, 1]))
    alphacos3y[KK, :] = (np.real(ematspec[KK, :, 1, 2]) /
                         np.sqrt(ematspec[KK, :, 1, 1]))
    alphasin3y[KK, :] = (-np.imag(ematspec[KK, :, 1, 2]) /
                         np.sqrt(ematspec[KK, :, 1, 1]))
    lambdau[KK, :, 1, 0] = alphay[KK, :]
    lambdau[KK, :, 1, 1] = (alphacos2y[KK, :] +
                            1j * alphasin2y[KK, :])
    lambdau[KK, :, 1, 2] = (alphacos3y[KK, :] +
                            1j * alphasin3y[KK, :])

    alphaz[KK, :] = np.sqrt(ematspec[KK, :, 2, 2])
    alphacos2z[KK, :] = (np.real(ematspec[KK, :, 2, 0]) /
                         np.sqrt(ematspec[KK, :, 2, 2]))
    alphasin2z[KK, :] = (-np.imag(ematspec[KK, :, 2, 0]) /
                         np.sqrt(ematspec[KK, :, 2, 2]))
    alphacos3z[KK, :] = (np.real(ematspec[KK, :, 2, 1]) /
                         np.sqrt(ematspec[KK, :, 2, 2]))
    alphasin3z[KK, :] = (-np.imag(ematspec[KK, :, 2, 1]) /
                         np.sqrt(ematspec[KK, :, 2, 2]))
    lambdau[KK, :, 2, 0] = alphaz[KK, :]
    lambdau[KK, :, 2, 1] = (alphacos2z[KK, :] +
                            1j * alphasin2z[KK, :])
    lambdau[KK, :, 2, 2] = (alphacos3z[KK, :] +
                            1j * alphasin3z[KK, :])

    for k in range(int(nopfft/2)):
        for k1 in range(3):
            upper = np.sum(2*np.real(lambdau[KK, k, k1, 0:3]) *
                           np.imag(lambdau[KK, k, k1, 0:3]))
            la2 = np.imag(lambdau[KK, k, k1, 0:3])**2
            lower = np.sum(np.real(lambdau[KK, k, k1, 0:3])**2 - la2)
            gammay = np.nan
            if np.isfinite(upper) and np.isfinite(lower):
                if upper > 0.0:
                    gammay = atan2c(upper, lower)
                else:
                    gammay = (2*np.pi + atan2c(upper, lower))
            lambday[KK, k, k1, :] = (np.exp((0.0 - 1j*0.5*gammay)) *
                                     lambdau[KK, k, k1, :])
            lay2 = np.imag(lambday[KK, k, k1, 0:3])**2
            helicity[KK, k, k1] = (1 /
                                   (np.sqrt(np.real(lambday[KK, k, k1, 0])**2 +
                                    np.real(lambday[KK, k, k1, 1])**2 +
                                    np.real(lambday[KK, k, k1, 2])**2) /
                                    np.sqrt(np.sum(lay2))))
            uppere = (np.imag(lambday[KK, k, k1, 0]) *
                      np.real(lambday[KK, k, k1, 0]) +
                      np.imag(lambday[KK, k, k1, 1]) *
                      np.real(lambday[KK, k, k1, 1]))
            lowere = (-np.imag(lambday[KK, k, k1, 0])**2 +
                      np.real(lambday[KK, k, k1, 0])**2 -
                      np.imag(lambday[KK, k, k1, 1])**2 +
                      np.real(lambday[KK, k, k1, 1])**2)
            gammarot = np.nan
            if np.isfinite(uppere) and np.isfinite(lowere):
                if uppere > 0.0:
                    gammarot = atan2c(uppere, lowere)
                else:
                    gammarot = 2*np.pi + atan2c(uppere, lowere)

            lam = lambday[KK, k, k1, 0:2]
            lambdaurot[KK, k, :] = np.exp(0 - 1j*0.5*gammarot) * lam[:]

            ellip[KK, k, k1] = (np.sqrt(np.imag(lambdaurot[KK, k, 0])**2 +
                                        np.imag(lambdaurot[KK, k, 1])**2) /
                                np.sqrt(np.real(lambdaurot[KK, k, 0])**2 +
                                        np.real(lambdaurot[KK, k, 1])**2))
            ellip[KK, k, k1] = (-ellip[KK, k, k1] *
                                (np.imag(ematspec[KK, k, 0, 1]) *
                                 np.sin(waveangle[KK, k])) /
                                np.abs(np.imag(ematspec[KK, k, 0, 1]) *
                                       np.sin(waveangle[KK, k])))

    # Average over helicity and ellipticity results.
    elliptict0 = (ellip[KK, :, 0]+ellip[KK, :, 1]+ellip[KK, :, 2])/3
    helict0 = (helicity[KK, :, 0]+helicity[KK, :, 1]+helicity[KK, :, 2])/3

    return (helict0, elliptict0)


def wavpol(ct, bx, by, bz,
           nopfft=256,
           steplength=-1,
           bin_freq=3):
    """
    Perform polarisation analysis of Bx, By, Bz time series data.

    Parameters
    ----------
    ct : list of float
        Time.
    b1 : list of float
        Bx field.
    b2 : list of float
        By field.
    b3 : list of float
        Bz field.
    nopfft : int, optional
        Number of points in FFT. The default is 256.
    steplength : int, optional
        The amount of overlap between successive FFT intervals.
        The default is -1 which means nopfft/2.
    bin_freq : int, optional
        Number of bins in frequency domain. The default is 3.

    Returns
    -------
    result: tuple with 9 items

    timeline : list of float
        Times.
    freqline : list of float
        Frequencies.
    powspec : 2-dim array of float
        Wave power.
    degpol : 2-dim array of float
        Degree of Polarisation.
    waveangle : 2-dim array of float
        Wavenormal Angle.
    elliptict : 2-dim array of float
        Ellipticity.
    helict : 2-dim array of float
        Helicity.
    pspec3 : 3-dim array of float
        Power spectra.
    err_flag : bool
        Error flag. The default is 0.
        Returns 1 if there are large number of batches and aborts.

    """
    # Default values.
    if nopfft < 0:
        nopfft = 256
    if steplength < 0:
        steplength = nopfft / 2
    if bin_freq < 0:
        bin_freq = 3

    # Convert to numpy arrays.
    ct = np.array(ct, np.float64)
    bx = np.array(bx, np.float64)
    by = np.array(by, np.float64)
    bz = np.array(bz, np.float64)

    # Define empty returns.
    timeline = ''
    freqline = ''
    powspec = ''
    degpol = ''
    waveangle = ''
    elliptict = ''
    helict = ''
    pspec3 = ''
    err_flag = 0

    # Define variables.
    nopoints = len(bx)
    iano = np.zeros(nopoints, dtype=int)
    dt = [ct[i+1]-ct[i] for i in range(len(ct)-1)]  # time difference
    beginsampfreq = 1./(ct[1]-ct[0])
    endsampfreq = 1./(ct[nopoints-1]-ct[nopoints-2])

    if beginsampfreq != endsampfreq:
        logging.warning('wavpol Warning: file sampling frequency changes from ' + str(beginsampfreq) + 'Hz to ' + str(endsampfreq) + 'Hz')
    else:
        logging.warning('wavpol: File sampling frequency=' + str(beginsampfreq) + 'Hz')

    samp_freq = beginsampfreq
    samp_per = 1./samp_freq

    # Time reversal detection.
    for i in range(len(dt)-1):
        if dt[i] < 0:
            iano[i] = 16

    # The accuracy of the sampling frequency should be about 1%
    accuracy = 0.01

    # Find discontinuities.
    discont_trigger = accuracy*samp_per
    for i in range(nopoints-1):
        if abs(dt[i]-1./samp_freq) > discont_trigger:
            iano[i] = 17
    iano[nopoints-1] = 22

    # Count batches, should be less than 80,000
    n_batches = 0
    errs = []
    for i in range(nopoints):
        if iano[i] >= 15:
            n_batches += 1
            errs.append(i)

    # If there are too many batches, return.
    if n_batches > 80000.0:
        logging.error("wavpol error: Large number of batches. " +
              "Returning to avoid memory runaway.")
        err_flag = 1
        result = (timeline, freqline, powspec, degpol, waveangle,
                  elliptict, helict, pspec3, err_flag)
        return result

    nbp_fft_batches = [0] * n_batches
    # Total numbers of FFT calculations including 1 leap frog for each batch
    ind_batch0 = 0
    nosteps = 0
    logging.info('n_batches: ' + str(n_batches))

    for i in range(n_batches):
        nosteps = int(nosteps + np.floor((errs[i] - ind_batch0)/steplength))
        ind_batch0 = errs[i]

    nosteps = nosteps + n_batches
    logging.info('Total number of steps:' + str(nosteps))

    # leveltplot = 0.000001  # Power rejection level 0 to 1
    nosmbins = bin_freq  # No. of bins in frequency domain
    # Smoothing profile based on Hanning:
    aa = np.array([0.024, 0.093, 0.232, 0.301, 0.232, 0.093, 0.024])

    ind0 = 0
    KK = 0

    # Create empty arrays
    specx = np.empty((nosteps, nopfft), dtype=complex)
    specy = np.empty((nosteps, nopfft), dtype=complex)
    specz = np.empty((nosteps, nopfft), dtype=complex)
    halfspecx = np.empty((nosteps, int(nopfft/2)), dtype=complex)
    halfspecy = np.empty((nosteps, int(nopfft/2)), dtype=complex)
    halfspecz = np.empty((nosteps, int(nopfft/2)), dtype=complex)
    matspec = np.empty((nosteps, int(nopfft/2), 3, 3), dtype=complex)
    ematspec = np.empty((nosteps, int(nopfft/2), 3, 3), dtype=complex)
    aaa2 = np.empty((nosteps, int(nopfft/2)))
    wnx = np.empty((nosteps, int(nopfft/2)))
    wny = np.empty((nosteps, int(nopfft/2)))
    wnz = np.empty((nosteps, int(nopfft/2)))
    waveangle = np.empty((nosteps, int(nopfft/2)))
    matsqrd = np.empty((nosteps, int(nopfft/2), 3, 3), dtype=complex)
    trmatsqrd = np.empty((nosteps, int(nopfft/2)))
    trmatspec = np.empty((nosteps, int(nopfft/2)))
    degpol = np.empty((nosteps, int(nopfft/2)))
    xrmatspec = np.empty((nosteps, int(nopfft/2)))
    yrmatspec = np.empty((nosteps, int(nopfft/2)))
    zrmatspec = np.empty((nosteps, int(nopfft/2)))

    # Return arrays.
    timeline = np.empty((nosteps))
    freqline = ''
    helict = np.empty((nosteps, int(nopfft/2)))
    elliptict = np.empty((nosteps, int(nopfft/2)))
    powspec = np.empty((nosteps, int(nopfft/2)))
    pspecx = np.empty((nosteps, int(nopfft/2)))
    pspecy = np.empty((nosteps, int(nopfft/2)))
    pspecz = np.empty((nosteps, int(nopfft/2)))
    pspec3 = np.empty((nosteps, int(nopfft/2), 3))

    for batch in range(n_batches):
        ind1 = errs[batch]+1
        # nbp_batch = ind1-ind0+1
        ind1_ref = ind1
        KK_batch_start = KK

        xs = np.array(bx[ind0:ind1])
        ys = np.array(by[ind0:ind1])
        zs = np.array(bz[ind0:ind1])

        ngood = np.count_nonzero(~np.isnan(xs))  # Count finite data.
        if ngood > nopfft:
            nbp_fft_batches[batch] = np.floor(ngood/steplength)
            logging.info('Total number of possible FFT in the batch no ' + str(batch) + ' is:' + str(nbp_fft_batches[batch]))
            ind0_fft = 0
            for j in range(int(nbp_fft_batches[batch])):
                # ind1_fft = nopfft * (j+1)-1
                # ind1_ref_fft = ind1_fft

                # FFT Calculation.
                smooth = 0.08 + 0.46 * (1 - np.cos(2 * np.pi *
                                                   np.arange(nopfft) / nopfft))
                tempx = smooth * xs[0:nopfft]
                tempy = smooth * ys[0:nopfft]
                tempz = smooth * zs[0:nopfft]

                # previous version (prior to 15Dec2021)
                # specx[KK, :] = np.fft.fft(tempx, norm='forward')
                # specy[KK, :] = np.fft.fft(tempy, norm='forward')
                # specz[KK, :] = np.fft.fft(tempz, norm='forward')

                # mask out the NaNs
                temp_i = np.arange(len(tempx))
                tempx_mask = np.isfinite(tempx)
                tempx_filtered = np.interp(temp_i, temp_i[tempx_mask], tempx[tempx_mask])
                tempy_mask = np.isfinite(tempy)
                tempy_filtered = np.interp(temp_i, temp_i[tempy_mask], tempy[tempy_mask])
                tempz_mask = np.isfinite(tempz)
                tempz_filtered = np.interp(temp_i, temp_i[tempz_mask], tempz[tempz_mask])

                # back to forward option, 23June2022, after applying mask for NaNs above
                # forward seems to be the only option that works now after the NaN mask
                # is applied; this requires numpy >= 1.20.0
                specx[KK, :] = np.fft.fft(tempx_filtered, norm='forward')
                specy[KK, :] = np.fft.fft(tempy_filtered, norm='forward')
                specz[KK, :] = np.fft.fft(tempz_filtered, norm='forward')

                halfspecx[KK, :] = specx[KK, 0:int(nopfft/2)]
                halfspecy[KK, :] = specy[KK, 0:int(nopfft/2)]
                halfspecz[KK, :] = specz[KK, 0:int(nopfft/2)]
                xs = np.roll(xs, -int(steplength))
                ys = np.roll(ys, -int(steplength))
                zs = np.roll(zs, -int(steplength))

                # Calculation of the spectral matrix.
                matspec[KK, :, 0, 0] = (halfspecx[KK, :] *
                                        np.conjugate(halfspecx[KK, :]))
                matspec[KK, :, 1, 0] = (halfspecx[KK, :] *
                                        np.conjugate(halfspecy[KK, :]))
                matspec[KK, :, 2, 0] = (halfspecx[KK, :] *
                                        np.conjugate(halfspecz[KK, :]))
                matspec[KK, :, 0, 1] = (halfspecy[KK, :] *
                                        np.conjugate(halfspecx[KK, :]))
                matspec[KK, :, 1, 1] = (halfspecy[KK, :] *
                                        np.conjugate(halfspecy[KK, :]))
                matspec[KK, :, 2, 1] = (halfspecy[KK, :] *
                                        np.conjugate(halfspecz[KK, :]))
                matspec[KK, :, 0, 2] = (halfspecz[KK, :] *
                                        np.conjugate(halfspecx[KK, :]))
                matspec[KK, :, 1, 2] = (halfspecz[KK, :] *
                                        np.conjugate(halfspecy[KK, :]))
                matspec[KK, :, 2, 2] = (halfspecz[KK, :] *
                                        np.conjugate(halfspecz[KK, :]))

                # Calculation of smoothed spectral matrix.
                for k in range(int((nosmbins-1)/2),
                               int((nopfft/2-1)-(nosmbins-1)/2)+1):
                    for k2 in range(0, 3):
                        for k1 in range(0, 3):
                            ematspec[KK, k, k1, k2] = wpol_ematspec(KK, k, k1,
                                                                    k2, aa,
                                                                    nosmbins,
                                                                    matspec)

                # Calculation of the minimum variance direction
                # and wavenormal angle.
                aaa2[KK, :] = np.sqrt(np.imag(ematspec[KK, :, 0, 1])**2 +
                                      np.imag(ematspec[KK, :, 0, 2])**2 +
                                      np.imag(ematspec[KK, :, 1, 2])**2)
                # Avoid warnings due to NaN values.
                np.seterr(divide='ignore', invalid='ignore')
                wnx[KK, :] = np.abs(np.imag(ematspec[KK, :, 1, 2]) /
                                    aaa2[KK, :])
                wny[KK, :] = -np.abs(np.imag(ematspec[KK, :, 0, 2]) /
                                     aaa2[KK, :])
                wnz[KK, :] = (np.imag(ematspec[KK, :, 0, 1]) / aaa2[KK, :])
                waveangle[KK, :] = np.arctan2(np.sqrt(wnx[KK, :]**2 +
                                                      wny[KK, :]**2),
                                              np.abs(wnz[KK, :]))

                # Calculation of the degree of polarization.
                # Calculation of square of smoothed spec matrix.
                for k1 in range(3):
                    for k2 in range(3):
                        matsqrd[KK, :, k1, k2] = wpol_matsqrd(KK, k1, k2,
                                                              ematspec)

                trmatsqrd[KK, :] = np.real(matsqrd[KK, :, 0, 0] +
                                           matsqrd[KK, :, 1, 1] +
                                           matsqrd[KK, :, 2, 2])
                trmatspec[KK, :] = np.real(ematspec[KK, :, 0, 0] +
                                           ematspec[KK, :, 1, 1] +
                                           ematspec[KK, :, 2, 2])
                id1 = int((nosmbins-1)/2)
                id2 = int((nopfft/2-1)-(nosmbins-1)/2) + 1
                degpol[KK, id1:id2] = ((3 * trmatsqrd[KK, id1:id2] -
                                        trmatspec[KK, id1:id2]**2) /
                                       (2 * trmatspec[KK, id1:id2]**2))

                xrmatspec[KK, :] = np.real(ematspec[KK, :, 0, 0])
                yrmatspec[KK, :] = np.real(ematspec[KK, :, 1, 1])
                zrmatspec[KK, :] = np.real(ematspec[KK, :, 2, 2])

                # Calculation of helicity, ellipticity
                # and the wave state vector
                (helict[KK], elliptict[KK]) = wpol_helicity(nosteps,
                                                            nopfft,
                                                            KK,
                                                            ematspec,
                                                            waveangle)

                # Scaling power results to units with meaning
                binwidth = samp_freq / nopfft
                W = np.sum(smooth**2) / np.real(nopfft)
                id2 = int(nopfft/2-1)
                powspec[KK, 1:id2] = 1./W*2*trmatspec[KK, 1:id2]/binwidth
                powspec[KK, 0] = 1./W * trmatspec[KK, 0]/binwidth
                powspec[KK, id2] = 1./W*trmatspec[KK, id2]/binwidth

                pspecx[KK, 1:id2] = 1./W*2*xrmatspec[KK, 1:id2]/binwidth
                pspecx[KK, 0] = 1./W*xrmatspec[KK, 0]/binwidth
                pspecx[KK, id2] = 1./W*xrmatspec[KK, id2]/binwidth

                pspecy[KK, 1:id2] = 1./W*2*yrmatspec[KK, 1:id2]/binwidth
                pspecy[KK, 0] = 1./W*yrmatspec[KK, 0]/binwidth
                pspecy[KK, id2] = 1./W*yrmatspec[KK, id2]/binwidth

                pspecz[KK, 1:id2] = 1./W*2*zrmatspec[KK, 1:id2]/binwidth
                pspecz[KK, 0] = 1./W*zrmatspec[KK, 0]/binwidth
                pspecz[KK, id2] = 1./W*zrmatspec[KK, id2]/binwidth

                pspec3[KK, :, 0] = pspecx[KK, :]
                pspec3[KK, :, 1] = pspecy[KK, :]
                pspec3[KK, :, 2] = pspecz[KK, :]

                ind0_fft = ind0_fft + steplength
                KK_batch_stop = KK

                # Print an indication that a computation is happening.
                if KK == 0 or KK % 40 == 0:
                    logging.info('wavpol step: ' + str(KK) + ' ')
                elif KK % 4 == 0:
                    print('.', end='')

                KK += 1
                # End loop "for j"

            ids = KK_batch_start
            idf = KK_batch_stop+1
            ta = np.arange(nbp_fft_batches[batch])
            timeline[ids:idf] = (ct[ind0] +
                                 np.abs(int(nopfft/2))/samp_freq +
                                 ta*steplength/samp_freq)
            if KK == len(timeline):
                continue

            timeline[idf] = (ct[ind0] +
                             np.abs(int(nopfft/2))/samp_freq +
                             (nbp_fft_batches[batch]+1)*steplength/samp_freq)
            KK += 1
            # End "if ngood > nopfft"
        else:
            binwidth = samp_freq/nopfft
            logging.error('Fourier Transform is not possible. ')
            logging.error('Ngood = ' + str(ngood))
            logging.error('Required number of points for FFT = ' + str(nopfft))

            timeline[KK] = (ct[ind0] +
                            np.abs(int(nopfft/2))/samp_freq +
                            steplength/samp_freq)
            powspec[KK, 0:int(nopfft/2)+1] = np.nan
            KK += 1
        ind0 = ind1_ref + 1
        # End "for batch in range(n_batches)"

    freqline = binwidth*np.arange(int(nopfft/2))

    # Make sure there aren't any missing data points at the end of the output.
    wherezero = np.argwhere(timeline == 0)
    if len(wherezero) > 0:
        timeline[wherezero] = np.nan
        powspec[wherezero, :] = np.nan
        pspecx[wherezero, :] = np.nan
        pspecy[wherezero, :] = np.nan
        pspecz[wherezero, :] = np.nan
        pspec3[wherezero, :, :] = np.nan
        elliptict[wherezero, :] = np.nan
        helict[wherezero, :] = np.nan

    # Returns results.
    result = (timeline, freqline, powspec, degpol, waveangle,
              elliptict, helict, pspec3, err_flag)
    logging.info('\nwavpol completed successfully')

    return result


def twavpol(tvarname, prefix='', nopfft=-1, steplength=-1, bin_freq=-1):
    """Apply wavpol to a pytplot variable.

    Creates multiple pytplot variables:
    '_powspec','_degpol', '_waveangle', '_elliptict', '_helict',
    '_pspec3_x', '_pspec3_y', '_pspec3_z'

    Parameters
    ----------
    tvarname : string
              Name of pytplot variable.
    prefix : string, optional
            Prefix for pytplot variables created.
    nopfft : int, optional
        Number of points in FFT. The default is 256.
    steplength : int, optional
        The amount of overlap between successive FFT intervals.
        The default is -1 which means nopfft/2.
    bin_freq : int, optional
        Number of bins in frequency domain. The default is 3.

    Returns
    -------
    result : bool
        Returns 1 if completed successfully.
        Returns 0 if it encountered problems and exited.
    """
    if prefix == '':
        prefix = tvarname

    all_names = tnames(tvarname)
    if len(all_names) < 1:
        logging.error('twavpol error: No valid pytplot variables match tvarname.')
        return 0

    xdata = get_data(tvarname)

    ct = xdata.times
    if len(ct) < 2:
        logging.error('twavpol error: Time variable does not have enough points.')
        return 0

    bfield = xdata.y
    if bfield.ndim != 2:
        logging.error('twavpol error: Data should have 2 dimensions.')
        return 0
    b1 = bfield[:, 0]
    b2 = bfield[:, 1]
    b3 = bfield[:, 2]
    if (len(ct) != len(b1) or len(ct) != len(b2) or len(ct) != len(b3)):
        logging.error('twavpol error: Number of time elements does not match' +
              'number of magnetic field elements.')
        return 0

    # Apply vawpol.
    (timeline, freqline, powspec, degpol, waveangle, elliptict,
     helict, pspec3, err_flag) = wavpol(ct, b1, b2, b3,
                                        nopfft=nopfft, steplength=steplength,
                                        bin_freq=bin_freq)

    if err_flag == 1:
        logging.error('twavpol error: There were errors while applying wavpol.')
        return 0

    # Store new pytplot variables as spectrograms.
    vt = prefix+'_powspec'
    store_data(vt, data={'x': timeline, 'y': powspec, 'v': freqline})
    options(vt, 'spec', 1)
    vt = prefix+'_degpol'
    store_data(vt, data={'x': timeline, 'y': degpol, 'v': freqline})
    options(vt, 'spec', 1)
    vt = prefix+'_waveangle'
    store_data(vt, data={'x': timeline, 'y': waveangle, 'v': freqline})
    options(vt, 'spec', 1)
    vt = prefix+'_elliptict'
    store_data(vt, data={'x': timeline, 'y': elliptict, 'v': freqline})
    options(vt, 'spec', 1)
    vt = prefix+'_helict'
    store_data(vt, data={'x': timeline, 'y': helict, 'v': freqline})
    options(vt, 'spec', 1)

    # Take the three components of pspec3.
    vt = prefix+'_pspec3_x'
    store_data(vt, data={'x': timeline, 'y': pspec3[:, :, 0], 'v': freqline})
    options(vt, 'spec', 1)
    vt = prefix+'_pspec3_y'
    store_data(vt, data={'x': timeline, 'y': pspec3[:, :, 1], 'v': freqline})
    options(vt, 'spec', 1)
    vt = prefix+'_pspec3_z'
    store_data(vt, data={'x': timeline, 'y': pspec3[:, :, 2], 'v': freqline})
    options(vt, 'spec', 1)

    return 1
