
## Two Wide-Angle Imaging Neutral-Atom Spectrometers (TWINS) Mission
The routines in this module can be used to load data from the TWINS mission. 

### Instruments
- Imager
- Lyman-alpha Detector (LAD)
- Ephemeris

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Imager

```python
img_vars = pyspedas.twins.imager(trange=['2018-11-5', '2018-11-6'])
```

#### Lyman-alpha Detector (LAD)

```python
lad_vars = pyspedas.twins.lad(trange=['2018-11-5', '2018-11-6'])

tplot(['lad1_data', 'lad2_data'])
```

#### Ephemeris

```python
ephem_vars = pyspedas.twins.ephemeris(trange=['2018-11-5', '2018-11-6'])

tplot('FSCGSM')
```

