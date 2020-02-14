
## Wind Mission
The routines in this module can be used to load data from the Wind mission. 

### Instruments
- Magnetic Field Investigation (MFI)
- Solar Wind Experiment (SWE)
- Radio and Plasma Waves (WAVES)
- 3D Plasma Analyzer (3DP)
- Solar Wind and Suprathermal Ion Composition Experiment (SMS)

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

#### Solar Wind Experiment (SWE)

```python
swe_vars = pyspedas.wind.swe(trange=['2013-11-5', '2013-11-6'])

tplot(['N_elec', 'T_elec'])
```

#### Radio and Plasma Waves (WAVES)

```python
waves_vars = pyspedas.wind.waves(trange=['2013-11-5', '2013-11-6'])

tplot(['E_VOLTAGE_RAD2', 'E_VOLTAGE_RAD1', 'E_VOLTAGE_TNR'])
```

#### 3D Plasma Analyzer (3DP)

```python
threedp_vars = pyspedas.wind.threedp(trange=['2013-11-5', '2013-11-6'])

tplot(['V_e_xyz_gse_wi_3dp', 'N_e_dens_wi_3dp', 'T_e_par_wi_3dp'])
```

#### Solar Wind and Suprathermal Ion Composition Experiment (SMS)

```python
sms_vars = pyspedas.wind.sms()

tplot(['C_ion_temp', 'O_ion_temp'])
```

#### Orbit data

```python
orb_vars = pyspedas.wind.orbit(trange=['2013-11-5', '2013-11-6'])

tplot(['GSE_POS', 'GSE_VEL', 'GSM_POS', 'GSM_VEL'])
```