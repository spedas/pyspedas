"""Find and optionally remove local MMS CDF files withdrawn from the SDC."""

import logging
import math
import os
import re
import stat
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from pyspedas.tplot_tools import time_double
from pyspedas.utilities.download import is_fsspec_uri

from .config import CONFIG
from .mms_file_filter import mms_file_filter
from .mms_login_lasp import mms_login_lasp

logger = logging.getLogger(__name__)

_FILENAME = re.compile(
    r"(?P<probe>mms[1-4])_(?P<instrument>[a-z0-9]+)_"
    r"(?P<rate>[a-z0-9]+)_(?P<level>[a-z0-9]+)"
    r"(?:_(?P<datatype>[a-z0-9_-]+))?_"
    r"(?P<date>[0-9]{14}|[0-9]{8})_v[0-9]+\.[0-9]+\.[0-9]+\.cdf"
)


def _selection(value):
    if value is None:
        return None
    if isinstance(value, (str, int)):
        value = [value]
    return {str(item).lower() for item in value}


def _snapshot(path):
    """Reject links and record enough metadata to detect a changed file."""
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode):
        raise RuntimeError(f"Not a regular local file: {path}")
    return info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns


def _check_candidate(root, path, snapshot):
    if any(parent.is_symlink() for parent in path.parents if parent == root or root in parent.parents):
        raise RuntimeError(f"MMS file directory changed during cleanup: {path}")
    if _snapshot(path) != snapshot:
        raise RuntimeError(f"MMS file changed during cleanup: {path}")


def _local_files(root, mirror, selections, start, end):
    groups = defaultdict(list)

    def walk_error(error):
        raise error

    for directory, directories, filenames in os.walk(root, onerror=walk_error):
        parent = Path(directory)
        directories[:] = sorted(name for name in directories if not (parent / name).is_symlink() and (parent / name) != mirror)
        for filename in sorted(filenames):
            match = _FILENAME.fullmatch(filename)
            if match is None:
                continue
            probe, instrument, rate, level, datatype, date = match.groups()
            values = (probe[3:], instrument, rate, level, datatype or "")
            if any(selected is not None and value not in selected for value, selected in zip(values, selections)):
                continue
            try:
                timestamp = datetime.strptime(date, "%Y%m%d%H%M%S" if len(date) == 14 else "%Y%m%d")
            except ValueError:
                continue
            if not start <= timestamp.replace(tzinfo=timezone.utc).timestamp() < end:
                continue
            parts = [probe, instrument, rate, level]
            if datatype:
                parts.append(datatype)
            parts.extend([date[:4], date[4:6]])
            if rate == "brst":
                parts.append(date[6:8])
            path = parent / filename
            if parent != root.joinpath(*parts) or path.is_symlink():
                continue
            groups[(probe, instrument, rate, level, datatype or "")].append((path, _snapshot(path)))
    return groups


def _sdc_files(session, url, params):
    """Require a successful, complete metadata response, including for absence."""
    with session.get(url, params=params, timeout=30, allow_redirects=False) as response:
        if response.status_code != 200:
            raise RuntimeError(f"MMS SDC returned HTTP {response.status_code}; no files removed.")
        try:
            payload = response.json()
        except ValueError as error:
            raise RuntimeError("Invalid MMS SDC JSON; no files removed.") from error
    if (
        not isinstance(payload, dict)
        or payload.get("files_were_truncated") is not False
        or not isinstance(payload.get("files"), list)
    ):
        raise RuntimeError("Invalid or truncated MMS SDC response; no files removed.")
    names = set()
    for entry in payload["files"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("file_name"), str):
            raise RuntimeError("Invalid MMS SDC file metadata; no files removed.")  # noqa: TRY004
        if _FILENAME.fullmatch(entry["file_name"]) is None:
            raise RuntimeError("Invalid MMS SDC filename; no files removed.")
        names.add(entry["file_name"])
    return names


