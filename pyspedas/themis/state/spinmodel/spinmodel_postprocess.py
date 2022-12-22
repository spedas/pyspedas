from .spinmodel import Spinmodel, save_spinmodel


def spinmodel_postprocess(probe: str):
    """ Create and initialize three Spinmodel objects using tplot variables loaded from the STATE CDFs.

        The three models correspond to the three available correction levels: 0 = no corrections, 1 = waveform
        corrections, 2 = spin fit corrections.

        Each of the three models is stored in a dictionary via the save_spinmodel routine.

    Args:
        probe (str):  A single letter string specifying the probe for the models being built.

    """
    print("Creating spin model for probe ", probe, "correction level 0")
    # Expect a warning message here: That name is currently not in tplot.
    # Maybe there's a better idiom in pytplot for checking whether a variable exists?
    model0 = Spinmodel(probe, 0)
    save_spinmodel(probe, 0, model0)
    print("Creating spin model for probe ", probe, "correction level 1")
    model1 = Spinmodel(probe, 1)
    save_spinmodel(probe, 1, model1)
    print("Creating spin model for probe ", probe, "correction level 2")
    model2 = Spinmodel(probe, 2)
    save_spinmodel(probe, 2, model2)
