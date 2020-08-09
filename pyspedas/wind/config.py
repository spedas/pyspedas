import os

CONFIG = {'local_data_dir': 'wind_data/',
          'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/wind/'}

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'wind'])

if os.environ.get('WIND_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['WIND_DATA_DIR']