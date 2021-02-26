import pytest
import csv
from datetime import datetime
from PyQt5 import QtCore
from it_hilfe_gui2 import MainWindow, StartScreen, registered_devices   


@pytest.fixture
def main_window(qtbot):
    var = MainWindow()
    qtbot.addWidget(var)
    return var


@pytest.fixture
def start_screen(qtbot):
    var = StartScreen()
    qtbot.addWidget(var)
    return var


@pytest.fixture(scope="function")
def create_csv():
    with open("testCSV.csv", "w") as f:
        f.truncate()

    with open("testCSV.csv", "w") as f:
        fieldnames = ["name", "username", "OS", "device_type", "comment", "extras", "datetime"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(
            {"name": 1,
             "username": "maurice",
             "OS": "win10",
             "device_type": "WindowsWorkStation",
             "extras": [],
             "comment": "toller pc",
             "datetime": str(datetime.now())
             })


def test_startscreen(start_screen):
    assert start_screen.label.text() == "welcome"


def test_p_register_validate_open(main_window, qtbot, create_csv):

    # check "registerNew" button
    qtbot.mouseClick(main_window.btRegisterNew, QtCore.Qt.LeftButton)
    assert main_window.stackedWidget.currentIndex() == 1

    # check "cancel" button
    qtbot.mouseClick(main_window.btCancelRegister, QtCore.Qt.LeftButton)
    assert main_window.stackedWidget.currentIndex() == 0

    # check shortcut
    qtbot.keyClick(main_window, "n", modifier=QtCore.Qt.ControlModifier)
    assert main_window.stackedWidget.currentIndex() == 1

    # no filepath specified
    main_window.inUsername.setText("maurice")
    main_window.inUsername.setText("2")
    qtbot.mouseClick(main_window.btRegister, QtCore.Qt.LeftButton)
    assert main_window.stackedWidget.currentIndex() == 1
    assert main_window.statusbar.currentMessage() == "no file path specified, visit Ctrl+o or menuebar/edit/open to fix"

    main_window.inUsername.clear()
    main_window.inDevicename.clear()
    main_window.fname = r"C:\Users\maurice.jarck\Documents\Projects\it_hilfe\tests\testCSV.csv"

    # comboboxes not filled
    main_window.inUsername.setText("maurice")
    main_window.inUsername.setText("2")
    qtbot.mouseClick(main_window.btRegister, QtCore.Qt.LeftButton)
    assert main_window.stackedWidget.currentIndex() == 1
    assert main_window.statusbar.currentMessage() == "all comboboxes must be specified"

    main_window.inUsername.clear()
    main_window.inDevicename.clear()

    # line edits not filled
    qtbot.mouseClick(main_window.btRegister, QtCore.Qt.LeftButton)
    assert main_window.inUsername.text() == "fill all fields"
    assert main_window.inDevicename.text() == "fill all fields"
    assert main_window.stackedWidget.currentIndex() == 1

    main_window.inUsername.clear()
    main_window.inDevicename.clear()

    # already taken devname
    main_window.open(True)
    main_window.inUsername.setText("maurice")
    main_window.inDevicename.setText("1")
    qtbot.mouseClick(main_window.btRegister, QtCore.Qt.LeftButton)
    assert main_window.stackedWidget.currentIndex() == 1
    assert main_window.inDevicename.text() == "in forbidden!!"

    main_window.inUsername.clear()
    main_window.inDevicename.clear()

    # check valid registration
    # get len(already displayed registrations) before new reg
    qtbot.mouseClick(main_window.btCancelRegister, QtCore.Qt.LeftButton)
    assert main_window.stackedWidget.currentIndex() == 0
    main_window.open(True)
    count = main_window.tableWidgetAllRegistered.rowCount()
    # register new
    qtbot.keyClick(main_window, "n", modifier=QtCore.Qt.ControlModifier)
    assert main_window.stackedWidget.currentIndex() == 1
    main_window.inUsername.setText("maurice")
    main_window.inDevicename.setText("2")
    main_window.inComboboxDevicetype.setCurrentIndex(2)
    main_window.inComboBoxRegisterOS.setCurrentIndex(1)
    qtbot.mouseClick(main_window.btRegister, QtCore.Qt.LeftButton)
    assert main_window.stackedWidget.currentIndex() == 0
    # get len(already displayed registrations) after new reg
    assert main_window.tableWidgetAllRegistered.rowCount() == count + 1

def test_change(main_window, qtbot):
    # valid change
    main_window.fname = r"C:\Users\maurice.jarck\Documents\Projects\it_hilfe\tests\testCSV.csv"
    main_window.open(True)
    qtbot.keyClick(main_window, "d", modifier=QtCore.Qt.ControlModifier)
    main_window.inComboBoxDevicename.setCurrentIndex(1)
    main_window.inComboBoxChangeParamtype.setCurrentIndex(2)
    main_window.inComboBoxChangeNewval.setCurrentIndex(1)
    # qtbot.stop()
    qtbot.mouseClick(main_window.btChange, QtCore.Qt.LeftButton)
    assert main_window.stackedWidget.currentIndex() == 0

    # check nothing registered
    registered_devices.clear()
    main_window.fname = None
    qtbot.keyClick(main_window, "d", modifier=QtCore.Qt.ControlModifier)
    qtbot.mouseClick(main_window.btChange, QtCore.Qt.LeftButton)
    assert main_window.statusbar.currentMessage() == "nothing registered yet"


    qtbot.mouseClick(main_window.btCancelRegister, QtCore.Qt.LeftButton)
    assert main_window.stackedWidget.currentIndex() == 0

def test_search(main_window, qtbot, create_csv):

    main_window.fname = r"C:\Users\maurice.jarck\Documents\Projects\it_hilfe\tests\testCSV.csv"
    main_window.open(True)
    qtbot.keyClick(main_window, "f", modifier=QtCore.Qt.ControlModifier)
    assert main_window.stackedWidget.currentIndex() == 2

    qtbot.mouseClick(main_window.cancelSearch, QtCore.Qt.LeftButton)
    assert main_window.stackedWidget.currentIndex() == 0

    main_window.inUserSearch.setText("peter")
    qtbot.mouseClick(main_window.btSearch, QtCore.Qt.LeftButton)
    assert main_window.statusbar.currentMessage() == "nothing found"

    main_window.inUserSearch.setText("maurice")
    qtbot.mouseClick(main_window.btSearch, QtCore.Qt.LeftButton)
    assert main_window.statusbar.currentMessage() == "found 1 match/es"
    assert main_window.tableWidgetSearch.rowCount() == 1

    main_window.inUserSearch.clear()
    qtbot.mouseClick(main_window.btSearch, QtCore.Qt.LeftButton)
    assert main_window.inUserSearch.text() == "fill all fields"


