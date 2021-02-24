from it_hilfe import it_hilfe4_2
from pytest import fixture, raises, mark

@fixture(scope="function")
def clearDir():
    yield
    it_hilfe4_2.registered_devices.clear()


@fixture(scope="function")
def create_single_register():
    new = it_hilfe4_2.WindowsLapTop(1, "Maurice")
    new.OS = "Win7"
    it_hilfe4_2.registered_devices[new.name] = new
    assert new.name == 1
    assert new.user == "Maurice"
    assert new.OS == "Win7"
    assert new.bitlockkey == 1234
    assert new.largerBattery is True
    assert new.upgradedCPU is False


def test_Device():
    dev1 = it_hilfe4_2.Device(1, "Maurice")
    assert dev1.name == 1
    assert dev1.user == "Maurice"
    assert dev1.OS is None
    assert str(dev1) == "1, Maurice, None, Device"


def test_WindowsLapTop():
    dev1 = it_hilfe4_2.WindowsLapTop(1, "Maurice")
    assert dev1.name == 1
    assert dev1.user == "Maurice"
    assert str(dev1) == "1, Maurice, None, WindowsLapTop, largerbattery: True, upgradedCPU: False"



def test_Macbook():
    dev1 = it_hilfe4_2.Macbook(2, "Maurice")
    assert dev1.name == 2
    assert dev1.user == "Maurice"
    assert str(dev1) == "2, Maurice, MacOS, Macbook"


def test_WinWorkStation():
    dev1 = it_hilfe4_2.WindowsWorkStation(3, "Maurice")
    assert dev1.name == 3
    assert dev1.user == "Maurice"
    assert str(dev1) == "3, Maurice, None, WindowsWorkStation"


def test_getAvialable(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: 1)
    assert it_hilfe4_2.get_available(["search by username", "register new", "view all"]) == "search by username"

    with raises(IndexError):
        monkeypatch.setattr("builtins.input", lambda _: 4)
        it_hilfe4_2.get_available(["search by username", "register new", "view all"])


@mark.parametrize("test_input,expected",
                  [([1, 1, "maurice", 1], [1, "maurice", "Win10", "WindowsLapTop", True, False, 1234]),
                   ([2, 2, "Peter", 1], [2, "Peter", "Win10", "WindowsWorkStation"]),
                   ([3, 3, "Heinz"], [3, "Heinz", "MacOS", "Macbook"]),
                   ([1, 1, "maurice", 1], [])])
def test_register(monkeypatch, test_input, expected):
    monkeypatch.setattr("builtins.input", lambda _x: test_input.pop(0))
    func = it_hilfe4_2.register()
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
    it_hilfe4_2.registered_devices.clear()

    new = it_hilfe4_2.WindowsLapTop(1, "maurice")
    new.OS = "Win7"
    it_hilfe4_2.registered_devices[new.name] = new
    func = it_hilfe4_2.view()
    assert func[0].name == 1
    assert func[0].user == "maurice"
    assert func[0].OS == "Win7"
    assert func[0].__class__.__name__ == "WindowsLapTop"
    assert func[0].largerBattery is True
    assert func[0].upgradedCPU is False
    assert func[0].bitlockkey == 1234

    it_hilfe4_2.registered_devices.clear()

    assert it_hilfe4_2.view() == ['None']

@mark.parametrize("test_input,expected", [
    ([1, "user", "peter"], [1, "peter", "Win7", "WindowsLapTop", True, False]),
    ([1, "OS", 2], [1, "Maurice", "Win7", "WindowsLapTop", True, False]),
    ([1, "largerBattery", False], [1, "Maurice", "Win7", "WindowsLapTop", False, False]),
    ([1, "upgradedCPU", True], [1, "Maurice", "Win7", "WindowsLapTop", True, True])])
def test_change(test_input, expected, create_single_register, monkeypatch):

    monkeypatch.setattr("builtins.input", lambda _x: test_input[2])
    func = it_hilfe4_2.change_param(test_input[0], test_input[1])

    assert func.name == expected[0]
    assert func.user == expected[1]
    assert func.OS == expected[2]
    assert func.__class__.__name__ == expected[3]
    assert func.largerBattery == expected[4]
    assert func.upgradedCPU == expected[5]


def test_search(create_single_register):
    func = it_hilfe4_2.search("Maurice")
    assert func[0].name == 1
    assert func[0].user == "Maurice"
    assert func[0].OS == "Win7"
    assert func[0].__class__.__name__ == "WindowsLapTop"
    assert func[0].largerBattery is True
    assert  func[0].upgradedCPU is False

    assert it_hilfe4_2.search("Heinz") == []

    it_hilfe4_2.registered_devices.clear()

    assert it_hilfe4_2.search("maurice") == []


@mark.parametrize("test_input, expected", [
    ([True, 1], '\x1b[91m\n' 'sure about clearing stored data?\x1b[0m\n' '\x1b[92m\n' 'everything cleared\n''\x1b[0m\n'),
    ([False, 1, 1, "Maurice"], '\x1b[92mdelete all related to:\x1b[0m\n' '\x1b[91m\n' 'sure about clearing stored data?\x1b[0m\n' '\x1b[92m\n' 'cleared\x1b[0m\n'),
    ([False, 2, 1, 1], '\x1b[92mdelete all related to:\x1b[0m\n' '\x1b[91m\n' 'sure about clearing stored data?\x1b[0m\n' '\x1b[92m\n' 'cleared\x1b[0m\n')])
