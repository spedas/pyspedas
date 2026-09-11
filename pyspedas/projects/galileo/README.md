
# Galileo

Jupiter equatorial orbiter - Launch date 1989-10-13

Load Galileo ephemeris and magnetic field data from the University of Iowa DAS2
server into PySPEDAS tplot variables. The loader requests ASCII data and uses
the shared DAS2 utilities to parse the response and create the variables.

Browse the [Galileo DAS2 catalog](https://das2.org/browse/uiowa/galileo) for dataset
information and availability. The examples below use dates from the Galileo mission.

## Quick start

```python
from pyspedas import tplot
from pyspedas.projects.galileo.load import load

variables = load(
    trange=["1996-09-30 12:00:00", "1996-09-30 14:00:00"],
    datatype="jovicentric",
)

print(variables)
if variables:
    tplot(variables)
```

`pyspedas.projects.galileo.load()` returns a list of the created tplot variable names. Data availability
depends on the dataset, requested time range, and server response.

## Parameters

| Parameter | Description |
| --- | --- |
| `trange` | A list containing start and end times. Use ISO date/time strings such as `"1996-06-30T12:00:00"`. The end must be later than the start, and the range must not exceed two days. |
| `datatype` | A supported abbreviation or full dataset path from the table below. Abbreviations are case-insensitive; full paths are case-sensitive. |
| `prefix` | Optional prefix for output variable names. If empty or omitted, the loader uses the dataset-specific prefix shown in the table. |
| `suffix` | Optional text appended to every output variable name. Defaults to `""`. |
| `varnames` | Optional source names to select, without prefix or suffix. Names are case-sensitive; `longitude` and `long` both select ephemeris longitude. |
| `interval` | Ephemeris sampling interval in seconds, default `300`. MAG datasets use native cadence and omit this parameter. |

A supported `datatype` and a valid `trange` must be supplied. Invalid selectors
and invalid time ranges raise errors.

## Supported datatypes

The variable names below use the default prefix and no suffix. A custom prefix
or suffix changes these names. The `full_path` column is the directory in the DAS2 server and it also corresponds to the `full_set` field in `config.py`.

| **abrev** | **full_path** | **description** | **tplot vars loaded** |
| --- | --- | --- | --- |
| `jovicentric` | `Galileo/Ephemeris/Jovicentric` | Galileo Jupiter orbit parameters | `galileo_radius`, `galileo_longitude`, `galileo_mlat`, `galileo_lt`, `galileo_l`, `galileo_io_phase` |
| `fce` | `Galileo/MAG/Fce` | Cyclotron Electron Frequnecy | `galileo_fce` |
| `magnitude` | `Galileo/MAG/Magnitude` | Magnetic Field Magnitude  | `galileo_b_mag` |

| **var** |  **description** | **units** |
| --- | --- | --- | 
| radius | Distance from the center of Jupiter in Jovian radii | Rj|
| longitude| Jupiter System III longitude of the sub-spacecraft point| degrees |
| mlat| Magnetic Latitude |degrees |
| lt| Magnetic Local time of the sub-spacecraft point | hours |
| l| L Value | Rj |
| io_phase | Io phase | degrees |
| fce | Cyclotron Electron Frequnecy | Hz |
| b_mag | B-Field Magnitude | nT |


## Selecting a dataset by its full path

The user can either use the abbreviated datatype or the full path:

```python
variables = load(
    trange=["1997-06-30T12:00:00", "1997-06-30T14:00:00"],
    datatype="Galileo/MAG/Magnitude",
)
```

Using `datatype="magnitude"` or `datatype="MAGNITUDE"` selects the same entry.
With the default naming options, its output variable is `galileo_b_mag`.

## Custom variable names

A supplied prefix replaces the entire default prefix. The suffix is
appended after the source variable name:

```python
variables = load(
    trange=["1996-06-30T12:00:00", "1996-06-30T14:00:00"],
    datatype="magnitude",
    prefix="custom_",
    suffix="_example",
)
# Output name: custom_b_mag_example
```

## Reading data and metadata

Use the public PySPEDAS functions to retrieve loaded arrays and metadata:

```python
from pyspedas import get_data

data = get_data("galileo_b_mag")
metadata = get_data("galileo_b_mag", metadata=True)

stream_title = metadata["DAS2"]["STREAM_TITLE"]
variable_attributes = metadata["DAS2"]["VATT"]
```

Each variable carries the shared stream title and its own DAS2 attributes.
These metadata entries are not displayed as plot titles by default. Axis
labels and units come from the dataset's variable descriptors 
and can be modified by the user using pyspedas options.

## Dataset information

```python
from pyspedas.projects.galileo.load import get_info

print(get_info("fce"))
```

This prints information for the Galileo/MAG/Fce dataset.
