# -*- coding: utf-8 -*-
"""
CDA GUI

Downloads data files from CDAWeb and loads them into pytplot variables.
Requires cdasws, PyQt5.

For cdasws documentation, see:
    https://test.pypi.org/project/cdasws/
    https://cdaweb.sci.gsfc.nasa.gov/WebServices/REST/py/cdasws/index.html

Notes:
    Currently, cdasws is not on the main pypi server.
    pip install -i https://test.pypi.org/simple/ cdasws

    To start the gui from the command line:
        python pyspedas/cdagui/cdagui.py
    To start the gui inside the python environment:
        exec(open('cdagui.py').read())

@author: nikos
"""


import sys
import os
import re
import datetime
import pyspedas
import pytplot
from cdasws import CdasWs
from PyQt5.QtCore import Qt, QDate, QCoreApplication
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow,
                             QGridLayout, QPushButton, QListWidget,
                             QGroupBox, QCheckBox, QMessageBox,
                             QVBoxLayout, QLabel, QLineEdit, QListWidgetItem,
                             QFileDialog, QCalendarWidget, QDialog)


def get_default_data_dir():
    """ Returns the default dowload directory for pyspedas.
    """
    data_dir = ''
    prefs = pyspedas.get_spedas_prefs()
    if 'data_dir' in prefs:
        data_dir = prefs['data_dir'] + 'cdaweb'

    return data_dir


def get_instr():
    """ Returns a list of instrument types.
    """
    cdas = CdasWs()
    instr = cdas.get_instrument_types()
    return instr


def get_observatories():
    """ Returns a list of missions.
    """
    cdas = CdasWs()
    observ = cdas.get_observatory_groups()
    return observ


def get_datasets(mission_list, instrument_list):
    """ Returns a list of datasets given the missions and instruments.
    """
    thisdict = {
        "observatoryGroup": mission_list,
        "instrumentType": instrument_list
    }
    cdas = CdasWs()
    dataset = cdas.get_datasets(**thisdict)

    return dataset


def files_to_download(dataset_list, t0, t1):
    """ Find the list of files for a dataset between dates t0 and t1.
        Return a list of url.
    """
    remote_url = []
    max_files = 50
    cdas = CdasWs()
    title = "Server response"

    # Set times to cdas format
    t0 = t0.strip().replace(' ', 'T', 1) + 'Z'
    t1 = t1.strip().replace(' ', 'T', 1) + 'Z'

    # Find dataset list
    for d in dataset_list:
        d0 = d.split(' ')
        if (len(d0) > 1):
            status, result = cdas.get_data_file(d0[0], [], t0, t1)
            if (status == 200 and (result is not None)):
                r = result.get('FileDescription')
                for f in r:
                    remote_url.append(f.get('Name'))

    # Show a message with the result
    msg = ""
    if (status != 200):
        msg = "There was a problem communicating with the SPDF server.\n"
        msg += "Status code:" + str(status)
    else:
        fcount = len(remote_url)
        if (fcount < 1):
            msg = "No files were found with the selected parameters."
        elif (fcount == 1):
            # msg = "Found 1 file.          "
            msg = ""
        else:
            if (fcount > max_files):
                msg = "Found " + str(fcount) + " files.      "
                remote_url = remote_url[0:max_files]
                msg += ("\nOnly a max of " + str(max_files)
                        + " files can be downloaded.")

    if (msg != ""):
        show_my_message(title, msg)

    ''' # For debugging only
    title = 'Debug'
    msg = (t0 + ' --- ' + t1 + ' --- ' + ' = '.join(dlist) +
            ' = '.join(remote_url))
    show_my_message(title, msg)
    '''

    return remote_url


