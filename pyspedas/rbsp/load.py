from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG


def load(trange=['2018-11-5', '2018-11-6'],
         probe='a',
         instrument='emfisis',
         level='l3',
         datatype='magnetometer',
         suffix='',
         cadence='4sec',  # for EMFISIS mag data
         coord='sm',  # for EMFISIS mag data
         wavetype='waveform',  # for EMFISIS waveform data
         rel='rel04',  # for ECT data
         get_support_data=False,
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False):
    """
    Load Van Allen Probes (RBSP) data for various instruments and data levels.

    It is not intended to be called directly. Instead, use the following wrappers for specific instruments:
        - pyspedas.rbsp.emfisis
        - pyspedas.rbsp.rbspice
        - pyspedas.rbsp.efw
        - pyspedas.rbsp.mageis
        - pyspedas.rbsp.hope
        - pyspedas.rbsp.rept
        - pyspedas.rbsp.rps

    Parameters
    ----------
    trange : list of str
        Time range of interest in the format ['YYYY-MM-DD', 'YYYY-MM-DD'] or
        ['YYYY-MM-DD/hh:mm:ss', 'YYYY-MM-DD/hh:mm:ss']. Default is ['2018-11-5', '2018-11-6'].

    probe : str or list of str, default='a'
        Spacecraft probe name ('a' or 'b').

    instrument : str, default='emfisis'
        Name of the instrument.

    level : str, default='l3'
        Data level (options: 'l1', 'l2', 'l3', 'l4').

    datatype : str, default='magnetometer'
        Instrument-specific data type.

    suffix : str, default=''
        Suffix for the tplot variable names.

    cadence : str, default='4sec'
        Data cadence

    coord : str, default='sm'
        Data coordinate system.

    wavetype : str, default='waveform'
        Type of level 2 waveform data (applicable for WFR and HFR data).

    rel : str, default='rel04'
        Data release version (for ECT data).

    get_support_data : bool, default=False
        If True, loads data with attribute "VAR_TYPE" of "support_data".

    varformat : str, optional
        The file variable formats to load. Accepts wildcard character "*".

    varnames : list of str, optional
        List of variable names to load. If not specified, all variables are loaded.

    downloadonly : bool, default=False
        If True, downloads the CDF files but does not load them into tplot variables.

    notplot : bool, default=False
        If True, returns data in hash tables instead of creating tplot variables.

    no_update : bool, default=False
        If True, only load data from the local cache.

    time_clip : bool, default=False
        If True, clips the variables to the specified range in trange.

    Returns
    -------
    tvars : dict or list
        List of created tplot variables or dict of data tables if notplot is True.

    Examples
    --------
    This function is not intended to be called directly.
    """


    if not isinstance(probe, list):
        probe = [probe]

    datatype_in = datatype
    datatype = datatype.lower()
    prefix = ''
    out_files = []

    if notplot:
        tvars = {}
    else:
        tvars = []

    for prb in probe:
        if instrument == 'emfisis':
            if datatype == 'density' or datatype == 'housekeeping' or datatype == 'wna-survey':
                pathformat = 'rbsp' + prb + '/' + level + '/' + instrument + '/' + datatype + '/%Y/rbsp-' + prb + '_' + datatype + '_' + instrument + '-' + level + '_%Y%m%d_v*.cdf'
            elif datatype == 'wfr' or datatype == 'hfr':
                pathformat = 'rbsp' + prb + '/' + level + '/' + instrument + '/' + datatype + '/' + wavetype + '/%Y/rbsp-' + prb + '_' + datatype + '-' + wavetype + '_' + instrument + '-' + level + '_%Y%m%d*_v*.cdf'
            else:
                if level == 'l2' and datatype == 'magnetometer':
                    pathformat = 'rbsp' + prb + '/' + level + '/' + instrument + '/' + datatype + '/uvw/%Y/rbsp-' + prb + '_' + datatype + '_uvw_' + instrument + '-' + level + '_%Y%m%d*_v*.cdf'
                else:
                    pathformat = 'rbsp' + prb + '/' + level + '/' + instrument + '/' + datatype + '/' + cadence + '/' + coord + '/%Y/rbsp-' + prb + '_' + datatype + '_' + cadence + '-' + coord + '_' + instrument + '-' + level + '_%Y%m%d_v*.cdf'
        elif instrument == 'rbspice':
            pathformat = 'rbsp' + prb + '/' + level + '/' + instrument + '/' + datatype + '/%Y/rbsp-' + prb + '-' + instrument + '_lev-' + str(
                level[-1]) + '?' + datatype + '_%Y%m%d_v*.cdf'
            prefix = 'rbsp' + prb + '_rbspice_' + level + '_' + datatype_in + '_'
        elif instrument == 'efw':
            if level == 'l3':
                pathformat = 'rbsp' + prb + '/' + level + '/' + instrument + '/%Y/rbsp' + prb + '_' + instrument + '-' + level + '_%Y%m%d_v??.cdf'
            else:
                pathformat = 'rbsp' + prb + '/' + level + '/' + instrument + '/' + datatype + '/%Y/rbsp' + prb + '_' + instrument + '-' + level + '_' + datatype + '_%Y%m%d_v??.cdf'
        elif instrument == 'mageis':
            pathformat = 'rbsp' + prb + '/' + level + '/ect/' + instrument + '/sectors/' + rel + '/%Y/rbsp' + prb + '_' + rel + '_ect-mageis-' + level + '_%Y%m%d_v*.cdf'
        elif instrument == 'hope':
            if datatype == 'moments':
                pathformat = 'rbsp' + prb + '/' + level + '/ect/' + instrument + '/' + datatype + '/' + rel + '/%Y/rbsp' + prb + '_' + rel + '_ect-hope-mom-' + level + '_%Y%m%d_v*.cdf'
            elif datatype == 'pitchangle':
                pathformat = 'rbsp' + prb + '/' + level + '/ect/' + instrument + '/' + datatype + '/' + rel + '/%Y/rbsp' + prb + '_' + rel + '_ect-hope-pa-' + level + '_%Y%m%d_v*.cdf'
            elif datatype == 'spinaverage':
                pathformat = 'rbsp' + prb + '/' + level + '/ect/' + instrument + '/' + datatype + '/' + rel + '/%Y/rbsp' + prb + '_' + rel + '_ect-hope-sci-' + level + 'sa_%Y%m%d_v*.cdf'
        elif instrument == 'rept':
            pathformat = 'rbsp' + prb + '/' + level + '/ect/' + instrument + '/sectors/' + rel + '/%Y/rbsp' + prb + '_' + rel + '_ect-rept-sci-' + level + '_%Y%m%d_v*.cdf'
        elif instrument == 'rps':
            if datatype == 'rps-1min':
                pathformat = 'rbsp' + prb + '/' + level + '/rps/psbr-rps-1min/%Y/rbsp' + prb + '_' + level + '-1min_psbr-rps_%Y%m%d_v*.cdf'
            elif datatype == 'rps':
                pathformat = 'rbsp' + prb + '/' + level + '/rps/psbr-rps/%Y/rbsp' + prb + '_' + level + '_psbr-rps_%Y%m%d_v*.cdf'

        # find the full remote path names using the trange
        remote_names = dailynames(file_format=pathformat, trange=trange)

        files = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'],
                         local_path=CONFIG['local_data_dir'], no_download=no_update)
        if files is not None:
            for file in files:
                out_files.append(file)

        if not downloadonly:
            tvars_o = cdf_to_tplot(sorted(out_files), prefix=prefix, suffix=suffix, get_support_data=get_support_data,
                                   varformat=varformat, varnames=varnames, notplot=notplot)

            if notplot:
                tvars = dict(tvars, **tvars_o)
            else:
                tvars.extend(tvars_o)

    if downloadonly:
        return sorted(out_files)

    if notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars
