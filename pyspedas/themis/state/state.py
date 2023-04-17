from pyspedas.themis.load import load
from pyspedas.utilities.data_exists import data_exists
from pyspedas.themis.state.apply_spinaxis_corrections import apply_spinaxis_corrections
from pyspedas.themis.state.spinmodel.spinmodel_postprocess import spinmodel_postprocess
from pytplot import del_data


def state(trange=['2007-03-23', '2007-03-24'],
          probe='c',
          level='l1',
          suffix='',
          get_support_data=False,
          varformat=None,
          varnames=[],
          downloadonly=False,
          notplot=False,
          no_update=False,
          time_clip=False,
          keep_spin=False):
    """
    This function loads THEMIS state data

    Parameters:
        trange: list of str
            time range of interest [starttime, endtime] with the format
            ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str or list of str
            Spacecraft probe letter(s) ('a', 'b', 'c', 'd' and/or 'e')

        level: str
            Data type; Valid options: 'l1'

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
            List of variable names to load
            (if not specified, all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified
            in the trange keyword

        keep_spin: bool
            If True, do not delete the spin model tplot variables after the spin models are built.

    Returns:
        List of tplot variables created.

    """
    # If support data is being loaded, premptively delete the thx_spinras_correction and thx_spindec_correction
    # variables, to avoid dangling corrections if they don't exist in this time interval.
    if get_support_data:
        for p in probe:
            spinras_corrvar='th'+probe+'_spinras_correction'
            spindec_corrvar='th'+probe+'_spindec_correction'
            if data_exists(spinras_corrvar):
                del_data(spinras_corrvar)
            if data_exists(spindec_corrvar):
                del_data(spindec_corrvar)

    res = load(instrument='state', trange=trange, level=level, probe=probe,
               suffix=suffix, get_support_data=get_support_data,
               varformat=varformat, varnames=varnames,
               downloadonly=downloadonly, notplot=notplot,
               time_clip=time_clip, no_update=no_update)
    if get_support_data:
        for p in probe:
            # Process spin model variables
            spinmodel_postprocess(p)
            if not keep_spin:
                spinvar_pattern = 'th' + p + '_spin_*'
                del_data(spinvar_pattern)
            # Perform spin axis RA and Dec corrections
            spinras_var = 'th' + p + '_spinras'
            delta_spinras_var = 'th' + p + '_spinras_correction'
            corrected_spinras_var = 'th' + p + '_spinras_corrected'

            spindec_var = 'th' + p + '_spindec'
            delta_spindec_var = 'th' + p + '_spindec_correction'
            corrected_spindec_var = 'th' + p + '_spindec_corrected'

            apply_spinaxis_corrections(spinras=spinras_var, delta_spinras=delta_spinras_var,
                                       corrected_spinras=corrected_spinras_var, spindec=spindec_var,
                                       delta_spindec=delta_spindec_var, corrected_spindec=corrected_spindec_var)
    return res
