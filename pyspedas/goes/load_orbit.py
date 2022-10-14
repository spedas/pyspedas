from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG


def load_orbit(trange=['2013-11-5', '2013-11-6'],
         probe='15',
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

    """
    remote_data_dir = 'https://spdf.gsfc.nasa.gov/pub/data/goes/'
    # yearly files
    pathformat = 'goes' + probe + '/orbit/%Y/goes' + probe + '_ephemeris_ssc_%Y0101_v??.cdf'

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat, trange=trange)

    out_files = []

    files = download(remote_file=remote_names, remote_path=remote_data_dir,
                     local_path=CONFIG['local_data_dir'], no_download=no_update)
    if files is not None:
        for file in files:
            out_files.append(file)

    out_files = sorted(out_files)

    if downloadonly:
        return out_files

    tvars = cdf_to_tplot(out_files, suffix=suffix, get_support_data=get_support_data, varformat=varformat,
                         varnames=varnames, notplot=notplot)

    if notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars
