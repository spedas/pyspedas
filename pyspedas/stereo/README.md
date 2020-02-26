
## Solar Terrestrial Relations Observatory (STEREO)
The routines in this module can be used to load data from the STEREO mission. 

### Instruments
- Magnetometer (MAG)
- PLAsma and SupraThermal Ion Composition (PLASTIC) 

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Magnetometer (MAG)

```python
mag_vars = pyspedas.stereo.mag(trange=['2013-11-5', '2013-11-6'])

tplot('BFIELD')
```


#### PLAsma and SupraThermal Ion Composition (PLASTIC) 

```python
plastic_vars = pyspedas.stereo.plastic(trange=['2013-11-5', '2013-11-6'])

tplot(['proton_number_density', 'proton_bulk_speed', 'proton_temperature', 'proton_thermal_speed'])
```
