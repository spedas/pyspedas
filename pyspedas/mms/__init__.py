"""
This module contains routines for loading MMS data


"""

from .mms_load_data import mms_load_data
from .fgm.mms_fgm_remove_flags import mms_fgm_remove_flags
from .fgm.mms_fgm_set_metadata import mms_fgm_set_metadata
from .fpi.mms_fpi_set_metadata import mms_fpi_set_metadata

def mms_load_fgm(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='', prefix='', suffix='', keep_flagged=False, get_support_data=True):
    """
    This function loads FGM data into tplot variables
    
    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str
            list of probes, valid values for MMS probes are ['1','2','3','4']. 

        data_rate : str or list of str
            instrument data rates for FGM include 'brst' 'fast' 'slow' 'srvy'. The
            default is 'srvy'.

        level : str
            indicates level of data processing. the default if no level is specified is 'l2'

        datatype : str or list of str
            no datatype for FGM instrument (all science data are loaded)

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".

        prefix: str
            The tplot variable names will be given this prefix.  By default, 
            no prefix is added.

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

            
    Returns:
        List of tplot variables created.

    """

    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='fgm', datatype=datatype, prefix=prefix, suffix=suffix, get_support_data=get_support_data)
    
    if tvars == None:
        return

    # remove flagged data
    if not keep_flagged:
        mms_fgm_remove_flags(probe, data_rate, level, suffix=suffix)

    mms_fgm_set_metadata(probe, data_rate, level, suffix=suffix)
    return tvars

def mms_load_hpca(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='moments', get_support_data=False):

    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='hpca', datatype=datatype, get_support_data=get_support_data)
    return tvars

def mms_load_fpi(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='fast', level='l2', datatype=['des-moms', 'dis-moms'], prefix='', suffix='', get_support_data=False):

    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='fpi', datatype=datatype, prefix=prefix, suffix=suffix, get_support_data=get_support_data)
    
    if tvars == None:
        return

    mms_fpi_set_metadata(probe, data_rate, datatype, level, suffix=suffix)
    return tvars

def mms_load_scm(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='', prefix='', suffix='', get_support_data=False):

    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='scm', datatype=datatype, prefix=prefix, suffix=suffix, get_support_data=get_support_data)
    return tvars

def mms_load_mec(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='ephts04d', prefix='', suffix='', get_support_data=False):

    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='mec', datatype=datatype, get_support_data=get_support_data)
    return tvars

def mms_load_feeps(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='electron', get_support_data=False):

    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='feeps', datatype=datatype, get_support_data=get_support_data)
    return tvars

def mms_load_eis(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='phxtof', get_support_data=False):
    from .eis.mms_eis_omni import mms_eis_omni
    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='epd-eis', datatype=datatype, get_support_data=get_support_data)

    if tvars == []:
        return

    if not isinstance(probe, list): probe = [probe]
    if not isinstance(data_rate, list): data_rate = [data_rate]
    if not isinstance(datatype, list): datatype = [datatype]

    for probe_id in probe:
        for datatype_id in datatype:
            for data_rate_id in data_rate:
                omni_spectra = mms_eis_omni(probe_id, data_rate=data_rate_id, datatype=datatype_id)
    return tvars

def mms_load_edi(trange=['2016-10-16', '2016-10-17'], probe='1', data_rate='srvy', level='l2', datatype='efield', get_support_data=False):

    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='edi', datatype=datatype, get_support_data=get_support_data)
    return tvars

def mms_load_edp(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='fast', level='l2', datatype='dce', get_support_data=False):

    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='edp', datatype=datatype, get_support_data=get_support_data)
    return tvars

def mms_load_dsp(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='', prefix='', suffix='', get_support_data=False):

    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='dsp', datatype=datatype, prefix=prefix, suffix=suffix, get_support_data=get_support_data)
    return tvars

def mms_load_aspoc(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='', get_support_data=False):

    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='aspoc', datatype=datatype, get_support_data=get_support_data)
    return tvars

