
## Magnetic Induction Coil Array (MICA)
The routines in this module can be used to load data from the Magnetic Induction Coil Array (MICA). 

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

```python
nal_vars = pyspedas.mica.induction(site='NAL', trange=['2019-02-01','2019-02-02'])

tplot('spectra_x_1Hz_NAL')
```

