import builtins
from it_hilfe import it_hilfe4


def keyboardInput(mocked_inputs):
    builtins.input = lambda _x: input_values.pop(0)
    input_values = mocked_inputs


def test_device():
    dev1 = it_hilfe4.device("macbook", "Maurice")
    assert dev1.name == "macbook"
    assert dev1.user == "Maurice"
    assert dev1.OS == None


def test_windowsLapTop():
    it_hilfe4.windowsLapTop("WindowsLapTop", "Maurice")

def test_macbook():
    it_hilfe4.macbook("macbook", "maurice")

def test_getAvialable():
    keyboardInput([1])
    assert it_hilfe4.getAvailable([1, 2, 3]) == 1

    try:
        keyboardInput([4])
        it_hilfe4.getAvailable([1, 2, 3])
    except ValueError:
        pass

    keyboardInput([1])
    assert type(it_hilfe4.getAvailable([1, 2, 3])) is int


def test_view(capsys):
    it_hilfe4.view()
    captured = capsys.readouterr()
    assert captured.out == "no device registered yet\n"

def test_search(capsys):
    it_hilfe4.search("maurice")
    captured = capsys.readouterr()
    assert captured.out == "no devices registered yet\n"

def test_register(capsys):
    keyboardInput([1, 1, "maurice", 2])
    assert it_hilfe4.register() == [0, 1, "maurice", "Win7"]

    keyboardInput([1, 1, "maurice", 2])
    it_hilfe4.register()
    captured = capsys.readouterr()
    assert captured.out == 'already taken dev name\n\n'


def test_view2(capsys):
    it_hilfe4.view()
    captured = capsys.readouterr()
    assert captured.out == ('device name, username, Os, device type, [notes]\n' "1, maurice, Win7 , [['largerBattery', True], ['upgradedCPU', 'False']]\n")

def test_search2(capsys):
    it_hilfe4.search("peter")
    captured = capsys.readouterr()
    assert captured.out == 'no match found\n'

# https://github.com/JackWolf24/ithilfe.git