import os

CONFIG = {'local_data_dir': 'poes_data/',
          'remote_data_dir': 'https://spdf.sci.gsfc.nasa.gov/pub/data/noaa/'}

# override local data directory with environment variables
if os.environ.get('ROOT_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['ROOT_DATA_DIR'], 'poes'])

if os.environ.get('POES_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['POES_DATA_DIR']