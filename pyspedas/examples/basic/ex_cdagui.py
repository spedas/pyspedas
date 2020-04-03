
"""
File:
    ex_cdagui.py

Description:
    Example of how to use cdagui.
    Since this is a GUI, we only print the instructions here.
    You have to follow these instructions on a python command line,
        for example the Spyder console in Anaconda.

"""


def ex_cdagui():
    # Import pyspedas
    # Run the following import command in a python command line:
    #     from pyspedas.cdagui.cdagui import cdagui
    print("--- In a command line, type the following import command:")
    print("from pyspedas.cdagui.cdagui import cdagui")
    # Open the cdagui by typing
    #     x = cdagui()
    print("x = cdagui()")
    # In the GUI window, do the following:
    # Select 'ARTEMIS', select 'Electric Fields (space)'
    # Click the button '1. Find Datasets' and a list of datasets shoulw appear.
    print("--- The cda GUI window should open.")
    print("--- Select 'ARTEMIS', 'Electric Fields (space)'\
 and click '1. Find Datasets'.")
    # Select 'THB_L2_FIT' and click the button '2. Get File List'
    print("--- Select 'THB_L2_FIT' and click '2. Get File List'.")
    # Select the filename, unselect 'Download Only'
    # and click the button '3. Get Data'
    print("--- Select the filename, unselect 'Download Only'\
 and click '3. Get Data'.")
    # Click 'Exit' to close the GUI
    print("--- Click 'Exit' to close the GUI.")
    # Type the following on the python command line and press Shift+Enter
    #   import pytplot
    #   pytplot.tplot_names()
    # You should get a list of tplot variables loaded.
    print("--- Type the following on the python command line\
 and press Shift+Enter.")
    print("import pytplot")
    print("pytplot.tplot_names()")
    print("--- You should get the list of loaded tplot variables.")
    # Type the following to create a plot:
    #   pytplot.tplot('thb_fgs_dsl')
    print("--- Type the following to create a plot:")
    print("pytplot.tplot('thb_fgs_dsl')")
    # Remind the user about needing PyQt5
    print()
    print("--- If you encounter problems, try to install the latest PyQt5:")
    print("pip install PyQt5 --upgrade")

    # Return 1 as indication that the example finished without problems.
    return 1

# Run the example code
# ex_cdagui()
