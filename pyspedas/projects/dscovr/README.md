
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
from pyspedas.dscovr import mag
mag_vars = mag(trange=['2018-11-5', '2018-11-6'])
tplot('dsc_h0_mag_B1GSE')
```

#### Faraday cup (FC)

```python
from pyspedas.dscovr import fc
fc_vars = fc(trange=['2018-11-5', '2018-11-6'])

tplot(['dsc_h1_fc_V_GSE', 'dsc_h1_fc_THERMAL_SPD', 'dsc_h1_fc_Np', 'dsc_h1_fc_THERMAL_TEMP'])
```

#### Orbit data

```python
from pyspedas.dscovr import orb 
orb_vars = orb(trange=['2018-11-5', '2018-11-6'])

tplot(['dsc_orbit_SUN_R', 'dsc_orbit_GCI_POS', 'dsc_orbit_GCI_VEL', 'dsc_orbit_GSE_POS', 'dsc_orbit_MOON_GSE_POS'])
```

#### Attitude data

```python
from pyspedas.dscovr import att
att_vars = att(trange=['2018-11-5', '2018-11-6'])

tplot(['dsc_att_GSE_Yaw', 'dsc_att_GSE_Pitch', 'dsc_att_GSE_Roll'])
```

#### Load all data at once

```python
from pyspedas.dscovr import all  
all_vars = all(trange=['2018-11-5', '2018-11-6'])

tplot(['dsc_h0_mag_B1GSE', 'dsc_h1_fc_V_GSE', 'dsc_h1_fc_THERMAL_SPD', 'dsc_h1_fc_Np', 'dsc_orbit_GSE_POS'])
```
