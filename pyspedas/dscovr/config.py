import os

CONFIG = {'local_data_dir': 'dscovr_data/',
          'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/dscovr/'}

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'dscovr'])

if os.environ.get('DSC_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['DSC_DATA_DIR']