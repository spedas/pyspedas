
## Solar & Heliospheric Observatory (SOHO)
The routines in this module can be used to load data from the Solar & Heliospheric Observatory (SOHO) mission. 

### Instruments
- Charge, Element, and Isotope Analysis System (CELIAS)
- Comprehensive Suprathermal and Energetic Particle Analyzer (COSTEP)
- Energetic and Relativistic Nuclei and Electron experiment (ERNE)
- Orbit (ephemeris and attitude) data (ORBIT)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Charge, Element, and Isotope Analysis System (CELIAS)

```python
celias_vars = pyspedas.soho.celias(trange=['2006-06-01', '2006-06-02'])

tplot(['V_p', 'N_p'])
```


#### Comprehensive Suprathermal and Energetic Particle Analyzer (COSTEP)

```python
costep_vars = pyspedas.soho.costep(trange=['2006-06-01', '2006-06-02'])

tplot(['P_int', 'He_int'])
```


#### Energetic and Relativistic Nuclei and Electron experiment (ERNE)

```python
erne_vars = pyspedas.soho.erne(trange=['2006-06-01', '2006-06-02'])

tplot('PH')
```


#### Orbit (ephemeris and attitude) data (ORBIT)

```python
orbit_vars = pyspedas.soho.orbit(trange=['2006-06-01', '2006-06-02'])

tplot(['GSE_POS', 'GSE_VEL'])
```


    