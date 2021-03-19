import datetime
import json
import sys

from PySide2.QtCore import QSortFilterProxyModel
from PySide2.QtGui import QPixmap, QIcon, QFont, QKeySequence, Qt, QStandardItemModel, QStandardItem
from PySide2.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PySide2.QtWidgets import QMainWindow, QWidget, QApplication, QFileDialog, QHBoxLayout
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
        self.setWindowIcon(QIcon("./data/favicon.ico"))
        self.file_path = None
        self.dir = None

        # setup statusbar
        self.statusbar = self.statusBar()
        # setup stackedwidget
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        # setup rest
        self.setup_menubar()
        self.setup_p_view()
        self.setup_p_register()
        # self.setup_pChange()
        self.setup_p_create()
        self.setup_signals()

        self.show()
        self.stacked_widget.setCurrentWidget(self.p_view)

    def setup_menubar(self):
        self.menu_Bar = self.menuBar()

        menu_file = self.menu_Bar.addMenu("file")
        self.action_open = QtWidgets.QAction("open")
        self.action_save = QtWidgets.QAction("save")
        self.action_new = QtWidgets.QAction("new")
        self.action_print = QtWidgets.QAction("print")
        self.action_print.setShortcut(QKeySequence("Ctrl+p"))
        self.action_open.setShortcut(QKeySequence("Ctrl+o"))
        self.action_save.setShortcut(QKeySequence("Ctrl+s"))
        self.action_print.setIcon(QIcon("./data/print.ico"))
        self.action_open.setIcon(QIcon("./data/open.ico"))
        self.action_save.setIcon(QIcon("./data/save.ico"))
        self.action_new.setIcon(QIcon("./data/newfile.ico"))

        menu_file.addAction(self.action_open)
        menu_file.addAction(self.action_save)
        menu_file.addAction(self.action_new)
        menu_file.addAction(self.action_print)

        menu_edit = self.menu_Bar.addMenu("edit")
        self.action_register = QtWidgets.QAction("register")
        self.action_search = QtWidgets.QAction("search")
        self.action_change = QtWidgets.QAction("change")
        self.action_register.setShortcut(QKeySequence("Ctrl+n"))
        self.action_search.setShortcut(QKeySequence("Ctrl+f"))
        self.action_change.setShortcut(QKeySequence("Ctrl+d"))
        self.action_search.setIcon(QIcon("./data/search.ico"))
        self.action_change.setIcon(QIcon("./data/change.ico"))
        self.action_register.setIcon(QIcon("./data/register.ico"))

        menu_edit.addAction(self.action_register)
        menu_edit.addAction(self.action_search)
        menu_edit.addAction(self.action_change)

    def setup_p_view(self):
        self.p_view = QtWidgets.QWidget()
        self.stacked_widget.addWidget(self.p_view)

        # TODO header labels:
        self.model = QStandardItemModel(self.p_view)
        self.model.setHorizontalHeaderLabels(["0", "1", "2"])

        self.filter = QSortFilterProxyModel()
        self.filter.setSourceModel(self.model)
        self.filter.setFilterKeyColumn(0)
        self.filter.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self.table = QtWidgets.QTableView(self.p_view)
        self.table.setModel(self.filter)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSortingEnabled(True)
        
        # TODO search labels
        self.p_view_search_line_edit = QtWidgets.QLineEdit(self.p_view)
        self.p_view_combo_search_key = QtWidgets.QComboBox(self.p_view)
        self.p_view_combo_search_key.addItems(["column 0", "column 1", "column 2"])
        self.bt_register_new = QtWidgets.QPushButton("register new", self.p_view)

        p_view_layout = QtWidgets.QVBoxLayout(self.p_view)
        h_layout = QHBoxLayout(self.p_view)
        h_layout.addWidget(self.p_view_search_line_edit)
        h_layout.addWidget(self.p_view_combo_search_key)

        p_view_layout.addWidget(self.table)
        # p_view_layout.addWidget(self.p_view_search_line_edit)
        # p_view_layout.addWidget(self.p_view_combo_search_key)
        p_view_layout.addLayout(h_layout)
        p_view_layout.addWidget(self.bt_register_new)
        self.p_view.setLayout(p_view_layout)


    def setup_p_register(self):
        self.p_register = QtWidgets.QWidget()
        self.stacked_widget.addWidget(self.p_register)

        l_user = QtWidgets.QLabel("Username", self.p_register)
        self.in_username = QtWidgets.QLineEdit(self.p_register)
        l_devicename = QtWidgets.QLabel("Devicename", self.p_register)
        self.in_devicename = QtWidgets.QLineEdit(self.p_register)
        l_devicetype = QtWidgets.QLabel("DeviceType", self.p_register)
        self.in_combobox_devicetype = QtWidgets.QComboBox(self.p_register)
        l_os = QtWidgets.QLabel("OS", self.p_register)
        self.in_combobox_os = QtWidgets.QComboBox(self.p_register)
        l_comment = QtWidgets.QLabel("Comment", self.p_register)
        self.text_edit_comment = QtWidgets.QTextEdit(self.p_register)
        self.bt_register = QtWidgets.QPushButton("register", self.p_register)
        self.bt_cancel_register = QtWidgets.QPushButton("cancel", self.p_register)

        p_register_layout = QtWidgets.QVBoxLayout(self.p_register)
        p_register_layout.addWidget(l_user)
        p_register_layout.addWidget(self.in_username)
        p_register_layout.addWidget(l_devicename)
        p_register_layout.addWidget(self.in_devicename)
        p_register_layout.addWidget(l_devicetype)
        p_register_layout.addWidget(self.in_combobox_devicetype)
        p_register_layout.addWidget(l_os)
        p_register_layout.addWidget(self.in_combobox_os)
        p_register_layout.addWidget(l_comment)
        p_register_layout.addWidget(self.text_edit_comment)
        p_register_layout.addWidget(self.bt_register)
        p_register_layout.addWidget(self.bt_cancel_register)
    
    # TODO: still necessary?
    def setup_p_change(self):
        self.p_change = QtWidgets.QWidget()
        self.stacked_widget.addWidget(self.p_change)

        self.p_line_edit = QtWidgets.QWidget()
        self.p_combo_box = QtWidgets.QWidget()
        self.change_stacked_widget = QtWidgets.QStackedWidget(self.p_change)
        self.change_stacked_widget.addWidget(self.p_line_edit)
        self.change_stacked_widget.addWidget(self.p_combo_box)

        self.l_change_device = QtWidgets.QLabel("devicename", self.p_change)
        self.inComboBoxDevicename = QtWidgets.QComboBox(self.p_change)
        self.lChangeParamtype = QtWidgets.QLabel("Paramtype", self.p_change)
        self.inComboBoxChangeParamtype = QtWidgets.QComboBox(self.p_change)
        self.lChangeNewVal = QtWidgets.QLabel("new value", self.p_change)
        self.inComboBoxChangeNewval = QtWidgets.QComboBox(self.p_combo_box)
        self.inChangeNewval = QtWidgets.QLineEdit(self.p_line_edit)
        self.btChange = QtWidgets.QPushButton("change", self.p_change)
        self.btCancelChange = QtWidgets.QPushButton("cancel", self.p_change)

        pChangeLayout = QtWidgets.QVBoxLayout(self.p_change)
        pChangeLayout.addWidget(self.l_change_device)
        pChangeLayout.addWidget(self.inComboBoxDevicename)
        pChangeLayout.addWidget(self.lChangeParamtype)
        pChangeLayout.addWidget(self.inComboBoxChangeParamtype)
        pChangeLayout.addWidget(self.lChangeNewVal)
        pChangeLayout.addWidget(self.change_stacked_widget)
        pChangeLayout.addStretch(100)
        pChangeLayout.addWidget(self.btChange)
        pChangeLayout.addWidget(self.btCancelChange)

        changeStackedWidgetlayout = QtWidgets.QVBoxLayout(self.p_combo_box)
        changeStackedWidgetlayout2 = QtWidgets.QVBoxLayout(self.p_line_edit)
        changeStackedWidgetlayout.addWidget(self.inComboBoxChangeNewval)
        changeStackedWidgetlayout2.addWidget(self.inChangeNewval)

    def setup_p_create(self):
        self.p_create = QtWidgets.QWidget()
        self.stacked_widget.addWidget(self.p_create)

        l_new_filepath = QtWidgets.QLabel("new filepath", self.p_create)
        self.bt_mod_new_path = QtWidgets.QPushButton("mod filepath", self.p_create)
        self.in_new_filepath = QtWidgets.QLineEdit(self.p_create)
        l_new_filename = QtWidgets.QLabel("new filename", self.p_create)
        self.in_new_filename = QtWidgets.QLineEdit(self.p_create)
        self.bt_create = QtWidgets.QPushButton("create", self.p_create)
        self.bt_cancel_create = QtWidgets.QPushButton("cancel", self.p_create)

        p_create_layout = QtWidgets.QVBoxLayout(self.p_create)
        p_create_layout.addWidget(l_new_filepath)
        p_create_layout.addWidget(self.in_new_filepath)
        p_create_layout.addWidget(l_new_filename)
        p_create_layout.addWidget(self.in_new_filename)
        p_create_layout.addStretch(100)
        p_create_layout.addWidget(self.bt_mod_new_path)
        p_create_layout.addWidget(self.bt_create)
        p_create_layout.addWidget(self.bt_cancel_create)

    def setup_signals(self):
        # return pressed
        
        # line edit
        self.p_view_search_line_edit.textChanged.connect(self.filter.setFilterRegExp)

        # self.inChangeNewval.returnPressed.connect(lambda: self.validate(self.change, data=2, checkregistered=True))
        self.in_new_filename.returnPressed.connect(
            lambda: self.validate(self.new, [self.in_new_filepath, self.in_new_filename], data=False))

        # comboboxes
        self.in_combobox_devicetype.addItems(["choose here"] + [x.__name__ for x in valid_devices])
        self.in_combobox_devicetype.currentIndexChanged.connect(lambda: self.update_combobox(self.in_combobox_os,
                                                                                               valid_devices[
                                                                                                   self.in_combobox_devicetype.currentIndex() - 1].expected_OS))
        self.p_view_combo_search_key.currentIndexChanged.connect(lambda: self.filter.setFilterKeyColumn
                                                                        (self.p_view_combo_search_key.currentIndex()))

        # btns
        self.bt_register_new.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.p_register))
        self.bt_register.clicked.connect(
            lambda: self.validate(self.register, line_edit_list=[self.in_username, self.in_devicename],
                                  combo_box_list=[self.in_combobox_devicetype, self.in_combobox_os],
                                  forbidden=list(registered_devices.keys()), checkfname=True))
        # self.btChange.clicked.connect(lambda: self.validate(self.change, data=2, checkregistered=True))
        self.bt_create.clicked.connect(
            lambda: self.validate(self.new, [self.in_new_filepath, self.in_new_filename], data=False))
        self.bt_mod_new_path.clicked.connect(lambda: self.new(True))
        # menu bar
        self.action_search.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.pSearch))
        self.action_register.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.p_register))
        self.action_change.triggered.connect(lambda: self.change(0))
        self.action_open.triggered.connect(lambda: self.open(False))
        self.action_save.triggered.connect(self.save)
        self.action_new.triggered.connect(lambda: self.new(True))
        self.action_print.triggered.connect(lambda: self.validate(self.print, data=False, checkfname=True))
        # # cancel
        self.bt_cancel_register.clicked.connect(lambda: self.cancel(
            [self.in_username, self.in_devicename, self.in_combobox_os, self.text_edit_comment]))
        # self.btCancelChange.clicked.connect(lambda: self.cancel(
        #     [self.inComboBoxChangeParamtype, self.inComboBoxChangeNewval, self.inChangeNewval]))

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
        self.stacked_widget.setCurrentWidget(self.p_view)

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

    # TODO: json file validation
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
        if checkfname is True and self.file_path is None:
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
        """registers a new device and saves it in csv"""
        logic.register(self.in_devicename.text(), valid_devices[self.in_combobox_os.currentIndex()],
                       self.in_username.text(), self.in_combobox_os.currentText(), self.text_edit_comment.toPlainText(),
                       str(datetime.datetime.now()), registered_devices)
        self.model._data.append([self.in_devicename.text(),self.in_username.text(),  str(valid_devices[self.in_combobox_os.currentIndex()].__name__),
                       self.in_combobox_os.currentText(), self.text_edit_comment.toPlainText(),
                       str(datetime.datetime.now())])
        print(valid_devices[self.in_combobox_os.currentIndex()].__name__)
        self.model.layoutChanged.emit()
        self.stacked_widget.setCurrentWidget(self.p_view)
        self.in_devicename.clear()
        self.in_username.clear()
        self.in_combobox_os.clear()
        self.text_edit_comment.clear()
        self.save()

    def change(self, x: int) -> None:
        """changes existing device parameters
        x == 0: fill combobox,
        x == 1: paramtypeIndex has changed, based on that the new valtype is determined
        x == 2: retrieve data, change parameter, clear, and save

        Args:
            x: determines a which state to execute this function """
        if x == 0:
            self.stacked_widget.setCurrentWidget(self.p_change)
            if self.inComboBoxDevicename.count() == 0:
                self.inComboBoxDevicename.addItems(["choose here"] + list(registered_devices.keys()))
            self.inComboBoxDevicename.currentIndexChanged.connect(lambda: self.update_combobox(self.inComboBoxChangeParamtype, registered_devices.get(self.inComboBoxDevicename.currentText()).visible_attr))
            self.inComboBoxChangeParamtype.currentIndexChanged.connect(lambda: self.change(1))
        elif x == 1:
            if self.inComboBoxChangeParamtype.currentText() != "OS":
                self.change_stacked_widget.setCurrentWidget(self.p_line_edit)
                self.statusbar.showMessage(f"current username: {registered_devices.get(self.inComboBoxDevicename.currentText()).user}")
            else:
                self.change_stacked_widget.setCurrentWidget(self.p_combo_box)
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
            self.stacked_widget.setCurrentWidget(self.p_view)
            self.save()

    def open(self, test: bool) -> None:
        """opens csv file and loads its content into registered devices
        Args:
            test: skip filedialog if unittested aka test == True, fname has to be set in test script"""

        registered_devices.clear()
        if not test:
            self.file_path = QFileDialog.getOpenFileName(self, "open file", "c://", "json files (*json)")[0]
        with open(self.file_path, "r") as file:

            data = dict(json.load(file)).values()
            for value in data:
                row = []
                for item in value:
                    cell = QStandardItem(str(item))
                    row.append(cell)
                self.model.appendRow(row)

        self.statusbar.showMessage("")

    def save(self) -> None:
        """saves content fo registered_devices into specified csv file"""

        if not self.file_path:
            self.statusbar.showMessage("no file path set all changes get lost if closed")
        else:
            with open(self.file_path, 'w',) as file:
                data = {k: v for (k, v) in enumerate(self.model._data)}
                json.dump(data, file)


    def new(self, stage: bool, test: bool=False) -> None:
        """creates new csv file to save into

        stage is True: set filepath
        stage is False: set new name, save
        Args:
            stage: determines a which stage to execute this function """
        if stage is True:
            if not test:
                self.dir = QFileDialog.getExistingDirectory(self, "select a folder", "c://")
            self.stacked_widget.setCurrentWidget(self.p_create)
            self.in_new_filepath.setText(self.dir)
            registered_devices.clear()

        else:
            self.file_path = self.dir + f"/{self.in_new_filename.text()}.json"
            self.save()
            self.stacked_widget.setCurrentWidget(self.p_view)

    def print(self, test) -> None:
        """setup and preview pViewTable for paper printing"""
        with open(self.file_path) as f:
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
        self.pic_label.setPixmap(QPixmap("./data/startscreenPic.png"))

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
        self.setWindowIcon(QIcon("./data/favicon.ico"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    startscreen = StartScreenUi()
    sys.exit(app.exec_())