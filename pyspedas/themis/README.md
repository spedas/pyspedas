
## Time History of Events and Macroscale Interactions during Substorms (THEMIS)
The routines in this module can be used to load data from the THEMIS mission. 

### Instruments
- Fluxgate magnetometer (FGM)
- Search-coil magnetometer (SCM)
- Electric Field Instrument (EFI)
- Electrostatic Analyzer (ESA)
- Solid State Telescope (SST)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Fluxgate magnetometer (FGM)

```python
fgm_vars = pyspedas.themis.fgm(probe='a', trange=['2013-11-5', '2013-11-6'])

tplot(['tha_fgs_btotal', 'tha_fgs_gse'])
```

