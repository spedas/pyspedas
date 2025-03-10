import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from functools import partial
from pytplot import time_string
from matplotlib.lines import Line2D
import numpy as np

# Store selected times
selected_times = []
vertical_lines = []
cid = None
motion_cid = None

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
            print(f"Selected Time: {timestamp_str}")
            #ax.plot(clicked_time, event.ydata, 'ro')  # Mark the selected point with a red dot
            plt.draw()
        elif event.button == 3:  # Right-click to stop
            print("Right-click: Ending selection.")
            plt.disconnect(cid)  # Disconnect the event handler
            plt.disconnect(motion_cid)  # Disconnect motion event handler
            for vline in vertical_lines:
                vline.remove()  # Remove the vertical line from the plot
            print(f"Selected Times: {selected_times}")



def ctime(fig):
    """ Select time values by clicking on a plot, similar to ctime in IDL SPEDAS

    Left click saves the time at the current cursor position.  Right click exits and returns the list
    of saved times.

    Parameters
    ----------
    fig
        A matplotlib fig object specifying the plot to be used for the time picker (returned by tplot with return_plot_objects=True)

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

    print("Use the mouse to select times.  Left click to add a new time, right click to exit")

    # Create vertical lines in each subplot to track the cursor position
    for ax in fig.axes:
        # Get the y-axis range
        y_bottom, y_top = ax.get_ylim()
        vline = Line2D([0, 0], [y_bottom, y_top], color='g', linestyle='--')
        vertical_lines.append(vline)
        ax.add_line(vline)

    # We only need to attach the event handlers to one axis (otherwise the handlers will trigger
    # multiple times on each event).  We also could have attached them to the figure rather than an axis.
    # Arbitrarily choose the first panel.

    # Use partial to pass ax and cid to on_click
    on_click_with_ax_and_cid = partial(ctime_on_click, fig.axes[0])

    # Connect the motion event to the handler
    motion_cid = fig.canvas.mpl_connect('motion_notify_event', on_motion)

    # Connect the click event to the handler
    cid = fig.canvas.mpl_connect('button_press_event', lambda event: on_click_with_ax_and_cid(cid, event))

    # Show the plot and block the execution until right-click ends selection

    plt.show()

    # The function returns selected times after the user has finished
    return selected_times
