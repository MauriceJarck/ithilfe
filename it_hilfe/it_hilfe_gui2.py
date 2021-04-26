import datetime
import json
import sys
from marshmallow import ValidationError

from PySide2.QtCore import QSortFilterProxyModel, QPropertyAnimation, QSize, QEasingCurve
from PySide2.QtGui import QPixmap, QIcon, QFont, QKeySequence, Qt, QStandardItemModel, QStandardItem
from PySide2.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PySide2.QtWidgets import \
    QMainWindow, QWidget, QApplication, QFileDialog, QItemDelegate, QComboBox, QLineEdit, \
    QHeaderView, QFrame, QPushButton, QSizePolicy, QLabel, QHBoxLayout, QMessageBox, QCompleter, QAction, \
    QStackedWidget, QListWidget, QGridLayout, QTextEdit, QSlider
from PySide2 import QtWidgets, QtCore

import it_hilfe.devices as devices
import it_hilfe.it_hilfe_logic as logic
from it_hilfe import validate_json

valid_devices = [devices.WindowsLapTop, devices.WindowsWorkStation, devices.Macbook]
labels = ['devname', 'username', 'os', 'devtype', "comment", "datetime", "extras"]
file_path = None


class FilterHeader(QHeaderView):
    """handels line edits for filtering in tableview self.header

    Returns:
            None"""

    def __init__(self, parent):
        """inits FilterHeader class"""
        super().__init__(QtCore.Qt.Horizontal, parent)
        self.editors = []
        self.setStretchLastSection(True)
        self.setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.sectionSize(0)
        self.setSortIndicatorShown(False)
        self.sectionResized.connect(self.adjust_in_filter_positions)

    def set_filter_boxes(self) -> None:
        """sets up line edit boxes for live filtering tableView

        Returns:
            None"""
        editor0 = QLineEdit(self.parent())
        editor0.setPlaceholderText('Filter')

        editor1 = QLineEdit(self.parent())
        editor1.setPlaceholderText('Filter')

        editor2 = QLineEdit(self.parent())
        editor2.setPlaceholderText('Filter')

        editor3 = QLineEdit(self.parent())
        editor3.setPlaceholderText('Filter')

        editor4 = QLineEdit(self.parent())
        editor4.setPlaceholderText('Filter')

        editor5 = QLineEdit(self.parent())
        editor5.setPlaceholderText('Filter')

        editor6 = QLineEdit(self.parent())
        editor6.setPlaceholderText('Filter')

        self.editors.append(editor0)
        self.editors.append(editor1)
        self.editors.append(editor2)
        self.editors.append(editor3)
        self.editors.append(editor4)
        self.editors.append(editor5)
        self.editors.append(editor6)

    def sizeHint(self) -> int:
        """returns height of headerView

        Returns:
            size: describes the height of headerView"""
        size = super().sizeHint()
        if self.editors:
            height = self.editors[0].sizeHint().height()
            size.setHeight(size.height() + height)
        return size

    def updateGeometries(self) -> None:
        """sets viewport of geometries

        Returns:
            None"""

        if self.editors:
            height = self.editors[0].sizeHint().height()
            self.setViewportMargins(0, 0, 0, height)
        else:
            self.setViewportMargins(0, 0, 0, 0)
        super().updateGeometries()
        self.adjust_in_filter_positions()

    def adjust_in_filter_positions(self) -> None:
        """keeps positions of filtering line edits right if columns get resized

        Returns:
            None"""

        for index, editor in enumerate(self.editors):
            height = editor.sizeHint().height()
            try:
                if main_window.model.rowCount() == 0 or main_window.filters[-1].rowCount() == 0:
                    editor.move(self.sectionPosition(index) - self.offset() + 4, height + 3)
                else:
                    editor.move(self.sectionPosition(index) - self.offset() + 26, height + 3)
            except NameError:
                pass

            editor.resize(self.sectionSize(index), height)

    def hide_show(self):
        """hides and shows filter line_edits in table Header

        Returns:
            None"""
        for editor in self.editors:
            if editor.isVisible():
                editor.hide()
            else:
                editor.show()


