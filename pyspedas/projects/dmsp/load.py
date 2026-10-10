"""Load DMSP space physics CDF products from NASA SPDF."""
import re

from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.tplot_tools import cdf_to_tplot, time_clip as tclip

from .config import CONFIG


_PRODUCTS = {
    'ssj': ('ssj/precipitating-electrons-ions', 'ssj_precipitating-electrons-ions', ''),
    'ssies': ('ssies/ssies-3rl/thermal-plasma-cdf', 'ssies-3_thermal-plasma', '????'),
    'ssm': ('ssm/magnetometer', 'ssm_magnetometer', ''),
}
_PROBES = {
    'ssj': {6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 18},
    'ssies': {16, 17, 18},
    'ssm': {15, 16, 17, 18},
}


def load(trange=('2014-01-01', '2014-01-02'), probe='18', instrument='ssj',
         prefix='', suffix='', get_support_data=False, varformat=None,
         varnames=None, downloadonly=False, notplot=False, no_update=False,
         time_clip=False, force_download=False):
    """Load DMSP SSJ, SSIES or SSM data from the SPDF CDF archive.

    Parameters
    ----------
    trange : sequence of str or float
        Start and end times, expressed as UTC strings or Unix seconds.
    probe : str, int or sequence
        Spacecraft number, e.g. 18, '18', 'f18', or ['16', '18'].
        SSJ supports F06-F09 and F12-F18; SSIES supports F16-F18;
        SSM supports F15-F18. Coverage varies by spacecraft and instrument.
    instrument : str
        'ssj' (precipitating electrons and ions), 'ssies' (thermal plasma),
        or 'ssm' (magnetometer).
    prefix, suffix : str
        Text prepended/appended to imported variable names. None means empty.
        Original CDF names are retained by default; use separate prefixes
        when loading spacecraft whose CDF variable names overlap.
    get_support_data : bool
        Import support variables as well as data variables.
    varformat : str, optional
        Wildcard pattern selecting CDF variables.
    varnames : sequence of str, optional
        Explicit CDF variable names to import.
    downloadonly : bool
        Return local file paths without importing data.
    notplot : bool
        Return dictionaries of data without creating tplot variables.
    no_update : bool
        Use cached files without contacting the archive.
    time_clip : bool
        Clip imported tplot variables to trange; ignored with notplot.
    force_download : bool
        Download again even when files are cached.

    Returns
    -------
    list of str or dict
        Imported tplot names, downloaded file paths, or data with notplot.

    Notes
    -----
    SSIES files cover individual orbits; SSJ and SSM files are daily.
    F19 SSJ, SSIES and SSM CDFs are not present in this archive.
    """
    instrument = instrument.lower()
    if instrument not in _PRODUCTS:
        raise ValueError('instrument must be ssj, ssies, or ssm')
    probes = [probe] if isinstance(probe, (str, int)) else list(probe)
    numbers = []
    for spacecraft in probes:
        number = int(str(spacecraft).lower().removeprefix('f'))
        if number not in _PROBES[instrument]:
            raise ValueError(f'F{number:02d} {instrument.upper()} CDF data are not '
                             'available in the SPDF DMSP archive')
        if number not in numbers:
            numbers.append(number)
    directory, product, orbit = _PRODUCTS[instrument]
    remote_names = []
    for number in numbers:
        path = (f'dmspf{number:02d}/{directory}/%Y/'
                f'dmsp-f{number:02d}_{product}_%Y%m%d{orbit}_v*.cdf')
        remote_names.extend(dailynames(file_format=path, trange=trange))
    if not remote_names:
        return {} if notplot and not downloadonly else []
    files = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'],
                     local_path=CONFIG['local_data_dir'],
                     no_download=no_update or CONFIG['no_download'],
                     force_download=force_download)
    # Keep every SSIES orbit, choosing the newest version of each file.
    newest = {}
    for filename in files or []:
        match = re.match(r'(.*)_v([0-9]+(?:\.[0-9]+)*)\.cdf$', filename)
        key = match[1] if match else filename
        version = tuple(map(int, match[2].split('.'))) if match else ()
        if key not in newest or version > newest[key][0]:
            newest[key] = (version, filename)
    files = sorted(item[1] for item in newest.values())
    if downloadonly:
        return files
    if not files:
        return {} if notplot else []
    variables = cdf_to_tplot(files, prefix=prefix or '', suffix=suffix or '',
                             get_support_data=get_support_data,
                             varformat=varformat, varnames=varnames or [],
                             notplot=notplot)
    if notplot:
        return variables
    if time_clip:
        for name in variables or []:
            tclip(name, trange[0], trange[1], suffix='')
    return variables
