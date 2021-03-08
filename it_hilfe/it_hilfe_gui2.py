import csv
import datetime
import sys

from PySide2.QtGui import QPixmap, QIcon, QFont, QKeySequence
from PySide2.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PySide2.QtWidgets import QMainWindow, QWidget, QApplication, QFileDialog
from PySide2 import QtWidgets, QtCore
import it_hilfe.devices as devices
import it_hilfe.it_hilfe_logic as logic

registered_devices = {}
valid_devices = [devices.WindowsLapTop, devices.WindowsWorkStation, devices.Macbook]

class MainWindowUi(QMainWindow):
    """sets up ui properties of MainWindowUi class"""
    def __init__(self):
        """inits MainWindow class

                  configuring parameters of MainWindow class and inherits from QtWidget.QMainWindow
                  loads .ui file sets up file and directory path vars, inits click events(menuebar, coboboxes, btns) and
                  shows gui the first time

                  """
        super(MainWindowUi, self).__init__()
        self.resize(820, 450)
        self.setWindowIcon(QIcon("../data/favicon.ico"))
        self.fname = None
        self.dir = None

        # setup statusbar
        self.statusbar = self.statusBar()
        # setup stackedwidget
        self.stackedWidget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stackedWidget)
        # setup rest
        self.setup_menubar()
        self.setup_pView()
        self.setup_pRegister()
        self.setup_pSearch()
        self.setup_pChange()
        self.setup_pCreate()
        self.setup_signals()

        self.show()
        self.stackedWidget.setCurrentWidget(self.pView)
        self.update_table(self.pViewTable, registered_devices.values())

    def setup_menubar(self):
        self.menuBar = self.menuBar()

        self.menuFile = self.menuBar.addMenu("file")
        self.actionOpen = QtWidgets.QAction("open")
        self.actionSave = QtWidgets.QAction("save")
        self.actionNew = QtWidgets.QAction("new")
        self.actionPrint = QtWidgets.QAction("print")
        self.actionPrint.setShortcut(QKeySequence("Ctrl+p"))
        self.actionOpen.setShortcut(QKeySequence("Ctrl+o"))
        self.actionSave.setShortcut(QKeySequence("Ctrl+s"))
        self.actionPrint.setIcon(QIcon("../data/print.ico"))
        self.actionOpen.setIcon(QIcon("../data/open.ico"))
        self.actionSave.setIcon(QIcon("../data/save.ico"))
        self.actionNew.setIcon(QIcon("../data/newfile.ico"))

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionPrint)

        self.menuEdit = self.menuBar.addMenu("edit")
        self.actionRegister = QtWidgets.QAction("register")
        self.actionSearch = QtWidgets.QAction("search")
        self.actionChange = QtWidgets.QAction("change")
        self.actionRegister.setShortcut(QKeySequence("Ctrl+n"))
        self.actionSearch.setShortcut(QKeySequence("Ctrl+f"))
        self.actionChange.setShortcut(QKeySequence("Ctrl+d"))
        self.actionSearch.setIcon(QIcon("../data/search.ico"))
        self.actionChange.setIcon(QIcon("../data/change.ico"))
        self.actionRegister.setIcon(QIcon("../data/register.ico"))

        self.menuEdit.addAction(self.actionRegister)
        self.menuEdit.addAction(self.actionSearch)
        self.menuEdit.addAction(self.actionChange)

    def setup_pView(self):
        self.pView = QtWidgets.QWidget()
        self.stackedWidget.addWidget(self.pView)

        self.pViewTable = QtWidgets.QTableWidget(self.pView)
        self.pViewTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.pViewTable.setWordWrap(True)
        self.pViewTable.setColumnCount(7)
        self.pViewTable.setHorizontalHeaderLabels(
            ['username', 'devname', 'devtype', 'os', "comment", "extras", "datetime"])
        self.pViewTable.horizontalHeader().setStretchLastSection(True)

        self.btRegisterNew = QtWidgets.QPushButton("register new", self.pView)

        pViewLayout = QtWidgets.QVBoxLayout(self.pView)
        pViewLayout.addWidget(self.pViewTable)
        pViewLayout.addWidget(self.btRegisterNew)

    def setup_pRegister(self):
        self.pRegister = QtWidgets.QWidget()
        self.stackedWidget.addWidget(self.pRegister)

        self.lUser = QtWidgets.QLabel("Username", self.pRegister)
        self.inUsername = QtWidgets.QLineEdit(self.pRegister)
        self.lDeviceName = QtWidgets.QLabel("Devicename", self.pRegister)
        self.inDevicename = QtWidgets.QLineEdit(self.pRegister)
        self.lDeviceType = QtWidgets.QLabel("DeviceType", self.pRegister)
        self.inComboboxDevicetype = QtWidgets.QComboBox(self.pRegister)
        self.lOs = QtWidgets.QLabel("OS", self.pRegister)
        self.inComboboxOs = QtWidgets.QComboBox(self.pRegister)
        self.lComment = QtWidgets.QLabel("Comment", self.pRegister)
        self.textEditComment = QtWidgets.QTextEdit(self.pRegister)
        self.btRegister = QtWidgets.QPushButton("register", self.pRegister)
        self.btCancelRegister = QtWidgets.QPushButton("cancel", self.pRegister)

        pRegisterLayout = QtWidgets.QVBoxLayout(self.pRegister)
        pRegisterLayout.addWidget(self.lUser)
        pRegisterLayout.addWidget(self.inUsername)
        pRegisterLayout.addWidget(self.lDeviceName)
        pRegisterLayout.addWidget(self.inDevicename)
        pRegisterLayout.addWidget(self.lDeviceType)
        pRegisterLayout.addWidget(self.inComboboxDevicetype)
        pRegisterLayout.addWidget(self.lOs)
        pRegisterLayout.addWidget(self.inComboboxOs)
        pRegisterLayout.addWidget(self.lComment)
        pRegisterLayout.addWidget(self.textEditComment)
        pRegisterLayout.addWidget(self.btRegister)
        pRegisterLayout.addWidget(self.btCancelRegister)

    def setup_pSearch(self):
        self.pSearch = QtWidgets.QWidget()
        self.stackedWidget.addWidget(self.pSearch)

        self.lUserSearch = QtWidgets.QLabel("Enter username to search for", self.pSearch)
        self.inUserSearch = QtWidgets.QLineEdit(self.pSearch)
        self.lOutputsearch = QtWidgets.QLabel("Output", self.pSearch)
        self.btSearch = QtWidgets.QPushButton("search", self.pSearch)
        self.btCancelSearch = QtWidgets.QPushButton("cancel", self.pSearch)
        self.pSearchTable = QtWidgets.QTableWidget(self.pSearch)
        self.pSearchTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.pSearchTable.setWordWrap(True)
        self.pSearchTable.setColumnCount(7)
        self.pSearchTable.setHorizontalHeaderLabels(['username', 'devname', 'devtype', 'os', "comment", "extras", "datetime"])
        self.pSearchTable.horizontalHeader().setStretchLastSection(True)

        pSearchLayout = QtWidgets.QVBoxLayout(self.pSearch)
        pSearchLayout.addWidget(self.lUserSearch)
        pSearchLayout.addWidget(self.inUserSearch)
        pSearchLayout.addWidget(self.lOutputsearch)
        pSearchLayout.addWidget(self.pSearchTable)
        pSearchLayout.addWidget(self.btSearch)
        pSearchLayout.addWidget(self.btCancelSearch)

    def setup_pChange(self):
        self.pChange = QtWidgets.QWidget()
        self.stackedWidget.addWidget(self.pChange)

        self.pLineEdit = QtWidgets.QWidget()
        self.pComboBox = QtWidgets.QWidget()
        self.changeStackedWidget = QtWidgets.QStackedWidget(self.pChange)
        self.changeStackedWidget.addWidget(self.pLineEdit)
        self.changeStackedWidget.addWidget(self.pComboBox)

        self.lChangeDevice = QtWidgets.QLabel("devicename", self.pChange)
        self.inComboBoxDevicename = QtWidgets.QComboBox(self.pChange)
        self.lChangeParamtype = QtWidgets.QLabel("Paramtype", self.pChange)
        self.inComboBoxChangeParamtype = QtWidgets.QComboBox(self.pChange)
        self.lChangeNewVal = QtWidgets.QLabel("new value", self.pChange)
        self.inComboBoxChangeNewval = QtWidgets.QComboBox(self.pComboBox)
        self.inChangeNewval = QtWidgets.QLineEdit(self.pLineEdit)
        self.btChange = QtWidgets.QPushButton("change", self.pChange)
        self.btCancelChange = QtWidgets.QPushButton("cancel", self.pChange)

        pChangeLayout = QtWidgets.QVBoxLayout(self.pChange)
        pChangeLayout.addWidget(self.lChangeDevice)
        pChangeLayout.addWidget(self.inComboBoxDevicename)
        pChangeLayout.addWidget(self.lChangeParamtype)
        pChangeLayout.addWidget(self.inComboBoxChangeParamtype)
        pChangeLayout.addWidget(self.lChangeNewVal)
        pChangeLayout.addWidget(self.changeStackedWidget)
        pChangeLayout.addStretch(100)
        pChangeLayout.addWidget(self.btChange)
        pChangeLayout.addWidget(self.btCancelChange)

        changeStackedWidgetlayout = QtWidgets.QVBoxLayout(self.pComboBox)
        changeStackedWidgetlayout2 = QtWidgets.QVBoxLayout(self.pLineEdit)
        changeStackedWidgetlayout.addWidget(self.inComboBoxChangeNewval)
        changeStackedWidgetlayout2.addWidget(self.inChangeNewval)

    def setup_pCreate(self):
        self.pCreate = QtWidgets.QWidget()
        self.stackedWidget.addWidget(self.pCreate)

        self.lNewFilepath = QtWidgets.QLabel("new filepath", self.pCreate)
        self.btModNewPath = QtWidgets.QPushButton("mod filepath", self.pCreate)
        self.inNewFilepath = QtWidgets.QLineEdit(self.pCreate)
        self.lNewFilename = QtWidgets.QLabel("new filename", self.pCreate)
        self.inNewFilename = QtWidgets.QLineEdit(self.pCreate)
        self.btCreate = QtWidgets.QPushButton("create", self.pCreate)
        self.btCancelCreate = QtWidgets.QPushButton("cancel", self.pCreate)

        pCreateLayout = QtWidgets.QVBoxLayout(self.pCreate)
        pCreateLayout.addWidget(self.lNewFilepath)
        pCreateLayout.addWidget(self.inNewFilepath)
        pCreateLayout.addWidget(self.lNewFilename)
        pCreateLayout.addWidget(self.inNewFilename)
        pCreateLayout.addStretch(100)
        pCreateLayout.addWidget(self.btModNewPath)
        pCreateLayout.addWidget(self.btCreate)
        pCreateLayout.addWidget(self.btCancelCreate)

    def setup_signals(self):
        # return pressed
        self.inUserSearch.returnPressed.connect(
            lambda: self.validate(self.search, [self.inUserSearch], checkregistered=True))
        self.inChangeNewval.returnPressed.connect(lambda: self.validate(self.change, data=2, checkregistered=True))
        self.inNewFilename.returnPressed.connect(
            lambda: self.validate(self.new, [self.inNewFilepath, self.inNewFilename], data=False))
        # doubleclick
        self.pViewTable.cellDoubleClicked.connect(
            lambda: self.d_click_table_devicename(self.pViewTable.currentItem().text()))
        self.pSearchTable.cellDoubleClicked.connect(
            lambda: self.d_click_table_devicename(self.pSearchTable.currentItem().text()))
        # comboboxes
        self.inComboboxDevicetype.addItems(["choose here"] + [x.__name__ for x in valid_devices])
        self.inComboboxDevicetype.currentIndexChanged.connect(lambda: self.update_combobox(self.inComboboxOs,
                                                                                               valid_devices[
                                                                                                   self.inComboboxDevicetype.currentIndex() - 1].expected_OS))
        # btns
        self.btSearch.clicked.connect(
            lambda: self.validate(self.search, [self.inUserSearch], checkregistered=True))
        self.btRegisterNew.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pRegister))
        self.btRegister.clicked.connect(
            lambda: self.validate(self.register, line_edit_list=[self.inUsername, self.inDevicename],
                                  combo_box_list=[self.inComboboxDevicetype, self.inComboboxOs],
                                  forbidden=list(registered_devices.keys()), checkfname=True))
        self.btChange.clicked.connect(lambda: self.validate(self.change, data=2, checkregistered=True))
        self.btCreate.clicked.connect(
            lambda: self.validate(self.new, [self.inNewFilepath, self.inNewFilename], data=False))
        self.btModNewPath.clicked.connect(lambda: self.new(True))
        # menu bar
        self.actionSearch.triggered.connect(lambda: self.stackedWidget.setCurrentWidget(self.pSearch))
        self.actionRegister.triggered.connect(lambda: self.stackedWidget.setCurrentWidget(self.pRegister))
        self.actionChange.triggered.connect(lambda: self.change(0))
        self.actionOpen.triggered.connect(lambda: self.open(False))
        self.actionSave.triggered.connect(self.save)
        self.actionNew.triggered.connect(lambda: self.new(True))
        self.actionPrint.triggered.connect(lambda: self.validate(self.print, data=False, checkfname=True))
        # # cancel
        self.btCancelRegister.clicked.connect(lambda: self.cancel(
            [self.inUsername, self.inDevicename, self.inComboboxOs, self.textEditComment]))
        self.btCancelSearch.clicked.connect(lambda: self.cancel([self.inUserSearch]))
        self.btCancelChange.clicked.connect(lambda: self.cancel(
            [self.inComboBoxChangeParamtype, self.inComboBoxChangeNewval, self.inChangeNewval]))

    def cancel(self, widgets: list) -> None:
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
        logic.register(self.inDevicename.text(), valid_devices[self.inComboboxOs.currentIndex()],
                       self.inUsername.text(), self.inComboboxOs.currentText(), self.textEditComment.toPlainText(),
                       str(datetime.datetime.now()), registered_devices)
        self.stackedWidget.setCurrentWidget(self.pView)
        self.inDevicename.clear()
        self.inUsername.clear()
        self.inComboboxOs.clear()
        self.textEditComment.clear()
        self.update_table(self.pViewTable, registered_devices.values())
        self.save()

    def search(self) -> None:
        """searches for a given username in registered devices and outputs on statusbar"""
        results = logic.search(self.inUserSearch.text(), registered_devices)
        if len(results) >= 1:
            self.update_table(self.pSearchTable, results)
            self.statusbar.showMessage(f"found {len(results)} match/es")
        else:
            self.statusbar.showMessage("nothing found")

    def change(self, x: int) -> None:
        """changes existing device parameters
        x == 0: fill combobox,
        x == 1: paramtypeIndex has changed, based on that the new valtype is determined
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
                self.changeStackedWidget.setCurrentWidget(self.pLineEdit)
                self.statusbar.showMessage(f"current username: {registered_devices.get(self.inComboBoxDevicename.currentText()).user}")
            else:
                self.changeStackedWidget.setCurrentWidget(self.pComboBox)
                self.inComboBoxChangeNewval.addItems(["choose here"] + registered_devices.get(self.inComboBoxDevicename.currentText()).expected_OS)
                self.statusbar.showMessage(f"current os: {registered_devices.get(self.inComboBoxDevicename.currentText()).OS}")
        elif x == 2:
            _class = registered_devices.get(self.inComboBoxDevicename.currentText())
            paramtype = self.inComboBoxChangeParamtype.currentText()
            if paramtype == "OS":
                newval = self.inComboBoxChangeNewval.currentText()
            else:
                newval = self.inChangeNewval.text()
            logic.change_param(self.inComboBoxDevicename.currentText(), paramtype, newval, registered_devices)
            # self.inComboBoxDevicename.clear()
            self.inComboBoxChangeParamtype.clear()
            self.inComboBoxChangeNewval.clear()
            self.update_table(self.pViewTable, registered_devices.values())
            self.stackedWidget.setCurrentWidget(self.pView)
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

        self.statusbar.showMessage("")
        self.update_table(self.pViewTable, registered_devices.values())

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

    def new(self, stage: bool, test: bool=False) -> None:
        """creates new csv file to save into

        stage is True: set filepath
        stage is False: set new name, save
        Args:
            stage: determines a which stage to execute this function """
        if stage is True:
            if not test:
                self.dir = QFileDialog.getExistingDirectory(self, "select a folder", "c://")
            self.stackedWidget.setCurrentWidget(self.pCreate)
            self.inNewFilepath.setText(self.dir)
            registered_devices.clear()

        else:
            self.fname = self.dir + f"/{self.inNewFilename.text()}.csv"
            self.save()
            self.pViewTable.clearContents()
            self.stackedWidget.setCurrentWidget(self.pView)

    def print(self, test) -> None:
        """setup and preview pViewTable for paper printing"""
        with open(self.fname) as f:
            text = " ".join(f.readlines())
        self.document = QtWidgets.QTextEdit()
        self.document.setText(text)

        if not test:
            printer = QPrinter()
            previewDialog = QPrintPreviewDialog(printer, self)
            previewDialog.paintRequested.connect(lambda: self.document.print_(printer))
            previewDialog.exec_()
class StartScreenUi(QWidget):
    """sets up ui properties of startscreen"""

    def __init__(self) -> None:
        """inits StartScreenUi class"""
        super(StartScreenUi, self).__init__()
        self.setup_startscreen()
        self.show()

        self.timer = QtCore.QTimer()
        self.timer.singleShot(1500, self.on_elapsed)

    def on_elapsed(self) -> None:
        """closes StartStartsceen Window and creates instance of MainWindow"""
        self.close()
        self.main = MainWindowUi()

    def setup_startscreen(self):
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    startscreen = StartScreenUi()
    sys.exit(app.exec_())