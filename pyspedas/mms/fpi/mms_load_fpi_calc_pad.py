from pyspedas import tnames
from pytplot import get_data, store_data, options

def mms_load_fpi_calc_pad(probe='1', level='sitl', datatype='', data_rate='', suffix='', autoscale=True):
    """
    Calculates the omni-directional pitch angle distribution (summed and averaged)
    from the individual tplot variables
    
    Parameters
    ----------
        probe: str 
            probe, valid values for MMS probes are ['1','2','3','4']. 

        level: str
            indicates level of data processing. the default if no level is specified is 'sitl'

        datatype: str
            Valid datatypes for FPI are:
              Quicklook: ['des', 'dis'] 
              SITL: '' (none; loads both electron and ion data from single CDF)
              L1b/L2: ['des-dist', 'dis-dist', 'dis-moms', 'des-moms']

        data_rate: str
            instrument data rates for FPI include 'brst' and 'fast'. The
            default is 'fast'.

        suffix: str
            The tplot variable names will be given this suffix.  By default, 
            no suffix is added.

        autoscale: bool
            If set, use the default zrange; otherwise, use the min and max of the data for the zrange

    Returns:
        List of tplot variables created.

    """
    out_vars = []

    if isinstance(datatype, str):
        if datatype == '*' or datatype == '':
            if level.lower() == 'ql':
                datatype = ['des', 'dis']
            else:
                datatype = ['des-dist', 'dis-dist']

    if isinstance(datatype, str):
        datatype = [datatype]

    for dtype in datatype:
        species = dtype[1]

        if level.lower() == 'sitl':
            spec_str_format = 'PitchAngDist'
            obs_str_format = '_fpi_' + species
        else:
            spec_str_format = 'pitchAngDist'
            obs_str_format = '_d' + species + 's_'

        obsstr = 'mms' + str(probe) + obs_str_format

        if level.lower() == 'l2':
            spec_str_format = 'pitchangdist'
            pad_vars = [obsstr+spec_str_format+'_'+erange+'en_'+data_rate+suffix for erange in ['low', 'mid', 'high']]
        else:
            pad_vars = [obsstr+spec_str_format+'_'+erange+'En'+suffix for erange in ['low', 'mid', 'high']]

        pad_avg_name = obsstr+'PitchAngDist_avg'+suffix

        low_en = get_data(pad_vars[0], dt=True)
        mid_en = get_data(pad_vars[1], dt=True)
        high_en = get_data(pad_vars[2], dt=True)

        if low_en is None or mid_en is None or high_en is None:
            v3_low_pad = tnames(pad_vars[0].lower()+'_'+data_rate)
            v3_mid_pad = tnames(pad_vars[1].lower()+'_'+data_rate)
            v3_high_pad = tnames(pad_vars[2].lower()+'_'+data_rate)
            if v3_low_pad == [] or v3_mid_pad == [] or v3_high_pad == []:
                continue

            low_en = get_data(v3_low_pad[0], dt=True)
            mid_en = get_data(v3_mid_pad[0], dt=True)
            high_en = get_data(v3_high_pad[0], dt=True)
            pad_avg_name = pad_avg_name.lower()

        e_pad_sum = low_en.y+mid_en.y+high_en.y
        e_pad_avg = e_pad_sum/3.0

        if level == 'l2':
            pad_avg_name = pad_avg_name.lower()

        if species == 'e':
            species_str = 'electron'
        elif species == 'i':
            species_str = 'ion'

        if level == 'ql':
            store_data(obsstr+'PitchAngDist_sum'+suffix, data={'x': low_en.times, 'y': e_pad_sum, 'v': low_en.v})
            options(obsstr+'PitchAngDist_sum'+suffix, 'ytitle', 'MMS'+str(probe)+' \\ '+species_str+' \\ PAD \\ SUM')
            options(obsstr+'PitchAngDist_sum'+suffix, 'yrange', [0, 180])
            options(obsstr+'PitchAngDist_sum'+suffix, 'zlog', True)
            options(obsstr+'PitchAngDist_sum'+suffix, 'spec', True)
            options(obsstr+'PitchAngDist_sum'+suffix, 'Colormap', 'spedas')
            out_vars.append(obsstr+'PitchAngDist_sum'+suffix)

        store_data(pad_avg_name, data={'x': low_en.times, 'y': e_pad_avg, 'v': low_en.v})
        options(pad_avg_name, 'ztitle', 'eV/(cm!U2!N s sr eV)')
        options(pad_avg_name, 'ytitle', 'MMS'+str(probe)+' \\ '+species_str+' \\ PAD \\ AVG')
        options(pad_avg_name, 'yrange', [0, 180])
        options(pad_avg_name, 'zlog', True)
        options(pad_avg_name, 'spec', True)
        out_vars.append(pad_avg_name)

        return out_vars