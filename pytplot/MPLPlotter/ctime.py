import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from matplotlib.lines import Line2D
from matplotlib.backend_bases import KeyEvent
from matplotlib.pyplot import rcParams

class TimeSelector:

    def add_selection_line(self,time):
        for item in self.axis_list:
            ax, y_bottom, y_top = item
            # Get the y-axis range
            vline = Line2D([time,time], [y_bottom, y_top], color='b', linestyle='--')
            self.selected_lines.append(vline)
            ax.add_line(vline)

    def clear_selection_lines(self):
        for vline in self.selected_lines:
            vline.set_color('r')
            vline.remove()
        plt.draw()
        self.selected_lines.clear()


    # Define the motion event handler
    def ctime_on_motion(self, event):
        if event.inaxes:  # Check if the mouse is over the plot's axes
            # Get the current x-position of the cursor (time)
            cursor_time = event.xdata
            # Update the vertical line position
            for vline in self.vertical_lines:
                vline.set_xdata([cursor_time, cursor_time])
            plt.draw()


    # Define the click event handler
    def ctime_on_click(self, event):

        if event.inaxes:  # Check if the click is within the plot's axes
            if event.button == 1:  # Left-click to add a timestamp, or shift-left-click to clear timestamps
                if self.shift_on:
                    self.clear_selection_lines()
                    self.selected_times.clear()
                    self.logs.append("shift left click")
                else:
                    # Convert the x-coordinate (time) to a datetime
                    self.logs.append("left click")
                    timestamp = mdates.num2date(event.xdata).timestamp()
                    self.selected_times.append(timestamp)
                    self.add_selection_line(event.xdata)
                plt.draw()
            elif event.button == 3:  # Right-click to stop
                self.logs.append("right click")
                plt.disconnect(self.cid)  # Disconnect the event handler
                plt.disconnect(self.motion_cid)  # Disconnect motion event handler
                plt.disconnect(self.kbd_on_cid)  # Disconnect kbd event handler
                plt.disconnect(self.kbd_off_cid)  # Disconnect kbd event handler
                for vline in self.vertical_lines:
                    vline.remove()  # Remove the vertical line from the plot
                plt.draw()
                self.saved_fig.canvas.stop_event_loop()

    # Define the key press event handler
    def ctime_on_key(self, event: KeyEvent):

        self.logs.append("key pressed: " + event.key)
        if event.key == 'c' or event.key == 'e':  # Check if 'c' was pressed
            #print("Pressed 'c', clearing selections")
            self.clear_selection_lines()
            self.selected_times.clear()
            plt.draw()
        elif event.key == 'shift':
            self.shift_on=True
        elif event.key == 'q':  # Check if 'q' was pressed
            #print("Pressed 'q', quitting...")
            plt.disconnect(self.cid)  # Disconnect the event handler
            plt.disconnect(self.motion_cid)  # Disconnect motion event handler
            plt.disconnect(self.kbd_on_cid)  # Disconnect kbd event handler
            plt.disconnect(self.kbd_off_cid)  # Disconnect kbd event handler
            for vline in self.vertical_lines:
                vline.remove()  # Remove the vertical line from the plot
            plt.draw()
            self.saved_fig.canvas.stop_event_loop()
            #clear_selection_lines()

    # Define the key release event handler
    def ctime_off_key(self, event: KeyEvent):
        self.logs.append("key released")
        if event.key == 'shift':
            self.shift_on=False

    def ctime_run_event_loop(self):
        # matplotlib defines some default keyboard commands for manipulating plots.  In particular,
        # 'c' is assigned to "navigate backward", and 'q' is assigned to "close the plot".  We want
        # to redefine these as "clear selections" and "quit ctime", then restore the original definitions
        # upon exit.
        #
        # This only works if the user hasn't redefined 'c' and 'q' to mean something else.
        # The correct way to do this would be to go through all the keymap.* keys, delete 'c' or 'q' from them,
        # then restore the whole map at the end.  This is probably good enough for now.
        #

        save_back = rcParams['keymap.back']
        save_quit = rcParams['keymap.quit']
        rcParams['keymap.back'] = []
        rcParams['keymap.quit'] = []

        #plt.draw()
        #plt.show(block=False)
        # plt.ioff()
        self.saved_fig.canvas.start_event_loop(-1)

        # Restore original keyboard shortcuts
        rcParams['keymap.back'] = save_back
        rcParams['keymap.quit'] = save_quit

        return self.selected_times

    def __init__(self, fig):
        """Initialize."""
        self.saved_fig = fig
        self.selected_times = []
        self.selected_lines = []
        self.vertical_lines = []
        self.axis_list = []
        self.cid = None
        self.motion_cid = None
        self.kbd_on_cid = None
        self.kbd_off_cid = None
        self.shift_on = False
        self.logs = []

        # Create vertical lines in each subplot to track the cursor position
        for ax in fig.axes:
            # Get the y-axis range
            y_bottom, y_top = ax.get_ylim()
            vline = Line2D([0, 0], [y_bottom, y_top], color='g', linestyle='--')
            self.vertical_lines.append(vline)
            ax.add_line(vline)
            self.axis_list.append((ax, y_bottom, y_top))

        # Connect the motion event to the handler
        self.motion_cid = fig.canvas.mpl_connect('motion_notify_event', self.ctime_on_motion)

        # Connect the click event to the handler
        self.cid = fig.canvas.mpl_connect('button_press_event', self.ctime_on_click)

        # Connect the key press/release events to the handler
        self.kbd_on_cid = fig.canvas.mpl_connect('key_press_event', self.ctime_on_key)
        self.kbd_off_cid = fig.canvas.mpl_connect('key_release_event', self.ctime_off_key)


def ctime(fig):
    """ Select time values by clicking on a plot, similar to ctime in IDL SPEDAS

    Left click saves the time at the current cursor position.  'c', 'e', or shift-left click clears the list of times selected. Right click or 'q' exits and returns the list
    of saved times (as floating point Unix times).

    Parameters
    ----------
    fig
        A matplotlib fig object specifying the plot to be used for the time picker (returned by tplot with return_plot_objects=True)

    Notes
    ------
    This feature is very platform-dependent, and should still be considered experimental.  Please let the PySPEDAS developers know
    if you have trouble using it in your environment.

    As of this release, ctime seems to work in most situations, except for Jupyter notebooks using the 'ipympl' (aka 'widget')
    matplotlib backend.  With that backend, the most common failure modes are that the ctime() call returns immediately, with no
    chance to interact with the plot, or the tplot call gets stuck somehow and never renders the plot.

    We are working on a fix for the ipympl incompatibility, but for now, the best workaround for Jupyter notebooks may be to use "%matplotlib auto"
    as the backend.  Depending on your exact environment, this will probably render the plots outside of the Jupyter notebooks (so the plot results
    won't be saved in the notebook), but at least ctime should work, allowing you to continue with your desired workflow.

    Returns
    -------
    list of double
        The selected times as floating point Unix times (in seconds)

    Examples
    --------

    >>> import pyspedas
    >>> from pyspedas import tplot, ctime, time_string
    >>> pyspedas.projects.themis.state(probe='a')
    >>> myfig, ax = tplot('tha_pos', return_plot_objects=True)
    >>> saved_timestamps = ctime(myfig)
    >>> print(time_string(saved_timestamps))

    """
    ctime_obj = TimeSelector(fig)
    print("Use the mouse to select times.  Left click to add a new time, type 'c' to clear selections, 'q' or right click to exit")
    selected_times = ctime_obj.ctime_run_event_loop()
    return selected_times

