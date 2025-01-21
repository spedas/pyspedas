Getting Started
====================================



Requirements
--------------
PySPEDAS supports Windows, macOS and Linux.

At this writing (January 2025), PySPEDAS is compatible with Python versions 3.9 through 3.12.

The following installation guide represents a somewhat minimal approach to getting a working PySPEDAS
installation.   It assumes you are starting from scratch, with no pre-existing Python version or developer tools installed.
More advanced users might wish to make different choices of Python distributions (e.g. anaconda rather than
python.org), or use a different development environment (e.g Spyder, Visual Studio Code, or some other
environment rather than PyCharm Community Edition).  The installation details might differ slightly for
various operating systems or choices of Python distribution or development environment, but the general
order of operations should be simple and straightforward.

Installing Python
-----------------

You will need to install a compatible version of Python on your system (even if one is pre-installed with the
operating system, it is not recommended to use it for PySPEDAS.  There is no issue having multiple Python
versions or installations on the same machine).

We recommend installing Python 3.12 from https://python.org/downloads .

Note that the latest available Python release is 3.13, and this is what the page will offer
to download by default, but PySPEDAS isn't yet compatible with this release.  Scroll
down to the section entitled "Looking for a specific release?", find the entry for Python 3.12
(whatever minor release is current -- Python 3.12.8 as of this writing), click the "Download" button
for it, then open the installer and follow the instructions.  You should probably accept the defaults
for any installation options that appear.  More detailed instructions for your platform are
available from https://docs.python.org/3/using/index.html .

Installing PyCharm Community Edition
------------------------------------

PyCharm (Community Edition) is a free-to-use interactive development environment for Python.
This is the main tool you will use to interact with Python and PySPEDAS.

The software can be downloaded and installed from https://www.jetbrains.com/pycharm/download/ .
Scoll down past the "PyCharm Professional" downloader (which requires a paid license) and choose
the "PyCharm Community Edition" download.  After completing the download, click on the installer and
follow the prompts.  Near the end of the installation (depending on your operating system), you may come to a screen with some
options: "64-bit launcher", "Open folder as project", ".py file associations", "Add launchers dir to the PATH".
We recommend selecting all these options.

You may need to restart your machine to finalize the installation.

More PyCharm installation instructions are available at https://www.jetbrains.com/help/pycharm/installation-guide.html

Set PySPEDAS environment variables
----------------------------------

By default, the data is stored in your pyspedas directory in a folder named 'pydata'. This is probably not what you want.

The recommended way of setting your local data directory is to set the **SPEDAS_DATA_DIR** environment variable. **SPEDAS_DATA_DIR** acts as a root data directory for all missions,
and will also be used by IDL (if you’re running a recent copy of the bleeding edge).  If you already use IDL SPEDAS, and have
**SPEDAS_DATA_DIR** set in your environment, no further action is needed.

You should set **SPEDAS_DATA_DIR** to a folder where you have write access, preferably on your hard drive rather than
a network drive or mount point, on a filesystem which has enough free space to accomodate many gigabytes of
downloaded data.  It's probably best to create that top-level folder by hand, if it doesn't already exist. (Any needed subdirectories
will be created automatically by SPEDAS or PySPEDAS).  For example, you might use "C:\\spedas_data" on Windows to put it
at the root of your hard drive, or "/Users/your_userid/spedas_data" on a Mac to put it under your home directory.

Once you've decided where to put your data directory, you need to ensure that the **SPEDAS_DATA_DIR** environment
variable is set whenever you log in. On Mac or Linux, this can be done by adding a line to your
shell startup files (e.g. .cshrc, .zshrc, .bashrc or whatever shell you use):

setenv SPEDAS_DATA_DIR /path/to/data/directory

On Windows, you can open the Windows settings, search for "environment variables",
go the the appropriate control panel, and add the SPEDAS_DATA_DIR environment variable to your
user environment variable settings.

You may need to log out of your account and log back in so these changes take effect.

Create a Python project in PyCharm
----------------------------------

