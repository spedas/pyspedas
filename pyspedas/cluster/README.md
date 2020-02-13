
## Cluster
The routines in this module can be used to load data from the Cluster mission. 

### Instruments
- Fluxgate Magnetometer (FGM)
- Active Spacecraft Potential Control experiment (ASPOC)
- Cluster Ion Spectroscopy experiment (CIS)
- Digital Wave Processing instrument (DWP)
- Electron Drift Instrument (EDI)
- Electric Field and Wave experiment (EFW)
- Plasma Electron and Current Experiment (PEACE)
- Research with Adaptive Particle Imaging Detectors (RAPID)
- Spatio-Temporal Analysis of Field Fluctuation experiment (STAFF)
- Wide Band Data receiver (WBD)
- Waves of High Frequency and Sounder for Probing of Density by Relaxation (WHISPER)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Fluxgate Magnetometer (FGM)

```python
fgm_vars = pyspedas.cluster.fgm(trange=['2018-11-5', '2018-11-6'])

tplot('B_xyz_gse__C1_UP_FGM')
```

#### Active Spacecraft Potential Control experiment (ASPOC)

```python
asp_vars = pyspedas.cluster.aspoc(trange=['2004-10-01', '2004-10-2'])

tplot('I_ion__C1_PP_ASP')
```

#### Cluster Ion Spectroscopy experiment (CIS)

```python
cis_vars = pyspedas.cluster.cis(trange=['2004-10-01', '2004-10-2'])

tplot(['N_p__C1_PP_CIS', 'V_p_xyz_gse__C1_PP_CIS', 'T_p_par__C1_PP_CIS', 'T_p_perp__C1_PP_CIS'])
```

#### Digital Wave Processing instrument (DWP)

```python
dwp_vars = pyspedas.cluster.dwp(trange=['2004-10-01', '2004-10-2'])

tplot('Correl_Ivar__C1_PP_DWP')
```

#### Electron Drift Instrument (EDI)

```python
edi_vars = pyspedas.cluster.edi(trange=['2004-10-01', '2004-10-2'])

tplot(['V_ed_xyz_gse__C1_PP_EDI', 'E_xyz_gse__C1_PP_EDI'])
```

#### Electric Field and Wave experiment (EFW)

```python
efw_vars = pyspedas.cluster.efw(trange=['2004-10-01', '2004-10-2'])

tplot('E_dusk__C1_PP_EFW')
```

#### Plasma Electron and Current Experiment (PEACE)

```python
peace_vars = pyspedas.cluster.peace(trange=['2004-10-01', '2004-10-2'])

tplot(['N_e_den__C1_PP_PEA', 'V_e_xyz_gse__C1_PP_PEA', 'T_e_par__C1_PP_PEA', 'T_e_perp__C1_PP_PEA'])
```

#### Research with Adaptive Particle Imaging Detectors (RAPID)

```python
rap_vars = pyspedas.cluster.rapid(trange=['2004-10-01', '2004-10-2'])

tplot(['J_e_lo__C1_PP_RAP', 'J_e_hi__C1_PP_RAP', 'J_p_lo__C1_PP_RAP', 'J_p_hi__C1_PP_RAP'])
```

#### Spatio-Temporal Analysis of Field Fluctuation experiment (STAFF)

```python
sta_vars = pyspedas.cluster.staff(trange=['2004-10-01', '2004-10-02'])

tplot('B_par_f1__C1_PP_STA')
```

#### Wide Band Data receiver (WBD)

```python
wbd_vars = pyspedas.cluster.wbd(trange=['2012-11-06/02:10', '2012-11-06/02:20'])

tplot('WBD_Elec')
```

#### Waves of High Frequency and Sounder for Probing of Density by Relaxation (WHISPER)

```python
whi_vars = pyspedas.cluster.whi()

tplot('N_e_res__C1_PP_WHI')
```

