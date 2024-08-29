import os

CONFIG = {'local_data_dir': 'solar_orbiter_data/',
          'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/solar-orbiter/'}

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'solar-orbiter'])

if os.environ.get('SOLO_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['SOLO_DATA_DIR']