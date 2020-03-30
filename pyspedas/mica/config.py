import os

CONFIG = {'local_data_dir': 'mica_data/',
          'remote_data_dir': 'http://mirl.unh.edu/ULF/cdf/'}

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'mica'])

if os.environ.get('MICA_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['MICA_DATA_DIR']