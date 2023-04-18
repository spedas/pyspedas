from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

LANL_SC = {'l0': '90',
           'l1': '91',
           'l4': '94',
           'l7': '97',
           'l9': '89',
           'a1': '01a',
           'a2': '02a'}


def load(trange=['2004-10-31', '2004-11-01'], 
         instrument='mpa',
         probe='a1',
         level='k0',
         suffix='', 
         get_support_data=False, 
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False):
    """
    This function loads data from the LANL mission; this function is not meant 
    to be called directly; instead, see the wrappers:

        pyspedas.lanl.mpa
        pyspedas.lanl.spa

    """

    probe = probe.lower()

    pathformat = LANL_SC[probe]+'_'+instrument+'/%Y/'+probe+'_'+level+'_'+instrument+'_%Y%m%d_v??.cdf'

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

    tvars = cdf_to_tplot(out_files, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, notplot=notplot)
    
    if notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars

    