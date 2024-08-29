
## Colorado Student Space Weather Experiment (CSSWE)
The routines in this module can be used to load data from the Colorado Student Space Weather Experiment (CSSWE) mission. 

### Instruments
- Relativistic Electron and Proton Telescope integrated little experiment (REPTile)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Relativistic Electron and Proton Telescope integrated little experiment (REPTile)

```python
reptile_vars = pyspedas.csswe.reptile(trange=['2013-11-5', '2013-11-6'])

tplot(['E1flux', 'E2flux', 'E3flux', 'P1flux', 'P2flux', 'P3flux'])
```

