from it_hilfe import it_hilfe4
from pytest import *

@fixture(scope="function")
def clearDir():

    yield
    it_hilfe4.registered_devices.clear()


def test_device():
    dev1 = it_hilfe4.device("macbook", "Maurice")
    assert dev1.name == "macbook"
    assert dev1.user == "Maurice"
    assert dev1.OS == None


def test_windowsLapTop():
    it_hilfe4.windowsLapTop("WindowsLapTop", "Maurice")


def test_macbook():
    it_hilfe4.macbook("macbook", "maurice")


def test_getAvialable(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: 1)
    assert it_hilfe4.getAvailable([1, 2, 3]) == 1

    with raises(IndexError) as Error:
        monkeypatch.setattr("builtins.input", lambda _: 4)
        it_hilfe4.getAvailable([1, 2, 3])
    assert Error.type is IndexError

    monkeypatch.setattr("builtins.input", lambda _: 1)
    assert type(it_hilfe4.getAvailable([1, 2, 3])) is int

@mark.parametrize("test_input,expected", [([1, 1, "maurice", 1],[0, 1, "maurice", "Win10"]),([2, 2, "Peter", 1],[1, 2, 'Peter', 'Win10']),([3, 3, "Heinz"],[2, 3, 'Heinz', 'MacOS']),([1, 1, "maurice", 1],[0, 1, "maurice", "Win10"])])
def test_register(capsys, monkeypatch, test_input, expected,clearDir):
    inputlist = test_input
    monkeypatch.setattr("builtins.input", lambda _x: inputlist.pop(0))
    assert it_hilfe4.register() == expected or '\x1b[91malready taken dev name\n\x1b[0m\n'


def test_view(capsys, monkeypatch,clearDir):
    it_hilfe4.view()
    captured = capsys.readouterr()
    assert captured.out == "no device registered yet\n"

    inputlist2 = [1, 1, "maurice", 2]
    monkeypatch.setattr("builtins.input", lambda _x: inputlist2.pop(0))
    assert it_hilfe4.register() == [0, 1, "maurice", "Win7"]

    it_hilfe4.view()
    captured = capsys.readouterr()
    assert captured.out == (
        'device name, username, Os, device type, [notes]\n' "1, maurice, Win7 , [['largerBattery', True], ['upgradedCPU', 'False']]\n")


def test_search(capsys, monkeypatch,clearDir):
    it_hilfe4.search("maurice")
    captured = capsys.readouterr()
    assert captured.out == "no devices registered yet\n"

    inputlist2 = [1, 1, "maurice", 2]
    monkeypatch.setattr("builtins.input", lambda _x: inputlist2.pop(0))
    assert it_hilfe4.register() == [0, 1, "maurice", "Win7"]

    it_hilfe4.search("peter")
    captured = capsys.readouterr()
    assert captured.out == 'no match found\n'
