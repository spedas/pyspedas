## GEO-KOMPSAT-2A

GEO-KOMPSAT-2A (GK-2A) is a South Korean meteorological and environmental satellite 
that was launched into geostationary orbit at 128.2 degrees East on 4 December 2018.

The space weather observation aboard GK-2A is performed by the Korea Space Environment Monitor (KSEM). 

It consists of three particle detectors, a charging monitor and a four-sensor Service Oriented Spacecraft Magnetometer (SOSMAG).

For more information, see:

- [Space Weather Magnetometer Aboard GEO-KOMPSAT-2A](https://link.springer.com/article/10.1007/s11214-020-00742-2)


### Data available

The routines in this module can be used to load real-time and calibrated data from the Service Oriented Spacecraft Magnetometer (SOSMAG),
and also real-time particle data (electron and proton flux) from the KSEM particle instrument.

The data is loaded using the ESA HAPI server (requires registration):
- [ESA HAPI server](https://swe.ssa.esa.int/hapi)

Users should register with ESA and then use their own username and password in the file sosmag/load.py
- [ESA registration](https://swe.ssa.esa.int/registration/)
  
For more information on SOSMAG, see:
- [SOSMAG at the ESA Space Weather Service Network](https://swe.ssa.esa.int/sosmag)


Three types of data are currently available:

- Magnetometer data (real-time or recalibrated)
- Electron flux (real-time, only since 14th March 2024, more dates in the future)
- Proton flux (real-time, only since 14th March 2024, more dates in the future)

The definition of the load function is the following:

```python
trange = ["2024-03-31T01:00:00.000Z", "2024-03-31T01:10:00.000Z"]  # start and end dates
load(trange=trange,  instrument='sosmag', datatype="", get_support_data=False, prefix="", suffix="")
```


### Instruments

The variable "instrument" can take three values:

- 'sosmag' or 'mag', for magnetometer data (default, it is optional for 'sosmag')

Magnetic Field Data with 1-16Hz from SOSMAG on GEO-KOMPSAT-2A in geostationary orbit at 128.2E.

- 'e' or 'electrons', for electron flux

1-minute averaging electron flux data from the particle detector on GEO-KOMPSAT-2A in geostationary orbit at 128.2E.

- 'p' or 'protons', for proton flux

1-minute averaging proton flux data from the particle detector on GEO-KOMPSAT-2A in geostationary orbit at 128.2E.


### Data types
For the magnetometer data only, there are two datatypes available:


- '', for Recalibrated L2 data (the default, can be empty or omitted)
- '1m', for near-realtime data


### Support data

Setting "get_support_data=True" for the load function, loads into tplot all available variables from the ESA HAPI server, including various instrument flags.


### Examples
First import the required functions from pyspedas and tplot.

Then load and plot magnetometer or particle data.

```python
from pytplot import tplot
from pyspedas import kompsat_load

# Plot L2 magnetometer data
var_names = kompsat_load(trange=["2024-03-31 02:00:00", "2024-03-31 03:00:00"])
tplot(var_names)

# Plot electron data
var_names = kompsat_load(trange=["2024-03-31 02:00:00", "2024-03-31 03:00:00"], instrument="e")
tplot(var_names)

# Plot proton data
var_names = kompsat_load(trange=["2024-03-31 02:00:00", "2024-03-31 03:00:00"], instrument="p")
tplot(var_names)
```
