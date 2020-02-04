
## Equator-S Mission
The routines in this module can be used to load data from the Equator-S mission. 

### Instruments
- Fluxgate magnetometer
- Electron beam sensing instrument
- Electrostatic analyzer (3DA)
- Solid state detector
- Time-of-fight spectrometer
- Ion emitter
- Scintillating fiber detector

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Fluxgate magnetometer

```python
mam_vars = pyspedas.equator_s.mam(trange=['1998-04-06', '1998-04-07'])

tplot(['B_xyz_gse%eq_pp_mam'])
```

