"""Load NOAA SWFO (SOLAR-1) daily netCDF products."""
from fnmatch import fnmatchcase
import gzip
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from netCDF4 import Dataset, num2date, date2num
import numpy as np

from pyspedas.tplot_tools import store_data, options, time_double
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download, configure_retry_session
from .config import CONFIG


def _latest(keys):
    """Keep the most recently processed file for each observation interval."""
    latest = {}
    for key in sorted(keys):
        match = re.search(r"(.+_s\d{8}T\d{6}Z_e\d{8}T\d{6}Z)_p", key)
        if match:
            latest[match[1]] = key
    return sorted(latest.values())


def _remote_keys(directory, dates):
    """List the archive's S3-compatible API, including paginated results."""
    keys = []
    with configure_retry_session() as session:
        for month in sorted({date[:6] for date in dates}):
            params = {"list-type": "2", "prefix": f"{directory}/{month[:4]}/{month[4:]}/"}
            while True:
                response = session.get(CONFIG["remote_data_dir"], params=params, timeout=60)
                response.raise_for_status()
                root = ET.fromstring(response.content)
                keys.extend(node.text for node in root.findall("{*}Contents/{*}Key")
                            if node.text.endswith((".nc", ".nc.gz"))
                            and any(f"_s{date}T" in node.text for date in dates))
                token = root.findtext("{*}NextContinuationToken")
                if not token:
                    break
                params["continuation-token"] = token
    return _latest(keys)


def _read(files, prefix, suffix, varformat, varnames, trange, clip):
    """Read each variable using its own time coordinate, retaining metadata."""
    result = {}
    for filename in sorted(files):
        if str(filename).endswith(".gz"):
            with gzip.open(filename, "rb") as stream:
                dataset = Dataset("swfo.nc", memory=stream.read())
        else:
            dataset = Dataset(filename)
        with dataset as ds:
            global_attrs = {key: ds.getncattr(key) for key in ds.ncattrs()}
            for name, variable in ds.variables.items():
                if not variable.dimensions or variable.dtype.kind not in "iuf":
                    continue
                dimension = variable.dimensions[0]
                time_name = "sweep_mid_time" if dimension == "sweep" else dimension
                if time_name not in ds.variables or name == time_name:
                    continue
                if varformat and not fnmatchcase(name, varformat):
                    continue
                if varnames and name not in varnames:
                    continue
                clock = ds.variables[time_name]
                units = getattr(clock, "units", "").split(", corrected")[0]
                if "since" not in units:
                    continue
                calendar = getattr(clock, "calendar", "standard")
                dates = num2date(clock[:], units, calendar=calendar)
                x = np.asarray(date2num(dates, "seconds since 1970-01-01", calendar=calendar))
                y = np.ma.asarray(variable[:], dtype=float).filled(np.nan)
                if not y.shape or y.shape[0] != len(x):
                    continue
                attrs = {key: variable.getncattr(key) for key in variable.ncattrs()}
                item = {"x": x, "y": y, "attrs": {"NETCDF": {
                    "VATT": attrs, "GATT": global_attrs}}}
                # STIS energy channels are time-dependent and supplied in MeV.
                energy_name = name.replace("_flux_", "_energy_").removesuffix("_uncert")
                if "_flux_" in name and energy_name in ds.variables:
                    item["v"] = np.ma.asarray(ds[energy_name][:], dtype=float).filled(np.nan)
                target = prefix + name + suffix
                if target in result:
                    previous = result[target]
                    for axis in ("x", "y", "v"):
                        if axis in item:
                            item[axis] = np.concatenate((previous[axis], item[axis]), axis=0)
                result[target] = item
    for item in result.values():
        order = np.argsort(item["x"], kind="stable")
        ordered = item["x"][order]
        keep = np.r_[True, ordered[1:] != ordered[:-1]] if len(order) else np.array([], dtype=bool)
        if clip:
            keep &= (ordered >= trange[0]) & (ordered <= trange[1])
        for axis in ("x", "y", "v"):
            if axis in item:
                item[axis] = item[axis][order][keep]
    return result


