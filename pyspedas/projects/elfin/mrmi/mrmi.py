from pyspedas.projects.elfin.load import load

def mrmi_load(trange=['2022-08-19', '2022-08-19'],
            probe='a',
            datatype='mrmi',
            level='l1',
            suffix='',
            get_support_data=False,
            varformat=None,
            varnames=[],
            downloadonly=False,
            notplot=False,
            no_update=False,
            time_clip=False,
            force_download=False):
    """
    This function loads data from the ELFIN Magneto Resistive Magnetometer (MRMi)

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2022-08-19', '2022-08-19']]

        probe: str
            Spacecraft identifier ('a' or 'b')
            Default: 'a'

        datatype: str
            Data type; Valid options::

                'mrmi' for L1 data

            Default: 'mrmi'

        level: str
            Data level; options: 'l1'
            efault: 'l1'

        suffix: str
            The tplot variable names will be given this suffix.
            Default: no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: only loads in data with a "VAR_TYPE" attribute of "data"

        varformat: str
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.
            Default: all variables are loaded in

        varnames: list of str
            List of variable names to load
            Default: all data variables are loaded

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
            Download file even if local version is more recent than server version
            Default: False

    Returns
    ----------
        List of tplot variables created.

    Example
    ----------
        import pyspedas
        from pytplot import tplot
        mrmi_vars = pyspedas.projects.elfin.mrmi(probe='b', trange=['2022-08-19', '2022-08-19']
        tplot('elb_mrmi')

    """
    tvars = load(instrument='mrmi', probe=probe, trange=trange, level=level, datatype=datatype, suffix=suffix,
                 get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly,
                 notplot=notplot, time_clip=time_clip, no_update=no_update, force_download=force_download)

    if tvars is None or notplot or downloadonly:
        return tvars

    return mrmi_postprocessing(tvars)

def mrmi_postprocessing(variables):
    """
    Placeholder for MRMa post-processing
    """
    return variables
