# -*- coding: utf-8 -*-
"""
File:
    ex_cdasws.py

Description:
    Example of how to use cdasws to find cdf files with NASA CDA web services.
    For more information on cdasws, see:
        https://pypi.org/project/cdasws/

"""

from cdasws import CdasWs
from pyspedas.cdagui.cdaweb import CDAWeb


def ex_cdasws():
    # Create an cdasws instance
    cdas = CdasWs()
    # Get a list of instrument types
    instr = cdas.get_instrument_types()
    # Print the list of instruments    print()
    print()
    print("------------- Using cdasws -------------")
    print("==========================================================")
    print()
    print("Instruments: " + str(instr))
    print()
    print("==========================================================")
    print()
    # Get a list of observatory groups
    observ = cdas.get_observatory_groups()
    # Print the list of observatory groups
    print("Observatories: " + str(observ))
    print()
    print("==========================================================")
    print()
    # Define a dictionary for the ARTEMIS mission
    mission_list = ['ARTEMIS']
    instrument_list = ['Electric Fields (space)']
    thisdict = {
        "observatoryGroup": mission_list,
        "instrumentType": instrument_list
    }
    # Get the datasets
    datasets = cdas.get_datasets(**thisdict)
    print("Datasets: " + str(datasets))
    print()
    print("==========================================================")
    print()
    # Get the filenames for 'THB_L2_FIT' cdf files
    dataset = ['THB_L2_FIT']
    t0 = '2020-01-01'
    t1 = '2020-01-01'
    result = cdas.get_data_file(dataset, [], t0, t1)
    print("File information: " + str(result))
    # Delete the cdas instance
    del cdas

    # Now use the simplified functions from pyspedas.cdagui.cdaweb
    cdaw = CDAWeb()
    print()
    print("==========================================================")
    print()
    print("-------------Using pyspedas -------------")
    print()
    print("==========================================================")
    print()
    i = cdaw.get_observatories()
    print("Instruments: " + str(i))
    print()
    print("==========================================================")
    print()
    o = cdaw.get_observatories()
    print("Observatories: " + str(o))
    print()
    print("==========================================================")
    print()
    d = cdaw.get_datasets(mission_list, instrument_list)
    print("Datasets: " + str(d))
    print()
    print("==========================================================")
    print()
    f = cdaw.get_filenames(dataset, t0, t1)
    print("Files: " + str(f))
    print()
    print("==========================================================")
    print()
    del cdaw

# Run the example code
# ex_cdasws()
