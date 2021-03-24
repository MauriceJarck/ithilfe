import datetime
import json
import sys

from PySide2.QtCore import QSortFilterProxyModel, Slot, SIGNAL, SLOT
from PySide2.QtGui import QPixmap, QIcon, QFont, QKeySequence, Qt, QStandardItemModel, QStandardItem
from PySide2.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PySide2.QtWidgets import QMainWindow, QWidget, QApplication, QFileDialog, QItemDelegate, QComboBox, QLineEdit, QHeaderView
from PySide2 import QtWidgets, QtCore

import it_hilfe.devices as devices
import it_hilfe.it_hilfe_logic as logic

registered_devices = {}
valid_devices = [devices.WindowsLapTop, devices.WindowsWorkStation, devices.Macbook]
labels = ['devname', 'username', 'os', 'devtype', "comment", "datetime", "extras"]


class FilterHeader(QHeaderView):
    """handels line edits for filtering in tableview self.header

    Returns:
            None"""
    filterActivated = QtCore.Signal(int)
    """custom signal carrying index of last combobox"""

    def __init__(self, parent):
        """inits FilterHeader class"""
        super().__init__(QtCore.Qt.Horizontal, parent)
        self._editors = []
        self.setStretchLastSection(True)
        self.setDefaultAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.setSortIndicatorShown(False)
        self.sectionResized.connect(self.adjust_in_filter_positions)

    def set_filter_boxes(self, count: int) -> None:
        """sets up line edit boxes for live filtering tableView

        Returns:
            None"""
        while self._editors:
            editor = self._editors.pop()
            editor.deleteLater()

        editor0 = QLineEdit(self.parent())
        editor0.setPlaceholderText('Filter')
        editor0.textChanged.connect(lambda: self.filterActivated.emit(0))

        editor1 = QLineEdit(self.parent())
        editor1.setPlaceholderText('Filter')
        editor1.textChanged.connect(lambda: self.filterActivated.emit(1))

        editor2 = QLineEdit(self.parent())
        editor2.setPlaceholderText('Filter')
        editor2.textChanged.connect(lambda: self.filterActivated.emit(2))

        editor3 = QLineEdit(self.parent())
        editor3.setPlaceholderText('Filter')
        editor3.textChanged.connect(lambda: self.filterActivated.emit(3))

        editor4 = QLineEdit(self.parent())
        editor4.setPlaceholderText('Filter')
        editor4.textChanged.connect(lambda: self.filterActivated.emit(4))

        editor5 = QLineEdit(self.parent())
        editor5.setPlaceholderText('Filter')
        editor5.textChanged.connect(lambda: self.filterActivated.emit(5))

        editor6 = QLineEdit(self.parent())
        editor6.setPlaceholderText('Filter')
        editor6.textChanged.connect(lambda: self.filterActivated.emit(6))

        self._editors.append(editor0)
        self._editors.append(editor1)
        self._editors.append(editor2)
        self._editors.append(editor3)
        self._editors.append(editor4)
        self._editors.append(editor5)
        self._editors.append(editor6)



    def sizeHint(self) -> int:
        """returns height of headerView

        Returns:
            size: describes the height of headerView"""
        size = super().sizeHint()
        if self._editors:
            height = self._editors[0].sizeHint().height()
            size.setHeight(size.height() + height)
        return size

    def updateGeometries(self) -> None:
        """sets viewport of geometries

        Returns:
            None"""

        if self._editors:
            height = self._editors[0].sizeHint().height()
            self.setViewportMargins(0, 0, 0, height)
        else:
            self.setViewportMargins(0, 0, 0, 0)
        super().updateGeometries()
        self.adjust_in_filter_positions()

    def adjust_in_filter_positions(self) -> None:
        """keeps positions of filtering line edits right if columns get resized

        Returns:
            None"""

        for index, editor in enumerate(self._editors):
            height = editor.sizeHint().height()
            editor.move(self.sectionPosition(index) - self.offset() + 16, height+3)
            editor.resize(self.sectionSize(index), height)

    def filter_text(self, index: int) -> str:
        """returns currentText of filter line edit at a given index

        Returns:
            
            """
        if 0 <= index < len(self._editors):
            return self._editors[index].text()
        return ''

    def hide_show(self):
        for editor in self._editors:
            if editor.isVisible():
                editor.hide()
            else:
                editor.show()


