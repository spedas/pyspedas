from cdasws import CdasWs


def find_datasets(mission=None, instrument=None, label=False):
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

    Returns
    -------
    None
        This function does not return any value. It prints the dataset IDs, and optionally labels, to the console.

    Examples
    --------
    >>> find_datasets(mission='MMS', instrument='FGM')
    MMS1_FGM_BRST_L2
    MMS1_FGM_SRVY_L2
    ...

    >>> find_datasets(mission='MMS', label=True)
    MMS1_ASPOC_SRVY_L2: Level 2 Active Spacecraft Potential Control Survey Data - K. Torkar, R. Nakamura (IWF)
    ...
    """

    cdas = CdasWs()
    datasets = cdas.get_datasets(observatoryGroup=mission)
    for index, dataset in enumerate(datasets):
        if instrument is not None:
            if instrument.upper() not in dataset['Id']:
                continue
        if label:
            print(dataset['Id'] + ': ' + dataset['Label'])
        else:
            print(dataset['Id'])
