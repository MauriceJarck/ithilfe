import sys
import csv
import datetime

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget
from PyQt5 import QtWidgets, QtCore
from PyQt5.uic import loadUi


class Device:
    """Device parent class

    base of all more specified device classes"""
    def __init__(self, name: str, user: str, comment: str, datetime: str) -> None:
        """inits Device class

        configuring parameters of Device class

        Args:
            name: defines devicename of registered device
            user: defines username of registered device
            comment: defines comment of registered device to point out some thing worth knowing
            datetime: defines date and time when registration was made
        Returns:
            None
        """

        self.name = name
        self.user = user
        self.OS = None
        self.comment = comment
        self.datetime = datetime

    def __str__(self) -> str:
        """overwrites str method

        houses readable information of Device parameters

        Returns:
            String representation of Device instance
        """
        return f"{self.name}, {self.user}, {self.OS}, {self.__class__.__name__}, {self.comment}"

    visible_attr = ["user", "OS"]
    """list of attributes which can be modified by the user"""


class WindowsLapTop(Device):
    """

    specifies Device class and adds exta status variables

    """
    def __init__(self, name: str, user: str, comment: str, datetime: str) -> None:
        """inits Device class

            configuring parameters of Device class

            Args:
                name: defines devicename of registered device
                user: defines username of registered device
                comment: defines comment of registered device to point out some thing worth knowing
                datetime: defines date and time when registration was made
            Returns:
                None
            """
        super().__init__(name, user, comment, datetime)
        self.bitlockkey = 1234
        """int: example of attribute not beeing visible to user"""
        self.largerBattery = True
        """bool: example of extra attribute describing class"""
        self.upgradedCPU = False
        """bool: example of extra attribute describing class"""

    def __str__(self):
        """overwrites str method

            houses readable information of Device parameters

            Returns:
                String representation of Device instance
            """
        return f"{self.name}, {self.user}, {self.OS}, {self.__class__.__name__}, largerbattery: {self.largerBattery}, upgradedCPU: {self.upgradedCPU}"

    expected_OS = ["Win10", "Win7"]
    """list: possible os which to this device type"""

    visible_attr = ["user", "OS", "largerBattery", "upgradedCPU"]
    """list: attributes which can be modified by the user overwrites same attribute of Device class"""



class WindowsWorkStation(Device):
    """specifies Device class and adds exta status variables

        """
    expected_OS = ["Win10", "Win7"]
    """list: possible os which to this device type"""


class Macbook(Device):
    """specifies Device class and adds exta status variables

            """
    expected_OS = ["MacOS"]
    """list: possible os which to this device type"""


registered_devices = {}
valid_devices = [WindowsLapTop, WindowsWorkStation, Macbook]


