import os

CONFIG = {'local_data_dir': 'csswe_data/',
          'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/csswe/'}

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'csswe'])

if os.environ.get('CSSWE_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['CSSWE_DATA_DIR']