
## Polar
The routines in this module can be used to load data from the Polar mission. 

### Instruments
- Magnetic Field Experiment (MFE)
- Electric Fields Instrument (EFI)
- Plasma Wave Instrument (PWI)
- Hot Plasma Analyzer Experiment (HYDRA)
- Thermal Ion Dynamics Experiment (TIDE)
- Toroidal Imaging Mass Angle Spectrograph (TIMAS)
- Charge and Mass Magnetospheric Ion Composition Experiment (CAMMICE)
- Comprehensive Energetic Particle-Pitch Angle Distribution (CEPPAD)
- Ultraviolet Imager (UVI)
- Visible Imaging System (VIS)
- Polar Ionospheric X-ray Imaging Experiment (PIXIE)
- Orbit data

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Magnetic Field Experiment (MFE)

```python
mfe_vars = pyspedas.polar.mfe(trange=['2003-10-28', '2003-10-29'])

tplot(['B_GSE', 'B_GSM'])
```

#### Electric Fields Instrument (EFI)

```python
efi_vars = pyspedas.polar.efi(trange=['2003-10-28', '2003-10-29'])

tplot(['ESPIN', 'EXY12G', 'EZ12G'])
```

#### Plasma Wave Instrument (PWI)

```python
pwi_vars = pyspedas.polar.pwi()

tplot(['Fce', 'Fcp', 'FcO'])
```

#### Hot Plasma Analyzer Experiment (HYDRA)

```python
hydra_vars = pyspedas.polar.hydra(trange=['2003-10-28', '2003-10-29'])

tplot('ELE_DENSITY')
```

#### Thermal Ion Dynamics Experiment (TIDE)

```python
tide_vars = pyspedas.polar.tide()

tplot(['total_den', 'total_v', 'total_t'])
```

#### Toroidal Imaging Mass Angle Spectrograph (TIMAS)

```python
timas_vars = pyspedas.polar.timas(trange=['1997-01-03/6:00', '1997-01-03/7:00'], time_clip=True)

tplot(['Density_H', 'Density_O'])
```

#### Charge and Mass Magnetospheric Ion Composition Experiment (CAMMICE)

```python
cammice_vars = pyspedas.polar.cammice(trange=['2003-10-28', '2003-10-29'])

tplot('Protons')
```

#### Comprehensive Energetic Particle-Pitch Angle Distribution (CEPPAD)

```python
cep_vars = pyspedas.polar.ceppad(trange=['2003-10-28', '2003-10-29'])

tplot(['IPS_10_ERR', 'IPS_30_ERR', 'IPS_50_ERR'])
```

#### Ultraviolet Imager (UVI)

```python
uvi_vars = pyspedas.polar.uvi(trange=['2003-10-28', '2003-10-29'])
```


#### Visible Imaging System (VIS)

```python
vis_vars = pyspedas.polar.vis(trange=['2003-10-28', '2003-10-29'])
```


#### Polar Ionospheric X-ray Imaging Experiment (PIXIE)

```python
pixie_vars = pyspedas.polar.pixie()
```


#### Orbit data

```python
orb_vars = pyspedas.polar.orbit(trange=['2003-10-28', '2003-10-29'])

tplot(['SPIN_PHASE', 'AVG_SPIN_RATE'])
```