
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

tplot('B1GSE')
```

#### Faraday cup (FC)

```python
fc_vars = pyspedas.dscovr.fc(trange=['2018-11-5', '2018-11-6'])

tplot(['V_GSE', 'THERMAL_SPD', 'Np', 'THERMAL_TEMP'])
```

#### Orbit data

```python
orb_vars = pyspedas.dscovr.orb(trange=['2018-11-5', '2018-11-6'])

tplot(['SUN_R', 'GCI_POS', 'GCI_VEL', 'GSE_POS', 'MOON_GSE_POS'])
```

#### Attitude data

```python
att_vars = pyspedas.dscovr.att(trange=['2018-11-5', '2018-11-6'])

tplot(['GSE_Yaw', 'GSE_Pitch', 'GSE_Roll'])
```

#### Load all data at once

```python
all_vars = pyspedas.dscovr.all(trange=['2018-11-5', '2018-11-6'])

tplot(['B1GSE', 'V_GSE', 'THERMAL_SPD', 'Np', 'GSE_POS'])
```
