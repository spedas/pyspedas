# DMSP

Load Defense Meteorological Satellite Program space physics CDF products from
[NASA SPDF](https://spdf.gsfc.nasa.gov/pub/data/dmsp/).

| Loader | Instrument | Spacecraft |
| --- | --- | --- |
| `ssj()` | Precipitating electrons and ions | F06?F09, F12?F18 |
| `ssies()` | SSIES-3 thermal plasma | F16?F18 |
| `ssm()` | Magnetic field | F15?F18 |

Coverage depends on spacecraft and instrument. SSJ and SSM files are daily;
SSIES files cover individual orbits. The archive currently has only SSUSI
products for F19; this plug-in does not load SSUSI or the F19 particle observations
mentioned in [issue #1299](https://github.com/spedas/pyspedas/issues/1299).

```python
import pyspedas

variables = pyspedas.projects.dmsp.ssj(
    trange=['2014-01-01', '2014-01-02'], probe='18', time_clip=True)
plasma = pyspedas.projects.dmsp.ssies(
    trange=['2014-01-01', '2014-01-02'], probe='18')
field = pyspedas.projects.dmsp.ssm(
    trange=['2015-03-01', '2015-03-02'], probe='18')
```

All loaders accept `prefix`, `suffix`, `get_support_data`, `varformat`, `varnames`,
`downloadonly`, `notplot`, `no_update`, `force_download`, and `time_clip`.
`probe` accepts integers, strings such as `'f18'`, or a list. Original CDF variable
names are preserved: use distinct prefixes in separate calls if spacecraft names
would overlap. `notplot=True` returns raw data without time clipping.

Configuration follows mission preferences, then environment overrides:
`SPEDAS_DATA_DIR` sets a shared cache root, `DMSP_DATA_DIR` sets this mission's cache,
and `DMSP_NO_DOWNLOAD=1` disables downloads. `no_update=True` also uses only the cache.
Run unit tests with `python -m unittest pyspedas.projects.dmsp.tests.test_dmsp`.
