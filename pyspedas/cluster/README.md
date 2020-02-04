
## Cluster Mission
The routines in this module can be used to load data from the Cluster mission. 

### Instruments
- Fluxgate Magnetometer (FGM)
- Active Spacecraft Potential Control experiment (ASPOC)
- Cluster Ion Spectroscopy experiment (CIS)
- Digital Wave Processing instrument (DWP)
- Electron Drift Instrument (EDI)
- Electric Field and Wave experiment (EFW)
- Plasma Electron and Current Experiment (PEACE)
- Research with Adaptive Particle Imaging Detectors (RAPID)
- Spatio-Temporal Analysis of Field Fluctuation experiment (STAFF)
- Wide Band Data receiver (WBD)
- Waves of High Frequency and Sounder for Probing of Density by Relaxation (WHISPER)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Fluxgate Magnetometer (FGM)

```python
fgm_vars = pyspedas.cluster.fgm(trange=['2018-11-5', '2018-11-6'])

tplot('B_xyz_gse__C1_UP_FGM')
```

