import json
import pytest
from PySide2 import QtCore
from PySide2.QtWidgets import QMessageBox

from it_hilfe.it_hilfe_gui2 import MainWindowUi, StartScreenUi, ComboDelegate
from it_hilfe.validate_json import ItHilfeDataSchema, ItHilfeUserPreferencesSchema


@pytest.fixture
def main_window(qtbot):
    var = MainWindowUi()
    var.show()
    qtbot.addWidget(var)
    return var


@pytest.fixture
def start_screen(qtbot):
    var = StartScreenUi()
    qtbot.addWidget(var)
    var.show()
    return var


@pytest.fixture
def combo_delegate(qtbot):
    var = ComboDelegate()
    qtbot.addWidget(var)
    var.show()
    return var


@pytest.fixture(scope="function")
def create_valid_json(main_window):
    with open("data/jsonTest.json", "w") as f:
        f.truncate()

    with open("data/jsonTest.json", "w") as f:
        data = {
            "devices": {"0": ["007", "peter", "Win7", "Macbook", "this is a comment", "2021-03-19 13:56:40.509002"]},
            "last_open_file_dir": "C:/Users/maurice.jarck/Documents/Projects/it_hilfe/it_hilfe/data"}
        json.dump(data, f)


def test_startscreen(start_screen):
    assert start_screen.txt_label.text() == "Welcome"


def test_p_register_validate_open(main_window, qtbot, create_valid_json, mocker):
    mocker.patch.object(QMessageBox, "question", return_value=QMessageBox.No)

    # check "registerNew" button
    qtbot.mouseClick(main_window.bt_register_new, QtCore.Qt.LeftButton)
    assert main_window.stacked_widget.currentIndex() == 1

    # check "cancel" button
    qtbot.mouseClick(main_window.bt_cancel_register, QtCore.Qt.LeftButton)
    assert main_window.stacked_widget.currentIndex() == 0

    # check shortcut
    qtbot.keyClick(main_window, "n", modifier=QtCore.Qt.ControlModifier)
    assert main_window.stacked_widget.currentIndex() == 1

    # no filepath specified
    qtbot.mouseClick(main_window.bt_register_new, QtCore.Qt.LeftButton)
    main_window.in_username.setText("maurice")
    main_window.in_username.setText("2")
    qtbot.mouseClick(main_window.bt_enter_register, QtCore.Qt.LeftButton)
    assert main_window.stacked_widget.currentIndex() == 1
    assert main_window.statusbar.currentMessage() == "no file path specified, visit Ctrl+o or menuebar/edit/open to fix"

    main_window.in_username.clear()
    main_window.in_devicename.clear()
    main_window.file_path = "./data/jsonTest.json"

    # comboboxes not filled
    main_window.in_username.setText("maurice")
    main_window.in_username.setText("2")
    qtbot.mouseClick(main_window.bt_enter_register, QtCore.Qt.LeftButton)
    assert main_window.stacked_widget.currentIndex() == 1
    assert main_window.statusbar.currentMessage() == "all comboboxes must be filled"

    main_window.in_username.clear()
    main_window.in_devicename.clear()

    # line edits not filled
    qtbot.mouseClick(main_window.bt_enter_register, QtCore.Qt.LeftButton)
    assert main_window.in_username.text() == "fill all fields"
    assert main_window.in_devicename.text() == "fill all fields"
    assert main_window.stacked_widget.currentIndex() == 1

    main_window.in_username.clear()
    main_window.in_devicename.clear()

    # already taken devname
    main_window.load()
    main_window.in_username.setText("maurice")
    main_window.in_devicename.setText("007")
    qtbot.mouseClick(main_window.bt_enter_register, QtCore.Qt.LeftButton)
    assert main_window.stacked_widget.currentWidget() == main_window.p_register
    assert main_window.in_devicename.text() == "in forbidden!!"

    main_window.in_username.clear()
    main_window.in_devicename.clear()

    # check valid registration
    # get len(already displayed registrations) before new reg
    qtbot.mouseClick(main_window.bt_cancel_register, QtCore.Qt.LeftButton)
    assert main_window.stacked_widget.currentIndex() == 0
    main_window.load()
    count = main_window.model.rowCount()
    # register new.
    qtbot.keyClick(main_window, "n", modifier=QtCore.Qt.ControlModifier)
    assert main_window.stacked_widget.currentIndex() == 1
    main_window.in_username.setText("maurice")
    main_window.in_devicename.setText("2")
    main_window.in_combobox_devicetype.setCurrentIndex(2)
    main_window.in_combobox_os.setCurrentIndex(1)
    qtbot.mouseClick(main_window.bt_enter_register, QtCore.Qt.LeftButton)
    assert main_window.stacked_widget.currentIndex() == 0
    # get len(already displayed registrations) after new reg
    assert main_window.model.rowCount() == count + 1
    count += 1
    qtbot.keyClick(main_window, "n", modifier=QtCore.Qt.ControlModifier)
    assert main_window.stacked_widget.currentIndex() == 1
    main_window.in_username.setText("maurice")
    main_window.in_devicename.setText("3")
    main_window.in_combobox_devicetype.setCurrentIndex(1)
    main_window.in_combobox_os.setCurrentIndex(2)
    qtbot.mouseClick(main_window.bt_enter_register, QtCore.Qt.LeftButton)
    assert main_window.stacked_widget.currentWidget() == main_window.p_view
    # get len(already displayed registrations) after new reg
    assert main_window.model.rowCount() == count + 1

    # test hide/show of filtering line_edits
    for editor in main_window.header.editors:
        assert editor.isVisible() is True

    qtbot.mouseClick(main_window.bt_hide_show_filter, QtCore.Qt.LeftButton)

    for editor in main_window.header.editors:
        assert editor.isVisible() is False

    qtbot.mouseClick(main_window.bt_hide_show_filter, QtCore.Qt.LeftButton)

    for editor in main_window.header.editors:
        assert editor.isVisible() is True

    # test save file with no destination specified
    main_window.file_path = None
    main_window.save()
    assert main_window.statusbar.currentMessage() == "no file path set all changes get lost if closed"

    # test delegate aka change values in p_view


