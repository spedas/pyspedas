# -*- coding: utf-8 -*-
"""
File:
    ex_line_spectra.py

Description:
    Basic example of plotting both a line and a spectrogram with THEMIS data.
    Downloads THEMIS data and creates a plot.

"""

import pyspedas
import pytplot


def ex_line_spectra():
    # Delete any existing pytplot variables
    pytplot.del_data()
    # Download THEMIS data for 2015-12-31
    pyspedas.load_data('themis', ['2015-12-31'], ['tha'], 'state', 'l1')
    pyspedas.load_data('themis', ['2015-12-31'], ['tha'], 'sst', 'l2')
    # Specify options
    pytplot.ylim('tha_pos', -23000.0, 81000.0)
    pytplot.ylim('tha_psif_en_eflux', 10000.0, 10000000.0)
    pytplot.options('tha_psif_en_eflux', 'colormap', 'viridis')
    pytplot.tplot_options('title', 'tha 2015-12-31')
    # Plot line and spectrogram
    pytplot.tplot(["tha_pos", 'tha_psif_en_eflux'])

# Run the example code
# ex_line_spectra()
