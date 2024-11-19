import os

CONFIG = {'local_data_dir': 'omni_data/',
          'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/omni/omni_cdaweb/'}

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'omni'])

if os.environ.get('OMNI_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['OMNI_DATA_DIR']