def mms_remove_old_files(
    trange=None,
    probes=None,
    instruments=None,
    data_rates=None,
    levels=None,
    datatypes=None,
    latest_version=False,
    major_version=False,
    min_version=None,
    cdf_version=None,
    dry_run=True,
    always_prompt=False,
):
    """Find local MMS CDF files no longer listed by the Science Data Center.

    Parameters
    ----------
    trange : sequence of str or float, optional
        Start and end times. Select files by their filename's start timestamp,
        including the start and excluding the end. Defaults to the full mission
        (2015-03-01 through the current time).
    probes : str, int or sequence, optional
        Spacecraft numbers, e.g. ``'1'`` or ``[1, 2]``. Default: all spacecraft.
    instruments : str or sequence of str, optional
        Instrument names, e.g. ``'fgm'``. Default: all local instruments.
    data_rates : str or sequence of str, optional
        Data rates, e.g. ``'srvy'`` or ``'brst'``. Default: all local rates.
    levels : str or sequence of str, optional
        Processing levels. Default: all local levels. With public access, only
        L2 files are checked; other levels are retained with a warning.
    datatypes : str or sequence of str, optional
        Descriptors, e.g. ``'dis-moms'``; use ``''`` for files without a
        descriptor. Default: all descriptors.
    latest_version : bool, optional
        Check only the latest full CDF version within each selected product.
    major_version : bool, optional
        Check only the latest major CDF version within each selected product.
    min_version : str, optional
        Check only CDF versions at or above this version.
    cdf_version : str, optional
        Check only this exact CDF version. Version selection uses
        ``mms_file_filter`` with its usual precedence.
    dry_run : bool, optional
        If True (default), return a preview without deleting files. Set False
        explicitly to delete the candidates after all remote checks succeed.
    always_prompt : bool, optional
        Request SDC credentials even if saved credentials are available.

    Returns
    -------
    dict
        ``files`` is the list of absolute candidate paths, ``total_size`` is
        their combined size in bytes, and ``deleted`` lists paths actually
        removed (empty during a dry run).

    Raises
    ------
    ValueError
        For an invalid time range, a non-local data directory, or a local
        directory inside the configured read-only mirror.
    TypeError
        If ``dry_run`` is not a boolean.
    RuntimeError
        If offline mode is enabled, an SDC response is unsuccessful, malformed
        or truncated, a health check fails, or a candidate changes during the
        check. No deletion begins until remote checks and file checks finish.
    requests.RequestException
        If a metadata request fails. No files are removed.
    OSError
        If scanning, reading metadata or deleting a local file fails. A deletion
        error can occur after earlier candidates have already been removed.

    Notes
    -----
    This follows IDL's ``mms_remove_old_files``: absence from the SDC determines
    obsolescence, rather than comparing local version numbers. Internet access
    is required. No CDF data are downloaded or read.

    Only regular CDF files in the standard MMS directory layout beneath
    ``CONFIG['local_data_dir']`` are considered. Symbolic links and the
    configured read-only mirror are skipped; cloud paths are unsupported.
    Non-L2 products require authenticated access and a nonempty listing for
    that product on the first selected local file's day. Otherwise they are
    retained because their visibility cannot be established.

    Each batch includes a known available filename to detect unexpectedly empty
    responses. Every candidate is checked again for local changes before any
    deletion. Avoid running downloads or other cache maintenance concurrently.

    Examples
    --------
    >>> from pyspedas.projects.mms import mms_remove_old_files
    >>> preview = mms_remove_old_files(  # doctest: +SKIP
    ...     trange=['2015-12-15', '2015-12-16'], probes='1', instruments='fgm')
    >>> print(preview['files'], preview['total_size'])  # doctest: +SKIP
    >>> result = mms_remove_old_files(  # doctest: +SKIP
    ...     trange=['2015-12-15', '2015-12-16'], probes='1', instruments='fgm',
    ...     dry_run=False)
    """
    if not isinstance(dry_run, bool):
        raise TypeError("dry_run must be True or False.")
    if trange is None:
        start, end = time_double("2015-03-01"), datetime.now(timezone.utc).timestamp()
    else:
        if isinstance(trange, str) or len(trange) != 2:
            raise ValueError("trange must contain a start and end time.")
        start, end = (float(time_double(value)) for value in trange)
    if not all(math.isfinite(value) for value in (start, end)) or start >= end:
        raise ValueError("trange must contain finite times with start before end.")

    local_dir = os.path.expandvars(os.path.expanduser(os.fspath(CONFIG["local_data_dir"])))
    if is_fsspec_uri(local_dir):
        raise ValueError("MMS cleanup supports local filesystem paths only.")
    root = Path(local_dir).resolve()
    mirror_dir = CONFIG.get("mirror_data_dir")
    mirror = None
    if mirror_dir is not None and not is_fsspec_uri(os.fspath(mirror_dir)):
        mirror = Path(os.path.expandvars(os.path.expanduser(os.fspath(mirror_dir)))).resolve()
        if root == mirror or mirror in root.parents:
            raise ValueError("The local data directory is inside the read-only MMS mirror.")
    selections = [_selection(value) for value in (probes, instruments, data_rates, levels, datatypes)]
    groups = _local_files(root, mirror, selections, start, end)
    for key, files in groups.items():
        selected = set(
            mms_file_filter(
                [str(path) for path, _ in files],
                latest_version=latest_version,
                major_version=major_version,
                min_version=min_version,
                version=cdf_version,
            )
        )
        groups[key] = [(path, info) for path, info in files if str(path) in selected]
    result = {"files": [], "total_size": 0, "deleted": []}
    if not any(groups.values()):
        logger.info("No matching local MMS files found.")
        return result
    if CONFIG.get("no_download"):
        raise RuntimeError("MMS cleanup requires internet access; no_download is enabled.")

    session, user = mms_login_lasp(always_prompt=always_prompt)
    candidates = []
    try:
        url = f"https://lasp.colorado.edu/mms/sdc/{'sitl' if user else 'public'}/files/api/v1/file_info/science"
        control_files = _sdc_files(
            session,
            url,
            {
                "sc_id": "mms1",
                "instrument_id": "fgm",
                "data_rate_mode": "srvy",
                "data_level": "l2",
                "start_date": "2015-12-15",
                "end_date": "2015-12-16",
            },
        )
        if not control_files or any(
            not name.startswith("mms1_fgm_srvy_l2_") or _FILENAME.fullmatch(name)["date"] not in {"20151215", "20151216"}
            for name in control_files
        ):
            raise RuntimeError("MMS SDC health check failed; no files removed.")
        control = min(control_files)
        for (probe, instrument, rate, level, datatype), files in sorted(groups.items()):
            if not files:
                continue
            batch_control = control
            if level != "l2":
                if not user:
                    logger.warning(
                        "Retaining %s %s %s %s %s: authenticated access required.", probe, instrument, rate, level, datatype
                    )
                    continue
                date = _FILENAME.fullmatch(files[0][0].name)["date"][:8]
                day = datetime.strptime(date, "%Y%m%d").strftime("%Y-%m-%d")
                params = {
                    "sc_id": probe,
                    "instrument_id": instrument,
                    "data_rate_mode": rate,
                    "data_level": level,
                    "start_date": day,
                    "end_date": day,
                }
                if datatype:
                    params["descriptor"] = datatype
                visible = _sdc_files(session, url, params)
                prefix = "_".join(filter(None, (probe, instrument, rate, level, datatype))) + "_"
                if not visible or any(
                    _FILENAME.fullmatch(name).groups()[:5] != (probe, instrument, rate, level, datatype or None)
                    or _FILENAME.fullmatch(name)["date"][:8] != date
                    for name in visible
                ):
                    logger.warning("Retaining %s: product visibility could not be established.", prefix)
                    continue
                batch_control = min(visible)
            # Bound URL sizes and include a positive control in every batch.
            for offset in range(0, len(files), 25):
                batch = files[offset : offset + 25]
                requested = {path.name for path, _ in batch} | {batch_control}
                available = _sdc_files(session, url, {"file": ",".join(sorted(requested))})
                if batch_control not in available or not available <= requested:
                    raise RuntimeError("MMS SDC filename check failed; no files removed.")
                candidates.extend((path, info) for path, info in batch if path.name not in available)
    finally:
        session.close()

    candidates.sort(key=lambda item: str(item[0]))
    for path, info in candidates:
        _check_candidate(root, path, info)
    result["files"] = [str(path) for path, _ in candidates]
    result["total_size"] = sum(info[2] for _, info in candidates)
    logger.info(
        "%s %d obsolete MMS files (%d bytes).",
        "Would remove" if dry_run else "Removing",
        len(candidates),
        result["total_size"],
    )
    if not dry_run:
        for path, info in candidates:
            _check_candidate(root, path, info)
            path.unlink()
            result["deleted"].append(str(path))
            logger.info("Removed %s", path)
    return result