def load(trange=("2026-10-01", "2026-10-02"), instrument="mag", level="l2",
         science=False, prefix="", suffix="", varformat=None, varnames=None,
         downloadonly=False, notplot=False, no_update=False, time_clip=False,
         force_download=False):
    """Load SWFO / SOLAR-1 MAG, SWiPS or STIS data from NOAA NCEI.

    Parameters
    ----------
    trange : sequence, optional
        Start and end times, in strings or Unix seconds.
    instrument : str, optional
        'mag', 'swips', or 'stis'; instrument wrappers set this automatically.
    level : str, optional
        Product level: 'l0b', 'l1a', 'l1b', 'l2' (default), or 'l3'.
        STIS science L3 uses 'l3-avg1m-nt-bc'.
    science : bool, optional
        Select retrospective science products rather than operational products.
        Availability depends on the instrument, level and date.
    prefix, suffix : str, optional
        Add to variable names around the default 'swfo_<instrument>_<level>_'.
    varformat : str, optional
        Wildcard pattern selecting original netCDF variable names.
    varnames : sequence of str, optional
        Select original netCDF variable names (combined with varformat).
    downloadonly : bool, optional
        Return downloaded compressed netCDF filenames without importing data.
    notplot : bool, optional
        Return a dictionary of arrays and metadata without creating variables.
    no_update : bool, optional
        Use cached files without contacting NOAA.
    time_clip : bool, optional
        Restrict returned samples to the requested inclusive time range.
    force_download : bool, optional
        Download even when the selected file is already cached.

    Returns
    -------
    list of str or dict
        Created tplot names, downloaded filenames, or raw data with notplot.

    Notes
    -----
    All numeric time-dependent variables, including quality flags, are loaded.
    Flags are retained without applying a science-quality mask. Missing values
    become NaN. CCOR image products are outside this in situ loader's scope.
    """
    instrument = instrument.lower()
    level = level.lower()
    if instrument not in {"mag", "swips", "stis"}:
        raise ValueError("instrument must be mag, swips or stis")
    if level not in {"l0b", "l1a", "l1b", "l2", "l3", "l3-avg1m-nt-bc"}:
        raise ValueError("Unsupported SWFO product level")
    if level == "l3-avg1m-nt-bc" and (instrument != "stis" or not science):
        raise ValueError("l3-avg1m-nt-bc requires STIS science data")
    if science and instrument == "stis" and level == "l3":
        level = "l3-avg1m-nt-bc"
    if trange is None or len(trange) != 2:
        raise ValueError("trange must contain a start and end time")
    bounds = np.asarray(time_double(trange), dtype=float)
    if not np.all(np.isfinite(bounds)) or bounds[0] > bounds[1]:
        raise ValueError("trange must contain finite, increasing times")
    dates = dailynames(file_format="%Y%m%d", trange=bounds.tolist())
    directory = f"SWFO/SOLAR-1/{instrument.upper()}/{instrument}-{level}"
    if science:
        directory += "_science"
    cache_only = no_update or CONFIG["no_download"]
    cache = Path(CONFIG["local_data_dir"])
    if cache_only:
        keys = _latest([path.relative_to(cache).as_posix()
                        for path in (cache / directory).glob("*/*/*")
                        if path.is_file() and path.name.endswith((".nc", ".nc.gz"))
                        and any(f"_s{date}T" in path.name for date in dates)])
    else:
        keys = _remote_keys(directory, dates)
    files = []
    for key in keys:
        found = download(remote_file=key, remote_path=CONFIG["remote_data_dir"],
                         local_path=str(cache), no_download=cache_only,
                         force_download=force_download)
        if found:
            files.extend(found if isinstance(found, list) else [found])
    files = sorted(set(files))
    if downloadonly:
        return files
    pre = (prefix or "") + f"swfo_{instrument}_{level}_" + ("science_" if science else "")
    data = _read(files, pre, suffix or "", varformat, varnames, bounds, time_clip)
    if notplot:
        return data
    stored = []
    for name, item in data.items():
        if store_data(name, data={k: v for k, v in item.items() if k != "attrs"},
                      attr_dict=item["attrs"]):
            stored.append(name)
            units = item["attrs"]["NETCDF"]["VATT"].get("units")
            if units:
                options(name, "ysubtitle", units)
            if "v" in item:
                options(name, "spec", True)
    return stored