def test_reopen_last_file(main_window, mocker, qtbot):
    mocker.patch.object(QMessageBox, "question", return_value=QMessageBox.Yes)
    main_window.reopen_last_file()
    assert main_window.model.rowCount() == 2


def test_delete(main_window, mocker, create_valid_json):

    main_window.file_path = "data/jsonTest.json"
    main_window.load()

    assert main_window.model.rowCount() == 1
    assert len(main_window.registered_devices) == 1

    mocker.patch.object(main_window.table, "selectedIndexes", return_value=[main_window.filters[-1].createIndex(0, 0)])
    mocker.patch.object(QMessageBox, "question", return_value=QMessageBox.Yes)
    mocker.patch.object(QMessageBox, "information", return_value=QMessageBox.Ok)
    main_window.delete()

    assert main_window.filters[-1].rowCount() == 0
    assert len(main_window.registered_devices) == 0


def test_change_theme(main_window):

    with open("./data/light_theme.css") as file:
        light_stylesheed = " ".join(file.readlines())
        assert main_window.styleSheet() == light_stylesheed
        assert main_window.p_preferences.styleSheet() == light_stylesheed

    assert main_window.in_combo_themes.currentText() == "light_theme"
    main_window.change_theme("dark_theme")

    with open("./data/dark_theme.css") as file:
        light_stylesheed = " ".join(file.readlines())
        assert main_window.styleSheet() == light_stylesheed
        assert main_window.p_preferences.styleSheet() == light_stylesheed

    main_window.change_theme("light_theme")

    with open("./data/light_theme.css") as file:
        light_stylesheed = " ".join(file.readlines())
        assert main_window.styleSheet() == light_stylesheed
        assert main_window.p_preferences.styleSheet() == light_stylesheed

    assert main_window.in_combo_themes.currentText() == "light_theme"


def test_hide_show_ani(main_window, qtbot):
    assert main_window.left_menu_frame.maximumWidth() == 0
    main_window.toggle_hide_show_ani(0, 66, "width", main_window.left_menu_frame, b"maximumWidth", )
    qtbot.wait(400)
    assert main_window.left_menu_frame.maximumWidth() == 66
    main_window.toggle_hide_show_ani(0, 66, "width", main_window.left_menu_frame, b"maximumWidth", )
    qtbot.wait(400)
    assert main_window.left_menu_frame.maximumWidth() == 0


def test_hide_show(main_window):
    assert main_window.bt_register_new.isVisible() is True
    main_window.toggle_hide_show(main_window.bt_register_new)
    assert main_window.bt_register_new.isVisible() is False
    main_window.toggle_hide_show(main_window.bt_register_new)
    assert main_window.bt_register_new.isVisible() is True


def test_json_validatation(qtbot, main_window):

    validate = main_window.validate(command=main_window.register, file_path="", forbidden=[""], schema=ItHilfeDataSchema)
    assert validate == 'problem\ncommand: register\nfails: 1'
    assert main_window.statusbar.currentMessage() == "select a file to continue"

    main_window.validate(command=main_window.stacked_widget.setCurrentWidget, data=main_window.p_register,
                         file_path="data/jsonTest.json",
                         forbidden=[""], schema=ItHilfeDataSchema)

    assert main_window.stacked_widget.currentWidget() == main_window.p_register


    # mocker.patch.object(QMessageBox, "critical", return_value = QMessageBox.Ok)
    # main_window.validate(command=main_window.register, file_path="./invalid_json_test.json", forbidden=[""])
    # assert main_window.msg_box == QMessageBox.Ok


def test_print(qtbot, main_window, create_valid_json):
    qtbot.keyClick(main_window, "p", modifier=QtCore.Qt.ControlModifier)
    assert main_window.statusbar.currentMessage() == "no file path specified, visit Ctrl+o or menuebar/edit/open to fix"

    main_window.file_path = "data/jsonTest.json"
    main_window.load()
    assert main_window.statusbar.currentMessage() == ""
    main_window.print(True)
    assert repr(
        main_window.data) == '\'{\\n      "devices"={\\n            "0"=[\\n                  ' '"007".\\n                  "peter".\\n                  ' '"Win7".\\n                  "Macbook".\\n                  "this is a ' 'comment".\\n                  "2021-03-19 13:56:40.509002"\\n            ' ']\\n      }.\\n      ' '"last_open_file_dir"="C:/Users/maurice.jarck/Documents/Projects/it_hilfe/it_hilfe/data"\\n}\''


def test_new(main_window, qtbot):
    main_window.dir = "."
    main_window.new(True, test=True)
    assert main_window.stacked_widget.currentWidget() == main_window.p_create
    main_window.in_new_filename.setText("newJson")

    qtbot.mouseClick(main_window.bt_create, QtCore.Qt.LeftButton)
    assert main_window.stacked_widget.currentWidget() == main_window.p_view

