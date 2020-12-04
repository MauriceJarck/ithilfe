from it_hilfe import it_hilfe4
from pytest import fixture, raises, mark


@fixture(scope="function")
def clearDir():
    yield
    it_hilfe4.registered_devices.clear()
    # print("clear", it_hilfe4.registered_devices)

@fixture(scope="function")
def create_single_register(monkeypatch):
    inputlist2 = [1, 1, "maurice", 2]
    monkeypatch.setattr("builtins.input", lambda _x: inputlist2.pop(0))
    it_hilfe4.register()
    # print("register", it_hilfe4.registered_devices)


def test_device():
    dev1 = it_hilfe4.device("1", "Maurice")
    assert dev1.name == "1"
    assert dev1.user == "Maurice"
    assert dev1.OS == None


def test_windowsLapTop():
    dev1 = it_hilfe4.windowsLapTop("1", "Maurice")
    assert dev1.name == "1"
    assert dev1.user == "Maurice"

def test_macbook():
    dev1 = it_hilfe4.windowsLapTop("2", "Maurice")
    assert dev1.name == "2"
    assert dev1.user == "Maurice"

def test_WinWorkStation():
    dev1 = it_hilfe4.windowsWorkStation("3", "Maurice")
    assert dev1.name == "3"
    assert dev1.user == "Maurice"

def test_getAvialable(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: 1)
    assert it_hilfe4.getAvailable([1, 2, 3]) == 1

    with raises(IndexError) as Error:
        monkeypatch.setattr("builtins.input", lambda _: 4)
        it_hilfe4.getAvailable([1, 2, 3])
    assert Error.type is IndexError


@mark.parametrize("test_input,expected",
                  [([1, 1, "maurice", 1], [0, 1, "maurice", "Win10"]), ([2, 2, "Peter", 1], [1, 2, 'Peter', 'Win10']),
                   ([3, 3, "Heinz"], [2, 3, 'Heinz', 'MacOS']), ([1, 1, "maurice", 1], [0, 1, "maurice", "Win10"])])
def test_register(capsys, monkeypatch, test_input, expected, clearDir):
    inputlist = test_input
    monkeypatch.setattr("builtins.input", lambda _x: inputlist.pop(0))
    assert it_hilfe4.register() == expected or '\x1b[91malready taken dev name\n\x1b[0m\n'

def test_view(capsys, monkeypatch, clearDir):

    it_hilfe4.view()
    captured = capsys.readouterr()
    assert captured.out == "no device registered yet\n"

    inputlist2 = [1, 1, "maurice", 2]
    monkeypatch.setattr("builtins.input", lambda _x: inputlist2.pop(0))
    it_hilfe4.register()

    it_hilfe4.view()
    captured = capsys.readouterr()
    assert captured.out == (
        'device name, username, Os, device type, [notes]\n'"1, maurice, Win7 , [['largerBattery', True], ['upgradedCPU', False]]\n")

@mark.parametrize("test_input,expected",[
        ([1,1,"peter"], ("{'name': 1, 'user': 'peter', 'OS': 'Win7', 'largerBattery': True, " "'upgradedCPU': False}")),
        ([1,2,"Win10"], ("{'name': 1, 'user': 'peter', 'OS': 'Win10', 'largerBattery': True, " "'upgradedCPU': False}")),
        ([1,3, True],   ("{'name': 1, 'user': 'peter', 'OS': 'Win10', 'largerBattery': True, " "'upgradedCPU': True}")),
        ([1,4, False],  ("{'name': 1, 'user': 'peter', 'OS': 'Win10', 'largerBattery': False, " "'upgradedCPU': True}"))])
def test_change(capsys, monkeypatch, test_input, expected, create_single_register):

    assert it_hilfe4.change_param(test_input[0], test_input[1], test_input[2]) == expected


def test_search(capsys, monkeypatch, clearDir):
    it_hilfe4.registered_devices.clear()

    it_hilfe4.search("maurice")
    captured = capsys.readouterr()
    assert captured.out == "no devices registered yet\n"

    inputlist2 = [1, 1, "maurice", 2]
    monkeypatch.setattr("builtins.input", lambda _x: inputlist2.pop(0))
    it_hilfe4.register()

    it_hilfe4.search("Heinz")
    captured = capsys.readouterr()
    assert captured.out == 'no match found\n'
