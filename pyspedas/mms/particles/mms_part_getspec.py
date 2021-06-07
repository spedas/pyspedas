
import logging
from time import time

import pyspedas
from pyspedas.mms.particles.mms_part_products import mms_part_products

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

def mms_part_getspec(instrument='fpi', probe='1', species='e', data_rate='fast', 
    trange=None, output=['energy', 'theta', 'phi'], units='eflux', energy=None,
    phi=None, theta=None, pitch=None, gyro=None, mag_data_rate='srvy', fac_type='mphigeo'):
    """

    """

    start_time = time()

    if trange is None:
        # test data for development
        trange = ['2015-10-16/13:06', '2015-10-16/13:07']
        # data_rate = 'brst'
    
    data_vars = pyspedas.mms.fpi(datatype='d'+species+'s-dist', probe=probe, data_rate=data_rate, trange=trange, time_clip=True)

    if len(data_vars) == 0:
        logging.error('Error, no data loaded.')
        return None

    if not isinstance(probe, list):
        probe = [probe]

    # load state data (needed for coordinate transformations and field-aligned coordinates)
    pos_vars = pyspedas.mms.mec(probe=probe, trange=trange, time_clip=True)

    if len(pos_vars) == 0:
        logging.error('Error, no state data loaded.')
        return

    mag_vars = pyspedas.mms.fgm(probe=probe, trange=trange, time_clip=True)

    if len(mag_vars) == 0:
        logging.error('Error, no magnetic field data loaded.')
        return

    out_vars = []

    for prb in probe:
        mag_name = 'mms'+prb+'_fgm_b_gse_'+mag_data_rate+'_l2_bvec'
        pos_name = 'mms'+prb+'_mec_r_gse'

        if instrument == 'fpi':
            tname = 'mms'+str(prb)+'_d'+species+'s_dist_'+data_rate

        new_vars = mms_part_products(tname, species=species, instrument=instrument, probe=probe, data_rate=data_rate,
                          output=output, units=units, energy=energy, phi=phi, theta=theta, pitch=pitch, gyro=gyro,
                          mag_name=mag_name, pos_name=pos_name, fac_type=fac_type)
        out_vars = out_vars + new_vars

    logging.info('Finished; time to run: ' + str(round(time()-start_time, 1)) + ' seconds.')
    
    return out_vars