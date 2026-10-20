import os

CONFIG = {'no_download': False,
          'local_data_dir': 'erg_data/',
          'remote_data_dir': 'https://ergsc.isee.nagoya-u.ac.jp/data/ergsc/',
          'ground_remote_data_dir': 'https://ergsc.isee.nagoya-u.ac.jp/data/ergsc/ground/',
          'satellite_remote_data_dir': 'https://ergsc.isee.nagoya-u.ac.jp/data/ergsc/satellite/erg/'}

from pyspedas.preferences import apply_mission_preferences, apply_no_download_environment

# Keep legacy base-URL preferences working, unless a split URL is also set.
_default_urls = CONFIG.copy()
apply_mission_preferences(CONFIG, "erg")
if CONFIG['remote_data_dir'] != _default_urls['remote_data_dir']:
    for key, subdir in [('ground_remote_data_dir', 'ground/'),
                        ('satellite_remote_data_dir', 'satellite/erg/')]:
        if CONFIG[key] == _default_urls[key]:
            CONFIG[key] = CONFIG['remote_data_dir'].rstrip('/') + '/' + subdir
apply_no_download_environment(CONFIG, "ERG_NO_DOWNLOAD")

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'ergsc'])

if os.environ.get('ERG_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['ERG_DATA_DIR']

if os.environ.get('ERG_REMOTE_DATA_DIR'):
    CONFIG['remote_data_dir'] = os.environ['ERG_REMOTE_DATA_DIR']
    CONFIG['ground_remote_data_dir'] = CONFIG['remote_data_dir'].rstrip('/') + '/ground/'
    CONFIG['satellite_remote_data_dir'] = CONFIG['remote_data_dir'].rstrip('/') + '/satellite/erg/'

if os.environ.get('ERG_GROUND_REMOTE_DATA_DIR'):
    CONFIG['ground_remote_data_dir'] = os.environ['ERG_GROUND_REMOTE_DATA_DIR']

if os.environ.get('ERG_SATELLITE_REMOTE_DATA_DIR'):
    CONFIG['satellite_remote_data_dir'] = os.environ['ERG_SATELLITE_REMOTE_DATA_DIR']
