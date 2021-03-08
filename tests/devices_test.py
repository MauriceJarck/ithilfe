import it_hilfe.devices as device

def test_Device():
    dev1 = device.Device("1", "Maurice", "this is a comment", "2021-03-08 11:09:50.368570")
    assert dev1.name == "1"
    assert dev1.user == "Maurice"
    assert dev1.OS is None
    assert str(dev1) == '1, Maurice, None, Device, this is a comment, 2021-03-08 11:09:50.368570'


def test_WindowsLapTop():
    dev1 = device.WindowsLapTop("1", "Maurice", "this is a comment", "2021-03-08 11:09:50.368570")
    assert dev1.name == "1"
    assert dev1.user == "Maurice"
    assert str(dev1) == "1, Maurice, None, WindowsLapTop, largerbattery: True, upgradedCPU: False"


def test_Macbook():
    dev1 = device.Macbook("2", "Maurice", "this is a comment", "2021-03-08 11:09:50.368570")
    assert dev1.name == "2"
    assert dev1.user == "Maurice"
    assert str(dev1) == '2, Maurice, None, Macbook, this is a comment, 2021-03-08 11:09:50.368570'


def test_WinWorkStation():
    dev1 = device.WindowsWorkStation("3", "Maurice", "this is a comment", "2021-03-08 11:09:50.368570")
    assert dev1.name == "3"
    assert dev1.user == "Maurice"
    assert str(dev1) == '3, Maurice, None, WindowsWorkStation, this is a comment, 2021-03-08 ' '11:09:50.368570'