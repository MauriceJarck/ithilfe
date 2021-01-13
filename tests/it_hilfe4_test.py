from it_hilfe import it_hilfe4
from pytest import fixture, raises, mark
from sys import setrecursionlimit

setrecursionlimit(68)  # avoid too much unnecessary recursions


@fixture(scope="function")
def create_single_register():
    new = it_hilfe4.WindowsLapTop(1, "Maurice")
    new.OS = "Win7"
    it_hilfe4.registered_devices[new.name] = new
    assert new.name == 1
    assert new.user == "Maurice"
    assert new.OS == "Win7"
    assert new.bitlockkey == 1234
    assert new.largerBattery is True
    assert new.upgradedCPU is False


def test_Device():
    dev1 = it_hilfe4.Device(1, "Maurice")
    assert dev1.name == 1
    assert dev1.user == "Maurice"
    assert dev1.OS is None
    assert str(dev1) == "1, Maurice, None, Device"


def test_WindowsLapTop():
    dev1 = it_hilfe4.WindowsLapTop(1, "Maurice")
    assert dev1.name == 1
    assert dev1.user == "Maurice"
    assert str(dev1) == "1, Maurice, None, WindowsLapTop, largerbattery: True, upgradedCPU: False"


def test_Macbook():
    dev1 = it_hilfe4.Macbook(2, "Maurice")
    assert dev1.name == 2
    assert dev1.user == "Maurice"
    assert str(dev1) == "2, Maurice, MacOS, Macbook"


def test_WinWorkStation():
    dev1 = it_hilfe4.WindowsWorkStation(3, "Maurice")
    assert dev1.name == 3
    assert dev1.user == "Maurice"
    assert str(dev1) == "3, Maurice, None, WindowsWorkStation"


def test_getAvialable(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: 1)
    assert it_hilfe4.get_available(["search by username", "register new", "view all"]) == "search by username"

    with raises(RecursionError):  # tests is input is wrong val gets invoked
        monkeypatch.setattr("builtins.input", lambda _: ["a"].pop(0))
        it_hilfe4.get_available(["search by username", "register new", "view all"])

    with raises(RecursionError):  # tests is input is help recursion gets invoked
        monkeypatch.setattr("builtins.input", lambda _: [4].pop(0))
        it_hilfe4.get_available(["search by username", "register new", "view all"])

    with raises(RecursionError):  # tests is input is over valid index val
        monkeypatch.setattr("builtins.input", lambda _: [5].pop(0))
        it_hilfe4.get_available(["search by username", "register new", "view all"])

    with raises(RecursionError):  # tests is input is under valid index val
        monkeypatch.setattr("builtins.input", lambda _: [0].pop(0))
        it_hilfe4.get_available(["search by username", "register new", "view all"])


@mark.parametrize("test_input,expected",
                  [([1, 1, "maurice", 1], [1, "maurice", "Win10", "WindowsLapTop", True, False, 1234]),
                   ([2, 2, "Peter", 1], [2, "Peter", "Win10", "WindowsWorkStation"]),
                   ([3, 3, "Heinz"], [3, "Heinz", "MacOS", "Macbook"]),
                   ])
def test_register(monkeypatch, test_input, expected):
    monkeypatch.setattr("builtins.input", lambda _x: test_input.pop(0))
    func = it_hilfe4.register()

    assert func.name == expected[0]
    assert func.user == expected[1]
    assert func.OS == expected[2]
    assert func.__class__.__name__ == expected[3]
    try:
        assert func.largerBattery == expected[4]
        assert func.upgradedCPU == expected[5]
        assert func.bitlockkey == expected[6]
    except AttributeError:
        pass

    with raises(RecursionError):  # test if a already existing registry provokes register() to call itself
        monkeypatch.setattr("builtins.input", lambda _: [1, 1, "maurice"].pop(0))
        it_hilfe4.register()


def test_view():
    it_hilfe4.registered_devices.clear()

    new = it_hilfe4.WindowsLapTop(1, "maurice")
    new.OS = "Win7"
    it_hilfe4.registered_devices[new.name] = new
    func = it_hilfe4.view()
    assert func[0].name == 1
    assert func[0].user == "maurice"
    assert func[0].OS == "Win7"
    assert func[0].__class__.__name__ == "WindowsLapTop"
    assert func[0].largerBattery is True
    assert func[0].upgradedCPU is False
    assert func[0].bitlockkey == 1234

    it_hilfe4.registered_devices.clear()

    assert it_hilfe4.view() == []


@mark.parametrize("test_input,expected", [
    ([1, 1, "peter"], [1, "peter", "Win7", "WindowsLapTop", True, False]),
    ([1, 2, 2], [1, "Maurice", "Win7", "WindowsLapTop", True, False]),
    ([1, 3, False], [1, "Maurice", "Win7", "WindowsLapTop", False, False]),
    ([1, 4, True], [1, "Maurice", "Win7", "WindowsLapTop", True, True])
])
def test_change(test_input, expected, create_single_register, monkeypatch):

    monkeypatch.setattr("builtins.input", lambda _x: test_input.pop(0))
    func = it_hilfe4.change_param()

    assert func.name == expected[0]
    assert func.user == expected[1]
    assert func.OS == expected[2]
    assert func.__class__.__name__ == expected[3]
    assert func.largerBattery == expected[4]
    assert func.upgradedCPU == expected[5]


def test_search(create_single_register):
    func = it_hilfe4.search("Maurice")
    assert func[0].name == 1
    assert func[0].user == "Maurice"
    assert func[0].OS == "Win7"
    assert func[0].__class__.__name__ == "WindowsLapTop"
    assert func[0].largerBattery is True
    assert func[0].upgradedCPU is False

    assert it_hilfe4.search("Heinz") == ['\x1b[91mno match found\n\x1b[0m']

    it_hilfe4.registered_devices.clear()

    assert it_hilfe4.search("maurice") == ['\x1b[91mno match found\n\x1b[0m']
