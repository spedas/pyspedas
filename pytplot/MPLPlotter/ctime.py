import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from functools import partial
from pytplot import time_string
from matplotlib.lines import Line2D
from matplotlib.backend_bases import KeyEvent
import numpy as np
import sys

# Store selected times
selected_times = []
vertical_lines = []
cid = None
motion_cid = None
kbd_cid = None

# Manage the lines to mark the selections

# list of tuples (ax, ylower, yupper)
axis_list = []
selected_lines = []

def add_selection_line(time):
    for item in axis_list:
        ax, y_bottom, y_top = item
        # Get the y-axis range
        vline = Line2D([time,time], [y_bottom, y_top], color='b', linestyle='--')
        selected_lines.append(vline)
        ax.add_line(vline)

def clear_selection_lines():
    for vline in selected_lines:
        vline.remove()
    plt.draw()
    selected_lines.clear()


# Define the motion event handler
def on_motion(event):
    if event.inaxes:  # Check if the mouse is over the plot's axes
        # Get the current x-position of the cursor (time)
        cursor_time = event.xdata
        # Update the vertical line position
        for vline in vertical_lines:
            vline.set_xdata([cursor_time, cursor_time])
        plt.draw()


# Define the click event handler
def ctime_on_click(ax, cid, event):
    global selected_times
    global vertical_lines

    if event.inaxes:  # Check if the click is within the plot's axes
        if event.button == 1:  # Left-click to add a timestamp
            # Convert the x-coordinate (time) to a datetime
            clicked_time = event.xdata
            timestamp = mdates.num2date(event.xdata).timestamp()
            timestamp_str = time_string(timestamp)
            selected_times.append(timestamp)
            #print(f"Selected Time: {timestamp_str}")
            add_selection_line(event.xdata)
            #ax.plot(clicked_time, event.ydata, 'ro')  # Mark the selected point with a red dot
            plt.draw()
        elif event.button == 3:  # Right-click to stop
            #print("Right-click: Ending selection.")
            plt.disconnect(cid)  # Disconnect the event handler
            plt.disconnect(motion_cid)  # Disconnect motion event handler
            plt.disconnect(kbd_cid)  # Disconnect kbd event handler
            for vline in vertical_lines:
                vline.remove()  # Remove the vertical line from the plot
            #clear_selection_lines()
            #print(f"Selected Times: {selected_times}")
            plt.draw()
            plt.FigureCanvasBase.stop_event_loop()

# Define the key press event handler
def on_key(event: KeyEvent):
    if event.key == 'c':  # Check if 'q' was pressed
        #print("Pressed 'c', clearing selections")
        clear_selection_lines()
        selected_times.clear()

    if event.key == 'q':  # Check if 'q' was pressed
        #print("Pressed 'q', quitting...")
        plt.disconnect(cid)  # Disconnect the event handler
        plt.disconnect(motion_cid)  # Disconnect motion event handler
        plt.disconnect(kbd_cid)  # Disconnect kbd event handler
        for vline in vertical_lines:
            vline.remove()  # Remove the vertical line from the plot
        plt.draw()
        plt.FigureCanvasBase.stop_event_loop()
        #clear_selection_lines()


def ctime(fig):
    """ Select time values by clicking on a plot, similar to ctime in IDL SPEDAS

    Left click saves the time at the current cursor position.  'c' clears the list of times selected. Right click or 'q' exits and returns the list
    of saved times (as floating point Unix times).

    Parameters
    ----------
    fig
        A matplotlib fig object specifying the plot to be used for the time picker (returned by tplot with return_plot_objects=True)

    Notes
    ------

    When using this tool in an interactive Jupyter notebook, there are a few factors that might affect the operation
    of ctime() in that environment.  You will need to specify an interactive backend, by using the "magic" commands
    "%matplotlib widget" or "%matplotlib notebook" prior to importing or calling any pyspedas, pytplot, or matplotlib
    routines.  These commands may require additional packages to be installed (for example, 'ipympl'). It is probably best to do the initial plot and the ctime() call in the same Jupyter cell.

    In a Jupyter environment, calling ctime() can result in a second copy of the plot, which can be confusing.  You can
    prevent this by using the "display=False" keyword on the initial tplot call. The plot will show as soon as ctime()
    is called.

    Some IDEs, like PyCharm Professional, have the ability to host a Jupyter session directly in the
    IDE, rather than in an external browser.  If this causes issues with ctime(), try opening the notebook using the
    standard "jupyter notebook" command rather than using the IDE's built-in Jupyter support.

    The most common failure mode
    of ctime() seems to be an immediate return of an empty time list, while the plot acts as if ctime is still running (time bars
    following the mouse, selection marks appearing and being cleared as expected, etc.  If this happens, please
    try the suggestions above, or let the developers know by opening a Github issue with a description of your
    environment, and some sample code showing what you're trying to do.

    Returns
    -------
    list of double
        The selected times as floating point Unix times (in seconds)

    Examples
    --------

    >>> import pyspedas
    >>> from pyspedas import tplot, ctime, time_string
    >>> pyspedas.projects.themis.state(probe='a')
    >>> fig, ax = tplot('tha_pos', return_plot_objects=True)
    >>> saved_timestamps = ctime(fig)
    >>> print(time_string(saved_timestamps))

    """
    # Reset the selected_times list before starting a new selection
    global selected_times
    global cid
    global motion_cid
    global vertical_lines

    selected_times = []
    vertical_lines = []

    print("Use the mouse to select times.  Left click to add a new time, type 'c' to clear selections, 'q' or right click to exit")

    # Create vertical lines in each subplot to track the cursor position
    for ax in fig.axes:
        # Get the y-axis range
        y_bottom, y_top = ax.get_ylim()
        vline = Line2D([0, 0], [y_bottom, y_top], color='g', linestyle='--')
        vertical_lines.append(vline)
        ax.add_line(vline)
        axis_list.append( (ax, y_bottom, y_top))

    # We only need to attach the event handlers to one axis (otherwise the handlers will trigger
    # multiple times on each event).  We also could have attached them to the figure rather than an axis.
    # Arbitrarily choose the first panel.

    # Use partial to pass ax and cid to on_click
    on_click_with_ax_and_cid = partial(ctime_on_click, fig.axes[0])

    # Connect the motion event to the handler
    motion_cid = fig.canvas.mpl_connect('motion_notify_event', on_motion)

    # Connect the click event to the handler
    cid = fig.canvas.mpl_connect('button_press_event', lambda event: on_click_with_ax_and_cid(cid, event))

    # Connect the key press event to the handler
    kbd_cid = fig.canvas.mpl_connect('key_press_event', on_key)
    # Show the plot and block the execution until right-click ends selection

    #plt.draw()
    #plt.show(block=True)
    plt.FigureCanvasBase.start_event_loop()

    #print("Exiting ctime")
    # The function returns selected times after the user has finished
    return selected_times
