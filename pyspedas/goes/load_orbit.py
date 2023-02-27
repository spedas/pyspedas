from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG


def load_orbit(trange=['2013-11-5', '2013-11-6'],
               probe='15',
               prefix='',
               suffix='',
               get_support_data=False,
               varformat=None,
               varnames=[],
               downloadonly=False,
               notplot=False,
               no_update=False,
               time_clip=True):
    """
    This function loads GOES orbit data from SPDF:

    https://spdf.gsfc.nasa.gov/pub/data/goes/goes#/orbit/YYYY/

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str/int or list of strs/ints
            GOES spacecraft #, e.g., probe=15

        prefix: str
            The tplot variable names will be given this prefix.
            By default, no prefix is added.
            If 'probename' then the name will be used, for example g16.

        suffix: str
            The tplot variable names will be given this suffix.
            By default, no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables

        notplot: bool
            If set, load the data into dictionaries containing the numpy objects instead
            of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created. Or list of filenames downloaded.

    """
    remote_data_dir = 'https://spdf.gsfc.nasa.gov/pub/data/goes/'
    out_files = []  # list of local files downloaded
    tvars = []  # list of tplot variables created

    if not isinstance(probe, list):
        probe = [probe]

    for prb in probe:

        # yearly files
        pathformat = 'goes' + str(prb) + '/orbit/%Y/goes' + str(prb) + '_ephemeris_ssc_%Y0101_v??.cdf'

        # find the full remote path names using the trange
        remote_names = dailynames(file_format=pathformat, trange=trange)

        files = download(remote_file=remote_names, remote_path=remote_data_dir,
                         local_path=CONFIG['local_data_dir'], no_download=no_update)

        out_files_local = []

        if files is not None:
            for file in files:
                out_files_local.append(file)

        out_files.extend(out_files_local)

        tvars_local = []
        if not downloadonly:
            if prefix == 'probename':
                prefix_local = 'g' + str(prb) + '_'
            else:
                prefix_local = prefix

            tvars_local = cdf_to_tplot(out_files_local, prefix=prefix_local, suffix=suffix, get_support_data=get_support_data,
                                       varformat=varformat, varnames=varnames, notplot=notplot)
            tvars.extend(tvars_local)

        if time_clip:
            for new_var in tvars_local:
                tclip(new_var, trange[0], trange[1], suffix='')

    if downloadonly:
        return out_files

    return tvars
