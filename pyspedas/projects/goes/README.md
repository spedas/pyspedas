# GOES

Load GOES space environment data with `pyspedas.projects.goes`.
There are **two science file formats**: the original netCDF format and the
newer GOES-R format (also netCDF).

## Choose the data files

| Satellites | Files | Supported instrument loaders | How to select |
| --- | --- | --- | --- |
| GOES-15 and earlier | Original netCDF | `fgm`, `eps`, `epead`, `maged`, `magpd`, `hepad`, `xrs` | Default: `goes_r=False` |
| GOES-8–15 | Reprocessed data in GOES-R format | `mag` (high resolution only), `xrs` | Set `goes_r=True` |
| GOES-16 and later | GOES-R format, level 2 | `mag`, `xrs`, `euvs`, `mpsh`, `sgps` | Selected automatically by `probe`; no flag needed |
| GOES-16 and later | GOES-R format, level 1 | `mag`, `xrs`, `euvs`, `mpsh`, `sgps` | Set `level='l1'` |

For GOES-15 and earlier, original and reprocessed files are separate datasets.
Reprocessed coverage is limited to GOES-8–15 MAG and XRS; it does not include
the older particle instruments. Use **`fgm` for original magnetometer files**
and **`mag` for GOES-R-format magnetometer files**. 

Location for original netCDF files:
https://www.ncei.noaa.gov/data/goes-space-environment-monitor/access/

Location for the newer GOES-R files (modified netCDF format): 
https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes/

Location for reprocessed netCDF files for GOES8-15, in GOES-R file format:
https://www.ncei.noaa.gov/data/goes-space-environment-monitor/access/science/

Instrument and date availability varies by satellite. In the original archive,
`eps` is for GOES-8–12; `epead`, `maged`, and `magpd` are for GOES-13–15.
The loader names refer to magnetometers (`fgm`, `mag`), X-ray and extreme
ultraviolet sensors (`xrs`, `euvs`), and particle instruments (`eps`, `epead`,
`maged`, `magpd`, `hepad`, `mpsh`, `sgps`).

## Loading examples

Specify the satellite and time range explicitly. Each instrument function is
a shortcut for `goes.load(instrument="...")` and returns the created tplot
variable names.

```python
from pyspedas.projects import goes
from pyspedas import tplot

# Original netCDF: GOES-15 magnetometer, 1-minute averages
names = goes.fgm(probe="15", trange=["2013-11-05", "2013-11-06"], datatype="1min")
tplot("g15_fgm_BX_1")

# Reprocessed GOES-13 magnetometer in GOES-R format
names = goes.mag(probe="13", trange=["2015-01-01", "2015-01-02"], goes_r=True, datatype="hi")
tplot("g13_mag_b_gsm")

# Reprocessed GOES-13 XRS in GOES-R format, 1-minute averages
names = goes.xrs(probe="13", trange=["2015-01-20", "2015-01-21"], goes_r=True, datatype="1min")

# GOES-18: GOES-R format is selected automatically for probes 16+
names = goes.mag(probe="18", trange=["2023-01-01", "2023-01-02"], datatype="1min")
tplot(["g18_mag_b_gsm", "g18_mag_b_total"])
```

## Levels and resolution

GOES-R-format data default to **Level 2** (`level="l2"`). For GOES-16 and later,
choose the L2 resolution with `datatype`:

| Instrument | Resolution choices |
| --- | --- |
| `mag` | `"1min"` or `"hi"` (0.1 seconds) |
| `xrs` | `"1min"` or `"hi"` (1 second) |
| `euvs` | `"1min"` or `"low"` (1 day) |
| `mpsh`, `sgps` | `"1min"` or `"5min"` |

Reprocessed GOES-8–15 MAG always loads high-resolution data; XRS offers
`"1min"` averages or `"hi"` unaveraged data. For original netCDF files, choices
depend on the instrument and satellite: `"1min"`, `"5min"`, or `"full"` where
available (`fgm` also accepts `"512ms"`). EPS has averaged data only, and the
MAGPD loader offers `"1min"` or `"full"`. These keywords are not interchangeable
across instruments.

**Level 1b** is supported for GOES-16–19 with `mag`, `xrs`, `euvs`, `mpsh`, and
`sgps`. Select it with `level="l1"`; data use their native cadence, so `datatype`
does not select a resolution. Set `get_support_data=True` for auxiliary variables.

```python
names = goes.xrs(probe="16", trange=["2025-01-01", "2025-01-02"], level="l1")
tplot("g16_xrs_irradiance_xrsa1")
```

By default, variable names start with `g<probe>_<instrument>_`, and data are
clipped to `trange` (`time_clip=True`). Use `suffix` to distinguish repeated
loads, `downloadonly=True` to return filenames, or `no_update=True` to use only
cached files. Orbit data are loaded separately with `goes.orbit(...)` from SPDF
CDF files.

For Level 1b science loads, `get_support_data=False` (the default) selects the
primary science variables. Set `get_support_data=True` to also load available
auxiliary variables, such as quality flags and instrument temperatures. This
keyword has no effect on Level 2 or original netCDF science loads.
