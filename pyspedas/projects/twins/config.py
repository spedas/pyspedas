import os

CONFIG = {'no_download': False,
          'local_data_dir': 'twins_data/',
          'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/twins/'}

from pyspedas.preferences import apply_mission_preferences, apply_no_download_environment

apply_mission_preferences(CONFIG, "twins")
apply_no_download_environment(CONFIG, "TWINS_NO_DOWNLOAD")

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'twins'])

if os.environ.get('TWINS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['TWINS_DATA_DIR']
