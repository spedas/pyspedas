import os
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['2013-11-5', '2013-11-6'], 
         instrument='fgm',
         datatype='h0',
         prefix='',
         suffix='', 
         get_support_data=False, 
         varformat=None,
         varnames=[],
         downloadonly=False,
         force_download=False,
         notplot=False,
         no_update=False,
         berkeley=False,
         time_clip=False,
         addmaster=True):
    """
    This function loads data from the WIND mission; this function is not meant 
    to be called directly; instead, see the wrappers:
        pyspedas.projects.wind.mfi
        pyspedas.projects.wind.swe
        pyspedas.projects.wind.sms
        pyspedas.projects.wind.threedp
        pyspedas.projects.wind.waves
        pyspedas.projects.wind.orbit

    """

    if prefix is None:
        prefix = ''
    if suffix is None:
        suffix = ''

    user_prefix = prefix

    if berkeley:
        remote_data_dir = 'http://themis.ssl.berkeley.edu/data/wind/'
    else:
        remote_data_dir = CONFIG['remote_data_dir']

    local_master_dir = CONFIG['local_data_dir']+'wind_masters/'

    masterpath = 'https://cdaweb.gsfc.nasa.gov/pub/software/cdawlib/0MASTERS/'
    if instrument == 'fgm':
        pathformat = 'mfi/mfi_'+datatype+'/%Y/wi_'+datatype+'_mfi_%Y%m%d_v??.cdf'
        masterfile = 'wi_'+datatype+'_mfi_00000000_v01.cdf'
    elif instrument == 'swe':
        pathformat = 'swe/swe_'+datatype+'/%Y/wi_'+datatype+'_swe_%Y%m%d_v??.cdf'
        masterfile = 'wi_'+datatype+'_swe_00000000_v01.cdf'
    elif instrument == 'sms':
        pathformat = 'sms/'+datatype+'/sms_'+datatype+'/%Y/wi_'+datatype+'_sms_%Y%m%d_v??.cdf'
        masterfile = 'wi_' + datatype + '_sms_00000000_v01.cdf'
    elif instrument == 'waves':
        if datatype == 'rad1' or datatype == 'rad2':
            prefix = user_prefix + 'wi_l2_wav_' + datatype + '_'
            pathformat = 'waves/'+datatype+'_l2/%Y/wi_l2_wav_'+datatype+'_%Y%m%d_v??.cdf'
            masterfile = 'wi_l2_wav_'+datatype+'_00000000_v01.cdf'
        else:
            pathformat = 'waves/wav_'+datatype+'/%Y/wi_'+datatype+'_wav_%Y%m%d_v??.cdf'
            masterfile = 'wi_' + datatype + '_wav_00000000_v01.cdf'
    elif instrument == 'orbit':
        pathformat = 'orbit/'+datatype+'/%Y/wi_'+datatype.split('_')[1]+'_'+datatype.split('_')[0]+'_%Y%m%d_v??.cdf'
        masterfile = 'wi_' + datatype.split('_')[1]+'_'+datatype.split('_')[0] + '_00000000_v01.cdf'
    elif instrument == '3dp':
        prefix = user_prefix + 'wi_' + datatype + '_'
        if datatype == '3dp_emfits_e0':
            prefix = user_prefix
            pathformat = '3dp/'+datatype+'/%Y/wi_'+datatype.split('_')[1]+'_'+datatype.split('_')[2]+'_'+datatype.split('_')[0]+'_%Y%m%d_v??.cdf'
            masterfile = 'wi_' + datatype.split('_')[1]+'_'+datatype.split('_')[2] + '_3dp_00000000_v01.cdf'
        else:
            if not berkeley:
                pathformat = '3dp/'+datatype+'/%Y/wi_'+datatype.split('_')[1]+'_'+datatype.split('_')[0]+'_%Y%m%d_v??.cdf'
                masterfile = 'wi_' + datatype.split('_')[1]+'_'+datatype.split('_')[0] + '_00000000_v01.cdf'
            else:
                pathformat = '3dp/'+datatype+'/%Y/wi_'+datatype+'_3dp_%Y%m%d_v??.cdf'
                masterfile = 'wi_' + datatype + '_3dp_00000000_v01.cdf'

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat, trange=trange)

    out_files = []

    if addmaster:
        mfile = download(remote_file=masterfile,remote_path=masterpath,local_path=local_master_dir,no_download=no_update,force_download=force_download,last_version=True)
    else:
        mfile = [None]

    datafiles = download(remote_file=remote_names, remote_path=remote_data_dir, local_path=CONFIG['local_data_dir'], no_download=no_update, force_download=force_download, last_version=True)

    out_files.extend(datafiles)

    if downloadonly:
        return out_files

    tvars = cdf_to_tplot(out_files, mastercdf=mfile[0], prefix=prefix, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, notplot=notplot)
    
    if notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars

