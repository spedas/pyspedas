"""THEMIS sources: explicit data layouts and independent support-data URLs.

All source settings accept stored preferences and matching THM_* environment
variables. Changing remote_data_dir does not change metadata, variometer, or SSC
sources. Each resource uses its configured source without automatic fallback.
"""
import logging
import os

# Provider presets contain only the CONFIG keys changed by that selection.
DATA_SOURCES = {
    'berkeley': {
        'remote_data_dir': 'https://themis.ssl.berkeley.edu/data/themis/',
        'remote_data_layout': 'themis',
    },
    'ucla': {
        'remote_data_dir': 'https://themis-data.igpp.ucla.edu/',
        'remote_data_layout': 'themis',
    },
    'spdf': {
        'remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/themis/',
        'remote_data_layout': 'spdf',
    },
    'heliocloud': {
        'remote_data_dir': 's3://gov-nasa-hdrl-data1/spdf/cdaweb/data/themis/',
        'remote_data_layout': 'spdf',
    },
}

VARIOMETER_SOURCES = {
    'berkeley': {
        'variometer_remote_data_dir': 'https://themis.ssl.berkeley.edu/data/themis/',
        'variometer_remote_data_layout': 'themis',
    },
    'spdf': {
        'variometer_remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/themis/',
        'variometer_remote_data_layout': 'spdf',
    },
}

GMAG_METADATA_SOURCES = {
    'berkeley': {
        'gmag_metadata_file': 'https://themis.ssl.berkeley.edu/data/themis/thg/gmags_meta.csv',
    },
    'spdf': {
        'gmag_metadata_file': 'https://spdf.gsfc.nasa.gov/pub/data/themis/thg/gmags_meta.csv',
    },
}

SSC_SOURCES = {
    'spdf': {
        'ssc_remote_data_dir': 'https://cdaweb.gsfc.nasa.gov/pub/data/themis/',
    },
}

CONFIG = {'no_download': False,
          'local_data_dir': 'themis_data/',
          **DATA_SOURCES['berkeley'],
          **VARIOMETER_SOURCES['berkeley'],
          **GMAG_METADATA_SOURCES['berkeley'],
          **SSC_SOURCES['spdf']}

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


def _set_source(source_tag, sources, family):
    """Validate a preset before updating its related CONFIG settings together."""
    if not isinstance(source_tag, str) or source_tag not in sources:
        choices = ', '.join(sorted(sources))
        raise ValueError(f'Unknown THEMIS {family} source {source_tag!r}; valid choices: {choices}')
    settings = sources[source_tag]
    CONFIG.update(settings)
    logging.info('THEMIS %s source set to %s: %s', family, source_tag,
                 ', '.join(f'{key}={value}' for key, value in settings.items()))


def _get_source(sources):
    """Recognize a preset from current settings, including direct CONFIG edits."""
    for source_tag, settings in sources.items():
        if all(CONFIG.get(key) == value for key, value in settings.items()):
            return source_tag
    return None


def set_data_source(source_tag):
    """Select the data provider for this session.

    Parameters
    ----------
    source_tag : str
        Provider tag: ``berkeley``, ``ucla``, ``spdf``, ``heliocloud``. Tags are case-sensitive.

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


def set_variometer_source(source_tag):
    """Select the variometer provider for this session.

    Parameters
    ----------
    source_tag : str
        Provider tag: ``berkeley``, ``spdf``. Tags are case-sensitive.

    Raises
    ------
    ValueError
        If the tag is unsupported. CONFIG is unchanged in that case.

    Notes
    -----
    Updates only this source's CONFIG keys and logs the resulting settings at
    INFO level. No network requests are made and preferences are not saved.
    """
    _set_source(source_tag, VARIOMETER_SOURCES, 'variometer')


def get_variometer_source():
    """Identify the current variometer provider from CONFIG.

    Returns
    -------
    str or None
        Matching provider tag, or None for custom or incomplete settings.
        Only this source's relevant settings participate in the match.
    """
    return _get_source(VARIOMETER_SOURCES)


def set_gmag_metadata_source(source_tag):
    """Select the GMAG metadata provider for this session.

    Parameters
    ----------
    source_tag : str
        Provider tag: ``berkeley``, ``spdf``. Tags are case-sensitive.

    Raises
    ------
    ValueError
        If the tag is unsupported. CONFIG is unchanged in that case.

    Notes
    -----
    Updates only this source's CONFIG keys and logs the resulting settings at
    INFO level. No network requests are made and preferences are not saved.
    """
    _set_source(source_tag, GMAG_METADATA_SOURCES, 'GMAG metadata')


def get_gmag_metadata_source():
    """Identify the current GMAG metadata provider from CONFIG.

    Returns
    -------
    str or None
        Matching provider tag, or None for custom or incomplete settings.
        Only this source's relevant settings participate in the match.
    """
    return _get_source(GMAG_METADATA_SOURCES)


def set_ssc_source(source_tag):
    """Select the SSC provider for this session.

    Parameters
    ----------
    source_tag : str
        Provider tag: ``spdf``. Tags are case-sensitive.

    Raises
    ------
    ValueError
        If the tag is unsupported. CONFIG is unchanged in that case.

    Notes
    -----
    Updates only this source's CONFIG keys and logs the resulting settings at
    INFO level. No network requests are made and preferences are not saved.
    """
    _set_source(source_tag, SSC_SOURCES, 'SSC')


def get_ssc_source():
    """Identify the current SSC provider from CONFIG.

    Returns
    -------
    str or None
        Matching provider tag, or None for custom or incomplete settings.
        Only this source's relevant settings participate in the match.
    """
    return _get_source(SSC_SOURCES)
