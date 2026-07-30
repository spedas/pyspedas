
from pyspedas.projects.themis.load import load
from pyspedas.projects.themis.state_tools.autoload_support import autoload_support
from pyspedas.projects.themis.state_tools.spinmodel.eclipse_spinmodel_corrections_vector import eclipse_spinmodel_corrections_vector
from pyspedas.projects.themis.state_tools.spinmodel.spinmodel import get_spinmodel
from pyspedas import wildcard_expand, time_string
import logging


def scm(trange=['2007-03-23', '2007-03-24'],
        probe='c',
        level='l2',
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
    This function loads Search-coil magnetometer (SCM) data

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2007-03-23', '2007-03-24']

        probe: str or list of str
            Spacecraft probe letter(s) ('a', 'b', 'c', 'd' and/or 'e')
            Default: 'c'

        level: str
            Data level; Valid options: 'l1', 'l2'
            Default: 'l2'

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

        apply_eclipse_correctios: bool
            If True, apply eclipse spinmodel corrections to output variables as appropriate
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
        >>> scm_vars = pyspedas.projects.themis.scm(probe='d', trange=['2013-11-05', '2013-11-06'])
        >>> tplot(['thd_scf_btotal', 'thd_scf_gse'])

    """
    loaded_vars =  load(instrument='scm', trange=trange, level=level,
                suffix=suffix, get_support_data=get_support_data,
                varformat=varformat, varnames=varnames,
                downloadonly=downloadonly, notplot=notplot,
                probe=probe, time_clip=time_clip, no_update=no_update)
    
    if not isinstance(level, list):
        level = [level]

    if not isinstance(probe, list):
        probe = [probe]
        
    for l in level:
        for p in probe:
            if l == 'l2' and apply_eclipse_corrections:
                autoload_support(probe=p, trange=trange, spinmodel=True)
                sm_spinfit=get_spinmodel(probe=p,correction_level=2,quiet=True)
                start_times, end_times, flags, flag_strings = sm_spinfit.eclipse_correction_status()
                n = len(start_times)
                if n > 0:
                    logging.info(f"Eclipse correction status for probe {probe}:")
                    for i in range(n):
                        logging.info(f"Eclipse {i+1} of {n}: start: {time_string(start_times[i])}  end: {time_string(end_times[i])} status: {flag_strings[i]}")
                    probe_vars = wildcard_expand(loaded_vars,'th'+p+'_*')
                    for v in probe_vars:
                        if 'btotal' in v:
                            pass
                        else:
                            logging.info(f"Applying waveform eclipse corrections to {v}")
                            eclipse_spinmodel_corrections_vector(v, p, spin_based=False)

    return loaded_vars

