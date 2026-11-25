"""Select one lexicographically last filename per explicitly captured identity."""

import re


def last_version_per_identity(filenames, versioned_regex):
    r"""Return the lexicographically last filename for each captured identity.

    Parameters
    ----------
    filenames : iterable of str, str, or None
        Matching filenames, paths, or URLs from one known directory. Only
        basenames are matched; the original input strings are returned.
    versioned_regex : str or compiled regular expression
        A regex that fully matches each basename and contains a named
        ``identity`` capture group. An optional named ``version`` group is
        permitted but is not used for ordering. An empty identity string is
        valid and groups all matching files together.

    Returns
    -------
    list of str
        One original filename per identity, sorted lexicographically. Empty
        input or None returns an empty list; a string returns a one-element
        list containing that string. These shortcuts do not validate the regex.
        The input is not modified.

    Raises
    ------
    ValueError
        If the regex is invalid, is not a string regex, lacks a named
        ``identity`` group, fails to fully match a basename, or does not
        capture an identity for a matching basename.
    TypeError
        If filenames is bytes or contains non-string elements.

    Notes
    -----
    All candidates must belong to the same directory; parent directories do
    not participate in identity matching. Both slash and backslash path
    separators are recognized. No files are opened and no network requests
    are made.

    Selection sorts complete original filenames as strings, not captured
    versions numerically. For example, ``v2.9.0`` sorts after ``v2.10.0``.
    Callers must supply a convention for which this ordering is appropriate.

    Examples
    --------
    >>> files = ['obs_A_v01.cdf', 'obs_A_v02.cdf', 'obs_B_v01.cdf']
    >>> pattern = r'(?P<identity>obs_[A-Z])_v(?P<version>\d+)\.cdf'
    >>> last_version_per_identity(files, pattern)
    ['obs_A_v02.cdf', 'obs_B_v01.cdf']
    """
    if filenames is None:
        return []
    if isinstance(filenames, str):
        return [filenames]
    if isinstance(filenames, bytes):
        raise TypeError('filenames must contain strings, not bytes')
    filenames = list(filenames)
    if not filenames:
        return []

    try:
        pattern = re.compile(versioned_regex)
    except (re.error, TypeError) as exc:
        raise ValueError('versioned_regex must be a valid string regex') from exc
    if not isinstance(pattern.pattern, str):
        raise ValueError('versioned_regex must be a string regex, not a bytes regex')
    if 'identity' not in pattern.groupindex:
        raise ValueError("versioned_regex must contain a named 'identity' group")

    grouped = {}
    for filename in filenames:
        if not isinstance(filename, str):
            raise TypeError('filenames must contain only strings')
        basename = filename.replace('\\', '/').rsplit('/', 1)[-1]
        match = pattern.fullmatch(basename)
        if match is None:
            raise ValueError(f'Filename {filename!r} does not fully match versioned_regex')
        identity = match.group('identity')
        if identity is None:
            raise ValueError(f'No identity captured for filename {filename!r}')
        grouped.setdefault(identity, []).append(filename)

    return sorted(sorted(matches)[-1] for matches in grouped.values())
