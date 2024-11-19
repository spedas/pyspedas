import logging
import numpy as np
from scipy.ndimage import shift
from pyspedas.projects.mms.particles.mms_convert_flux_units import mms_convert_flux_units


def moka_mms_clean_data(data_in, units=None, disterr=None):
    """
    This is a translation of Mitsuo Oka's IDL routine: moka_mms_clean_data
    """
    if units is None:
        logging.error('Units must be specified.')
        return

    data = mms_convert_flux_units(data_in, units=units)
    data_psd = mms_convert_flux_units(data_in, units='df_km')

    output = {'charge': data_in['charge'], 'mass': data_in['mass'],
              'data': np.reshape(data_in['data'], [data_in['data'].shape[0]*data_in['data'].shape[1]*data_in['data'].shape[2]], order='F'),
              'bins': np.reshape(data_in['bins'], [data_in['data'].shape[0]*data_in['data'].shape[1]*data_in['data'].shape[2]], order='F'),
              'theta': np.reshape(data_in['theta'], [data_in['data'].shape[0]*data_in['data'].shape[1]*data_in['data'].shape[2]], order='F'),
              'energy': np.reshape(data_in['energy'], [data_in['data'].shape[0], data_in['data'].shape[1]*data_in['data'].shape[2]], order='F'),
              'phi': np.reshape(data_in['phi'], [data_in['data'].shape[0]*data_in['data'].shape[1]*data_in['data'].shape[2]], order='F'),
              'dtheta': np.reshape(data_in['dtheta'], [data_in['data'].shape[0]*data_in['data'].shape[1]*data_in['data'].shape[2]], order='F'),
              'dphi': np.reshape(data_in['dphi'], [data_in['data'].shape[0]*data_in['data'].shape[1]*data_in['data'].shape[2]], order='F'),
              'denergy': np.reshape(data_in['denergy'], [data_in['data'].shape[0]*data_in['data'].shape[1]*data_in['data'].shape[2]], order='F')}

    de = output['energy'] - shift(output['energy'], [1, 0])
    output['denergy'] = shift((de+shift(de, [1, 0]))/2.0, -1)
    # just have to make a guess at the edges(bottom edge)
    output['denergy'][0, :] = de[1, :]
    # just have to make a guess at the edges(top edge)
    output['denergy'][-1, :] = de[-1, :]

    dims = data['data'].shape
    imax = dims[0]*dims[1]*dims[2]

    output['energy'] = np.reshape(output['energy'], [output['energy'].shape[0] * output['energy'].shape[1]],
                                  order='F')
    output['denergy'] = np.reshape(output['denergy'], [output['denergy'].shape[0] * output['denergy'].shape[1]],
                                  order='F')

    # Error
    psd = output['data']
    if disterr is None:
        err = np.zeros(imax)
        cnt = np.zeros(imax)
    else:
        data_err = mms_convert_flux_units(disterr, units='df_km')
        err = data_err['data']
        cnt = (psd/err)**2  # actual counts recovered

    # NaN
    dat = output['data']
    bins = output['bins']
    idx = np.argwhere(bins == False)
    if len(idx) > 0:
        dat[idx] = 0.0
        psd[idx] = 0.0
        err[idx] = 0.0
        cnt[idx] = 0.0

    dat = np.nan_to_num(dat, nan=0.0)
    psd = np.nan_to_num(psd, nan=0.0)
    err = np.nan_to_num(err, nan=0.0)
    cnt = np.nan_to_num(cnt, nan=0.0)

    output['data_dat'] = dat
    output['data_psd'] = psd
    output['data_err'] = err
    output['data_cnt'] = cnt
    output['pa'] = np.zeros(imax)

    return output
