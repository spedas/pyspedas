from cdasws import CdasWs


def find_datasets(mission=None, instrument=None, label=False, quiet=False):
    """
    Find datasets from the Coordinated Data Analysis System (CDAS) based on mission and/or instrument criteria.

    This function queries the CDAS for datasets, optionally filtering by mission and instrument. It can
    also display labels for the datasets.

    Parameters
    ----------
    mission : str, optional
        The name of the mission to filter the datasets. If None, datasets are not filtered by mission.
    instrument : str, optional
        The name of the instrument to filter the datasets. If None, datasets are not filtered by instrument.
    label : bool, default=False
        If True, the function prints both the dataset ID and label. If False, only the dataset ID is printed.
    quiet: bool, default=False
        If True, suppresses printing of dataset IDs (and labels) found

    Returns
    -------
    list of str
        List of datasets found

    Examples
    --------
    >>> from pyspedas import find_datasets
    >>> find_datasets(mission='MMS', instrument='FGM')
    MMS1_FGM_BRST_L2
    MMS1_FGM_SRVY_L2
    ...

    >>> # Suppress printed output
    >>> from pyspedas import find_datasets
    >>> mms_list = find_datasets(mission='MMS', quiet=True)
    >>> print(mms_list[0:3])

    """

    cdas = CdasWs()
    datasets = cdas.get_datasets(observatoryGroup=mission)
    output_list = []
    for index, dataset in enumerate(datasets):
        if instrument is not None:
            if instrument.upper() not in dataset['Id']:
                continue
        if label:
            if not quiet:
                print(dataset['Id'] + ': ' + dataset['Label'])
        else:
            if not quiet:
                print(dataset['Id'])
        output_list.append(dataset['Id'])
    return output_list