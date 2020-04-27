
import numpy as np
from pyspedas.erg.load import load
from pytplot import options, clip, ylim, get_data

def mgf(trange=['2017-03-27', '2017-03-28'],
        datatype='8sec', 
        level='l2', 
        suffix='',  
        get_support_data=False, 
        varformat=None,
        downloadonly=False,
        notplot=False,
        no_update=False,
        uname=None,
        passwd=None,
        time_clip=False):
    """
    This function loads data from the MGF experiment from the Arase mission
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options:

        level: str
            Data level; Valid options:

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns:
        List of tplot variables created.

    """

    if datatype == '8s' or datatype == '8':
        datatype = '8sec'
    elif datatype == '64':
        datatype = '64hz'
    elif datatype == '128':
        datatype = '128hz'
    elif datatype == '256':
        datatype = '256hz'

    loaded_data = load(instrument='mgf', trange=trange, level=level, datatype=datatype, suffix=suffix, get_support_data=get_support_data, varformat=varformat, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update, uname=uname, passwd=passwd)
    
    if loaded_data == None or loaded_data == [] or notplot or downloadonly:
        return loaded_data

    clip('erg_mgf_'+level+'_mag_'+datatype+'_dsi'+suffix, -1e+6, 1e6)
    clip('erg_mgf_'+level+'_mag_'+datatype+'_gse'+suffix, -1e+6, 1e6)
    clip('erg_mgf_'+level+'_mag_'+datatype+'_gsm'+suffix, -1e+6, 1e6)
    clip('erg_mgf_'+level+'_mag_'+datatype+'_sm'+suffix, -1e+6, 1e6)

    # set yrange
    times, bdata = get_data('erg_mgf_'+level+'_mag_'+datatype+'_dsi'+suffix)
    ylim('erg_mgf_'+level+'_mag_'+datatype+'_dsi'+suffix, np.nanmin(bdata), np.nanmax(bdata))
    times, bdata = get_data('erg_mgf_'+level+'_mag_'+datatype+'_gse'+suffix)
    ylim('erg_mgf_'+level+'_mag_'+datatype+'_gse'+suffix, np.nanmin(bdata), np.nanmax(bdata))
    times, bdata = get_data('erg_mgf_'+level+'_mag_'+datatype+'_gsm'+suffix)
    ylim('erg_mgf_'+level+'_mag_'+datatype+'_gsm'+suffix, np.nanmin(bdata), np.nanmax(bdata))
    times, bdata = get_data('erg_mgf_'+level+'_mag_'+datatype+'_sm'+suffix)
    ylim('erg_mgf_'+level+'_mag_'+datatype+'_sm'+suffix, np.nanmin(bdata), np.nanmax(bdata))

    # set labels
    options('erg_mgf_'+level+'_mag_'+datatype+'_dsi'+suffix, 'legend_names', ['Bx', 'By', 'Bz'])
    options('erg_mgf_'+level+'_mag_'+datatype+'_gse'+suffix, 'legend_names', ['Bx', 'By', 'Bz'])
    options('erg_mgf_'+level+'_mag_'+datatype+'_gsm'+suffix, 'legend_names', ['Bx', 'By', 'Bz'])
    options('erg_mgf_'+level+'_mag_'+datatype+'_sm'+suffix, 'legend_names', ['Bx', 'By', 'Bz'])

    # set color of the labels
    options('erg_mgf_'+level+'_mag_'+datatype+'_dsi'+suffix, 'Color', ['b', 'g', 'r'])
    options('erg_mgf_'+level+'_mag_'+datatype+'_gse'+suffix, 'Color', ['b', 'g', 'r'])
    options('erg_mgf_'+level+'_mag_'+datatype+'_gsm'+suffix, 'Color', ['b', 'g', 'r'])
    options('erg_mgf_'+level+'_mag_'+datatype+'_sm'+suffix, 'Color', ['b', 'g', 'r'])

    return loaded_data
