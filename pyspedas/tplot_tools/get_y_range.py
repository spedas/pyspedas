# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/PyTplot

import numpy as np

def get_y_range(dataset):
    # This takes the data and sets the minimum and maximum range of the data values.
    # If the data type later gets set to 'spec', then we'll change the ymin and ymax
    import warnings
    warnings.filterwarnings("ignore")

    # Special rule if 'spec' is True
    if 'spec' in dataset.attrs['plot_options']['extras']:
        if dataset.attrs['plot_options']['extras']['spec']:
            try:
                ymin = np.nanmin(dataset.coords['spec_bins'].values)
                ymax = np.nanmax(dataset.coords['spec_bins'].values)
                return [ymin, ymax]
            except Exception as e:
                #continue on to the code below
                pass

    dataset_temp = dataset.where(dataset != np.inf)
    dataset_temp = dataset_temp.where(dataset != -np.inf)
    try:
        y_min = np.nanmin(dataset_temp.values)
        y_max = np.nanmax(dataset_temp.values)
    except RuntimeWarning:
        y_min = np.nan
        y_max = np.nan

    # CDF files may have array of strings (e.g., RBSP EMFISIS)
    if isinstance(y_min, str):
        y_min = np.nan
        y_max = np.nan
        
    if y_min == y_max:
        # Show 10% and 10% below the straight line
        y_min = y_min - (.1 * np.abs(y_min))
        y_max = y_max + (.1 * np.abs(y_max))
    warnings.resetwarnings()
    return [y_min, y_max]

