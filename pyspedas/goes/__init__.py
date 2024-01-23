from .load import load, loadr
from .load_orbit import load_orbit


def orbit(
    trange=["2013-11-5", "2013-11-6"],
    probe="15",
    prefix="",
    suffix="",
    downloadonly=False,
    no_update=False,
    notplot=False,
    get_support_data=False,
    varformat=None,
    varnames=[],
    time_clip=True,
):
    """

    This function loads GOES orbit data (probes 8-18)

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str/int or list of strs/ints
            GOES spacecraft #, e.g., probe=15

        prefix: str
            The tplot variable names will be given this prefix.
            By default, no prefix is added.
            If 'probename' then the name will be used, for example g16.

        suffix: str
            The tplot variable names will be given this suffix.
            By default, no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables

        notplot: bool
            If set, load the data into dictionaries containing the numpy objects instead
            of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    -------
        List of tplot variables created. Or list of filenames downloaded.

    """
    return load_orbit(
        trange=trange,
        probe=probe,
        varnames=varnames,
        varformat=varformat,
        prefix=prefix,
        suffix=suffix,
        downloadonly=downloadonly,
        no_update=no_update,
        time_clip=time_clip,
        notplot=notplot,
        get_support_data=get_support_data,
    )


def fgm(
    trange=["2013-11-5", "2013-11-6"],
    probe="15",
    datatype="1min",
    prefix="",
    suffix="",
    downloadonly=False,
    no_update=False,
    time_clip=False,
):
    """
    This function loads data from the GOES Magnetometer  (probes 8-15)

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str/int or list of strs/ints
            GOES spacecraft #, e.g., probe=15

        datatype: str
            Data type; Valid options:

        prefix: str
            The tplot variable names will be given this prefix.
            By default, no prefix is added.
            If 'probename' then the name will be used, for example g16.

        suffix: str
            The tplot variable names will be given this suffix.
            By default, no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    -------
        List of tplot variables created. Or list of filenames downloaded.

    """
    return load(
        instrument="fgm",
        trange=trange,
        probe=probe,
        datatype=datatype,
        prefix=prefix,
        suffix=suffix,
        downloadonly=downloadonly,
        time_clip=time_clip,
        no_update=no_update,
    )


def eps(
    trange=["2013-11-5", "2013-11-6"],
    probe="12",
    datatype="1min",
    prefix="",
    suffix="",
    downloadonly=False,
    no_update=False,
    time_clip=False,
):
    """
    This function loads data from the GOES energetic particle sensor  (probes 8-15)

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str/int or list of strs/ints
            GOES spacecraft #, e.g., probe=15

        datatype: str
            Data type; Valid options:

        prefix: str
            The tplot variable names will be given this prefix.
            By default, no prefix is added.
            If 'probename' then the name will be used, for example g16.

        suffix: str
            The tplot variable names will be given this suffix.
            By default, no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    -------
        List of tplot variables created. Or list of filenames downloaded.

    """
    return load(
        instrument="eps",
        trange=trange,
        probe=probe,
        datatype=datatype,
        prefix=prefix,
        suffix=suffix,
        downloadonly=downloadonly,
        time_clip=time_clip,
        no_update=no_update,
    )


def epead(
    trange=["2013-11-5", "2013-11-6"],
    probe="15",
    datatype="1min",
    prefix="",
    suffix="",
    downloadonly=False,
    no_update=False,
    time_clip=False,
):
    """
    This function loads data from the GOES Electron, Proton, Alpha Detector  (probes 8-15)

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str/int or list of strs/ints
            GOES spacecraft #, e.g., probe=15

        datatype: str
            Data type; Valid options:

        prefix: str
            The tplot variable names will be given this prefix.
            By default, no prefix is added.
            If 'probename' then the name will be used, for example g16.

        suffix: str
            The tplot variable names will be given this suffix.
            By default, no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    -------
        List of tplot variables created. Or list of filenames downloaded.

    """
    return load(
        instrument="epead",
        trange=trange,
        probe=probe,
        datatype=datatype,
        prefix=prefix,
        suffix=suffix,
        downloadonly=downloadonly,
        time_clip=time_clip,
        no_update=no_update,
    )


