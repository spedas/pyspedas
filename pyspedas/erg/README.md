
## Arase (ERG)
The routines in this module can be used to load data from the Arase mission.

Please note that the routines in this module are EXPERIMENTAL.

### Instruments
- MGF

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Magnetic field data (MGF)

```python
mgf_vars = pyspedas.erg.mgf(trange=['2017-03-27', '2017-03-28'])

tplot('erg_mgf_l2_mag_8sec_sm')
```