class ComboDelegate(QItemDelegate):
    """handels os change in form of a combobox directly in tableView"""

    def createEditor(self, parent, option, proxyModelIndex):
        print(parent, option, proxyModelIndex)
        neighbour_data = main_window.filters[-1].data(
            main_window.filters[-1].index(proxyModelIndex.row(), proxyModelIndex.column() + 1))
        self.combo_OS = [x for x in valid_devices if x.__name__ == neighbour_data].pop().expected_OS
        combo = QComboBox(parent)
        combo.addItems(self.combo_OS)
        return combo

    def setModelData(self, combo, model, index):
        combo_index = combo.currentIndex()
        text = self.combo_OS[combo_index]
        model.setData(index, text)

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled


class MainWindowUi(QMainWindow):
    """sets up ui properties of MainWindowUi class"""

    def __init__(self) -> None:
        """inits MainWindow class

        configuring parameters of MainWindow class and inherits from QtWidget.QMainWindow
        loads .ui file sets up file and directory path vars, inits click events(menuebar, coboboxes, btns) and
        shows gui the first time

        Returns:
            None"""
        super(MainWindowUi, self).__init__()
        self.setWindowTitle("It_Hilfe")
        self.resize(820, 450)
        self.setWindowIcon(QIcon("./data/favicon2.png"))
        self.setMinimumSize(700, 250)

        self.file_path = None
        self.dir = None
        self.last_open_file_path = None
        self.last_open_file_dir = None
        self.initial_theme = None
        self.registered_devices = {}
        self.user_config_file = "./data/user_config.json"

        # setup stackedwidget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.setup_menubar()
        self.setup_p_view()
        self.setup_p_register()
        self.setup_p_create()
        self.setup_p_preferences()
        self.setup_signals()

        self.font = QFont()
        self.font.setPointSize(9)

        self.validate(self.set_user_preferences, file_path=self.user_config_file, schema=validate_json.ItHilfeUserPreferencesSchema, forbidden=[""])

        # setup statusbar
        self.statusbar = self.statusBar()

        self.stacked_widget.setCurrentWidget(self.p_view)

    def setup_menubar(self) -> None:
        """inits menubar

        Returns:
            None"""
        self.menu_Bar = self.menuBar()

        menu_file = self.menu_Bar.addMenu("file")
        self.action_open = QAction("open")
        self.action_save = QAction("save")
        self.action_new = QAction("new")
        self.action_print = QAction("print")
        self.action_preferences = QAction("preferences")
        self.action_hide_menu_bar = QAction("hide menubar")
        self.action_print.setShortcut(QKeySequence("Ctrl+p"))
        self.action_open.setShortcut(QKeySequence("Ctrl+o"))
        self.action_save.setShortcut(QKeySequence("Ctrl+s"))
        self.action_hide_menu_bar.setShortcut(QKeySequence("Ctrl+h"))
        self.action_hide_menu_bar.setIcon(QIcon("./data/show_hide.ico"))
        self.action_print.setIcon(QIcon("./data/print2.ico"))
        self.action_open.setIcon(QIcon("./data/open.ico"))
        self.action_save.setIcon(QIcon("./data/save.ico"))
        self.action_new.setIcon(QIcon("./data/newfile.ico"))
        self.action_preferences.setIcon(QIcon("./data/preferences.ico"))

        menu_file.addAction(self.action_open)
        menu_file.addAction(self.action_save)
        menu_file.addAction(self.action_new)
        menu_file.addAction(self.action_print)
        menu_file.addAction(self.action_preferences)

        menu_edit = self.menu_Bar.addMenu("edit")
        self.action_register = QAction("register")
        self.action_register.setShortcut(QKeySequence("Ctrl+n"))
        self.action_register.setIcon(QIcon("./data/register.ico"))

        menu_edit.addAction(self.action_register)

        menu_view = self.menu_Bar.addMenu("view")
        menu_view.addAction(self.action_hide_menu_bar)

    def setup_p_view(self) -> None:
        """inits stacked widget page widget

        Returns:
            None"""
        self.p_view = QtWidgets.QWidget()
        self.stacked_widget.addWidget(self.p_view)

        self.model = QStandardItemModel(self.p_view)
        self.model.setHorizontalHeaderLabels(labels)

        self.filters = []
        source_model = self.model
        for filter_num in range(7):
            filter = QSortFilterProxyModel()
            filter.setSourceModel(source_model)
            filter.setFilterKeyColumn(filter_num)
            source_model = filter
            self.filters.append(filter)

        delegate = ComboDelegate()
        self.table = QtWidgets.QTableView(self.p_view)
        self.table.setModel(self.filters[-1])
        self.table.setItemDelegateForColumn(2, delegate)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.header = FilterHeader(self.table)
        self.header.set_filter_boxes()
        self.header.setMaximumHeight(50)
        self.table.setHorizontalHeader(self.header)

        self.bt_burger = QPushButton(self.p_view)
        self.bt_burger.setIcon(QIcon("./data/menu2.svg"))
        self.bt_burger.setIconSize(QSize(30, 30))
        self.bt_burger.setToolTip('slide out description')
        l_burger = QLabel("menu", self.p_view)

        self.bt_register_new = QPushButton(self.p_view)
        self.bt_register_new.setIcon(QIcon("./data/add.ico"))
        self.bt_register_new.setIconSize(QSize(30, 30))
        self.bt_register_new.setToolTip("register new")
        l_register_new = QLabel("register new", self.p_view)

        self.bt_delete_column = QPushButton(self.p_view)
        self.bt_delete_column.setIcon(QIcon("./data/remove.ico"))
        self.bt_delete_column.setIconSize(QSize(30, 30))
        self.bt_delete_column.setToolTip("delete columns with min 1 cell selected")
        l_delete = QLabel("delete column", self.p_view)

        self.bt_hide_show_filter = QPushButton(self.p_view)
        self.bt_hide_show_filter.setIcon(QIcon("./data/show_hide.ico"))
        self.bt_hide_show_filter.setIconSize(QSize(30, 30))
        self.bt_hide_show_filter.setToolTip("hide/show filter input")
        l_hide_show = QLabel("hide/show", self.p_view)

        self.left_btn_frame = QFrame(self.p_view)
        self.left_btn_frame.setMaximumWidth(40)
        self.left_btn_frame.setContentsMargins(0, 0, 0, 0)

        self.left_menu_frame = QFrame(self.p_view)
        self.left_menu_frame.setMaximumWidth(0)
        self.left_menu_frame.setContentsMargins(0, 0, 0, 0)

        p_view_layout2 = QtWidgets.QVBoxLayout(self.left_btn_frame)
        p_view_layout2.addWidget(self.bt_burger)
        p_view_layout2.addWidget(self.bt_register_new)
        p_view_layout2.addWidget(self.bt_delete_column)
        p_view_layout2.addWidget(self.bt_hide_show_filter)
        p_view_layout2.setAlignment(Qt.AlignTop)
        p_view_layout2.setContentsMargins(0, 0, 0, 0)

        self.p_view_layout3 = QtWidgets.QVBoxLayout(self.left_menu_frame)
        self.p_view_layout3.addWidget(l_burger)
        self.p_view_layout3.addWidget(l_register_new)
        self.p_view_layout3.addWidget(l_delete)
        self.p_view_layout3.addWidget(l_hide_show)
        self.p_view_layout3.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.p_view_layout3.setContentsMargins(0, 0, 0, 0)
        self.p_view_layout3.setSpacing(25)

        p_view_layout = QHBoxLayout(self.p_view)
        p_view_layout.setContentsMargins(0, 0, 0, 0)
        p_view_layout.addWidget(self.left_btn_frame)
        p_view_layout.addWidget(self.left_menu_frame)
        p_view_layout.addWidget(self.table)
        self.p_view.setLayout(p_view_layout)

        self.p_view.addAction(self.action_open)
        self.p_view.addAction(self.action_save)
        self.p_view.addAction(self.action_new)
        self.p_view.addAction(self.action_print)
        self.p_view.addAction(self.action_register)
        self.p_view.addAction(self.action_hide_menu_bar)

    def setup_p_register(self) -> None:
        """inits stacked widget page widgets

        Returns:
            None"""

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
        self.in_comment = QtWidgets.QTextEdit(self.p_register)
        self.bt_enter_register = QPushButton("register", self.p_register)
        self.bt_cancel_register = QPushButton("cancel", self.p_register)

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
        p_register_layout.addWidget(self.in_comment)
        p_register_layout.addWidget(self.bt_enter_register)
        p_register_layout.addWidget(self.bt_cancel_register)

    def setup_p_create(self) -> None:
        """inits stacked widget page widget

        Returns:
            None"""

        self.p_create = QtWidgets.QWidget()
        self.stacked_widget.addWidget(self.p_create)

        l_new_filepath = QtWidgets.QLabel("new filepath", self.p_create)
        self.bt_mod_new_path = QPushButton("mod filepath", self.p_create)
        self.in_new_filepath = QtWidgets.QLineEdit(self.p_create)
        l_new_filename = QtWidgets.QLabel("new filename", self.p_create)
        self.in_new_filename = QtWidgets.QLineEdit(self.p_create)
        self.bt_create = QPushButton("create", self.p_create)
        self.bt_cancel_create = QPushButton("cancel", self.p_create)

        p_create_layout = QtWidgets.QVBoxLayout(self.p_create)
        p_create_layout.addWidget(l_new_filepath)
        p_create_layout.addWidget(self.in_new_filepath)
        p_create_layout.addWidget(l_new_filename)
        p_create_layout.addWidget(self.in_new_filename)
        p_create_layout.addStretch(100)
        p_create_layout.addWidget(self.bt_mod_new_path)
        p_create_layout.addWidget(self.bt_create)
        p_create_layout.addWidget(self.bt_cancel_create)

    def setup_p_preferences(self) -> None:
        """inits setup_p_preferences stacked widget page widget

            Returns:
                None"""

        self.p_preferences = QWidget()
        self.p_preferences.resize(500, 250)
        self.p_preferences.setWindowTitle("preferences")
        self.list_Widget = QListWidget(self.p_preferences)
        self.list_Widget.addItems(["appearance", "about"])
        self.list_Widget.setMaximumWidth(100)

        self.stacked_widget_preferences = QStackedWidget(self.p_preferences)

        # setup appearance
        self.apperence_widget = QWidget()
        self.stacked_widget_preferences.addWidget(self.apperence_widget)
        self.in_combo_themes = QComboBox(self.apperence_widget)
        self.in_combo_themes.addItems(["dark_theme", "light_theme"])

        self.in_combo_theme_initial = QComboBox(self.apperence_widget)
        self.in_combo_theme_initial.addItems(["dark_theme", "light_theme"])

        self.text_size_slider = QSlider(QtCore.Qt.Orientation.Horizontal, self.apperence_widget)
        self.text_size_slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.text_size_slider.setMaximum(15)
        self.text_size_slider.setMinimum(8)

        stacked_widget_preferences_layout = QGridLayout(self.apperence_widget)
        stacked_widget_preferences_layout.setAlignment(QtCore.Qt.AlignTop)
        stacked_widget_preferences_layout.addWidget(QLabel("theme"), 0, 0)
        stacked_widget_preferences_layout.addWidget(self.in_combo_themes, 0, 1)
        stacked_widget_preferences_layout.addWidget(QLabel("initial theme"), 1, 0)
        stacked_widget_preferences_layout.addWidget(self.in_combo_theme_initial, 1, 1)
        stacked_widget_preferences_layout.addWidget(QLabel("Fontsize"), 2, 0)
        stacked_widget_preferences_layout.addWidget(self.text_size_slider, 2, 1)

        self.about_widget = QWidget()
        self.stacked_widget_preferences.addWidget(self.about_widget)

        about_text_edit = QTextEdit(self.about_widget)
        about_text_edit.setText("developed by Maurice Jarck\nwith kind support from Shuai Lou\n07.2020-04.2021")
        about_text_edit.setEnabled(False)
        stacked_widget_about_layout = QGridLayout(self.about_widget)
        stacked_widget_about_layout.addWidget(about_text_edit)

        p_apperance_layout = QHBoxLayout(self.p_preferences)
        p_apperance_layout.addWidget(self.list_Widget)
        p_apperance_layout.addWidget(self.stacked_widget_preferences)

    def setup_signals(self) -> None:
        """connects signals

        Returns:
            None"""

        # header
        for filter, editor in zip(self.filters, self.header.editors):
            editor.textChanged.connect(filter.setFilterRegExp)

        # line edit
        self.in_new_filename.returnPressed.connect(
            lambda: self.validate(self.new, line_edit_list=[self.in_new_filepath, self.in_new_filename], data=False))

        # comboboxes
        self.in_combobox_devicetype.addItems(["choose here"] + [x.__name__ for x in valid_devices])
        self.in_combobox_devicetype.currentIndexChanged.connect(lambda: self.update_combobox(self.in_combobox_os,
                                                                                             valid_devices[
                                                                                                 self.in_combobox_devicetype.currentIndex() - 1].expected_OS))
        self.in_combo_themes.currentIndexChanged.connect(lambda: self.change_theme(self.in_combo_themes.currentText()))
        self.in_combo_theme_initial.currentTextChanged.connect(lambda: setattr(self, "initial_theme", self.in_combo_theme_initial.currentText()))
        # btns
        self.bt_delete_column.clicked.connect(self.delete)
        # self.bt_hide_show_filter.clicked.connect(lambda: self.toggle_hide_show_ani(37, 47, "height", self.header, b"maximumHeight"))
        self.bt_hide_show_filter.clicked.connect(self.header.hide_show)
        # self.bt_hide_show_filter.clicked.connect(lambda: self.toggle_hide_show_ani(30, 44, "height", self.header, b"maximumHeight"))
        self.bt_register_new.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.p_register))
        self.bt_enter_register.clicked.connect(
            lambda: self.validate(self.register, line_edit_list=[self.in_username, self.in_devicename],
                                  combo_box_list=[self.in_combobox_devicetype, self.in_combobox_os],
                                  forbidden=list(self.registered_devices.keys()), checkfname=True))
        self.bt_create.clicked.connect(
            lambda: self.validate(self.new, line_edit_list=[self.in_new_filepath, self.in_new_filename], data=False))
        self.bt_mod_new_path.clicked.connect(lambda: self.new(True))
        self.bt_burger.clicked.connect(lambda: self.toggle_hide_show_ani(0, 66, "width", self.left_menu_frame, b"maximumWidth", ))
        # menu bar
        self.action_register.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.p_register))
        self.action_open.triggered.connect(self.get_open_file_path)
        self.action_save.triggered.connect(self.save)
        self.action_new.triggered.connect(lambda: self.new(True))
        self.action_print.triggered.connect(lambda: self.validate(self.print, data=False, checkfname=True))
        self.action_hide_menu_bar.triggered.connect(lambda: self.toggle_hide_show(self.menu_Bar))
        self.action_preferences.triggered.connect(self.p_preferences.show)
        # cancel
        self.bt_cancel_register.clicked.connect(lambda: self.cancel(
            [self.in_username, self.in_devicename, self.in_combobox_os, self.in_comment]))

        # list widget
        self.list_Widget.currentRowChanged.connect(lambda: self.stacked_widget_preferences.setCurrentIndex(self.list_Widget.currentIndex().row()))

        # slider
        self.text_size_slider.sliderMoved.connect(lambda: self.change_font_size(self.text_size_slider.value()))
        # self.text_size_slider.sliderMoved.connect(lambda: print(self.text_size_slider.value()))

    def change_theme(self, theme) -> None:
        """changes theme according to combobox selection

        Returns:
            None"""

        with open(f"./data/{theme}.css", "r") as file:
            stylesheed = " ".join(file.readlines())
            self.setStyleSheet(stylesheed)
            self.p_preferences.setStyleSheet(stylesheed)

        if self.in_combo_themes.currentText() == "dark_theme":

            self.left_btn_frame.setStyleSheet(u"background: #455364; border: 0px solid;")
            self.p_view_layout3.setSpacing(30)

        else:
            self.left_btn_frame.setStyleSheet(u"background: #ADADAD; border: 0px solid;")
            self.p_view_layout3.setSpacing(25)

        return self.in_combo_themes.currentText()

    def toggle_hide_show_ani(self, collapsed_val: int, expanded_val: int, actual: str, to_animate, property: bytes):
        """interpolates over a defined range of vales and sets it to a given property of a given widget"""
        if getattr(to_animate, actual)() == expanded_val:
            destination = collapsed_val
        else:
            destination = expanded_val
        print(getattr(to_animate, actual)(), destination)
        self.ani = QPropertyAnimation(to_animate, property)
        self.ani.setDuration(300)
        self.ani.setStartValue(getattr(to_animate, actual)())
        self.ani.setEndValue(destination)
        self.ani.setEasingCurve(QEasingCurve.Linear)
        self.ani.start()

    def toggle_hide_show(self, widget: QWidget) -> None:
        """toggles visibiliy of a given widget
        Arg:
            widget: widget which is aimed to be hidden or shown
        Returs:
            None"""

        if widget.isVisible():
            widget.hide()
        else:
            widget.show()

    def reopen_last_file(self)-> None:
        """asks for reopening of the last opened file"""
        if self.last_open_file_path != "" or self.last_open_file_path is not None:
            reopen_dialog = QMessageBox.question(self.p_view, "reopen last file?", "Do you want to reopen the last edited file?", QMessageBox.Yes | QMessageBox.No)
            if reopen_dialog == QMessageBox.Yes:
                self.file_path = self.last_open_file_path
                self.load()

    def change_font_size(self, size: int) -> None:
        """changes all font sizes"""
        self.font.setPointSize(size)
        self.menu_Bar.setFont(self.font)
        self.header.setFont(self.font)
        self.table.setFont(self.font)
        self.p_preferences.setFont(self.font)

    def set_user_preferences(self) -> None:
        """Reads user_config file and sets its propertys"""
        with open(self.user_config_file, "r") as config_file:
            data = dict(json.load(config_file))

            self.last_open_file_path = data["last_open_file_path"]
            self.initial_theme = data['initial_theme']
            self.change_font_size(data['font_size'])
            self.text_size_slider.setValue(data['font_size'])
            self.in_combo_theme_initial.setCurrentText(self.initial_theme)
            self.in_combo_themes.setCurrentText(self.initial_theme)

            with open(f"./data/{self.initial_theme}.css") as file:
                style_sheed = " ".join(file.readlines())
                self.setStyleSheet(style_sheed)
                self.p_preferences.setStyleSheet(style_sheed)

            self.bt_burger.setStyleSheet("border: 0px solid; background: transparent;")
            self.bt_register_new.setStyleSheet("border: 0px solid; background: transparent;")
            self.bt_delete_column.setStyleSheet("border: 0px solid; background: transparent;")
            self.bt_hide_show_filter.setStyleSheet("border: 0px solid; background: transparent;")
            self.left_menu_frame.setStyleSheet(u" border: 0px solid;")

            if self.initial_theme == "dark_theme":
                self.left_btn_frame.setStyleSheet(u"background: #455364; border: 0px solid;")

            else:
                self.left_btn_frame.setStyleSheet(u"background: #ADADAD; border: 0px solid;")

    def cancel(self, widgets: list) -> None:
        """click event for all cancel buttons

        shows fist page in stacked widget and clears all widgets in widgets

        Args:
               widgets: defines list containing widgets to clear, only widgets with method .clear() are possible

        Returns:
            None"""
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

    def validate(self, command, file_path: str = None, schema= None, line_edit_list: list = None, combo_box_list: list = None,
                 data=None, forbidden: list = None, checkfname: bool = None) -> None:
        """validates user input

        Args:
            command: function to be called after vailidation process if finished
            line_edit_list: contents pyqt5.QtWidgets.QlineEdit instances to be checked if empty or current text in forbidden or not in allowed
            combo_box_list: contents pyqt5.QtWidgets.qComboBox instances to be checked if nothing selected
            data: data to be passed into command function if needed
            forbidden: houses keys which are not allowed to be entered
            checkfname: check weather an file path exists or not

        Returns:
            None"""

        fails = 0
        if line_edit_list is not None:
            for x in line_edit_list:
                if x.text() == "":
                    x.setText("fill all fields")
                    fails += 1
                if forbidden is not None and x.text() in forbidden:
                    x.setText("in forbidden!!")
                    fails += 1
        if combo_box_list is not None:
            for combobox in combo_box_list:
                if combobox.currentText() == "":
                    self.statusbar.showMessage("all comboboxes must be filled")
                    fails += 1
        if checkfname is True and self.file_path is None:
            self.statusbar.showMessage("no file path specified, visit Ctrl+o or menuebar/edit/open to fix")
            fails += 1

        if file_path is not None:
            if forbidden is not None and file_path in forbidden:
                fails += 1
                self.statusbar.showMessage("select a file to continue")
            else:
                try:
                    validate_json.validate(file_path, schema)
                except ValidationError as e:
                    self.msg_box = QtWidgets.QMessageBox.critical(self, "validation failed",
                                                                  f"Invalid Json file, problem in: {e.messages}")
                    fails += 1
        if fails == 0:
            if data is None:
                command()
            else:
                command(data)
        else:
            message = f"problem\ncommand: {command.__name__}\nfails: {fails}"
            print(message)
            return message

    def register(self) -> None:
        """registers a new device and saves

        Returns:
            None"""
        logic.register(devname=self.in_devicename.text(),
                       devtype=[device for device in valid_devices if
                                device.__name__ == self.in_combobox_devicetype.currentText()].pop(),
                       username=self.in_username.text(),
                       os=self.in_combobox_os.currentText(),
                       comment=self.in_comment.toPlainText(),
                       datetime=str(datetime.datetime.now()),
                       registered_devices=self.registered_devices)

        new_values = [self.in_devicename.text(), self.in_username.text(),
                      self.in_combobox_os.currentText(),
                      [device.__name__ for device in valid_devices if
                       device.__name__ == self.in_combobox_devicetype.currentText()].pop(),
                      self.in_comment.toPlainText(),
                      str(datetime.datetime.now())]
        row = [QStandardItem(str(item)) for item in new_values]
        self.model.appendRow(row)

        self.stacked_widget.setCurrentWidget(self.p_view)
        self.in_devicename.clear()
        self.in_username.clear()
        self.in_combobox_os.clear()
        self.in_comment.clear()
        self.save()

    def delete(self) -> None:
        """deletes all rows associated with min 1 slected cell
        Returns:
            None"""
        rows = sorted(set(index.row() for index in self.table.selectedIndexes()), reverse=True)
        qb = QMessageBox()
        answ = qb.question(self, 'delete rows', f"Are you sure to delete {rows} rows?", qb.Yes | qb.No)

        if answ == qb.Yes:
            for row in rows:
                self.registered_devices.pop(str(self.model.index(row, 0).data()))
                self.model.removeRow(row)
            qb.information(self, 'notification', f"deleted {rows} row")
        else:
            qb.information(self, 'notification', "Nothing Changed")
        self.save()

    def get_open_file_path(self) -> None:
        """gets file-path and set it to self.file_path, extra step for json validation

        Returns:
            None"""

        self.file_path = \
            QFileDialog.getOpenFileName(self, "open file", f"{self.last_open_file_dir or 'c://'}",
                                        "json files (*json)")[0]
        self.validate(command=self.load, file_path=self.file_path, schema=validate_json.ItHilfeDataSchema, forbidden=[""])

    def load(self) -> None:
        """opens json file and loads its content into registered devices

        Returns:
            None"""

        self.model.clear()
        self.registered_devices.clear()
        with open(self.file_path, "r") as file:
            data = dict(json.load(file))
            devices = data["devices"].values()
            self.last_open_file_dir = data["last_open_file_dir"]
            for value in devices:
                row = []
                for i, item in enumerate(value):
                    cell = QStandardItem(str(item))
                    row.append(cell)
                    if i == 0 or i == 3 or i == 5:
                        cell.setEditable(False)
                self.model.appendRow(row)

                new = [x for x in valid_devices if x.__name__ == value[3]].pop(0)(value[0], value[1], value[4],
                                                                                  value[5])
                new.OS = value[2]
                self.registered_devices[value[0]] = new

        self.model.setHorizontalHeaderLabels(labels)
        self.statusbar.showMessage("")

        # auto complete
        for a in range(len(self.header.editors)):
            completer = QCompleter(
                [self.model.data(self.model.index(x, a)) for x in range(self.model.rowCount())])
            completer.setCompletionMode(QCompleter.InlineCompletion)
            self.header.editors[a].setCompleter(completer)

    def save(self) -> None:
        """saves content fo self.registered_devices into specified json file

        Returns:
            None"""
        if not self.file_path:
            self.statusbar.showMessage("no file path set all changes get lost if closed")
        else:
            with open(self.file_path, 'w', ) as file:
                devices = {k: [v.name, v.user, v.OS, v.__class__.__name__, v.comment, v.datetime] for (k, v) in
                           enumerate(self.registered_devices.values())}
                last_open_file_dir = "/".join(self.file_path.split("/")[:-1])
                resulting_dict = {"devices": devices, "last_open_file_dir": last_open_file_dir}
                json.dump(resulting_dict, file)
                self.statusbar.showMessage("saved file")

        with open(self.user_config_file, "w") as user_preferences_file:
            json.dump({"last_open_file_path": self.last_open_file_path, "initial_theme": self.initial_theme, "font_size": self.text_size_slider.value()}, user_preferences_file)

    def new(self, stage: bool, test: bool = False) -> None:
        """creates new csv file to save into

        stage is True: set filepath
        stage is False: set new name, save
        Args:
            stage: determines a which stage to execute this function

        Returns:
            None"""

        if stage is True:
            if not test:
                self.dir = QFileDialog.getExistingDirectory(self, "select a folder", "c://")
            self.stacked_widget.setCurrentWidget(self.p_create)
            self.in_new_filepath.setText(self.dir)
            self.registered_devices.clear()

        else:
            self.file_path = self.dir + f"/{self.in_new_filename.text()}.json"
            self.save()
            self.stacked_widget.setCurrentWidget(self.p_view)

    def print(self, test: bool) -> None:
        """setup and preview pViewTable for paper printing

        Returns:
            None"""

        with open(self.file_path) as f:
            self.data = json.dumps(dict(json.load(f)), sort_keys=True, indent=6, separators=(".", "="))
        self.document = QtWidgets.QTextEdit()
        self.document.setText(self.data)

        if not test:
            printer = QPrinter()
            previewDialog = QPrintPreviewDialog(printer, self)
            previewDialog.paintRequested.connect(lambda: self.document.print_(printer))
            previewDialog.exec_()


