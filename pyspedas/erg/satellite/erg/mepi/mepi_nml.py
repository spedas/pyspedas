import cdflib
from pytplot import options, ylim, get_data

from ..load import load


def mepi_nml(trange=['2017-03-27', '2017-03-28'],
             datatype='omniflux',
             level='l2',
             suffix='',
             get_support_data=False,
             varformat=None,
             varnames=[],
             downloadonly=False,
             notplot=False,
             no_update=False,
             uname=None,
             passwd=None,
             time_clip=False,
             ror=True):
    """
    This function loads data from the MEP-i experiment from the Arase mission

    Parameters:
        trange : list of str
            time range of interest [starttime, endtime] with the format
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']

        datatype: str
            Data type; Valid options:

        level: str
            Data level; Valid options:

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
            List of variable names to load (if not specified,
            all data variables are loaded)

        downloadonly: bool
            Set this flag to download the CDF files, but not load them into
            tplot variables

        notplot: bool
            Return the data in hash tables instead of creating tplot variables

        no_update: bool
            If set, only load data from your local cache

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword

        ror: bool
            If set, print PI info and rules of the road

    Returns:
        List of tplot variables created.

    """
    initial_notplot_flag = False
    if notplot:
        initial_notplot_flag = True

    file_res = 3600. * 24
    prefix = 'erg_mepi_'+level+'_'+datatype+'_'

    pathformat = 'satellite/erg/mepi/'+level+'/'+datatype + \
        '/%Y/%m/erg_mepi_'+level+'_'+datatype+'_%Y%m%d_v??_??.cdf'

    loaded_data = load(pathformat=pathformat, trange=trange, level=level, datatype=datatype, file_res=file_res, prefix=prefix, suffix=suffix, get_support_data=get_support_data,
                       varformat=varformat, varnames=varnames, downloadonly=downloadonly, notplot=notplot, time_clip=time_clip, no_update=no_update, uname=uname, passwd=passwd)

    if (len(loaded_data) > 0) and ror:
        try:
            if isinstance(loaded_data, list):
                if downloadonly:
                    cdf_file = cdflib.CDF(loaded_data[-1])
                    gatt = cdf_file.globalattsget()
                else:
                    gatt = get_data(loaded_data[-1], metadata=True)['CDF']['GATT']
            elif isinstance(loaded_data, dict):
                gatt = loaded_data[list(loaded_data.keys())[-1]]['CDF']['GATT']


            # --- print PI info and rules of the road

            print(' ')
            print(
                '**************************************************************************')
            print(gatt["LOGICAL_SOURCE_DESCRIPTION"])
            print('')
            print('PI: ', gatt['PI_NAME'])
            print("Affiliation: "+gatt["PI_AFFILIATION"])
            print('')
            print('- The rules of the road (RoR) common to the ERG project:')
            print(
                '      https://ergsc.isee.nagoya-u.ac.jp/data_info/rules_of_the_road.shtml.en')
            print(
                '- RoR for MEP-i data: https://ergsc.isee.nagoya-u.ac.jp/mw/index.php/ErgSat/Mepi')
            print('')
            print('Contact: erg_mep_info at isee.nagoya-u.ac.jp')
            print(
                '**************************************************************************')
        except:
            print('printing PI info and rules of the road was failed')

    if initial_notplot_flag or downloadonly:
        return loaded_data

    if (datatype == 'omniflux') and (level == 'l2'):
        original_suffix_list = ['FPDO', 'FHE2DO', 'FHEDO', 'FOPPDO', 'FODO', 'FO2PDO',
                                'FPDO_tof', 'FHE2DO_tof', 'FHEDO_tof', 'FOPPDO_tof', 'FODO_tof', 'FO2PDO_tof']
        tplot_names_list = []
        for i in range(len(original_suffix_list)):
            tplot_names_list.append(prefix + original_suffix_list[i] + suffix)
            # set ylim
            ylim(tplot_names_list[i], 4, 190)
            # set ytitle
            if 'tof' in tplot_names_list[i]:
                options(
                    tplot_names_list[i], 'ytitle', f'ERG\nMEP-i/TOF\n{original_suffix_list[i]}\nEnergy')
            else:
                options(
                    tplot_names_list[i], 'ytitle', f'ERG\nMEP-i/NML\n{original_suffix_list[i]}\nEnergy')

        # set spectrogram plot option
        options(tplot_names_list, 'Spec', 1)

        # set y axis to logscale
        options(tplot_names_list, 'ylog', 1)

        # set ysubtitle
        options(tplot_names_list, 'ysubtitle', '[keV/q]')

        # set z axis to logscale
        options(tplot_names_list, 'zlog', 1)

        # set ztitle
        options(tplot_names_list, 'ztitle', '[/s-cm^{2}-sr-keV/q]')

        # change colormap option
        options(tplot_names_list, 'Colormap', 'jet')

    elif (datatype == '3dflux') and (level == 'l2'):
        original_suffix_list = ['FPDU', 'FHE2DU', 'FHEDU', 'FOPPDU', 'FODU', 'FO2PDU',
                                'count_raw_P', 'count_raw_HE2', 'count_raw_HE', 'count_raw_OPP', 'count_raw_O', 'count_raw_O2P']
        tplot_names_list = []
        for i in range(len(original_suffix_list)):
            tplot_names_list.append(prefix + original_suffix_list[i] + suffix)
            ylim(tplot_names_list[i], 4, 190)

        # set spectrogram plot option
        options(tplot_names_list, 'Spec', 1)

        # set y axis to logscale
        options(tplot_names_list, 'ylog', 1)

        # set ysubtitle
        options(tplot_names_list, 'ysubtitle', '[keV/q]')

        # set ztitle
        options(tplot_names_list[:6], 'ztitle', '[/s-cm^{2}-sr-keV/q]')
        options(tplot_names_list[6:], 'ztitle', '[cnt/smpl]')

        # set z axis to logscale
        options(tplot_names_list, 'zlog', 1)

    return loaded_data
