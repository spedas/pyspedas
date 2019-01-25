
# pyspedas

Pyspedas is an implementation of the SPEDAS framework in python. 

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

### Install pyspedas

To install pyspedas, open a command line and type the command:

`pip install pyspedas`

### Upgrade pyspedas

If you have already installed pyspedas, you can upgrade to the latest version using:

`pip install --upgrade pyspedas`


## Running pyspedas

After installation, please change the file `pyspedas/prefs.ini` and set `data_dir=C:\Datapy\themis` to a writable directory of your choice. This is the local directory where the CDF files will be saved. 

To download CDF files for the Themis mission, use: 

`import pyspedas`

`pyspedas.load_data(mission, dates, probes, instruments, level, downloadonly)`

For example: 

`d = pyspedas.load_data('themis', '2015-12-31', ['tha'], 'state', 'l1', False)`

### Crib sheets

Folder `examples` contains some crib sheets to get you started. 


### Additional Information

For pytplot, see: https://github.com/MAVENSDC/PyTplot

For cdflib, see: https://github.com/MAVENSDC/cdflib

For SPEDAS, see http://spedas.org/blog/

For information on the Themis mission, see http://themis.ssl.berkeley.edu/ 

