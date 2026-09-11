# Juno

Jupiter polar orbiter - Launch date 2011-08-05

Load Juno ephemeris and magnetic field data from the University of Iowa DAS2
server into PySPEDAS tplot variables. The loader requests ASCII data and uses
the shared DAS2 utilities to parse the response and create the variables.

Browse the [Juno DAS2 catalog](https://das2.org/browse/uiowa/juno) for dataset
information and availability.

## Quick start

```python
from pyspedas import tplot
from pyspedas.projects.juno.load import load

variables = load(
    trange=["2020-02-02T12:00:00", "2020-02-02T14:00:00"],
    datatype="jovicentric",
)

print(variables)
if variables:
    tplot(variables)
```

`load()` returns a list of the created tplot variable names. Data availability
depends on the dataset, requested time range, and server response.

## Parameters

| Parameter | Description |
| --- | --- |
| `trange` | A list containing start and end times. Use ISO date/time strings such as `"2020-02-02T12:00:00"`. The end must be later than the start, and the range must not exceed two days. |
| `datatype` | A supported abbreviation or full dataset path from the table below. Abbreviations are case-insensitive; full paths are case-sensitive. |
| `prefix` | Optional prefix for output variable names. If empty or omitted, the loader uses the configured abbreviation followed by `_`. |
| `suffix` | Optional text appended to every output variable name. Defaults to `""`. |
| `interval` | Sampling interval passed to the DAS2 server, in seconds. Defaults to `300`; its effect depends on the dataset. |

A supported `datatype` and a valid `trange` must be supplied. Invalid selectors
and invalid time ranges raise errors.

## Supported datatypes

The "tplot vars" variable names below use the default prefix and no suffix. A custom prefix
or suffix changes these names. The `full_path` column is the directory in the DAS2 server and it also corresponds to the `full_set` field in `config.py`. The "params" column shows optional variables that might be available for each datatype. 

| **abrev** | **full_path** | **description** | **tplot vars** | **params**|
| --- | --- | --- | --- | --- |
| `europa` | `Juno/Ephemeris/EuropaCoRotational` | Juno Europa Co-Rotational orbit | `europa_x`, `europa_y`, `europa_z`, `europa_radius` | JLAT JALT JPLG SALT |
| `ganymede` | `Juno/Ephemeris/GanymedeCoRotational` | Juno Ganymede Co-Rotational orbit | `ganymede_x`, `ganymede_y`, `ganymede_z`, `ganymede_radius` | JLAT JALT JPLG SALT |
| `geocentric` | `Juno/Ephemeris/Geocentric` | Juno Earth orbit parameters | `geocentric_radius`, `geocentric_mlat`, `geocentric_mlt`, `geocentric_l_shell` | None |
| `heliocentric` | `Juno/Ephemeris/Heliocentric` | Juno Solar orbit parameters | `heliocentric_radius`, `heliocentric_lon`, `heliocentric_lat` | None |
| `io` | `Juno/Ephemeris/IoCoRotational` | Juno Io Co-Rotational orbit parameters | `io_x`, `io_y`, `io_z`, `io_radius` | JLAT JALT JPLG SALT |
| `jse` | `Juno/Ephemeris/JSE_Attitude` | Juno Jupiter Solar Ecliptic Pointing angles | `jse_phi`, `jse_theta`, `jse_omega` | None |
| `jovicentric` | `Juno/Ephemeris/Jovicentric` | Juno Jupiter orbit parameters | `jovicentric_radius`, `jovicentric_long`, `jovicentric_mlat`, `jovicentric_mlt`, `jovicentric_L`, `jovicentric_io_phase` | JLAT JALT JPLG CLAT JULT SALT |
| `electron` | `Juno/FGM/ElectronCyclotron` | Electron Cyclotron Resonance Frequency | `electron_fce` | None |
| `mag` | `Juno/FGM/MagComponents` | Quicklook Magnetic Field Components in Payload, Planetocentric or Sun State Coordinates | `mag_x`, `mag_y`, `mag_z`, `mag_mag` | None |
| `magnitude` | `Juno/FGM/Magnitude` | Magnetic Field Magnitude from payload coordinates data | `magnitude_mag` | None |

## Selecting a dataset by its full path

The "abrev" and "full_path" selectors identify the same dataset:

```python
variables = load(
    trange=["2020-02-02T12:00:00", "2020-02-02T14:00:00"],
    datatype="Juno/FGM/Magnitude",
    interval=300,
)
```

Using `datatype="magnitude"` or `datatype="MAGNITUDE"` selects the same entry.
With the default naming options, its output variable is `magnitude_mag`.

## Custom variable names

A supplied prefix replaces the default abbreviation prefix. The suffix is
appended after the source variable name:

```python
variables = load(
    trange=["2020-02-02T12:00:00", "2020-02-02T14:00:00"],
    datatype="magnitude",
    prefix="juno_",
    suffix="_example",
)
# Output name: juno_mag_example
```

## Reading data and metadata

Use the public PySPEDAS functions to retrieve loaded arrays and metadata:

```python
from pyspedas import get_data

data = get_data("magnitude_mag")
metadata = get_data("magnitude_mag", metadata=True)

stream_title = metadata["DAS2"]["STREAM_TITLE"]
variable_attributes = metadata["DAS2"]["VATT"]
```

Each variable carries the shared stream title and its own DAS2 attributes.
These metadata entries are not displayed as plot titles by default. Axis
labels and units come from the dataset's variable descriptors.
