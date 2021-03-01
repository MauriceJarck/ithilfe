import os
import sys
import csv
import datetime

from PySide2.QtGui import QPixmap, QIcon, QFont
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget
from PySide2 import QtWidgets, QtCore
# from PySide2.QtUiTools import QUiLoader

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


class MainWindowUi(QMainWindow):
    def __init__(self):
        super(MainWindowUi, self).__init__()
        self.resize(100, 100)

        stackedWidget = QtWidgets.QStackedWidget(self)
        pRegister = QtWidgets.QWidget()
        self.btRegister = QtWidgets.QPushButton(pRegister)

        # pSearch = QtWidgets.QWidget()
        # pChange = QtWidgets.QWidget()
        stackedWidget.addWidget(pRegister)
        # stackedWidget.addWidget(pSearch)
        # stackedWidget.addWidget(pChange)
        stackedWidget.setCurrentWidget(pRegister)
        self.setWindowIcon(QIcon("../data/favicon.ico"))

class MainWindow_logic:
    """handles all action on MainWin"""

    def __init__(self):
        """inits MainWindow class

            configuring parameters of MainWindow class and inherits from QtWidget.QMainWindow
            loads .ui file sets up file and directory path vars, inits click events(menuebar, coboboxes, btns) and
            shows gui the first time

            """

        self.win = MainWindowUi()
        self.win.show()

        self.win.btRegister.clicked.connect(lambda: print("hallo"))

        # etc
        # self.fname = None
        # self.dir = None
        # self.win.stackedWidget.setCurrentWidget(self.win.pView)
        # # return pressed
        # self.win.inUserSearch.returnPressed.connect(lambda: self.validate(self.search, [self.win.inUserSearch], checkregistered=True))
        # self.win.inChangeNewval.returnPressed.connect(lambda: self.validate(self.change, data=2, checkregistered=True))
        # self.win.inNewFilename.returnPressed.connect(lambda: self.validate(self.new, [self.win.inNewFilepath, self.win.inNewFilename], data=False))
        # # doubleclick
        # self.win.tableWidgetAllRegistered.cellDoubleClicked.connect(lambda: self.d_click_table_devicename(self.win.tableWidgetAllRegistered.currentItem().text()))
        # self.win.tableWidgetSearch.cellDoubleClicked.connect(lambda: self.d_click_table_devicename(self.win.tableWidgetSearch.currentItem().text()))
        # # comboboxes
        # self.win.inComboboxDevicetype.addItems(["choose here"]+[x.__name__ for x in valid_devices])
        # self.win.inComboboxDevicetype.currentIndexChanged.connect(lambda: self.update_combobox(self.win.inComboBoxRegisterOS, valid_devices[self.win.inComboboxDevicetype.currentIndex()-1].expected_OS))
        # # btns
        # self.win.btSearch.clicked.connect(lambda: self.validate(self.search, [self.win.inUserSearch], checkregistered=True))
        # self.win.btRegisterNew.clicked.connect(lambda: self.win.stackedWidget.setCurrentWidget(self.win.pRegister))
        # self.win.btRegister.clicked.connect(lambda: self.validate(self.register, line_edit_list=[self.win.inUsername, self.win.inDevicename],
        #                                                       combo_box_list=[self.win.inComboboxDevicetype, self.win.inComboBoxRegisterOS],
        #                                                       forbidden=list(registered_devices.keys()), checkfname=True))
        # self.win.btChange.clicked.connect(lambda: self.validate(self.change, data=2, checkregistered=True))
        # self.win.btCreate.clicked.connect(lambda: self.validate(self.new, [self.inNewFilepath, self.inNewFilename], data=False))
        # self.win.btModNewPath.clicked.connect(lambda: self.new(True))
        # # menu bar
        # self.win.actionSearch.triggered.connect(lambda: self.win.stackedWidget.setCurrentWidget(self.win.pSearch))
        # self.win.actionRegister.triggered.connect(lambda: self.win.stackedWidget.setCurrentWidget(self.win.pRegister))
        # self.win.actionChange.triggered.connect(lambda: self.change(0))
        # self.win.actionOpen.triggered.connect(lambda: self.open(False))
        # self.win.actionSave.triggered.connect(self.save)
        # self.win.actionNew.triggered.connect(lambda: self.new(True))
        # # cancel
        # self.win.btCancelRegister.clicked.connect(lambda: self.cancel([self.win.inUsername, self.win.inDevicename, self.win.inComboBoxRegisterOS, self.win.textEditComment]))
        # self.win.cancelSearch.clicked.connect(lambda: self.cancel([self.win.inUserSearch]))
        # self.win.btCancelChange.clicked.connect(lambda: self.cancel([self.win.inComboBoxChangeParamtype, self.win.inComboBoxChangeNewval, self.win.inChangeNewval]))
        # # funcs
        # self.update_table(self.win.tableWidgetAllRegistered, registered_devices.values())

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
        self.win.stackedWidget.setCurrentWidget(self.win.pView)

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
            self.win.inComboBoxDevicename.addItems(["choose here", referenz])
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
                    self.win.statusbar.showMessage("all comboboxes must be specified")
                    fails += 1
        if checkfname is True and self.fname is None:
            self.win.statusbar.showMessage("no file path specified, visit Ctrl+o or menuebar/edit/open to fix")
            fails += 1
        if checkregistered is True and len(registered_devices) == 0:
            self.win.statusbar.showMessage("nothing registered yet")
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
        new = valid_devices[self.win.inComboBoxRegisterOS.currentIndex()](self.win.inDevicename.text(), self.win.inUsername.text(), self.win.textEditComment.toPlainText(), str(datetime.datetime.now()))
        new.OS = self.win.inComboBoxRegisterOS.currentText()
        registered_devices[self.win.inDevicename.text()] = new
        self.win.stackedWidget.setCurrentWidget(self.win.pView)
        self.win.inDevicename.clear()
        self.win.inUsername.clear()
        self.win.inComboBoxRegisterOS.clear()
        self.win.textEditComment.clear()
        self.update_table(self.win.tableWidgetAllRegistered, registered_devices.values())
        self.save()

    def search(self) -> None:
        """searches for a given username in registered devices and outputs on statusbar"""
        results = [x for x in registered_devices.values() if x.user == self.win.inUserSearch.text()]
        if len(results) >= 1:
            self.update_table(self.win.tableWidgetSearch, results)
            self.win.statusbar.showMessage(f"found {len(results)} match/es")
        else:
            self.win.statusbar.showMessage("nothing found")

    def change(self, x: int) -> None:
        """changes existing device parameters
        x == 0: fill combobox,
        x == 1: paramtypeIndex has changed, based on that new valtype is determined
        x == 2: retrieve data, change parameter, clear, and save
        Args:
            x: determines a which state to execute this function """
        if x == 0:
            self.win.stackedWidget.setCurrentWidget(self.win.pChange)
            if self.win.inComboBoxDevicename.count() == 0:
                self.win.inComboBoxDevicename.addItems(["choose here"] + list(registered_devices.keys()))
            self.win.inComboBoxDevicename.currentIndexChanged.connect(lambda: self.update_combobox(self.win.inComboBoxChangeParamtype, registered_devices.get(self.win.inComboBoxDevicename.currentText()).visible_attr))
            self.win.inComboBoxChangeParamtype.currentIndexChanged.connect(lambda: self.change(1))
        elif x == 1:
            if self.win.inComboBoxChangeParamtype.currentText() != "OS":
                self.win.stackedWidget2.setCurrentWidget(self.win.pLineEdit)
            else:
                self.win.stackedWidget2.setCurrentWidget(self.win.pComboBox)
                self.win.inComboBoxChangeNewval.addItems(["choose here"] + registered_devices.get(self.win.inComboBoxDevicename.currentText()).expected_OS)
        elif x == 2:
            _class = registered_devices.get(self.win.inComboBoxDevicename.currentText())
            paramtype = self.win.inComboBoxChangeParamtype.currentText()
            if paramtype == "OS":
                newval = self.win.inComboBoxChangeNewval.currentText()
            else:
                newval = self.win.inChangeNewval.text()
            setattr(_class, paramtype, newval)
            self.update_table(self.win.tableWidgetAllRegistered, registered_devices.values())
            self.win.stackedWidget.setCurrentWidget(self.win.pView)

            self.win.inComboBoxChangeParamtype.clear()
            self.win.inComboBoxChangeNewval.clear()
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
        self.update_table(self.win.tableWidgetAllRegistered, registered_devices.values())

    def save(self) -> None:
        """saves content fo registered_devices into specified csv file"""

        if not self.fname:
            self.win.statusbar.showMessage("no file path set all changes get lost if closed")
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
            self.win.stackedWidget.setCurrentWidget(self.win.pCreate)
            self.win.inNewFilepath.setText(self.dir)
        else:
            self.fname = self.dir + f"/{self.win.inNewFilename.text()}.csv"
            self.save()
            self.win.tableWidgetAllRegistered.clearContents()
            self.win.stackedWidget.setCurrentWidget(self.win.pView)


