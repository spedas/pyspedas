
## Imager for Magnetopause-to-Aurora Global Exploration (IMAGE)
The routines in this module can be used to load data from the IMAGE mission. 

### Instruments
- Low-Energy Neutral Atom (LENA) imager
- Medium-Energy Neutral Atom (MENA) imager
- High-Energy Neutral Atom (HENA) imager
- Radio Plasma Imaging (RPI)
- Extreme Ultraviolet Imager (EUV)
- Far Ultraviolet Imager (FUV)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Low-Energy Neutral Atom (LENA) imager

```python
lena_vars = pyspedas.image.lena(trange=['2005-11-5', '2005-11-6'])
```

#### Medium-Energy Neutral Atom (MENA) imager

```python
mena_vars = pyspedas.image.mena(trange=['2005-11-5', '2005-11-6'])
```

#### High-Energy Neutral Atom (HENA) imager

```python
hena_vars = pyspedas.image.hena(trange=['2005-11-5', '2005-11-6'])
```

#### Radio Plasma Imaging (RPI)

```python
rpi_vars = pyspedas.image.rpi(trange=['2005-11-5', '2005-11-6'])
```

#### Extreme Ultraviolet Imager (EUV)

```python
euv_vars = pyspedas.image.euv(trange=['2005-11-5', '2005-11-6'])
```

#### Far Ultraviolet Imager (FUV)

```python
fuv_vars = pyspedas.image.fuv(trange=['2005-11-5', '2005-11-6'])
```

#### Orbit data

```python
orb_vars = pyspedas.image.orbit(trange=['2005-11-5', '2005-11-6'])
```
