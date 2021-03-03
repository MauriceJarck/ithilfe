from PySide2.QtGui import QPixmap, QIcon, QFont, QKeySequence
from PySide2.QtWidgets import QMainWindow, QWidget
from PySide2 import QtWidgets, QtCore


class MainWindowUi(QMainWindow):
    """sets up ui properties of MainWindowUi class"""
    def __init__(self):
        """inits MainWindowUi class"""
        super(MainWindowUi, self).__init__()
        self.resize(820, 450)
        self.setWindowIcon(QIcon("../data/favicon.ico"))

        # TODO: menu bar
        self.menuBar = self.menuBar()

        self.menuFile = self.menuBar.addMenu("file")
        self.actionOpen = QtWidgets.QAction("open")
        self.actionSave = QtWidgets.QAction("save")
        self.actionNew = QtWidgets.QAction("new")
        self.actionOpen.setShortcut(QKeySequence("Ctrl+o"))
        self.actionSave.setShortcut(QKeySequence("Ctrl+s"))

        self.menuEdit = self.menuBar.addMenu("edit")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionNew)
        self.actionRegister = QtWidgets.QAction("register")
        self.actionSearch = QtWidgets.QAction("search")
        self.actionChange = QtWidgets.QAction("change")
        self.actionRegister.setShortcut(QKeySequence("Ctrl+n"))
        self.actionSearch.setShortcut(QKeySequence("Ctrl+f"))
        self.actionChange.setShortcut(QKeySequence("Ctrl+d"))

        self.menuEdit.addAction(self.actionRegister)
        self.menuEdit.addAction(self.actionSearch)
        self.menuEdit.addAction(self.actionChange)

        # TODO: statusbar
        self.statusbar = self.statusBar()

        # TODO: stackedwidget
        self.stackedWidget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        # TODO: pview
        self.pView = QtWidgets.QWidget()
        self.stackedWidget.addWidget(self.pView)

        self.pViewTable = QtWidgets.QTableWidget(self.pView)
        self.pViewTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.pViewTable.setWordWrap(True)
        self.pViewTable.setColumnCount(7)
        self.pViewTable.setHorizontalHeaderLabels(['username', 'devname', 'devtype', 'os', "comment", "extras", "datetime"])
        self.pViewTable.horizontalHeader().setStretchLastSection(True)

        self.btRegisterNew = QtWidgets.QPushButton("register new", self.pView)

        pViewLayout = QtWidgets.QVBoxLayout(self.pView)
        pViewLayout.addWidget(self.pViewTable)
        pViewLayout.addWidget(self.btRegisterNew)

        # TODO: pRegister
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
        self.btRegister = QtWidgets.QPushButton("register",self.pRegister)
        self.btCancelRegister = QtWidgets.QPushButton("cancel",self.pRegister)

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

        # TODO: pSearch
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

        # TODO: pChange
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

        # TODO: pCreate
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


class StartScreenUi(QWidget):
    """sets up ui properties of startscreen"""

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