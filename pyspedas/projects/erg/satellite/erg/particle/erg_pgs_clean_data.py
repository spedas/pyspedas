import numpy as np

from .erg_convert_flux_units import erg_convert_flux_units


def erg_pgs_clean_data(data_in,
                       units='flux',
                       relativistic=False,
                       for_moments=False,
                       magf=np.array([0., 0., 0.]),
                       muconv=False
                       ):

    converted_data = erg_convert_flux_units(input_dist=data_in,
                                            units=units,
                                            relativistic=relativistic)

    dims = np.array(converted_data['data'].shape)
    angdims = converted_data['data'][0, :].size

    output = {
        'dims': dims,
        'time': converted_data['time'],
        'end_time': converted_data['end_time'],
        'charge': converted_data['charge'],
        'mass': converted_data['mass'],
        'species': converted_data['species'],
        'magf': magf,
        'sc_pot': 0.,
        'scaling': np.ones(shape=(dims[0], angdims)),
        'units_name': data_in['units_name'],
        'psd': data_in['data'].reshape(dims[0], angdims),
        'data': converted_data['data'].reshape(dims[0], angdims),
        'bins': converted_data['bins'].reshape(dims[0], angdims),
        'energy': converted_data['energy'].reshape(dims[0], angdims),
        'denergy': converted_data['denergy'].reshape(dims[0], angdims),
        'phi': converted_data['phi'].reshape(dims[0], angdims),
        'dphi': converted_data['dphi'].reshape(dims[0], angdims),
        'theta': converted_data['theta'].reshape(dims[0], angdims),
        'dtheta': converted_data['dtheta'].reshape(dims[0], angdims),
    }

    # Exclude f_nan values from further calculations
    bins = output['bins'].astype(np.int8)
    output['bins'] = np.where((bins == 0)
                              | (np.isinf(output['data']) == True)
                              | (np.isnan(output['data']) == True)
                              | (np.isinf(output['energy']) == True)
                              | (np.isnan(output['energy']) == True),
                              0, 1)

    # Fill invalid values with zero for moment calculations
    if for_moments:
        output['data'] = np.where(output['bins'] == 0, 0., output['data'])
        output['psd'] = np.where(output['bins'] == 0, 0., output['psd'])
        output['energy'] = np.where(output['bins'] == 0, 1., output['energy'])
        output['denergy'] = np.where(output['bins'] == 0,
                                    1., output['denergy'])

    if 'orig_energy' in converted_data.keys():
        output['orig_energy'] = converted_data['orig_energy']

    return output
