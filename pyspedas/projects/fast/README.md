
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

#### Fluxgate Magnetometer (DCF)

```python
dcf_vars = pyspedas.fast.dcf(trange=["1996-12-01", "1996-12-02"])
tplot(['fast_dcf_DeltaB_GEI'])
```


#### Search-coil Magnetometer (ACF)

```python
acf_vars = pyspedas.fast.acf(trange=["1996-12-01", "1996-12-02"])
tplot('fast_acf_HF_E_SPEC')
```


#### Electrostatic Analyzers (ESA)

```python
esa_vars = pyspedas.fast.esa(trange=["1996-12-01", "1996-12-02"])
tplot('fast_esa_eflux')
```


#### Time-of-flight Energy Angle Mass Spectrograph (TEAMS)

```python
teams_vars = pyspedas.fast.teams(trange=["2005-08-01", "2005-08-02"])
tplot(['fast_teams_helium_omni_flux'])
```