class ComboDelegate(QItemDelegate):
    """handels os change in form of a combobox directly in tableView"""
    
    def createEditor(self, parent, option, proxyModelIndex):
        neighbour_data = startscreen.main.filters[-1][1].data(startscreen.main.filters[-1][1].index(proxyModelIndex.row(), proxyModelIndex.column()+1))
        self.combo_OS = [x for x in valid_devices if x.__name__ == neighbour_data].pop().expected_OS
        combo = QComboBox(parent)
        combo.addItems(self.combo_OS)
        self.connect(combo, SIGNAL("currentIndexChanged(int)"), self, SLOT("currentIndexChanged()"))
        return combo

    def setModelData(self, combo, model, index):
        comboIndex = combo.currentIndex()
        text = self.combo_OS[comboIndex]
        model.setData(index, text)

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled


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
        self.last_open_file_path = None

        # setup statusbar
        self.statusbar = self.statusBar()
        # setup stackedwidget
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.setup_menubar()
        self.setup_p_view()
        self.setup_p_register()
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

        self.model = QStandardItemModel(self.p_view)
        self.model.setHorizontalHeaderLabels(labels)

        delegate = ComboDelegate()

        self.table = QtWidgets.QTableView(self.p_view)
        self.table.setModel(self.model)
        self.table.setItemDelegateForColumn(2, delegate)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSortingEnabled(True)

        self.bt_register_new = QtWidgets.QPushButton("register new", self.p_view)
        self.bt_hide_show_filter = QtWidgets.QPushButton("hide/show filter inputs", self.p_view)

        p_view_layout = QtWidgets.QVBoxLayout(self.p_view)

        p_view_layout.addWidget(self.table)
        p_view_layout.addWidget(self.bt_register_new)
        p_view_layout.addWidget(self.bt_hide_show_filter)
        self.p_view.setLayout(p_view_layout)

        self.header = FilterHeader(self.table)
        self.header.set_filter_boxes(self.model.columnCount())

        self.filters = []
        # if len(self.filters) == 0:
        #     filter = QSortFilterProxyModel()
        #     filter.setSourceModel(self.model)
        #     filter.setFilterRegExp("")
        #     self.filters.append((0, filter))

        self.table.setHorizontalHeader(self.header)


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

        # header
        self.header.filterActivated.connect(self.handleFilterActivated)

        # line edit

        self.in_new_filename.returnPressed.connect(
            lambda: self.validate(self.new, [self.in_new_filepath, self.in_new_filename], data=False))

        # comboboxes
        self.in_combobox_devicetype.addItems(["choose here"] + [x.__name__ for x in valid_devices])
        self.in_combobox_devicetype.currentIndexChanged.connect(lambda: self.update_combobox(self.in_combobox_os,
                                                                                               valid_devices[
                                                                                                   self.in_combobox_devicetype.currentIndex() - 1].expected_OS))
        # btns
        self.bt_hide_show_filter.clicked.connect(lambda: self.header.hide_show())
        self.bt_register_new.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.p_register))
        self.bt_register.clicked.connect(
            lambda: self.validate(self.register, line_edit_list=[self.in_username, self.in_devicename],
                                  combo_box_list=[self.in_combobox_devicetype, self.in_combobox_os],
                                  forbidden=list(registered_devices.keys()), checkfname=True))
        self.bt_create.clicked.connect(
            lambda: self.validate(self.new, [self.in_new_filepath, self.in_new_filename], data=False))
        self.bt_mod_new_path.clicked.connect(lambda: self.new(True))
        # menu bar
        self.action_search.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.pSearch))
        self.action_register.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.p_register))
        self.action_change.triggered.connect(lambda: self.change(0))
        self.action_open.triggered.connect(self.get_open_file_path)
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
    def validate(self, command, file_path: str = None, line_edit_list: list = None, combo_box_list: list = None, data=None, allowed: list = None, forbidden: list = None, checkfname: bool = None, checkregistered: bool = None) -> None:
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
        if file_path is not None:
            with open(file_path) as file:
                loaded = dict(json.load(file))
                for key in loaded.keys():
                    if key not in allowed:
                        self.statusbar.showMessage("invalid json file")
                        fails += 1
        if fails == 0:
            if data is None:
                command()
            else:
                command(data)
        else:
            print(f"problem\ncommand: {command.__name__}\nfails: {fails}")

    @Slot(int)
    def handleFilterActivated(self, in_filter_index: int) -> None:
        text = self.table.horizontalHeader().filter_text(in_filter_index)
        check = [x for x in self.filters if x[0] == in_filter_index]

        if len(check) == 0:
            filter = QSortFilterProxyModel()
            if len(self.filters) == 0:
                filter.setSourceModel(self.model)
            else:
                filter.setSourceModel(self.filters[-1][1])
            filter.setFilterKeyColumn(in_filter_index)
            filter.setFilterCaseSensitivity(Qt.CaseInsensitive)
            self.table.setModel(filter)
            filter.setFilterRegExp(str(text))
            self.filters.append((in_filter_index, filter))

        elif len(check) == 1:
            self.filters[-1][1].setFilterRegExp(str(text))
        else:
            print(check)

    def register(self) -> None:
        """registers a new device and saves it in csv"""
        logic.register(self.in_devicename.text(), valid_devices[self.in_combobox_os.currentIndex()],
                       self.in_username.text(), self.in_combobox_os.currentText(), self.text_edit_comment.toPlainText(),
                       str(datetime.datetime.now()), registered_devices)

        new_values = [self.in_devicename.text(), self.in_username.text(), str(valid_devices[self.in_combobox_os.currentIndex()].__name__),
         self.in_combobox_os.currentText(), self.text_edit_comment.toPlainText(),
         str(datetime.datetime.now())]
        row = [QStandardItem(str(item)) for item in new_values]
        self.model.appendRow(row)

        self.stacked_widget.setCurrentWidget(self.p_view)
        self.in_devicename.clear()
        self.in_username.clear()
        self.in_combobox_os.clear()
        self.text_edit_comment.clear()
        self.save()

    def get_open_file_path(self):

        self.file_path = \
        QFileDialog.getOpenFileName(self, "open file", f"{self.last_open_file_path or 'c://'}", "json files (*json)")[0]
        self.validate(command=self.load, file_path=self.file_path, allowed=["devices", "last_open_file_path"])

    def load(self) -> None:
        """opens json file and loads its content into registered devices"""

        self.model.clear()
        registered_devices.clear()
        with open(self.file_path, "r") as file:
            data = dict(json.load(file))
            devices = data["devices"].values()
            self.last_open_file_path = data["last_open_file_path"]
            for value in devices:
                row = []
                for i, item in enumerate(value):
                    cell = QStandardItem(str(item))
                    row.append(cell)
                    if i == 0 or i == 3 or i == 5:
                        cell.setEditable(False)
                self.model.appendRow(row)

                new = [x for x in valid_devices if x.__name__ == value[3]].pop(0)(value[0], value[1], value[4], value[5])
                new.OS = value[2]
                registered_devices[value[0]] = new

        self.model.setHorizontalHeaderLabels(labels)
        self.statusbar.showMessage("")

    def save(self) -> None:
        """saves content fo registered_devices into specified json file"""
        if not self.file_path:
            self.statusbar.showMessage("no file path set all changes get lost if closed")
        else:
            with open(self.file_path, 'w',) as file:
                devices = {k: [v.name, v.user, v.OS, v.__class__.__name__, v.comment, v.datetime] for (k, v) in enumerate(registered_devices.values())}
                last_open_file_path = "/".join(self.file_path.split("/")[:-1])
                resulting_dict = {"devices": devices, "last_open_file_path": last_open_file_path}
                json.dump(resulting_dict, file)
                self.statusbar.showMessage("saved file")

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

    def print(self, test:bool) -> None:
        """setup and preview pViewTable for paper printing"""
        with open(self.file_path) as f:
            data = json.dumps(dict(json.load(f)), sort_keys=True, indent=6, separators= (".", "="))
        self.document = QtWidgets.QTextEdit()
        self.document.setText(data)

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