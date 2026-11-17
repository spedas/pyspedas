"""GOES-R L1b products and their instrument-specific time dependencies."""

import copy
from fnmatch import fnmatchcase

import numpy as np
from netCDF4 import Dataset

from pyspedas.tplot_tools import options, store_data, time_double
from pyspedas.tplot_tools import time_clip as tclip
from pyspedas.tplot_tools.importers.netcdf_to_tplot import _read_netcdf_variable
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download

from .config import CONFIG

# Explicit mappings from the IDL GOES-R loader; equal lengths alone are ambiguous.
_TIME_MAP = {
    "mag": {
        "IB_time": [
            "IB_data_uncorrected",
            "IB_mag_ACRF_uncorrected",
            "IB_mag_BRF_uncorrected",
            "IB_mag_ECI_uncorrected",
            "IB_mag_EPN_uncorrected",
            "IB_data",
            "IB_mag_ACRF",
            "IB_mag_BRF",
            "IB_mag_ECI",
            "IB_mag_EPN",
            "IB_status",
        ],
        "OB_time": [
            "OB_data_uncorrected",
            "OB_mag_ACRF_uncorrected",
            "OB_mag_BRF_uncorrected",
            "OB_mag_ECI_uncorrected",
            "OB_mag_EPN_uncorrected",
            "OB_data",
            "OB_mag_ACRF",
            "OB_mag_BRF",
            "OB_mag_ECI",
            "OB_mag_EPN",
            "OB_status",
        ],
        "report_time": ["Instrument_ID", "yaw_flip", "eclipse_flag", "ECEF_X", "ECEF_Y", "ECEF_Z", "solar_array_current"],
        "quat_timestamp": [
            "attitude_quat_Q0",
            "attitude_quat_Q1",
            "attitude_quat_Q2",
            "attitude_quat_Q3",
            "orbit_quat_Q0",
            "orbit_quat_Q1",
            "orbit_quat_Q2",
            "orbit_quat_Q3",
        ],
    },
    "xrs": {
        "time": [
            "irradiance_xrsa1",
            "irradiance_xrsa2",
            "primary_xrsa",
            "irradiance_xrsb1",
            "irradiance_xrsb2",
            "primary_xrsb",
            "xrs_ratio",
            "corrected_current_xrsa_1",
            "corrected_current_xrsa_2",
            "corrected_current_xrsa_3",
            "corrected_current_xrsa_4",
            "corrected_current_xrsb_1",
            "corrected_current_xrsb_2",
            "corrected_current_xrsb_3",
            "corrected_current_xrsb_4",
            "dispersion_angle",
            "crossdispersion_angle",
            "sc_power_side",
            "exis_flight_model",
            "exis_configuration_id",
            "xrs_runctrlmd",
            "integration_time",
            "exs_sl_pwr_ena",
            "asic1_temperature",
            "asic2_temperature",
            "invalid_flags",
            "xrs_det_chg",
            "xrs_mode",
            "sps_obs_time",
            "sps_int_time",
            "sps_temperature",
            "sps_det_chg",
            "num_angle_pairs",
            "yaw_flip_flag",
            "au_factor",
            "quality_flags",
            "packet_count",
            "fov_unknown",
            "fov_eclipse",
            "fov_lunar_transit",
            "fov_planet_transit",
            "fov_off_point",
            "quaternion_Q0",
            "quaternion_Q1",
            "quaternion_Q2",
            "quaternion_Q3",
            "ecef_X",
            "ecef_Y",
            "ecef_Z",
            "solar_array_current",
            "SC_eclipse_flag",
        ],
        "SPP_roll_angle_time": ["SPP_roll_angle"],
    },
}