def download_and_load(remote_files, local_dir, download_only=False,
                      varformat=None, get_support_data=False, prefix='',
                      suffix=''):
    """ Download cdf files.
        Load cdf files into pytplot variables.
        TODO: Loading files into pytplot has problems.
    """

    result = []

    """ # For debug only
    msg = local_dir + str(download_only) + " ... " + '==='.join(remote_files)
    title = 'Download Files'
    show_my_message(title, msg)
    print(msg)
    """

    remotehttp = "https://cdaweb.sci.gsfc.nasa.gov/sp_phys/data"
    count = 0
    dcount = 0
    for remotef in remote_files:
        f = remotef.strip().replace(remotehttp, '', 1)
        localf = local_dir + os.path.sep + f

        resp, err, locafile = pyspedas.download_files(remotef, localf)
        count += 1
        if resp:
            print(str(count) + '. File was downloaded. Location: ' + locafile)
            dcount += 1
            result.append(localf)
            if not download_only:
                try:
                    pytplot.cdf_to_tplot(locafile, varformat, get_support_data,
                                         prefix, suffix, False, True)
                except ValueError as err:
                    msg = "cdf_to_tplot could not load " + locafile
                    msg += "\n\n"
                    msg += "Error from pytplot: " + str(err)
                    print(msg)
                    show_my_message("Error!", msg)

        else:
            print(str(count) + '. There was a problem. Could not download \
                  file: ' + remotef)
            print(err)

    print('Downloaded ' + str(dcount) + ' files.')
    print('tplot variables:')
    print(pyspedas.tplot_names())

    return result


def clean_time_str(t):
    """ Removes the time part from datetime variable.
    """
    t0 = re.sub('T.+Z', '', t)
    return t0


def show_my_message(title, msg):
    """ Shows a message.
    """
    alert = QMessageBox()
    alert.setWindowTitle(title)
    alert.setText(msg)
    alert.exec_()


class cdagui(QMainWindow):
    """ Main CDAWeb Window.
    """

    def __init__(self, parent=None):
        super().__init__()
        self.main_widget = GUIWidget(self)
        self.setCentralWidget(self.main_widget)
        self.init_UI()

    def init_UI(self):
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Status: Ready')
        self.setWindowTitle('CDAWeb Data Downloader')
        self.showMaximized()


