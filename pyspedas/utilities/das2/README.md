# DAS2 utilities

Request data and dataset information from DAS2 servers, parse ASCII responses,
and create PySPEDAS tplot variables. These utilities are used by the
[Juno loader](../../projects/juno/README.md).

Currently, functions in this directory support DAS 2.1 server API, but only ASCII responses. 

## Main Functions

| Function | Purpose |
| --- | --- |
| `das2ascii()` | Download ASCII response text. Use `server="dataset"` for data requests. |
| `das2tplot()` | Convert ASCII response text into tplot variables. |
| `das2info()` | Request dataset listings (`list`), peer servers (`peers`), or dataset definitions (`dsdf`). |

## Example

```python
from pyspedas import tplot
from pyspedas.utilities.das2.das2ascii import das2ascii
from pyspedas.utilities.das2.das2tplot import das2tplot

data = das2ascii(
    url="https://jupiter.physics.uiowa.edu/das/server",
    server="dataset",
    dataset="Juno/Ephemeris/Jovicentric",
    start_time="2020-01-01T01:00:00",
    end_time="2020-01-01T02:00:00",
    interval=300,
    extra="ascii=true",
)

if data:
    variables = das2tplot(data, prefix="jovicentric_")
    if variables:
        tplot(variables)
```

## Notes

- Output names are `prefix + source_name.lower() + suffix`.
- Labels and units support common Autoplot codes, such as `R!bJ!n` → `R_J`.
- Parsing currently supports scalar ASCII time series, not binary data or
  spectra. Coordinate systems are not inferred from the dataset.
