import cdflib
import numpy as np
from pytplot import clip, options, store_data, ylim, zlim, get_data

from ..load import load


def xep(trange=['2017-06-01', '2017-06-02'],
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
    This function loads data from the XEP-e experiment from the Arase mission

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

    if (datatype == 'omniflux') or (datatype == '2dflux'):
        # to avoid failure of creation Tplot variables (at store_data.py) of xep
        notplot = True
    file_res = 3600. * 24
    prefix = 'erg_xep_'+level+'_'
    pathformat = 'satellite/erg/xep/'+level+'/'+datatype + \
        '/%Y/%m/erg_xep_'+level+'_'+datatype+'_%Y%m%d_v??_??.cdf'
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
            print('Information about ERG XEP')
            print('')
            print('PI: ', gatt['PI_NAME'])
            print("Affiliation: "+gatt["PI_AFFILIATION"])
            print('')
            print('RoR of ERG project common: https://ergsc.isee.nagoya-u.ac.jp/data_info/rules_of_the_road.shtml.en')
            print('RoR of XEP: https://ergsc.isee.nagoya-u.ac.jp/mw/index.php/ErgSat/Xep')
            print('')
            print('Contact: erg_xep_info at isee.nagoya-u.ac.jp')
            print(
                '**************************************************************************')
        except:
            print('printing PI info and rules of the road was failed')

    if initial_notplot_flag or downloadonly:
        return loaded_data

    if isinstance(loaded_data, dict):

        if datatype == 'omniflux':
            tplot_variables = []

            if prefix + 'FEDO_SSD' + suffix in loaded_data:
                v_vars_min = loaded_data[prefix + 'FEDO_SSD' + suffix]['v'][0]
                v_vars_max = loaded_data[prefix + 'FEDO_SSD' + suffix]['v'][1]
                v_vars = np.sqrt(v_vars_min * v_vars_max)  # Geometric mean

                store_data(prefix + 'FEDO_SSD' + suffix, data={'x': loaded_data[prefix + 'FEDO_SSD' + suffix]['x'],
                                                               'y': loaded_data[prefix + 'FEDO_SSD' + suffix]['y'],
                                                               'v': v_vars},
                           attr_dict={'CDF':loaded_data[prefix + 'FEDO_SSD' + suffix]['CDF']})
                tplot_variables.append(prefix + 'FEDO_SSD' + suffix)

                if prefix + 'FEDO_SSD' + suffix in tplot_variables:
                    # remove minus valuse of y array
                    clip(prefix + 'FEDO_SSD' + suffix, 0., 5000.)
                # set spectrogram plot option
                options(prefix + 'FEDO_SSD' + suffix, 'Spec', 1)
                # set y axis to logscale
                options(prefix + 'FEDO_SSD' + suffix, 'ylog', 1)
                # set yrange
                options(prefix + 'FEDO_SSD' + suffix,
                        'yrange', [4.0e+02, 4.5e+03])
                # set z axis to logscale
                options(prefix + 'FEDO_SSD' + suffix, 'zlog', 1)
                # set zrange
                options(prefix + 'FEDO_SSD' + suffix,
                        'zrange', [1.0e-01, 1.0e+3])
                # change colormap option
                options(prefix + 'FEDO_SSD' + suffix, 'Colormap', 'jet')

                # set ztitle
                options(prefix + 'FEDO_SSD' + suffix,
                        'ztitle', '[/cm^{2}-str-s-keV]')
                # set ytitle
                options(prefix + 'FEDO_SSD' + suffix,
                        'ytitle', 'XEP\nomniflux\nLv2\nEnergy')
                # set ysubtitle
                options(prefix + 'FEDO_SSD' + suffix, 'ysubtitle', '[keV]')

                ylim(prefix + 'FEDO_SSD' + suffix, 4.0e+02, 4.5e+03)
                zlim(prefix + 'FEDO_SSD' + suffix, 1.0e-01, 1.0e+3)

            return tplot_variables

        if datatype == '2dflux':
            tplot_variables = []

            if prefix + 'FEDU_SSD' + suffix in loaded_data:
                store_data(prefix + 'FEDU_SSD' + suffix,
                           data={'x': loaded_data[prefix + 'FEDU_SSD' + suffix]['x'],
                                 'y': loaded_data[prefix + 'FEDU_SSD' + suffix]['y'],
                                 'v1': np.sqrt(loaded_data[prefix + 'FEDU_SSD' + suffix]['v'][:, 0]
                                               * loaded_data[prefix + 'FEDU_SSD' + suffix]['v'][:, 1]),  # Geometric mean of 'v'
                                 'v2': [i for i in range(16)]},  # [0, 1, 2, .., 15]
                           attr_dict={'CDF':loaded_data[prefix + 'FEDU_SSD' + suffix]['CDF']})

                tplot_variables.append(prefix + 'FEDU_SSD' + suffix)

                if prefix + 'FEDU_SSD' + suffix in tplot_variables:
                    clip(prefix + 'FEDU_SSD' + suffix, -1.0e+10, 1.0e+10)

                return tplot_variables

    return loaded_data
