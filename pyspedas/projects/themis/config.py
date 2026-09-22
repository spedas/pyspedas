import os

CONFIG = {'no_download': False,
          'local_data_dir': 'themis_data/',
          'remote_data_dir': 'https://themis.ssl.berkeley.edu/data/themis/'}
#          'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/themis/'}
#          'remote_data_dir': 'https://themis-data.igpp.ucla.edu/'}

from pyspedas.preferences import apply_mission_preferences, apply_no_download_environment

apply_mission_preferences(CONFIG, "themis")
apply_no_download_environment(CONFIG, "THM_NO_DOWNLOAD")

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'],
                                           'themis'])

if os.environ.get('THM_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['THM_DATA_DIR']
