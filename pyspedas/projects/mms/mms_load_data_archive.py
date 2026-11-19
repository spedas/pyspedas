import logging
from fnmatch import fnmatch
from urllib.parse import unquote, urlsplit
from pyspedas.tplot_tools import time_double
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download, is_fsspec_uri, _managed_filesystem, LinkParser
from pyspedas.utilities.last_version_per_identity import last_version_per_identity
from .mms_file_filter import mms_file_filter
from .mms_get_local_files import mms_get_local_files
from pyspedas.tplot_tools import cdf_to_tplot
from pyspedas.tplot_tools import time_clip as tclip
from .config import CONFIG

# Instruments for which this module implements archive path templates. Requests
# outside this set use the SDC directly; missing archive files never trigger SDC.
ARCHIVE_INSTRUMENTS = frozenset({
    'fgm', 'aspoc', 'edi', 'fpi', 'epd-eis', 'feeps', 'hpca', 'mec', 'scm', 'dsp', 'edp',
})


# Include the product and timestamp in the identity, preserving every observation
# while choosing one CDF version for it. Both daily and burst filenames use this form.
MMS_VERSIONED_REGEX = r'(?P<identity>mms[1-4]_.+)_v(?P<version>\d+\.\d+\.\d+)\.cdf'


def archive_supported(instrument, level):
    """Identify implemented archive instruments and known SDC-only levels.

    SITL/trigger products and restricted FEEPS L1b products use the SDC.
    This describes routing, not the time coverage of any particular archive.
    """
    return (instrument in ARCHIVE_INSTRUMENTS and level not in ('sitl', 'trig')
            and not (instrument == 'feeps' and level == 'l1b'))


def _archive_available_files(patterns, archive_root):
    """List matching remote CDFs without transferring their contents."""
    found = set()
    directories = {}
    for pattern in patterns:
        url = archive_root + pattern
        if is_fsspec_uri(url):
            protocol = url.split('://', 1)[0]
            with _managed_filesystem(protocol, anon=True) as fs:
                for path in fs.glob(url):
                    found.add(path if '://' in path else protocol + '://' + path)
        else:
            directory, filename = url.rsplit('/', 1)
            if directory not in directories:
                html = download(remote_file=directory + '/', return_text=True, no_wildcards=True)
                if html is None:
                    directories[directory] = []
                else:
                    parser = LinkParser()
                    parser.feed(html)
                    directories[directory] = [unquote(urlsplit(link).path).rsplit('/', 1)[-1]
                                               for link in parser.links]
            for name in directories[directory]:
                if fnmatch(name, filename):
                    found.add(directory + '/' + name)
    return sorted(found)


