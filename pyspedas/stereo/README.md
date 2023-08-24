
## Solar Terrestrial Relations Observatory (STEREO)
The routines in this module can be used to load data from the STEREO mission. 

### Instruments
- Magnetometer (MAG)
- PLAsma and SupraThermal Ion Composition (PLASTIC) 
- STEREO Electromagnetic Waves Experiement (SWAVES)
- Beacon (low resolution beacon data)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Magnetometer (MAG)

```python
mag_vars = pyspedas.stereo.mag(trange=['2013-1-5', '2013-1-6'])

tplot('BFIELD')
```

#### Solar Wind Electron Analyzer (SWEA)

```python
swea_vars = pyspedas.stereo.swea(trange=['2013-1-5', '2013-1-6'])
```

#### Suprathermal Electron Telescope (STE)

```python
ste_vars = pyspedas.stereo.ste(trange=['2013-1-5', '2013-1-6'])
```

#### Solar Electron Proton Telescope (SEPT)

```python
sept_vars = pyspedas.stereo.sept(trange=['2013-1-5', '2013-1-6'])
```

#### Suprathermal Ion Telescope (SIT)

```python
sit_vars = pyspedas.stereo.sit(trange=['2013-1-5', '2013-1-6'])
```

#### Low Energy Telescope (LET)

```python
sit_vars = pyspedas.stereo.let(trange=['2013-1-5', '2013-1-6'])
```

#### High Energy Telescope (HET)

```python
sit_vars = pyspedas.stereo.het(trange=['2013-1-5', '2013-1-6'])
```

#### PLAsma and SupraThermal Ion Composition (PLASTIC) 

```python
plastic_vars = pyspedas.stereo.plastic(trange=['2013-11-5', '2013-11-6'])

tplot(['proton_number_density', 'proton_bulk_speed', 'proton_temperature', 'proton_thermal_speed'])
```

#### STEREO/WAVES (S/WAVES)

```python
hfr_vars = pyspedas.stereo.waves(trange=['2013-11-5', '2013-11-6'])
tplot(['PSD_FLUX'])
```

#### Beacon Data

```python
beacon_vars = pyspedas.stereo.beacon(trange=['2013-11-5', '2013-11-6'])
tplot(['MAGBField'])
```