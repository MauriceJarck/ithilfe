from it_hilfe import it_hilfe4
from pytest import fixture, raises, mark


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


def test_getAvialable(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: 1)
    assert it_hilfe4.get_available(["search by username", "register new", "view all"]) == "search by username"

    with raises(IndexError):
        monkeypatch.setattr("builtins.input", lambda _: 4)
        it_hilfe4.get_available(["search by username", "register new", "view all"])


@mark.parametrize("test_input,expected",
                  [([1, 1, "maurice", 1], [1, "maurice", "Win10", "WindowsLapTop", True, False, 1234]),
                   ([2, 2, "Peter", 1], [2, "Peter", "Win10", "WindowsWorkStation"]),
                   ([3, 3, "Heinz"], [3, "Heinz", "MacOS", "Macbook"]),
                   ([1, 1, "maurice", 1], [])])
def test_register(monkeypatch, test_input, expected):
    monkeypatch.setattr("builtins.input", lambda _x: test_input.pop(0))
    func = it_hilfe4.register()
    if func is not None:
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
    else:
        assert func is None


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
    ([1, "user", "peter"], [1, "peter", "Win7", "WindowsLapTop", True, False]),
    ([1, "OS", 2], [1, "Maurice", "Win7", "WindowsLapTop", True, False]),
    ([1, "largerBattery", False], [1, "Maurice", "Win7", "WindowsLapTop", False, False]),
    ([1, "upgradedCPU", True], [1, "Maurice", "Win7", "WindowsLapTop", True, True])])
def test_change(test_input, expected, create_single_register, monkeypatch):

    monkeypatch.setattr("builtins.input", lambda _x: test_input[2])
    func = it_hilfe4.change_param(test_input[0], test_input[1])

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
    assert  func[0].upgradedCPU is False

    assert it_hilfe4.search("Heinz") == []

    it_hilfe4.registered_devices.clear()

    assert it_hilfe4.search("maurice") == []
