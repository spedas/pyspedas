import os

CONFIG = {'local_data_dir': 'themis_data/',
          'remote_data_dir': 'http://themis.ssl.berkeley.edu/data/themis/'}

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'],
                                           'themis'])

if os.environ.get('THM_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['THM_DATA_DIR']
