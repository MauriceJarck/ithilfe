import os

import pytest
import csv
from datetime import datetime
from PySide2 import QtCore
from it_hilfe.it_hilfe_gui2_logic import MainWindowLogic, StartScreen_logic, registered_devices


@pytest.fixture
def main_window(qtbot):
    var = MainWindowLogic()
    qtbot.addWidget(var)
    return var


@pytest.fixture
def start_screen(qtbot):
    var = StartScreen_logic()
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
             "datetime": "2021-03-08 11:09:50.368570"
             })


def test_startscreen(start_screen):
    assert start_screen.win.txt_label.text() == "Welcome"


def test_p_register_validate_open(main_window, qtbot, create_csv):

    # check "registerNew" button
    qtbot.mouseClick(main_window.win.btRegisterNew, QtCore.Qt.LeftButton)
    assert main_window.win.stackedWidget.currentIndex() == 1

    # check "cancel" button
    qtbot.mouseClick(main_window.win.btCancelRegister, QtCore.Qt.LeftButton)
    assert main_window.win.stackedWidget.currentIndex() == 0

    # check shortcut
    qtbot.keyClick(main_window, "n", modifier=QtCore.Qt.ControlModifier)
    assert main_window.win.stackedWidget.currentIndex() == 1

    # no filepath specified
    main_window.win.inUsername.setText("maurice")
    main_window.win.inUsername.setText("2")
    qtbot.mouseClick(main_window.win.btRegister, QtCore.Qt.LeftButton)
    assert main_window.win.stackedWidget.currentIndex() == 1
    assert main_window.win.statusbar.currentMessage() == "no file path specified, visit Ctrl+o or menuebar/edit/open to fix"

    main_window.win.inUsername.clear()
    main_window.win.inDevicename.clear()
    main_window.fname = "testCSV.csv"

    # comboboxes not filled
    main_window.win.inUsername.setText("maurice")
    main_window.win.inUsername.setText("2")
    qtbot.mouseClick(main_window.win.btRegister, QtCore.Qt.LeftButton)
    assert main_window.win.stackedWidget.currentIndex() == 1
    assert main_window.win.statusbar.currentMessage() == "all comboboxes must be specified"

    main_window.win.inUsername.clear()
    main_window.win.inDevicename.clear()

    # line edits not filled
    qtbot.mouseClick(main_window.win.btRegister, QtCore.Qt.LeftButton)
    assert main_window.win.inUsername.text() == "fill all fields"
    assert main_window.win.inDevicename.text() == "fill all fields"
    assert main_window.win.stackedWidget.currentIndex() == 1

    main_window.win.inUsername.clear()
    main_window.win.inDevicename.clear()

    # already taken devname
    main_window.open(True)
    main_window.win.inUsername.setText("maurice")
    main_window.win.inDevicename.setText("1")
    qtbot.mouseClick(main_window.win.btRegister, QtCore.Qt.LeftButton)
    assert main_window.win.stackedWidget.currentIndex() == 1
    assert main_window.win.inDevicename.text() == "in forbidden!!"

    main_window.win.inUsername.clear()
    main_window.win.inDevicename.clear()

    # check valid registration
    # get len(already displayed registrations) before new reg
    qtbot.mouseClick(main_window.win.btCancelRegister, QtCore.Qt.LeftButton)
    assert main_window.win.stackedWidget.currentIndex() == 0
    main_window.open(True)
    count = main_window.win.pViewTable.rowCount()
    # register new
    qtbot.keyClick(main_window, "n", modifier=QtCore.Qt.ControlModifier)
    assert main_window.win.stackedWidget.currentIndex() == 1
    main_window.win.inUsername.setText("maurice")
    main_window.win.inDevicename.setText("2")
    main_window.win.inComboboxDevicetype.setCurrentIndex(2)
    main_window.win.inComboboxOs.setCurrentIndex(1)
    qtbot.mouseClick(main_window.win.btRegister, QtCore.Qt.LeftButton)
    assert main_window.win.stackedWidget.currentIndex() == 0
    # get len(already displayed registrations) after new reg
    assert main_window.win.pViewTable.rowCount() == count + 1
    count += 1
    qtbot.keyClick(main_window, "n", modifier=QtCore.Qt.ControlModifier)
    assert main_window.win.stackedWidget.currentIndex() == 1
    main_window.win.inUsername.setText("maurice")
    main_window.win.inDevicename.setText("3")
    main_window.win.inComboboxDevicetype.setCurrentIndex(1)
    main_window.win.inComboboxOs.setCurrentIndex(2)
    qtbot.mouseClick(main_window.win.btRegister, QtCore.Qt.LeftButton)
    assert main_window.win.stackedWidget.currentIndex() == 0
    # get len(already displayed registrations) after new reg
    assert main_window.win.pViewTable.rowCount() == count + 1