class StartScreenUi(QWidget):
    """sets up ui properties of startscreen"""

    def __init__(self) -> None:
        """inits StartScreenUi class

        Returns:
            None"""

        super(StartScreenUi, self).__init__()
        self.setWindowTitle("It_Hilfe")
        self.conf_file = "./data/user_config.json"
        self.setup_startscreen()
        self.show()

        self.timer = QtCore.QTimer()
        self.timer.singleShot(1500, self.on_elapsed)

    def on_elapsed(self) -> None:
        """closes startsceen window and shows previously created instance of MainWindow

        Returns:
            None"""
        main_window.show()
        main_window.reopen_last_file()
        self.close()

    def setup_startscreen(self):
        """sets up startscreen ui

        Returns:
            None"""
        self.pic_label = QtWidgets.QLabel(self)
        self.pic_label.setPixmap(QPixmap("./data/startscreenPic2.png"))

        with open(self.conf_file, "r") as config_file:
            data = dict(json.load(config_file))

            with open(f"./data/{data['initial_theme']}.css") as file:
                self.setStyleSheet(" ".join(file.readlines()))

        self.txt_label = QtWidgets.QLabel(self)
        self.txt_label.setText("Welcome")
        b_font = QFont()
        b_font.setPointSize(19)
        b_font.setBold(True)
        b_font.setWeight(75)
        self.txt_label.setFont(b_font)
        self.txt_label.setAlignment(QtCore.Qt.AlignCenter)

        self.resize(507, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.pic_label)
        self.verticalLayout.addWidget(self.txt_label)
        self.setWindowIcon(QIcon("./data/favicon2.png"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindowUi()
    startscreen = StartScreenUi()
    sys.exit(app.exec_())
