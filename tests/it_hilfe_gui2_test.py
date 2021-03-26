import json
import pytest
from PySide2 import QtCore
from it_hilfe.it_hilfe_gui2 import MainWindowUi, StartScreenUi


@pytest.fixture
def main_window(qtbot):
    var = MainWindowUi()
    qtbot.addWidget(var)
    return var


@pytest.fixture
def start_screen(qtbot):
    var = StartScreenUi()
    qtbot.addWidget(var)
    return var


@pytest.fixture(scope="function")
def create_valid_json():
    with open("jsonTest.json", "w") as f:
        f.truncate()

    with open("jsonTest.json", "w") as f:
        data = {"devices": {"0": [ "007", "peter", "Win7", "Macbook", "this is a comment", "2021-03-19 13:56:40.509002"] }, "last_open_file_path": "C:/Users/maurice.jarck/Documents/Projects/it_hilfe/it_hilfe/data"}
        json.dump(data, f)


def test_startscreen(start_screen):
    assert start_screen.txt_label.text() == "Welcome"


def test_p_register_validate_open(main_window, qtbot, create_valid_json):
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
    main_window.in_username.setText("maurice")
    main_window.in_username.setText("2")
    qtbot.mouseClick(main_window.bt_register, QtCore.Qt.LeftButton)
    assert main_window.stacked_widget.currentIndex() == 1
    assert main_window.statusbar.currentMessage() == "no file path specified, visit Ctrl+o or menuebar/edit/open to fix"

    main_window.in_username.clear()
    main_window.in_devicename.clear()
    main_window.file_path = "jsonTest.json"

    # comboboxes not filled
    main_window.in_username.setText("maurice")
    main_window.in_username.setText("2")
    qtbot.mouseClick(main_window.bt_register, QtCore.Qt.LeftButton)
    assert main_window.stacked_widget.currentIndex() == 1
    assert main_window.statusbar.currentMessage() == "all comboboxes must be specified"

    main_window.in_username.clear()
    main_window.in_devicename.clear()

    # line edits not filled
    qtbot.mouseClick(main_window.bt_register, QtCore.Qt.LeftButton)
    assert main_window.in_username.text() == "fill all fields"
    assert main_window.in_devicename.text() == "fill all fields"
    assert main_window.stacked_widget.currentIndex() == 1

    main_window.in_username.clear()
    main_window.in_devicename.clear()

    # already taken devname
    main_window.load()
    main_window.in_username.setText("maurice")
    main_window.in_devicename.setText("007")
    qtbot.mouseClick(main_window.bt_register, QtCore.Qt.LeftButton)
    # qtbot.stop()
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
    # register new
    qtbot.keyClick(main_window, "n", modifier=QtCore.Qt.ControlModifier)
    assert main_window.stacked_widget.currentIndex() == 1
    main_window.in_username.setText("maurice")
    main_window.in_devicename.setText("2")
    main_window.in_combobox_devicetype.setCurrentIndex(2)
    main_window.in_combobox_os.setCurrentIndex(1)
    qtbot.mouseClick(main_window.bt_register, QtCore.Qt.LeftButton)
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
    qtbot.mouseClick(main_window.bt_register, QtCore.Qt.LeftButton)
    assert main_window.stacked_widget.currentIndex() == 0
    # get len(already displayed registrations) after new reg
    assert main_window.model.rowCount() == count + 1

    # test hide/show of filtering line_edits
    for editor in main_window.header._editors:
        assert editor.isVisible() is True

    qtbot.mouseClick(main_window.bt_hide_show_filter, QtCore.Qt.LeftButton)

    for editor in main_window.header._editors:
        assert editor.isVisible() is False

    qtbot.mouseClick(main_window.bt_hide_show_filter, QtCore.Qt.LeftButton)

    for editor in main_window.header._editors:
        assert editor.isVisible() is True

    # test save file with no destination specified
    main_window.file_path = None
    main_window.save()
    assert main_window.statusbar.currentMessage() == "no file path set all changes get lost if closed"

    # test delegate aka change values in p_view

def test_print(qtbot, main_window, create_valid_json):
    qtbot.keyClick(main_window, "p", modifier=QtCore.Qt.ControlModifier)
    assert main_window.statusbar.currentMessage() == "no file path specified, visit Ctrl+o or menuebar/edit/open to fix"

    main_window.file_path = "jsonTest.json"
    main_window.load()
    assert main_window.statusbar.currentMessage() == ""
    main_window.print(True)
    # assert main_window.document.toPlainText() == '{"devices": {"0": [ "007", "peter", "Win7", "Macbook", "this is a comment", "2021-03-19 13:56:40.509002" ] }, "last_open_file_path": "C:/Users/maurice.jarck/Documents/Projects/it_hilfe/it_hilfe/data"}'


def test_new(main_window, qtbot):
    main_window.dir = ".."
    main_window.new(True, test=True)
    assert main_window.stacked_widget.currentWidget() == main_window.p_create
    main_window.in_new_filename.setText("newJson")

    qtbot.mouseClick(main_window.bt_create, QtCore.Qt.LeftButton)
    assert main_window.stacked_widget.currentWidget() == main_window.p_view
    # os.remove("newCSV.csv")
