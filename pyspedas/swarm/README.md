## Swarm
The routines in this module can be used to load data from the Swarm mission. 

### Instruments
- Vector Field Magnetometer (VFM)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Vector Field Magnetometer (VFM)

```python
vfm_vars = pyspedas.swarm.vfm(probe='c', trange=['2017-03-27/06:00', '2017-03-27/08:00'], datatype='hr')

tplot('swarmc_B_VFM')
```

