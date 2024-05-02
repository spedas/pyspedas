import os

CONFIG = {'local_data_dir': 'mth5/',
          'remote_data_dir': ''}  # Reserved for the future use

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'],
                                           'mth5'])