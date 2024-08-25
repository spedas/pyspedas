
## Magnetospheric Multiscale (MMS) Mission
The routines in this module can be used to load data from the Magnetospheric Multiscale (MMS) mission. 

### Instruments
- Fluxgate Magnetometer (FGM)
- Search-coil Magnetometer (SCM)
- Level 3 FGM+SCM Data (FSM)
- Electric field Double Probe (EDP)
- Electron Drift Instrument (EDI)
- Fast Plasma Investigation (FPI)
- Hot Plasma Composition Analyzer (HPCA)
- Energetic Ion Spectrometer (EIS)
- Fly's Eye Energetic Particle Sensor (FEEPS)
- Active Spacecraft Potential Control (ASPOC)
- Digital Signal Processor (DSP)

### Other data products
- State data (definitive/predicted ASCII files)
- Mission Ephemeris and Coordinates (MEC)
- Tetrahedron quality factor (tetrahedron_qf)



### What's included:
- Access to team-only data (SITL, QL, L1, L2pre, L3pre), as well as all L2 data
- Access to support data via the `get_support_data` keyword
- Data can be loaded from disk without contacting the SDC via the `no_update` keyword, or by setting the `no_download` option to `True` in the configuration table found in `mms_config.py`
- Data files can be downloaded without loading into tplot variables by setting the `download_only` option in `mms_config.py`
- List available data files (without downloading) with the `available` keyword
- Data can be loaded from disk without internet connectivity 
- Data can be loaded from a network mirror by setting the `MMS_MIRROR_DATA_DIR` environment variable, or the `mirror_data_dir` option in `mms_config.py` (and using the `no_update` keyword, or by setting the `no_download` option to `True` in `mms_config.py`)
- The data can be loaded from the Space Physics Data Facility (SPDF) instead of the Science Data Center (SDC) by setting the `spdf` keyword to `True`
- Data files are stored in temporary directories until each download completes, to avoid partial downloads of files due to internet connectivity issues
- Local data directory can be specified by the MMS_DATA_DIR environment variable, or by the `local_data_dir` option in `mms_config.py`
- Local data paths match those at the SDC, as well as those used by IDL SPEDAS
- Data can be clipped to the requested time range after loading via the `time_clip` keyword
- FGM data are automatically deflagged 
- FEEPS and EIS omni-directional spectrograms are calculated from the individual telescope data by default
- FEEPS and EIS spin-averaged spectrograms are calculated by default
- Sun contamination is removed from FEEPS omni-directional spectrograms
- FEEPS integral channels are removed from the telescope spectrogram data and included in their own tplot variables
- FEEPS pitch angle distributions can be calculated using the routine `mms_feeps_pad`
- EIS pitch angle distributions can be calculated using the routine `mms_eis_pad`
- HPCA omni-directional spectrograms can be calculated using the routines `mms_hpca_calc_anodes` and `mms_hpca_spin_sum`
- FPI and HPCA measurements can be adjusted to the center of the accumulation interval with the `center_measurement` keyword
- Limit the CDF variables loaded with the `varformat` keyword
- Limit the CDF file versions loaded with the `cdf_version`, `min_version`, `latest_version` or `major_version` keywords
- CDF data can be returned in numpy arrays instead of tplot variables using the `notplot` keyword
- Suffixes can be appended to the variable names using the `suffix` keyword
- Keywords for specifying instrument details (`level`, `data_rate`, `datatype`) accept strings as well as arrays of strings
- The `probe` keyword accepts strings, arrays of strings, ints and arrays of ints
- The load routines accept a wide range of time range formats via the `trange` keyword
- The load routines correctly handle access to all burst-mode data, even when small time ranges are requested
- The load routines can be imported from `pyspedas` using the IDL procedure names (e.g., `from pyspedas import mms_load_fgm`)
- MMS orbits can be plotted using the `pyspedas.mms_orbit_plot` function
- div(B), curl(B), total current, perpendicular and parallel currents can be calculated using the curlometer technique using `pyspedas.mms.curlometer`
- Cross platform: tested on Windows, macOS and Linux

