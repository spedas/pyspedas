import numpy as np
from pytplot import get_data, store_data, options


def mms_fpi_make_errorflagbars(tname, level='l2'):
    """
    This procedure creates FPI error flag bars for plotting

        For DES/DIS moments:
            tname+'_flagbars_full': Detailed flag bars (all bars)
            tname+'_flagbars_main': Standard flag bars (4 bars)
            tname+'_flagbars_mini': Smallest flag bar (1 bars)

        For DES/DIS distribution functions
            tname+'_flagbars_dist': Standard flag bars (2 bars)

    Input
    -----------
        tname: str
            tplot variable containing the DIS or DES errorflag data

    Parameters
    -----------
        level: str
            Level of the data to create the errorflags bar for;
            (default is l2; this only needs to be set for QL data)

    Examples
    -----------
       > mms_fpi_make_errorflagbars('mms1_des_errorflags_fast')
       > mms_fpi_make_errorflagbars('mms1_dis_errorflags_fast')
       > mms_fpi_make_errorflagbars('mms1_des_errorflags_brst')
       > mms_fpi_make_errorflagbars('mms1_dis_errorflags_brst')

       For DES/DIS distribution function (Brst and Fast):
         bit 0 = manually flagged interval --> contact the FPI team for direction when utilizing this data; further correction is required
         bit 1 = overcounting/saturation effects likely present in skymap

       For DES/DIS moments (Brst):
         bit 0 = manually flagged interval  --> contact the FPI team for direction when utilizing this data; further correction is required
         bit 1 = overcounting/saturation effects likely present in skymap
         bit 2 = reported spacecraft potential above 20V
         bit 3 = invalid/unavailable spacecraft potential
         bit 4 = significant (>10%) cold plasma (<10eV) component
         bit 5 = significant (>25%) hot plasma (>30keV) component
         bit 6 = high sonic Mach number (v/vth > 2.5)
         bit 7 = low calculated density (n_DES < 0.05 cm^-3)
         bit 8 = onboard magnetic field used instead of brst l2pre magnetic field
         bit 9 = srvy l2pre magnetic field used instead of brst l2pre magnetic field
         bit 10 = no internally generated photoelectron correction applied
         bit 11 = compression pipeline error
         Bit 12 = spintone calculation error (DBCS only)
         Bit 13 = significant (>=20%) penetrating radiation (DIS only)
         Bit 14 = high MMS3 spintone due to DIS008 anomaly (DIS only)

       For DES/DIS moments (Fast):
         bit 0 = manually flagged interval --> contact the FPI team for direction when utilizing this data; further correction is required
         bit 1 = overcounting/saturation effects likely present in skymap
         bit 2 = reported spacecraft potential above 20V
         bit 3 = invalid/unavailable spacecraft potential
         bit 4 = significant (>10%) cold plasma (<10eV) component
         bit 5 = significant (>25%) hot plasma (>30keV) component
         bit 6 = high sonic Mach number (v/vth > 2.5)
         bit 7 = low calculated density (n_DES < 0.05 cm^-3)
         bit 8 = onboard magnetic field used instead of srvy l2pre magnetic field
         bit 9 = not used
         bit 10 = no internally generated photoelectron correction applied
         bit 11 = compression pipeline error
         Bit 12 = spintone calculation error (DBCS only)
         Bit 13 = significant (>=20%) penetrating radiation (DIS only)
         Bit 14 = high MMS3 spintone due to DIS008 anomaly (DIS only)

    Notes
    -----------
        EXPERIMENTAL!
        Based on the IDL version by Naritoshi Kitamura

    Returns
    -----------
        List containing the names of the created tplot variables
    """
    instrument = tname.split('_')[1].upper()
    data_rate = tname.split('_')[3].capitalize()

    data = get_data(tname, dt=True)
    metadata = get_data(tname, metadata=True)

    if metadata is None:
        return


    # Workaround for cdflib globalattsget() bug
    md_dt = metadata['CDF']['GATT']['Data_type']
    if isinstance(md_dt, list):
        md_dt = md_dt[0]

    if md_dt[-4:] == 'moms' or level == 'ql':
        labels_full=['Contact FPI team','Saturation','SCpot>20V','no SCpot','>10% Cold','>25% Hot','High Mach#','Low Density','Onboard Mag','L2pre Mag','Photoelectrons','Compression', 'Spintones', 'Radiation', 'MMS3 DIS Spintone']

        flags = ['{0:015b}'.format(flag) for flag in data.y]
        flagline = np.zeros((len(data.times), 15))
        flagline_others = np.zeros(len(data.times))
        flagline_all = np.zeros(len(data.times))
        for j, flag in enumerate(flags):
            for i in range(15):
                if int(flag[14-i:14-i+1]) == 0:
                    flagline[j, i] = np.nan
                    if flagline_all[j] != 1:
                        flagline_all[j] = np.nan
                    if instrument == 'DES':
                        if i != 1 and i != 4 and i != 5:
                            if flagline_others[j] != 1:
                                flagline_others[j] = np.nan
                    else:
                        if i != 1 and i != 5 and i != 13:
                            if flagline_others[j] != 1:
                                flagline_others[j] = np.nan
                else:
                    if instrument == 'DES':
                        if i != 1 and i != 4 and i != 5:
                            flagline_others[j] = 1
                    else:
                        if i != 1 and i != 5 and i != 13:
                            flagline_others[j] = 1
                        if i != 1 and i != 4 and i != 5:
                            flagline_others[j] = 1
                    flagline_all[j] = 1.0
                    flagline[j, i] = 1.0

        labels_full=['Contact FPI team','Saturation','SCpot>20V','no SCpot','>10% Cold','>25% Hot','High Mach#','Low Density','Onboard Mag','L2pre Mag','Photoelectrons','Compression', 'Spintones', 'Radiation', 'MMS3 DIS Spintone']

        if instrument == 'DES':
            des_full = np.array([[flagline[:,0]],[flagline[:,1]-0.1],[flagline[:,2]-0.2],[flagline[:,3]-0.3],[flagline[:,4]-0.4],[flagline[:,5]-0.5],[flagline[:,6]-0.6],[flagline[:,7]-0.7],[flagline[:,8]-0.8],[flagline[:,9]-0.9],[flagline[:,10]-1.0],[flagline[:,11]-1.1],[flagline[:,12]-1.2]])
            des_full = des_full.squeeze().T
            store_data(tname + '_flagbars_full', data={'x': data.times, 'y': des_full})
            options(tname + '_flagbars_full', 'yrange', [-0.15, 1.25])
            options(tname + '_flagbars_full', 'legend_names', labels_full)
            options(tname + '_flagbars_full', 'symbols', True)
            options(tname + '_flagbars_full', 'markers', 's')
            options(tname + '_flagbars_full', 'thick', 3)
            options(tname + '_flagbars_full', 'panel_size', 0.8)
            options(tname + '_flagbars_full', 'border', False)
            options(tname + '_flagbars_full', 'ytitle', instrument)
            options(tname + '_flagbars_full', 'ysubtitle', data_rate)
            options(tname + '_flagbars_full', 'color', ['k', 'red', 'green', 'teal', 'blue', 'purple', 'teal', 'black', 'blue', 'green', 'red', 'k', 'blue'])

            des_main = np.array([[flagline[:,1]-0.2],[flagline[:,4]-0.4],[flagline[:,5]-0.6],[flagline_others-0.8]])
            des_main = des_main.squeeze().T
            store_data(tname + '_flagbars_main', data={'x': data.times, 'y': des_main})
            options(tname + '_flagbars_main', 'yrange', [0.1, 0.9])
            options(tname + '_flagbars_main', 'color', ['red', 'blue', 'purple', 'black'])
            options(tname + '_flagbars_main', 'legend_names', ['Saturation','Cold (>10%)','Hot (>25%)','Others'])
            options(tname + '_flagbars_main', 'ytitle', instrument)
            options(tname + '_flagbars_main', 'ysubtitle', data_rate)
            options(tname + '_flagbars_main', 'border', False)
            options(tname + '_flagbars_main', 'symbols', True)
            options(tname + '_flagbars_main', 'markers', 's')
            options(tname + '_flagbars_main', 'thick', 3)

            des_others = np.array([[flagline[:,11]-0.8],[flagline[:,12]-0.8],[flagline[:,7]-0.8],[flagline[:,6]-0.8],[flagline[:,8]-0.8],[flagline[:,9]-0.8],[flagline[:,2]-0.8],[flagline[:,3]-0.8],[flagline[:,10]-0.8],[flagline[:,0]-0.8]])
            des_others = des_others.squeeze().T
            store_data(tname + '_flagbars_others', data={'x': data.times, 'y': des_others})
            options(tname + '_flagbars_others', 'ytitle', instrument)
            options(tname + '_flagbars_others', 'ysubtitle', data_rate)
            options(tname + '_flagbars_others', 'border', False)
            options(tname + '_flagbars_others', 'thick', 4)

            store_data(tname + '_flagbars_mini', data={'x': data.times, 'y': flagline_all})
            options(tname + '_flagbars_mini', 'ytitle', instrument)
            options(tname + '_flagbars_mini', 'ysubtitle', data_rate)
            options(tname + '_flagbars_mini', 'yrange', [0.9, 1.1])
            options(tname + '_flagbars_mini', 'color', 'black')
            options(tname + '_flagbars_mini', 'panel_size', 0.1)
            options(tname + '_flagbars_mini', 'border', False)
            options(tname + '_flagbars_mini', 'thick', 4)
            options(tname + '_flagbars_mini', 'legend_names', 'Flagged')
            options(tname + '_flagbars_mini', 'symbols', True)
            options(tname + '_flagbars_mini', 'markers', 's')
        else:
            dis_full = np.array([[flagline[:,0]],[flagline[:,1]-0.1],[flagline[:,2]-0.2],[flagline[:,3]-0.3],[flagline[:,4]-0.4],[flagline[:,5]-0.5],[flagline[:,6]-0.6],[flagline[:,7]-0.7],[flagline[:,8]-0.8],[flagline[:,9]-0.9],[flagline[:,10]-1.0],[flagline[:,11]-1.1],[flagline[:,12]-1.2],[flagline[:,13]-1.3],[flagline[:,14]-1.4]])
            dis_full = dis_full.squeeze().T
            store_data(tname + '_flagbars_full', data={'x': data.times, 'y': dis_full})
            options(tname + '_flagbars_full', 'yrange', [-1.5, 1.35])
            options(tname + '_flagbars_full', 'legend_names', labels_full)
            options(tname + '_flagbars_full', 'symbols', True)
            options(tname + '_flagbars_full', 'markers', 's')
            options(tname + '_flagbars_full', 'thick', 3)
            options(tname + '_flagbars_full', 'panel_size', 0.8)
            options(tname + '_flagbars_full', 'border', False)
            options(tname + '_flagbars_full', 'ytitle', instrument)
            options(tname + '_flagbars_full', 'ysubtitle', data_rate)
            options(tname + '_flagbars_full', 'color', ['k', 'red', 'green', 'teal', 'blue', 'purple', 'teal', 'black', 'blue', 'green', 'red', 'k', 'blue', 'orange', 'red'])

            dis_main = np.array([[flagline[:,1]-0.2],[flagline[:,13]-0.4],[flagline[:,5]-0.6],[flagline_others-0.8]])
            dis_main = dis_main.squeeze().T
            store_data(tname + '_flagbars_main', data={'x': data.times, 'y': dis_main})
            options(tname + '_flagbars_main', 'yrange', [0.1, 0.9])
            options(tname + '_flagbars_main', 'color', ['red', 'orange', 'purple', 'black'])
            options(tname + '_flagbars_main', 'legend_names', ['Saturation','Radiation','Hot (>25%)','Others'])
            options(tname + '_flagbars_main', 'ytitle', instrument)
            options(tname + '_flagbars_main', 'ysubtitle', data_rate)
            options(tname + '_flagbars_main', 'border', False)
            options(tname + '_flagbars_main', 'symbols', True)
            options(tname + '_flagbars_main', 'markers', 's')
            options(tname + '_flagbars_main', 'thick', 3)

            dis_others = np.array([[flagline[:,11]-0.8],[flagline[:,12]-0.8],[flagline[:,7]-0.8],[flagline[:,6]-0.8],[flagline[:,8]-0.8],[flagline[:,9]-0.8],[flagline[:,2]-0.8],[flagline[:,3]-0.8],[flagline[:,10]-0.8],[flagline[:,0]-0.8]])
            dis_others = dis_others.squeeze().T
            store_data(tname + '_flagbars_others', data={'x': data.times, 'y': dis_others})
            options(tname + '_flagbars_others', 'ytitle', instrument)
            options(tname + '_flagbars_others', 'ysubtitle', data_rate)
            options(tname + '_flagbars_others', 'border', False)
            options(tname + '_flagbars_others', 'thick', 4)

            store_data(tname + '_flagbars_mini', data={'x': data.times, 'y': flagline_all})
            options(tname + '_flagbars_mini', 'ytitle', instrument)
            options(tname + '_flagbars_mini', 'ysubtitle', data_rate)
            options(tname + '_flagbars_mini', 'yrange', [0.9, 1.1])
            options(tname + '_flagbars_mini', 'color', 'black')
            options(tname + '_flagbars_mini', 'panel_size', 0.1)
            options(tname + '_flagbars_mini', 'border', False)
            options(tname + '_flagbars_mini', 'thick', 4)
            options(tname + '_flagbars_mini', 'legend_names', 'Flagged')
            options(tname + '_flagbars_mini', 'symbols', True)
            options(tname + '_flagbars_mini', 'markers', 's')

        out_vars = [tname + '_flagbars_full',
                    tname + '_flagbars_main',
                    tname + '_flagbars_others',
                    tname + '_flagbars_mini']
    elif md_dt[-4:] == 'dist':
        flags = ['{0:014b}'.format(flag) for flag in data.y]
        flagline = np.zeros((len(data.times), 2))
        for i in [0, 1]:
            for j in range(len(flags)):
                try:
                    flagset = int(flags[13-i:13-i+1][0])
                except IndexError:
                    continue
                if flagset == 0:
                    flagline[j, i] = np.nan
                else:
                    flagline[j, i] = 1

        dist_full = np.array([[flagline[:,0]-0.25],[flagline[:,1]-0.75]])
        dist_full = dist_full.squeeze().T
        store_data(tname + '_flagbars_dist', data={'x': data.times, 'y': dist_full})
        options(tname + '_flagbars_dist', 'yrange', [0, 1])
        options(tname + '_flagbars_dist', 'color', ['black', 'red'])
        options(tname + '_flagbars_dist', 'legend_names', ['Manually flagged', 'Saturation'])
        options(tname + '_flagbars_dist', 'panel_size', 0.25)
        options(tname + '_flagbars_dist', 'border', False)
        options(tname + '_flagbars_dist', 'thick', 4)
        options(tname + '_flagbars_dist', 'symbols', True)
        options(tname + '_flagbars_dist', 'markers', 's')
        out_vars = [tname + '_flagbars_dist']

    return out_vars
