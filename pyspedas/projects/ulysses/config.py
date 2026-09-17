import os

CONFIG = {'local_data_dir': 'ulysses_data/',
          'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/ulysses/'}

from pyspedas.preferences import apply_mission_preferences

apply_mission_preferences(CONFIG, "ulysses")

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'ulysses'])

if os.environ.get('ULY_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['ULY_DATA_DIR']
