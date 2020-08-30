
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
- Ephemeris and Coordinates (MEC)
- Digital Signal Processor (DSP)

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
Get started by importing pyspedas and tplot; this is required to plot the data:

```python
import pyspedas
from pytplot import tplot
```

#### Fluxgate Magnetometer (FGM)

```python
fgm_vars = pyspedas.mms.fgm(trange=['2015-10-16', '2015-10-17'])

tplot('mms1_fgm_b_gsm_srvy_l2')
```

#### Search-coil Magnetometer (SCM)

```python
scm_vars = pyspedas.mms.scm(trange=['2015-10-16', '2015-10-17'])

tplot('mms1_scm_acb_gse_scsrvy_srvy_l2')
```

#### Electric field Double Probe (EDP)

```python
edp_vars = pyspedas.mms.edp(trange=['2015-10-16', '2015-10-17'])

tplot('mms1_edp_dce_gse_fast_l2')
```

#### Electron Drift Instrument (EDI)

```python
edi_vars = pyspedas.mms.edi(trange=['2016-10-16', '2016-10-17'])

tplot('mms1_edi_e_gse_srvy_l2')
```

#### Fast Plasma Investigation (FPI)

```python
fpi_vars = pyspedas.mms.fpi(trange=['2015-10-16', '2015-10-17'], datatype='dis-moms')

tplot(['mms1_dis_bulkv_gse_fast', 'mms1_dis_numberdensity_fast'])
```

#### Hot Plasma Composition Analyzer (HPCA)

```python
mom_vars = pyspedas.mms.hpca(trange=['2015-10-16', '2015-10-17'], datatype='moments')

tplot(['mms1_hpca_hplus_number_density', 'mms1_hpca_hplus_ion_bulk_velocity'])

# load the ion data
ion_vars = pyspedas.mms.hpca(trange=['2016-10-16', '2016-10-17'], datatype='ion')

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
from pyspedas import mms_eis_pad

eis_vars = pyspedas.mms.eis(trange=['2015-10-16', '2015-10-17'], datatype=['phxtof', 'extof'])

# plot the non-spin averaged flux
tplot(['mms1_epd_eis_extof_proton_flux_omni', 'mms1_epd_eis_phxtof_proton_flux_omni'])

# plot the spin averaged flux
tplot(['mms1_epd_eis_extof_proton_flux_omni_spin', 'mms1_epd_eis_phxtof_proton_flux_omni_spin'])

# calculate the ExTOF pitch angle distribution
mms_eis_pad(datatype='extof')

tplot(['mms1_epd_eis_extof_56-535keV_proton_flux_omni_pad_spin', 'mms1_epd_eis_extof_56-535keV_proton_flux_omni_pad'])
```

#### Fly's Eye Energetic Particle Sensor (FEEPS)

```python
from pyspedas import mms_feeps_pad

feeps_data = pyspedas.mms.feeps(trange=['2015-10-16', '2015-10-17'], datatype='electron')

tplot(['mms1_epd_feeps_srvy_l2_electron_intensity_omni_spin', 'mms1_epd_feeps_srvy_l2_electron_intensity_omni'])

# calculate the electron pitch angle distribution
mms_feeps_pad(datatype='electron')

tplot(['mms1_epd_feeps_srvy_l2_electron_intensity_70-600keV_pad_spin', 'mms1_epd_feeps_srvy_l2_electron_intensity_70-600keV_pad'])
```

#### Active Spacecraft Potential Control (ASPOC)

```python
asp_data = pyspedas.mms.aspoc(trange=['2015-10-16', '2015-10-17'])

tplot('mms1_aspoc_ionc')
```

#### MMS Ephemeris and Coordinates (MEC)

```python
mec_data = pyspedas.mms.mec(trange=['2015-10-16', '2015-10-17'])

tplot(['mms1_mec_r_gsm', 'mms1_mec_v_gsm'])
```

#### Digital Signal Processor (DSP)

```python
dsp_data = pyspedas.mms.dsp(trange=['2015-10-16', '2015-10-17'], data_rate='fast', datatype='bpsd')

tplot('mms1_dsp_bpsd_omni_fast_l2')
```

#### State data (definitive/predicted ASCII files)

To load the state data from the definitive/predicted ASCII files, use `pyspedas.mms.state`, e.g.,

```python
pos_data = pyspedas.mms.state(trange=['2015-10-16', '2015-10-17'], datatypes='pos', level='def')

tplot('mms1_defeph_pos')
```


### Configuration
Configuration settings are set in the CONFIG hash table in the mms_config.py file. 


### Additional Information

MMS Science Data Center: https://lasp.colorado.edu/mms/sdc/public/

MMS Datasets: https://lasp.colorado.edu/mms/sdc/public/datasets/

MMS - Goddard Space Flight Center: http://mms.gsfc.nasa.gov/

