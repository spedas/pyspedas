
## Geostationary Operational Environmental Satellite (GOES)
The routines in this module can be used to load data from the GOES mission. 

### Instruments
- Magnetometer (FGM)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Magnetometer (FGM)

```python
mag_vars = pyspedas.goes.fgm(trange=['2013-11-5', '2013-11-6'], datatype='512ms')

tplot(['BX_1', 'BY_1', 'BZ_1'])
```

