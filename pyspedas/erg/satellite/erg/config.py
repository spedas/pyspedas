import os

CONFIG = {'local_data_dir': 'erg_data/',
          'remote_data_dir': 'https://ergsc.isee.nagoya-u.ac.jp/data/ergsc/'}

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join(
        [os.environ['SPEDAS_DATA_DIR'], 'ergsc'])

if os.environ.get('ERG_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['ERG_DATA_DIR']

if os.environ.get('ERG_REMOTE_DATA_DIR'):
    CONFIG['remote_data_dir'] = os.environ['ERG_REMOTE_DATA_DIR']
