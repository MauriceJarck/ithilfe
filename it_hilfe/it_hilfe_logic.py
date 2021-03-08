

def register(devname: str, devtype, username: str, os: str, comment: str, datetime: str, registered_devices: dict) -> object:
    """creates new instance of a given class
    Args:
        devname: defines the Name of a device
        devtype: defines the parent class
        username: defines the name of new Device user
        os: defines os of new Device
        registered_devices: new instance will be stored in this dict
    Returns:
        new instance to given class  """

    new = devtype(devname, username, comment, datetime)
    new.OS = os
    registered_devices[new.name] = new
    return new


def search(username, registered_devices):
    """searches registered_devices for a given username
    Args:
        username: defines the username to search for
        registered_devices: new instance will be stored in this dict
    Returns:
        list of matching usernames or list containing "nothing found"
    """

    return [x for x in registered_devices.values() if x.user == username]


def change_param(devicename: str, paramtype, newval: str, registered_devices: dict) -> object:
    """changes a parameter
    Changes a parameter of a device stored in registered_devices to a new value
    Args:
        devicename: defines the name of the device of which a parameter will be changed
        paramtype: defines the parameter which will be changed
        newval: defines the value which will replace the previously defined value
        registered_devices: changed to device will be stored in this dict
    Returns:
        newly changed device
        """
    setattr(registered_devices[devicename], paramtype, newval)
    return registered_devices[devicename]