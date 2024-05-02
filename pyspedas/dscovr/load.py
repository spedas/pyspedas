from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=['2018-10-16', '2018-10-17'], 
         instrument='mag', 
         datatype='h0', 
         suffix='',
         prefix='',
         get_support_data=False, 
         varformat=None,
         varnames=[],
         downloadonly=False,
         notplot=False,
         no_update=False,
         time_clip=False):
    """
    This function loads DSCOVR data into tplot variables; this function is not 
    meant to be called directly; instead, see the wrappers: 
        dscovr.mag: Fluxgate Magnetometer data
        dscovr.fc: Faraday Cup data
        dscovr.orb: Ephemeris data
        dscovr.att: Attitude data
        dscovr.all: Load all data

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            Default: ['2018-10-16', '2018-10-17']

        instrument: str
            type of instrument ('mag', 'fc', 'orb', 'att', 'all')
            Default: 'mag'

        datatype: str
            type of data
                mag: 'h0'
                fc: 'h1'
                orb: 'orbit'
                att: 'orbit'
                all: ['h0', 'h1', 'orbit']
            Default: 'h0'

        suffix: str
            The tplot variable names will be given this suffix.
            Default: no suffix is added

        prefix: str
            The tplot variable names will be given this prefix.
            Default: no prefix is added

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot.
            Default: only loads in data with a "VAR_TYPE" attribute of "data".

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

   Returns
    ----------
        List of tplot variables created.

    Example
    ----------
        import pyspedas
        from pytplot import tplot
        mag_vars = pyspedas.dscovr.mag(trange=['2018-11-5', '2018-11-6'])
        tplot('dsc_h0_mag_B1GSE')

    """

    remote_path = datatype + '/' + instrument + '/%Y/'

    if instrument == 'mag':
        if datatype == 'h0':
            pathformat = remote_path + 'dscovr_h0_mag_%Y%m%d_v??.cdf'
    elif instrument == 'faraday_cup':
        if datatype == 'h1':
            pathformat = remote_path + 'dscovr_h1_fc_%Y%m%d_v??.cdf'
    elif instrument == 'pre_or':
        if datatype == 'orbit':
            pathformat = remote_path + 'dscovr_orbit_pre_%Y%m%d_v??.cdf'
    elif instrument == 'def_at':
        if datatype == 'orbit':
            pathformat = remote_path + 'dscovr_at_def_%Y%m%d_v??.cdf'

    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat, trange=trange)

    out_files = []

    files = download(remote_file=remote_names, remote_path=CONFIG['remote_data_dir'], local_path=CONFIG['local_data_dir'], no_download=no_update)
    if files is not None:
        for file in files:
            out_files.append(file)

    out_files = sorted(out_files)

    if downloadonly:
        return out_files

    tvars = cdf_to_tplot(out_files, prefix=prefix, suffix=suffix, 
        get_support_data=get_support_data, varformat=varformat, 
        varnames=varnames, notplot=notplot)

    if notplot:
        return tvars
        
    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix='')

    return tvars
