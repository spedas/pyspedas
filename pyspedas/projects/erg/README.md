
## Arase (ERG)
The routines in this module can be used to load data from the Arase mission, as well as several other ground-based datasets made available by 
the ERG Science Center: https://ergsc.isee.nagoya-u.jp

Please note that the routines in this module are still highly EXPERIMENTAL.

### Data servers and file versions

Ground and satellite data use separate configurable URLs. Both default to ERG-SC.
To load satellite data from the SPDF Arase mirror:

```python
from pyspedas.projects.erg.config import CONFIG
from pyspedas.projects.erg import mepe

CONFIG['satellite_remote_data_dir'] = 'https://spdf.gsfc.nasa.gov/pub/data/arase/'
mepe(version='v01_02')
```

`CONFIG['ground_remote_data_dir']` controls ground data independently. SPDF mirrors
only some satellite products; ground data still come from ERG-SC. The shared loader
translates SPDF directory layouts and EFD filename case automatically. Files are cached
beneath `local_data_dir` using paths relative to the selected data-family URL. For
example, MEPE omniflux files use `mepe/l2/omniflux/2017/` with SPDF and
`mepe/l2/omniflux/2017/03/` with ERG-SC. No `satellite/erg/` or `ground/` prefix is
added to the cache path.

To read an existing SPDF filesystem without HTTP requests, point `local_data_dir`
at the directory corresponding to the Arase URL root and enable `no_download`:

```python
CONFIG['satellite_remote_data_dir'] = 'https://spdf.gsfc.nasa.gov/pub/data/arase/'
CONFIG['local_data_dir'] = '/path/to/pub/data/arase/'
CONFIG['no_download'] = True
mepe()
```

Switching servers can create separate copies where their layouts or filenames differ.
Existing files are not moved or renamed.

Stored ERG preferences accept both URL keys. Environment variables
`ERG_SATELLITE_REMOTE_DATA_DIR` and `ERG_GROUND_REMOTE_DATA_DIR` override them.
The legacy `remote_data_dir` preference and `ERG_REMOTE_DATA_DIR` environment
variable still set the common ERG-SC base URL; the separate environment variables
take precedence over the legacy environment variable.

Every satellite loader accepts `version`, including the leading `v` and the
product's separator (for example, `v03` for ATT, `v03.03` for MGF or `v01_02`
for MEPE). An exact filename avoids a directory listing. The default `None`
uses a wildcard to select the latest available version. Versions and product
availability can differ between ERG-SC and SPDF.

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
from pyspedas import tplot

att_vars = pyspedas.erg.att(trange=['2017-04-01', '2017-04-02'])
tplot(['erg_att_sprate', 'erg_att_spphase', 'erg_att_izras', 'erg_att_izdec', 'erg_att_gxras', 'erg_att_gxdec', 'erg_att_gzras', 'erg_att_gzdec'])
```

#### High Energy Electrons (HEP)
```python
import pyspedas
from pyspedas import tplot

hep_vars = pyspedas.erg.hep(trange=['2017-03-27', '2017-03-28'])
tplot('erg_hep_l2_FEDO_L')

```

#### Low Energy Electrons (LEPE)
```python
import pyspedas
from pyspedas import tplot

lepe_vars = pyspedas.erg.lepe(trange=['2017-03-27', '2017-03-28'])
tplot('erg_lepe_l2_omniflux_FEDO')
```

#### Low Energy Ions (LEPI)
```python
import pyspedas
from pyspedas import tplot

lepi_vars = pyspedas.erg.lepi(trange=['2017-03-27', '2017-03-28'])
tplot('erg_lepi_l2_omniflux_FODO')

```

#### Medium Energy Electrons (MEPE)
```python
import pyspedas
from pyspedas import tplot

mepe_vars = pyspedas.erg.mepe(trange=['2017-03-27', '2017-03-28'])
tplot('erg_mepe_l2_omniflux_FEDO')
```

#### Medium Energy Ions, Normal Mode (MEPI-NML)
```python
import pyspedas
from pyspedas import tplot

