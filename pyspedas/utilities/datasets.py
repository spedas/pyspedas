from cdasws import CdasWs


def find_datasets(mission=None, instrument=None, label=False):
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
