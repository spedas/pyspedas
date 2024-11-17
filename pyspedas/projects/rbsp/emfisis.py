from .load import load


def emfisis(trange=['2018-11-5', '2018-11-6'],
            probe='a',
            datatype='magnetometer',
            level='l3',
            cadence='4sec',  # for EMFISIS mag data
            coord='sm',  # for EMFISIS mag
            wavetype='waveform',  # for EMFISIS waveform data
            prefix='',
            suffix='',
            force_download=False,
            get_support_data=False,
            varformat=None,
            varnames=[],
            downloadonly=False,
            notplot=False,
            no_update=False,
            time_clip=False):
    """
    This function loads data from the Electric and Magnetic Field Instrument Suite and Integrated Science (EMFISIS) instrument

    For information on the EMFISIS data products, see:
        https://emfisis.physics.uiowa.edu/data/level_descriptions
        https://emfisis.physics.uiowa.edu/data/L2_products


    Parameters
    ----------
        trange : list of str, default=['2018-11-5', '2018-11-6']
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        probe : str or list of str, default='a'
            Spacecraft probe name: 'a' or 'b'

        datatype : str, default='magnetometer'
            Data type with options varying by data level.
            Level 1:

                'magnetometer'
                'hfr'
                'housekeeping'
                'sc-hk'
                'spaceweather'
                'wfr'
                'wna'

            Level 2:

                'magnetometer'
                'wfr'
                'hfr'
                'housekeeping'

            Level 3:

                'magnetometer'

            Level 4:

                'density'
                'wna-survey'

        level : str, default='l3'
            Data level; options: 'l1', 'l2', 'l3', l4'

        cadence : str, default='4sec'
            Data cadence; options: '1sec', 'hires', '4sec'

        coord : str, default='sm'
            Data coordinate system

        wavetype : str, default='waveform'
            Type of level 2 waveform data with options:

                For WFR data:

                    'waveform' (default)
                    'waveform-continuous-burst'
                    'spectral-matrix'
                    'spectral-matrix-diagonal'
                    'spectral-matrix-diagonal-merged'

                For HFR data:

                    'waveform'
                    'spectra'
                    'spectra-burst'
                    'spectra-merged'

        prefix : str, optional
            The tplot variable names will be given this prefix. By default, no prefix is added.

        suffix : str, optional
            Suffix for tplot variable names. By default, no suffix is added.

        force_download : bool, default=False
            Download file even if local version is more recent than server version.

        get_support_data : bool, default=False
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot. By default, only loads in data with a
            "VAR_TYPE" attribute of "data".

        varformat : str, optional
            The file variable formats to load into tplot. Wildcard character
            "*" is accepted. By default, all variables are loaded in.

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
    tvars : dict or list
        List of created tplot variables or dict of data tables if notplot is True.

    Examples
    --------
    >>> emfisis_vars = pyspedas.projects.rbsp.emfisis(trange=['2018-11-5/10:00', '2018-11-5/15:00'], datatype='magnetometer', level='l3', time_clip=True)
    >>> tplot(['Mag', 'Magnitude'])
    """
    return load(instrument='emfisis', wavetype=wavetype, trange=trange, probe=probe, datatype=datatype, level=level, cadence=cadence, coord=coord, prefix=prefix, suffix=suffix, force_download=force_download, get_support_data=get_support_data, varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update)

