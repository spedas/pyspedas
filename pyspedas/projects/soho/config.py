import os

CONFIG = {'no_download': False,
          'local_data_dir': 'soho_data/',
          'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/soho/'}

from pyspedas.preferences import apply_mission_preferences, apply_no_download_environment

apply_mission_preferences(CONFIG, "soho")
apply_no_download_environment(CONFIG, "SOHO_NO_DOWNLOAD")

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'soho'])

if os.environ.get('SOHO_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['SOHO_DATA_DIR']
