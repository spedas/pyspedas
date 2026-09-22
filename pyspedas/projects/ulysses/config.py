import os

CONFIG = {'no_download': False,
          'local_data_dir': 'ulysses_data/',
          'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/ulysses/'}

from pyspedas.preferences import apply_mission_preferences, apply_no_download_environment

apply_mission_preferences(CONFIG, "ulysses")
apply_no_download_environment(CONFIG, "ULY_NO_DOWNLOAD")

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'ulysses'])

if os.environ.get('ULY_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['ULY_DATA_DIR']
