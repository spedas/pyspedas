import pyspedas
# from pyspedas.projects.rbsp import load, rbsp_load_rbspice_read, rbsp_rbspice_omni, rbsp_rbspice_spin_avg
from .load import load
from .rbspice_lib.rbsp_load_rbspice_read import rbsp_load_rbspice_read
from .rbspice_lib.rbsp_rbspice_omni import rbsp_rbspice_omni
from .rbspice_lib.rbsp_rbspice_spin_avg import rbsp_rbspice_spin_avg


def rbspice(trange=['2018-11-5', '2018-11-6'],
            probe='a',
            datatype='TOFxEH',
            level='l3',
            prefix='',
            suffix='',
            force_download=False,
            get_support_data=True,
            varformat=None,
            varnames=[],
            downloadonly=False,
            notplot=False,
            no_update=False,
            time_clip=False):
    """
    This function loads data from the Radiation Belt Storm Probes Ion Composition Experiment (RBSPICE) instrument

    Parameters
    ----------
        trange : list of str, default=['2018-11-5', '2018-11-6']
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str, default='a'
            Spacecraft probe name: 'a' or 'b'

        datatype: str, default='TOFxEH'
            Data type; Valid options are specific to different data levels.

        level : str, default='l3'
            Data level. Valid options: 'l1', 'l2', 'l3'

        prefix : str, optional
            The tplot variable names will be given this prefix. By default, no prefix is added.

        suffix: str, optional
            The tplot variable names will be given this suffix.  By default,
            no suffix is added.

        force_download : bool, default=False
            Download file even if local version is more recent than server version.

        get_support_data: bool, default=True
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a
            "VAR_TYPE" attribute of "data".

        varformat: str, optional
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool, default=False
            Set this flag to download the CDF files, but not load them into
            tplot variables

        notplot: bool, default=False
            Return the data in hash tables instead of creating tplot variables

        no_update: bool, default=False
            If set, only load data from your local cache

        time_clip: bool, default=False
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    -------
    tvars : dict or list
        List of created tplot variables or dict of data tables if notplot is True.

    Examples
    --------
    >>> rbspice_vars = pyspedas.projects.rbsp.rbspice(trange=['2018-11-5', '2018-11-6'], datatype='TOFxEH', level='l3')
    >>> tplot('rbspa_rbspice_l3_TOFxEH_proton_omni_spin')

    # Calculate the pitch angle distributions
    >>> from pyspedas.projects.rbsp.rbspice_lib.rbsp_rbspice_pad import rbsp_rbspice_pad
    >>> rbsp_rbspice_pad(probe='a', datatype='TOFxEH', level='l3')
    >>> tplot('rbspa_rbspice_l3_TOFxEH_proton_omni_0-1000keV_pad_spin')
    """

    # Valid names
    vprobe = ['a', 'b']
    vlevels = ['l1', 'l2', 'l3', 'l4']
    vdatatypesl1 = ['TOFxEH', 'TOFxEnonH', 'TOFxPHHHELT']
    vdatatypesl2 = ['TOFxEH', 'TOFxEnonH', 'TOFxPHHHELT']
    vdatatypesl3 = ['TOFxEH', 'TOFxEnonH', 'TOFxPHHHELT']
    vdatatypesl3pap = ['']  # L3PAP data is not yet supported
    vdatatypesl4 = ['']  # L4 data is not yet supported
    vdatatypes = vdatatypesl1 + vdatatypesl2 + vdatatypesl3 + vdatatypesl3pap + vdatatypesl4
    vdatatypes_lower = [vdatatype.lower() for vdatatype in vdatatypes]

    tvars = load(instrument='rbspice', trange=trange, probe=probe, datatype=datatype, level=level, prefix=prefix, suffix=suffix, force_download=force_download, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

    if tvars is None or notplot or downloadonly:
        return tvars

    if not isinstance(probe, list):
        probe = [probe]

    if datatype.lower() in vdatatypes_lower:
        for prb in probe:
            # Add energy channel energy values to primary data variable,
            # create variables for individual telescopes, and set appropriate tplot options
            rbsp_load_rbspice_read(level=level, probe=prb, datatype=datatype)

            # Calculate omni-directional variable
            omni_vars = rbsp_rbspice_omni(probe=prb, datatype=datatype, level=level)
            if omni_vars:
                tvars.extend(omni_vars)

            # Calculate spin-averaged variable
            sp_avg_vars = rbsp_rbspice_spin_avg(probe=prb, datatype=datatype, level=level)
            if sp_avg_vars:
                tvars.extend(sp_avg_vars)

    return tvars
