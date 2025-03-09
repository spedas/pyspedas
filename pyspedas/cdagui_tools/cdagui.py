"""
GUI for CDAWeb.

A GUI that can download data files from CDAWeb
and load them into tplot variables.

Requires cdasws.
For cdasws documentation, see:
    https://pypi.org/project/cdasws/
    https://cdaweb.gsfc.nasa.gov/WebServices/REST/py/cdasws/index.html


To open the GUI window:
    from pyspedas import cdagui
    x = cdagui()
To start the gui from the command line, use:
    python pyspedas/cdagui_tools/cdagui.py
"""

import logging
import os
import time
from pyspedas.cdagui_tools.cdaweb import CDAWeb
from pyspedas.cdagui_tools.config import CONFIG
from typing import Optional, Tuple
from types import ModuleType

# Rather than import tkinter unconditionally at the top of the module (possibly leading
# to error messages each time pyspedas is imported), if python isn't built with tkinter included,
# we move those imports into a function that only gets called when someone tries to use the GUI.
# If tkinter isn't available, let the user know that they need a different build of Python
# to use this feature.


def import_tkinter_with_message() -> Tuple[Optional[ModuleType], Optional[ModuleType], Optional[ModuleType]]:
    """Attempt to import tkinter and return the module. If unavailable, log an error message describing the problem. """
    try:
        import tkinter as tk
        from tkinter import messagebox, filedialog
        return tk, messagebox, filedialog
    except ImportError:
        logging.error("The version of Python you are using does not support the tkinter module needed to run the PySPEDAS CDAWeb GUI.")
        logging.error("You may need to reinstall a different version of Python compiled with tkinter support.")
        return None, None, None

