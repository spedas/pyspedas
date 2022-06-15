import warnings
import astropy

from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['2013-11-5', '2013-11-6'], 
         instrument='fgm',
         datatype='k0', 
         suffix='', 
         get_support_data=False, 
         varformat=None,
         downloadonly=False,
         notplot=False,
         no_update=False,
         varnames=[],
         time_clip=False):
    """
    This function loads data from the ACE mission; this function is not meant 
    to be called directly; instead, see the wrappers:
        pyspedas.ace.mfi
        pyspedas.ace.swe
        pyspedas.ace.epam
        pyspedas.ace.cris
        pyspedas.ace.sis
        pyspedas.ace.uleis
        pyspedas.ace.sepica
        pyspedas.ace.swics

    """

    if instrument == 'fgm':
        pathformat = 'mag/level_2_cdaweb/mfi_'+datatype+'/%Y/ac_'+datatype+'_mfi_%Y%m%d_v??.cdf'
    elif instrument == 'swe':
        pathformat = 'swepam/level_2_cdaweb/swe_'+datatype+'/%Y/ac_'+datatype+'_swe_%Y%m%d_v??.cdf'
    elif instrument == 'epm':
        pathformat = 'epam/level_2_cdaweb/epm_'+datatype+'/%Y/ac_'+datatype+'_epm_%Y%m%d_v??.cdf'
    elif instrument == 'cris':
        pathformat = 'cris/level_2_cdaweb/cris_'+datatype+'/%Y/ac_'+datatype+'_cris_%Y%m%d_v??.cdf'
    elif instrument == 'sis':
        pathformat = 'sis/level_2_cdaweb/sis_'+datatype+'/%Y/ac_'+datatype+'_sis_%Y%m%d_v??.cdf'
    elif instrument == 'ule':
        pathformat = 'uleis/level_2_cdaweb/ule_'+datatype+'/%Y/ac_'+datatype+'_ule_%Y%m%d_v??.cdf'
    elif instrument == 'sep':
        pathformat = 'sepica/level_2_cdaweb/sep_'+datatype+'/%Y/ac_'+datatype+'_sep_%Y%m%d_v??.cdf'
    elif instrument == 'swics':
        filename_dtype = datatype.split('_')[1] + '_' + datatype.split('_')[0]
        pathformat = 'swics/level_2_cdaweb/'+datatype+'/%Y/ac_'+filename_dtype+'_%Y%m%d_v??.cdf'

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

    with warnings.catch_warnings():
        # for some reason, ACE CDFs throw ERFA warnings (likely while converting
        # times inside astropy); we're ignoring these here
        # see: https://github.com/astropy/astropy/issues/9603
        warnings.simplefilter('ignore', astropy.utils.exceptions.ErfaWarning)
        tvars = cdf_to_tplot(out_files, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, notplot=notplot)
    
    if notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars
