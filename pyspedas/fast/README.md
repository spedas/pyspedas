
## Fast Auroral Snapshot Explorer (FAST) Mission
The routines in this module can be used to load data from the Fast Auroral Snapshot Explorer (FAST) mission. 

### Instruments
- Fluxgate Magnetometer
- Search-coil Magnetometer
- Electrostatic Analyzers (ESA)
- Time-of-flight Energy Angle Mass Spectrograph (TEAMS)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Fluxgate Magnetometer

```python
mag_vars = pyspedas.fast.dcb(trange=['1998-09-05', '1998-09-06'])

```

