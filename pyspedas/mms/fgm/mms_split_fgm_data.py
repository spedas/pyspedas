import logging

from pytplot import data_exists
from pytplot import get_data, store_data, options

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def mms_split_fgm_data(probe, data_rate, level, instrument, suffix=''):
    """
    Helper routine for splitting 4-vector FGM data (Bx, By, Bz, b_total)
    into 2 tplot variables, one for the vector (Bx, By, Bz), and one for the total
    """

    probe = probe.lower()
    instrument = instrument.lower()
    data_rate = data_rate.lower()
    level = level.lower()

    if level.lower() == 'l2pre':
        data_rate_mod = data_rate + '_l2pre'
    else:
        data_rate_mod = data_rate

    coords = ['dmpa', 'gse', 'gsm', 'bcs']

    out_vars = []

    for coord in coords:
        if level in ['l2', 'l2pre']:
            tplot_name = 'mms' + probe + '_' + instrument + '_b_' + coord + '_' + data_rate + '_' + level + suffix
        else:
            tplot_name = 'mms' + probe + '_' + instrument + '_' + data_rate_mod + '_' + coord + suffix

        if not data_exists(tplot_name):
            continue

        fgm_data = get_data(tplot_name, dt=True)

        if fgm_data is None:
            continue

        metadata = get_data(tplot_name, metadata=True)

        if suffix != '':
            tplot_name = tplot_name[0:-len(suffix)]

        store_data(tplot_name + '_bvec' + suffix, data={'x': fgm_data.times, 'y': fgm_data.y[:, :3]}, attr_dict=metadata)
        store_data(tplot_name + '_btot' + suffix, data={'x': fgm_data.times, 'y': fgm_data.y[:, 3]}, attr_dict=metadata)

        options(tplot_name + '_btot' + suffix, 'legend_names', 'Bmag')
        options(tplot_name + '_btot' + suffix, 'ytitle', 'MMS'+probe + ' FGM')

        out_vars.append(tplot_name + '_bvec' + suffix)
        out_vars.append(tplot_name + '_btot' + suffix)

    return out_vars