_PRODUCTS = {
    "mag": ("mag-l1b-flat", "ops_mag-l1b-flat"),
    "xrs": ("exis-l1b-sfxr_science", "sci_exis-l1b-sfxr"),
    "euvs": ("exis-l1b-sfeu_science", "sci_exis-l1b-sfeu"),
    "mpsh": ("seis-l1b-mpsh_science", "sci_seis-l1b-mpsh"),
    "sgps": ("seis-l1b-sgps", "ops_seis-l1b-sgps"),
}
_SCIENCE = {
    "mag": ["IB_mag_ECI", "OB_mag_ECI"],
    "xrs": ["irradiance_xrs*", "primary_xrs*", "xrs_ratio"],
    "euvs": ["irradianceSpectrum", "avgIrradiance*", "lowWavelength", "highWavelength"],
    "mpsh": ["*Flux*"],
    "sgps": ["*Flux*"],
}


def _unix_time(variable):
    """Convert each clock independently, preserving sensor columns and missing times."""
    attrs = {key: variable.getncattr(key) for key in variable.ncattrs()}
    values = np.asarray(_read_netcdf_variable(variable, attrs), dtype=float)
    units = attrs.get("units", attrs.get("Units", attrs.get("UNITS")))
    cal = attrs.get("calendar", "standard")
    if cal not in ("standard", "gregorian", "proleptic_gregorian"):
        raise ValueError(f"Unsupported GOES time calendar: {cal}")
    if not isinstance(units, str) or " since " not in units.lower():
        raise ValueError(f"Invalid GOES time units: {units!r}")
    unit, epoch = units.split(" ", 1)
    epoch = epoch.strip()[len("since") :].strip()
    # Older MAG files append this description to the reference epoch.
    epoch = epoch.removesuffix(", neglecting leap seconds")
    scales = {
        "seconds": 1.0,
        "second": 1.0,
        "sec": 1.0,
        "s": 1.0,
        "milliseconds": 1.0e-3,
        "millisecond": 1.0e-3,
        "ms": 1.0e-3,
        "microseconds": 1.0e-6,
        "microsecond": 1.0e-6,
        "us": 1.0e-6,
        "minutes": 60.0,
        "minute": 60.0,
        "hours": 3600.0,
        "hour": 3600.0,
        "days": 86400.0,
        "day": 86400.0,
    }
    scale = scales.get(unit.lower())
    if scale is None or not epoch:
        raise ValueError(f"Unsupported GOES time units: {units!r}")
    return values * scale + time_double(epoch)


