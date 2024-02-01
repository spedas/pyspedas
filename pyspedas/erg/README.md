
## Arase (ERG)
The routines in this module can be used to load data from the Arase mission, as well as several other ground-based datasets made available by 
the ERG Science Center, https://ergsc.isee.nagoya-u.jp

Please note that the routines in this module are still highly EXPERIMENTAL.

### Arase (ERG) Satellite Data Load Routines
- Attitude data (ATT)
- High Energy Electron Experiments (HEP)
- Low Energy Particle Experiments (electrons) (LEPE)
- Low Energy Particle Experiments (ions) (LEPI)
- Medium Energy Particle Experiments (electrons) (MEPE)
- Medium Energy Particle Experiments (ions) (MEPI)
  - MEPI NML ("normal mode")
  - MEPI TOF ("time of flight mode")
- Magnetic Field Experiment (MGF)
- Orbit data (ORB)
- Plasma Wave Experiment (PWE)
  - Electric Field Detector (EFD)
  - High Frequency Analyzer (HFA)
  - Onboard Frequency Analyzer (OFA)
  - Waveform Capture (WFC)
- Extremely High-energy Electron Experiment (XEP)

### Arase (ERG) Coordinate Transforms

### Arase (ERG) Particle Analysis Tools

### Ground Instruments and Data Products
- Cameras
  - OMTI ASI
- Geomagnetic Instruments
  - ISEE Fluxgate Magnetometers
  - ISEE Induction Magnetometers
  - MAGDAS 1sec Data
  - MM210 Data
  - STEL Fluxgate Magnetometers (alternate name for ISEE Fluxgate Magnetometers)
  - STEL Induction Magnetometers (alternate name for ISEE Induction Magnetometers)
- SuperDARN (radar)
- ISEE BRIO (Riometer)
- ISEE VLF

### Arase (ERG) Load Routine Examples

#### Attitude (ATT)
```python
import pyspedas
from pytplot import tplot

att_vars = pyspedas.erg.att(trange=['2017-04-01', '2017-04-02'])
tplot(['erg_att_sprate', 'erg_att_spphase', 'erg_att_izras', 'erg_att_izdec', 'erg_att_gxras', 'erg_att_gxdec', 'erg_att_gzras', 'erg_att_gzdec'])
```

#### High Energy Electrons (HEP)
```python
import pyspedas
from pytplot import tplot

hep_vars = pyspedas.erg.hep(trange=['2017-03-27', '2017-03-28'])

```

#### Low Energy Electrons (LEPE)
```python
import pyspedas
from pytplot import tplot

lepe_vars = pyspedas.erg.lepe(trange=['2017-03-27', '2017-03-28'])
tplot('erg_lepe_l2_omniflux_FEDO')
```

#### Low Energy Ions (LEPI)
```python
import pyspedas
from pytplot import tplot

lepi_vars = pyspedas.erg.lepi(trange=['2017-03-27', '2017-03-28'])
tplot('erg_lepi_l2_omniflux_FODO')

```

#### Medium Energy Electrons (MEPE)
```python
import pyspedas
from pytplot import tplot

mepe_vars = pyspedas.erg.mepe(trange=['2017-03-27', '2017-03-28'])
tplot('erg_mepe_l2_omniflux_FEDO')
```

#### Medium Energy Ions, Normal Mode (MEPI-NML)
```python
import pyspedas
from pytplot import tplot

mepi_nml_vars = pyspedas.erg.mepi_nml(trange=['2017-03-27', '2017-03-28'])
tplot('erg_mepi_l2_omniflux_FPDO')
```

#### Medium Energy Ions, Time of Flight Mode (MEPI-TOF)
```python
import pyspedas
from pytplot import tplot

mepi_tof_vars = pyspedas.erg.mepi_tof(trange=['2017-03-27', '2017-03-28'])

```

#### Magnetic Field (MGF)
```python
import pyspedas
from pytplot import tplot

mgf_vars = pyspedas.erg.mgf(trange=['2017-03-27', '2017-03-28'])

tplot('erg_mgf_l2_mag_8sec_sm')
```

#### Orbit (ORB)
```python
import pyspedas
from pytplot import tplot

orb_vars = pyspedas.erg.orb(trange=['2017-03-27', '2017-03-28'])
tplot('erg_orb_l2_pos_gse')

```

#### Electric Field Detector (PWE-EFD)
```python
import pyspedas
from pytplot import tplot

pwe_efd_vars = pyspedas.erg.pwe_efd(trange=['2017-03-27', '2017-03-28'])
tplot('erg_pwe_efd_l2_E_spin_Eu_dsi')

```

#### High Frequency Analyzer (PWE-HFA)
```python
import pyspedas
from pytplot import tplot

pwe_hfa_vars = pyspedas.erg.pwe_hfa(trange=['2017-03-27', '2017-03-28'])
tplot('erg_pwe_hfa_l2_low_spectra_eu')
```

#### Onboard Frequency Analyzer (PWE-OFA)
```python
import pyspedas
from pytplot import tplot

pwe_ofa_vars = pyspedas.erg.pwe_ofa(trange=['2017-03-27', '2017-03-28'])
tplot('erg_pwe_ofa_l2_spec_E_spectra_132')

```
#### Waveform Capture (PWE-WFC)
```python
import pyspedas
from pytplot import tplot

pwe_wfc_vars = pyspedas.erg.pwe_wfc(trange=['2017-04-01/12:00:00', '2017-04-01/13:00:00'])
tplot('erg_pwe_wfc_l2_e_65khz_Ex_waveform')
```

#### Extremely High-energy Electrons (XEP)
```python
import pyspedas
from pytplot import tplot

xep_vars = pyspedas.erg.xep(trange=['2017-03-27', '2017-03-28'])
tplot('erg_xep_l2_FEDO_SSD')
```


### ERG-SC Ground Data Load Routine Examples
#### OMTI ASI
#### ISEE Fluxgate Magnetometers
#### ISEE Induction Magnetometers
#### MAGDAS 1sec
#### MM210
#### STEL Fluxgate Magnetometers
#### STEL Induction Magnetometers
#### SuperDARN (radar)
#### ISEE BRIO (riometer)
#### ISEE VLF
