class device:
    def __init__(self, name, user):
        self.name = name
        self.user = user
        self.OS = None

    def __str__(self):
        return f"{self.name}, {self.user}, {self.OS}"


class windowsWorkStation(device):
    expected_OS = ["Win10", "Win7"]


class windowsLapTop(device):
    def __init__(self, name, user):
        super().__init__(name, user)
        self.largerBattery = True
        self.upgradedCPU = False

    expected_OS = ["Win10", "Win7"]


class macbook(device):
    def __init__(self, name, user):
        super().__init__(name, user)
        self.OS = "MacOS"


registered_devices = {}
options = ["search by username", "register new", "view all", "change parameter", "quit program"]    #to extend functionality add new menue options here
attributes = ["name", "user", "OS", "upgradedCPU", "largerBattery"]                                 #to extend functionality add new attributes here
valid_OS = {"windows": ["windowsLapTop", "windowsWorkStation"], "apple": ["macbook"],               #to extend variety of OS add os type as key and vaild devices as value to dict
            "Linux": ["LinuxWorkstation, LinuxLapTop"]}
valid_devices = [windowsLapTop, windowsWorkStation, macbook]                                        #to add more classes add class here


def getAvailable(list):
    a = int(input("\n".join("{}:{}".format(i + 1, x) for i, x in enumerate(list)) + "\n>"))
    if a != 0 and a <= len(list):
        return a
    else:
        raise IndexError


def view():
    if len(registered_devices) != 0:
        print("device name, username, Os, device type, [notes]")
        for x in registered_devices.keys():
            print(registered_devices.get(x), ",", [[y, registered_devices.get(x).__dict__.get(y)] for y in
                                                   list(registered_devices.get(x).__dict__)[3:]])
    else:
        print("no device registered yet")


def register():
    newDeviceType = getAvailable([x.__name__ for x in valid_devices]) - 1
    newDeviceName = int(input("enter devicename as int \nalready taken:{}\n>".format(' '.join(str(list(registered_devices.keys()))))))
    new = valid_devices[newDeviceType](newDeviceName, input("enter username \n>"))
    if newDeviceName not in registered_devices.keys():
        if str(valid_devices[newDeviceType].__name__) in valid_OS.get("windows"):  # extend for more OS options/types
            new.OS = valid_devices[newDeviceType].expected_OS[getAvailable(valid_devices[newDeviceType].expected_OS) - 1]
        registered_devices[new.name] = new
    else:
        print('\033[91m' + "already taken dev name\n" + '\033[0m')
    return [newDeviceType, newDeviceName, new.user, new.OS]#for testing purposes


def search(username):
    if len(registered_devices) == 0:
        print("no devices registered yet")
    else:
        if not [print("match found: ", registered_devices.get(x)) for x in registered_devices.keys() if
                registered_devices.get(x).user == username]:
            print("no match found")


def change_param(devicename, paramtype, newparam):
    for x in registered_devices:
        a = registered_devices.get(x)
        if a.name == devicename:
            setattr(a, str(attributes[paramtype]), newparam)
    return (f"{registered_devices.get(devicename).__dict__}")#for testing purposes

def main():                                                             #to extend menue functionality add here
    print("welcome to IT service\ntype no. of what you wish to do\n")
    while True:
        try:
            w = getAvailable(options)
            if w == 1:
                search(input("enter name you wish to search for\n>"))
            if w == 2:
                register()
            elif w == 3:
                view()
            elif w == 4:
                if len(registered_devices) != 0:
                    name = int(input("existent devicenames: {}\nenter devicename you want to change \n> ".format(
                            " ".join(str(list(registered_devices.keys()))))))
                    type = getAvailable(list(registered_devices.get(name).__dict__.keys())[1:])
                    print(name)
                    change_param(name,type,input("enter new parameter > "))

                else:
                    print("no devices registered yet")
            elif w == 5:
                break

        except(ValueError, IndexError):
            print('\033[91m' + "index can only be int and must belong to range of available choices\n" + '\033[0m')
    quit(0)

if __name__ == "__main__":
    main()