class cdaWindow:

     def __init__(self, master):
        tk, messagebox, filedialog = import_tkinter_with_message()
        if tk is None:
            return
        # CDAWeb connection
        cda = CDAWeb()

        # Defaults
        default_start_time = "2023-01-01 00:00:00"
        default_end_time = "2023-01-01 23:59:59"
        download_box = tk.IntVar()
        clip_box = tk.IntVar(value=1)  # start with time clip on
        default_dir = CONFIG["local_data_dir"]
        default_status = "Status: Ready!"

        def status(txt):
            # Change status bar, show wait cursor
            if txt == "":
                status_label.config(text=default_status)
                master.config(cursor="")
            else:
                status_label.config(text="Status: " + str(txt))
                master.config(cursor="wait")
                time.sleep(0.2)

            master.update_idletasks()
            master.update()

        def select_dir():
            # Button: Select dir
            initial_dir = str(dir_entry.get())
            path = filedialog.askdirectory(
                parent=window,
                initialdir=initial_dir,
                title="Please select a directory",
                mustexist=True,
            )
            if os.path.exists(path):
                dir_entry.delete(0, tk.END)
                dir_entry.insert(0, path)

        def clear_boxes():
            # Button: Clear all list boxes
            mission_list.selection_clear(0, tk.END)
            instrument_list.selection_clear(0, tk.END)
            dataset_list.delete(0, tk.END)
            file_list.delete(0, tk.END)
            label_groups.config(text="Selected Mission Groups:")
            label_instruments.config(text="Selected Instrument Types:")

        def exit_gui():
            # Button: Exit
            window.destroy()

        def find_datasets():
            # Button: 1. Find Datasets
            msgtitle = "Find Datasets"

            # Change status
            status(msgtitle + "...")

            datasets = []
            dataset_list.delete(0, tk.END)
            file_list.delete(0, tk.END)
            sel_g = list(mission_list.curselection())
            sel_g_val = [mission_list.get(index) for index in sel_g]
            sel_i = list(instrument_list.curselection())
            sel_i_val = [instrument_list.get(index) for index in sel_i]
            if len(sel_g_val) < 1:
                messagebox.showerror(
                    msgtitle, "Please select one or more Mission Groups!"
                )
            elif len(sel_i_val) < 1:
                messagebox.showerror(
                    msgtitle, "Please select one or more Instrument Types!"
                )
            else:
                label_groups.config(
                    text="Selected Mission Groups: [" + ",".join(sel_g_val) + "]"
                )
                label_instruments.config(
                    text="Selected Instrument Types: [" + ",".join(sel_i_val) + "]"
                )

                datasets = cda.get_datasets(sel_g_val, sel_i_val)
                if len(datasets) < 1:
                    messagebox.showerror(
                        msgtitle, "No datasets found for these parameters!"
                    )
                else:
                    for i in datasets:
                        dataset_list.insert(tk.END, str(i))

            status("")  # Reset status

            return datasets

        def find_filelist():
            # Button: 2. Get File List
            msgtitle = "Get File List"

            # Change status
            status(msgtitle + "...")

            file_list.delete(0, tk.END)
            all_files = []
            sel_d = list(dataset_list.curselection())
            sel_d_val = [dataset_list.get(index) for index in sel_d]
            if len(sel_d_val) < 1:
                messagebox.showerror(msgtitle, "Please select one or more Datasets!")
                status("")  # Reset status
                return []

            t0 = str(start_time.get())
            t1 = str(end_time.get())
            if len(t0) < 1 or len(t1) < 1:
                messagebox.showerror(msgtitle, "Please set start and end time!")
                status("")  # Reset status
                return []

            # Get all files for this dataset and start/end times.
            all_files = cda.get_filenames(sel_d_val, t0, t1)
            filelen = len(all_files)
            if filelen < 1:
                msg = "No files were found with these parameters."
                messagebox.showinfo(msgtitle, msg)
                status("")  # Reset status
                return []
            elif filelen > 50:
                msg = "Number of files found: " + str(filelen)
                msg += "\nOnly 50 will be shown."
                messagebox.showinfo(msgtitle, msg)

            # Add filenames to listbox (up to 50 files)
            for i in all_files[:50]:
                file_list.insert(tk.END, str(i))

            status("")  # Reset status

            # Return all files, even if they are more than 50
            return all_files

        def get_data():
            # Button: 3. Get Data
            msgtitle = "Get Data"

            # Change status
            status(msgtitle + "...")

            file_result = []
            sel_f = list(file_list.curselection())
            sel_f_val = [file_list.get(index) for index in sel_f]
            if len(sel_f_val) < 1:
                messagebox.showerror(
                    msgtitle, "Please select one or more files to download!"
                )
                status("")  # Reset status
                return []

            if download_box.get() == 1:
                download_only = True
            else:
                download_only = False
            if clip_box.get() == 1:
                time_clip = True
            else:
                time_clip = False

            local_dir = str(dir_entry.get())
            if len(local_dir) < 1:
                local_dir = default_dir
                dir_entry.insert(0, default_dir)

            # Get the files, and/or the tplot variables
            # sesults is a list [remote filename, local filename, status]
            trange = [str(start_time.get()), str(end_time.get())]
            result = cda.cda_download(
                sel_f_val,
                local_dir,
                download_only=download_only,
                trange=trange,
                time_clip=time_clip,
            )
            no_of_files, no_of_variables, loaded_vars = result

            # Show a message about the results
            logging.info(loaded_vars)
            msg = "Results:\n"
            msg += "\nDownloaded files: " + str(no_of_files)
            msg += "\ntplot variables created: " + str(no_of_variables)
            messagebox.showinfo(msgtitle, msg)
            
            status("")  # Reset status
            return loaded_vars

        # Create the main window
        window = master
        window.title("CDAWeb Data Downloader")
        window.geometry("800x600")
        window.configure()
        window.option_add("*font", "lucida 10")
        window.state("zoomed")  # Start maximazed
        window.minsize(800, 600)

        # Size of grid
        no_of_cols = 2
        no_of_rows = 14

        # Create columns
        for i in range(no_of_cols):
            window.grid_columnconfigure(i, weight=1)

        # Create rows
        for i in range(no_of_rows):
            window.grid_rowconfigure(i, weight=1)

        # Row 0 - just a label
        window.grid_rowconfigure(0, weight=0)
        label00 = tk.Label(
            window,
            text="Download Data from CDAWeb",
            bg="#AFEEEE",
            font=("Helvetica", 10, "bold"),
        )
        label00.grid(row=0, columnspan=2, sticky="new")

        # Row 1, 2 - Mission Groups and Instrument Types
        window.grid_rowconfigure(1, weight=0)
        label10 = tk.Label(window, text="Mission Groups:")
        label10.grid(row=1, column=0, sticky="ws")

        label11 = tk.Label(window, text="Instrument Types:")
        label11.grid(row=1, column=1, sticky="ws")

        cell20 = tk.Frame(window)
        cell20.grid(row=2, column=0, sticky="nsew")
        mission_list = tk.Listbox(cell20, selectmode=tk.MULTIPLE, exportselection=False)
        mission_list.pack(
            side=tk.TOP, fill=tk.BOTH, padx=5, pady=5, ipadx=5, ipady=5, expand=True
        )
        cdagroups = cda.get_observatories()
        # cdagroups = [i for i in range(200)]
        for g in cdagroups:
            mission_list.insert(tk.END, str(g))
        scrollbar20 = tk.Scrollbar(mission_list, orient="vertical")
        scrollbar20.pack(side=tk.RIGHT, fill=tk.BOTH)
        mission_list.config(yscrollcommand=scrollbar20.set)
        scrollbar20.config(command=mission_list.yview)

        cell21 = tk.Frame(window)
        cell21.grid(row=2, column=1, sticky="nsew")
        instrument_list = tk.Listbox(
            cell21, selectmode=tk.MULTIPLE, exportselection=False
        )
        instrument_list.pack(
            side=tk.TOP, fill=tk.BOTH, padx=5, pady=5, ipadx=5, ipady=5, expand=True
        )
        cdainstr = cda.get_instruments()
        # cdainstr = [i for i in range(200)]
        for i in cdainstr:
            instrument_list.insert(tk.END, str(i))
        scrollbar21 = tk.Scrollbar(instrument_list, orient="vertical")
        scrollbar21.pack(side=tk.RIGHT, fill=tk.BOTH)
        instrument_list.config(yscrollcommand=scrollbar21.set)
        scrollbar21.config(command=instrument_list.yview)

        # Row 3 - Find Datasets button
        window.grid_rowconfigure(3, weight=0)
        msg = "Select Mission Group(s) and Instrument Type(s) and press:"
        label30 = tk.Label(window, text=msg)
        label30.grid(row=3, column=0, sticky="nse")

        button31 = tk.Button(
            window,
            text="1. Find Datasets",
            bg="#AFEEAF",
            command=find_datasets,
            width=30,
        )
        button31.grid(row=3, column=1, sticky="nsw")

        # Row 4 - Dataset labels
        window.grid_rowconfigure(4, weight=0)
        cell40 = tk.Frame(window)
        cell40.grid(row=4, columnspan=2, sticky="new")
        for i in range(3):
            cell40.grid_rowconfigure(i, weight=1)
        cell40.grid_columnconfigure(0, weight=1)
        label_groups = tk.Label(
            cell40, text="Selected Mission Groups:", justify="left", anchor="w"
        )
        label_groups.grid(row=0, sticky="new")
        label_instruments = tk.Label(
            cell40, text="Selected Instrument Types:", justify="left", anchor="w"
        )
        label_instruments.grid(row=1, sticky="new")
        label_2 = tk.Label(cell40, text="Datasets:", justify="left", anchor="w")
        label_2.grid(row=2, sticky="new")

        # Row 5 - Datasets
        cell50 = tk.Frame(window)
        cell50.grid(row=5, columnspan=2, sticky="nsew")
        dataset_list = tk.Listbox(cell50, selectmode=tk.MULTIPLE, exportselection=False)
        dataset_list.pack(
            side=tk.TOP, fill=tk.BOTH, padx=5, pady=5, ipadx=5, ipady=5, expand=True
        )
        scrollbar50 = tk.Scrollbar(dataset_list, orient="vertical")
        scrollbar50.pack(side=tk.RIGHT, fill=tk.BOTH)
        dataset_list.config(yscrollcommand=scrollbar50.set)
        scrollbar50.config(command=dataset_list.yview)

        # Row 6, 7 - Date Time
        window.grid_rowconfigure(6, weight=0)
        label60 = tk.Label(
            window,
            text="Date and Time (format: YYYY-MM-DD[ HH:MM:SS])",
            justify="left",
            anchor="w",
        )
        label60.grid(row=6, columnspan=2, sticky="new")

        window.grid_rowconfigure(7, weight=0)
        cell70 = tk.Frame(window)
        cell70.grid(row=7, column=0, sticky="new")
        cell70.grid_rowconfigure(0, weight=1)
        cell70.grid_columnconfigure(0, weight=0)
        cell70.grid_columnconfigure(1, weight=1)
        cell70.grid_columnconfigure(2, weight=0)
        label70 = tk.Label(cell70, text="Start Time:", justify="left", anchor="w")
        label70.grid(row=0, column=0, sticky="wsn")
        start_time = tk.Entry(cell70)
        start_time.insert(0, default_start_time)
        start_time.grid(row=0, column=1, sticky="ewsn", padx=6)

        cell71 = tk.Frame(window)
        cell71.grid(row=7, column=1, sticky="new")
        cell71.grid_rowconfigure(0, weight=1)
        cell71.grid_columnconfigure(0, weight=0)
        cell71.grid_columnconfigure(1, weight=1)
        cell71.grid_columnconfigure(2, weight=0)
        label71 = tk.Label(cell71, text="End Time:", justify="left", anchor="w")
        label71.grid(row=0, column=0, sticky="wsn")
        end_time = tk.Entry(cell71)
        end_time.insert(0, default_end_time)
        end_time.grid(row=0, column=1, sticky="sewn", padx=6)

        # Row 8 - Get File List button
        window.grid_rowconfigure(8, weight=0)
        msg = "Select Dataset(s) and Times and press:"
        label80 = tk.Label(window, text=msg)
        label80.grid(row=8, column=0, sticky="nse", pady=6)

        button81 = tk.Button(
            window,
            text="2. Get File List",
            bg="#AFEEAF",
            command=find_filelist,
            width=30,
        )
        button81.grid(row=8, column=1, sticky="nsw", pady=6)

        # Row 9, 10 - Files
        window.grid_rowconfigure(9, weight=0)
        label90 = tk.Label(window, text="Remote Files:", justify="left", anchor="w")
        label90.grid(row=9, columnspan=2, sticky="new")

        cell100 = tk.Frame(window)
        cell100.grid(row=10, columnspan=2, sticky="nsew")
        file_list = tk.Listbox(cell100, selectmode=tk.MULTIPLE, exportselection=False)
        file_list.pack(
            side=tk.TOP, fill=tk.BOTH, padx=5, pady=5, ipadx=5, ipady=5, expand=True
        )
        scrollbar100 = tk.Scrollbar(file_list, orient="vertical")
        scrollbar100.pack(side=tk.RIGHT, fill=tk.BOTH)
        file_list.config(yscrollcommand=scrollbar100.set)
        scrollbar100.config(command=file_list.yview)

        # Row 11 - Download Directory
        window.grid_rowconfigure(11, weight=0)
        cell110 = tk.Frame(window)
        cell110.grid(row=11, columnspan=2, sticky="new")
        cell110.grid_columnconfigure(0, weight=0)
        cell110.grid_columnconfigure(1, weight=1)
        cell110.grid_columnconfigure(2, weight=0)

        label110 = tk.Label(
            cell110, text="Local Directory:", justify="left", anchor="w"
        )
        label110.grid(row=0, column=0, sticky="new", padx=4)
        dir_entry = tk.Entry(cell110)
        dir_entry.insert(0, default_dir)
        dir_entry.grid(row=0, column=1, sticky="sewn", padx=4)
        # dir_entry.bind("<Key>", lambda e: "break")  # Make it read-only
        button110 = tk.Button(
            cell110, text="Select Directory", command=select_dir, width=15
        )
        button110.grid(row=0, column=2, sticky="wns", padx=4)

        # Row 12 - Download Only checkbox, Get Data button, Clear, Exit
        window.grid_rowconfigure(12, weight=0)

        cell120 = tk.Frame(window)
        cell120.grid(row=12, column=0, sticky="new", pady=4)
        cell120.grid_columnconfigure(0, weight=0)
        cell120.grid_columnconfigure(1, weight=0)
        cell120.grid_columnconfigure(2, weight=1)
        cell120.grid_columnconfigure(3, weight=0)
        only_ch = tk.Checkbutton(
            cell120,
            text="Download Only",
            variable=download_box,
            onvalue=1,
            offvalue=0,
        )
        only_ch.grid(row=0, column=0, sticky="new", padx=4)
        clip_ch = tk.Checkbutton(
            cell120,
            text="Time Clip",
            variable=clip_box,
            onvalue=1,
            offvalue=0,
        )
        clip_ch.grid(row=0, column=1, sticky="new", padx=4, ipadx=0)
        msg = "Select Files(s) and press:"
        label120 = tk.Label(cell120, text=msg)
        label120.grid(row=0, column=2, sticky="nse", pady=6)

        cell121 = tk.Frame(window)
        cell121.grid(row=12, column=1, sticky="new", pady=4)
        cell121.grid_columnconfigure(0, weight=0)
        cell121.grid_columnconfigure(1, weight=1)
        cell121.grid_columnconfigure(2, weight=0)
        cell121.grid_columnconfigure(3, weight=0)
        button122 = tk.Button(
            cell121, text="3. Get Data", bg="#AFEEAF", command=get_data, width=30
        )
        button122.grid(row=0, column=0, sticky="wns", padx=4)
        button123 = tk.Button(
            cell121, text="Clear", command=clear_boxes, width=10, bg="#E9967A"
        )
        button123.grid(row=0, column=2, sticky="wns", padx=4)
        button124 = tk.Button(
            cell121, text="Exit", command=exit_gui, width=10, bg="#E9967A"
        )
        button124.grid(row=0, column=3, sticky="wns", padx=4)

        # Row 13 - Status bar
        window.grid_rowconfigure(13, weight=0)
        status_label = tk.Label(
            window, text=default_status, justify="left", anchor="w", relief="groove"
        )
        status_label.grid(row=13, columnspan=2, sticky="new", padx=2)


def cdagui():
    tk, messagebox, filedialog = import_tkinter_with_message()
    if tk is not None:
        root = tk.Tk()
        startgui = cdaWindow(root)
        root.mainloop()
        return startgui


if __name__ == "__main__":
    tk, messagebox, filedialog = import_tkinter_with_message()
    if tk is not None:
        root = tk.Tk()
        startgui = cdaWindow(root)
        root.mainloop()