def _read_l1(files, instrument, prefix, suffix, get_support_data):
    """Merge record data along time; retain static tables once."""
    records, static, metadata = {}, {}, {}
    mapping = _TIME_MAP.get(instrument, {})
    dependencies = {name: clock for clock, names in mapping.items() for name in names}
    primary_clock = "L1a_SciData_TimeStamp" if instrument in ("mpsh", "sgps") else "time"
    for filename in sorted(set(files)):
        with Dataset(filename) as dataset:
            clock_names = list(mapping) if mapping else [primary_clock]
            time_arrays = {name: _unix_time(dataset[name]) for name in clock_names}
            global_attrs = {key: dataset.getncattr(key) for key in dataset.ncattrs()}
            for name, variable in dataset.variables.items():
                if name in time_arrays or np.dtype(variable.dtype).kind not in "fiu":
                    continue
                if not get_support_data and not any(fnmatchcase(name, pattern) for pattern in _SCIENCE[instrument]):
                    continue
                attrs = {key: variable.getncattr(key) for key in variable.ncattrs()}
                values = _read_netcdf_variable(variable, attrs)
                clock = dependencies.get(name) if mapping else primary_clock
                # Bind by netCDF dimension identity, never by coincident lengths.
                record = clock is not None and variable.dimensions and variable.dimensions[0] == dataset[clock].dimensions[0]
                base_attrs = {
                    "NETCDF": {"VATT": attrs, "GATT": global_attrs, "FILENAME": [filename], "TIME_VARIABLE": clock},
                    "data_att": {"units": attrs.get("units", "")},
                }
                for coord in ("ECI", "EPN", "ACRF", "BRF", "GSE", "GSM"):
                    if coord in name.split("_"):
                        base_attrs["data_att"]["coord_sys"] = coord
                if clock is None or not record:
                    # Unmapped MAG sample arrays have ambiguous IB/OB clocks.
                    if variable.dimensions and variable.dimensions[0] in ("sample_number", "report_number"):
                        continue
                    output = prefix + name + suffix
                    static.setdefault(output, values)
                    continue
                times = time_arrays[clock]
                split = (instrument == "mpsh" and values.ndim == 3 and variable.dimensions[1] == "direction") or (
                    instrument == "sgps" and values.ndim >= 2 and variable.dimensions[1] == "sensor_unit"
                )
                for index in range(values.shape[1]) if split else [None]:
                    output = prefix + name + (f"_{index}" if split else "") + suffix
                    y = values[:, index, ...] if split else values
                    x = times[:, index] if split and times.ndim == 2 else times
                    # Non-sensor SGPS housekeeping uses the first sensor's clock.
                    if x.ndim == 2:
                        x = x[:, 0]
                    valid = np.isfinite(x)
                    if not valid.any():
                        continue
                    records.setdefault(output, []).append((x[valid], y[valid]))
                    if output not in metadata:
                        metadata[output] = copy.deepcopy(base_attrs)
                        if split:
                            metadata[output]["sensor" if instrument == "sgps" else "telescope"] = index
                    elif filename not in metadata[output]["NETCDF"]["FILENAME"]:
                        metadata[output]["NETCDF"]["FILENAME"].append(filename)
    names = []
    for name, chunks in records.items():
        x = np.concatenate([chunk[0] for chunk in chunks])
        y = np.concatenate([chunk[1] for chunk in chunks], axis=0)
        order = np.argsort(x, kind="stable")
        if store_data(name, data={"x": x[order], "y": y[order]}, attr_dict=metadata[name]):
            names.append(name)
            if instrument == "xrs" and "irradiance" in name:
                options(name, "ylog", True)
    for name, values in static.items():
        if store_data(name, data={"y": values}):
            names.append(name)
    return names, list(records)


def _load_l1(trange, probe, instrument, prefix, suffix, downloadonly, no_update, time_clip, force_download, get_support_data):
    probes = list(probe) if isinstance(probe, (list, tuple)) else [probe]
    instruments = list(instrument) if isinstance(instrument, (list, tuple)) else [instrument]
    # Validate the whole request before downloading or creating variables.
    for prb in probes:
        if str(prb) not in ("16", "17", "18", "19"):
            raise ValueError("GOES L1 requires probes 16-19")
    if any(instr not in _PRODUCTS for instr in instruments):
        raise ValueError("GOES L1 instruments are mag, xrs, euvs, mpsh and sgps")
    names, out_files = [], []
    for prb in probes:
        for instr in instruments:
            directory, product = _PRODUCTS[instr]
            path = f"goes{prb}/l1b/{directory}/%Y/%m/{product}_g{prb}_d%Y%m%d_v?-?-?.nc"
            filenames = dailynames(file_format=path, trange=trange) or []
            files = (
                download(
                    remote_file=filenames,
                    remote_path=CONFIG["remote_goes_r"],
                    local_path=CONFIG["local_data_dir"],
                    no_download=no_update or CONFIG["no_download"],
                    force_download=force_download,
                    last_version=True,
                )
                or []
            )
            files = sorted(set(files))
            out_files.extend(files)
            if downloadonly or not files:
                continue
            local_prefix = f"g{prb}_{instr}_" if prefix in (None, "", "probename") else prefix
            created, record_names = _read_l1(files, instr, local_prefix, suffix or "", get_support_data)
            if time_clip and record_names:
                tclip(record_names, trange[0], trange[1], overwrite=True)
            names.extend(created)
    return sorted(set(out_files if downloadonly else names))