### Examples
In all the following examples, we start by importing pyspedas and tplot.
```python
import pyspedas
from pytplot import tplot
```

#### Fluxgate Magnetometer (FGM)

```python
import pyspedas
from pytplot import tplot
fgm_vars = pyspedas.mms.mms_load_fgm(trange=['2015-10-16', '2015-10-17'], probe='1')

tplot('mms1_fgm_b_gsm_srvy_l2')
```
#### L3 FGM+SCM Data (FSM)

```python
import pyspedas
from pytplot import tplot
fsm_data = pyspedas.mms.mms_load_fsm(trange=['2015-10-16/05:59', '2015-10-16/06:01'], probe='1')
tplot(['mms1_fsm_b_mag_brst_l3','mms1_fsm_b_gse_brst_l3','mms1_fsm_r_gse_brst_l3'])

```
#### Search-coil Magnetometer (SCM)

```python
import pyspedas
from pytplot import tplot
scm_vars = pyspedas.mms.mms_load_scm(trange=['2015-10-16', '2015-10-17'], probe='1')

tplot('mms1_scm_acb_gse_scsrvy_srvy_l2')
```

#### Electric field Double Probe (EDP)

```python
import pyspedas
from pytplot import tplot
edp_vars = pyspedas.mms.mms_load_edp(trange=['2015-10-16', '2015-10-17'], probe='1')

tplot('mms1_edp_dce_gse_fast_l2')
```

#### Electron Drift Instrument (EDI)

```python
import pyspedas
from pytplot import tplot
edi_vars = pyspedas.mms.mms_load_edi(trange=['2016-10-16', '2016-10-17'], probe='1')

tplot('mms1_edi_e_gse_srvy_l2')
```

#### Fast Plasma Investigation (FPI)

```python
import pyspedas
from pytplot import tplot
fpi_vars = pyspedas.mms.mms_load_fpi(trange=['2015-10-16', '2015-10-17'], probe='1', datatype='dis-moms')

tplot(['mms1_dis_bulkv_gse_fast', 'mms1_dis_numberdensity_fast'])
```

#### Hot Plasma Composition Analyzer (HPCA)

```python
import pyspedas
from pytplot import tplot
mom_vars = pyspedas.mms.mms_load_hpca(trange=['2015-10-16', '2015-10-17'], datatype='moments', probe='1')

tplot(['mms1_hpca_hplus_number_density', 'mms1_hpca_hplus_ion_bulk_velocity'])

# load the ion data
ion_vars = pyspedas.mms.mms_load_hpca(trange=['2016-10-16/00:00', '2016-10-16/05:59'], datatype='ion', probe='1')

from pyspedas import mms_hpca_calc_anodes
from pyspedas import mms_hpca_spin_sum

# average the flux over the full field of view (0-360)
mms_hpca_calc_anodes(fov=[0, 360], probe='1')

# spin-average to calculate the omni-directional flux
mms_hpca_spin_sum()

# show omni-directional flux for H+, O+ and He+, He++
tplot(['mms1_hpca_hplus_flux_elev_0-360_spin', 
             'mms1_hpca_oplus_flux_elev_0-360_spin', 
             'mms1_hpca_heplus_flux_elev_0-360_spin', 
             'mms1_hpca_heplusplus_flux_elev_0-360_spin'])
```

#### Energetic Ion Spectrometer (EIS)

