from it_hilfe import it_hilfe4
from pytest import raises


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


def test_register(capsys, monkeypatch):
    inputlist = [1, 1, "maurice", 1]
    monkeypatch.setattr("builtins.input", lambda _x: inputlist.pop(0))
    assert it_hilfe4.register() == [0, 1, "maurice", "Win10"]

    inputlist = [1, 1, "maurice", 1]
    monkeypatch.setattr("builtins.input", lambda _x: inputlist.pop(0))
    it_hilfe4.register()
    captured = capsys.readouterr()
    assert captured.out == '\x1b[91malready taken dev name\n\x1b[0m\n'

    it_hilfe4.registered_devices.clear()


def test_view(capsys, monkeypatch):
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

    inputlist2 = [2, 2, "Peter", 1]
    monkeypatch.setattr("builtins.input", lambda _x: inputlist2.pop(0))
    assert it_hilfe4.register() == [1, 2, 'Peter', 'Win10']

    inputlist2 = [3, 3, "Heinz"]
    monkeypatch.setattr("builtins.input", lambda _x: inputlist2.pop(0))
    assert it_hilfe4.register() == [2, 3, 'Heinz', 'MacOS']

    it_hilfe4.registered_devices.clear()


def test_search(capsys, monkeypatch):
    it_hilfe4.search("maurice")
    captured = capsys.readouterr()
    assert captured.out == "no devices registered yet\n"

    inputlist2 = [1, 1, "maurice", 2]
    monkeypatch.setattr("builtins.input", lambda _x: inputlist2.pop(0))
    assert it_hilfe4.register() == [0, 1, "maurice", "Win7"]

    it_hilfe4.search("peter")
    captured = capsys.readouterr()
    assert captured.out == 'no match found\n'
