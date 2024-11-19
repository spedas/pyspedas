
## Ulysses
The routines in this module can be used to load data from the Ulysses mission.

### Instruments
- Magnetic field (VHM)
- Solar wind plasma (SWOOPS)
- Solar wind ion composition (SWICS)
- Energetic particles (EPAC)
- Low-energy ions and electrons (HI-SCALE)
- Cosmic rays and solar particles (COSPIN)
- Radio and plasma waves (URAP)
- Solar X-rays and cosmic gamma-ray bursts (GRB)

### Examples

#### Magnetic field (VHM)

```python
import pyspedas
from pytplot import tplot

vhm_vars = pyspedas.ulysses.vhm()

tplot('B_MAG')
```

#### Solar wind plasma (SWOOPS)

```python
import pyspedas
from pytplot import tplot

swoops_vars = pyspedas.ulysses.swoops()

tplot(['Density', 'Temperature', 'Velocity'])
```

#### Solar wind ion composition (SWICS)

```python
import pyspedas
from pytplot import tplot

swics_vars = pyspedas.ulysses.swics()

tplot('Velocity')
```

#### Energetic particles (EPAC)

```python
import pyspedas
from pytplot import tplot

epac_vars = pyspedas.ulysses.epac()

tplot('Omni_Protons')
```

#### Low-energy ions and electrons (HI-SCALE)

```python
import pyspedas
from pytplot import tplot

hiscale_vars = pyspedas.ulysses.hiscale()

tplot('Electrons')
```

#### Cosmic rays and solar particles (COSPIN)

```python
import pyspedas
from pytplot import tplot

cospin_vars = pyspedas.ulysses.cospin()
```

#### Radio and plasma waves (URAP)

```python
import pyspedas
from pytplot import tplot

urap_vars = pyspedas.ulysses.urap()
```

#### Solar X-rays and cosmic gamma-ray bursts (GRB)

```python
import pyspedas
from pytplot import tplot

grb_vars = pyspedas.ulysses.grb()

tplot('Count_Rate')
```
