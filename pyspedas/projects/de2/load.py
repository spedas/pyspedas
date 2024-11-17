from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG


def load(
    trange=["1982-12-06", "1982-12-07"],
    instrument="mag",
    prefix="",
    suffix="",
    get_support_data=False,
    varformat=None,
    varnames=[],
    downloadonly=False,
    notplot=False,
    no_update=False,
    time_clip=False,
    force_download=False,
):
    """
    This function loads data from the DE2 mission.

    Data is available for three years: 1981, 1982, and 1983.

    Parameters
    ----------
    trange : list of str, optional
        Time range of interest [starttime, endtime] with the format
        ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
        ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss'].
        Default is ["1982-12-06", "1982-12-07"].
        Data is available only for years 1981, 1982, 1983.
    instrument : str, optional
        Valid options are: 'mag', 'nacs', 'rpa', 'idm', 'wats', 'vefi', 'lang'.
        Default is 'mag'.
        Each instrument has only one datatype available, so the datatype is not a keyword option.
    prefix : str, optional
        The tplot variable names will be given this prefix.
        Default is no prefix is added.
    suffix : str, optional
        The tplot variable names will be given this suffix.
        Default is no suffix is added.
    get_support_data : bool, optional
        Data with an attribute "VAR_TYPE" with a value of "support_data"
        will be loaded into tplot.
        Default is only loads in data with a "VAR_TYPE" attribute of "data".
    varformat : str, optional
        The file variable formats to load into tplot.
        Wildcard character "*" is accepted.
        Default is all variables are loaded in.
    varnames : list of str, optional
        List of variable names to load.
        Default is all data variables are loaded.
    downloadonly : bool, optional
        Set this flag to download the CDF files, but not load them into tplot variables.
        Default is False.
    notplot : bool, optional
        Return the data in hash tables instead of creating tplot variables.
        Default is False.
    no_update : bool, optional
        If set, only load data from your local cache.
        Default is False.
    time_clip : bool, optional
        Time clip the variables to exactly the range specified in the trange keyword.
        Default is False.
    force_download : bool, optional
        Download file even if local version is more recent than server version.
        Default is False.

    Returns
    -------
    list
        List of tplot variables created.
        If notplot is set to True, returns a list of dictionaries containing the data.
        If downloadonly is set to True, returns a list of the downloaded files.


    Examples
    --------
    >>> import pyspedas
    >>> vars = pyspedas.projects.de2.load(instrument='mag', trange=['1983-02-10', '1983-02-11'], datatype='62ms', prefix = 'de2_')
    >>> print(vars)
    ['de2_ex', 'de2_ey', 'de2_bx', 'de2_by', 'de2_bz', 'de2_bxm', 'de2_bym', 'de2_bzm',
    'de2_glat', 'de2_glon', 'de2_ilat', 'de2_mlt', 'de2_alt']

    >>> import pyspedas
    >>> vars = pyspedas.projects.de2.lang(trange=['1983-02-10', '1983-02-11'], prefix = 'de2_')
    >>> print(vars)
    ['de2_OrbitNumber', 'de2_electronTemp', 'de2_plasmaDensity', 'de2_satPotential',
    'de2_alt', 'de2_glat', 'de2_glon', 'de2_lst', 'de2_lmt', 'de2_L', 'de2_ilat', 'de2_sza']
    """

    mastercdf = None
    addmaster = False
    masterpath = "https://cdaweb.gsfc.nasa.gov/pub/software/cdawlib/0MASTERS/"
    local_master_dir = CONFIG["local_data_dir"] + "de2_masters/"
    tvars = []

    if instrument == "mag":
        # https://spdf.gsfc.nasa.gov/pub/data/de/de2/magnetic_electric_fields_vefi_magb/62ms_vefimagb_cdaweb/
        datatype = "62ms"  # this is the only available datatype
        pathformat = (
            "magnetic_electric_fields_vefi_magb/"
            + datatype
            + "_vefimagb_cdaweb/%Y/de2_"
            + datatype
            + "_vefimagb_%Y%m%d_v??.cdf"
        )
    elif instrument == "nacs":
        # https://spdf.gsfc.nasa.gov/pub/data/de/de2/neutral_gas_nacs/neutral1s_nacs_cdaweb/
        datatype = "neutral1s"  # this is the only available datatype
        pathformat = (
            "neutral_gas_nacs/"
            + datatype
            + "_"
            + instrument
            + "_cdaweb/%Y/de2_"
            + datatype
            + "_"
            + instrument
            + "_%Y%m%d_v??.cdf"
        )
    elif instrument == "rpa":
        # https://spdf.gsfc.nasa.gov/pub/data/de/de2/plasma_rpa/ion2s_cdaweb/
        datatype = "ion2s"  # this is the only available datatype
        pathformat = (
            "plasma_rpa/"
            + datatype
            + "_cdaweb/%Y/de2_"
            + datatype
            + "_"
            + instrument
            + "_%Y%m%d_v??.cdf"
        )
    elif instrument == "fpi":
        # https://spdf.gsfc.nasa.gov/pub/data/de/de2/neutral_gas_fpi/de2_neutral8s_fpi/
        datatype = "8s"  # this is the only available datatype
        pathformat = (
            "neutral_gas_fpi/de2_neutral8s_fpi/%Y/de2_neutral"
            + datatype
            + "_"
            + instrument
            + "_%Y%m%d_v??.cdf"
        )
    elif instrument == "idm":
        # https://spdf.gsfc.nasa.gov/pub/data/de/de2/plasma_idm/vion250ms_cdaweb/
        datatype = "250ms"  # this is the only available datatype
        masterfile = "de2_vion250ms_idm_00000000_v01.cdf"
        addmaster = True
        pathformat = (
            "plasma_idm/vion250ms_cdaweb/%Y/de2_vion"
            + datatype
            + "_"
            + instrument
            + "_%Y%m%d_v??.cdf"
        )
    elif instrument == "wats":
        # https://spdf.gsfc.nasa.gov/pub/data/de/de2/neutral_gas_wats/wind2s_wats_cdaweb/
        datatype = "2s"  # this is the only available datatype
        pathformat = (
            "neutral_gas_wats/wind2s_wats_cdaweb/%Y/de2_wind"
            + datatype
            + "_"
            + instrument
            + "_%Y%m%d_v??.cdf"
        )
    elif instrument == "vefi":
        # https://spdf.gsfc.nasa.gov/pub/data/de/de2/electric_fields_vefi/dca500ms_vefi_cdaweb/
        datatype = "ac500ms"  # this is the only available datatype
        pathformat = (
            "electric_fields_vefi/"
            + datatype
            + "_vefi_cdaweb/%Y/de2_"
            + datatype
            + "_"
            + instrument
            + "_%Y%m%d_v??.cdf"
        )
    elif instrument == "lang":
        # https://spdf.gsfc.nasa.gov/pub/data/de/de2/plasma_lang/plasma500ms_lang_cdaweb/
        datatype = "500ms"  # this is the only available datatype
        pathformat = (
            "plasma_lang/plasma500ms_lang_cdaweb/%Y/de2_plasma"
            + datatype
            + "_"
            + instrument
            + "_%Y%m%d_v??.cdf"
        )

    if addmaster:
        mastercdf = download(
            remote_file=masterfile,
            remote_path=masterpath,
            local_path=local_master_dir,
            no_download=no_update,
            force_download=force_download,
        )
    else:
        mastercdf = [None]
    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat, trange=trange)

    out_files = []

    files = download(
        remote_file=remote_names,
        remote_path=CONFIG["remote_data_dir"],
        local_path=CONFIG["local_data_dir"],
        no_download=no_update,
        force_download=force_download,
    )
    if files is not None:
        for file in files:
            out_files.append(file)

    out_files = sorted(out_files)

    if downloadonly:
        return out_files

    if len(out_files) > 0:
        tvars = cdf_to_tplot(
            out_files,
            mastercdf=mastercdf[0],
            prefix=prefix,
            suffix=suffix,
            get_support_data=get_support_data,
            varformat=varformat,
            varnames=varnames,
            notplot=notplot,
        )

        if notplot:
            return tvars

        if len(tvars) > 0 and time_clip:
            tclip(tvars, trange[0], trange[1], suffix="")

    return tvars
