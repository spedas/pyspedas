import logging 

from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG


def load(trange=['2020-11-5', '2020-11-6'],
         probe='a',
         instrument='fgm',
         datatype='flux', 
         level='l2', 
         suffix='', 
         get_support_data=False, 
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False,
         force_download=False):
    """
    This function loads data from the ELFIN mission; this function is not meant 
    to be called directly; instead, see the wrappers:

        pyspedas.projects.elfin.fgm
        pyspedas.projects.elfin.epd
        pyspedas.projects.elfin.mrma
        pyspedas.projects.elfin.mrmi
        pyspedas.projects.elfin.state
        pyspedas.projects.elfin.eng

        This is a test
    """

    if instrument == 'fgm':
        datatype_str = 'fgs'
        if datatype.lower() == 'fast':
            datatype_str = 'fgf'
        pathformat = f'el{probe}/{level}/{instrument}/{datatype}/%Y/el{probe}_{level}_{datatype_str}_%Y%m%d_v??.cdf'
    elif instrument == 'epd':
        if datatype == 'pef':
            pathformat = f'el{probe}/{level}/{instrument}/fast/electron/%Y/el{probe}_{level}_epdef_%Y%m%d_v??.cdf'
        elif datatype == 'pif':
            pathformat = f'el{probe}/{level}/{instrument}/fast/ion/%Y/el{probe}_{level}_epdif_%Y%m%d_v??.cdf'
        elif datatype == 'pes':
            pathformat = f'el{probe}/{level}/{instrument}/survey/electron/%Y/el{probe}_{level}_epdes_%Y%m%d_v??.cdf'
        elif datatype == 'pis':
            pathformat = f'el{probe}/{level}/{instrument}/survey/ion/%Y/el{probe}_{level}_epdis_%Y%m%d_v??.cdf'
    elif instrument == 'mrma':
        pathformat = f'el{probe}/{level}/{instrument}/%Y/el{probe}_{level}_{instrument}_%Y%m%d_v??.cdf'
    elif instrument == 'mrmi':
        pathformat = f'el{probe}/{level}/{instrument}/%Y/el{probe}_{level}_{instrument}_%Y%m%d_v??.cdf'
    elif instrument == 'state':
        pathformat = f'el{probe}/{level}/{instrument}/{datatype}/%Y/el{probe}_{level}_{instrument}_{datatype}_%Y%m%d_v??.cdf'
    elif instrument == 'eng':
        pathformat = f'el{probe}/{level}/{instrument}/%Y/el{probe}_{level}_{instrument}_%Y%m%d_v??.cdf'

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat, trange=trange)

    out_files = []

    files = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'], local_path=CONFIG['local_data_dir'], no_download=no_update, last_version=True, force_download=force_download)

    if not files:
        logging.error(f"ELFIN LOAD: NO CDF FILE FOUND! check file {remote_names}")
    else:
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
