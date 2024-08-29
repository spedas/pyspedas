# Spherical Elementary Current Systems (SECS)

## EICS and SECS data

This module can load, read and plot EICS (Equivalent ionospheric currents) and SECS (Spherical Elementary Current Systems) data. 

It can plot the vector field and the contour map for a given time.

Data can be loaded either from the UCLA server or from SPDF. 

For more information, see:
https://sites.epss.ucla.edu/jweygand/eics_na_greenland-html-preview-equivalent-ionospheric-currents-over-north-america-and-greenland/

## Installation

This module requires the basemap toolkit, which may not be installed automatically. 

To install it, please use:

``
pip install basemap
``

For more information on basemap, see:
https://matplotlib.org/basemap/stable/users/installation.html


## Example
```python
# Save the following in a file (eg. eics_plots.py) and run it.
import pyspedas
from pyspedas.secs.makeplots import make_plots

if __name__ == "__main__":
    # Download and unzip the data files.
    dtype = "EICS"  # 'EICS or SECS'
    files_downloaded = pyspedas.secs.data(
        trange=["2012-04-05/02:15:35", "2012-04-06/02:15:35"],
        dtype=dtype,
        downloadonly=True,
    )

    # Read the data files and create the plots.
    dtime = "2012-04-05/09:12:00"  # set one single data point when plotting.
    make_plots(
        dtype=dtype,
        dtime=dtime,
        vplot_sized=True,
        contour_den=201,
        s_loc=False,
        quiver_scale=30,
    )
```