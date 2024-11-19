
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
emfisis_vars = pyspedas.rbsp.emfisis(trange=['2018-11-5/10:00', '2018-11-5/15:00'], datatype='magnetometer', level='l3', time_clip=True)

tplot(['Mag', 'Magnitude'])
```

#### Electric Field and Waves Suite (EFW)

```python
efw_vars = pyspedas.rbsp.efw(trange=['2015-11-5', '2015-11-6'], level='l3')

tplot(['efield_in_inertial_frame_spinfit_mgse', 'spacecraft_potential'])
```

#### Radiation Belt Storm Probes Ion Composition Experiment (RBSPICE)

```python
rbspice_vars = pyspedas.rbsp.rbspice(trange=['2018-11-5', '2018-11-6'], datatype='TOFxEH', level='l3')

tplot('rbspa_rbspice_l3_TOFxEH_proton_omni_spin')

# calculate the pitch angle distributions
from pyspedas.rbsp.rbspice_lib.rbsp_rbspice_pad import rbsp_rbspice_pad
rbsp_rbspice_pad(probe='a', datatype='TOFxEH', level='l3')

tplot('rbspa_rbspice_l3_TOFxEH_proton_omni_0-1000keV_pad_spin')
```

#### Energetic Particle, Composition, and Thermal Plasma Suite (ECT)

```python
mageis_vars = pyspedas.rbsp.mageis(trange=['2018-11-5', '2018-11-6'], level='l3', rel='rel04')

tplot('I')

hope_vars = pyspedas.rbsp.hope(trange=['2018-11-5', '2018-11-6'], datatype='moments', level='l3', rel='rel04')

tplot('Ion_density')

rept_vars = pyspedas.rbsp.rept(trange=['2018-11-5', '2018-11-6'], level='l3', rel='rel03')

```

#### Relativistic Proton Spectrometer (RPS)

```python
rps_vars = pyspedas.rbsp.rps(trange=['2018-11-5', '2018-11-6'], datatype='rps', level='l2')

tplot('DOSE1')
```
