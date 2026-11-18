
## Time History of Events and Macroscale Interactions during Substorms (THEMIS)
The routines in this module can be used to load data from the THEMIS mission. 

### Data sources and layouts

Ordinary satellite and ground data use `remote_data_dir` and
`remote_data_layout`. The THEMIS server and UCLA mirror
(`https://themis-data.igpp.ucla.edu/`) use layout `themis`; SPDF and heliocloud
use layout `spdf`. Layouts are explicit and independent of the URL hostname
or scheme. Defaults use the THEMIS server and `themis` layout.

Variometers have their own `variometer_remote_data_dir` and
`variometer_remote_data_layout`, also defaulting to THEMIS. Both data URLs point
to mission roots: paths below them include `tha/`, `thg/`, etc. A single GMAG
request can mix variometers from one source with other networks from another.
The currently implemented variometer paths are shared by both layouts.

`gmag_metadata_file` is a complete URL to the station/network CSV. It defaults to
`https://themis.ssl.berkeley.edu/data/themis/thg/gmags_meta.csv` and is independent
of the science-data source. Metadata is cached as `thg/gmags_meta.csv` beneath
`local_data_dir`. `gmag(no_update=True)` and `CONFIG['no_download']` suppress
metadata downloads as well as CDF downloads. Missing offline metadata raises
`FileNotFoundError`. The in-memory table is reloaded when its configured URL or
cache root changes; changing the science-data URL alone does not reload it.

`ssc_remote_data_dir` configures both definitive and predicted SSC orbit files.
It defaults to `https://cdaweb.gsfc.nasa.gov/pub/data/themis/` and retains the
existing SSC path conventions.

For heliocloud science data with THEMIS variometers and metadata:

```python
from pyspedas.projects.themis.config import CONFIG

CONFIG.update({
    'remote_data_dir': 's3://gov-nasa-hdrl-data1/spdf/cdaweb/data/themis/',
    'remote_data_layout': 'spdf',
    'variometer_remote_data_dir': 'https://themis.ssl.berkeley.edu/data/themis/',
    'variometer_remote_data_layout': 'themis',
    'gmag_metadata_file': 'https://themis.ssl.berkeley.edu/data/themis/thg/gmags_meta.csv',
    'ssc_remote_data_dir': 'https://cdaweb.gsfc.nasa.gov/pub/data/themis/',
})
```

To use SPDF science data, change `remote_data_dir` to
`https://spdf.gsfc.nasa.gov/pub/data/themis/` and retain `spdf` layout. To use
SPDF variometers too, set their URL to that same mission root and their layout
to `spdf`. Heliocloud does not currently supply variometers or the metadata CSV.
Each resource uses only its configured source; there is no automatic fallback.
Cache paths follow the server's layout, and existing files are not moved.

State version selection is unchanged: without `version`, `themis` uses the
unversioned current-file link, while `spdf` wildcards the version and selects the
highest available. An explicit version requests that exact file, which may not
be present on the selected server. Other instruments retain their existing
version defaults. Existing SPDF/S3 configurations must set `remote_data_layout`
to `spdf` explicitly.

All six source settings can be stored under `[projects.themis]` in the PySPEDAS
preferences file. Matching environment variables override preferences:
`THM_REMOTE_DATA_DIR`, `THM_REMOTE_DATA_LAYOUT`,
`THM_VARIOMETER_REMOTE_DATA_DIR`, `THM_VARIOMETER_REMOTE_DATA_LAYOUT`,
`THM_GMAG_METADATA_FILE`, and `THM_SSC_REMOTE_DATA_DIR`.

### Instruments
- Fluxgate magnetometer (FGM)
- Search-coil magnetometer (SCM)
- Electric Field Instrument (EFI)
- Electrostatic Analyzer (ESA)
- Solid State Telescope (SST)

### Examples
Get started by importing pyspedas and tplot; these are required to load and plot the data:

```python
import pyspedas
from pyspedas import tplot
```

#### Fluxgate magnetometer (FGM)

```python
fgm_vars = pyspedas.themis.fgm(probe='d', trange=['2013-11-5', '2013-11-6'])

tplot(['thd_fgs_btotal', 'thd_fgs_gse'])
```

#### Search-coil magnetometer (SCM)

```python
scm_vars = pyspedas.themis.scm(probe='d', trange=['2013-11-5', '2013-11-6'])

tplot(['thd_scf_btotal', 'thd_scf_gse'])
```

#### Electric Field Instrument (EFI)

```python
efi_vars = pyspedas.themis.efi(probe='d', trange=['2013-11-5', '2013-11-6'])

tplot('thd_efs_dot0_gse')
```

#### Electrostatic Analyzer (ESA)

```python
esa_vars = pyspedas.themis.esa(probe='d', trange=['2013-11-5', '2013-11-6'])

tplot(['thd_peif_density', 'thd_peif_vthermal'])
```

#### Solid State Telescope (SST)

```python
sst_vars = pyspedas.themis.sst(probe='d', trange=['2013-11-5', '2013-11-6'])

tplot('thd_psif_density')
```

#### Moments data

```python
mom_vars = pyspedas.themis.mom(probe='d', trange=['2013-11-5', '2013-11-6'])

tplot(['thd_peim_velocity_gsm', 'thd_peim_density'])
```

#### Ground computed moments data

```python
gmom_vars = pyspedas.themis.gmom(probe='d', trange=['2013-11-5', '2013-11-6'])

tplot(['thd_ptiff_velocity_gse', 'thd_pteff_density', 'thd_pteff_avgtemp'])
```

#### State data

```python
state_vars = pyspedas.themis.state(probe='d', trange=['2013-11-5', '2013-11-6'])

tplot(['thd_pos', 'thd_vel'])
```

#### Ground magnetometer data

```python
gmag_vars = pyspedas.themis.gmag(sites='ccnv', trange=['2013-11-5', '2013-11-6'])

tplot('thg_mag_ccnv')
```



