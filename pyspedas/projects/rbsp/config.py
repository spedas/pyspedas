import os

CONFIG = {'local_data_dir': 'rbsp_data/',
          'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/rbsp/'}

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'rbsp'])

if os.environ.get('RBSP_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['RBSP_DATA_DIR']