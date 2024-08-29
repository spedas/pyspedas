import os

CONFIG = {'local_data_dir': 'stereo_data/',
          'remote_data_dir': 'http://sprg.ssl.berkeley.edu/data/misc/stereo/'}

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'stereo'])

if os.environ.get('STEREO_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['STEREO_DATA_DIR']