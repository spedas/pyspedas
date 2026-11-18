"""Compatibility entry point for the configurable MMS archive loader."""

from .mms_load_data_archive import mms_load_data_archive


def mms_load_data_spdf(*args, **kwargs):
    """Load from CONFIG['remote_data_dir']; retain the historical helper name.

    The configured archive can be SPDF, heliocloud, or another compatible mirror.
    """
    return mms_load_data_archive(*args, **kwargs)
