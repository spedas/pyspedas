
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

To load the L2 Magnetometer data in RTN Coordinates in Normal Mode :
```python
mag_vars = pyspedas.solo.mag(trange=['2020-06-01', '2020-06-02'], datatype='rtn-normal')

tplot('B_RTN')
```


#### Energetic Particle Detector (EPD)

To load the L2 High Cadence (HCAD) SupraThermal Electrons and Protons (STEP) data:
```python
epd_vars = pyspedas.solo.epd(trange=['2020-06-01', '2020-06-02'], datatype='step', mode='hcad')

tplot(['Magnet_Rows_Flux', 'Integral_Rows_Flux', 'Magnet_Cols_Flux', 'Integral_Cols_Flux'])
```


#### Radio and Plasma Waves (RPW)

```python
rpw_vars = pyspedas.solo.rpw(trange=['2020-06-15', '2020-06-16'], datatype='hfr-surv')

tplot(['AVERAGE_NR', 'TEMPERATURE', 'FLUX_DENSITY1', 'FLUX_DENSITY2'])
```


#### Solar Wind Plasma Analyser (SWA)

To load the L2 Proton and Alpha Sensor (PAS) energy flux data:
```python
swa_vars = pyspedas.solo.swa(trange=['2020-07-22', '2020-07-23'], datatype='pas-eflux')

tplot('eflux')
```

