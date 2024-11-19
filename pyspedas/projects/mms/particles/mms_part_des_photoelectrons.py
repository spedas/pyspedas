import os
import logging
from pyspedas.projects.mms.mms_config import CONFIG
from pyspedas.utilities.download import download
from pytplot import get_data, cdf_to_tplot

logging.captureWarnings(True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def mms_part_des_photoelectrons(dist_var):
    """
    Loads and returns the FPI/DES photoelectron model based on stepper ID

    Input
    ----------
        dist_var: str
            tplot variable containing DES distribution data

    Notes
    ----------
        For more information on the model, see:
        https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2017JA024518

    Returns
    ----------
        Dictionary containing the photoelectron model
    """
    data = get_data(dist_var)

    if data is None:
        logging.error('Problem reading DES distribution variable')
        return

    # get the metadata for the 'energy_table_name' from the global attributes
    metadata = get_data(dist_var, metadata=True)

    try:
        table_name = metadata['CDF']['GATT']['Energy_table_name']
    except KeyError:
        logging.error('Problem extracting the energy table name from the DF metadata')
        return

    # Workaround for cdflib globalattsget() bug
    if isinstance(table_name,list):
        table_name = table_name[0]
    stepper_id = table_name.replace('.txt', '').split('energies_des_')[-1]

    # we'll need the data rate
    data_rate = dist_var.split('_')[-1]

    # download the model file from the SDC
    pe_model = download(
        last_version=True,
        remote_path='https://lasp.colorado.edu/mms/sdc/public/data/models/fpi/',
        remote_file='mms_fpi_'+data_rate+'_l2_des-bgdist_v?.?.?_p'+stepper_id+'.cdf',
        local_path=os.path.join(CONFIG['local_data_dir'], 'mms'+os.path.sep+'sdc'+os.path.sep+'public'+os.path.sep+'data'+os.path.sep+'models'+os.path.sep+'fpi'+os.path.sep+''))

    if len(pe_model) != 1:
        logging.error('Problem downloading DES model from the SDC')
        return

    model_vars = cdf_to_tplot(pe_model[0], get_support_data=True)

    if data_rate == 'fast':
        bg_dist = get_data('mms_des_bgdist_fast')
        nphoto = get_data('mms_des_numberdensity_fast')
        return {'bg_dist': bg_dist, 'n': nphoto}
    elif data_rate == 'brst':
        bg_dist_0 = get_data('mms_des_bgdist_p0_brst')
        bg_dist_1 = get_data('mms_des_bgdist_p1_brst')
        nphoto_0 = get_data('mms_des_numberdensity_p0_brst')
        nphoto_1 = get_data('mms_des_numberdensity_p1_brst')
        return {'bgdist_p0': bg_dist_0, 
                'bgdist_p1': bg_dist_1, 
                'n_0': nphoto_0, 
                'n_1': nphoto_1}

    # shouldn't get here
    logging.error('Error: something went wrong with the photoelectron model')
    return
