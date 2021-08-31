
## Deep Space Climate Observatory (DSCOVR)
The routines in this module can be used to load data from the Deep Space Climate Observatory (DSCOVR) mission. 

### Instruments
- Magnetometer
- Faraday cup

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Magnetometer (MAG)

```python
mag_vars = pyspedas.dscovr.mag(trange=['2018-11-5', '2018-11-6'])

tplot('dsc_h0_mag_B1GSE')
```

#### Faraday cup (FC)

```python
fc_vars = pyspedas.dscovr.fc(trange=['2018-11-5', '2018-11-6'])

tplot(['dsc_h1_fc_V_GSE', 'dsc_h1_fc_THERMAL_SPD', 'dsc_h1_fc_Np', 'dsc_h1_fc_THERMAL_TEMP'])
```

#### Orbit data

```python
orb_vars = pyspedas.dscovr.orb(trange=['2018-11-5', '2018-11-6'])

tplot(['dsc_orbit_SUN_R', 'dsc_orbit_GCI_POS', 'dsc_orbit_GCI_VEL', 'dsc_orbit_GSE_POS', 'dsc_orbit_MOON_GSE_POS'])
```

#### Attitude data

```python
att_vars = pyspedas.dscovr.att(trange=['2018-11-5', '2018-11-6'])

tplot(['dsc_att_GSE_Yaw', 'dsc_att_GSE_Pitch', 'dsc_att_GSE_Roll'])
```

#### Load all data at once

```python
all_vars = pyspedas.dscovr.all(trange=['2018-11-5', '2018-11-6'])

tplot(['dsc_h0_mag_B1GSE', 'dsc_h1_fc_V_GSE', 'dsc_h1_fc_THERMAL_SPD', 'dsc_h1_fc_Np', 'dsc_orbit_GSE_POS'])
```
