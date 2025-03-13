import gzip


def is_gzip(file_path):
    r"""
    Check if a file is gzip-compressed.

    Parameters
    ----------
    file_path : str
       Path to the file to be checked

    Returns
    -------
    bool
        True if first two bytes are '0x1f 0x8b', false otherwise

    """
    with open(file_path, 'rb') as f:
        return f.read(2) == b'\x1f\x8b'