def mms_load_data_archive(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2',
    instrument='fgm', datatype='', varformat=None, exclude_format=None, suffix='', get_support_data=False, time_clip=False,
    no_update=False, center_measurement=False, available=False, notplot=False, latest_version=False,
    major_version=False, min_version=None, cdf_version=None, varnames=[], prefix=''):
    """
    Load MMS CDFs from the configured SPDF-style HTTP or S3 archive

    This function is not meant to be called directly. Please see the individual load routines for documentation and use.
    """

    if instrument not in ARCHIVE_INSTRUMENTS:
        raise ValueError(f'MMS archive access does not support instrument {instrument!r}')
    archive_root = CONFIG['remote_data_dir']
    if not isinstance(archive_root, str) or not archive_root.strip():
        raise ValueError('MMS remote_data_dir must be a nonempty archive URL')
    archive_root = archive_root.rstrip('/') + '/'
    no_download = no_update or CONFIG['no_download']
    download_only = CONFIG['download_only']
    tvars_created = {} if notplot else []
    selected_files = []
    # Keep all candidates until explicit version filters have run. In particular,
    # selecting first could discard an older version requested by cdf_version.
    select_before_download = not (latest_version or major_version
                                  or min_version is not None or cdf_version is not None)
    # Compute padding once; never extend trange repeatedly across product groups.

    if not isinstance(probe, list): probe = [probe]
    if not isinstance(data_rate, list): data_rate = [data_rate]
    if not isinstance(level, list): level = [level]
    if not isinstance(datatype, list): datatype = [datatype]

    for prb in probe:
        for lvl in level:
            for drate in data_rate:
                if drate == 'brst':
                    time_format = '%Y%m%d%H%M??'
                    file_res = 60.
                else:
                    time_format = '%Y%m%d'
                    file_res = 24*3600.
                for dtype in datatype:
                    remote_path = 'mms' + prb + '/' + instrument + '/' + drate + '/' + lvl + '/'

                    if instrument == 'fgm':
                        pathformat = remote_path + '%Y/%m/mms' + prb + '_fgm_' + drate + '_' + lvl + '_' + time_format + '_v*.cdf'
                    elif instrument == 'aspoc':
                        pathformat = remote_path + '%Y/%m/mms' + prb + '_aspoc_' + drate + '_' + lvl + '_' + time_format + '_v*.cdf'
                    elif instrument == 'edi':
                        pathformat = remote_path + dtype + '/%Y/%m/mms' + prb + '_edi_' + drate + '_' + lvl + '_' + dtype + '_' + time_format + '_v*.cdf'
                    elif instrument == 'fpi':
                        if drate != 'brst':
                            time_format = '%Y%m%d??0000'
                        pathformat = remote_path + dtype + '/%Y/%m/mms' + prb + '_fpi_' + drate + '_' + lvl + '_' + dtype + '_' + time_format + '_v*.cdf'
                    elif instrument == 'epd-eis':
                        pathformat = remote_path + dtype + '/%Y/%m/mms' + prb + '_epd-eis_' + drate + '_' + lvl + '_' + dtype + '_' + time_format + '_v*.cdf'
                    elif instrument == 'feeps':
                        if drate != 'brst':
                            time_format = '%Y%m%d000000'
                        pathformat = remote_path + dtype + '/%Y/%m/mms' + prb + '_feeps_' + drate + '_' + lvl + '_' + dtype + '_' + time_format + '_v*.cdf'
                    elif instrument == 'hpca':
                        time_format = '%Y%m%d??????'
                        pathformat = remote_path + dtype + '/%Y/%m/mms' + prb + '_hpca_' + drate + '_' + lvl + '_' + dtype + '_' + time_format + '_v*.cdf'
                    elif instrument == 'mec':
                        pathformat = remote_path + dtype + '/%Y/%m/mms' + prb + '_mec_' + drate + '_' + lvl + '_' + dtype + '_' + time_format + '_v*.cdf'
                    elif instrument == 'scm':
                        pathformat = remote_path + dtype + '/%Y/%m/mms' + prb + '_scm_' + drate + '_' + lvl + '_' + dtype + '_' + time_format + '_v*.cdf'
                    elif instrument == 'dsp':
                        pathformat = remote_path + dtype + '/%Y/%m/mms' + prb + '_dsp_' + drate + '_' + lvl + '_' + dtype + '_' + time_format + '_v*.cdf'
                    elif instrument == 'edp':
                        pathformat = remote_path + dtype + '/%Y/%m/mms' + prb + '_edp_' + drate + '_' + lvl + '_' + dtype + '_' + time_format + '_v*.cdf'

                    search_trange = [time_double(trange[0]) - 300., time_double(trange[1])] if drate == 'brst' else trange
                    # find the full remote path names using the trange
                    remote_names = dailynames(file_format=pathformat, trange=search_trange, res=file_res)

                    out_files = []

                    if available and not no_download:
                        files = _archive_available_files(remote_names, archive_root)
                    else:
                        files = download(remote_file=remote_names, remote_path=archive_root,
                                         local_path=CONFIG['local_data_dir'], no_download=no_download,
                                         last_version=select_before_download,
                                         versioned_regex=MMS_VERSIONED_REGEX)
                    if files is not None:
                        for file in files:
                            out_files.append(file)

                    if not out_files and not available:
                        logging.info('Searching for local files...')
                        out_files = mms_get_local_files(prb, instrument, drate, lvl, dtype, search_trange)

                        if not out_files and CONFIG['mirror_data_dir'] != None:
                            # check for network mirror; note: network mirrors are assumed to be read-only
                            # and we always copy the files from the mirror to the local data directory
                            # before trying to load into tplot variables
                            logging.info('No local files found; checking network mirror...')
                            out_files = mms_get_local_files(prb, instrument, drate, lvl, dtype, search_trange, mirror=True)

                    out_files = sorted(out_files)

                    filtered_out_files = mms_file_filter(out_files, latest_version=latest_version, major_version=major_version, min_version=min_version, version=cdf_version)

                    # Also covers available-only listings and local/mirror fallback.
                    filtered_out_files = last_version_per_identity(filtered_out_files, MMS_VERSIONED_REGEX)
                    selected_files.extend(filtered_out_files)
                    if available or download_only:
                        continue

                    tvars = cdf_to_tplot(filtered_out_files, varformat=varformat, exclude_format=exclude_format, varnames=varnames, get_support_data=get_support_data, prefix=prefix, suffix=suffix, center_measurement=center_measurement, notplot=notplot)
                    if tvars is not None:
                        if notplot:
                            tvars_created.update(tvars)
                        else:
                            tvars_created.extend(tvars)

    if available:
        return sorted({file.rsplit('/', 1)[-1] for file in selected_files})
    if download_only:
        return sorted(set(selected_files))
    if time_clip and not notplot:
        for new_var in tvars_created:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars_created if notplot else sorted(set(tvars_created))
