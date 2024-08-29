
## Two Wide-Angle Imaging Neutral-Atom Spectrometers (TWINS) Mission
The routines in this module can be used to load data from the TWINS mission. 

### Instruments
- Imager
- Lyman-alpha Detector (LAD)
- Ephemeris

### Examples

#### Imager

```python
import pyspedas
from pytplot import tplot

img_vars = pyspedas.twins.imager(trange=['2018-11-5', '2018-11-6'])
tplot('smooth_image_val')
```

#### Lyman-alpha Detector (LAD)

```python
import pyspedas
from pytplot import tplot

lad_vars = pyspedas.twins.lad(trange=['2018-11-5/6:00', '2018-11-5/6:20'], time_clip=True)

tplot(['lad1_data', 'lad2_data'])
```

#### Ephemeris

```python
import pyspedas
from pytplot import tplot

ephem_vars = pyspedas.twins.ephemeris(trange=['2018-11-5', '2018-11-6'])

tplot('FSCGSM')
```

