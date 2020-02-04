
## Polar Mission
The routines in this module can be used to load data from the Polar mission. 

### Instruments
- Magnetic Field Experiment (MFE)
- Electric Fields Instrument (EFI)
- Plasma Wave Instrument (PWI)
- Hot Plasma Analyzer Experiment (HYDRA)
- Thermal Ion Dynamics Experiment (TIDE)
- Toroidal Imaging Mass Angle Spectrograph (TIMAS)
- Charge and Mass Magnetospheric Ion Composition Experiment (CAMMICE)
- Comprehensive Energetic Particle-Pitch Angle Distribution (CEPPAD)
- Ultraviolet Imager (UVI)
- Visible Imaging System (VIS)
- Polar Ionospheric X-ray Imaging Experiment (PIXIE)
- Orbit data

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Magnetic Field Experiment (MFE)

```python
mfe_vars = pyspedas.polar.mfe(trange=['2003-10-28', '2003-10-29'])

tplot(['B_GSE'])
```

