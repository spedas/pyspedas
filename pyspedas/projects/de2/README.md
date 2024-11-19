
## Dynamics Explorer 2 (DE2)
The routines in this module can be used to load data from the Dynamics Explorer 2 (DE2) mission. 

### Instruments
- Magnetometer (MAG)
- Neutral Atmosphere Composition Spectrometer (NACS)
- Retarding Potential Analyzer (RPA)
- Fabry-Pérot Interferometer (FPI)
- Ion Drift Meter (IDM)
- Wind and Temperature Spectrometer (WATS)
- Vector Electric Field Instrument (VEFI)
- Langmuir Probe Instrument (LANG)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Magnetometer (MAG)

```python
mag_vars = pyspedas.de2.mag(trange=['1983-02-10', '1983-02-11'])

tplot(['bx', 'by', 'bz'])
```


#### Neutral Atmosphere Composition Spectrometer (NACS)

```python
nacs_vars = pyspedas.de2.nacs(trange=['1983-02-10', '1983-02-11'])

tplot(['O_density', 'N_density'])
```


#### Retarding Potential Analyzer (RPA)

```python
rpa_vars = pyspedas.de2.rpa(trange=['1983-02-10', '1983-02-11'])

tplot(['ionDensity', 'ionTemperature'])
```


#### Fabry-Pérot Interferometer (FPI)

```python
fpi_vars = pyspedas.de2.fpi(trange=['1983-02-10', '1983-02-11'])

tplot('TnF')
```


#### Ion Drift Meter (IDM)

```python
idm_vars = pyspedas.de2.idm(trange=['1983-02-10', '1983-02-11'])

tplot(['ionVelocityZ', 'ionVelocityY'])
```


#### Wind and Temperature Spectrometer (WATS)

```python
wats_vars = pyspedas.de2.wats(trange=['1983-02-10', '1983-02-11'])

tplot(['density', 'Tn'])
```


#### Vector Electric Field Instrument (VEFI)

```python
vefi_vars = pyspedas.de2.vefi(trange=['1983-02-10', '1983-02-11'])

tplot(['spectA', 'spectB', 'spectC'])
```


#### Langmuir Probe Instrument (LANG)

```python
lang_vars = pyspedas.de2.lang(trange=['1983-02-10', '1983-02-11'])

tplot(['plasmaDensity', 'electronTemp'])
```


    