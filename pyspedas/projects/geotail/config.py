import os

CONFIG = {'local_data_dir': 'geotail_data/',
          'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/geotail/'}

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'geotail'])

if os.environ.get('GEOTAIL_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['GEOTAIL_DATA_DIR']