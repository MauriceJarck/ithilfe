from pytest import fixture
import it_hilfe.it_hilfe_logic as logic
import it_hilfe.devices as devices

registered_devices = {}

@fixture(scope="function")
def create_one_entry():
    entry = logic.register("1", devices.WindowsWorkStation, "maurice", "win10", "this is another comment",
                           "2021-03-08 11:09:50.368570", registered_devices)
    assert entry.name == "1"
    assert entry.user == "maurice"
    assert entry.OS == "win10"
    assert entry.comment == "this is another comment"
    assert entry.datetime == "2021-03-08 11:09:50.368570"

@fixture(scope="function")
def cleanup_registered_devices():
    yield
    registered_devices.clear()


def test_register(cleanup_registered_devices):
    entry = logic.register("1", devices.WindowsWorkStation, "maurice", "win10", "this is another comment", "2021-03-08 11:09:50.368570", registered_devices)
    assert entry.name == "1"
    assert entry.user == "maurice"
    assert entry.OS == "win10"
    assert entry.comment == "this is another comment"
    assert entry.datetime == "2021-03-08 11:09:50.368570"


def test_search(create_one_entry, cleanup_registered_devices):
    results = logic.search("maurice", registered_devices)

    assert len(results) == 1
    assert results[0] == "maurice"



def test_change_param(create_one_entry, cleanup_registered_devices):

    assert registered_devices["1"].OS == "win10"
    to_change = logic.change_param("1", "OS", "win7", registered_devices)
    assert to_change.OS == "win7"
