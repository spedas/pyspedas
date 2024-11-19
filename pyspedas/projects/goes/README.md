
## Geostationary Operational Environmental Satellite (GOES)
The routines in this module can be used to load data from the GOES mission. 

The load routine works for both the older GOES probes (GOES-8 to GOES-15) and the newer GOES-R probes (GOES-16 and later). 
However, the datasets are different for probes 8-15 and for probes 16+.



### Instruments
For GOES 8-15: fgm, eps, epead, maged, magpd, hepad, xrs

For GOES-R 16-18: euvs, xrs, mag, mpsh, sgps


### Datatypes

Depends on the probe and the instrument. It is usually the instrument resolution.

For GOES-8 to 15, valid values: hi, low, full, avg, 1min, 5min

For GOES-R (16 and later), valid values: hi, low, full, avg


### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### For older GOES probes (up to GOES-15) 

Example for Magnetometer data (FGM):

```python
mag_vars = pyspedas.goes.fgm(trange=['2013-11-5', '2013-11-6'], datatype='512ms')
print(mag_vars)
tplot(['BX_1', 'BY_1', 'BZ_1'])
```

#### For GOES-R probes (GOES-16 or newer)

Example for Magnetometer data (mag):

```python
mag_goes18 = pyspedas.goes.load(trange=['2023-01-01', '2023-01-02'], probe='18', instrument='mag')
print(mag_goes18)
tplot(['b_gsm', 'b_total'])
```


### Further Information

For more information on GOES-R, see:
https://www.ngdc.noaa.gov/stp/satellite/goes-r.html

For NOAA Space Weather Prediction Center, see:
https://www.swpc.noaa.gov/

For GOES summary plots, see:
https://themis.ssl.berkeley.edu/summary.php?year=2024&month=01&day=01&hour=0024&sumType=goes&type=goes18

