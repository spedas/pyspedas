import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pytplot import time_string
from matplotlib.lines import Line2D
from matplotlib.backend_bases import KeyEvent


# Store selected times
selected_times = []
vertical_lines = []
cid = None
motion_cid = None
kbd_on_cid = None
kbd_off_cid = None
logs=[]

shift_on=False

# Manage the lines to mark the selections

# list of tuples (ax, ylower, yupper)
saved_fig = None
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
    global selected_lines
    print("Clearing selection lines")
    for vline in selected_lines:
        vline.set_color('r')
        vline.remove()
    plt.draw()
    selected_lines.clear()


# Define the motion event handler
def ctime_on_motion(event):
    if event.inaxes:  # Check if the mouse is over the plot's axes
        # Get the current x-position of the cursor (time)
        cursor_time = event.xdata
        # Update the vertical line position
        for vline in vertical_lines:
            vline.set_xdata([cursor_time, cursor_time])
        plt.draw()


# Define the click event handler
def ctime_on_click(event):
    global selected_times
    global vertical_lines
    global logs
    global saved_fig

    if event.inaxes:  # Check if the click is within the plot's axes
        if event.button == 1:  # Left-click to add a timestamp, or shift-left-click to clear timestamps
            if shift_on:
                clear_selection_lines()
                selected_times.clear()
                logs.append("shift left click")
            else:
                # Convert the x-coordinate (time) to a datetime
                logs.append("left click")
                timestamp = mdates.num2date(event.xdata).timestamp()
                selected_times.append(timestamp)
                add_selection_line(event.xdata)
            plt.draw()
        elif event.button == 3:  # Right-click to stop
            logs.append("right click")
            plt.disconnect(cid)  # Disconnect the event handler
            plt.disconnect(motion_cid)  # Disconnect motion event handler
            plt.disconnect(kbd_on_cid)  # Disconnect kbd event handler
            plt.disconnect(kbd_off_cid)  # Disconnect kbd event handler
            for vline in vertical_lines:
                vline.remove()  # Remove the vertical line from the plot
            plt.draw()
            saved_fig.canvas.stop_event_loop()

# Define the key press event handler
def ctime_on_key(event: KeyEvent):
    global logs
    global saved_fig
    global shift_on
    logs.append("key pressed: " + event.key)
    if event.key == 'c' or event.key == 'e':  # Check if 'c' was pressed
        #print("Pressed 'c', clearing selections")
        clear_selection_lines()
        selected_times.clear()
        plt.draw()
    elif event.key == 'shift':
        shift_on=True
    elif event.key == 'q':  # Check if 'q' was pressed
        #print("Pressed 'q', quitting...")
        plt.disconnect(cid)  # Disconnect the event handler
        plt.disconnect(motion_cid)  # Disconnect motion event handler
        plt.disconnect(kbd_on_cid)  # Disconnect kbd event handler
        plt.disconnect(kbd_off_cid)  # Disconnect kbd event handler
        for vline in vertical_lines:
            vline.remove()  # Remove the vertical line from the plot
        plt.draw()
        saved_fig.canvas.stop_event_loop()
        #clear_selection_lines()

# Define the key release event handler
def ctime_off_key(event: KeyEvent):
    global logs
    global shift_on
    logs.append("key released")
    if event.key == 'shift':
        shift_on=False

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
    This feature is very platform-dependent, and should still be considered experimental.  Please let the PySPEDAS developers know
    if you have trouble using it in your environment.

    When using this tool in an interactive Jupyter notebook, there are a few factors that might affect the operation
    of ctime.  You will need to specify an interactive backend, by using the "magic" commands
    "%matplotlib ipympl" (or some other backend appropriate for your environment) prior to importing or calling any pyspedas, pytplot, or matplotlib
    routines.  It is probably best to do the initial plot and the ctime() call in the same Jupyter cell.

    In a Jupyter environment, calling ctime() can result in a second copy of the plot, which can be confusing.  You can
    prevent this by using the "display=False" keyword on the initial tplot call. The plot will show as soon as ctime()
    is called.

    Some IDEs, like PyCharm Professional, have the ability to host a Jupyter session directly in the
    IDE, rather than in an external browser.  If this causes issues with ctime(), try opening the notebook using the
    standard "jupyter notebook" command rather than using the IDE's built-in Jupyter support.

    The most common failure mode
    of ctime() seems to be an immediate return of an empty time list, while the plot acts as if ctime is still running (time bars
    following the mouse, selection marks appearing and being cleared as expected, etc.)  If this happens, please
    try the suggestions above, or let the developers know by opening a GitHub issue with a description of your
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
    global kbd_on_cid
    global kbd_off_cid
    global saved_fig
    global shift_on
    global logs

    saved_fig = fig

    selected_times = []
    vertical_lines = []
    shift_on=False
    logs=[]

    print("Use the mouse to select times.  Left click to add a new time, type 'c' to clear selections, 'q' or right click to exit")

    # Create vertical lines in each subplot to track the cursor position
    for ax in fig.axes:
        # Get the y-axis range
        y_bottom, y_top = ax.get_ylim()
        vline = Line2D([0, 0], [y_bottom, y_top], color='g', linestyle='--')
        vertical_lines.append(vline)
        ax.add_line(vline)
        axis_list.append( (ax, y_bottom, y_top))

    # Connect the motion event to the handler
    motion_cid = fig.canvas.mpl_connect('motion_notify_event', ctime_on_motion)

    # Connect the click event to the handler
    cid = fig.canvas.mpl_connect('button_press_event', ctime_on_click)

    # Connect the key press/release events to the handler
    kbd_on_cid = fig.canvas.mpl_connect('key_press_event', ctime_on_key)
    kbd_off_cid = fig.canvas.mpl_connect('key_release_event', ctime_off_key)

    # Show the plot and block the execution until right-click ends selection

    plt.draw()
    plt.show(block=False)
    #plt.ioff()
    fig.canvas.start_event_loop(-1)

    #print("Exiting ctime")
    # The function returns selected times after the user has finished
    return selected_times

