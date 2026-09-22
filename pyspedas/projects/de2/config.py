import os

CONFIG = {'no_download': False,
          'local_data_dir': 'de2_data/',
          'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/de/de2/'}

from pyspedas.preferences import apply_mission_preferences, apply_no_download_environment

apply_mission_preferences(CONFIG, "de2")
apply_no_download_environment(CONFIG, "DE2_NO_DOWNLOAD")

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'de2'])

if os.environ.get('DE2_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['DE2_DATA_DIR']
