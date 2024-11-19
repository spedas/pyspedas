from pyspedas import find_datasets


def datasets(instrument=None, label=True):
    """
    Retrieves available datasets for the specified instrument on the Van Allen Probes (RBSP) mission.

    Parameters
    ----------
    instrument : str, optional
        Name of the instrument for which to find datasets. If None, finds datasets for all instruments on the mission.

    label : bool, default=True
        If True, the function prints both the dataset ID and label. If False, only the dataset ID is printed.

    Returns
    -------
    list of str
        List of available datasets for the specified instrument or for all instruments if no instrument is specified.

    Examples
    --------
    >>> pyspedas.projects.rbsp.find_datasets(instrument='REPT', label=True)
    ...
    RBSPA_REL03_ECT-REPT-SCI-L3: RBSP/ECT REPT Pitch Angle Resolved Electron and Proton Fluxes. Electron energies: 2 - 59.45 MeV. Proton energies: 21.25 - 0 MeV - D. Baker (University of Colorado at Boulder)
    ...
    """
    return find_datasets(mission='Van Allen Probes (RBSP)', instrument=instrument, label=label)
