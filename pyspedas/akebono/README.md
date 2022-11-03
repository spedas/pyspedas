
## Akebono
The routines in this module can be used to load data from the Akebono mission. 

### Instruments
- Plasma Waves and Sounder experiment (PWS)
- Radiation Moniter (RDM)
- Orbit data (orb)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Plasma Waves and Sounder experiment (PWS)

```python
pws_vars = pyspedas.akebono.pws(trange=['2012-10-01', '2012-10-02'])

tplot(['akb_pws_RX1', 'akb_pws_RX2'])
```


#### Radiation Moniter (RDM)

```python
rdm_vars = pyspedas.akebono.rdm(trange=['2012-10-01', '2012-10-02'])

tplot('akb_rdm_FEIO')
```


#### Orbit data (orb)

```python
orb_vars = pyspedas.akebono.orb(trange=['2012-10-01', '2012-10-02'])

tplot(['akb_orb_geo', 'akb_orb_MLT'])
```


    