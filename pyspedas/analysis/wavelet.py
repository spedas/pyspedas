"""
Apply a wavelet transformation to every component of a tplot variable.

Notes
-----
Similar to wav_data.pro in IDL SPEDAS.
For pywavelets library, see:
    https://pywavelets.readthedocs.io/en/latest/ref/cwt.html
For an example, see:
    http://spedas.org/wiki/index.php?title=Wavelet

"""
import numpy as np
import pywt
import pytplot


def wavelet(names, new_names=None, suffix='_pow', wavename='morl', scales=None,
            method='fft', sampling_period=1.0):
    """
    Find the wavelet transofrmation of a tplot variable.

    Parameters
    ----------
    names: str/list of str
        List of pytplot names.
    new_names: str/list of str, optional
        List of new_names for pytplot variables.
        If not given, then a suffix is applied.
    suffix: str, optional
        A suffix to apply. Default is '_pow'.
    wavename: str, optional
        The name of the continous wavelet function to apply.
        Examples: 'gaus1', 'morl', 'cmorlB-C'.
    scales: list of float, optional
        The wavelet scales to use.
    method: str, optional
        Either ‘fft’ for  frequency domain convolution,
        or 'conv' for numpy.convolve.
    sampling_period: float, optional
        The sampling period for the frequencies output.

    Returns
    -------
    A list of pytplot variables that contain the wavelet power.

    """
    varnames = pytplot.split_vec(names)
    powervar = []

    if len(varnames) < 1:
        print('wavelet error: No pytplot names were provided.')
        return

    if scales is None:
        scales = np.arange(1, 128)

    for i, old in enumerate(varnames):
        old = varnames[i]

        if (new_names is not None) and (len(new_names) == len(varnames)):
            new = new_names[i]
        else:
            new = old + suffix

        alldata = pytplot.get_data(old)
        time = alldata[0]
        len_time = len(time)
        data = alldata[1]

        if len_time < 2:
            print('wavelet error: Not enought data points for ' + old)
            continue

        coef, freqs = pywt.cwt(data, scales=scales, wavelet=wavename,
                               method=method, sampling_period=sampling_period)

        power = np.abs(coef)**2
        power = power.transpose()
        pytplot.store_data(new, data={'x': time, 'y': power, 'v': freqs})
        pytplot.options(new, 'spec', 1)
        powervar.append(new)

        print('wavelet was applied to: ' + new)

    return powervar
