# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/Pytplot

import pyspedas

def tplot_ascii(tvar, filename=None, extension='.csv'):
    """
    Save a single tplot variable in CSV format.

    This routine converts the internal tplot data structure into a Pandas data frame, then uses
    the Pandas to_csv() function to save it in CSV format.

    If the tplot variable includes spectral bin metadata, it will be written to a separate file with
    a "_v" inserted after the filename and before the ".csv" suffix.

    Parameters
    ----------
        tvar: str
            tplot variable name
        filename: str
            Base filename to use.  If spec_bin data is present, it will be written to a separate file
            with "_v" appended to the base filename. The file extension suffix should not be included here (it will be added internally).
        extension: str
            File extension suffix to apply to the base filename.  Default: ".csv" (no other file formats
            are supported).

    Examples
    --------

    >>> import pyspedas
    >>> pyspedas.projects.themis.state(probe='a', trange=['2007-03-23', '2007-03-24'])
    >>> pyspedas.tplot_ascii('tha_pos',filename='themis_a_position')
    """

    # grab data, prepend index column
    if filename is None:
        filename = tvar
    # save data
    pyspedas.tplot_tools.data_quants[tvar].to_pandas().to_csv(filename + extension)
    # only try to save spec_bins (y-values in spectrograms) if we're sure they exist
    if 'spec_bins' in pyspedas.tplot_tools.data_quants[tvar].coords.keys():
        pyspedas.tplot_tools.data_quants[tvar].coords['spec_bins'].to_pandas().to_csv(filename + '_v' + extension)

