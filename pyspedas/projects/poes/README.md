
## Polar Orbiting Environmental Satellites (POES) Mission
The routines in this module can be used to load data from the POES mission. 


### Instruments
- Space Environment Monitor (SEM)


### Data location

Data is loaded from the SPDF server. However, some older data is only available at NOAA 
and in this case, the user must set ncei_server=True. 


### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Space Environment Monitor (SEM)

```python
sem_vars = pyspedas.poes.sem(trange=['2013-11-5', '2013-11-6'])

tplot('ted_ele_tel30_low_eflux')
```

