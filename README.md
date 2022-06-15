
# PySPEDAS
[![build](https://github.com/spedas/pyspedas/workflows/build/badge.svg)](https://github.com/spedas/pyspedas/actions)
[![Coverage Status](https://coveralls.io/repos/github/spedas/pyspedas/badge.svg)](https://coveralls.io/github/spedas/pyspedas)
[![Version](https://img.shields.io/pypi/v/pyspedas.svg)](https://pypi.org/project/pyspedas/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/spedas/pyspedas.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/spedas/pyspedas/context:python)
![Status](https://img.shields.io/pypi/status/pyspedas.svg)
![License](https://img.shields.io/pypi/l/pyspedas.svg)

PySPEDAS is an implementation of the SPEDAS framework for Python. 

The Space Physics Environment Data Analysis Software ([SPEDAS](http://spedas.org/wiki)) framework is written in IDL and contains data loading, data analysis and data plotting tools for various scientific missions (NASA, NOAA, etc.) and ground magnetometers.   

Please see our documentation at: 

https://pyspedas.readthedocs.io/


## Projects Supported
- [Advanced Composition Explorer (ACE)](https://pyspedas.readthedocs.io/en/latest/ace.html)
- [Arase (ERG)](https://pyspedas.readthedocs.io/en/latest/erg.html)
- [Cluster](https://pyspedas.readthedocs.io/en/latest/cluster.html)
- [Colorado Student Space Weather Experiment (CSSWE)](https://pyspedas.readthedocs.io/en/latest/csswe.html)
- [Deep Space Climate Observatory (DSCOVR)](https://pyspedas.readthedocs.io/en/latest/dscovr.html)
- [Equator-S](https://pyspedas.readthedocs.io/en/latest/equator-s.html)
- [Fast Auroral Snapshot Explorer (FAST)](https://pyspedas.readthedocs.io/en/latest/fast.html)
- [Geotail](https://pyspedas.readthedocs.io/en/latest/geotail.html)
- [Geostationary Operational Environmental Satellite (GOES)](https://pyspedas.readthedocs.io/en/latest/goes.html)
- [Imager for Magnetopause-to-Aurora Global Exploration (IMAGE)](https://pyspedas.readthedocs.io/en/latest/image.html)
- [Kyoto Dst Index](https://pyspedas.readthedocs.io/en/latest/kyoto.html)
- [Mars Atmosphere and Volatile Evolution (MAVEN)](https://pyspedas.readthedocs.io/en/latest/maven.html)
- [Magnetic Induction Coil Array (MICA)](https://pyspedas.readthedocs.io/en/latest/mica.html)
- [Magnetospheric Multiscale (MMS)](https://pyspedas.readthedocs.io/en/latest/mms.html)
- [OMNI](https://pyspedas.readthedocs.io/en/latest/omni.html)
- [Polar Orbiting Environmental Satellites (POES)](https://pyspedas.readthedocs.io/en/latest/poes.html)
- [Polar](https://pyspedas.readthedocs.io/en/latest/polar.html)
- [Parker Solar Probe (PSP)](https://pyspedas.readthedocs.io/en/latest/psp.html)
- [Solar Orbiter (SOLO)](https://pyspedas.readthedocs.io/en/latest/solo.html)
- [Solar Terrestrial Relations Observatory (STEREO)](https://pyspedas.readthedocs.io/en/latest/stereo.html)
- [Spherical Elementary Currents (SECS)](https://github.com/spedas/pyspedas/blob/master/pyspedas/secs/README.md)
- [Swarm](https://github.com/spedas/pyspedas/blob/master/pyspedas/swarm/README.md)
- [Time History of Events and Macroscale Interactions during Substorms (THEMIS)](https://pyspedas.readthedocs.io/en/latest/themis.html)
- [Two Wide-Angle Imaging Neutral-Atom Spectrometers (TWINS)](https://pyspedas.readthedocs.io/en/latest/twins.html)
- [Ulysses](https://pyspedas.readthedocs.io/en/latest/ulysses.html)
- [Van Allen Probes (RBSP)](https://pyspedas.readthedocs.io/en/latest/rbsp.html)
- [Wind](https://pyspedas.readthedocs.io/en/latest/wind.html)

## Requirements

Python 3.7+ is required.  

We recommend [Anaconda](https://www.continuum.io/downloads/) which comes with a suite of packages useful for scientific data analysis. Step-by-step instructions for installing Anaconda can be found at: [Windows](https://docs.anaconda.com/anaconda/install/windows/), [macOS](https://docs.anaconda.com/anaconda/install/mac-os/), [Linux](https://docs.anaconda.com/anaconda/install/linux/)

## Installation

### Setup your Virtual Environment
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

## Usage

To get started, import pyspedas and pytplot:

```python
import pyspedas
from pytplot import tplot
```

You can load data into tplot variables by calling `pyspedas.mission.instrument()`, e.g., 

To load and plot 1 day of THEMIS FGM data for probe 'd':
```python
thm_fgm = pyspedas.themis.fgm(trange=['2015-10-16', '2015-10-17'], probe='d')

tplot(['thd_fgs_gse', 'thd_fgs_gsm'])
```

To load and plot 2 minutes of MMS burst mode FGM data:
```python
mms_fgm = pyspedas.mms.fgm(trange=['2015-10-16/13:05:30', '2015-10-16/13:07:30'], data_rate='brst')

tplot(['mms1_fgm_b_gse_brst_l2', 'mms1_fgm_b_gsm_brst_l2'])
```

Note: by default, PySPEDAS loads all data contained in CDFs found within the requested time range; this can potentially load data outside of your requested trange. To remove the data outside of your requested trange, set the `time_clip` keyword to `True`

To load and plot 6 hours of PSP SWEAP/SPAN-i data:
```python
spi_vars = pyspedas.psp.spi(trange=['2018-11-5', '2018-11-5/06:00'], time_clip=True)

tplot(['DENS', 'VEL', 'T_TENSOR', 'TEMP'])
```

To download 5 days of STEREO magnetometer data (but not load them into tplot variables):
```python
stereo_files = pyspedas.stereo.mag(trange=['2013-11-1', '2013-11-6'], downloadonly=True)
```

### Standard Options
- `trange`: two-element list specifying the time range of interest. This keyword accepts a wide range of formats
- `time_clip`: if set, clip the variables to the exact time range specified by the `trange` keyword 
- `suffix`: string specifying a suffix to append to the loaded variables
- `varformat`: string specifying which CDF variables to load; accepts the wild cards * and ?
- `varnames`: string specifying which CDF variables to load (exact names)
- `get_support_data`: if set, load the support variables from the CDFs
- `downloadonly`: if set, download the files but do not load them into tplot
- `no_update`: if set, only load the data from the local cache
- `notplot`: if set, load the variables into dictionaries containing numpy arrays (instead of creating the tplot variables)

## Getting Help
To find the options supported, call `help` on the instrument function you're interested in:
```python
help(pyspedas.themis.fgm)
```

You can ask questions by creating an issue or by joining the [SPEDAS mailing list](http://spedas.org/mailman/listinfo/spedas-list_spedas.org).

## Contributing
We welcome contributions to PySPEDAS; to learn how you can contribute, please see our [Contributing Guide](https://github.com/spedas/pyspedas/blob/master/CONTRIBUTING.md)

## Code of Conduct
In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation. To learn more, please see our [Code of Conduct](https://github.com/spedas/pyspedas/blob/master/CODE_OF_CONDUCT.md).

## Additional Information

For examples of pyspedas, see: https://github.com/spedas/pyspedas_examples

For MMS examples, see: https://github.com/spedas/mms-examples

For pytplot, see: https://github.com/MAVENSDC/PyTplot

For cdflib, see: https://github.com/MAVENSDC/cdflib

For SPEDAS, see http://spedas.org/
