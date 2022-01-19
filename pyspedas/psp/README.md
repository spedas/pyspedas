
## Parker Solar Probe (PSP)
The routines in this module can be used to load data from the Parker Solar Probe (PSP) mission. 

### Instruments
- Electromagnetic Fields Investigation (FIELDS)
- Solar Wind Electrons Alphas and Protons (SWEAP)
- Integrated Science Investigation of the Sun (IS☉IS)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Electromagnetic Fields Investigation (FIELDS)

```python
fields_vars = pyspedas.psp.fields(trange=['2018-11-5', '2018-11-5/06:00'], datatype='mag_rtn', level='l2', time_clip=True)

tplot('psp_fld_l2_mag_RTN')
```

#### Solar Probe Cup

```python
spc_vars = pyspedas.psp.spc(trange=['2018-11-5', '2018-11-6'], datatype='l3i', level='l3')

tplot(['np_fit', 'vp_fit_RTN'])
```

#### SWEAP/SPAN-e

```python
spe_vars = pyspedas.psp.spe(trange=['2018-11-5', '2018-11-5/06:00'], datatype='spa_sf1_32e', level='l2', time_clip=True)

tplot('EFLUX')
```

#### SWEAP/SPAN-i

```python
spi_vars = pyspedas.psp.spi(trange=['2018-11-5', '2018-11-5/06:00'], datatype='spi_sf0a_mom_inst', level='l3', time_clip=True)

tplot(['DENS', 'VEL', 'T_TENSOR', 'TEMP', 'EFLUX_VS_ENERGY', 'EFLUX_VS_THETA', 'EFLUX_VS_PHI'])
```

#### IS☉IS/EPI-Hi

```python
epihi_vars = pyspedas.psp.epihi(trange=['2018-11-5', '2018-11-5/06:00'], datatype='let1_rates1h', level='l2', time_clip=True)

tplot(['B_He_Rate', 'A_He_Flux', 'A_S_Rate'])
```

#### IS☉IS/EPI-Lo

```python
epilo_vars = pyspedas.psp.epilo(trange=['2018-11-5', '2018-11-5/06:00'], datatype='pe', level='l2', time_clip=True)

```

#### IS☉IS/EPI (merged summary data)

```python
epi_vars = pyspedas.psp.epi(trange=['2018-11-5', '2018-11-5/06:00'], datatype='summary', level='l2', time_clip=True)

tplot(['A_H_Rate_TS', 'H_CountRate_ChanT_SP', 'Electron_CountRate_ChanE', 'HET_A_H_Rate_TS', 'HET_A_Electrons_Rate_TS'])
```

