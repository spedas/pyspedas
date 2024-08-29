def check_args(**kwargs):
    """
    Check arguments for themis load function

    Parameters:
        **kwargs : a dictionary of arguments
            Possible arguments are: probe, level
            The arguments can be: a string or a list of strings
            Invalid argument are ignored (e.g. probe = 'g', level='l0', etc.)
            Invalid argument names are ignored (e.g. 'probes', 'lev', etc.)


    Returns: list
        Prepared arguments in the same order as the inputs

    Examples:
        res_probe = check_args(probe='a')
        (res_probe, res_level) = check_args(probe='a b', level='l2')
        (res_level, res_probe) = check_args(level='l1', probe=['a', 'b'])

        # With incorrect argument probes:
        res = check_args(probe='a', level='l2', probes='a b') : res = [['a'], ['l2']]
    """

    valid_keys = {'probe', 'level'}
    valid_probe = {'a', 'b', 'c', 'd', 'e'}
    valid_level = {'l1', 'l2'}

    # Return list of values from arg_list that are only included in valid_set
    def valid_list(arg_list, valid_set):
        valid_res = []
        for arg in arg_list:
            if arg in valid_set:
                valid_res.append(arg)
        return valid_res

    # Return list
    res = []
    for key, values in kwargs.items():
        if key.lower() not in valid_keys:
            continue

        # resulting list
        arg_values = []

        # convert string into list, or ignore the argument
        if isinstance(values, str):
            values = [values]
        elif not isinstance(values, list):
            continue

        for value in values:
            arg_values.extend(value.strip().lower().split())

        # simple validation of the arguments
        if key.lower() == 'probe':
            arg_values = valid_list(arg_values, valid_probe)

        if key.lower() == 'level':
            arg_values = valid_list(arg_values, valid_level)

        res.append(arg_values)

    return res
