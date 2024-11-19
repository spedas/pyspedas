
## Time History of Events and Macroscale Interactions during Substorms (THEMIS)
The routines in this module can be used to load data from the THEMIS mission. 

### Instruments
- Fluxgate magnetometer (FGM)
- Search-coil magnetometer (SCM)
- Electric Field Instrument (EFI)
- Electrostatic Analyzer (ESA)
- Solid State Telescope (SST)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Fluxgate magnetometer (FGM)

```python
fgm_vars = pyspedas.themis.fgm(probe='d', trange=['2013-11-5', '2013-11-6'])

tplot(['thd_fgs_btotal', 'thd_fgs_gse'])
```

#### Search-coil magnetometer (SCM)

```python
scm_vars = pyspedas.themis.scm(probe='d', trange=['2013-11-5', '2013-11-6'])

tplot(['thd_scf_btotal', 'thd_scf_gse'])
```

#### Electric Field Instrument (EFI)

```python
efi_vars = pyspedas.themis.efi(probe='d', trange=['2013-11-5', '2013-11-6'])

tplot('thd_efs_dot0_gse')
```

#### Electrostatic Analyzer (ESA)

```python
esa_vars = pyspedas.themis.esa(probe='d', trange=['2013-11-5', '2013-11-6'])

tplot(['thd_peif_density', 'thd_peif_vthermal'])
```

#### Solid State Telescope (SST)

```python
sst_vars = pyspedas.themis.sst(probe='d', trange=['2013-11-5', '2013-11-6'])

tplot('thd_psif_density')
```

#### Moments data

```python
mom_vars = pyspedas.themis.mom(probe='d', trange=['2013-11-5', '2013-11-6'])

tplot(['thd_peim_velocity_gsm', 'thd_peim_density'])
```

#### Ground computed moments data

```python
gmom_vars = pyspedas.themis.gmom(probe='d', trange=['2013-11-5', '2013-11-6'])

tplot(['thd_ptiff_velocity_gse', 'thd_pteff_density', 'thd_pteff_avgtemp'])
```

#### State data

```python
state_vars = pyspedas.themis.state(probe='d', trange=['2013-11-5', '2013-11-6'])

tplot(['thd_pos', 'thd_vel'])
```

#### Ground magnetometer data

```python
gmag_vars = pyspedas.themis.gmag(sites='ccnv', trange=['2013-11-5', '2013-11-6'])

tplot('thg_mag_ccnv')
```