```python
import pyspedas
from pytplot import tplot
from pyspedas import mms_eis_pad

eis_vars = pyspedas.mms.mms_load_eis(trange=['2015-10-16', '2015-10-17'], datatype=['phxtof', 'extof'], probe='1')

# plot the non-spin averaged flux
tplot(['mms1_epd_eis_srvy_l2_extof_proton_flux_omni', 'mms1_epd_eis_srvy_l2_phxtof_proton_flux_omni'])

# plot the spin averaged flux
tplot(['mms1_epd_eis_srvy_l2_extof_proton_flux_omni_spin', 'mms1_epd_eis_srvy_l2_phxtof_proton_flux_omni_spin'])

# calculate the ExTOF pitch angle distribution
mms_eis_pad(datatype='extof')

tplot(['mms1_epd_eis_extof_56-535keV_proton_flux_omni_pad_spin', 'mms1_epd_eis_extof_56-535keV_proton_flux_omni_pad'])
```

#### Fly's Eye Energetic Particle Sensor (FEEPS)

```python
import pyspedas
from pytplot import tplot
from pyspedas import mms_feeps_pad

feeps_data = pyspedas.mms.mms_load_feeps(trange=['2015-10-16', '2015-10-17'], datatype='electron', probe='1')

tplot(['mms1_epd_feeps_srvy_l2_electron_intensity_omni_spin', 'mms1_epd_feeps_srvy_l2_electron_intensity_omni'])

# calculate the electron pitch angle distribution
mms_feeps_pad(datatype='electron')

tplot(['mms1_epd_feeps_srvy_l2_electron_intensity_70-600keV_pad_spin', 'mms1_epd_feeps_srvy_l2_electron_intensity_70-600keV_pad'])
```

#### Active Spacecraft Potential Control (ASPOC)

```python
import pyspedas
from pytplot import tplot
asp_data = pyspedas.mms.mms_load_aspoc(trange=['2015-10-16', '2015-10-17'], probe='1')

tplot('mms1_aspoc_ionc')
```

#### MMS Ephemeris and Coordinates (MEC)

```python
import pyspedas
from pytplot import tplot
mec_data = pyspedas.mms.mms_load_mec(trange=['2015-10-16', '2015-10-17'], probe='1')

tplot(['mms1_mec_r_gsm', 'mms1_mec_v_gsm'])
```

#### Digital Signal Processor (DSP)

```python
import pyspedas
from pytplot import tplot
dsp_data = pyspedas.mms.mms_load_dsp(trange=['2015-10-16', '2015-10-17'], data_rate='fast', datatype='bpsd', probe='1')

tplot('mms1_dsp_bpsd_omni_fast_l2')
```

#### State data (definitive/predicted ASCII files)

```python
import pyspedas
from pytplot import tplot
pos_data = pyspedas.mms.mms_load_state(trange=['2015-10-16', '2015-10-17'], probe='1', datatypes='pos', level='def')

tplot('mms1_defeph_pos')
```

#### Tetrahedron quality factor data (tetrahedron_qf)
```python
import pyspedas
from pytplot import tplot
qf_vars = pyspedas.mms.mms_load_tetrahedron_qf(trange=['2015-10-16', '2015-10-17'], probe='1')
tplot('mms_tetrahedron_qf')

```

### Short names for MMS load routines

PySPEDAS includes wrappers for the MMS load routines that let you call them with shorter
names.  This can be convenient when working in an interactive Python session.
All routines of the form `pyspedas.mms.mms_load_something()` can also be called as 
`pyspedas.mms.something()`, or just `something()` depending on how you've imported them.
However, the `mms_load_something()` form is probably preferable when you're writing code to be saved 
and reused.  Your IDE can probably give you tooltips with parameter names, types, and
default values when you use the longer names, but if you use the short names, you'll
probably only see the generic `*args, **kwargs` wrapper routine parameters.

### Configuration
Configuration settings are set in the CONFIG hash table in the mms_config.py file. 


### Additional Information

MMS Science Data Center: https://lasp.colorado.edu/mms/sdc/public/

MMS Datasets: https://lasp.colorado.edu/mms/sdc/public/datasets/

MMS - Goddard Space Flight Center: http://mms.gsfc.nasa.gov/

