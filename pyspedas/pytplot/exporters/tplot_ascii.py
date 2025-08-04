# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pytplot

def tplot_ascii(tvar, filename=None, extension='.csv'):
    # grab data, prepend index column
    if filename == None:
        filename = tvar
    # save data
    pytplot.data_quants[tvar].to_pandas().to_csv(filename + extension)
    # only try to save spec_bins (y-values in spectrograms) if we're sure they exist
    if 'spec_bins' in pytplot.data_quants[tvar].coords.keys():
        pytplot.data_quants[tvar].coords['spec_bins'].to_pandas().to_csv(filename + '_v' + extension)

