from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG


def load(trange=['2014-10-18', '2014-10-19'], 
         instrument='mag',
         datatype='', 
         level='l2', 
         suffix='', 
         get_support_data=False, 
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False):
    """
    This function loads data from the MAVEN mission; this function is not meant 
    to be called directly; instead, see the wrappers:

        pyspedas.maven.mag
        pyspedas.maven.swea
        pyspedas.maven.swia
        pyspedas.maven.static
        pyspedas.maven.sep
        pyspedas.maven.kp

    """

    if instrument == 'mag':
        pathformat = f"{instrument}/{level}/{datatype}/cdfs/%Y/%m/mvn_{instrument}_{level}-{datatype}_%Y%m%d_v??_r??.cdf"
    elif instrument == 'swea':
        pathformat = f"{instrument}/{level}/{datatype}/%Y/%m/mvn_swe_{level}_{datatype}_%Y%m%d_v??_r??.cdf"
    elif instrument == 'swia':
        pathformat = f"{instrument}/{level}/{datatype}/%Y/%m/mvn_swi_{level}_{datatype}_%Y%m%d_v??_r??.cdf"
    elif instrument == 'static':
        pathformat = f"{instrument}/{level}/{datatype}/%Y/%m/mvn_sta_{level}_{datatype}_%Y%m%d_v??_r??.cdf"
    elif instrument == 'sep':
        pathformat = f"{instrument}/{level}/{datatype}/%Y/%m/mvn_{instrument}_{level}_{datatype}_%Y%m%d_v??_r??.cdf"
    elif instrument == 'kp':
        # https://spdf.gsfc.nasa.gov/pub/data/maven/insitu/kp-4sec/cdfs/2016/
        pathformat = f"insitu/{datatype}/cdfs/%Y/%m/mvn_insitu_{datatype}_%Y%m%d_v??_r??.cdf"

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat, trange=trange)

    out_files = []

    files = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'], local_path=CONFIG['local_data_dir'], no_download=no_update)
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
