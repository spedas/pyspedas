## Service Oriented Spacecraft Magnetometer on GEO-KOMPSAT-2A (SOSMAG)
The routines in this module can be used to load data from the SOSMAG magnetometer. 

For more information, see:
- [SOSMAG at the ESA Space Weather Service Network](https://swe.ssa.esa.int/sosmag)

The data is loaded using the ESA HAPI server (requires registration):
- [ESA HAPI server](https://swe.ssa.esa.int/hapi)

Users should register with ESA and then use their own username and password in the file sosmag/load.py
- [ESA registration](https://swe.ssa.esa.int/registration/)


### Instruments
- Magnetometer (MAG)


### Example
First import the required functions from pyspedas and tplot.

Then load and plot the magnetometer data.

```python
from pytplot import tplot
from pyspedas import sosmag_load

tplot_ok, var_names = sosmag_load(trange=['2021-01-01 02:00:00', '2021-01-01 03:00:00'], datatype='1m')
tplot(var_names)
```
