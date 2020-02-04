
## Wind Mission
The routines in this module can be used to load data from the Wind mission. 

### Instruments
- Magnetic Field Investigation (MFI)
- Solar Wind Experiment (SWE)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Magnetic Field Investigation (MFI)

```python
mfi_vars = pyspedas.wind.mfi(trange=['2013-11-5', '2013-11-6'])

tplot('BGSE')
```

