
# pySPEDAS
[![Build Status](https://travis-ci.com/spedas/pyspedas.svg?branch=master)](https://travis-ci.com/spedas/pyspedas)
![Version](https://img.shields.io/pypi/v/pyspedas.svg)
![License](https://img.shields.io/pypi/l/pyspedas.svg)
![Status](https://img.shields.io/pypi/status/pyspedas.svg)
![Downloads](https://img.shields.io/pypi/dm/pyspedas.svg)

pySPEDAS is an implementation of the SPEDAS framework in python. 

The Space Physics Environment Data Analysis Software ([SPEDAS](http://spedas.org/wiki)) framework is written in IDL and contains data loading, data analysis and data plotting tools for various scientific NASA missions.   

This package is designed to work with the libraries [cdflib](https://github.com/MAVENSDC/cdflib) and [pytplot](https://github.com/MAVENSDC/PyTplot).

### How It Works

CDF files are downloaded from the internet to the local machine. 
The data from these files is loaded into pytplot objects and can be plotted. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Install Python

Python 3.5+ is required.  

We recommend [Anaconda](https://www.continuum.io/downloads/) which comes with a suite of packages useful for science. 

### Install pySPEDAS

To install pySPEDAS, open a command line and type the command:

`pip install pyspedas`

### Upgrade pySPEDAS

If you have already installed pySPEDAS, you can upgrade to the latest version using:

`pip install --upgrade pyspedas`


## Running pySPEDAS

### Time History of Events and Macroscale Interactions during Substorms (THEMIS) data
After installation, please change the file `pyspedas/prefs.ini` and set `data_dir=C:\Datapy\themis` to a writable directory of your choice. This is the local directory where the CDF files will be saved. 

To download CDF files for the THEMIS mission, use: 

```python
import pyspedas

pyspedas.load_data(mission, dates, probes, instruments, level, downloadonly)

```
For example: 

```python
d = pyspedas.load_data('themis', '2015-12-31', ['tha'], 'state', 'l1', False)
```

#### Crib sheets

Folder `examples` contains some crib sheets to get you started. 

### Magnetospheric Multiscale (MMS) data
To set your local data directory for MMS, change the local_data_dir option in pyspedas/mms/mms_config.py

To load 1 day of L2 srvy-mode FGM data:
```python
from pyspedas import mms_load_fgm

mms_load_fgm(trange=['2015-10-16', '2015-10-17'], data_rate='srvy')
```

To load 1 minute of L2 brst-mode FPI electron distribution moments data:
```python
from pyspedas import mms_load_fpi

mms_load_fpi(trange=['2015-10-16/13:06', '2015-10-16/13:07'], data_rate='brst', datatype='des-moms')
```

### Additional Information

For pytplot, see: https://github.com/MAVENSDC/PyTplot

For cdflib, see: https://github.com/MAVENSDC/cdflib

For SPEDAS, see http://spedas.org/blog/

For information on the THEMIS mission, see http://themis.ssl.berkeley.edu/ 

(This is the permanent location of pyspedas. Previous location for the initial version of pyspedas was: https://github.com/nickssl/pyspedas)

