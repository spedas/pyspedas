## Mars Atmosphere and Volatile Evolution (MAVEN)
The routines in this module can be used to load data from the MAVEN mission. 

Files are downloaded from the following SPDF data store. All files are level 2.

https://spdf.gsfc.nasa.gov/pub/data/maven/

Data exists for dates between 2014 and 2023.


### Instruments
- Magnetometer (MAG)
- Solar Wind Electron Analyzer (SWEA)
- Solar Wind Ion Analyzer (SWIA)
- SupraThermal And Thermal Ion Composition (STATIC)
- Solar Energetic Particle (SEP)

Also in the SPDF data store:
- kp (Key Parameters) insitu files

Instruments not included in the SPDF data store:
- Langmuir Probe and Waves (LPW) 
- Extreme Ultraviolet Monitor (EUV)


### Datatypes

SPDF only contains level 2 data (level=l2).

Valid datatypes for each instrument:

- mag (1): 'sunstate-1sec'
- swea (5): 'arc3d', 'arcpad', 'svy3d', 'svypad', 'svyspec'
- swia (6): 'onboardsvyspec', 'onboardsvymom', 'finesvy3d', 'finearc3d', 'coarsesvy3d', 'coarsearc3d'
- static (20): 'c0-64e2m', 'c2-32e32m', 'c4-4e64m', 'c6-32e64m', 'c8-32e16d', 'ca-16e4d16a', 'cc-32e8d32m',
               'cd-32e8d32m', 'ce-16e4d16a16m', 'cf-16e4d16a16m', 'd0-32e4d16a8m', 'd1-32e4d16a8m', 'd4-4d16a2m',
               'd6-events', 'd7-fsthkp', 'd8-12r1e', 'd9-12r64e', 'da-1r64e', 'db-1024tof', 'hkp'
- sep (2): 's1-cal-svy-full', 's2-cal-svy-full'
- kp or insitu (1): 'kp-4sec'


### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
from pyspedas.maven.spdf import load
from pytplot import tplot
```

#### Magnetometer (MAG)

```python
mag_vars = load(trange=['2014-10-18', '2014-10-19'], instrument='mag')
print(mag_vars)
tplot('OB_B')
```

#### Solar Wind Electron Analyzer (SWEA)

```python
swe_vars = load(trange=['2014-10-18', '2014-10-19'], instrument='swea')
print(swe_vars)
```

#### Solar Wind Ion Analyzer (SWIA)

```python
swi_vars = load(trange=['2015-11-29', '2015-11-30'], instrument='swia')
print(swi_vars)
tplot('spectra_diff_en_fluxes')
```

#### SupraThermal And Thermal Ion Composition (STATIC)

```python
sta_vars = load(trange=['2015-07-01', '2015-07-02'], instrument='static', datatype='hkp')
print(sta_vars)
tplot(sta_vars)
```

#### Solar Energetic Particle (SEP)

```python
sep_vars = load(trange=['2014-10-18', '2014-10-19'], instrument='sep')
print(sep_vars)
tplot('f_elec_flux_tot')
```

#### Key Parameters files (kp)

```python
in_vars = load(trange=['2014-10-18', '2014-10-19'], instrument='kp')
print(in_vars)
tplot('SWEA_Electron_temperature')
```