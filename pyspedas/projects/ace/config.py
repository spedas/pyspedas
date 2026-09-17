import os

CONFIG = {'local_data_dir': 'ace_data/',
          'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/ace/'}

from pyspedas.preferences import apply_mission_preferences

apply_mission_preferences(CONFIG, "ace")

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'ace'])

if os.environ.get('ACE_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['ACE_DATA_DIR']