class GUIWidget(QWidget):
    """ Main GUI class.
    """

    # Define mission and instrument variables
    mission_list = None
    instrument_list = None
    mission_box1 = None
    instrument_box1 = None
    dataset_box1 = None
    file_box1 = None
    mission_selected = None
    instrument_selected = None
    time_start_box = None
    time_end_box = None
    dir_box = None
    local_dir = None
    button_css = "background-color:#AFEEAF;font-family:Verdana;"
    clear_css = "background-color:#E9967A;font-family:Verdana;"
    title_css = "background-color:#AFEEEE;font-family:Verdana;font-size:14px;"

    def __init__(self, parent):
        super(GUIWidget, self).__init__(parent)
        self.parent = parent
        self.initUI()

    def createMissionGroupBox(self):
        # 1. Missions and instruments group of GUI

        def find_datasets():
            # Fill the dataset list
            # Reads the selections for missions and instruments
            self.dataset_box1.clear()
            self.file_box1.clear()
            self.mission_list = []
            for m in self.mission_box1.selectedIndexes():
                self.mission_list.append(m.data())
            self.mission_selected.setText(str(self.mission_list))
            self.instrument_list = []
            for m in self.instrument_box1.selectedIndexes():
                self.instrument_list.append(m.data())
            self.instrument_selected.setText(str(self.instrument_list))
            allsets = get_datasets(self.mission_list, self.instrument_list)

            allsetslen = len(allsets)

            # Limit dataset results to 100
            datasetmaxshown = 100
            msg = ""
            if allsetslen < 1:
                title = 'Datasets Search'
                msg = ("No datasets found with these parameters: "
                       + str(self.mission_list) + ", "
                       + str(self.instrument_list))
                show_my_message(title, msg)
            elif allsetslen > datasetmaxshown:
                allsets = allsets[0:datasetmaxshown]
                title = 'Datasets Search'
                msg = ("Found " + str(allsetslen) + " datasets with these "
                       + "parameters: "
                       + str(self.mission_list) + ", "
                       + str(self.instrument_list)
                       + ". Only 100 will be shown.")
                show_my_message(title, msg)

            count = 0
            for dataItem in allsets:
                dataSet = dataItem["Id"].strip()
                if len(dataSet) > 1 and dataSet != "(null)":
                    tnow = dataItem["TimeInterval"]
                    t1 = tnow["Start"].strip()
                    t2 = tnow["End"].strip()
                    t1 = clean_time_str(t1)
                    t2 = clean_time_str(t2)

                    dataSet += " (" + t1 + ' to ' + t2 + ")"
                    item = QListWidgetItem(dataSet)
                    self.dataset_box1.addItem(item)
                    count += 1

            # Clear previous selections
            self.instrument_box1.clearSelection()
            self.mission_box1.clearSelection()

            if (msg == ""):
                if (count == 1):
                    msg = "Found 1 dataset."
                else:
                    msg = "Found " + str(count) + " datasets."
            self.parent.statusbar.showMessage('Status: ' + msg)

        # Begin construction of the GUI
        self.missionGroupBox = QGroupBox("Missions and Instruments")
        label1 = QLabel("Mission Groups:")
        label2 = QLabel("Instrument Types:")
        list1 = QListWidget(self)
        list1.setSelectionMode(QListWidget.MultiSelection)
        list1.setMinimumHeight(50)
        list1.setMinimumWidth(400)
        self.mission_box1 = list1
        list2 = QListWidget(self)
        list2.setSelectionMode(QListWidget.MultiSelection)
        list2.setMinimumHeight(50)
        list2.setMinimumWidth(400)
        self.instrument_box1 = list2
        label3 = QLabel("Select one or more Mission Group(s) and one"
                        + " or more Instrument Type(s) and press:")
        button1 = QPushButton("1. Find Datasets")
        button1.setStyleSheet(self.button_css)

        # Create the layout and add GUI elements
        layout = QGridLayout()
        layout.addWidget(label1, 0, 0)
        layout.addWidget(label2, 0, 1)
        layout.addWidget(list1, 1, 0)
        layout.addWidget(list2, 1, 1)
        layout.addWidget(label3, 2, 0, 1, 1)
        layout.addWidget(button1, 2, 1, 1, 1)

        # Fill the mission list
        for dataItem in get_observatories():
            # Contains Name, ShortDescription, LongDescription
            # mission = dataItem["ShortDescription"].strip()
            # mission = dataItem["LongDescription"].strip()
            mission = dataItem["Name"].strip()
            if len(mission) > 1 and mission != "(null)":
                item = QListWidgetItem(mission)
                list1.addItem(item)

        # Fill the instruments list
        for dataItem in get_instr():
            instr = dataItem["Name"].strip()
            if len(instr) > 1 and instr != "(null)":
                item = QListWidgetItem(instr)
                list2.addItem(item)

        # Button1 action
        button1.clicked.connect(find_datasets)

        self.missionGroupBox.setLayout(layout)

    def createDatasetBox(self):
        # 2. Dataset group of GUI

        self.datasetGroupBox = QGroupBox("Datasets")

        label1 = QLabel("Selected Mission Groups:")
        ans1 = QLabel("   ")
        self.mission_selected = ans1
        ans1.setWordWrap(True)
        label2 = QLabel("Selected Instruments:")
        ans2 = QLabel("   ")
        self.instrument_selected = ans2
        ans2.setWordWrap(True)

        listds = QListWidget(self)
        self.dataset_box1 = listds
        listds.setMinimumHeight(50)
        listds.setMinimumWidth(400)
        listds.setSelectionMode(QListWidget.MultiSelection)
        layout = QGridLayout()
        # row, column, rowSpan, columnSpan
        layout.addWidget(label1, 0, 0, 1, 1)
        layout.addWidget(ans1, 0, 1, 1, 5)
        layout.addWidget(label2, 1, 0, 1, 1)
        layout.addWidget(ans2, 1, 1, 1, 5)
        layout.addWidget(listds, 2, 0, 1, 6)

        self.datasetGroupBox.setLayout(layout)

    def createTimeGroupBox(self):
        # 3. Date and time group of GUI

        def get_file_list():
            # Find remote files

            self.file_box1.clear()

            # Find the selected datasets
            dataset_list = []
            msg = ""
            for m in self.dataset_box1.selectedIndexes():
                dataset_list.append(m.data())
            if len(dataset_list) < 1:
                msg = "Please select a dataset."
                title = "No Datasets"
                show_my_message(title, msg)
                self.parent.statusbar.showMessage('Status: ' + msg)
                return

            # Find the the files
            t0 = self.time_start_box.text()
            t1 = self.time_end_box.text()
            remote_file_list = files_to_download(dataset_list, t0, t1)

            count = 0
            for f in remote_file_list:
                item = QListWidgetItem(f)
                self.file_box1.addItem(item)
                count += 1

            if (msg == ""):
                if (count == 1):
                    msg = "Found 1 file."
                else:
                    msg = "Found " + str(count) + " files."
            self.parent.statusbar.showMessage('Status: ' + msg)

        def pick_time(start_or_end):
            dlg = QDialog(self)
            gridc = QVBoxLayout()
            dlg.setLayout(gridc)
            if (start_or_end == "start"):
                title_str = "Start date"
            else:
                title_str = "End date"
            titlelabel = QLabel(title_str)
            gridc.addWidget(titlelabel)

            my_calendar = QCalendarWidget()
            my_calendar.setGridVisible(True)
            my_calendar.move(10, 20)
            gridc.addWidget(my_calendar)

            labeldate = QLabel("")
            gridc.addWidget(labeldate)

            def dial_exit():
                dlg.done(1)

            buttonc = QPushButton("Close")
            buttonc.clicked.connect(dial_exit)
            gridc.addWidget(buttonc)

            def show_date():
                date = my_calendar.selectedDate()
                date_string = date.toString('yyyy-MM-dd')
                if (start_or_end == "start"):
                    self.time_start_box.setText(date_string + " 00:00:01")
                else:
                    self.time_end_box.setText(date_string + " 23:59:59")
                labeldate.setText(date_string)

            my_calendar.clicked[QDate].connect(show_date)

            dlg.setWindowTitle("Calendar")
            dlg.exec_()

        self.timeGroupBox = QGroupBox("Date and Time")

        label1 = QLabel("Start Time:")
        # By default show date 7 days behind to ensure that there is data
        t0 = datetime.datetime.strftime(datetime.datetime.now()
                                        - datetime.timedelta(7), '%Y-%m-%d')
        time1 = QLineEdit(str(t0) + " 00:00:01")
        self.time_start_box = time1
        label2 = QLabel("End Time:")
        time2 = QLineEdit(str(t0) + " 23:59:59")
        self.time_end_box = time2
        label3 = QLabel("Date and time format: YYYY-MM-DD[ HH:MM:SS]")
        button1 = QPushButton("Select")
        button2 = QPushButton("Select")
        button3 = QPushButton("2. Get File List")
        button3.setStyleSheet(self.button_css)

        layout = QGridLayout()
        layout.addWidget(label1, 0, 0)
        layout.addWidget(time1, 0, 1)
        layout.addWidget(button1, 0, 2)
        layout.addWidget(label2, 0, 3)
        layout.addWidget(time2, 0, 4)
        layout.addWidget(button2, 0, 5)
        layout.addWidget(label3, 1, 0, 1, 3)
        layout.addWidget(button3, 1, 3, 1, 3)

        # Calendar pick
        button1.clicked.connect(lambda: pick_time("start"))
        button2.clicked.connect(lambda: pick_time("end"))

        # Button3 action
        button3.clicked.connect(get_file_list)

        self.timeGroupBox.setLayout(layout)

    def createDownloadGroupBox(self):
        # 4. Download group of GUI

        msg2 = ("If checked, then the files will"
                + " only be downloaded. If unchecked, then they will also"
                + " be read and loaded into pytplot variables.")
        check1 = QCheckBox("Download Only")
        check1.setToolTip(msg2)
        check1.setChecked(True)
        buttondown = QPushButton("3. Get Data")
        buttondown.setStyleSheet(self.button_css)

        def clear_all():
            # Clear all boxes
            self.file_box1.clear()
            self.dataset_box1.clear()
            self.instrument_box1.clearSelection()
            self.mission_box1.clearSelection()
            self.instrument_selected.setText('')
            self.mission_selected.setText('')
            self.parent.statusbar.showMessage('Status: Ready')

        def get_data():
            # Download files
            download_only = False
            if check1.isChecked():
                download_only = True

            # Find the selected files
            remote_file_list = []
            for m in self.file_box1.selectedIndexes():
                remote_file_list.append(m.data())
            if len(remote_file_list) < 1:
                title = "No files"
                msg = "Please select some files to download."
                show_my_message(title, msg)
                return
            # Load downloaded files into pytplot
            result = []
            if len(remote_file_list) < 1:
                msg = "No files to download."
                show_my_message(title, msg)
                return

            self.local_dir = self.dir_box.text()

            QApplication.setOverrideCursor(Qt.WaitCursor)
            result = download_and_load(remote_file_list, self.local_dir,
                                       download_only)
            QApplication.restoreOverrideCursor()

            reslen = len(result)
            if reslen > 0:
                msg = "Donwload complete. Number of files: " + str(reslen)
            else:
                msg = "No files were downloaded."

            title = 'Download Files'
            show_my_message(title, msg)
            self.parent.statusbar.showMessage('Status: ' + msg)

        def select_dir():
            file = str(QFileDialog.getExistingDirectory(self,
                                                        "Select Directory"))
            self.local_dir = file
            dir1.setText(self.local_dir)

        def exit_all():
            self.parent.close()
            app.exit()

        self.dirGroupBox = QGroupBox("Remote Files and Download")

        listf = QListWidget(self)
        self.file_box1 = listf
        listf.setMinimumHeight(50)
        listf.setMinimumWidth(400)
        listf.setSelectionMode(QListWidget.MultiSelection)

        label1 = QLabel("Download Directory:")
        dir1 = QLineEdit()
        self.local_dir = get_default_data_dir()
        dir1.setText(self.local_dir)
        self.dir_box = dir1
        button1 = QPushButton("Change Directory")
        buttonclear = QPushButton("Clear")
        buttonclear.setStyleSheet(self.clear_css)
        buttonexit = QPushButton("Exit")
        buttonexit.setStyleSheet(self.clear_css)

        layout = QGridLayout()
        layout.addWidget(listf, 0, 0, 1, 6)
        layout.addWidget(label1, 1, 0, 1, 1)
        layout.addWidget(dir1, 1, 1, 1, 4)
        layout.addWidget(button1, 1, 5, 1, 1)
        layout.addWidget(check1, 2, 0, 1, 2)
        layout.addWidget(buttondown, 2, 2, 1, 2)
        layout.addWidget(buttonclear, 2, 4, 1, 1)
        layout.addWidget(buttonexit, 2, 5, 1, 1)

        # Button1 action
        button1.clicked.connect(select_dir)
        buttondown.clicked.connect(get_data)
        buttonclear.clicked.connect(clear_all)
        buttonexit.clicked.connect(exit_all)

        self.dirGroupBox.setLayout(layout)

    def initUI(self):
        """ Create GUI
        """

        # Main layout is vertical
        grid = QVBoxLayout()
        self.setLayout(grid)

        # Top label
        label1 = QLabel("Download Data from CDAWeb")
        label1.setStyleSheet(self.title_css)
        label1.setAlignment(Qt.AlignCenter)
        grid.addWidget(label1)

        # 1. Create missions and instruments group
        self.createMissionGroupBox()
        grid.addWidget(self.missionGroupBox)

        # 2. Create dataset group
        self.createDatasetBox()
        grid.addWidget(self.datasetGroupBox)

        # 3. Create datetime group
        self.createTimeGroupBox()
        grid.addWidget(self.timeGroupBox)

        # 4. Create download group
        self.createDownloadGroupBox()
        grid.addWidget(self.dirGroupBox)

        self.showMaximized()


if __name__ == '__main__':
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    cdagui = cdagui()
    app.exec_()
