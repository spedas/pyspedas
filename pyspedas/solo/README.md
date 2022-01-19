
## Solar Orbiter (SOLO)
The routines in this module can be used to load data from the Solar Orbiter (SOLO) mission. 

### Instruments
- Magnetometer (MAG)
- Energetic Particle Detector (EPD)
- Radio and Plasma Waves (RPW)
- Solar Wind Plasma Analyser (SWA)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Magnetometer (MAG)

```python
mag_vars = pyspedas.solo.mag(trange=['2020-06-01', '2020-06-02'], datatype='rtn-normal')

tplot('B_RTN')
```

#### Solar Wind Plasma Analyser (SWA)

```python
swa_vars = pyspedas.solo.swa(trange=['2020-07-22', '2020-07-23'], datatype='pas-eflux')

tplot('eflux')
```

#### Energetic Particle Detector (EPD)

```python
epd_vars = pyspedas.solo.epd(trange=['2020-06-01', '2020-06-02'], datatype='step', mode='rates')

tplot(['Magnet_Flux', 'Integral_Flux'])
```

#### Radio and Plasma Waves (RPW)

```python
rpw_vars = pyspedas.solo.rpw(trange=['2020-06-15', '2020-06-16'], datatype='hfr-surv')

tplot(['AVERAGE_NR', 'TEMPERATURE', 'FLUX_DENSITY1', 'FLUX_DENSITY2'])
```
