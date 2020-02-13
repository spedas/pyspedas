
## Van Allen Probes (RBSP)
The routines in this module can be used to load data from the Van Allen Probes (RBSP) mission. 

### Instruments
- Electric and Magnetic Field Instrument Suite and Integrated Science (EMFISIS)
- Electric Field and Waves Suite (EFW)
- Radiation Belt Storm Probes Ion Composition Experiment (RBSPICE)
- Energetic Particle, Composition, and Thermal Plasma Suite (ECT)
- Relativistic Proton Spectrometer (RPS)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Electric and Magnetic Field Instrument Suite and Integrated Science (EMFISIS)

```python
emfisis_vars = pyspedas.rbsp.emfisis(trange=['2018-11-5', '2018-11-6'], datatype='magnetometer', level='l3')

tplot(['Mag', 'Magnitude'])
```

#### Electric Field and Waves Suite (EFW)

```python
efw_vars = pyspedas.rbsp.efw(trange=['2015-11-5', '2015-11-6'], level='l3')

tplot(['density', 'Vavg', 'vel_gse', 'pos_gse'])
```

#### Radiation Belt Storm Probes Ion Composition Experiment (RBSPICE)

```python
rbspice_vars = pyspedas.rbsp.rbspice(trange=['2018-11-5', '2018-11-6'], datatype='tofxeh', level='l3')

tplot('Alpha')
```

#### Energetic Particle, Composition, and Thermal Plasma Suite (ECT)

```python
mageis_vars = pyspedas.rbsp.mageis(trange=['2018-11-5', '2018-11-6'], level='l3', rel='rel04')

tplot('I')

hope_vars = pyspedas.rbsp.hope(trange=['2018-11-5', '2018-11-6'], datatype='moments', level='l3', rel='rel04')

tplot('Ion_density')

rept_vars = pyspedas.rbsp.rept(trange=['2018-11-5', '2018-11-6'], level='l3', rel='rel03')

tplot('Tperp_e_200')
```

#### Relativistic Proton Spectrometer (RPS)

```python
rps_vars = pyspedas.rbsp.rps(trange=['2018-11-5', '2018-11-6'], datatype='rps', level='l2')

tplot('Alpha')
```
