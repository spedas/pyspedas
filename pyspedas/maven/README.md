
## Mars Atmosphere and Volatile Evolution (MAVEN)
The routines in this module can be used to load data from the MAVEN mission. 

There are two locations for MAVEN data files:

- MAVEN SDC at Colorado: https://lasp.colorado.edu/maven/sdc/public/data/ 
- SPDF: https://spdf.gsfc.nasa.gov/pub/data/maven/

For more information on MAVEN, see:

https://lasp.colorado.edu/maven/sdc/public/


### Instruments
- Magnetometer (MAG)
- Solar Wind Electron Analyzer (SWEA)
- Solar Wind Ion Analyzer (SWIA)
- SupraThermal And Thermal Ion Composition (STATIC)
- Solar Energetic Particle (SEP)
- Langmuir Probe and Waves (LPW) 
- Extreme Ultraviolet Monitor (EUV)

Files with data from multiple instruments:
- kp (Key Parameters) files


### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Magnetometer (MAG)

```python
mag_vars = pyspedas.maven.mag(trange=['2014-10-18', '2014-10-19'])

tplot('OB_B')
```

#### Solar Wind Electron Analyzer (SWEA)

```python
swe_vars = pyspedas.maven.swea(trange=['2014-10-18', '2014-10-19'])

tplot('diff_en_fluxes_svyspec')
```

#### Solar Wind Ion Analyzer (SWIA)

```python
swi_vars = pyspedas.maven.swia(trange=['2014-10-18', '2014-10-19'])

tplot('spectra_diff_en_fluxes_onboardsvyspec')
```

#### SupraThermal And Thermal Ion Composition (STATIC)

```python
sta_vars = pyspedas.maven.sta(trange=['2014-10-18', '2014-10-19'])

tplot('hkp_2a-hkp')
```

#### Solar Energetic Particle (SEP)

```python
sep_vars = pyspedas.maven.sep(trange=['2014-10-18', '2014-10-19'])

tplot('f_ion_flux_tot_s2-cal-svy-full')
```

#### Langmuir Probe and Waves (LPW)

```python
lpw_vars = pyspedas.maven.lpw(trange=['2014-10-18', '2014-10-19'])

tplot('mvn_lpw_lp_iv_l2_lpiv')
```

#### Extreme Ultraviolet Monitor (EUV)

```python
euv_vars = pyspedas.maven.euv(trange=['2014-10-18', '2014-10-19'])

tplot('mvn_euv_calib_bands_bands')
```
