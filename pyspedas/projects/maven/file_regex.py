import re


def maven_kp_l2_regex():
    """
    Compile regular expressions for matching MAVEN KP and L2 file names.

    Parameters
    ----------

    Returns
    -------
    tuple 
        A tuple containing two compiled regular expressions:
            - kp_regex: Regular expression for matching Maven KP file names.
            - l2_regex: Regular expression for matching Maven L2 file names.
    """
    
    # kp pattern
    kp_pattern = (
        r"^mvn_(?P<{0}>kp)_"
        r"(?P<{1}>insitu|iuvs)"
        r"(?P<{2}>|_[a-zA-Z0-9\-]+)_"
        r"(?P<{3}>[0-9]{{4}})"
        r"(?P<{4}>[0-9]{{2}})"
        r"(?P<{5}>[0-9]{{2}})"
        r"(?P<{6}>|[t|T][0-9]{{6}})_"
        r"v(?P<{7}>[0-9]+)_r(?P<{8}>[0-9]+)\."
        r"(?P<{9}>tab)"
        r"(?P<{10}>\.gz)*"
    ).format(
        "instrument",
        "level",
        "description",
        "year",
        "month",
        "day",
        "time",
        "version",
        "revision",
        "extension",
        "gz",
    )

    kp_regex = re.compile(kp_pattern)

    l2_pattern = (
        r"^mvn_(?P<{0}>[a-zA-Z0-9]+)_"
        r"(?P<{1}>l[a-zA-Z0-9]+)"
        r"(?P<{2}>|_[a-zA-Z0-9\-]+)_"
        r"(?P<{3}>[0-9]{{4}})"
        r"(?P<{4}>[0-9]{{2}})"
        r"(?P<{5}>[0-9]{{2}})"
        r"(?P<{6}>|T[0-9]{{6}}|t[0-9]{{6}})_"
        r"v(?P<{7}>[0-9]+)_"
        r"r(?P<{8}>[0-9]+)\."
        r"(?P<{9}>cdf|xml|sts|md5)"
        r"(?P<{10}>\.gz)*"
    ).format(
        "instrument",
        "level",
        "description",
        "year",
        "month",
        "day",
        "time",
        "version",
        "revision",
        "extension",
        "gz",
    )
    l2_regex = re.compile(l2_pattern)
    return (kp_regex, l2_regex)
