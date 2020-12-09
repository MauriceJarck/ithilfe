from it_hilfe.it_hilfe4_2 import *
from pytest import fixture, raises, mark


@fixture(scope="function")
def clearDir():
    yield
    registered_devices.clear()
    # print("clear", it_hilfe4.registered_devices)

@fixture(scope="function")
def create_single_register(monkeypatch):
    inputlist2 = [1, 1, "maurice", 2]
    monkeypatch.setattr("builtins.input", lambda _x: inputlist2.pop(0))
    register()
    # print("register", registered_devices)


def test_device():
    dev1 = device("1", "Maurice")
    assert dev1.name == "1"
    assert dev1.user == "Maurice"
    assert dev1.OS == None


def test_windowsLapTop():
    dev1 = windowsLapTop("1", "Maurice")
    assert dev1.name == "1"
    assert dev1.user == "Maurice"

def test_macbook():
    dev1 = windowsLapTop("2", "Maurice")
    assert dev1.name == "2"
    assert dev1.user == "Maurice"

def test_WinWorkStation():
    dev1 = windowsWorkStation("3", "Maurice")
    assert dev1.name == "3"
    assert dev1.user == "Maurice"

def test_getAvialable(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: 1)
    assert getAvailable([1, 2, 3]) == 1

    with raises(IndexError) as Error:
        monkeypatch.setattr("builtins.input", lambda _: 4)
        getAvailable([1, 2, 3])
    assert Error.type is IndexError


@mark.parametrize("test_input,expected",
                  [([1, 1, "maurice", 1], [0, 1, "maurice", "Win10"]), ([2, 2, "Peter", 1], [1, 2, 'Peter', 'Win10']),
                   ([3, 3, "Heinz"], [2, 3, 'Heinz', 'MacOS']), ([1, 1, "maurice", 1], [0, 1, "maurice", "Win10"])])
def test_register(capsys, monkeypatch, test_input, expected, clearDir):
    inputlist = test_input
    monkeypatch.setattr("builtins.input", lambda _x: inputlist.pop(0))
    assert register() == expected or '\x1b[91malready taken dev name\n\x1b[0m\n'

def test_view(capsys, monkeypatch, clearDir):

    view()
    captured = capsys.readouterr()
    assert captured.out == '\x1b[92mdevice name, username, Os, device type, [notes]\x1b[0m\n'

    inputlist2 = [1, 1, "maurice", 2]
    monkeypatch.setattr("builtins.input", lambda _x: inputlist2.pop(0))
    register()

    view()
    captured = capsys.readouterr()
    assert captured.out == ('\x1b[92mdevice name, username, Os, device type, [notes]\x1b[0m\n'"1, maurice, Win7 , windowsLapTop , [['largerBattery', True], ['upgradedCPU', " 'False]]\n')

@mark.parametrize("test_input,expected",[
        ([1,1,"peter"], ("{'name': 1, 'user': 'peter', 'OS': 'Win7', 'largerBattery': True, " "'upgradedCPU': False}")),
        ([1,2,"Win10"], ("{'name': 1, 'user': 'peter', 'OS': 'Win10', 'largerBattery': True, " "'upgradedCPU': False}")),
        ([1,3, True],   ("{'name': 1, 'user': 'peter', 'OS': 'Win10', 'largerBattery': True, " "'upgradedCPU': True}")),
        ([1,4, False],  ("{'name': 1, 'user': 'peter', 'OS': 'Win10', 'largerBattery': False, " "'upgradedCPU': True}"))])
def test_change(capsys, monkeypatch, test_input, expected, create_single_register):

    assert change_param(test_input[0], test_input[1], test_input[2]) == expected


def test_search(capsys, monkeypatch, clearDir):
    registered_devices.clear()

    inputlist2 = [1, 1, "maurice", 2]
    monkeypatch.setattr("builtins.input", lambda _x: inputlist2.pop(0))
    assert register() == [0, 1, 'maurice', 'Win7']

    search("Heinz")
    captured = capsys.readouterr()
    assert captured.out == '\x1b[91mno match found\n\x1b[0m\n'

@mark.parametrize("test_input, expected", [
    ([True, None, 1], ('\x1b[91m\n''sure about clearing stored data?\x1b[0m\n''\x1b[92m\n''everthing cleared\x1b[0m\n')),
    ([False, 1, 1, "maurice"], ('\x1b[91m\n''sure about clearing stored data?\x1b[0m\n''\x1b[92m\n''cleared\x1b[0m\n')),
    ([False, 2, 1, 1], ('\x1b[91m\n''sure about clearing stored data?\x1b[0m\n''\x1b[92m\n''cleared\x1b[0m\n'))])
def test_delete(capsys, clearDir, test_input, expected, monkeypatch, create_single_register):
    inputlist2 = test_input[2:]
    monkeypatch.setattr("builtins.input", lambda _x: inputlist2.pop(0))
    delete(test_input[0], test_input[1])
    captured = capsys.readouterr()
    assert captured.out == expected

def test_save(create_single_register, clearDir, monkeypatch):
    save()

    with open("../data/names.csv", "r") as file:
        data = file.readlines()
        assert data == ['sep = ,\n','name,username,OS,device_type,notes\n','1,maurice,Win7,windowsLapTop,"[\'largerBattery\', \'upgradedCPU\']"\n']

    monkeypatch.setattr("builtins.input", lambda _x: [1].pop(0))
    delete(True, None)

def test_update(clearDir, monkeypatch):
    inputlist2 = [1, 1, "maurice", 2]
    monkeypatch.setattr("builtins.input", lambda _x: inputlist2.pop(0))
    assert register() == [0, 1, "maurice", "Win7"]
    save()

    with open("../data/names.csv", "r") as file:
        data = file.readlines()
        assert data == ['sep = ,\n', 'name,username,OS,device_type,notes\n', '1,maurice,Win7,windowsLapTop,"[\'largerBattery\', \'upgradedCPU\']"\n']

    update()

    with open("../data/names.csv", "r") as file:
        data = file.readlines()
        assert data == ['name,username,OS,device_type,notes\n', '1,maurice,Win7,windowsLapTop,"[\'largerBattery\', \'upgradedCPU\']"\n','CPU\']"\n']


    monkeypatch.setattr("builtins.input", lambda _x: [1].pop(0))
    delete(True, None)

@mark.parametrize("test_input, expected",[([1],"")])#,([2],""),([3],""),([4],""),([5],""),([6],""),([7],""),([8],""),([0],""),([9],"")])
def test_main(test_input,expected,  monkeypatch, capsys):

    monkeypatch.setattr("builtins.input", lambda _x: test_input.pop(0))
    main()
    captured = capsys.readouterr()
    assert captured.out == expected

    monkeypatch.setattr("builtins.input", lambda _x: [8].pop(0))



