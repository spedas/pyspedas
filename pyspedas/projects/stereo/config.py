import os

CONFIG = {'no_download': False,
          'local_data_dir': 'stereo_data/',
          'remote_data_dir': 'http://sprg.ssl.berkeley.edu/data/misc/stereo/'}

from pyspedas.preferences import apply_mission_preferences, apply_no_download_environment

apply_mission_preferences(CONFIG, "stereo")
apply_no_download_environment(CONFIG, "STEREO_NO_DOWNLOAD")

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'stereo'])

if os.environ.get('STEREO_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['STEREO_DATA_DIR']
