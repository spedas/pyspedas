from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas.analysis.time_clip import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['1997-01-03', '1997-01-04'], 
         instrument='mfe',
         datatype='k0',
         suffix='', 
         get_support_data=False, 
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False):
    """
    This function loads data from the Polar mission; this function is not meant 
    to be called directly; instead, see the wrappera:
        pyspedas.polar.mfe
        pyspedas.polar.efi
        pyspedas.polar.pwi
        pyspedas.polar.hydra
        pyspedas.polar.tide
        pyspedas.polar.timas
        pyspedas.polar.cammice
        pyspedas.polar.ceppad
        pyspedas.polar.uvi
        pyspedas.polar.vis
        pyspedas.polar.pixie
        pyspedas.polar.orbit

    """

    if instrument == 'mfe':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'efi':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'pwi':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'hydra':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_hyd_%Y%m%d_v??.cdf'
    elif instrument == 'tide':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_tid_%Y%m%d_v??.cdf'
    elif instrument == 'timas':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_tim_%Y%m%d_v??.cdf'
    elif instrument == 'cammice':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_cam_%Y%m%d_v??.cdf'
    elif instrument == 'ceppad':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_cep_%Y%m%d_v??.cdf'
    elif instrument == 'uvi':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'vis':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'pixie':
        pathformat = instrument+'/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_pix_%Y%m%d_v??.cdf'
    elif instrument == 'spha':
        pathformat = 'orbit/'+instrument+'_'+datatype+'/%Y/po_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'

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