def maged(
    trange=["2013-11-5", "2013-11-6"],
    probe="15",
    datatype="1min",
    prefix="",
    suffix="",
    downloadonly=False,
    no_update=False,
    time_clip=False,
):
    """
    This function loads data from the GOES Magnetospheric Electron Detector (probes 8-15)

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str/int or list of strs/ints
            GOES spacecraft #, e.g., probe=15

        datatype: str
            Data type; Default '1min'

        prefix: str
            The tplot variable names will be given this prefix.
            By default, no prefix is added.
            If 'probename' then the name will be used, for example g16.

        suffix: str
            The tplot variable names will be given this suffix.
            By default, no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    -------
        List of tplot variables created. Or list of filenames downloaded.

    """
    return load(
        instrument="maged",
        trange=trange,
        probe=probe,
        datatype=datatype,
        prefix=prefix,
        suffix=suffix,
        downloadonly=downloadonly,
        time_clip=time_clip,
        no_update=no_update,
    )


def magpd(
    trange=["2013-11-5", "2013-11-6"],
    probe="15",
    datatype="1min",
    prefix="",
    suffix="",
    downloadonly=False,
    no_update=False,
    time_clip=False,
):
    """
    This function loads data from the GOES Magnetospheric Proton Detector (probes 8-15)

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str/int or list of strs/ints
            GOES spacecraft #, e.g., probe=15

        datatype: str
            Data type; Default '1min'

        prefix: str
            The tplot variable names will be given this prefix.
            By default, no prefix is added.
            If 'probename' then the name will be used, for example g16.

        suffix: str
            The tplot variable names will be given this suffix.
            By default, no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    -------
        List of tplot variables created. Or list of filenames downloaded.

    """
    return load(
        instrument="magpd",
        trange=trange,
        probe=probe,
        datatype=datatype,
        prefix=prefix,
        suffix=suffix,
        downloadonly=downloadonly,
        time_clip=time_clip,
        no_update=no_update,
    )


def hepad(
    trange=["2013-11-5", "2013-11-6"],
    probe="15",
    datatype="1min",
    prefix="",
    suffix="",
    downloadonly=False,
    no_update=False,
    time_clip=False,
):
    """
    This function loads data from the GOES High energy Proton and Alpha Detector (probes 8-15)

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str/int or list of strs/ints
            GOES spacecraft #, e.g., probe=15

        datatype: str
            Data type; Default '1min'

        prefix: str
            The tplot variable names will be given this prefix.
            By default, no prefix is added.
            If 'probename' then the name will be used, for example g16.

        suffix: str
            The tplot variable names will be given this suffix.
            By default, no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    -------
        List of tplot variables created. Or list of filenames downloaded.

    """
    return load(
        instrument="hepad",
        trange=trange,
        probe=probe,
        datatype=datatype,
        prefix=prefix,
        suffix=suffix,
        downloadonly=downloadonly,
        time_clip=time_clip,
        no_update=no_update,
    )


def xrs(
    trange=["2013-11-5", "2013-11-6"],
    probe="15",
    datatype="1min",
    prefix="",
    suffix="",
    downloadonly=False,
    no_update=False,
    time_clip=False,
):
    """
    This function loads data from the GOES X-ray Sensor (probes 8-18)

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str/int or list of strs/ints
            GOES spacecraft #, e.g., probe=15

        datatype: str
            Data type; Default '1min'

        prefix: str
            The tplot variable names will be given this prefix.
            By default, no prefix is added.
            If 'probename' then the name will be used, for example g16.

        suffix: str
            The tplot variable names will be given this suffix.
            By default, no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    -------
        List of tplot variables created. Or list of filenames downloaded.

    """
    return load(
        instrument="xrs",
        trange=trange,
        probe=probe,
        datatype=datatype,
        prefix=prefix,
        suffix=suffix,
        downloadonly=downloadonly,
        time_clip=time_clip,
        no_update=no_update,
    )


