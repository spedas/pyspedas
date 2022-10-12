from pyspedas.vires.load import load


def data(trange=None,
         collection=None,
         measurements=None,
         models=None,
         sampling_step=None,
         auxiliaries=None,
         residuals=False):
    return load(trange=trange,
                collection=collection,
                measurements=measurements,
                models=models,
                sampling_step=sampling_step,
                auxiliaries=auxiliaries,
                residuals=residuals)
