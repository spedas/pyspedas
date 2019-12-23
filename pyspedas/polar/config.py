import os

CONFIG = {'local_data_dir': 'polar_data/',
          'remote_data_dir': 'https://spdf.sci.gsfc.nasa.gov/pub/data/polar/'}

# override local data directory with environment variables
if os.environ.get('ROOT_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['ROOT_DATA_DIR'], 'polar'])

if os.environ.get('POLAR_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['POLAR_DATA_DIR']