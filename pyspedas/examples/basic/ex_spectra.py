# -*- coding: utf-8 -*-
"""
File:
    ex_spectra.py

Description:
    Basic example of plotting a spectrogram with THEMIS data.

"""

import pyspedas
import pytplot


def ex_spectra():
    # Delete any existing pytplot variables
    pytplot.del_data()

    # Download THEMIS data for 2015-12-31
    pyspedas.load_data('themis', ['2015-12-31'], ['tha'], 'sst', 'l2')

    # Specify options
    pytplot.tplot_options('title', 'tha_psif_en_eflux 2015-12-31')
    pytplot.ylim('tha_psif_en_eflux', 10000.0, 10000000.0)
    pytplot.options('tha_psif_en_eflux', 'colormap', 'viridis')

    # Plot spectrogram
    pytplot.tplot(['tha_psif_en_eflux'])

    # Return 1 as indication that the example finished without problems.
    return 1

# Run the example code
# ex_spectra()