class MainWindow(QMainWindow):
    """handles all action on MainWin"""

    def __init__(self):
        """inits MainWindow class

            configuring parameters of MainWindow class and inherits from QtWidget.QMainWindow
            loads .ui file sets up file and directory path vars, inits click events(menuebar, coboboxes, btns) and
            shows gui the first time

            """
        super(MainWindow, self).__init__()
        loadUi("../tests/mainWindow.ui", self)
        # etc
        self.fname = None
        self.dir = None
        self.stackedWidget.setCurrentWidget(self.pView)
        # return pressed
        self.inUserSearch.returnPressed.connect(lambda: self.validate(self.search, [self.inUserSearch], checkregistered=True))
        self.inChangeNewval.returnPressed.connect(lambda: self.validate(self.change, data=2, checkregistered=True))
        self.inNewFilename.returnPressed.connect(lambda: self.validate(self.new, [self.inNewFilepath, self.inNewFilename], data=False))
        # doubleclick
        self.tableWidgetAllRegistered.cellDoubleClicked.connect(lambda: self.d_click_table_devicename(self.tableWidgetAllRegistered.currentItem().text()))
        self.tableWidgetSearch.cellDoubleClicked.connect(lambda: self.d_click_table_devicename(self.tableWidgetSearch.currentItem().text()))
        # comboboxes
        self.inComboboxDevicetype.addItems(["choose here"]+[x.__name__ for x in valid_devices])
        self.inComboboxDevicetype.currentIndexChanged.connect(lambda: self.update_combobox(self.inComboBoxRegisterOS, valid_devices[self.inComboboxDevicetype.currentIndex()-1].expected_OS))
        # btns
        self.btSearch.clicked.connect(lambda: self.validate(self.search, [self.inUserSearch], checkregistered=True))
        self.btRegisterNew.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pRegister))
        self.btRegister.clicked.connect(lambda: self.validate(self.register, line_edit_list=[self.inUsername, self.inDevicename],
                                                              combo_box_list=[self.inComboboxDevicetype, self.inComboBoxRegisterOS],
                                                              forbidden=list(registered_devices.keys()), checkfname=True))
        self.btChange.clicked.connect(lambda: self.validate(self.change, data=2, checkregistered=True))
        self.btCreate.clicked.connect(lambda: self.validate(self.new, [self.inNewFilepath, self.inNewFilename], data=False))
        self.btModNewPath.clicked.connect(lambda: self.new(True))
        # menu bar
        self.actionSearch.triggered.connect(lambda: self.stackedWidget.setCurrentWidget(self.pSearch))
        self.actionRegister.triggered.connect(lambda: self.stackedWidget.setCurrentWidget(self.pRegister))
        self.actionChange.triggered.connect(lambda: self.change(0))
        self.actionOpen.triggered.connect(lambda: self.open(False))
        self.actionSave.triggered.connect(self.save)
        self.actionNew.triggered.connect(lambda: self.new(True))
        # cancel
        self.btCancelRegister.clicked.connect(lambda: self.cancel([self.inUsername, self.inDevicename, self.inComboBoxRegisterOS, self.textEditComment]))
        self.cancelSearch.clicked.connect(lambda: self.cancel([self.inUserSearch]))
        self.btCancelChange.clicked.connect(lambda: self.cancel([self.inComboBoxChangeParamtype, self.inComboBoxChangeNewval, self.inChangeNewval]))
        # funcs
        self.update_table(self.tableWidgetAllRegistered, registered_devices.values())
        self.show()

    def cancel(self, widgets: list)->None:
        """click event for all cancel buttons

        shows fist page in stacked widget and clears all widgets in widgets

        Args:
               widgets: defines list containing widgets to clear, only widgets with method .clear() are possible

        Returns:
            None
            """
        for widget in widgets:
            widget.clear()
        self.stackedWidget.setCurrentWidget(self.pView)

    def update_combobox(self, box, data: list) -> None:
        """ clears combo box

        updates combobox so that old content not needed any more isnt displayed and adds 'choose here' dummy
        to ensure an index change will be made (updating next box depends on index change)
        Args:
            box: instance of pyqt5.QtWidgets.qComboBox
            data: data supposed to be inserted into combobox
        Returns:
            None"""

        box.clear()
        box.addItems(["choose here"] + data)

    def update_table(self, table, content) -> None:
        """updates any table with data of registered_devices

        first clears table, then fills up with new values

        Args:
            table: instance of pyqt5.QtWidgets.qTable
            content: instances of any device of which its attributes will be content of table

        Returns:
            None"""
        row = 0
        table.clearContents()
        table.setRowCount(len(content))
        table.setHorizontalHeaderLabels(['username', 'devname', 'devtype', 'os', "comment", "extras", "datetime"])
        for x in content:
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(x.user))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(x.name))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(x.__class__.__name__))
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(x.OS))
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(x.comment))
            table.setItem(row, 5, QtWidgets.QTableWidgetItem(",".join([str(a) for a in x.visible_attr[2:]])))
            table.setItem(row, 6, QtWidgets.QTableWidgetItem(x.datetime))
            row += 1

    def d_click_table_devicename(self, referenz: str) -> None:
        """handels double click event on devicename in table widget

        Args:
            referenz: current selceted text of cell
        Returns:
            None
            """
        if referenz in registered_devices.keys():
            self.inComboBoxDevicename.addItems(["choose here", referenz])
            self.change(0)

    def validate(self, command, line_edit_list: list = None, combo_box_list: list = None, data = None, allowed: list = None, forbidden: list = None, checkfname: bool = None, checkregistered: bool = None) -> None:
        """validates user input

        Args:
            command: function to be called after vailidation process if finished
            line_edit_list: contents pyqt5.QtWidgets.QlineEdit instances to be checked if empty or current text in forbidden or not in allowed
            combo_box_list: contents pyqt5.QtWidgets.qComboBox instances to be checked if nothing selected
            data: data to be passed into command function if needed
            allowed: houses key wihich are allowed to be entered
            forbidden: houses keys which are not allowed to be entered
            checkfname: check weather an file path exists or not
            checkregistered: check weather something is already registered or not

        Returns:
            None"""

        fails = 0
        if line_edit_list is not None:
            for x in line_edit_list:
                if x.text() == "":
                    x.setText("fill all fields")
                    fails += 1
                if allowed is not None and x.text() not in allowed:
                    x.setText("not in allowed!!")
                    fails += 1
                if forbidden is not None and x.text() in forbidden:
                    x.setText("in forbidden!!")
                    fails += 1
        if combo_box_list is not None:
            for combobox in combo_box_list:
                if combobox.currentText() == "":
                    self.statusbar.showMessage("all comboboxes must be specified")
                    fails += 1
        if checkfname is True and self.fname is None:
            self.statusbar.showMessage("no file path specified, visit Ctrl+o or menuebar/edit/open to fix")
            fails += 1
        if checkregistered is True and len(registered_devices) == 0:
            self.statusbar.showMessage("nothing registered yet")
            fails += 1
        if fails == 0:
            if data is None:
                command()
            else:
                command(data)
        else:
            print("problem")

    def register(self) -> None:
        """registers a new device and saves it int csv"""
        new = valid_devices[self.inComboBoxRegisterOS.currentIndex()](self.inDevicename.text(), self.inUsername.text(), self.textEditComment.toPlainText(), str(datetime.datetime.now()))
        new.OS = self.inComboBoxRegisterOS.currentText()
        registered_devices[self.inDevicename.text()] = new
        self.stackedWidget.setCurrentWidget(self.pView)
        self.inDevicename.clear()
        self.inUsername.clear()
        self.inComboBoxRegisterOS.clear()
        self.textEditComment.clear()
        self.update_table(self.tableWidgetAllRegistered, registered_devices.values())
        self.save()

    def search(self) -> None:
        """searches for a given username in registered devices and outputs on statusbar"""
        results = [x for x in registered_devices.values() if x.user == self.inUserSearch.text()]
        if len(results) >= 1:
            self.update_table(self.tableWidgetSearch, results)
            self.statusbar.showMessage(f"found {len(results)} match/es")
        else:
            self.statusbar.showMessage("nothing found")

    def change(self, x: int) -> None:
        """changes existing device parameters
        x == 0: fill combobox,
        x == 1: paramtypeIndex has changed, based on that new valtype is determined
        x == 2: retrieve data, change parameter, clear, and save
        Args:
            x: determines a which state to execute this function """
        if x == 0:
            self.stackedWidget.setCurrentWidget(self.pChange)
            if self.inComboBoxDevicename.count() == 0:
                self.inComboBoxDevicename.addItems(["choose here"] + list(registered_devices.keys()))
            self.inComboBoxDevicename.currentIndexChanged.connect(lambda: self.update_combobox(self.inComboBoxChangeParamtype, registered_devices.get(self.inComboBoxDevicename.currentText()).visible_attr))
            self.inComboBoxChangeParamtype.currentIndexChanged.connect(lambda: self.change(1))
        elif x == 1:
            if self.inComboBoxChangeParamtype.currentText() != "OS":
                self.stackedWidget2.setCurrentWidget(self.pLineEdit)
            else:
                self.stackedWidget2.setCurrentWidget(self.pComboBox)
                self.inComboBoxChangeNewval.addItems(["choose here"] + registered_devices.get(self.inComboBoxDevicename.currentText()).expected_OS)
        elif x == 2:
            _class = registered_devices.get(self.inComboBoxDevicename.currentText())
            paramtype = self.inComboBoxChangeParamtype.currentText()
            if paramtype == "OS":
                newval = self.inComboBoxChangeNewval.currentText()
            else:
                newval = self.inChangeNewval.text()
            setattr(_class, paramtype, newval)
            self.update_table(self.tableWidgetAllRegistered, registered_devices.values())
            self.stackedWidget.setCurrentWidget(self.pView)

            self.inComboBoxChangeParamtype.clear()
            self.inComboBoxChangeNewval.clear()
            self.save()

    def open(self, test: bool) -> None:
        """opens csv file and loads its content into registered devices
        Args:
            test: skip filedialog if unittested aka test == True, fname has to be set in test script"""

        registered_devices.clear()
        if not test:
            self.fname = QFileDialog.getOpenFileName(self, "open file", "c://", "text files (*csv)")[0]
        with open(self.fname, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                new = [x for x in valid_devices if x.__name__ == row["device_type"]].pop(0)(row["name"], row["username"], row["comment"], row["datetime"])
                new.OS = row["OS"]
                registered_devices[row["name"]] = new
        self.update_table(self.tableWidgetAllRegistered, registered_devices.values())

    def save(self) -> None:
        """saves content fo registered_devices into specified csv file"""

        if not self.fname:
            self.statusbar.showMessage("no file path set all changes get lost if closed")
        else:
            with open(self.fname, 'w',) as csvfile:
                fieldnames = ["name", "username", "OS", "device_type", "comment", "extras", "datetime"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for x in registered_devices.values():
                    writer.writerow(
                        {"name": x.name,
                         "username": getattr(x, x.visible_attr[0]),
                         "OS": getattr(x, x.visible_attr[1]),
                         "device_type": x.__class__.__name__,
                         "extras": [(a, getattr(x, a)) for a in x.visible_attr[2:-1]],
                         "comment": x.comment,
                         "datetime": x.datetime
                         })

    def new(self, stage: bool) -> None:
        """creates new csv file to save into

        stage is True: set filepath
        stage is False: set new name, save
        Args:
            stage: determines a which stage to execute this function """
        if stage is True:
            self.dir = QFileDialog.getExistingDirectory(self, "select a folder", "c://")
            self.stackedWidget.setCurrentWidget(self.pCreate)
            self.inNewFilepath.setText(self.dir)
        else:
            self.fname = self.dir + f"/{self.inNewFilename.text()}.csv"
            self.save()
            self.tableWidgetAllRegistered.clearContents()
            self.stackedWidget.setCurrentWidget(self.pView)


class StartScreen(QWidget):
    """startscreen to be displayed at begining"""
    def __init__(self) -> None:
        """inits StartScreen class

        loads interface aka .ui file"""

        super(StartScreen, self).__init__()
        loadUi("../tests/startscreen.ui", self)
        self.show()
        self.timer = QtCore.QTimer()
        self.timer.singleShot(1500, self.on_elapsed)

    def on_elapsed(self) -> None:
        """closes StartStartsceen Window and creates instance of MainWindow"""
        self.close()
        MainWindow()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    startscreen = StartScreen()

    sys.exit(app.exec_())
