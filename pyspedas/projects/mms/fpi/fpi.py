from pyspedas.projects.mms.mms_load_data import mms_load_data
from pyspedas.projects.mms.fpi.mms_fpi_set_metadata import mms_fpi_set_metadata
from pyspedas.projects.mms.fpi.mms_load_fpi_calc_pad import mms_load_fpi_calc_pad
from pyspedas.projects.mms.fpi.mms_fpi_make_compressionlossbars import mms_fpi_make_compressionlossbars
from pyspedas.projects.mms.fpi.mms_fpi_make_errorflagbars import mms_fpi_make_errorflagbars
from pyspedas.projects.mms.mms_config import CONFIG
from pytplot import tplot_rename, del_data


def mms_load_fpi(trange=['2015-10-16', '2015-10-17'], probe='1', data_rate='fast',
    level='l2', datatype='*', varformat=None, varnames=[], suffix='',
    get_support_data=False, time_clip=False, no_update=False, center_measurement=False,
    available=False, notplot=False, latest_version=False, major_version=False, 
    min_version=None, cdf_version=None, spdf=False, always_prompt=False):
    """
    Load data from the MMS Fast Plasma Investigation (FPI)
    
    Parameters
    ----------
        trange : list of str
            time range of interest [start time, end time] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2015-10-16', '2015-10-17']

        probe : str or list of str
            list of probes, valid values for MMS probes are ['1','2','3','4'].
            Default: '1'

        data_rate : str or list of str
            instrument data rates for FPI include 'brst', 'fast'.
            Default: 'fast'

        level : str
            indicates level of data processing. Valid options: 'l2', 'ql'
            Default: 'l2'

        datatype : str or list of str
            Valid datatypes for FPI are:
             'des-moms', 'dis-moms', 'des-momsaux', 'dis-momsaux', 'des-dist', 'dis-dist', 'des', 'dis'
             Defaults:
             ['des-moms', 'dis-moms', 'des-dist' , 'dis-dist', 'des-momsaux', 'dis-momsaux'] (for level != 'ql' or unspecified)
             ['des', 'dis'] (for level == 'ql')

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: False

        time_clip: bool
            Data will be clipped to the exact trange specified by the trange keyword.
            Default: False
            
        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None (All variables are loaded)

        varnames: list of str
            List of variable names to load. If list is empty or not specified,
            all data variables are loaded
            Default: [] (all variables are loaded)

        suffix: str
            The tplot variable names will be given this suffix.
            Default: None

        center_measurement: bool
            If True, the CDF epoch variables are time-shifted to the middle
            of the accumulation interval by their DELTA_PLUS_VAR and
            DELTA_MINUS_VAR variable attributes
            Default: False

        notplot: bool
            If True, then data are returned in a hash table instead of 
            being stored in tplot variables (useful for debugging, and
            access to multidimensional data products)
            Default: False

        available: bool
            If True, simply return the available data files (without downloading)
            for the requested parameters
            Default: False

        no_update: bool
            Set this flag to preserve the original data. if not set and newer 
            data is found the existing data will be overwritten
            Default: False

        cdf_version: str
            Specify a specific CDF version # to load (e.g., cdf_version='4.3.0')
            Default: None

        min_version: str
            Specify a minimum CDF version # to load
            Default: None

        latest_version: bool
            Only grab the latest CDF version in the requested time interval
            Default: False

        major_version: bool
            Only open the latest major CDF version (e.g., X in vX.Y.Z) in the requested time interval
            Default: False

        always_prompt: bool
            Set this keyword to always prompt for the user's username and password;
            useful if you accidentally save an incorrect password, or if your SDC password has changed
            Default: False

        spdf: bool
            If True, download the data from the SPDF instead of the SDC
            Default: False
            
    Returns
    -------
        list of str
            List of tplot variables created.

    Example
    -------

    >>> import pyspedas
    >>> from pytplot import tplot
    >>> fpi_vars = pyspedas.mms.mms_load_fpi(trange=['2015-10-16', '2015-10-17'], datatype='dis-moms')
    >>> tplot(['mms1_dis_bulkv_gse_fast', 'mms1_dis_numberdensity_fast'])

    """
    # different datatypes for burst mode files
    if data_rate.lower() == 'brst':
        if isinstance(datatype, str):
            if (datatype == '*' or datatype == '') and level.lower() != 'ql':
                datatype = ['des-dist', 'dis-dist', 'dis-moms', 'des-moms', 'dis-momsaux', 'des-momsaux']
    else:
        if isinstance(datatype, str):
            if (datatype == '*' or datatype == '') and level.lower() == 'ql':
                datatype = ['des', 'dis']
            if (datatype == '*' or datatype == '') and level.lower() != 'ql':
                datatype = ['des-dist', 'dis-dist', 'dis-moms', 'des-moms', 'dis-momsaux', 'des-momsaux']

    # kludge for level = 'sitl' -> datatype shouldn't be defined for sitl data.
    if level.lower() == 'sitl' or level.lower() == 'trig':
        datatype = ''

    if varformat is None and varnames == []:
        get_support_data = True

    tvars = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='fpi',
            datatype=datatype, varformat=varformat, varnames=varnames, suffix=suffix, get_support_data=get_support_data,
            time_clip=time_clip, no_update=no_update, center_measurement=center_measurement, available=available, 
            notplot=notplot, latest_version=latest_version, major_version=major_version, min_version=min_version, 
            cdf_version=cdf_version, spdf=spdf, always_prompt=always_prompt)
    
    if tvars is None or available or notplot or CONFIG['download_only']:
        return tvars

    mms_fpi_set_metadata(probe, data_rate, datatype, level, suffix=suffix)

    if not isinstance(probe, list): probe = [probe]
    if not isinstance(data_rate, list): data_rate = [data_rate]
    if not isinstance(datatype, list): datatype = [datatype]
    if not isinstance(level, list): level = [level]

    # the following kludge is due to the errorflags variable in the dist and moments files having the
    # same variable name, so loading d?s-dist and d?s-moms files at the same time will overwrite
    # one of the vars containing errorflags
    if 'des-dist' in datatype and 'des-moms' in datatype:
        # delete the old vars first
        del_data('*_des_errorflags_*')
        del_data('*_des_compressionloss_*')
        # load the bars with a suffix applied
        tplotnames_errflags_emom = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='fpi',
                              datatype='des-moms', varformat='*errorflags*|*compressionloss*', varnames=varnames,
                              suffix=suffix+'_moms', get_support_data=0,
                              time_clip=time_clip, no_update=no_update, center_measurement=center_measurement,
                              available=available,
                              notplot=notplot, latest_version=latest_version, major_version=major_version,
                              min_version=min_version,
                              cdf_version=cdf_version, spdf=spdf, always_prompt=always_prompt)
        tplotnames_errflags_edist = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='fpi',
                              datatype='des-dist', varformat='*errorflags*|*compressionloss*', varnames=varnames,
                              suffix=suffix+'_dist', get_support_data=0,
                              time_clip=time_clip, no_update=no_update, center_measurement=center_measurement,
                              available=available,
                              notplot=notplot, latest_version=latest_version, major_version=major_version,
                              min_version=min_version,
                              cdf_version=cdf_version, spdf=spdf, always_prompt=always_prompt)
        if tplotnames_errflags_emom is not None:
            tvars.extend(tplotnames_errflags_emom)
        if tplotnames_errflags_edist is not None:
            tvars.extend(tplotnames_errflags_edist)
    else:
        # user didn't request both dist and moments, so no variables should have been clobbered
        # but we still need to append _dist, _moms to the end of the names
        for prb in probe:
            for drate in data_rate:
                this_probe = str(prb)
                if 'des-dist' in datatype:
                    tplot_rename('mms'+this_probe+'_des_errorflags_'+drate+suffix, 'mms'+this_probe+'_des_errorflags_'+drate+suffix+'_dist')
                    tplot_rename('mms'+this_probe+'_des_compressionloss_'+drate+suffix, 'mms'+this_probe+'_des_compressionloss_'+drate+suffix+'_dist')
                    tvars.append('mms'+this_probe+'_des_errorflags_'+drate+suffix+'_dist')
                    tvars.append('mms'+this_probe+'_des_compressionloss_'+drate+suffix+'_dist')
                if 'des-moms' in datatype or 'des' in datatype:
                    tplot_rename('mms'+this_probe+'_des_errorflags_'+drate+suffix, 'mms'+this_probe+'_des_errorflags_'+drate+suffix+'_moms')
                    tplot_rename('mms'+this_probe+'_des_compressionloss_'+drate+suffix, 'mms'+this_probe+'_des_compressionloss_'+drate+suffix+'_moms')
                    tvars.append('mms'+this_probe+'_des_errorflags_'+drate+suffix+'_moms')
                    tvars.append('mms'+this_probe+'_des_compressionloss_'+drate+suffix+'_moms')

    # same kludge as above, but for ions
    if 'dis-dist' in datatype and 'dis-moms' in datatype:
        # delete the old vars first
        del_data('*_dis_errorflags_*')
        del_data('*_dis_compressionloss_*')
        # load the bars with a suffix applied
        tplotnames_errflags_imom = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='fpi',
                              datatype='dis-moms', varformat='*errorflags*|*compressionloss*', varnames=varnames,
                              suffix=suffix+'_moms', get_support_data=0,
                              time_clip=time_clip, no_update=no_update, center_measurement=center_measurement,
                              available=available,
                              notplot=notplot, latest_version=latest_version, major_version=major_version,
                              min_version=min_version,
                              cdf_version=cdf_version, spdf=spdf, always_prompt=always_prompt)
        tplotnames_errflags_idist = mms_load_data(trange=trange, probe=probe, data_rate=data_rate, level=level, instrument='fpi',
                              datatype='dis-dist', varformat='*errorflags*|*compressionloss*', varnames=varnames,
                              suffix=suffix+'_dist', get_support_data=0,
                              time_clip=time_clip, no_update=no_update, center_measurement=center_measurement,
                              available=available,
                              notplot=notplot, latest_version=latest_version, major_version=major_version,
                              min_version=min_version,
                              cdf_version=cdf_version, spdf=spdf, always_prompt=always_prompt)
        if tplotnames_errflags_imom is not None:
            tvars.extend(tplotnames_errflags_imom)
        if tplotnames_errflags_idist is not None:
            tvars.extend(tplotnames_errflags_idist)
    else:
        # user didn't request both dist and moments, so no variables should have been clobbered
        # but we still need to append _dist, _moms to the end of the names
        for prb in probe:
            for drate in data_rate:
                this_probe = str(prb)
                if 'dis-dist' in datatype:
                    tplot_rename('mms'+this_probe+'_dis_errorflags_'+drate+suffix, 'mms'+this_probe+'_dis_errorflags_'+drate+suffix+'_dist')
                    tplot_rename('mms'+this_probe+'_dis_compressionloss_'+drate+suffix, 'mms'+this_probe+'_dis_compressionloss_'+drate+suffix+'_dist')
                    tvars.append('mms'+this_probe+'_dis_errorflags_'+drate+suffix+'_dist')
                    tvars.append('mms'+this_probe+'_dis_compressionloss_'+drate+suffix+'_dist')
                if 'dis-moms' in datatype or 'dis' in datatype:
                    tplot_rename('mms'+this_probe+'_dis_errorflags_'+drate+suffix, 'mms'+this_probe+'_dis_errorflags_'+drate+suffix+'_moms')
                    tplot_rename('mms'+this_probe+'_dis_compressionloss_'+drate+suffix, 'mms'+this_probe+'_dis_compressionloss_'+drate+suffix+'_moms')
                    tvars.append('mms'+this_probe+'_dis_errorflags_'+drate+suffix+'_moms')
                    tvars.append('mms'+this_probe+'_dis_compressionloss_'+drate+suffix+'_moms')

    for prb in probe:
        for drate in data_rate:
            for dtype in datatype:
                for lvl in level:
                    out_var = mms_load_fpi_calc_pad(probe=prb, level=lvl, datatype=dtype, data_rate=drate, suffix=suffix, autoscale=True)
                    if out_var:
                        tvars.extend(out_var)

                    # create the error bars
                    # moments
                    if dtype == 'des-moms':
                        des_moms_eflags = mms_fpi_make_errorflagbars('mms' + str(prb) + '_des_errorflags_' + drate + '_moms', level=lvl)
                        if des_moms_eflags is not None:
                            tvars.extend(des_moms_eflags)

                    if dtype == 'dis-moms':
                        dis_moms_eflags = mms_fpi_make_errorflagbars('mms' + str(prb) + '_dis_errorflags_' + drate + '_moms', level=lvl)
                        if dis_moms_eflags is not None:
                            tvars.extend(dis_moms_eflags)

                    # distributions
                    if dtype == 'des-dist':
                        des_dist_eflags = mms_fpi_make_errorflagbars('mms' + str(prb) + '_des_errorflags_' + drate + '_dist', level=lvl)
                        if des_dist_eflags is not None:
                            tvars.extend(des_dist_eflags)

                    if dtype == 'dis-dist':
                        dis_dist_eflags = mms_fpi_make_errorflagbars('mms' + str(prb) + '_dis_errorflags_' + drate + '_dist', level=lvl)
                        if dis_dist_eflags is not None:
                            tvars.extend(dis_dist_eflags)

                    if drate == 'brst':
                        des_moms_comp = mms_fpi_make_compressionlossbars('mms' + str(prb) + '_des_compressionloss_' + drate + '_moms')
                        dis_moms_comp = mms_fpi_make_compressionlossbars('mms' + str(prb) + '_dis_compressionloss_' + drate + '_moms')
                        des_dist_comp = mms_fpi_make_compressionlossbars('mms' + str(prb) + '_des_compressionloss_' + drate + '_dist')
                        dis_dist_comp = mms_fpi_make_compressionlossbars('mms' + str(prb) + '_dis_compressionloss_' + drate + '_dist')

                        if des_moms_comp is not None:
                            tvars.extend(des_moms_comp)
                        if dis_moms_comp is not None:
                            tvars.extend(dis_moms_comp)
                        if des_dist_comp is not None:
                            tvars.extend(des_dist_comp)
                        if dis_dist_comp is not None:
                            tvars.extend(dis_dist_comp)
    return tvars
