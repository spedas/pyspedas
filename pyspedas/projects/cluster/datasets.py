from .load import load
from pyspedas.utilities.datasets import find_datasets


def datasets(instrument=None, label=True):
    """
    Query SPDF for datasets available for a given Cluster instrument

    Parameters
    ----------
        instrument : str
            Instrument to use in query. Valid options: 'ASP','CIS','DWP','EDI','EFW','FGM','PEA','RAP','STA','WBD','WHI'
            Default: None

        label: bool
            If True, print both the dataset name and label; otherwise print only the dataset name.


    Examples
    --------
    >>> import pyspedas
    >>> pyspedas.projects.cluster.datasets('FGM')
    """
    return find_datasets(mission='Cluster', instrument=instrument, label=label)
