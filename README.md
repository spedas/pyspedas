
# PySPEDAS
[![build](https://github.com/spedas/pyspedas/workflows/build/badge.svg)](https://github.com/spedas/pyspedas/actions)
[![Coverage Status](https://coveralls.io/repos/github/spedas/pyspedas/badge.svg)](https://coveralls.io/github/spedas/pyspedas)
[![Version](https://img.shields.io/pypi/v/pyspedas.svg)](https://pypi.org/project/pyspedas/)
![Status](https://img.shields.io/pypi/status/pyspedas.svg)
![License](https://img.shields.io/pypi/l/pyspedas.svg)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

The Python-based Space Physics Environment Data Analysis Software (PySPEDAS) framework supports multi-mission, multi-instrument retrieval, analysis, and visualization of heliophysics time series data.


## Projects Supported
- [Advanced Composition Explorer (ACE)](https://pyspedas.readthedocs.io/en/latest/ace.html)
- [Akebono](https://pyspedas.readthedocs.io/en/latest/akebono.html)
- [Arase (ERG)](https://pyspedas.readthedocs.io/en/latest/erg.html)
- [Cluster](https://pyspedas.readthedocs.io/en/latest/cluster.html)
- [Colorado Student Space Weather Experiment (CSSWE)](https://pyspedas.readthedocs.io/en/latest/csswe.html)
- [Communications/Navigation Outage Forecasting System (C/NOFS)](https://pyspedas.readthedocs.io/en/latest/cnofs.html)
- [Deep Space Climate Observatory (DSCOVR)](https://pyspedas.readthedocs.io/en/latest/dscovr.html)
- [Dynamics Explorer 2 (DE2)](https://pyspedas.readthedocs.io/en/latest/de2.html)
- [Equator-S](https://pyspedas.readthedocs.io/en/latest/equator-s.html)
- [Fast Auroral Snapshot Explorer (FAST)](https://pyspedas.readthedocs.io/en/latest/fast.html)
- [Geotail](https://pyspedas.readthedocs.io/en/latest/geotail.html)
- [Geostationary Operational Environmental Satellite (GOES)](https://pyspedas.readthedocs.io/en/latest/goes.html)
- [Imager for Magnetopause-to-Aurora Global Exploration (IMAGE)](https://pyspedas.readthedocs.io/en/latest/image.html)
- [Kyoto Dst Index](https://pyspedas.readthedocs.io/en/latest/kyoto.html)
- [LANL](https://pyspedas.readthedocs.io/en/latest/lanl.html)
- [Mars Atmosphere and Volatile Evolution (MAVEN)](https://pyspedas.readthedocs.io/en/latest/maven.html)
- [Magnetic Induction Coil Array (MICA)](https://pyspedas.readthedocs.io/en/latest/mica.html)
- [Magnetospheric Multiscale (MMS)](https://pyspedas.readthedocs.io/en/latest/mms.html)
- [OMNI](https://pyspedas.readthedocs.io/en/latest/omni.html)
- [Polar Orbiting Environmental Satellites (POES)](https://pyspedas.readthedocs.io/en/latest/poes.html)
- [Polar](https://pyspedas.readthedocs.io/en/latest/polar.html)
- [Parker Solar Probe (PSP)](https://pyspedas.readthedocs.io/en/latest/psp.html)
- [Solar & Heliospheric Observatory (SOHO)](https://pyspedas.readthedocs.io/en/latest/soho.html)
- [Solar Orbiter (SOLO)](https://pyspedas.readthedocs.io/en/latest/solo.html)
- [Solar Terrestrial Relations Observatory (STEREO)](https://pyspedas.readthedocs.io/en/latest/stereo.html)
- [Space Technology 5 (ST5)](https://pyspedas.readthedocs.io/en/latest/st5.html)
- [Spherical Elementary Currents (SECS)](https://github.com/spedas/pyspedas/blob/master/pyspedas/secs/README.md)
- [Swarm](https://github.com/spedas/pyspedas/blob/master/pyspedas/swarm/README.md)
- [Time History of Events and Macroscale Interactions during Substorms (THEMIS)](https://pyspedas.readthedocs.io/en/latest/themis.html)
- [Two Wide-Angle Imaging Neutral-Atom Spectrometers (TWINS)](https://pyspedas.readthedocs.io/en/latest/twins.html)
- [Ulysses](https://pyspedas.readthedocs.io/en/latest/ulysses.html)
- [Van Allen Probes (RBSP)](https://pyspedas.readthedocs.io/en/latest/rbsp.html)
- [Wind](https://pyspedas.readthedocs.io/en/latest/wind.html)


## Requirements

Python 3.9+ is required.

We recommend [Anaconda](https://www.continuum.io/downloads/) which comes with a suite of packages useful for scientific data analysis. Step-by-step instructions for installing Anaconda can be found at: [Windows](https://docs.anaconda.com/anaconda/install/windows/), [macOS](https://docs.anaconda.com/anaconda/install/mac-os/), [Linux](https://docs.anaconda.com/anaconda/install/linux/)


## Installation

### Virtual Environment
To avoid potential dependency issues with other Python packages, we suggest creating a virtual environment for PySPEDAS; you can create a virtual environment in your terminal with:

```bash
python -m venv pyspedas
```

To enter your virtual environment, run the 'activate' script:

#### Windows

```bash
.\pyspedas\Scripts\activate
```

#### macOS and Linux

```bash
source pyspedas/bin/activate
```

#### Using Jupyter notebooks with your virtual environment

To get virtual environments working with Jupyter, in the virtual environment, type:

```bash
pip install ipykernel
python -m ipykernel install --user --name pyspedas --display-name "Python (pySPEDAS)"
```

(note: "pyspedas" is the name of your virtual environment)

Then once you open the notebook, go to "Kernel" then "Change kernel" and select the one named "Python (PySPEDAS)"

### Install
PySPEDAS supports Windows, macOS and Linux. To get started, install the `pyspedas` package using PyPI:

```bash
pip install pyspedas
```

### Upgrade

To upgrade to the latest version of PySPEDAS:

```bash
pip install pyspedas --upgrade
```


## Local Data Directories

The recommended way of setting your local data directory is to set the `SPEDAS_DATA_DIR` environment variable. `SPEDAS_DATA_DIR` acts as a root data directory for all missions, and will also be used by IDL (if you’re running a recent copy of the bleeding edge).

Mission specific data directories (e.g., `MMS_DATA_DIR` for MMS, `THM_DATA_DIR` for THEMIS) can also be set, and these will override `SPEDAS_DATA_DIR`

## Cloud Repositories

`SPEDAS_DATA_DIR` and mission specific data directories can also be the URI of a cloud repository (e.g., an S3 repository). If this data directory is set to an URI, files will be downloaded from the data server to the URI location. The data will then be streamed from the URI without needing to download the file locally. 

In order to successfully access the specified cloud repository, the user is required to correctly set up permissions to be able to read and write to that cloud repository on their own. Refer (here)[https://docs.aws.amazon.com/cli/v1/userguide/cli-configure-files.html] for how to prepare your AWS configuration and credentials.

## Usage

You can load data into tplot variables by calling `pyspedas.projecs.mission.instrument()`, e.g.,

To load and plot 1 day of THEMIS FGM data for probe 'd':
```python
import pyspedas
from pyspedas import tplot

thm_fgm = pyspedas.projects.themis.fgm(trange=['2015-10-16', '2015-10-17'], probe='d')

tplot(['thd_fgs_gse', 'thd_fgs_gsm'])
```

The above example used the fully qualified load routine name `pyspedas.projects.themis.fgm`.
It is also possible to use abbreviated names by importing them from the appropriate mission module:

To load and plot 2 minutes of MMS burst mode FGM data:
```python
from pyspedas.projects.mms import fgm
from pyspedas import tplot

mms_fgm = fgm(trange=['2015-10-16/13:05:30', '2015-10-16/13:07:30'], data_rate='brst')

tplot(['mms1_fgm_b_gse_brst_l2', 'mms1_fgm_b_gsm_brst_l2'])
```

Note: by default, PySPEDAS loads all data contained in CDFs found within the requested time range; this can potentially load data outside of your requested trange. To remove the data outside of your requested trange, set the `time_clip` keyword to `True`

To load and plot 6 hours of PSP SWEAP/SPAN-i data:
```python
import pyspedas
from pyspedas import tplot

spi_vars = pyspedas.projects.psp.spi(trange=['2018-11-5', '2018-11-5/06:00'], time_clip=True)

tplot(['DENS', 'VEL', 'T_TENSOR', 'TEMP'])
```

To download 5 days of STEREO magnetometer data (but not load them into tplot variables):
```python
import pyspedas

stereo_files = pyspedas.projects.stereo.mag(trange=['2013-11-1', '2013-11-6'], downloadonly=True)
```

### Standard Load Routine Options
- `trange`: two-element list specifying the time range of interest. This keyword accepts a wide range of formats
- `time_clip`: if set, clip the variables to the exact time range specified by the `trange` keyword
- `suffix`: string specifying a suffix to append to the loaded variables
- `varformat`: string specifying which CDF variables to load; accepts the wild cards * and ?
- `varnames`: string specifying which CDF variables to load (exact names)
- `get_support_data`: if set, load the support variables from the CDFs
- `downloadonly`: if set, download the files but do not load them into tplot
- `no_update`: if set, only load the data from the local cache
- `notplot`: if set, load the variables into dictionaries containing numpy arrays (instead of creating the tplot variables)


## Examples
Please see the following notebooks for examples of using PySPEDAS

### PyTplot Basics
- [Introduction to PyTplot](https://github.com/spedas/pyspedas_examples/blob/master/pyspedas_examples/notebooks/Introduction_to_PyTplot.ipynb)

### Loading Data
- [MMS examples](https://github.com/spedas/mms-examples/tree/master/basic)
- [THEMIS examples](https://github.com/spedas/themis-examples/tree/main/basic)
- [Load data from HAPI servers](https://github.com/spedas/pyspedas_examples/blob/master/pyspedas_examples/notebooks/PySPEDAS_loading_data_from_HAPI_servers.ipynb)
- [Exploring the Heliosphere with Python](https://github.com/spedas/pyspedas_examples/blob/master/pyspedas_examples/notebooks/Exploring_the_Heliosphere_with_Python.ipynb)

### Plotting
- [Annotations](https://github.com/spedas/pyspedas_examples/blob/master/pyspedas_examples/notebooks/PyTplot_annotations.ipynb)
- [Range options](https://github.com/spedas/pyspedas_examples/blob/master/pyspedas_examples/notebooks/PyTplot_range_options.ipynb)
- [Spectrogram options](https://github.com/spedas/pyspedas_examples/blob/master/pyspedas_examples/notebooks/PyTplot_spectrogram_options.ipynb)
- [Legend options](https://github.com/spedas/pyspedas_examples/blob/master/pyspedas_examples/notebooks/PyTplot_legend_options.ipynb)
- [Markers and symbols](https://github.com/spedas/pyspedas_examples/blob/master/pyspedas_examples/notebooks/PyTplot_markers_and_symbols.ipynb)
- [Error bars](https://github.com/spedas/pyspedas_examples/blob/master/pyspedas_examples/notebooks/PyTplot_error_bars.ipynb)
- [Pseudo variables](https://github.com/spedas/pyspedas_examples/blob/master/pyspedas_examples/notebooks/PyTplot_pseudo_variables.ipynb)
- [Highlight intervals and vertical bars](https://github.com/spedas/pyspedas_examples/blob/master/pyspedas_examples/notebooks/PyTplot_highlight_intervals_and_vertical_bars.ipynb)

Additional examples of loading and plotting data can be found in the documentation for the project you're interested in ([PySPEDAS projects](https://pyspedas.readthedocs.io/en/latest/projects.html)), as well as the project's README file.

### Dates and Times
- [Working with dates and times](https://github.com/spedas/pyspedas_examples/blob/master/pyspedas_examples/notebooks/Working_with_dates_and_times_with_PySPEDAS_PyTplot.ipynb)

### Coordinate Transformations
- [Coordinate transformations](https://github.com/spedas/pyspedas_examples/blob/master/pyspedas_examples/notebooks/Coordinate_transformations_with_OMNI_data.ipynb)
- [Boundary normal (LMN) coordinates](https://github.com/spedas/mms-examples/blob/master/advanced/MMS_LMN_coordinate_transformation.ipynb)
- [Quaternion transformations with SpacePy](https://github.com/spedas/mms-examples/blob/master/basic/MMS_quaternion_coordinate_transformations.ipynb)

### Analysis
- [Plasma calculations with PlasmaPy](https://github.com/spedas/mms-examples/blob/master/advanced/Plasma%20calculations%20with%20PlasmaPy.ipynb)
- [Poynting flux with MMS data](https://github.com/spedas/mms-examples/blob/master/advanced/Poynting_flux_with_MMS_data.ipynb)
- [Plasma beta with MMS data](https://github.com/spedas/mms-examples/blob/master/basic/Plasma%20Beta%20with%20FGM%20and%20FPI%20data.ipynb) (note: the PlasmaPy notebook above shows a much easier method)
- [Curlometer calculations](https://github.com/spedas/mms-examples/blob/master/basic/Curlometer%20Technique.ipynb)
- [Neutral sheet models](https://github.com/spedas/mms-examples/blob/master/advanced/MMS_neutral_sheet_models.ipynb)
- [Wave polarization calculations](https://github.com/spedas/mms-examples/blob/master/advanced/Wave_polarization_using_SCM_data.ipynb)
- [Dynamic power spectra calculations](https://github.com/spedas/mms-examples/blob/master/basic/Search-coil%20Magnetometer%20(SCM).ipynb)
- [2D slices of MMS distribution functions](https://github.com/spedas/mms-examples/blob/master/advanced/Generate_2D_slices_of_FPI_and_HPCA_data.ipynb)
- [Generating spectrograms and moments from MMS distribution functions](https://github.com/spedas/mms-examples/blob/master/advanced/Generate%20spectrograms%20and%20moments%20with%20mms_part_getspec.ipynb)


## Documentation
For more information, please see our HTML documentation at:

https://pyspedas.readthedocs.io/


## Getting Help
To find the options supported, call `help` on the instrument function you're interested in:
```python
import pyspedas

help(pyspedas.projects.themis.fgm)
```

To find PySPEDAS routine names by a keyword search, use the `libs` command (similar to the one found in IDL SPEDAS.)

```python
import pyspedas
from pyspedas import libs

# Find all PySPEDAS routine names containing the given string
libs('fgm')

# If you don't know the exact spelling, you can use wildcard characters * and ? in the search pattern:
libs('wav*pol')

```
You can ask questions by creating an issue here on Github, by joining the [SPEDAS mailing list](http://spedas.org/mailman/listinfo/spedas-list_spedas.org),
or by emailing the project maintainers at jwl@ssl.berkeley.edu .


## PyTplot

Pytplot is a separate project (soon to be merged into PySPEDAS), that replicates the IDL "tplot" functionality. Pyspedas uses a modified version of pytplot with matplotlib as the plotting library.


## Contributing
We welcome contributions to PySPEDAS; to learn how you can contribute, please see our [Contributing Guide](https://github.com/spedas/pyspedas/blob/master/CONTRIBUTING.md)


## Plug-in Development
An introduction to PySPEDAS plug-in development can be found here:

[Introduction to PySPEDAS plug-in development](https://github.com/spedas/pyspedas/tree/master/docs/pyspedas_plugin_development.pdf)


## Code of Conduct
In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation. To learn more, please see our [Code of Conduct](https://github.com/spedas/pyspedas/blob/master/CODE_OF_CONDUCT.md).


## Additional Information

For examples of pyspedas, see: https://github.com/spedas/pyspedas_examples

For MMS examples, see: https://github.com/spedas/mms-examples

For pytplot (matplotlib version), see: https://github.com/MAVENSDC/PyTplot/tree/matplotlib-backend

For cdflib, see: https://github.com/MAVENSDC/cdflib

For SPEDAS, see http://spedas.org/
