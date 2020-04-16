
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
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Magnetic field (VHM)

```python
vhm_vars = pyspedas.ulysses.vhm()

tplot('B_MAG')
```

#### Solar wind plasma (SWOOPS)

```python
swoops_vars = pyspedas.ulysses.swoops()

tplot(['Density', 'Temperature', 'Velocity']
```

#### Solar wind ion composition (SWICS)

```python
swics_vars = pyspedas.ulysses.swics()

tplot('Velocity')
```

#### Energetic particles (EPAC)

```python
epac_vars = pyspedas.ulysses.epac()

tplot('Omni_Protons')
```

#### Low-energy ions and electrons (HI-SCALE)

```python
hiscale_vars = pyspedas.ulysses.hiscale()

tplot('Electrons')
```

#### Cosmic rays and solar particles (COSPIN)

```python
cospin_vars = pyspedas.ulysses.cospin()
```

#### Radio and plasma waves (URAP)

```python
urap_vars = pyspedas.ulysses.urap()
```

#### Solar X-rays and cosmic gamma-ray bursts (GRB)

```python
grb_vars = pyspedas.ulysses.grb()

tplot('Count_Rate')
```
