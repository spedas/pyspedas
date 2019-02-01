"""
This module contains routines for loading MMS data


"""

from .mms_load_data import mms_load_data

def mms_load_fgm(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='', prefix='', suffix=''):
    """
    This function loads FGM data into tplot variables
    
    Parameters
    ----------
        trange : list of str
            The file names and full paths of CDF files.   
        probe : str
            The file variable formats to load into tplot.  Wildcard character 
            "*" is accepted.  By default, all variables are loaded in.  
        data_rate
        level
        datatype

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

            
    Returns
    -------
        List of tplot variables created.

    """

    files = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='fgm', datatype=datatype, prefix=prefix, suffix=suffix)
    return files

def mms_load_hpca(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='moments'):

    files = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='hpca', datatype=datatype)
    return files

def mms_load_fpi(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='fast', level='l2', datatype=['des-moms', 'dis-moms'], prefix='', suffix=''):

    files = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='fpi', datatype=datatype, prefix=prefix, suffix=suffix)
    return files

def mms_load_scm(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='', prefix='', suffix=''):

    files = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='scm', datatype=datatype, prefix=prefix, suffix=suffix)
    return files

def mms_load_mec(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='ephts04d', prefix='', suffix=''):

    files = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='mec', datatype=datatype)
    return files

def mms_load_feeps(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='electron'):

    files = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='feeps', datatype=datatype)
    return files

def mms_load_eis(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='phxtof'):
    from .eis.mms_eis_omni import mms_eis_omni
    files = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='epd-eis', datatype=datatype)

    if not isinstance(probe, list): probe = [probe]
    if not isinstance(data_rate, list): data_rate = [data_rate]
    if not isinstance(datatype, list): datatype = [datatype]

    for probe_id in probe:
        for datatype_id in datatype:
            for data_rate_id in data_rate:
                omni_spectra = mms_eis_omni(probe_id, data_rate=data_rate_id, datatype=datatype_id)
    return files

def mms_load_edi(trange=['2016-10-16', '2016-10-17'], probe='1', data_rate='srvy', level='l2', datatype='efield'):

    files = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='edi', datatype=datatype)
    return files

def mms_load_edp(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='fast', level='l2', datatype='dce'):

    files = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='edp', datatype=datatype)
    return files

def mms_load_dsp(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype='', prefix='', suffix=''):

    files = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='dsp', datatype=datatype, prefix=prefix, suffix=suffix)
    return files

def mms_load_aspoc(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='srvy', level='l2', datatype=''):

    files = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='aspoc', datatype=datatype)
    return files

