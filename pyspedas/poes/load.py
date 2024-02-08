from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['2018-11-5', '2018-11-6'], 
         probe=['noaa19'],
         instrument='sem', 
         datatype='*', 
         suffix='', 
         get_support_data=False, 
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False):
    """
    This function loads POES Space Environment Monitor data. This function is
    not meant to be called directly; instead, see the wrapper:
        pyspedas.poes.sem

    Parameters
    ----------
        trange : list of str, default=['2018-11-5', '2018-11-6']
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str or list of str, default=['noaa19']
            POES spacecraft name(s); e.g., metop1, metop2, noaa15, noaa16,
            noaa18, noaa19

        instrument: str, default='sem'
             Name of the instrument.

        datatype: str, default='*'
            This variable is unused. It is reserved for the future use.

        suffix: str, optional
            The tplot variable names will be given this suffix.  By default,
            no suffix is added.

        get_support_data: bool, default=False
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.  By default, only loads in data with a
            "VAR_TYPE" attribute of "data".

        varformat: str, default=False
            The file variable formats to load into tplot.  Wildcard character
            "*" is accepted.  By default, all variables are loaded in.

        varnames: list of str, optional
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
    dict or list
        List of tplot variables created.

    Examples
    --------
    This function is not intended to be called directly.
    """

    if not isinstance(probe, list):
        probe = [probe]

    out_files = []

    for prb in probe:
        if instrument == 'sem':
            pathformat = prb + '/sem2_fluxes-2sec/%Y/' + prb + '_poes-sem2_fluxes-2sec_%Y%m%d_v??.cdf'

        # find the full remote path names using the trange
        remote_names = dailynames(file_format=pathformat, trange=trange)

        files = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'], local_path=CONFIG['local_data_dir'], no_download=no_update)
        if files is not None:
            for file in files:
                out_files.append(file)

    out_files = sorted(out_files)

    if downloadonly:
        return out_files

    tvars = cdf_to_tplot(out_files, suffix=suffix, get_support_data=get_support_data, varformat=varformat, varnames=varnames, notplot=notplot)

    if notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars
