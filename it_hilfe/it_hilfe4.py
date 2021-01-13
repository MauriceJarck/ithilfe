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
    try:
        if optionslist[len(optionslist)-1] != "help":
            optionslist = optionslist+["help"]
        a = int(input("\n".join(["{}:{}".format(i + 1, x) if type(x) == str else "{}:{}".format(i + 1, x.__name__) for i, x in enumerate(optionslist)])+"\n>"))
    except(ValueError):
        print('\033[91m' + "\nindex can only be int, retry:\n" + '\033[0m')
        return str(get_available(optionslist))
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    else:
        if a <= len(optionslist) and a >= 1:
            if optionslist[a-1] == "help":
                print("\nwhen running in terminal: press ctrl+c+return to exit current menue => back to  main\n")
                return get_available(optionslist)
            return optionslist[a-1]
        else:
            print('\033[91m' + "\nindex must belong to range of available choices, retry:\n" + '\033[0m')
            return get_available(optionslist)


def view():
    print("\nname, user, OS, devtype, notes")
    return [x for x in registered_devices.values()]


def register():
    newdevicename = input("enter devicename \nalready taken: {}\n>".format(', '.join([str(x) for x in list(registered_devices.keys())]) or "None"))
    if newdevicename not in registered_devices.keys():
        newdevicetype = get_available(valid_devices)
        new = newdevicetype(newdevicename, input("enter username \n>"))
        if len(newdevicetype.expected_OS) > 1:
            new.OS = get_available(newdevicetype.expected_OS)
        registered_devices[new.name] = new
        return new
    else:
        print('\033[91m' + "already taken dev name\n" + '\033[0m')
        return register()


def search(username):
    return [x for x in registered_devices.values() if x.user == username] or ['\033[91m' + "no match found\n" + '\033[0m']


def change_param():
    try:
        devicename = input("existent devicenames: {}\nenter devicename you want to change \n> ".format(", ".join([str(x) for x in list(registered_devices.keys())])))
        paramtype= get_available(registered_devices[devicename].visible_attr)
        a = registered_devices.get(devicename)
        print("current val:", getattr(a, paramtype))
        if paramtype == "OS":
            setattr(a, paramtype, get_available(a.expected_OS))
        else:
            setattr(a, paramtype, input("enter new parameter\n>"))
        return a
    except KeyError:
        print('\033[91m' + "\nnot found, retry:\n" + '\033[0m')
        return change_param()

def main():  # to extend menu functionality add here
    print("welcome to IT service\ntype no. of what you wish to do\n")
    while True:
        try:
            w = get_available(options)
            if len(registered_devices) >= 0:
                if w == "register new":
                    print("\n" + str(register()) + "\n")
                elif w == "quit program":
                    quit(0)

            if len(registered_devices) != 0:
                if w == "search by username":
                    print("\n"+"\n".join([str(x) for x in search(input(f"enter username to search for, available: {', '.join([str(x) for x in set([x.user for x in list(registered_devices.values())])])}\n>"))]))
                elif w == "view all":
                    print("\n".join([str(x) for x in view()]), "\n" or '\033[91m' + "no device registered yet\n" + '\033[0m')
                elif w == "change parameter":
                    print("\n" + str(change_param()) + "\n")
            else:
                print('\033[91m' + "no device registered yet\n" + '\033[0m')


        except(KeyboardInterrupt):
            print("\nback to the roots\n" )


if __name__ == "__main__":
    main()
