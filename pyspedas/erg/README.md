
## Arase (ERG)
The routines in this module can be used to load data from the Arase mission, as well as several other ground-based datasets made available by 
the ERG Science Center: https://ergsc.isee.nagoya-u.jp

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
tplot('erg_hep_l2_FEDO_L')

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

#### Plasma Wave Experiment - Electric Field Detector (PWE-EFD)
```python
import pyspedas
from pytplot import tplot

pwe_efd_vars = pyspedas.erg.pwe_efd(trange=['2017-03-27', '2017-03-28'])
tplot('erg_pwe_efd_l2_E_spin_Eu_dsi')

```

#### Plasma Wave Experiment - High Frequency Analyzer (PWE-HFA)
```python
import pyspedas
from pytplot import tplot

pwe_hfa_vars = pyspedas.erg.pwe_hfa(trange=['2017-03-27', '2017-03-28'])
tplot('erg_pwe_hfa_l2_low_spectra_eu')
```

#### Plasma Wave Experiment - Onboard Frequency Analyzer (PWE-OFA)
```python
import pyspedas
from pytplot import tplot

pwe_ofa_vars = pyspedas.erg.pwe_ofa(trange=['2017-03-27', '2017-03-28'])
tplot('erg_pwe_ofa_l2_spec_E_spectra_132')

```
#### Plasma Wave Experiment - Waveform Capture (PWE-WFC)
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
```python
import pyspedas
omti_vars=pyspedas.erg.camera_omti_asi(site='ath', trange=['2020-01-20','2020-01-21'])
print(omti_vars)

```
#### ISEE Fluxgate Magnetometers
```python
import pyspedas
from pytplot import tplot
fluxgate_vars=pyspedas.erg.gmag_isee_fluxgate(trange=['2020-08-01','2020-08-02'], site='all')
tplot('isee_fluxgate_mag_ktb_1min_hdz')

```
#### ISEE Induction Magnetometers
```python
import pyspedas
from pytplot import tplot
ind_vars=pyspedas.erg.gmag_isee_induction(trange=['2020-08-01','2020-08-02'], site='all')
tplot('isee_induction_db_dt_msr')

```
#### MAGDAS 1sec
```python
import pyspedas
from pytplot import tplot
magdas_vars=pyspedas.erg.gmag_magdas_1sec(trange=["2010-01-01", "2010-01-02"],site='ama')
tplot('magdas_mag_ama_1sec_hdz')

```
#### MM210
```python
import pyspedas
from pytplot import tplot
mm210_vars=pyspedas.erg.gmag_mm210(trange=["2005-01-01", "2005-01-02"],site='adl',datatype='1min')
tplot('mm210_mag_adl_1min_hdz')

```
#### STEL Fluxgate Magnetometers
```python
import pyspedas
from pytplot import tplot
fluxgate_vars=pyspedas.erg.gmag_stel_fluxgate(trange=['2020-08-01','2020-08-02'], site='all')
tplot('isee_fluxgate_mag_ktb_1min_hdz')

```
#### STEL Induction Magnetometers
```python
import pyspedas
from pytplot import tplot
ind_vars=pyspedas.erg.gmag_stel_induction(trange=['2020-08-01','2020-08-02'], site='all')
tplot('isee_induction_db_dt_msr')

```
#### SuperDARN (radar)
```python
import pyspedas
sd_vars=pyspedas.erg.sd_fit(trange=['2018-10-14/00:00:00','2018-10-14/02:00:00'],site='ade')
print(sd_vars)

```
#### ISEE BRIO (riometer)
```python
import pyspedas
brio_vars=pyspedas.erg.isee_brio(trange=['2020-08-01', '2020-08-02'],site='ath')
print(brio_vars)

```
#### ISEE VLF
```python
import pyspedas
vlf_vars=pyspedas.erg.isee_vlf(trange=['2017-03-30/12:00:00', '2017-03-30/15:00:00'],site='ath')
print(vlf_vars)

```
