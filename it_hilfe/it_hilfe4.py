class Device:
    def __init__(self, name, user):
        self.name = name
        self.user = user
        self.OS = None

    def __str__(self):
        return f"{self.name}, {self.user}, {self.OS}, {self.__class__.__name__}"

    visible_attr = ["user", "OS"]

class WindowsWorkStation(Device):
    expected_OS = ["Win10", "Win7"] # extend for more OS options/types


class WindowsLapTop(Device):
    def __init__(self, name, user):
        super().__init__(name, user)
        self.bitlockkey = 1234
        self.largerBattery = True
        self.upgradedCPU = False

    def __str__(self):
        return f"{self.name}, {self.user}, {self.OS}, {self.__class__.__name__}, largerbattery: {self.largerBattery}, upgradedCPU: {self.upgradedCPU}"

    expected_OS = ["Win10", "Win7"] # extend for more OS options/types
    visible_attr = ["user", "OS", "largerBattery", "upgradedCPU"]

class Macbook(Device):
    def __init__(self, name, user):
        super().__init__(name, user)
        self.OS = "MacOS"

    expected_OS = ["MacOS"] # extend for more OS options/types


registered_devices = {}
options = ["search by username", "register new", "view all", "change parameter", "quit program"]  # to extend functionality add new menu options here
valid_devices = [WindowsLapTop, WindowsWorkStation, Macbook]  # to add more classes add class here


def get_available(optionslist):
    a = int(input("\n".join(["{}:{}".format(i + 1, x) if type(x) == str else "{}:{}".format(i + 1, x.__name__) for i, x in enumerate(optionslist)])+"\n>"))
    if a != 0 and a <= len(optionslist):
        return optionslist[a-1]
    else:
        raise IndexError


def view():
    print("\nname, user, OS, devtype, notes")
    return "\n".join([str(x) for x in registered_devices.values()]) or "no device registered yet\n"


def register():
    newdevicetype = get_available(valid_devices)
    newdevicename = int(
        input("enter devicename \nalready taken:{}\n>".format(' '.join(str(list(registered_devices.keys()))))))
    new = newdevicetype(newdevicename, input("enter username \n>"))
    if newdevicename not in registered_devices.keys():
        if len(newdevicetype.expected_OS) > 1:
            new.OS = get_available(newdevicetype.expected_OS)
        registered_devices[new.name] = new
        content = f"{newdevicename}, {new.user}, {new.OS}, {newdevicetype.__name__}"  # for testing purposes
    else:
        content = '\033[91m' + "already taken dev name\n" + '\033[0m'
    return content


def search(username):
    if len(registered_devices) == 0:
        msg = ["\nno devices registered yet\n"]
    else:
        msg = [f"match found: {x}\n" for x in registered_devices.values() if x.user == username] or ["\nno match found\n"]
    return msg


def change_param(devicename, paramtype):
    a = registered_devices.get(devicename)
    if paramtype == "OS":  # OS
        newparam = get_available(a.expected_OS)
    else:
        newparam = input("enter new parameter\n>")

    setattr(a, paramtype, newparam)
    return str(a)


def main():  # to extend menu functionality add here
    print("welcome to IT service\ntype no. of what you wish to do\n")
    while True:
        try:
            w = get_available(options)
            if w == "search by username":
                print("\n" + "".join(search(input("enter name you wish to search for\n>"))))
            if w == "register new":
                print("\nentered:\n" + str(register()) + "\n")
            elif w == "view all":
                print(view()+ "\n")
            elif w == "change parameter":
                if len(registered_devices) != 0:
                    name = int(input("existent devicenames: {}\nenter devicename you want to change \n> ".format(" ".join(str(list(registered_devices.keys()))))))
                    print("enter value num. you want to change")
                    paramtype = get_available(registered_devices[name].visible_attr)
                    print("\n" + change_param(name, paramtype) + "\n")
                else:
                    print("no devices registered yet")
            elif w == "quit program":
                break
        except(ValueError, IndexError, AttributeError, KeyError):
            print('\033[91m' + "index can only be int and must belong to range of available choices\n" + '\033[0m')
    quit(0)


if __name__ == "__main__":
    main()
