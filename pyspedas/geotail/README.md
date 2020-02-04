
## Geotail Mission
The routines in this module can be used to load data from the Geotail mission. 

### Instruments
- Magnetic Field Experiment (MGF)
- Electric Field Detector (EFD)
- Low Energy Particle experiment (LEP)
- Comprehensive Plasma Instrumentation (CPI)
- Energetic Particles and Ion Composition Instrument (EPIC)
- Plasma Wave Instrument (PWI)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Magnetic Field Experiment (MGF)

```python
mgf_vars = pyspedas.geotail.mgf(trange=['2018-11-5', '2018-11-6'])

tplot('IB')
```

