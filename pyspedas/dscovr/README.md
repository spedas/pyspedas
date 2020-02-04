
## Deep Space Climate Observatory (DSCOVR) Mission
The routines in this module can be used to load data from the Deep Space Climate Observatory (DSCOVR) mission. 

### Instruments
- Magnetometer
- Faraday cup

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Magnetometer (MAG)

```python
mag_vars = pyspedas.dscovr.mag(trange=['2018-11-5', '2018-11-6'])

tplot('B1GSE')
```
