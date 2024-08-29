
## Fast Auroral Snapshot Explorer (FAST)
The routines in this module can be used to load data from the Fast Auroral Snapshot Explorer (FAST) mission. 

### Instruments
- Fluxgate Magnetometer (DCB)
- Search-coil Magnetometer (ACB)
- Electrostatic Analyzers (ESA)
- Time-of-flight Energy Angle Mass Spectrograph (TEAMS)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Fluxgate Magnetometer (DCB)

```python
dcb_vars = pyspedas.fast.dcb(trange=['1998-09-05', '1998-09-06'])

tplot('')
```


#### Search-coil Magnetometer (ACB)

```python
acb_vars = pyspedas.fast.acb()

tplot('HF_E_SPEC')
```


#### Electrostatic Analyzers (ESA)

```python
esa_vars = pyspedas.fast.esa(downloadonly=True)

```


#### Time-of-flight Energy Angle Mass Spectrograph (TEAMS)

```python
teams_vars = pyspedas.fast.teams(trange=['1998-09-05', '1998-09-06'])

tplot(['H+', 'H+_low', 'H+_high'])
```

