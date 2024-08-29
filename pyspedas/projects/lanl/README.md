
## LANL
The routines in this module can be used to load data from the LANL mission. 


### Instruments
- Magnetospheric Plasma Analyzer (MPA)
- Synchronous Orbit Particle Analyzer (SPA)


### Probes and dates

Different data is available for different dates and different probes and instruments.

The following are the valid probe values for mpa and spa, and the approximate time ranges when data is available (but there are gaps).

```
    'l0' for mpa 1992-12-16 to 2005-11-09 (l0_k0_mpa_20051109_v02.cdf)
    'l0' for spa 1992-08-01 to 2005-11-09 (l0_k0_spa_20051109_v01.cdf)
    'l1' for mpa 1993-10-27 to 2004-11-23 (l1_k0_mpa_20041123_v02.cdf)
    'l1' for spa 1992-08-01 to 2004-11-23 (l1_k0_spa_20041123_v01.cdf)
    'l4' for mpa 1996-01-01 to 2008-01-03 (l4_k0_mpa_20080103_v02.cdf)
    'l4' for spa 1996-02-16 to 2007-10-15 (l4_k0_spa_20071015_v01.cdf)
    'l7' for mpa 1997-07-04 to 2008-01-03 (l7_k0_mpa_20080103_v02.cdf)
    'l7' for spa 1999-01-01 to 2007-10-15 (l7_k0_spa_20071015_v01.cdf)
    'l9' for mpa 1993-03-15 to 2008-01-03 (l9_k0_mpa_20080103_v02.cdf)
    'l9' for spa 1992-08-01 to 2007-10-15 (l9_k0_spa_20071015_v01.cdf)
    'a1' for mpa 2005-06-07 to 2008-01-03 (a1_k0_mpa_20080103_v02.cdf)
    'a2' for mpa 2005-06-07 to 2008-01-03 (a2_k0_mpa_20080103_v02.cdf)
```
For more information, see:

https://spdf.gsfc.nasa.gov/pub/data/lanl/


### Datatype

Levels can be 'k0' or 'h0' (high precision). However, there is very limited 'h0' data available, only for 'mpa' and only for a few days in 1998.


### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
from pyspedas.lanl import load
from pytplot import tplot
```

#### Magnetospheric Plasma Analyzer (MPA)

```python
mpa_vars = load(instrument='mpa', trange=['2007-11-01', '2007-11-02'])
print(mpa_vars)
tplot(['dens_lop', 'vel_lop'])
```

#### Synchronous Orbit Particle Analyzer (SPA)

```python
spa_vars = load(instrument='spa', probe='l7', trange=['2003-12-30', '2003-12-31'])
print(spa_vars)
tplot(['spa_p_temp', 'spa_e_temp'])
```


    