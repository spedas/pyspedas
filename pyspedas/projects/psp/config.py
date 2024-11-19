import os

CONFIG = {
    'local_data_dir': 'psp_data/',
    'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/psp/',
    'sweap_remote_data_dir': 'http://sweap.cfa.harvard.edu/data/sci/',
    'fields_remote_data_dir': 'https://sprg.ssl.berkeley.edu/data/spp/data/sci/'
}

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'psp'])

if os.environ.get('PSP_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['PSP_DATA_DIR']