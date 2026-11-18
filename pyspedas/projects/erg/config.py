"""ERG data sources and cache configuration.

``remote_data_dir`` and ``ERG_REMOTE_DATA_DIR`` are deprecated compatibility
settings for a common ERG-SC root. Use the satellite, att, and ground URL/layout
pairs instead. Explicit family preferences override the legacy preference;
family environment variables override the legacy environment variable.
"""
import logging
import os

CONFIG = {'no_download': False,
          'local_data_dir': 'erg_data/',
          'remote_data_dir': 'https://ergsc.isee.nagoya-u.ac.jp/data/ergsc/',
          'ground_remote_data_dir': 'https://ergsc.isee.nagoya-u.ac.jp/data/ergsc/ground/',
          'ground_remote_data_layout': 'ergsc',
          'att_remote_data_dir': 'https://ergsc.isee.nagoya-u.ac.jp/data/ergsc/satellite/erg/',
          'att_remote_data_layout': 'ergsc',
          'satellite_remote_data_layout': 'ergsc',
          'satellite_remote_data_dir': 'https://ergsc.isee.nagoya-u.ac.jp/data/ergsc/satellite/erg/'}

from pyspedas.preferences import apply_mission_preferences, apply_no_download_environment

# Keep legacy base-URL preferences working, unless a split URL is also set.
_default_urls = CONFIG.copy()
apply_mission_preferences(CONFIG, "erg")
if CONFIG['remote_data_dir'] != _default_urls['remote_data_dir']:
    logging.warning('ERG remote_data_dir is deprecated; use satellite_remote_data_dir, '
                    'att_remote_data_dir, and ground_remote_data_dir instead.')
    for key, subdir in [('ground_remote_data_dir', 'ground/'),
                        ('satellite_remote_data_dir', 'satellite/erg/'),
                        ('att_remote_data_dir', 'satellite/erg/')]:
        if CONFIG[key] == _default_urls[key]:
            CONFIG[key] = CONFIG['remote_data_dir'].rstrip('/') + '/' + subdir
apply_no_download_environment(CONFIG, "ERG_NO_DOWNLOAD")

# override local data directory with environment variables
if os.environ.get('SPEDAS_DATA_DIR'):
    CONFIG['local_data_dir'] = os.sep.join([os.environ['SPEDAS_DATA_DIR'], 'ergsc'])

if os.environ.get('ERG_DATA_DIR'):
    CONFIG['local_data_dir'] = os.environ['ERG_DATA_DIR']

if os.environ.get('ERG_REMOTE_DATA_DIR'):
    logging.warning('ERG_REMOTE_DATA_DIR is deprecated; use ERG_SATELLITE_REMOTE_DATA_DIR, ERG_ATT_REMOTE_DATA_DIR, and ERG_GROUND_REMOTE_DATA_DIR instead.')
    CONFIG['remote_data_dir'] = os.environ['ERG_REMOTE_DATA_DIR']
    CONFIG['ground_remote_data_dir'] = CONFIG['remote_data_dir'].rstrip('/') + '/ground/'
    CONFIG['satellite_remote_data_dir'] = CONFIG['remote_data_dir'].rstrip('/') + '/satellite/erg/'
    CONFIG['att_remote_data_dir'] = CONFIG['remote_data_dir'].rstrip('/') + '/satellite/erg/'

if os.environ.get('ERG_GROUND_REMOTE_DATA_DIR'):
    CONFIG['ground_remote_data_dir'] = os.environ['ERG_GROUND_REMOTE_DATA_DIR']

if os.environ.get('ERG_SATELLITE_REMOTE_DATA_DIR'):
    CONFIG['satellite_remote_data_dir'] = os.environ['ERG_SATELLITE_REMOTE_DATA_DIR']

if os.environ.get('ERG_ATT_REMOTE_DATA_DIR'):
    CONFIG['att_remote_data_dir'] = os.environ['ERG_ATT_REMOTE_DATA_DIR']

for family in ('satellite', 'att', 'ground'):
    layout_env = 'ERG_' + family.upper() + '_REMOTE_DATA_LAYOUT'
    if layout_env in os.environ:
        CONFIG[family + '_remote_data_layout'] = os.environ[layout_env]


def resolve_source(family):
    """Return explicit loader keywords for an ERG data family.

    URLs name the family root (including ``satellite/erg/`` for ERG-SC
    satellite and attitude data). Layouts describe paths below that root,
    independently of the hostname or URL scheme. Ground data support only
    the ERG-SC layout. There is no automatic source fallback.
    """
    if family not in ('satellite', 'att', 'ground'):
        raise ValueError(f'Unknown ERG data family: {family!r}')
    url = CONFIG[family + '_remote_data_dir']
    layout = CONFIG[family + '_remote_data_layout']
    supported = ('ergsc',) if family == 'ground' else ('ergsc', 'spdf')
    if layout not in supported:
        raise ValueError(f'Unsupported ERG {family} layout: {layout!r}; expected {supported}')
    if not isinstance(url, str) or not url.strip():
        raise ValueError(f'ERG {family}_remote_data_dir must be a nonempty URL')
    return {'remote_data_dir': url, 'remote_data_layout': layout}
