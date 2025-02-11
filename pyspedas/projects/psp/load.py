from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot
from .rfs import rfs_variables_to_load
from .config import CONFIG

def load(trange=['2018-11-5', '2018-11-6'],
         instrument='fields',
         datatype='mag_RTN',
         spec_types=None,  # for DFB AC spectral data
         level='l2',
         suffix='',
         prefix='',
         get_support_data=False,
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False,
         username=None,
         password=None,
         last_version=False,
         force_download=False):
    """
    This function loads Parker Solar Probe (PSP) data into tplot variables; this function is not
    meant to be called directly; instead, see the wrappers: 
        psp.fields: FIELDS data
        psp.spc: Solar Probe Cup data
        psp.spe: SWEAP/SPAN-e data
        psp.spi: SWEAP/SPAN-i data
        psp.epihi: ISoIS/EPI-Hi data
        psp.epilo: ISoIS/EPI-Lo data
        psp.epi ISoIS/EPI (merged Hi-Lo) data

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2018-11-5', '2018-11-6']

        instrument: str
            Spacecraft identifier ('fields', 'spc', 'spe', 'spi', 'epihi', 'epilo', 'epi')
            Default: 'fields'

        datatype: str
            Valid options: ['mag_RTN_4_Sa_per_Cyc',
                            'mag_RTN',
                            'mag_SC',
                            'mag_SC_1min',
                            'mag_SC_4_Sa_per_Cyc',
                            'sqtn_rfs_V1V2']
            Default: 'mag_RTN'

        spectypes: str
            Valid options: for DFB AC spectral data
            Default: None

        level: str
            Valid options: 'l2'
            Default: 'l2'

        suffix: str
            The tplot variable names will be given this suffix. By default,
            no prefix is added.
            Default: ''

        prefix: str
            The tplot variable names will be given this prefix.  By default,
            no prefix is added.
            Default: ''

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: 'False', only loads in data with a "VAR_TYPE" attribute of "data".

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None, all variables are loaded in.

        varnames: list of str
            List of variable names to load
            Default: [], all data variables are loaded

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
        
        force_download: bool
            If True, downloads the file even if a newer version exists locally. 
            Default: False.

    Returns
    ----------
        List of tplot variables created.

    Examples
    ----------
        import pyspedas
        from pytplot import tplot
        fields_psp_vars = pyspedas.projects.psp.fields(trange=['2018-11-5', '2018-11-6'])

        spc_psp_vars = pyspedas.projects.psp.spc(trange=['2018-11-5', '2018-11-6'])

        spe_psp_vars = pyspedas.projects.psp.spe(trange=['2018-11-5', '2018-11-6'])

        spi_psp_vars = pyspedas.projects.psp.spi(trange=['2018-11-5', '2018-11-6'])

        epihi_psp_vars = pyspedas.projects.psp.epihi(trange=['2018-11-5', '2018-11-6'])

        epilo_psp_vars = pyspedas.projects.psp.epilo(trange=['2018-11-5', '2018-11-6'])

        epi_psp_vars = pyspedas.projects.psp.epi(trange=['2018-11-5', '2018-11-6'])

    """
    # remote path formats generally are going to be all lowercase except for
    # on the Berkeley FIELDS server
    if (username is not None) and (datatype in ['mag_RTN_1min',
                                            'mag_RTN_4_Sa_per_Cyc',
                                            'mag_RTN',
                                            'mag_SC',
                                            'mag_SC_1min',
                                            'mag_SC_4_Sa_per_Cyc',
                                            'sqtn_rfs_V1V2'
                                            ]):
        pass
    else:
        datatype = datatype.lower()

    if suffix is None:
        suffix = ''

    if prefix is not None:
        user_prefix = prefix
    else:
        user_prefix = ''

    prefix = user_prefix + 'psp_'  #To cover the case if one *does* call this routine directly.

    file_resolution = 24*3600.
    if instrument == 'fields':
        prefix = user_prefix + '' #CDF Variables are already prefixed with psp_fld_

        # 4_per_cycle and 1min are daily, not 6h like the full resolution 'mag_(rtn|sc)'
        if datatype in ['mag_rtn', 'mag_sc']:
            pathformat = instrument + '/' + level + '/' + datatype + '/%Y/psp_fld_' + level + '_' + datatype + '_%Y%m%d%H_v??.cdf'
            file_resolution = 6*3600.
        elif datatype in ['mag_rtn_1min', 'mag_sc_1min', 'rfs_hfr', 'rfs_lfr', 'rfs_burst', 'f2_100bps', 'aeb']:
            pathformat = instrument + '/' + level + '/' + datatype + '/%Y/psp_fld_' + level + '_' + datatype + '_%Y%m%d_v??.cdf'
        elif datatype in ['mag_rtn_4_per_cycle', 'mag_rtn_4_sa_per_cyc']:
            pathformat = instrument + '/' + level + '/mag_rtn_4_per_cycle/%Y/psp_fld_' + level + '_mag_rtn_4_sa_per_cyc_%Y%m%d_v??.cdf'
        elif datatype in ['mag_sc_4_per_cycle', 'mag_sc_4_sa_per_cyc']:
            pathformat = instrument + '/' + level + '/mag_sc_4_per_cycle/%Y/psp_fld_' + level + '_mag_sc_4_sa_per_cyc_%Y%m%d_v??.cdf'
        elif datatype == 'sqtn_rfs_v1v2':
            pathformat = instrument + '/' + level + '/' + datatype + '/%Y/psp_fld_' + level + '_' + datatype + '_%Y%m%d_v?.?.cdf'        
        elif datatype == 'rfs_lfr_qtn':
            pathformat = instrument + '/' + level + '/' + datatype + '/psp_fld_' + level + '_' + datatype + '_%Y%m*_v??.cdf'
        elif datatype in ['dfb_dc_spec', 'dfb_ac_spec', 'dfb_dc_xspec', 'dfb_ac_xspec']:
            out_vars = []
            for item in spec_types:
                loaded_data = load(trange=trange, instrument=instrument, datatype=datatype + '_' + item, level=level, 
                    suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, 
                    downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update, last_version=last_version, force_download=force_download)
                if loaded_data != []:
                    out_vars.extend(loaded_data)
            return out_vars
        elif datatype[:12] == 'dfb_dc_spec_' or datatype[:12] == 'dfb_ac_spec_' or datatype[:13] == 'dfb_dc_xspec_' or datatype[:13] == 'dfb_ac_xspec_':
            if datatype[:13] == 'dfb_dc_xspec_' or datatype[:13] == 'dfb_ac_xspec_':
                dtype_tmp = datatype[:12]
                stype_tmp = datatype[13:]
            else:
                dtype_tmp = datatype[:11]
                stype_tmp = datatype[12:]
            pathformat = instrument + '/' + level + '/' + dtype_tmp + '/' + stype_tmp + '/%Y/psp_fld_' + level + '_' + datatype + '_%Y%m%d_v??.cdf'
        elif datatype == 'sqtn_rfs_v1v2':
            # unfortunately the naming format of quasi-thermal-noise cdf file is different from others
            pathformat = instrument + '/' + level + '/' + datatype + '/%Y/psp_fld_' + level + '_' + datatype + '_%Y%m%d_v?.?.cdf'
        elif datatype == 'sqtn_rfs_V1V2':
            # unpublished QTN data
            pathformat = instrument + '/' + level + '/' + datatype + '/%Y/%m/psp_fld_' + level + '_' + datatype + '_%Y%m%d_v?.?.cdf'
        elif datatype == 'merged_scam_wf':
            if username == None:
                pathformat = instrument + '/' + level + '/' + datatype + '/%Y/psp_fld_' + level + '_' + datatype + '_%Y%m%d%H_v??.cdf'
            else:
                pathformat = instrument + '/' + level + '/' + datatype + '/%Y/%m/psp_fld_' + level + '_' + datatype + '_%Y%m%d%H_v??.cdf'

        # unpublished data
        elif username != None:
            if datatype in ['mag_RTN', 'mag_SC']:
                pathformat = instrument + '/' + level + '/' + datatype + '/%Y/%m/psp_fld_' + level + '_' + datatype + '_%Y%m%d%H_v??.cdf'
                file_resolution = 6*3600.

            elif datatype in ['mag_RTN_1min', 'mag_RTN_4_Sa_per_Cyc', 'mag_SC_1min', 'mag_SC_4_Sa_per_Cyc']:
                pathformat = instrument + '/' + level + '/' + datatype + '/%Y/%m/psp_fld_' + level + '_' + datatype + '_%Y%m%d_v??.cdf'

            elif datatype ==  'sqtn_rfs_V1V2':
                pathformat = instrument + '/' + level + '/' + datatype + '/%Y/%m/psp_fld_' + level + '_' + datatype + '_%Y%m%d_v?.?.cdf'
            elif datatype in ['ephem_spp_rtn']:
                pathformat = instrument + '/' + level + '/' + datatype + '/%Y/%m/spp_fld_' + level + '_' + datatype + '_%Y%m%d_v01.cdf'
            else:
                pathformat = instrument + '/' + level + '/' + datatype + '/%Y/%m/psp_fld_' + level + '_' + datatype + '_%Y%m%d_v??.cdf'


        else:
            # Generic SPDF path.  
            pathformat = instrument + '/' + level + '/' + datatype + '/%Y/psp_fld_' + level + '_' + datatype + '_%Y%m%d%H_v??.cdf'
            file_resolution = 6*3600.

        # Files on Berkeley server are stored in monthly directories 
        if username != None:
            pathformat = pathformat.replace('/%Y/psp_fld', '/%Y/%m/psp_fld')
            if datatype == 'rfs_lfr_qtn':
                pathformat = pathformat.replace('l3/rfs_lfr_qtn/', 'l3/rfs_lfr_qtn/%Y/%m/')
            if level == 'l1':
                pathformat = pathformat.replace('psp_fld', 'spp_fld')


    elif instrument == 'spc':
        # spc changes the filename on the secure server depending on
        # whether data has been publicly released or not.
        # the publicly released data is on the NASA spdf server with the 'psp'
        # prefix. 
        #
        # However, data on the secure server exists with both the 'psp' and 'spp' 
        # prefixes. This prefix ambiguity will be handled farther down
        # and is set to 'psp' for the time being.
        prefix = user_prefix + 'psp_spc_'
        pathformat = 'sweap/spc/' + level + '/' + datatype + '/%Y/psp_swp_spc_' + datatype + '_%Y%m%d_v??.cdf'
    elif instrument == 'spe':
        prefix = user_prefix + 'psp_spe_'
        pathformat = 'sweap/spe/' + level + '/' + datatype + '/%Y/psp_swp_sp?_*_%Y%m%d_v??.cdf'
    elif instrument == 'spi':
        if username is None:
            prefix = user_prefix + 'psp_spi_'
            pathformat = 'sweap/spi/' + level + '/' + datatype + '/%Y/psp_swp_spi_*_%Y%m%d_v??.cdf'
        else:
            # unpublished data
            prefix = user_prefix + 'psp_spi_'
            pathformat = 'sweap/spi/' + level + '/' + datatype + '/%Y/%m/psp_swp_' + datatype + '*_%Y%m%d_v0?.cdf'
    elif instrument == 'epihi':
        prefix = user_prefix + 'psp_epihi_'
        pathformat = 'isois/epihi/' + level + '/' + datatype + '/%Y/psp_isois-epihi_' + level + '*_%Y%m%d_v??.cdf'
    elif instrument == 'epilo':
        prefix = user_prefix + 'psp_epilo_'
        pathformat = 'isois/epilo/' + level + '/' + datatype + '/%Y/psp_isois-epilo_' + level + '*_%Y%m%d_v??.cdf'
    elif instrument == 'epi':
        prefix = user_prefix + 'psp_isois_'
        pathformat = 'isois/merged/' + level + '/' + datatype + '/%Y/psp_isois_' + level + '-' + datatype + '_%Y%m%d_v??.cdf'

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat, trange=trange, res=file_resolution)

    out_files = []

    if username is None:
        files = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'], 
                        local_path=CONFIG['local_data_dir'], no_download=no_update,last_version=last_version, force_download=force_download)
    else:
        if instrument == 'fields':
            try:
                print("Downloading unpublished FIELDS Data....")
                files = download(
                    remote_file=remote_names, remote_path=CONFIG['fields_remote_data_dir'], 
                    local_path=CONFIG['local_data_dir'], no_download=no_update,
                    username=username, password=password, basic_auth=True,last_version=last_version, force_download=force_download,
                )
                if files == []: # I think this is a temp-fix, the logic of these blocks doesnt work now that download() doesnt raise an exception
                    raise RuntimeError("No links found.")
            except:
                files = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'], 
                                local_path=CONFIG['local_data_dir'], no_download=no_update,last_version=last_version, force_download=force_download)
        elif instrument == 'spi':
            try:
                print("Downloading unpublished SWEAP Data....")
                files = download(
                    remote_file=remote_names, remote_path=CONFIG['sweap_remote_data_dir'], 
                    local_path=CONFIG['local_data_dir'], no_download=no_update,
                    username=username, password=password, basic_auth=True,last_version=last_version, force_download=force_download
                )
                if files == []: # I think this is a temp-fix, the logic of these blocks doesnt work now that download() doesnt raise an exception
                    raise RuntimeError("No links found.")
            except:
                files = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'], 
                                local_path=CONFIG['local_data_dir'], no_download=no_update,last_version=last_version, force_download=force_download)

        elif instrument == 'spc':
            # try secure server first
            # secure server may have two file names, 
            # the publicly released data will be prefixed 'psp_swp_spc_' 
            # so check that filename first, as it will have the most
            # up to date version of the data

            try:
                print("Downloading unpublished SWEAP/SPC Data ('psp' prefix)....")
                prefix = user_prefix + 'psp_spc_'
                pathformat = 'sweap/spc/' + level + '/%Y/%m/psp_swp_spc_' + datatype + '_%Y%m%d_v0?.cdf'
                # find the full remote path names using the trange
                remote_names_spc = dailynames(file_format=pathformat, trange=trange, res=file_resolution)
                remote_dates = dailynames(file_format='%Y-%m-%d', trange=trange, res=file_resolution)
                files = download(
                    remote_file=remote_names_spc, remote_path=CONFIG['sweap_remote_data_dir'], 
                    local_path=CONFIG['local_data_dir'], no_download=no_update,
                    username=username, password=password, basic_auth=True,last_version=last_version, force_download=force_download
                )

                if len(files) != len(remote_dates): # I think this is a temp-fix, the logic of these blocks doesnt work now that download() doesnt raise an exception
                    if str(type(trange[1])) == "<class 'datetime.datetime'>" : #Handle case when user input is type <datetime.datetime>
                        t_end = trange[1].strftime('%Y-%m-%d')
                    trange_temp = [remote_dates[len(files)],trange[1]]    # set new trange to check for spp prefixes
                    raise RuntimeError("No 'psp...' prefix links found.")
            except RuntimeError as e:
                print(e)
                try :
                    
                    # then, if a date does not have 'psp_swp_spc_' prefix 
                    # then check for prefix 'spp_swp_spc_' which is the pre-released data
                    prefix = user_prefix + 'spp_spc_'
                    pathformat = 'sweap/spc/' + level + '/%Y/%m/spp_swp_spc_' + datatype + '_%Y%m%d_v0?.cdf'
                    # find the full remote path names using the trange
                    remote_names_spc = dailynames(file_format=pathformat, trange=trange_temp, res=file_resolution)
                    print("Downloading unpublished SWEAP/SPC Data ('spp' prefix)....")
                    files = download(
                        remote_file=remote_names_spc, remote_path=CONFIG['sweap_remote_data_dir'], 
                        local_path=CONFIG['local_data_dir'], no_download=no_update,
                        username=username, password=password, basic_auth=True,last_version=last_version, force_download=force_download
                        )
                    if files == []: # I think this is a temp-fix, the logic of these blocks doesnt work now that download() doesnt raise an exception
                        raise RuntimeError("No 'spp...' prefix links found.")
                # if all else fails switch to the NASA spdf server.        
                except RuntimeError as e :
                    print(e)
                    print("Trying public data....")
                    files = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'], 
                                    local_path=CONFIG['local_data_dir'], no_download=no_update,last_version=last_version, force_download=force_download)

    if files is not None:
        for file in files:
            out_files.append(file)

    out_files = sorted(out_files)

    if downloadonly:
        return out_files

    # find the list of varnames for RFS data
    # these files have > 1500 variables, but
    # we only load ~50
    if 'rfs' in datatype.lower() and varformat is None and varnames == []:
        varnames = rfs_variables_to_load(out_files)
        # we'll need the support data for the quality flags
        get_support_data = True

    tvars = cdf_to_tplot(out_files, suffix=suffix, prefix=prefix, get_support_data=get_support_data, 
                        varformat=varformat, varnames=varnames, notplot=notplot)

    if notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars
