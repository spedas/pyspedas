
import cdflib
from pytplot import options, ylim, get_data

from ..load import load


def mepe(trange=['2017-03-27', '2017-03-28'],
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
    This function loads data from the MEP-e experiment from the Arase mission

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

    if level == 'l3':
        datatype = '3dflux'

    file_res = 3600. * 24
    prefix = 'erg_mepe_'+level + '_' + datatype + '_'
    pathformat = 'satellite/erg/mepe/'+level+'/'+datatype + \
        '/%Y/%m/erg_mepe_'+level+'_'+datatype+'_%Y%m%d_v??_??.cdf'

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
                '- RoR for MEP-e data:  https://ergsc.isee.nagoya-u.ac.jp/mw/index.php/ErgSat/Mepe')
            print('')
            print('Contact: erg_mep_info at isee.nagoya-u.ac.jp')
            print(
                '**************************************************************************')
        except:
            print('printing PI info and rules of the road was failed')

    if initial_notplot_flag or downloadonly:
        return loaded_data

    if datatype == 'omniflux':
        # set spectrogram plot option
        options(prefix + 'FEDO' + suffix, 'Spec', 1)
        # set y axis to logscale
        options(prefix + 'FEDO' + suffix, 'ylog', 1)
        # set ytitle
        options(prefix + 'FEDO' + suffix, 'ytitle', 'ERG\nMEP-e\nFEDO\nEnergy')
        # set ysubtitle
        options(prefix + 'FEDO' + suffix, 'ysubtitle', '[keV]')
        # set ylim
        ylim(prefix + 'FEDO' + suffix, 6., 100.)
        # set z axis to logscale
        options(prefix + 'FEDO' + suffix, 'zlog', 1)
        # set ztitle
        options(prefix + 'FEDO' + suffix, 'ztitle', '[/s-cm^{2}-sr-keV]')
        # change colormap option
        options(prefix + 'FEDO' + suffix, 'Colormap', 'jet')
    elif (datatype == '3dflux') and (level == 'l2'):
        # set spectrogram plot option
        options(prefix + 'FEDU' + suffix, 'Spec', 1)
        options(prefix + 'FEDU_n' + suffix, 'Spec', 1)
        options(prefix + 'FEEDU' + suffix, 'Spec', 1)
        options(prefix + 'count_raw' + suffix, 'Spec', 1)

        # set y axis to logscale
        options(prefix + 'FEDU' + suffix, 'ylog', 1)
        options(prefix + 'FEDU_n' + suffix, 'ylog', 1)
        options(prefix + 'FEEDU' + suffix, 'ylog', 1)
        options(prefix + 'count_raw' + suffix, 'ylog', 1)

        # set ysubtitle
        options(prefix + 'FEDU' + suffix, 'ysubtitle', '[keV]')
        options(prefix + 'FEDU_n' + suffix, 'ysubtitle', '[keV]')
        options(prefix + 'count_raw' + suffix, 'ysubtitle', '[keV]')

        # set ylim
        ylim(prefix + 'FEDU' + suffix, 6., 100.)
        ylim(prefix + 'FEDU_n' + suffix, 6., 100.)
        ylim(prefix + 'count_raw' + suffix, 6., 100.)

        # set z axis to logscale
        options(prefix + 'FEDU' + suffix, 'zlog', 1)
        options(prefix + 'FEDU_n' + suffix, 'zlog', 1)
        options(prefix + 'FEEDU' + suffix, 'zlog', 1)
        options(prefix + 'count_raw' + suffix, 'zlog', 1)

        # set ztitle
        options(prefix + 'FEDU' + suffix, 'ztitle', '[/s-cm^{2}-sr-keV]')
        options(prefix + 'FEDU_n' + suffix, 'ztitle', '[/s-cm^{2}-sr-keV]')

        # change colormap option
        options(prefix + 'FEDU' + suffix, 'Colormap', 'jet')
        options(prefix + 'FEDU_n' + suffix, 'Colormap', 'jet')
        options(prefix + 'FEEDU' + suffix, 'Colormap', 'jet')
        options(prefix + 'count_raw' + suffix, 'Colormap', 'jet')

    return loaded_data
