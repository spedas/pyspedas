
## Communications/Navigation Outage Forecasting System (C/NOFS)
The routines in this module can be used to load data from the Communications/Navigation Outage Forecasting System (C/NOFS) mission. 

### Instruments
- Coupled Ion-Neutral Dynamics Investigation (CINDI)
- Planar Langmuir Probe (PLP)
- Vector Electric Field Instrument (VEFI)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Coupled Ion-Neutral Dynamics Investigation (CINDI)

```python
cindi_vars = pyspedas.cnofs.cindi(trange=['2013-11-5', '2013-11-6'])

tplot(['ionVelocityX', 'ionVelocityY', 'ionVelocityZ'])
```

#### Planar Langmuir Probe (PLP)

```python
plp_vars = pyspedas.cnofs.plp(trange=['2010-11-5', '2010-11-6'])

tplot('Ni')
```

#### Vector Electric Field Instrument (VEFI)

```python
vefi_vars = pyspedas.cnofs.vefi(trange=['2013-11-5', '2013-11-6'])

tplot(['E_meridional', 'E_zonal'])
```



