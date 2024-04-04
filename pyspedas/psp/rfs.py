import cdflib


def rfs_variables_to_load(files):
    """
    This function finds a list of variables to load
    from the RFS files (essentially the same behavior
    as the IDL code).
    """
    out = []
    if len(files) == 0:
        return []
    # the variables should be the same across all files
    file = files[0]
    cdf_file = cdflib.CDF(file)
    cdf_info = cdf_file.cdf_info()
    variables = cdf_info.rVariables + cdf_info.zVariables
    for variable in variables:
        if variable[0:7] != 'psp_fld':
            continue
        try:
            elements = cdf_file.varget(variable)
        except ValueError:
            continue
        if elements is None:
            continue
        if variable in out:
            continue
        out.append(variable)
    return out
