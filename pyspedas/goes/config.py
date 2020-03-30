import os

CONFIG = {'local_data_dir': 'goes_data/',
          'remote_data_dir': 'https://satdat.ngdc.noaa.gov/sem/goes/data/'}

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'goes'])

if os.environ.get('GOES_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['GOES_DATA_DIR']