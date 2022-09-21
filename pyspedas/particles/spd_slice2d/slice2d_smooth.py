import logging
import numpy as np
import scipy.signal as signal


def slice2d_smooth(the_slice, width):
    """
    Smooths the output data by applying a gaussian blur.
    """

    smooth = np.round(width)

    if smooth >= 2:
        # ensure kernel with odd # of elements in [3:slice resolution]
        if smooth > 3:
            n = smooth

        if the_slice['data'].shape[0] < 3:
            n = the_slice['data'].shape[0]

        if n % 2 == 0:
            n = n - 1

        # Increase the STDV with the smoothing width to allow convolve2d to
        # effectively smooth over a greater area. Simply extending the
        # width with constant STDV adds negligable terms to the kernel.
        # Allowing the STDV to grow too quickly results in flat distributions.
        c = np.log(n) - 0.25  # There's no simple solution for c = f(n) for small n
                              # so this was partly arrived at empirically. It
                              # should allow the width of the gaussian to increase
                              # with the smoothing window without becoming flat
                              # (too quick) or adding negligible terms (to slow).

        # set up the kernel
        s = np.arange(0, n) - np.floor(n/2.0)
        ones = np.ones(n)
        sx = np.outer(s, ones)
        sy = np.outer(s, ones).T

        # 2D normalized gaussian kernel
        kernel = np.exp((-0.5)*((sx/c)**2 + (sy/c)**2))
        kernel = kernel / np.nansum(kernel)

        the_slice['data'] = signal.convolve2d(the_slice['data'], kernel, mode='same')
    else:
        logging.error('Smoothing not applied. Smoothing value must be >= 2')

    return the_slice
