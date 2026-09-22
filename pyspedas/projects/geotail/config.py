import os

CONFIG = {'no_download': False,
          'local_data_dir': 'geotail_data/',
          'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/geotail/'}

from pyspedas.preferences import apply_mission_preferences, apply_no_download_environment

apply_mission_preferences(CONFIG, "geotail")
apply_no_download_environment(CONFIG, "GEOTAIL_NO_DOWNLOAD")

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'geotail'])

if os.environ.get('GEOTAIL_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['GEOTAIL_DATA_DIR']