def test_change(main_window, qtbot):
    # valid change
    main_window.fname = "testCSV.csv"
    main_window.open(True)
    qtbot.keyClick(main_window, "d", modifier=QtCore.Qt.ControlModifier)
    main_window.win.inComboBoxDevicename.setCurrentIndex(1)
    main_window.win.inComboBoxChangeParamtype.setCurrentIndex(2)
    main_window.win.inComboBoxChangeNewval.setCurrentIndex(1)
    # qtbot.stop()
    qtbot.mouseClick(main_window.win.btChange, QtCore.Qt.LeftButton)
    assert main_window.win.stackedWidget.currentIndex() == 0

    # check nothing registered
    registered_devices.clear()
    main_window.fname = None
    qtbot.keyClick(main_window, "d", modifier=QtCore.Qt.ControlModifier)
    qtbot.mouseClick(main_window.win.btChange, QtCore.Qt.LeftButton)
    assert main_window.win.statusbar.currentMessage() == "nothing registered yet"


    qtbot.mouseClick(main_window.win.btCancelRegister, QtCore.Qt.LeftButton)
    assert main_window.win.stackedWidget.currentIndex() == 0


def test_search(main_window, qtbot, create_csv):

    main_window.fname = "testCSV.csv"
    main_window.open(True)
    qtbot.keyClick(main_window, "f", modifier=QtCore.Qt.ControlModifier)
    assert main_window.win.stackedWidget.currentIndex() == 2

    qtbot.mouseClick(main_window.win.btCancelSearch, QtCore.Qt.LeftButton)
    assert main_window.win.stackedWidget.currentIndex() == 0

    main_window.win.inUserSearch.setText("peter")
    qtbot.mouseClick(main_window.win.btSearch, QtCore.Qt.LeftButton)
    assert main_window.win.statusbar.currentMessage() == "nothing found"

    main_window.win.inUserSearch.setText("maurice")
    qtbot.mouseClick(main_window.win.btSearch, QtCore.Qt.LeftButton)
    assert main_window.win.statusbar.currentMessage() == "found 1 match/es"
    assert main_window.win.pSearchTable.rowCount() == 1

    main_window.win.inUserSearch.clear()
    qtbot.mouseClick(main_window.win.btSearch, QtCore.Qt.LeftButton)
    assert main_window.win.inUserSearch.text() == "fill all fields"


def test_print(qtbot, main_window, create_csv):
    qtbot.keyClick(main_window, "p", modifier=QtCore.Qt.ControlModifier)
    assert main_window.win.statusbar.currentMessage() == "no file path specified, visit Ctrl+o or menuebar/edit/open to fix"

    main_window.fname = "testCSV.csv"
    main_window.open(True)
    assert main_window.win.statusbar.currentMessage() == ""
    main_window.print(True)
    assert main_window.document.toPlainText() == 'name,username,OS,device_type,comment,extras,datetime\n' ' \n'' 1,maurice,win10,WindowsWorkStation,toller pc,[],2021-03-08 11:09:50.368570\n' ' \n'

def test_new(main_window, qtbot):

    main_window.dir = ".."
    main_window.new(True, test=True)
    assert main_window.win.stackedWidget.currentIndex() == 4
    main_window.win.inNewFilename.setText("newCSV")

    qtbot.mouseClick(main_window.win.btCreate, QtCore.Qt.LeftButton)
    assert main_window.win.stackedWidget.currentWidget() == main_window.win.pView
    # os.remove("newCSV.csv")
