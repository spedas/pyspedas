import logging
import os

# Provider presets contain only the CONFIG keys changed by that selection.
SDC_SOURCES = {
    'sdc': {
        'sdc_data_dir': 'https://lasp.colorado.edu/mms/sdc/',
    },
}

DATA_SOURCES = {
    'sdc': {
        'data_access': 'sdc',
        'sdc_data_dir': 'https://lasp.colorado.edu/mms/sdc/',
    },
    'spdf': {
        'data_access': 'archive',
        'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/mms/',
    },
    'heliocloud': {
        'data_access': 'archive',
        'remote_data_dir': 's3://gov-nasa-hdrl-data1/spdf/cdaweb/data/mms/',
    },
}

CONFIG = {'local_data_dir': 'pydata',
         #'local_data_dir': '/Users/eric/data/mms', # example of setting your local data directory on macOS
         #'local_data_dir': 'c:\users\eric\data\mms', # and Windows
          'mirror_data_dir': None, # e.g., '/Volumes/data_network/data/mms'
          'debug_mode': False,
          'download_only': False,
          'no_download': False,
          **DATA_SOURCES['sdc'],
          'remote_data_dir': DATA_SOURCES['spdf']['remote_data_dir']}

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


def _set_source(source_tag, sources, family):
    """Validate a preset before updating its related CONFIG settings together."""
    if not isinstance(source_tag, str) or source_tag not in sources:
        choices = ', '.join(sorted(sources))
        raise ValueError(f'Unknown MMS {family} source {source_tag!r}; valid choices: {choices}')
    settings = sources[source_tag]
    CONFIG.update(settings)
    logging.info('MMS %s source set to %s: %s', family, source_tag,
                 ', '.join(f'{key}={value}' for key, value in settings.items()))


def _get_source(sources):
    """Recognize a preset from current settings, including direct CONFIG edits."""
    for source_tag, settings in sources.items():
        if all(CONFIG.get(key) == value for key, value in settings.items()):
            return source_tag
    return None


def set_data_source(source_tag):
    """Select the data provider for this session.

    Selecting ``sdc`` sets the SDC URL and API access; archive selections set
    the archive URL and access method, retaining the independent SDC URL.
    The inactive archive URL is retained when selecting SDC.

    Parameters
    ----------
    source_tag : str
        Provider tag: ``sdc``, ``spdf``, ``heliocloud``. Tags are case-sensitive.

    Raises
    ------
    ValueError
        If the tag is unsupported. CONFIG is unchanged in that case.

    Notes
    -----
    Updates only this source's CONFIG keys and logs the resulting settings at
    INFO level. No network requests are made and preferences are not saved.
    """
    _set_source(source_tag, DATA_SOURCES, 'data')


def get_data_source():
    """Identify the current data provider from CONFIG.

    Returns
    -------
    str or None
        Matching provider tag, or None for custom or incomplete settings.
        Only this source's relevant settings participate in the match.
    """
    return _get_source(DATA_SOURCES)


def set_sdc_source(source_tag):
    """Select the SDC provider for this session.

    Parameters
    ----------
    source_tag : str
        Provider tag: ``sdc``. Tags are case-sensitive.

    Raises
    ------
    ValueError
        If the tag is unsupported. CONFIG is unchanged in that case.

    Notes
    -----
    Updates only this source's CONFIG keys and logs the resulting settings at
    INFO level. No network requests are made and preferences are not saved.
    """
    _set_source(source_tag, SDC_SOURCES, 'SDC')


def get_sdc_source():
    """Identify the current SDC provider from CONFIG.

    Returns
    -------
    str or None
        Matching provider tag, or None for custom or incomplete settings.
        Only this source's relevant settings participate in the match.
    """
    return _get_source(SDC_SOURCES)
