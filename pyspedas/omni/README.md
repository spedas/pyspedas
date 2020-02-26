
## OMNI data
The routines in this module can be used to load OMNI (Combined 1AU IP Data; Magnetic and Solar Indices) data.

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

```python
omni_vars = pyspedas.omni.data(trange=['2013-11-5', '2013-11-6'])

tplot(['BX_GSE', 'BY_GSE', 'BZ_GSE', 'flow_speed', 'Vx', 'Vy', 'Vz', 'SYM_H'])
```

