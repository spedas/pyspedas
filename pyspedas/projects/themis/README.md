
## Time History of Events and Macroscale Interactions during Substorms (THEMIS)
The routines in this module can be used to load data from the THEMIS mission. 

### Provider shortcuts

Setters update in-memory `CONFIG` settings for the current session, log the new
settings at INFO level, and make no network requests. Tags are case-sensitive.
Unsupported tags raise `ValueError` with the valid choices before changing any
settings. Other data families and cache/offline settings are unaffected.

Each setter has a corresponding `get_..._source()` function. Getters match the
current relevant URL/layout or access settings exactly, including changes made
directly to `CONFIG`. They return the provider tag, or `None` for custom or
incomplete settings. Direct URL configuration remains supported. Setters do not
save preferences; use the existing preferences API explicitly to persist them.

| Data family | Setter | Supported tags |
| --- | --- | --- |
| All satellite/ground data and GMAG metadata | `set_data_source(source_tag)` | `berkeley`, `ucla`, `spdf`, `heliocloud` |
| SSC orbit data | `set_ssc_source(source_tag)` | `spdf` |

```python
from pyspedas.projects.themis import config

config.set_data_source('heliocloud')
print(config.get_data_source())  # heliocloud
```

The `berkeley` and `ucla` presets select `themis` layout; `spdf` and
`heliocloud` select `spdf` layout. A data-source change applies to satellite
products, all ground magnetometer networks (including variometers), and GMAG
station metadata. SSC remains independent.

### Data sources and layouts

`remote_data_dir` and `remote_data_layout` control all mission data. The THEMIS
server and UCLA mirror (`https://themis-data.igpp.ucla.edu/`) use `themis` layout;
SPDF and heliocloud use `spdf` layout. Layouts are explicit and independent of
hostname or URL scheme. Defaults remain the THEMIS server and `themis` layout.
The URL names the mission root containing `tha/`, `thg/`, etc. Mixed-network
GMAG requests use that same root for every station.

GMAG station metadata is read from `thg/gmags_meta.csv` beneath the main URL and
cached at the same relative path beneath `local_data_dir`. S3 metadata is copied
locally so it can be reused offline. `gmag(no_update=True)` and
`CONFIG['no_download']` suppress metadata downloads as well as CDF downloads.
Missing metadata raises `FileNotFoundError`. Changing the main URL or cache root
invalidates the in-memory metadata table on its next lookup.

`ssc_remote_data_dir` controls definitive and predicted SSC orbit files. Its
`spdf` preset retains `https://cdaweb.gsfc.nasa.gov/pub/data/themis/`, independently
of the main source. For example:

```python
from pyspedas.projects.themis import config

config.set_data_source('heliocloud')  # Includes GMAG data and metadata
config.set_ssc_source('spdf')
```

Heliocloud holdings are being synchronized with SPDF; some files may remain
unavailable until ingest/backfilling completes. Coverage gaps do not select a
different provider automatically. Select `spdf` or another provider explicitly
when needed. Cache paths follow server layouts; existing files are not moved.

State version selection is unchanged: without `version`, `themis` uses the
unversioned current-file link, while `spdf` wildcards the version and selects the
highest available. An explicit version requests that exact file, which may not
be present on the selected server. Other instruments retain their existing
version defaults. Existing SPDF/S3 configurations must set `remote_data_layout`
to `spdf` explicitly.

The three source settings (`remote_data_dir`, `remote_data_layout`,
`ssc_remote_data_dir`) accept stored preferences under `[projects.themis]` and
matching `THM_*` environment variables. Environment settings override preferences.

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



