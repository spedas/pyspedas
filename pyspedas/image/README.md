
## Imager for Magnetopause-to-Aurora Global Exploration (IMAGE) Mission
The routines in this module can be used to load data from the IMAGE mission. 

### Instruments
- Low-Energy Neutral Atom (LENA) imager
- Medium-Energy Neutral Atom (MENA) imager
- High-Energy Neutral Atom (HENA) imager
- Radio Plasma Imaging (RPI)
- Extreme Ultraviolet Imager (EUV)
- Far Ultraviolet Imager (FUV)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Medium-Energy Neutral Atom (MENA) imager

```python
mena_vars = pyspedas.image.mena(trange=['2005-11-5', '2005-11-6'])
```

