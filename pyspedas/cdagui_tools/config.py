import os

CONFIG = {'local_data_dir': 'cdaweb/',
          'cdas_endpoint': 'https://cdaweb.gsfc.nasa.gov/WS/cdasr/1/dataviews/sp_phys/',
          'remote_data_dir': 'https://cdaweb.gsfc.nasa.gov/sp_phys/data'}

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'cdaweb/'])