import os

CONFIG = {'local_data_dir': 'pydata',
         #'local_data_dir': '/Users/eric/data/mms', # example of setting your local data directory on macOS
         #'local_data_dir': 'c:\users\eric\data\mms', # and Windows
          'mirror_data_dir': None, # e.g., '/Volumes/data_network/data/mms'
          'debug_mode': False,
          'download_only': False,
          'no_download': False,
          'data_access': 'sdc',
          'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/mms/',
          'sdc_data_dir': 'https://lasp.colorado.edu/mms/sdc/'}

from pyspedas.preferences import apply_mission_preferences

apply_mission_preferences(CONFIG, "mms")

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'mms'])

if os.environ.get('MMS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['MMS_DATA_DIR']


if os.environ.get('MMS_MIRROR_DATA_DIR'):
    CONFIG['mirror_data_dir'] = os.environ['MMS_MIRROR_DATA_DIR']

for key in ('data_access', 'remote_data_dir', 'sdc_data_dir'):
    env_key = 'MMS_' + key.upper()
    if env_key in os.environ:
        CONFIG[key] = os.environ[env_key]


def sdc_url(path):
    """Build an SDC endpoint beneath the configured root, including public/sitl.

    This is independent of archive selection: ancillary data, interval services,
    authentication and models always use the SDC. Paths are relative to
    ``sdc_data_dir``, whose default ends with ``mms/sdc/``.
    """
    root = CONFIG['sdc_data_dir']
    if not isinstance(root, str) or not root.strip():
        raise ValueError('MMS sdc_data_dir must be a nonempty URL')
    return root.rstrip('/') + '/' + path.lstrip('/')
