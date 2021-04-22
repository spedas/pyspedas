import logging
import numpy as np

from pytplot import get_data, store_data, options

from pyspedas.particles.spd_part_products.spd_pgs_make_theta_spec import spd_pgs_make_theta_spec
from pyspedas.particles.spd_part_products.spd_pgs_make_phi_spec import spd_pgs_make_phi_spec
from pyspedas.particles.spd_part_products.spd_pgs_make_e_spec import spd_pgs_make_e_spec
from pyspedas.particles.spd_part_products.spd_pgs_make_tplot import spd_pgs_make_tplot

from pyspedas.mms.fpi.mms_get_fpi_dist import mms_get_fpi_dist
from pyspedas.mms.particles.mms_convert_flux_units import mms_convert_flux_units
from pyspedas.mms.particles.mms_pgs_clean_data import mms_pgs_clean_data

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

def mms_part_products(in_tvarname, units='eflux', species='e', data_rate='fast', instrument='fpi', probe='1',
    output=['energy', 'theta', 'phi']):
    """

    """

    units = units.lower()
    if isinstance(probe, int):
        probe = str(probe)

    data_in = get_data(in_tvarname)

    if data_in == None:
        logging.error('Error, could not find the variable: ' + in_tvarname)
        return None

    if isinstance(output, str):
        output = output.split(' ')

    dist_in = mms_get_fpi_dist(in_tvarname, species=species, probe=probe, data_rate=data_rate)
    out_energy = np.zeros((dist_in['n_times'], dist_in['n_energy']))
    out_energy_y = np.zeros((dist_in['n_times'], dist_in['n_energy']))
    out_theta = np.zeros((dist_in['n_times'], dist_in['n_theta']))
    out_phi = np.zeros((dist_in['n_times'], dist_in['n_phi']))
    out_theta_y = np.zeros((dist_in['n_times'], dist_in['n_theta']))
    out_phi_y = np.zeros((dist_in['n_times'], dist_in['n_phi']))

    out_vars = []

    for i in range(0, len(data_in.times)):
        dist_in = mms_get_fpi_dist(in_tvarname, index=i, species=species, probe=probe, data_rate=data_rate)

        data = mms_convert_flux_units(dist_in, units=units)

        clean_data = mms_pgs_clean_data(data)

        if 'energy' in output:
            out_energy_y[i, :], out_energy[i, :] = spd_pgs_make_e_spec(clean_data)

        if 'theta' in output:
            out_theta_y[i, :], out_theta[i, :] = spd_pgs_make_theta_spec(clean_data)

        if 'phi' in output:
            out_phi_y[i, :], out_phi[i, :] = spd_pgs_make_phi_spec(clean_data)

    if 'energy' in output:
        spd_pgs_make_tplot(in_tvarname+'_energy', x=data_in.times, y=out_energy_y, z=out_energy, units=units, ylog=True)
        out_vars.append(in_tvarname+'_energy')

    if 'theta' in output:
        spd_pgs_make_tplot(in_tvarname+'_theta', x=data_in.times, y=out_theta_y, z=out_theta, units=units)
        out_vars.append(in_tvarname+'_theta')

    if 'phi' in output:
        spd_pgs_make_tplot(in_tvarname+'_phi', x=data_in.times, y=out_phi_y, z=out_phi, units=units)
        out_vars.append(in_tvarname+'_phi')

    return out_vars