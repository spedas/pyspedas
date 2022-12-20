import os

CONFIG = {'local_data_dir': 'cnofs_data/',
          'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/cnofs/'}

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'cnofs'])

if os.environ.get('CNOFS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['CNOFS_DATA_DIR']