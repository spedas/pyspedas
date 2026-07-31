
import logging
from pyspedas import wildcard_expand
from pyspedas.projects.themis.load import load
from pyspedas.projects.themis.state_tools.autoload_support import autoload_support
from pyspedas.projects.themis.state_tools.spinmodel.eclipse_spinmodel_corrections_vector import eclipse_spinmodel_corrections_vector
from pyspedas.projects.themis.state_tools.spinmodel.spinmodel import get_spinmodel
from pyspedas import wildcard_expand, time_string
import logging


def efi(trange=['2007-03-23', '2007-03-24'],
        probe='c',
        level='l2',
        datatype=None,
        suffix='',
        get_support_data=False,
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False,
        apply_eclipse_corrections=False):
    """
    This function loads Electric Field Instrument (EFI) data

    Parameters
    ----------

        trange: list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2007-03-23', '2007-03-24']

        probe: str or list of str
            Spacecraft probe letter(s) ('a', 'b', 'c', 'd' and/or 'e')
            Default: 'c'

        level: str
            Processing level; Valid options: 'l1', 'l2'
            Default: 'l2'

        datatype: str or list of str
            Data type; Valid L1 options::

                'eff', Fast survey E12, E34, E56 waveforms
                'efp', Particle burst E12, E34, E56 waveforms
                'efw', Wave burst E12 E34, E56 waveforms
                'vaf', Fast survey voltage group A, V1-V6 boom voltages
                'vap', Particle burst voltage group A, V1-V6 boom voltages
                'vaw', Wave burst voltage group A, V1-V6 boom voltages
                'vbf', Fast survey voltage group B, V1-V6 boom voltages
                'vbp', Particle burst voltage group B, V1-V6 boom voltages
                'vbw', Wave burst voltage group B, V1-V6 boom voltages
                L1 default: [eff. efp, efw, vaf. vap, vaw]

            Valid L2 options::

                'efi', Fast survey E field vectors and other quantities
                'efp', Particle burst E field vectors
                'efw', Wave burst E field vectors
                L2 default: efi

        suffix: str
            The tplot variable names will be given this suffix.
            Default: no suffix

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  
            Default: False; only loads data with a "VAR_TYPE" attribute of "data"

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: None; all variables are loaded

        varnames: list of str
            List of variable names to load
            Default: Empty list, so all data variables are loaded

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
            Time clip the variables to exactly the range specified
            in the trange keyword
            Default: False
            
        apply_eclipse_corrections: bool
            If True, apply eclipse spin model corrections to output variables as appropriate.
            Default: False

    Returns
    -------
    List of str
        List of tplot variables created
        Empty list if no data
    
    Example
    -------
        >>> import pyspedas
        >>> from pyspedas import tplot
        >>> efi_vars = pyspedas.projects.themis.efi(probe='d', trange=['2013-11-5', '2013-11-6'])
        >>> tplot('thd_efs_dot0_gse')


    """
    valid_levels = ['l1', 'l2']
    valid_l1_datatypes = ['eff', 'efp', 'efw', 'vaf', 'vap', 'vaw', 'vbf', 'vbp', 'vbw']
    default_l1_datatypes = ['eff', 'efp', 'efw', 'vaf', 'vap', 'vaw']  # omit vb* by default
    valid_l2_datatypes = ['efi', 'efp', 'efw']
    default_l2_datatypes = ['efi'] # omit efp and efw unless specifically requested

    if level.lower() not in valid_levels:
        logging.error("Unrecognized level %s", level)
        return []

    level=level.lower()

    if level == 'l1':
        valid_datatypes=valid_l1_datatypes
        default_datatypes=default_l1_datatypes
    else:
        valid_datatypes=valid_l2_datatypes
        default_datatypes=default_l2_datatypes

    if datatype is None:
        selected_datatype=default_datatypes
    else:
        selected_datatype=wildcard_expand(valid_datatypes, datatype, case_sensitive=False)

    if len(selected_datatype) == 0:
        logging.error("No valid datatypes selected")
        return []

    loaded_vars =  load(instrument='efi', trange=trange, level=level,
                datatype=selected_datatype,
                suffix=suffix, get_support_data=get_support_data,
                varformat=varformat, varnames=varnames,
                downloadonly=downloadonly, notplot=notplot,
                probe=probe, time_clip=time_clip, no_update=no_update)
    
    if not downloadonly and level=='l2' and apply_eclipse_corrections:
        p = probe
        autoload_support(probe=p, trange=trange, spinmodel=True)
        sm_spinfit = get_spinmodel(probe=p, correction_level=2, quiet=True)
        start_times, end_times, flags, flag_strings = sm_spinfit.eclipse_correction_status()
        n = len(start_times)
        if n > 0:
            logging.info(f"Eclipse correction status for probe {probe}:")
            for i in range(n):
                logging.info(
                    f"Eclipse {i + 1} of {n}: start: {time_string(start_times[i])}  end: {time_string(end_times[i])} status: {flag_strings[i]}"
                )
            probe_vars = wildcard_expand(loaded_vars, "th" + p + "_*")
            for v in probe_vars:
                if ("btotal" in v) or ("_q_" in v) :
                    pass
                elif "efs" in v:
                    # These are spin fits, but they're not the *onboard* spin fits that rely on
                    # the onboard spin sectoring clock. They won't suffer from the sudden-onset fixed
                    # spin plan offset that happens when the onboard spin sectoring clock is disrupted.
                    # So they should probably be corrected using the waveform model,
                    # rather than the spin fit model.
                    logging.info(f"Applying waveform eclipse corrections to {v}")
                    eclipse_spinmodel_corrections_vector(v, p, spin_based=False)
                else:
                    logging.info(f"Applying waveform eclipse corrections to {v}")
                    eclipse_spinmodel_corrections_vector(v, p, spin_based=False)

    return loaded_vars