def euvs(
    trange=["2023-01-30", "2023-01-31"],
    probe="16",
    datatype="1min",
    prefix="",
    suffix="",
    downloadonly=False,
    no_update=False,
    time_clip=False,
):
    """
    This function loads data from the GOES Extreme Ultraviolet Sensor (EUVS), (probes 16-18)

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str/int or list of strs/ints
            GOES spacecraft #, e.g., probe=16

        datatype: str
            Data type; Default '1min'

        prefix: str
            The tplot variable names will be given this prefix.
            By default, no prefix is added.
            If 'probename' then the name will be used, for example g16.

        suffix: str
            The tplot variable names will be given this suffix.
            By default, no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    -------
        List of tplot variables created. Or list of filenames downloaded.

    """
    return load(
        instrument="euvs",
        trange=trange,
        probe=probe,
        datatype=datatype,
        prefix=prefix,
        suffix=suffix,
        downloadonly=downloadonly,
        time_clip=time_clip,
        no_update=no_update,
    )


def mag(
    trange=["2023-01-30", "2023-01-31"],
    probe="16",
    datatype="1min",
    prefix="",
    suffix="",
    downloadonly=False,
    no_update=False,
    time_clip=False,
):
    """
    This function loads data from the GOES Magnetometer, (probes 16-18)

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str/int or list of strs/ints
            GOES spacecraft #, e.g., probe=16

        datatype: str
            Data type; Default '1min'

        prefix: str
            The tplot variable names will be given this prefix.
            By default, no prefix is added.
            If 'probename' then the name will be used, for example g16.

        suffix: str
            The tplot variable names will be given this suffix.
            By default, no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    -------
        List of tplot variables created. Or list of filenames downloaded.

    """
    return load(
        instrument="mag",
        trange=trange,
        probe=probe,
        datatype=datatype,
        prefix=prefix,
        suffix=suffix,
        downloadonly=downloadonly,
        time_clip=time_clip,
        no_update=no_update,
    )


def mpsh(
    trange=["2023-01-30", "2023-01-31"],
    probe="16",
    datatype="1min",
    prefix="",
    suffix="",
    downloadonly=False,
    no_update=False,
    time_clip=False,
):
    """
    This function loads data from the GOES Magnetospheric Particle Sensor (MPS-HI), (probes 16-18)

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str/int or list of strs/ints
            GOES spacecraft #, e.g., probe=16

        datatype: str
            Data type; Default '1min'

        prefix: str
            The tplot variable names will be given this prefix.
            By default, no prefix is added.
            If 'probename' then the name will be used, for example g16.

        suffix: str
            The tplot variable names will be given this suffix.
            By default, no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    ----------
        List of tplot variables created. Or list of filenames downloaded.

    """
    return load(
        instrument="mpsh",
        trange=trange,
        probe=probe,
        datatype=datatype,
        prefix=prefix,
        suffix=suffix,
        downloadonly=downloadonly,
        time_clip=time_clip,
        no_update=no_update,
    )


def sgps(
    trange=["2023-01-30", "2023-01-31"],
    probe="16",
    datatype="1min",
    prefix="",
    suffix="",
    downloadonly=False,
    no_update=False,
    time_clip=False,
):
    """
    This function loads data from the GOES Solar and Galactic Proton Sensor (SGPS), (probes 16-18)

    Parameters
    ----------
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe: str/int or list of strs/ints
            GOES spacecraft #, e.g., probe=16

        datatype: str
            Data type; Default '1min'

        prefix: str
            The tplot variable names will be given this prefix.
            By default, no prefix is added.
            If 'probename' then the name will be used, for example g16.

        suffix: str
            The tplot variable names will be given this suffix.
            By default, no suffix is added.

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

    Returns
    -------
        List of tplot variables created. Or list of filenames downloaded.

    """
    return load(
        instrument="sgps",
        trange=trange,
        probe=probe,
        datatype=datatype,
        prefix=prefix,
        suffix=suffix,
        downloadonly=downloadonly,
        time_clip=time_clip,
        no_update=no_update,
    )
