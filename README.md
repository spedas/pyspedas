
# pySPEDAS
[![Build Status](https://travis-ci.com/spedas/pyspedas.svg?branch=master)](https://travis-ci.com/spedas/pyspedas)
[![Coverage Status](https://coveralls.io/repos/github/spedas/pyspedas/badge.svg)](https://coveralls.io/github/spedas/pyspedas)
![Version](https://img.shields.io/pypi/v/pyspedas.svg)
![License](https://img.shields.io/pypi/l/pyspedas.svg)
![Status](https://img.shields.io/pypi/status/pyspedas.svg)
![Downloads](https://img.shields.io/pypi/dm/pyspedas.svg)

pySPEDAS is an implementation of the SPEDAS framework in python. 

The Space Physics Environment Data Analysis Software ([SPEDAS](http://spedas.org/wiki)) framework is written in IDL and contains data loading, data analysis and data plotting tools for various scientific missions (NASA, NOAA, etc.) and ground magnetometers.   

## Requirements

Python 3.5+ is required.  

We recommend [Anaconda](https://www.continuum.io/downloads/) which comes with a suite of packages useful for scientific data analysis. 

## Installation

pySPEDAS supports Windows, macOS and Linux. To get started, install the `pyspedas` package using PyPI or Anaconda:

### PyPI

```bash
pip install pyspedas --upgrade
```

### Anaconda

```bash
conda install -c spedas pyspedas
```

You can upgrade to the latest version using:

```bash
conda update -c spedas pyspedas
```

## Usage

To get started, import pyspedas and pytplot:

```python
import pyspedas
import pytplot
```

You can load data into tplot variables by calling `pyspedas.mission.instrument()`, e.g., 

To load and plot 1 minute of MMS burst mode FGM data:
```python
mms_fgm = pyspedas.mms.fgm(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', time_clip=True)

tplot(['mms1_fgm_b_gse_brst_l2', 'mms1_fgm_b_gsm_brst_l2'])
```

To load and plot 1 day of THEMIS FGM data for probe 'd':
```python
thm_fgm = pyspedas.themis.fgm(trange=['2015-10-16', '2015-10-17'], probe='d')

tplot(['thd_fgs_gse', 'thd_fgs_gsm'])
```

To load and plot 6 hours of PSP SWEAP/SPAN-i data:
```python
spi_vars = pyspedas.psp.spi(trange=['2018-11-5', '2018-11-5/06:00'], time_clip=True)

tplot(['DENS', 'VEL', 'T_TENSOR', 'TEMP'])
```

### Projects Supported
- [Advanced Composition Explorer (ACE)](https://github.com/spedas/pyspedas/blob/master/pyspedas/ace/README.md)
- [Cluster](https://github.com/spedas/pyspedas/blob/master/pyspedas/cluster/README.md)
- [Colorado Student Space Weather Experiment (CSSWE)](https://github.com/spedas/pyspedas/blob/master/pyspedas/csswe/README.md)
- [Deep Space Climate Observatory (DSCOVR)](https://github.com/spedas/pyspedas/blob/master/pyspedas/dscovr/README.md)
- [Equator-S](https://github.com/spedas/pyspedas/blob/master/pyspedas/equator_s/README.md)
- [Fast Auroral Snapshot Explorer (FAST)](https://github.com/spedas/pyspedas/blob/master/pyspedas/fast/README.md)
- [Geotail](https://github.com/spedas/pyspedas/blob/master/pyspedas/geotail/README.md)
- [Imager for Magnetopause-to-Aurora Global Exploration (IMAGE)](https://github.com/spedas/pyspedas/blob/master/pyspedas/image/README.md)
- Mars Atmosphere and Volatile Evolution (MAVEN)
- [Magnetospheric Multiscale (MMS)](https://github.com/spedas/pyspedas/blob/master/pyspedas/mms/README.md)
- [OMNI](https://github.com/spedas/pyspedas/blob/master/pyspedas/omni/README.md)
- [Polar Orbiting Environmental Satellites (POES)](https://github.com/spedas/pyspedas/blob/master/pyspedas/poes/README.md)
- [Polar](https://github.com/spedas/pyspedas/blob/master/pyspedas/polar/README.md)
- [Parker Solar Probe (PSP)](https://github.com/spedas/pyspedas/blob/master/pyspedas/psp/README.md)
- [Van Allen Probes (RBSP)](https://github.com/spedas/pyspedas/blob/master/pyspedas/rbsp/README.md)
- [Solar Terrestrial Relations Observatory (STEREO)](https://github.com/spedas/pyspedas/blob/master/pyspedas/stereo/README.md)
- [Time History of Events and Macroscale Interactions during Substorms (THEMIS)](https://github.com/spedas/pyspedas/blob/master/pyspedas/themis/README.md)
- [Two Wide-Angle Imaging Neutral-Atom Spectrometers (TWINS)](https://github.com/spedas/pyspedas/blob/master/pyspedas/twins/README.md)
- [Wind](https://github.com/spedas/pyspedas/blob/master/pyspedas/wind/README.md)

## Getting Help
To find the options supported, call `help` on the instrument function you're interested in:
```python
help(pyspedas.themis.fgm)
```

You can ask questions by creating an issue or by joining the [SPEDAS mailing list](http://spedas.org/mailman/listinfo/spedas-list_spedas.org).

## Contributing

## Code of Conduct

## Additional Information

For pytplot, see: https://github.com/MAVENSDC/PyTplot

For cdflib, see: https://github.com/MAVENSDC/cdflib

For SPEDAS, see http://spedas.org/
