import logging
from .spinmodel import Spinmodel, save_spinmodel
from pytplot import data_exists


def spinmodel_postprocess(probe: str, suffix: str=''):
    """ Create and initialize three Spinmodel objects using tplot variables loaded from the STATE CDFs.

        The three models correspond to the three available correction levels: 0 = no corrections, 1 = waveform
        corrections, 2 = spin fit corrections.

        Each of the three models is stored in a dictionary via the save_spinmodel routine.

    Args:
        probe (str):  A single letter string specifying the probe for the models being built.

    """

    # It is possible that /get_support_data was specified, but only a limited set of variables
    # was requested.  Check that all needed spin model variables are present before attempting
    # to create the models.

    sm_quantities = ['tend', 'spinper', 'c', 'phaserr', 'nspins', 'npts', 'maxgap', 'initial_delta_phi', 'idpu_spinper',
                     'segflags']
    missing_var = False
    for v in sm_quantities:
        non_ecl_v = 'th' + probe + '_spin_' + v + suffix
        ecl_v = 'th' + probe + '_spin_ecl_' + v + suffix
        if not (data_exists(non_ecl_v) and data_exists(ecl_v)):
            missing_var = True

    if missing_var:
        logging.warning("Some required spin model variables were not requested, skipping spin model creation")
        return

    logging.info("Creating spin model for probe " + probe + " correction level 0")
    # Expect a warning message here: That name is currently not in tplot.
    # Maybe there's a better idiom in pytplot for checking whether a variable exists?
    model0 = Spinmodel(probe, 0, suffix)
    save_spinmodel(probe, 0, model0)
    logging.info("Creating spin model for probe " + probe + " correction level 1")
    model1 = Spinmodel(probe, 1, suffix)
    save_spinmodel(probe, 1, model1)
    logging.info("Creating spin model for probe " + probe + " correction level 2")
    model2 = Spinmodel(probe, 2, suffix)
    save_spinmodel(probe, 2, model2)
