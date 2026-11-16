# FDSN/MTH5 data model

FDSN (Federation of Digital Seismograph Networks) defines the data and
metadata conventions that EarthScope and similar archives use for
time-series instrument data, including magnetotelluric magnetic and
electric field measurements. MTH5 is an HDF5-based container format that
stores FDSN-sourced data and metadata in a hierarchy suited to analysis.
This document describes that data model: how data is identified, organized,
and calibrated to physical units.

## FDSN/SEED channel naming

A channel is identified by a three-character SEED code:
`<band><instrument><orientation>`.

- **Band code**: indicates sample rate, e.g. `M`, `L`, `V`, `U`.
- **Instrument code**: indicates the measured field. `F` is magnetic field;
  `Q` is electric field.
- **Orientation code**: `Z`, `N`, `E` (vertical, north, east) are the most
  common convention. Some stations instead use numeric orientations `1`,
  `2`, `3` for either instrument code.

The SEED manual (appendix A) is the authoritative reference for these
codes. Examples: `LFE`, `LFN`, `LFZ` are magnetic channels (band `L`,
instrument `F`); `LQE`, `LQN` are electric channels (band `L`, instrument
`Q`) for the same orientations.

Wildcards (`?` for one character, `*` for multiple) are useful for the band
position, since a station may record a field at several sample rates.
Wildcards should be avoided in the orientation position: the instrument
code alone is not a safe filter, since other channel types can coincidentally
share a letter (for example `VFP`, a station-health "packet buffer usage"
channel, ends in `F` but is not magnetic field data).

## FDSN hierarchy

FDSN organizes data as `network` → `station` → `channel`, where a network
is a two-character code, a station is a physical observatory, and a channel
is one instrument data stream identified by its SEED code.

## MTH5 hierarchy

MTH5 adds two levels around the FDSN hierarchy and renames `network`:

`experiment` (optional top level, holds multiple surveys) → `survey`
(MTH5's analog of FDSN's `network`) → `station` → `run` (a contiguous
acquisition interval, identified by a letter such as `a`, `b`, `c`) →
`channel` (one component's time series within that run).

A station's full history may span many runs with gaps between them (e.g. an
instrument deployment interrupted and resumed); a single request time range
can fall inside one run or span several. Programmatic access to the metadata
hierarchy (survey → station → run → channel) mirrors a station's "channel
summary" or "run summary" table, which lists each run's time coverage,
components, and sample rate without requiring the time-series data itself to
be downloaded first.

## Component naming: FDSN channel → MTH5 component

| FDSN channel (examples) | MTH5 component | Field |
|---|---|---|
| `?FE`, `?FN`, `?FZ`, `?F1`, `?F2`, `?F3` | `hx`, `hy`, `hz` | Magnetic |
| `?QE`, `?QN`, `?QZ`, `?Q1`, `?Q2`, `?Q3` (e.g. `LQE`, `LQN`) | `ex`, `ey` | Electric |

Both orientation conventions (`E`/`N`/`Z` and `1`/`2`/`3`) end up under the
same `hx`/`hy`/`hz` (or `ex`/`ey`) component names — MTH5 handles that
translation internally.

MTH5 components are accessed per run as `run.get_channel(<component>)`,
returning a `ChannelTS` object; a full run's components together form a
`RunTS`. Both expose the same calibration API regardless of field type.

## Filter chain and calibration

Each channel carries an ordered filter chain, inspectable via
`channel.channel_response`, that converts the raw digital-counts time series
to physical units. Applying this chain (`remove_instrument_response()` on a
`ChannelTS`, or `calibrate()` on a `RunTS`) produces calibrated data; the raw
and calibrated forms differ in units and in which filter stages are marked
`applied`.

- **Magnetic** filter chain (typical fluxgate magnetometer): an analog
  low-pass stage (nanoTesla → Volt), an analog-to-digital stage (Volt →
  digital counts, reversed on calibration), and a sub-second time-offset
  stage (not applied by default). Calibrated output units: **nanoTesla
  (nT)**.
- **Electric** filter chain: an SI-units stage (milliVolt per kilometer →
  Volt per meter), a dipole-length stage named by the dipole length in
  meters (e.g. `electric_dipole_92.000`; Volt per meter → Volt, the dipole
  separation that converts field strength to measured voltage), analog
  low-pass/high-pass stages, an analog-to-digital stage, and a time-offset
  stage. Calibrated output units: **milliVolt per kilometer (mV/km)** — not
  a raw voltage, since the dipole-length stage already divides out the
  physical separation between electrodes.

Filter stage presence and units are metadata properties of the specific
station and run, not a fixed property of the instrument code. A channel
whose filter chain is missing a stage, or whose units are unknown, cannot be
calibrated to physical units without resolving that metadata first:
assuming a dipole length or treating an uncalibrated voltage as a field
value produces silently incorrect results.

## Request tables

FDSN requests to MTH5 clients are expressed as a table with one row per
requested channel-time-range pair, with columns `network`, `station`,
`location`, `channel`, `start`, `end`. This table can be built
programmatically (e.g. one row per channel code of interest) or loaded from
a CSV, and is the structure MTH5's FDSN client methods expect as input
regardless of which field(s) the requested channels measure.
