import os

CONFIG = {'local_data_dir': 'ace_data/',
          'remote_data_dir': 'https://spdf.sci.gsfc.nasa.gov/pub/data/ace/'}

# override local data directory with environment variables
if os.environ.get('ROOT_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['ROOT_DATA_DIR'], 'ace'])

if os.environ.get('ACE_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['ACE_DATA_DIR']