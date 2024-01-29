from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG


def load(trange=['1983-02-16', '1983-02-17'], 
         instrument='mag',
         datatype='',
         suffix='', 
         get_support_data=False, 
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False):
    """
    This function loads data from the DE2 mission; this function is not meant 
    to be called directly; instead, see the wrappers:

        pyspedas.de2.mag
        pyspedas.de2.nacs
        pyspedas.de2.rpa
        pyspedas.de2.fpi
        pyspedas.de2.idm
        pyspedas.de2.wats
        pyspedas.de2.vefi
        pyspedas.de2.lang

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2020-11-5/10:00', '2020-11-5/12:00']

        instrument : instruments include
            'mag'
            'nacs'
            'rpa'
            'idm'
            'wats'
            'vefi'
            'lang'
            Default: 'mag'

         datatype : see if statements below in main code
            Default: ''

        suffix: str
            The tplot variable names will be given this suffix.
            Default: no suffix is added

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: only loads in data with a "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: all variables are loaded in

        varnames: list of str
            List of variable names to load
            Default: all data variables are loaded

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables
            Default: False

        notplot: bool
            Return the data in hash tables instead of creating tplot variables
            Default: False

        no_update: bool
            If set, only load data from your local cache
            Default: False

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword
            Default: False

     Returns
    ----------
        List of tplot variables created.

    Example
    ----------
        import pyspedas
        from pytplot import tplot
        pyspedas.de2.load(instrument='mag', trange=['2020-11-5/10:00', '2020-11-5/12:00'])
        tplot()

        import pyspedas
        from pytplot import tplot
        mag_vars = pyspedas.de2.mag(trange=['1983-02-16', '1983-02-17'])
        tplot(['bx', 'by', 'bz'])

    """

    if instrument == 'mag':
        pathformat = 'magnetic_electric_fields_vefi_magb/'+datatype+'_vefimagb_cdaweb/%Y/de2_'+datatype+'_vefimagb_%Y%m%d_v??.cdf'
    elif instrument == 'nacs':
        pathformat = 'neutral_gas_nacs/'+datatype+'_'+instrument+'_cdaweb/%Y/de2_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'rpa':
        pathformat = 'plasma_rpa/'+datatype+'_cdaweb/%Y/de2_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'fpi':
        pathformat = 'neutral_gas_fpi/de2_neutral8s_fpi/%Y/de2_neutral'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'idm':
        pathformat = 'plasma_idm/vion250ms_cdaweb/%Y/de2_vion'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'wats':
        pathformat = 'neutral_gas_wats/wind2s_wats_cdaweb/%Y/de2_wind'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'vefi':
        pathformat = 'electric_fields_vefi/'+datatype+'_vefi_cdaweb/%Y/de2_'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'
    elif instrument == 'lang':
        pathformat = 'plasma_lang/plasma500ms_lang_cdaweb/%Y/de2_plasma'+datatype+'_'+instrument+'_%Y%m%d_v??.cdf'

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

    