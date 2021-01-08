class Device:
    def __init__(self, name, user):
        self.name = name
        self.user = user
        self.OS = None

    def __str__(self):
        return f"{self.name}, {self.user}, {self.OS}, {self.__class__.__name__}"

    visible_attr = ["user", "OS"]


class WindowsWorkStation(Device):
    expected_OS = ["Win10", "Win7"]  # extend for more OS options/types


class WindowsLapTop(Device):
    def __init__(self, name, user):
        super().__init__(name, user)
        self.bitlockkey = 1234
        self.largerBattery = True
        self.upgradedCPU = False

    def __str__(self):
        return f"{self.name}, {self.user}, {self.OS}, {self.__class__.__name__}, largerbattery: {self.largerBattery}, upgradedCPU: {self.upgradedCPU}"

    expected_OS = ["Win10", "Win7"]  # extend for more OS options/types
    visible_attr = ["user", "OS", "largerBattery", "upgradedCPU"]


class Macbook(Device):
    def __init__(self, name, user):
        super().__init__(name, user)
        self.OS = "MacOS"

    expected_OS = ["MacOS"]  # extend for more OS options/types


registered_devices = {}
options = ["search by username", "register new", "view all", "change parameter", "quit program"]  # to extend str rep of new menue functionality add here
valid_devices = [WindowsLapTop, WindowsWorkStation, Macbook]  # to add more classes add class here

def get_available(optionslist):
    a = int(input("\n".join(["{}:{}".format(i + 1, x) if type(x) == str else "{}:{}".format(i + 1, x.__name__) for i, x in enumerate(optionslist)])+"\n>"))
    if a != 0 and a <= len(optionslist):
        return optionslist[a-1]
    else:
        raise IndexError


def view():
    print("\nname, user, OS, devtype, notes")
    return [x for x in registered_devices.values()]


def register():
    newdevicetype = get_available(valid_devices)
    newdevicename = input("enter devicename \nalready taken: {}\n>".format(', '.join([str(x) for x in list(registered_devices.keys())]) or "None"))
    new = newdevicetype(newdevicename, input("enter username \n>"))
    if newdevicename not in registered_devices.keys():
        if len(newdevicetype.expected_OS) > 1:
            new.OS = get_available(newdevicetype.expected_OS)
        registered_devices[new.name] = new
        return new


def search(username):
    return [x for x in registered_devices.values() if x.user == username]


def change_param(devicename, paramtype):
    a = registered_devices.get(devicename)
    if paramtype == "OS":
        setattr(a, paramtype, get_available(a.expected_OS))
    else:
        setattr(a, paramtype, input("enter new parameter\n>"))
    return a


def main():  # to extend menu functionality add here
    print("welcome to IT service\ntype no. of what you wish to do\n")
    while True:
        try:
            w = get_available(options)
            if w == "search by username":
                if len(registered_devices) != 0:
                    print("\n"+"".join([str(x) for x in search(input("enter username you wish to search for\n>"))]), "\n" or '\033[91m' + "no match found\n" + '\033[0m')
                else:
                    print('\033[91m' + "no device registered yet\n" + '\033[0m')
            if w == "register new":
                a = register()
                if a is None:
                    print('\033[91m' + "already taken dev name\n" + '\033[0m')
                else:
                    print("\n" + str(a) + "\n")
            elif w == "view all":
                print("\n".join([str(x) for x in view()]),"\n" or '\033[91m' + "no device registered yet\n" + '\033[0m')
            elif w == "change parameter":
                if len(registered_devices) != 0:
                    name = input("existent devicenames: {}\nenter devicename you want to change \n> ".format(", ".join(list(registered_devices.keys()))))
                    paramtype = get_available(registered_devices[name].visible_attr)
                    print("\n" + str(change_param(name, paramtype)) + "\n")
                else:
                    print('\033[91m' + "no device registered yet\n" + '\033[0m')
            elif w == "quit program":
                quit(0)
        except(ValueError, IndexError, AttributeError, KeyError):
            print('\033[91m' + "index can only be int and must belong to range of available choices\n" + '\033[0m')

if __name__ == "__main__":
    main()