def test_delete(capsys, clearDir, test_input, expected, monkeypatch, create_single_register):
    inputlist2 = test_input[1:]
    monkeypatch.setattr("builtins.input", lambda _x: inputlist2.pop(0))
    it_hilfe4_2.delete(test_input[0])
    captured = capsys.readouterr()
    assert captured.out == expected

def test_save(create_single_register, clearDir, monkeypatch):
    it_hilfe4_2.save()

    with open("../data/names.csv", "r") as file:
        data = file.readlines()
        assert data == ['sep = ,\n', 'name,username,OS,device_type,notes\n', '1,Maurice,Win7,WindowsLapTop,"[(\'largerBattery\', True), (\'upgradedCPU\', ' 'False)]"\n']

    monkeypatch.setattr("builtins.input", lambda _x: [1].pop(0))
    it_hilfe4_2.delete(True)

def test_update(clearDir, monkeypatch):
    inputlist2 = [1, 1, "maurice", 2]
    monkeypatch.setattr("builtins.input", lambda _x: inputlist2.pop(0))
    assert str(it_hilfe4_2.register()) == '1, maurice, Win7, WindowsLapTop, largerbattery: True, upgradedCPU: False'
    it_hilfe4_2.save()

    with open("../data/names.csv", "r") as file:
        data = file.readlines()
        assert data == ['sep = ,\n', 'name,username,OS,device_type,notes\n', '1,maurice,Win7,WindowsLapTop,"[(\'largerBattery\', True), (\'upgradedCPU\', ' 'False)]"\n']

    it_hilfe4_2.update()

    with open("../data/names.csv", "r") as file:
        data = file.readlines()
        assert data == ['name,username,OS,device_type,notes\n', '1,maurice,Win7,WindowsLapTop,"[(\'largerBattery\', True), (\'upgradedCPU\', ' 'False)]"\n', 'lse)]"\n']


    monkeypatch.setattr("builtins.input", lambda _x: [1].pop(0))
    it_hilfe4_2.delete(True)

@mark.parametrize("test_input, expected",
                  [([2,1,1,"maurice",2,8], '\n' '1, maurice, Win7, WindowsLapTop, largerbattery: True, upgradedCPU: False\n' '\n' '\x1b[92m\n' 'saved\x1b[0m\n' 'ended program\n'),
                   ([1,"maurice",8], '\n' '1, maurice, Win7, WindowsLapTop, largerbattery: True, upgradedCPU: False \n' '\n' '\x1b[92m\n' 'saved\x1b[0m\n' 'ended program\n'),
                   ([3,8],'\n' '\x1b[92mdevice name, username, Os, device type, [notes]\x1b[0m\n' '1, maurice, Win7, WindowsLapTop, largerbattery: True, upgradedCPU: False \n' '\n' '\x1b[92m\n' 'saved\x1b[0m\n' 'ended program\n'),
                   ([4,1,1,"peter",8],'\x1b[92mcurrent value:\x1b[0m maurice\n' '\x1b[92m\n''changed:\n' '\x1b[0m1, peter, Win7, WindowsLapTop, largerbattery: True, upgradedCPU: ' 'False\n' '\n' '\x1b[92m\n' 'saved\x1b[0m\n' 'ended program\n'),
                   ([5,1,1,"peter",8],'\x1b[92mdelete all related to:\x1b[0m\n' '\x1b[91m\n' 'sure about clearing stored data?\x1b[0m\n' '\x1b[92m\n' 'cleared\x1b[0m\n' '\x1b[92m\n' 'saved\x1b[0m\n' 'ended program\n'),
                   ([2,1,1,"maurice",2,8], '\n' '1, maurice, Win7, WindowsLapTop, largerbattery: True, upgradedCPU: False\n' '\n' '\x1b[92m\n' 'saved\x1b[0m\n' 'ended program\n'),
                   ([6,1,8],'\x1b[91m\n' 'sure about clearing stored data?\x1b[0m\n' '\x1b[92m\n' 'everything cleared\n' '\x1b[0m\n' '\x1b[92m\n' 'saved\x1b[0m\n' 'ended program\n'),
                   ([2,1,1,"maurice",2,8], '\n' '1, maurice, Win7, WindowsLapTop, largerbattery: True, upgradedCPU: False\n' '\n' '\x1b[92m\n' 'saved\x1b[0m\n' 'ended program\n'),
                   ([7,8],'\x1b[92m\nsaved\x1b[0m\nended program\n'),
                   ([8],'\x1b[92m\nsaved\x1b[0m\nended program\n'),
                   ([0,8],'\x1b[91m\n' 'index must belong to range of available choices\n' '\x1b[0m\n' '\x1b[92m\n' 'saved\x1b[0m\n' 'ended program\n'),
                   ([9,8],'\x1b[91m\n' 'index must belong to range of available choices\n' '\x1b[0m\n' '\x1b[92m\n' 'saved\x1b[0m\n' 'ended program\n')])
def test_main(test_input,expected,  monkeypatch, capsys):

    monkeypatch.setattr("builtins.input", lambda _x: test_input.pop(0))
    it_hilfe4_2.main()
    captured = capsys.readouterr()
    assert captured.out == expected