You will need to create a Python project and "virtual environment", which is where you'll
install pyspedas and some other tools you'll need.

You should have an icon for PyCharm on your desktop or start menu.  Use it to open PyCharm.

Instructions for creating a new PyCharm project and environment can be found here:
https://www.jetbrains.com/help/pycharm/creating-and-running-your-first-python-project.html
The default name for your project will probably be something like "pythonProject" under
a "PycharmProjects" folder...feel free to change that to a name like "pyspedas_project".

This step may take several minutes, as it sets up a new Python virtual environment, copies the
necessary files into it, and indexes them.  At the bottom of your PyCharm window, there
should be a status area and progress bar showing what it's doing.

The section in the "Creating and running your first Python project" page entitled
"Create a Python file", and everything below it, are optional at this point (though it doesn't hurt to try).

Install PySPEDAS and some related packages
------------------------------------------

You will now need to install PySPEDAS in the environment you've just created.
This will be done in the PyCharm terminal window.  On the left side of the PyCharm window,
there should be a stack of icons near the bottom.  Hover over them until you find the one
labeled "Terminal", and open it.   You can also get to this with View->Tool Windows->Terminal

To install the pyspedas package using PyPI:

.. code-block:: bash

   pip install pyspedas


In the future, to upgrade to the latest version of pySPEDAS, include the '--upgrade' option when calling pip, e.g.,

.. code-block:: bash

   pip install pyspedas --upgrade

This will start the installation of the PySPEDAS package, along with various other packages that it depends on.
This may take quite a while, depending on your internet connection speed and hard drive speed.  Keep an eye on the
status area and progress bar at the bottom of the PyCharm window to see what it's doing.
Eventually, you should see a message that pyspedas (and probably many other packages) were successfully installed.

There are a few other packages that are not installed by default alongside pyspedas.
The spacepy, basemap, and mth5 packages are optional dependencies that are needed to support
the MMS mission, SECS and EICS plots, and MTH5 magnetometer station data.
To install:

.. code-block:: bash

   pip install spacepy
   pip install basemap
   pip install mth5

Many PySPEDAS examples are distributed as jupyter notebooks, so you will probably
want the "jupyter" package:

.. code-block:: bash

   pip install jupyter

Try a simple PySPEDAS workflow
------------------------------

You should now be ready to run some code using PySPEDAS!  Here's a quick demo to try.

In the upper left pane of the PyCharm window, there should be a file tree showing
the PyCharm project you've created (let's say it was "pyspedas_project".  If it's not
showing, look for a "folder" icon in the upper left, and click on it.

Click on the "pyspedas_project" entry in the directory tree to select it.
Then click on "File->New..." and choose "Python File" from the list of options.
Name it "pyspedas_demo.py".   It should open in an editing pane in the upper left of the
PyCharm window.

Now copy and paste this demo code into the editing pane:

.. code-block:: python

    # Load and plot THEMIS FGM data
    def pyspedas_demo():
        # Import pyspedas routines to be used
        from pyspedas import tplot
        from pyspedas.projects.themis import fgm

        # Set the time range: 2007-03-23, complete day
        trange=['2007-03-23' , '2007-03-24']
        # Load THEMIS FGM data for probe A
        fgm_vars = fgm(probe='a',trange=trange)
        # Print the list of tplot variables just loaded
        print(fgm_vars)
        # Plot the 'tha_fgl_dsl' variable
        tplot('tha_fgl_dsl')

    # Run the example code
    if __name__ == '__main__':
        pyspedas_demo()

If all goes well you should see a green triangle just to the left of the "if __name__ == '__main' line
of code.  (If not, look for any red squiggles indicating syntax errors or other issues in the
demo program).

Click on the green triangle and select "Run pyspedas_demo".  This should
run the example program,  In the "Run" pane on the bottom half of the PyCharm window,
you should see some output as pyspedas downloads THEMIS data, and prints the tplot
variables loaded.  A plot should appear, showing a plot for "tha_fgl_dsl".

If you got this far, congratualations! You are now ready to write your own programs
using PySPEDAS!
