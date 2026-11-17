# SWFO / SOLAR-1

Load NOAA Space Weather Follow-On MAG, SWiPS and STIS in situ products:

```python
import pyspedas

names = pyspedas.projects.swfo.mag(
    trange=['2026-10-01', '2026-10-02'], level='l3',
    varnames=['b_gse_min', 'b_gsm_min'], time_clip=True)
pyspedas.tplot(names)
plasma = pyspedas.projects.swfo.swips(
    trange=['2026-10-01', '2026-10-02'], notplot=True)
```

The [NOAA SWFO page](https://www.ncei.noaa.gov/products/space-weather/swfo)
links to the operational and retrospective science archives. Files are daily,
gzip-compressed netCDF; the loader selects the latest processing timestamp for
each observation interval. `science=True` selects retrospective products where
available. STIS science `level='l3'` selects `l3-avg1m-nt-bc`.

Use `downloadonly=True` for file paths, `no_update=True` for offline cache use,
`force_download=True` to refresh files, and `varformat`/`varnames` to select
original file variables. `notplot=True` returns dictionaries containing `x`, `y`,
optional energy coordinates `v`, and netCDF metadata in `attrs`. `time_clip=True`
works for both tplot and dictionary output. Quality flags are retained; the
loader does not mask data by quality flag. Missing values become NaN.

Variables use `swfo_<instrument>_<level>_` prefixes, with `science_` added for
science products. User `prefix` and `suffix` surround these names. MAG L3 retains
both native time axes, and STIS fluxes retain time-dependent energy coordinates.
CCOR FITS images are not handled by this in situ loader.

Set `SWFO_DATA_DIR` or `SPEDAS_DATA_DIR` to choose a cache directory, and
`SWFO_NO_DOWNLOAD=true` to enforce cache-only loading. Configuration preferences
are supported under `[projects.swfo]`. Product availability depends on date,
instrument and level; an empty archive selection returns an empty list or dict.
