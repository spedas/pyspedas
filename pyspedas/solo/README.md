
## Solar Orbiter (SOLO)
The routines in this module can be used to load data from the Solar Orbiter (SOLO) mission. 

### Instruments
- Magnetometer (MAG)
- Energetic Particle Detector (EPD)
- Radio and Plasma Waves (RPW)
- Solar Wind Plasma Analyser (SWA)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Magnetometer (MAG)

```python
mag_vars = pyspedas.solo.mag(trange=['2020-06-01', '2020-06-02'])

tplot('B_RTN')
```

