
from .load import load
from .filter import filter_fields

from pytplot import options, data_quants

# Loading
def fields(trange=['2018-11-5', '2018-11-6'], 
        datatype='mag_rtn', 
        level='l2',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False,
        username=None,
        password=None
        ):
    """
    This function loads Parker Solar Probe FIELDS data
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options include:
                'mag_RTN'
                'mag_RTN_1min'
                'mag_rtn_4_per_cycle' (SPDF only)
                'mag_RTN_4_Sa_per_Cyc' 
                'mag_SC'
                'mag_SC_1min'
                'mag_sc_4_per_cycle' (SPDF only)
                'mag_SC_4_Sa_per_Cyc' 
                'mag_VSO' (limited dates)
                'rfs_burst' (limited dates)
                'rfs_hfr', 
                'rfs_lfr'
                'f2_100bps'
                'dfb_dc_spec'
                'dfb_ac_spec'
                'dfb_dc_xspec'
                'dfb_ac_xspec'
                'merged_scam_wf'
                'sqtn_rfs_V1V2'

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, this flag is False but 
            FIELDS support data is always loaded for datatypes where filtering
            on quality flags is supported.

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

        username: str
            Username to use for authentication.

            If passed, attempt to download data from the FIELDS Instrument Team server
            instead of the fully public server at SPDF.
            Provides access to unpublished, V02 files.

            Implemented for dataypes:
                'mag_RTN_1min'
                'mag_RTN_4_Sa_per_Cyc'
                'mag_SC'
                'mag_SC_1min'
                'mag_SC_4_Sa_per_Cyc'
                'sqtn_rfs_V1V2'

        password: str
            Password to use for authentication

    Returns
    ----------
        List of tplot variables created.

    """

    if suffix:
        suffix = '_' + suffix

    # SCaM and QTN data are Level 3
    if datatype.lower() in ['merged_scam_wf', 'sqtn_rfs_v1v2']:
        level = 'l3'
        print("Using LEVEL=L3")

    spec_types = None
    if datatype in ['dfb_dc_spec', 'dfb_ac_spec', 'dfb_dc_xspec', 'dfb_ac_xspec']:
        if level == 'l1':
            spec_types = ['1', '2', '3', '4']
        else:
            if datatype == 'dfb_dc_spec' or datatype == 'dfb_ac_spec':
                spec_types = ['dV12hg','dV34hg','dV12lg','dV34lg',
                    'SCMulfhg','SCMvlfhg','SCMwlfhg',
                    'SCMulflg','SCMvlflg','SCMwlflg',
                    'SCMdlfhg','SCMelfhg','SCMflfhg',
                    'SCMdlflg','SCMelflg','SCMflflg',
                    'SCMmf', 'V5hg']
            else:
                spec_types = ['SCMdlfhg_SCMelfhg','SCMdlfhg_SCMflfhg','SCMelfhg_SCMflfhg',
                    'SCMulfhg_SCMvlfhg','SCMulfhg_SCMwlfhg','SCMvlfhg_SCMwlfhg',
                    'dV12hg_dV34hg']

    loaded_vars = load(
        instrument='fields', trange=trange, datatype=datatype, spec_types=spec_types, level=level, 
        suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, 
        downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update,
        username=username, password=password
    )
    
    if loaded_vars is None or notplot or downloadonly:
        return loaded_vars

    # If variables are loaded that quality flag filtering supports --
    # Make sure the quality flag variable is also loaded and linked. 
    mag_rtnvars = [x for x in loaded_vars if 'fld_l2_mag_RTN' in x ]
    mag_scvars = [x for x in loaded_vars if 'fld_l2_mag_SC' in x ]
    rfs_vars = [x for x in loaded_vars if 'rfs_lfr' in x or 'rfs_hfr' in x]
    if (len(mag_rtnvars + mag_scvars + rfs_vars) > 0) \
        & ('psp_fld_l2_quality_flags'+suffix not in loaded_vars):
        loaded_extra = load(
            instrument='fields', trange=trange, datatype=datatype, spec_types=spec_types, level=level, 
            suffix=suffix, get_support_data=True, varformat=varformat, varnames=['psp_fld_l2_quality_flags'], 
            downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update,
            username=username, password=password
        )
        qf_root = 'psp_fld_l2_quality_flags'+suffix if 'psp_fld_l2_quality_flags'+suffix in loaded_extra else None
        loaded_vars += loaded_extra

    for var in mag_rtnvars:
        options(var, 'legend_names', ['Br (RTN)', 'Bt (RTN)', 'Bn (RTN)'])
        data_quants[var] = data_quants[var].assign_attrs({'qf_root':qf_root})

    for var in mag_scvars:
        options(var, 'legend_names', ['Bx', 'By', 'Bz'])
        data_quants[var] = data_quants[var].assign_attrs({'qf_root':qf_root})

    for var in rfs_vars:
        data_quants[var] = data_quants[var].assign_attrs({'qf_root':qf_root})

    return loaded_vars


