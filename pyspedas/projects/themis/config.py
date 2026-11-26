"""THEMIS sources: one mission data source and an independent SSC source.

Experimental source-routing API: the configuration interface for selecting data
sources and layouts has not been finalized. Please share feedback on configuration
names, source selection and cache behavior at
https://github.com/spedas/pyspedas/issues to help shape the stable API.

Satellite data, all GMAG networks and station metadata share remote_data_dir.
Source settings accept stored preferences and matching THM_* environment
variables. Requests never fall back to a different provider.
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

SSC_SOURCES = {
    'spdf': {
        'ssc_remote_data_dir': 'https://cdaweb.gsfc.nasa.gov/pub/data/themis/',
    },
}

CONFIG = {'no_download': False,
          'local_data_dir': 'themis_data/',
          **DATA_SOURCES['berkeley'],
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
for key in ('remote_data_dir', 'remote_data_layout', 'ssc_remote_data_dir'):
    env_key = 'THM_' + key.upper()
    if env_key in os.environ:
        CONFIG[key] = os.environ[env_key]


def resolve_source():
    """Return the shared URL and explicit layout for all mission data.

    THEMIS and UCLA use ``themis`` layout. SPDF and heliocloud use ``spdf``.
    URLs point to mission roots; paths beneath them include ``tha/``, ``thg/``,
    etc. Layout selection never depends on hostname or URL scheme, and sources
    are not retried against a different server.
    """
    url = CONFIG['remote_data_dir']
    layout = CONFIG['remote_data_layout']
    if layout not in ('themis', 'spdf'):
        raise ValueError(f'Unsupported THEMIS remote_data_layout: {layout!r}')
    if not isinstance(url, str) or not url.strip():
        raise ValueError('THEMIS remote_data_dir must be a nonempty URL')
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
    """Select the satellite, ground and GMAG metadata provider for this session.

    .. warning::

        Experimental API. Parameters, return values, and behavior may
        change, or this feature may be removed, between releases without
        the standard deprecation period.

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

    .. warning::

        Experimental API. Parameters, return values, and behavior may
        change, or this feature may be removed, between releases without
        the standard deprecation period.

    Returns
    -------
    str or None
        Matching provider tag, or None for custom or incomplete settings.
        Only this source's relevant settings participate in the match.
    """
    return _get_source(DATA_SOURCES)


def set_ssc_source(source_tag):
    """Select the SSC provider for this session.

    .. warning::

        Experimental API. Parameters, return values, and behavior may
        change, or this feature may be removed, between releases without
        the standard deprecation period.

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

    .. warning::

        Experimental API. Parameters, return values, and behavior may
        change, or this feature may be removed, between releases without
        the standard deprecation period.

    Returns
    -------
    str or None
        Matching provider tag, or None for custom or incomplete settings.
        Only this source's relevant settings participate in the match.
    """
    return _get_source(SSC_SOURCES)
