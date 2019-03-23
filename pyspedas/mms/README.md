
## Magnetospheric Multiscale (MMS) Mission
The routines in this folder can be used to load data from the Magnetospheric Multiscale (MMS) mission. 

### What's included:
- Access to team-only data (QL, L1, L2pre), as well as L2 data
- Access to support data via the get_support_data keyword
- Data can be loaded from disk without internet connectivity 
- Data files are stored in temporary directories until each download completes, to avoid partial downloads of files due to internet connectivity issues
- Local data directory can be specified by the MMS_DATA_DIR environment variable, or by the 'local_data_dir' value in mms_config.py
- Local data paths match those at the SDC, as well as those used by IDL SPEDAS
- Data can be clipped to the requested time range after loading via the time_clip keyword
- FGM data are automatically deflagged 
- EIS omni-directional spectrograms are calculated from the individual telescope data by default
- FPI and HPCA measurements can be adjusted to the center of the accumulation interval with the center_measurement keyword
- Keywords for specifying instrument details (level, data_rate, datatype) accept strings as well as arrays of strings
- The probe keyword accepts strings, arrays of strings, ints and arrays of ints
- The load routines accept a wide range of time range formats via the trange keyword
- The load routines correctly handle access to all burst-mode data, even when small time ranges are requested
- Cross platform: tested on Windows, macOS and Linux

### Instruments
- Fluxgate Magnetometer (FGM)
- Search-coil Magnetometer (SCM)
- Electric field Double Probe (EDP)
- Electron Drift Instrument (EDI)
- Fast Plasma Investigation (FPI)
- Hot Plasma Composition Analyzer (HPCA)
- Energetic Ion Spectrometer (EIS)
- Fly's Eye Energetic Particle Sensor (FEEPS)
- Active Spacecraft Potential Control (ASPOC)
- MMS Ephemeris and Coordinates (MEC)
- Digital Signal Processor (DSP)

### Examples
Get started by importing tplot; this is required to plot the data:

```python
from pytplot import tplot
```

#### Fluxgate Magnetometer (FGM)

```python
from pyspedas import mms_load_fgm

mms_load_fgm(trange=['2015-10-16', '2015-10-17'])

tplot('mms1_fgm_b_gsm_srvy_l2')
```

#### Search-coil Magnetometer (SCM)

```python
from pyspedas import mms_load_scm

mms_load_scm(trange=['2015-10-16', '2015-10-17'])

tplot('mms1_scm_acb_gse_scsrvy_srvy_l2')
```

#### Electric field Double Probe (EDP)

```python
from pyspedas import mms_load_edp

mms_load_edp(trange=['2015-10-16', '2015-10-17'])

tplot('mms1_edp_dce_gse_fast_l2')
```

#### Electron Drift Instrument (EDI)

```python
from pyspedas import mms_load_edi

mms_load_edi(trange=['2016-10-16', '2016-10-17'])

tplot('mms1_edi_e_gse_srvy_l2')
```

#### Fast Plasma Investigation (FPI)

```python
from pyspedas import mms_load_fpi

mms_load_fpi(trange=['2015-10-16', '2015-10-17'], datatype='dis-moms')

tplot(['mms1_dis_bulkv_gse_fast', 'mms1_dis_numberdensity_fast'])
```

#### Hot Plasma Composition Analyzer (HPCA)

```python
from pyspedas import mms_load_hpca

mms_load_hpca(trange=['2015-10-16', '2015-10-17'], datatype='moments')

tplot(['mms1_hpca_hplus_number_density', 'mms1_hpca_hplus_ion_bulk_velocity'])
```

#### Energetic Ion Spectrometer (EIS)

```python
from pyspedas import mms_load_eis

mms_load_eis(trange=['2015-10-16', '2015-10-17'], datatype=['phxtof', 'extof'])

tplot(['mms1_epd_eis_extof_proton_flux_omni', 'mms1_epd_eis_phxtof_proton_flux_omni'])
```

#### Fly's Eye Energetic Particle Sensor (FEEPS)

```python
from pyspedas import mms_load_feeps

mms_load_feeps(trange=['2015-10-16', '2015-10-17'], datatype='electron')

tplot('mms1_epd_feeps_srvy_l2_electron_top_intensity_sensorid_1')
```

#### Active Spacecraft Potential Control (ASPOC)

```python
from pyspedas import mms_load_aspoc

mms_load_aspoc(trange=['2015-10-16', '2015-10-17'])

tplot('mms1_aspoc_ionc')
```

#### MMS Ephemeris and Coordinates (MEC)

```python
from pyspedas import mms_load_mec

mms_load_mec(trange=['2015-10-16', '2015-10-17'])

tplot(['mms1_mec_r_gsm', 'mms1_mec_v_gsm'])
```

#### Digital Signal Processor (DSP)

```python
from pyspedas import mms_load_dsp

mms_load_dsp(trange=['2015-10-16', '2015-10-17'], data_rate='fast', datatype='bpsd')

tplot('mms1_dsp_bpsd_omni_fast_l2')
```


### Configuration
Configuration settings are set in the CONFIG hash table in the mms_config.py file. 


### Additional Information

MMS Science Data Center: https://lasp.colorado.edu/mms/sdc/public/

MMS Datasets: https://lasp.colorado.edu/mms/sdc/public/datasets/

MMS - Goddard Space Flight Center: http://mms.gsfc.nasa.gov/

