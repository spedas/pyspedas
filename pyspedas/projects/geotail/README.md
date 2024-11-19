
## Geotail
The routines in this module can be used to load data from the Geotail mission. 

### Instruments
- Magnetic Field Experiment (MGF)
- Electric Field Detector (EFD)
- Low Energy Particle experiment (LEP)
- Comprehensive Plasma Instrumentation (CPI)
- Energetic Particles and Ion Composition Instrument (EPIC)
- Plasma Wave Instrument (PWI)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Magnetic Field Experiment (MGF)

```python
mgf_vars = pyspedas.geotail.mgf(trange=['2018-11-5', '2018-11-6'])

tplot(['IB', 'IB_vector'])
```

#### Electric Field Detector (EFD)

```python
efd_vars = pyspedas.geotail.efd(trange=['2018-11-5', '2018-11-6'])

tplot(['Es', 'Ss', 'Bs', 'Vs', 'Ew', 'Sw', 'Bw', 'Vw'])
```

#### Low Energy Particle experiment (LEP)

```python
lep_vars = pyspedas.geotail.lep(trange=['2018-11-5/05:00', '2018-11-5/06:00'], time_clip=True)

tplot(['N0', 'V0'])
```

#### Comprehensive Plasma Instrumentation (CPI)

```python
cpi_vars = pyspedas.geotail.cpi(trange=['2018-11-5/15:00', '2018-11-5/18:00'], time_clip=True)

tplot(['SW_P_Den', 'SW_P_AVGE', 'SW_V', 'HP_P_Den'])
```

#### Energetic Particles and Ion Composition Instrument (EPIC)

```python
epic_vars = pyspedas.geotail.epic(trange=['2018-11-5', '2018-11-6'])

tplot('IDiffI_I')
```

#### Plasma Wave Instrument (PWI)

```python
pwi_vars = pyspedas.geotail.pwi(trange=['2018-11-5/06:00', '2018-11-5/07:00'], time_clip=True)

tplot(['MCAE_AVE', 'MCAB_AVE'])
```
