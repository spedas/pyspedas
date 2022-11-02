
## LANL
The routines in this module can be used to load data from the LANL mission. 

### Instruments
- Magnetospheric Plasma Analyzer (MPA)
- Synchronous Orbit Particle Analyzer (SPA)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Magnetospheric Plasma Analyzer (MPA)

```python
mpa_vars = pyspedas.lanl.mpa(trange=['2004-10-31', '2004-11-01'])

tplot(['dens_lop', 'vel_lop'])
```


#### Synchronous Orbit Particle Analyzer (SPA)

```python
spa_vars = pyspedas.lanl.spa(trange=['2004-10-31', '2004-11-01'])

tplot(['spa_p_temp', 'spa_e_temp'])
```


    