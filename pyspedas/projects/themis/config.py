"""THEMIS sources: explicit data layouts and independent support-data URLs.

All source settings accept stored preferences and matching THM_* environment
variables. Changing remote_data_dir does not change metadata, variometer, or SSC
sources. Each resource uses its configured source without automatic fallback.
"""
import os

CONFIG = {'no_download': False,
          'local_data_dir': 'themis_data/',
          'remote_data_dir': 'https://themis.ssl.berkeley.edu/data/themis/',
          'remote_data_layout': 'themis',
          'variometer_remote_data_dir': 'https://themis.ssl.berkeley.edu/data/themis/',
          'variometer_remote_data_layout': 'themis',
          'gmag_metadata_file': 'https://themis.ssl.berkeley.edu/data/themis/thg/gmags_meta.csv',
          'ssc_remote_data_dir': 'https://cdaweb.gsfc.nasa.gov/pub/data/themis/'}

from pyspedas.preferences import apply_mission_preferences, apply_no_download_environment

apply_mission_preferences(CONFIG, "themis")
apply_no_download_environment(CONFIG, "THM_NO_DOWNLOAD")

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'],
                                           'themis'])

if os.environ.get('THM_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['THM_DATA_DIR']

# Source URLs and layouts can be overridden independently of the local cache.
for key in ('remote_data_dir', 'remote_data_layout',
            'variometer_remote_data_dir', 'variometer_remote_data_layout',
            'gmag_metadata_file', 'ssc_remote_data_dir'):
    env_key = 'THM_' + key.upper()
    if env_key in os.environ:
        CONFIG[key] = os.environ[env_key]


def resolve_source(family='data'):
    """Return the URL and explicit layout for ordinary or variometer data.

    THEMIS and UCLA use ``themis`` layout. SPDF and heliocloud use ``spdf``.
    URLs point to mission roots; paths beneath them include ``tha/``, ``thg/``,
    etc. Layout selection never depends on hostname or URL scheme, and sources
    are not retried against a different server.
    """
    if family not in ('data', 'variometer'):
        raise ValueError(f'Unknown THEMIS data family: {family!r}')
    prefix = 'variometer_' if family == 'variometer' else ''
    url = CONFIG[prefix + 'remote_data_dir']
    layout = CONFIG[prefix + 'remote_data_layout']
    if layout not in ('themis', 'spdf'):
        raise ValueError(f'Unsupported THEMIS {prefix}remote_data_layout: {layout!r}')
    if not isinstance(url, str) or not url.strip():
        raise ValueError(f'THEMIS {prefix}remote_data_dir must be a nonempty URL')
    return url, layout
