import os

CONFIG = {'local_data_dir': 'st5_data/',
          'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/st5/'}

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'st5'])

if os.environ.get('ST5_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['ST5_DATA_DIR']
    