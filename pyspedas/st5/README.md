
## Space Technology 5 (ST5)
The routines in this module can be used to load data from the Space Technology 5 (ST5) mission. 

### Instruments
- Magnetometer (MAG)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Magnetometer (MAG)

```python
mag_vars = pyspedas.st5.mag(trange=['2006-06-01', '2006-06-02'])

tplot(['B_SM', 'SC_POS_SM'])
```


    