mepi_nml_vars = pyspedas.erg.mepi_nml(trange=['2017-03-27', '2017-03-28'])
tplot('erg_mepi_l2_omniflux_FPDO')
```

#### Medium Energy Ions, Time of Flight Mode (MEPI-TOF)
```python
import pyspedas
from pyspedas import tplot

mepi_tof_vars = pyspedas.erg.mepi_tof(trange=['2017-03-27', '2017-03-28'])

```

#### Magnetic Field (MGF)
```python
import pyspedas
from pyspedas import tplot

mgf_vars = pyspedas.erg.mgf(trange=['2017-03-27', '2017-03-28'])
tplot('erg_mgf_l2_mag_8sec_sm')
```

#### Orbit (ORB)
```python
import pyspedas
from pyspedas import tplot

orb_vars = pyspedas.erg.orb(trange=['2017-03-27', '2017-03-28'])
tplot('erg_orb_l2_pos_gse')

```

#### Plasma Wave Experiment - Electric Field Detector (PWE-EFD)
```python
import pyspedas
from pyspedas import tplot

pwe_efd_vars = pyspedas.erg.pwe_efd(trange=['2017-03-27', '2017-03-28'])
tplot('erg_pwe_efd_l2_E_spin_Eu_dsi')

```

#### Plasma Wave Experiment - High Frequency Analyzer (PWE-HFA)
```python
import pyspedas
from pyspedas import tplot

pwe_hfa_vars = pyspedas.erg.pwe_hfa(trange=['2017-03-27', '2017-03-28'])
tplot('erg_pwe_hfa_l2_low_spectra_eu')
```

#### Plasma Wave Experiment - Onboard Frequency Analyzer (PWE-OFA)
```python
import pyspedas
from pyspedas import tplot

pwe_ofa_vars = pyspedas.erg.pwe_ofa(trange=['2017-03-27', '2017-03-28'])
tplot('erg_pwe_ofa_l2_spec_E_spectra_132')

```
#### Plasma Wave Experiment - Waveform Capture (PWE-WFC)
```python
import pyspedas
from pyspedas import tplot

pwe_wfc_vars = pyspedas.erg.pwe_wfc(trange=['2017-04-01/12:00:00', '2017-04-01/13:00:00'])
tplot('erg_pwe_wfc_l2_e_65khz_Ex_waveform')
```

#### Extremely High-energy Electrons (XEP)
```python
import pyspedas
from pyspedas import tplot

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
from pyspedas import tplot
fluxgate_vars=pyspedas.erg.gmag_isee_fluxgate(trange=['2020-08-01','2020-08-02'], site='all')
tplot('isee_fluxgate_mag_ktb_1min_hdz')

```
#### ISEE Induction Magnetometers
```python
import pyspedas
from pyspedas import tplot
ind_vars=pyspedas.erg.gmag_isee_induction(trange=['2020-08-01','2020-08-02'], site='all')
tplot('isee_induction_db_dt_msr')

```
#### MAGDAS 1sec
```python
import pyspedas
from pyspedas import tplot
magdas_vars=pyspedas.erg.gmag_magdas_1sec(trange=["2010-01-01", "2010-01-02"],site='ama')
tplot('magdas_mag_ama_1sec_hdz')

```
#### MM210
```python
import pyspedas
from pyspedas import tplot
mm210_vars=pyspedas.erg.gmag_mm210(trange=["2005-01-01", "2005-01-02"],site='adl',datatype='1min')
tplot('mm210_mag_adl_1min_hdz')

```
#### STEL Fluxgate Magnetometers
```python
import pyspedas
from pyspedas import tplot
fluxgate_vars=pyspedas.erg.gmag_stel_fluxgate(trange=['2020-08-01','2020-08-02'], site='all')
tplot('isee_fluxgate_mag_ktb_1min_hdz')

```
#### STEL Induction Magnetometers
```python
import pyspedas
from pyspedas import tplot
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
