
"""
GUI for CDAWeb

A GUI that can download data files from CDAWeb
and load them into pytplot variables.
Requires cdasws, PyQt5.

To open the GUI window:
    from pyspedas.cdagui.cdagui import cdagui
    x = cdagui()

For cdasws documentation, see:
    https://test.pypi.org/project/cdasws/
    https://cdaweb.gsfc.nasa.gov/WebServices/REST/py/cdasws/index.html

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
import datetime
from PyQt5.QtCore import Qt, QDate, QCoreApplication
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow,
                             QGridLayout, QPushButton, QListWidget,
                             QGroupBox, QCheckBox, QMessageBox,
                             QVBoxLayout, QLabel, QLineEdit,
                             QFileDialog, QCalendarWidget, QDialog)
from .cdaweb import CDAWeb
from .config import CONFIG

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
        self.setWindowTitle('CDAWeb Data Downloader')
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Status: Ready')
        self.showMaximized()


class GUIWidget(QWidget):
    """ Main GUI class.
    """

    def __init__(self, parent):
        super(GUIWidget, self).__init__(parent)
        self.parent = parent
        self.cda = CDAWeb()
        self.title_css = "background-color:#AFEEEE;\
            font-family:Verdana;font-size:14px;"
        self.button_css = "background-color:#AFEEAF;font-family:Verdana;"
        self.clear_css = "background-color:#E9967A;font-family:Verdana;"
        self.initUI()

    def createMissionGroupBox(self):
        # 1. Missions and instruments group of GUI

        def button1_find_datasets():
            title = "Find Datasets"
            self.dataset_box.clear()
            self.file_box.clear()
            mission_list = [item.text() for item in
                            self.mission_box.selectedItems()]
            instrument_list = [item.text() for item in
                               self.instrument_box.selectedItems()]
            if len(mission_list) < 1 or len(instrument_list) < 1:
                msg = "Please select at least one mission and one instrument."
                show_my_message(title, msg)
                return 0
            datasets = self.cda.get_datasets(mission_list, instrument_list)
            datalen = len(datasets)
            if datalen < 1:
                msg = "No datasets were found with these parameters."
                show_my_message(title, msg)
                return 0
            elif datalen > 50:
                msg = "Number of datasets found: " + str(datalen)
                msg += "\nOnly 50 will be shown."
                show_my_message(title, msg)
            self.mission_selected.setText(str(mission_list))
            self.instrument_selected.setText(str(instrument_list))
            self.dataset_box.addItems(datasets[:50])

        # Missions group GUI elements
        self.missionGroupBox = QGroupBox("Missions and Instruments")

        label1 = QLabel("Mission Groups:")
        list1 = QListWidget(self)
        list1.setSelectionMode(QListWidget.MultiSelection)
        list1.setMinimumHeight(50)
        list1.setMinimumWidth(400)
        list1.addItems(self.cda.get_observatories())
        self.mission_box = list1

        label2 = QLabel("Instrument Types:")
        list2 = QListWidget(self)
        list2.setSelectionMode(QListWidget.MultiSelection)
        list2.setMinimumHeight(50)
        list2.setMinimumWidth(400)
        list2.addItems(self.cda.get_instruments())
        self.instrument_box = list2

        label3 = QLabel("Select one or more Mission Group(s) and one"
                        + " or more Instrument Type(s) and press:")
        button1 = QPushButton("1. Find Datasets")
        button1.setStyleSheet(self.button_css)
        button1.clicked.connect(button1_find_datasets)

        # Create the layout and add GUI elements
        # row, column, rowSpan, columnSpan
        layout = QGridLayout()
        layout.addWidget(label1, 0, 0)
        layout.addWidget(label2, 0, 1)
        layout.addWidget(list1, 1, 0)
        layout.addWidget(list2, 1, 1)
        layout.addWidget(label3, 2, 0, 1, 1)
        layout.addWidget(button1, 2, 1, 1, 1)

        self.missionGroupBox.setLayout(layout)

    def createDatasetBox(self):
        # 2. Dataset group of GUI

        # Datasets group GUI elements
        self.datasetGroupBox = QGroupBox("Datasets")

        label1 = QLabel("Selected Mission Groups:")
        ans1 = QLabel("   ")
        self.mission_selected = ans1
        ans1.setWordWrap(True)

        label2 = QLabel("Selected Instruments:")
        ans2 = QLabel("   ")
        self.instrument_selected = ans2
        ans2.setWordWrap(True)

        list1 = QListWidget(self)
        self.dataset_box = list1
        list1.setMinimumHeight(50)
        list1.setMinimumWidth(400)
        list1.setSelectionMode(QListWidget.MultiSelection)

        layout = QGridLayout()
        layout.addWidget(label1, 0, 0, 1, 1)
        layout.addWidget(ans1, 0, 1, 1, 15)
        layout.addWidget(label2, 1, 0, 1, 1)
        layout.addWidget(ans2, 1, 1, 1, 15)
        layout.addWidget(list1, 2, 0, 1, 16)

        self.datasetGroupBox.setLayout(layout)

    def createTimeGroupBox(self):
        # 3. Date and time group of GUI

        def button2_get_file_list():
            title = "Get File List"
            self.file_box.clear()
            dataset_list = [item.text() for item in
                            self.dataset_box.selectedItems()]
            t0 = self.time_start_box.text()
            t1 = self.time_end_box.text()
            if len(dataset_list) < 1 or len(t0) < 9 or len(t1) < 9:
                msg = "Please select at least one dataset and start-end times."
                show_my_message(title, msg)
                return 0
            file_list = self.cda.get_filenames(dataset_list, t0, t1)
            filelen = len(file_list)
            if filelen < 1:
                msg = "No datasets were found with these parameters."
                show_my_message(title, msg)
                return 0
            elif filelen > 50:
                msg = "Number of files found: " + str(filelen)
                msg += "\nOnly 50 will be shown."
                show_my_message(title, msg)
            self.file_box.addItems(file_list[:50])

        def pick_time(start_or_end):
            # Date picker
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

        # Date and Time group GUI elements
        self.timeGroupBox = QGroupBox("Date and Time")

        # By default show 7 days behind to ensure that there is data
        label1 = QLabel("Start Time:")
        t0 = datetime.datetime.strftime(datetime.datetime.now()
                                        - datetime.timedelta(7), '%Y-%m-%d')
        time1 = QLineEdit(str(t0) + " 00:00:01")
        self.time_start_box = time1
        button1 = QPushButton("Select")
        button1.clicked.connect(lambda: pick_time("start"))

        label2 = QLabel("End Time:")
        time2 = QLineEdit(str(t0) + " 23:59:59")
        self.time_end_box = time2
        button2 = QPushButton("Select")
        button2.clicked.connect(lambda: pick_time("end"))

        label3 = QLabel("Date and time format: YYYY-MM-DD[ HH:MM:SS]")
        button3 = QPushButton("2. Get File List")
        button3.setStyleSheet(self.button_css)
        button3.clicked.connect(button2_get_file_list)

        layout = QGridLayout()
        layout.addWidget(label1, 0, 0)
        layout.addWidget(time1, 0, 1)
        layout.addWidget(button1, 0, 2)
        layout.addWidget(label2, 0, 3)
        layout.addWidget(time2, 0, 4)
        layout.addWidget(button2, 0, 5)
        layout.addWidget(label3, 1, 0, 1, 3)
        layout.addWidget(button3, 1, 3, 1, 3)

        self.timeGroupBox.setLayout(layout)

    def createDownloadGroupBox(self):
        # 4. Download group of GUI

        def button3_get_data():
            title = "Download Files"
            file_list = [item.text() for item in self.file_box.selectedItems()]
            if len(file_list) < 1:
                msg = "Please select at least one file to download."
                show_my_message(title, msg)
                return 0
            local_dir = self.dir_box.text()
            if len(local_dir) < 1:
                msg = "Please select a local directory."
                show_my_message(title, msg)
                return 0
            download_only = False
            if check1.isChecked():
                download_only = True

            # The following can be slow, especially if there are multiple files
            self.parent.statusbar.showMessage('Status: Downloading, \
                                              please wait...')
            QApplication.setOverrideCursor(Qt.WaitCursor)
            QApplication.processEvents()
            result = self.cda.download(file_list, local_dir, download_only)
            QApplication.restoreOverrideCursor()
            self.parent.statusbar.showMessage('Status: Ready')

            filelen = len(result)
            if filelen < 1:
                msg = "No files were downloaded."
                show_my_message(title, msg)
                return 0
            else:
                count_no_downloads = 0
                count_tplot_problem = 0
                count_tplot = 0
                for item in result:
                    if item[2] == -1:
                        count_no_downloads += 1
                    elif item[2] == 0 and not download_only:
                        count_tplot_problem += 1
                    elif item[2] == 1:
                        count_tplot += 1
                msg = "Results:"
                msg += "\n"
                msg += "\nFiles to download: " + str(filelen)
                msg += ("\nFiles that could not be downloaded: "
                        + str(count_no_downloads))
                if not download_only:
                    msg += "\n"
                    msg += ("\nFiles loaded to pytplot: " + str(count_tplot))
                    msg += ("\nFiles that could not be loaded to pytplot: "
                            + str(count_tplot_problem))
                show_my_message(title, msg)

        def select_dir():
            file = str(QFileDialog.getExistingDirectory(self,
                                                        "Select Directory"))
            if file:
                self.local_dir = file
                self.dir_box.setText(self.local_dir)

        def clear_all():
            # Clear all boxes
            self.mission_box.clearSelection()
            self.instrument_box.clearSelection()
            self.instrument_selected.setText('')
            self.mission_selected.setText('')
            self.dataset_box.clear()
            self.file_box.clear()
            self.parent.statusbar.showMessage('Status: Ready')

        def exit_all():
            self.parent.close()

        # Download Files GUI elements
        self.dirGroupBox = QGroupBox("Remote Files and Download")

        list1 = QListWidget(self)
        list1.setMinimumHeight(50)
        list1.setMinimumWidth(400)
        list1.setSelectionMode(QListWidget.MultiSelection)
        self.file_box = list1

        label1 = QLabel("Download Directory:")
        dir1 = QLineEdit()
        self.local_dir = CONFIG['local_data_dir']
        dir1.setText(self.local_dir)
        self.dir_box = dir1
        button1 = QPushButton("Change Directory")
        button1.clicked.connect(select_dir)

        msg2 = ("If checked, then the files will"
                + " only be downloaded. If unchecked, then they will also"
                + " be read and loaded into pytplot variables.")
        check1 = QCheckBox("Download Only")
        check1.setToolTip(msg2)
        check1.setChecked(True)
        buttondown = QPushButton("3. Get Data")
        buttondown.setStyleSheet(self.button_css)
        buttondown.clicked.connect(button3_get_data)

        buttonclear = QPushButton("Clear")
        buttonclear.setStyleSheet(self.clear_css)
        buttonclear.clicked.connect(clear_all)

        buttonexit = QPushButton("Exit")
        buttonexit.setStyleSheet(self.clear_css)
        buttonexit.clicked.connect(exit_all)

        layout = QGridLayout()
        layout.addWidget(list1, 0, 0, 1, 6)
        layout.addWidget(label1, 1, 0, 1, 1)
        layout.addWidget(dir1, 1, 1, 1, 4)
        layout.addWidget(button1, 1, 5, 1, 1)
        layout.addWidget(check1, 2, 0, 1, 2)
        layout.addWidget(buttondown, 2, 2, 1, 2)
        layout.addWidget(buttonclear, 2, 4, 1, 1)
        layout.addWidget(buttonexit, 2, 5, 1, 1)

        # Button1 action

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
        label1.setMaximumHeight(20)
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
    sys.exit(app.exec_())