def spc(trange=['2018-11-5', '2018-11-6'], 
        datatype='l3i', 
        level='l3',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False,
        username=None,
        password=None
    ):
    """
    This function loads Parker Solar Probe Solar Probe Cup data
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options include:
                'l3i' (level='l3')
                'l2i' (level='l2')

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

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

        username: str
            Username to use for authentication.
            
            If passed, attempt to download data from the SWEAP Instrument Team server
            instead of the fully public server at SPDF.
            Provides access to unpublished files.

        password: str
            Password to use for authentication

    Returns
    ----------
        List of tplot variables created.

    """

    if datatype == 'l3i':
        level = 'l3'
        print("Using LEVEL=L3")
    elif datatype == 'l2i':
        level = 'l2'
        print("Using LEVEL=L2")

    return load(instrument='spc', trange=trange, datatype=datatype, level=level, suffix=suffix, 
        get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, 
        notplot=notplot, time_clip=time_clip, no_update=no_update, username=username, password=password)

def spe(trange=['2018-11-5', '2018-11-6'], 
        datatype='spa_sf1_32e', 
        level='l2',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False
    ):
    """
    This function loads Parker Solar Probe SWEAP/SPAN-e data
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options include:
                spa_sf0_pad  (L3)
                spb_sf0_pad  (L3)
                spe_sf0_pad  (L3)
                spa_sf1_32e  (L2)
                spb_sf1_32e  (L2)
                spa_sf0_16ax8dx32e  (L2)
                spb_sf0_16ax8dx32e  (L2)

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

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

    """
    return load(instrument='spe', trange=trange, datatype=datatype, level=level, 
        suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, 
        downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

def spi(trange=['2018-11-5', '2018-11-6'], 
        datatype='sf00_l3_mom', 
        level='l3',
        suffix='',  
        get_support_data=False, 
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False,
        username=None,
        password=None
    ):
    """
    This function loads Parker Solar Probe SWEAP/SPAN-i data
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options Include:
                'sf00_l3_mom': Moments of the Proton distribution function (RTN)
                'sf0a_l3_mom': Moments of the Alpha distribution function (RTN)
                'sf00_l3_mom_inst': Moments of the Proton distribution function (Instrument Frame)
                'sf0a_l3_mom_inst': Moments of the Alpha distribution function (Instrument Frame)

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

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

        username: str
            Username to use for authentication.
            
            If passed, attempt to download data from the SWEAP Instrument Team server
            instead of the fully public server at SPDF.
            Provides access to unpublished files.

        password: str
            Password to use for authentication

    Returns
    ----------
        List of tplot variables created.

    """
    if datatype in ['sf00_l3_mom','sf0a_l3_mom','sf00_l3_mom_inst','sf0a_l3_mom_inst']:
        datatype = 'spi_' + datatype
        level = 'l3'
        print("Using LEVEL=L3")

    return load(instrument='spi', trange=trange, datatype=datatype, level=level, 
        suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, 
        downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update, 
        username=username, password=password
        )

def epihi(trange=['2018-11-5', '2018-11-6'], 
        datatype='let1_rates1h', 
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
    This function loads Parker Solar Probe ISoIS/EPI-Hi data
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options:

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

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

    """
    return load(instrument='epihi', trange=trange, datatype=datatype, level=level, 
        suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, 
        downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

def epilo(trange=['2018-11-5', '2018-11-6'], 
        datatype='pe', 
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
    This function loads Parker Solar Probe ISoIS/EPI-Lo data
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options:

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

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

    """
    return load(instrument='epilo', trange=trange, datatype=datatype, level=level, 
        suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, 
        downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

def epi(trange=['2018-11-5', '2018-11-6'], 
        datatype='summary', 
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
    This function loads Parker Solar Probe ISoIS/EPI (merged summary) data
    
    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options:

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

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created.

    """
    return load(instrument='epi', trange=trange, datatype=datatype, level=level, 
        suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, 
        downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