class StartScreenUi(QWidget):
    """sets up ui props of startscreen"""

    def __init__(self) -> None:
        """inits StartScreenUi class"""

        super(StartScreenUi, self).__init__()
        self.pic_label = QtWidgets.QLabel(self)
        self.pic_label.setPixmap(QPixmap("../data/startscreenPic.png"))

        self.txt_label = QtWidgets.QLabel(self)
        self.txt_label.setText("Welcome")
        font = QFont()
        font.setPointSize(19)
        font.setBold(True)
        font.setWeight(75)
        self.txt_label.setFont(font)
        self.txt_label.setAlignment(QtCore.Qt.AlignCenter)

        self.resize(507, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.pic_label)
        self.verticalLayout.addWidget(self.txt_label)
        self.setWindowIcon(QIcon("../data/favicon.ico"))


class StartScreen_logic:
    """contains startscreen logic to be displayed at begining"""
    def __init__(self) -> None:
        """inits StartScreen_logic class"""

        self.win = StartScreenUi()
        self.win.show()
        self.timer = QtCore.QTimer()
        self.timer.singleShot(1500, self.on_elapsed)

    def on_elapsed(self) -> None:
        """closes StartStartsceen Window and creates instance of MainWindow"""
        self.win.close()
        MainWindow_logic()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    startscreen = StartScreen_logic()
    sys.exit(app.exec_())
