class Device:
    def __init__(self, name, user):
        self.name = name
        self.user = user
        self.OS = None

    def __str__(self):
        return f"device name: {self.name}, username: {self.user}, OS: {self.OS}, devtype: {self.__class__.__name__} "


class WindowsWorkStation(Device):
    expected_OS = ["Win10", "Win7"]


class WindowsLapTop(Device):
    def __init__(self, name, user):
        super().__init__(name, user)
        self.bitlockkey = 1234
        self.largerBattery = True
        self.upgradedCPU = False

    def __str__(self):
        return f"device name: {self.name}, username: {self.user}, OS: {self.OS}, largerBattery: {self.largerBattery}, upgradedCPU: {self.upgradedCPU}, devtype: {self.__class__.__name__},"

    expected_OS = ["Win10", "Win7"]


class Macbook(Device):
    def __init__(self, name, user):
        super().__init__(name, user)
        self.OS = "MacOS"
    expected_OS = ["MacOS"]


registered_devices = {}
options = ["search by username", "register new", "view all", "change parameter", "quit program"]  # to extend functionality add new menu options here
attributes = ["name", "user", "OS", "upgradedCPU", "largerBattery"]  # to extend functionality add new attributes here
valid_devices = [WindowsLapTop, WindowsWorkStation, Macbook]  # to add more classes add class here


def get_available(optionslist):
    a = int(input("\n".join("{}:{}".format(i + 1, x) for i, x in enumerate(optionslist)) + "\n>"))
    if a != 0 and a <= len(optionslist):
        return a
    else:
        raise IndexError


def view():
    if len(registered_devices) != 0:
        for x in registered_devices.keys():
            return str(registered_devices.get(x))+"\n"
    else:
        return "no device registered yet\n"


def register():
    newdevicetype = get_available([x.__name__ for x in valid_devices]) - 1
    newdevicename = int(input("enter devicename as int \nalready taken:{}\n>".format(' '.join(str(list(registered_devices.keys()))))))
    new = valid_devices[newdevicetype](newdevicename, input("enter username \n>"))
    if newdevicename not in registered_devices.keys():
        if len(valid_devices[newdevicetype].expected_OS) > 1 :  # extend for more OS options/types
            new.OS = valid_devices[newdevicetype].expected_OS[get_available(valid_devices[newdevicetype].expected_OS) - 1]
        registered_devices[new.name] = new
        content = f"{newdevicetype}, {newdevicename}, {new.user}, {new.OS}"  # for testing purposes
    else:
        content = '\033[91m' + "already taken dev name\n" + '\033[0m'
    return content


def search(username):
    msg = []
    if len(registered_devices) == 0:
        msg = ["\nno devices registered yet\n"]
    else:
        if not [msg.append(f"match found: {registered_devices.get(x)}\n") for x in registered_devices.keys() if registered_devices.get(x).user == username]:
            msg = ["\nno match found\n"]
    return msg


def change_param(devicename, paramtype):
    for x in registered_devices:
        a = registered_devices.get(x)
        if a.name == devicename:
            if paramtype == 2: #OS
                newparam = a.expected_OS[get_available(a.expected_OS)-1]
            else:
                newparam = input("enter new parameter\n>")

            setattr(a, str(attributes[paramtype]), newparam)
            return a


def main():  # to extend menu functionality add here
    print("welcome to IT service\ntype no. of what you wish to do\n")
    while True:
        try:
            w = get_available(options)
            if w == 1:
                print("\n" + "".join(search(input("enter name you wish to search for\n>"))))
            if w == 2:
                print("\nentered:\n" + str(register()) + "\n")
            elif w == 3:
                print("".join(view()))
            elif w == 4:
                if len(registered_devices) != 0:
                    name = int(input("existent devicenames: {}\nenter devicename you want to change \n> ".format(" ".join(str(list(registered_devices.keys()))))))
                    print("enter value num. you want to change")
                    paramtype = get_available(str(registered_devices.get(name)).split(", ")[1:-1])  #provide only keys to choose which are also mentioned in class __str__ func
                    print(change_param(name, paramtype), "\n")
                else:
                    print("no devices registered yet")
            elif w == 5:
                break
        except(ValueError, IndexError):
            print('\033[91m' + "index can only be int and must belong to range of available choices\n" + '\033[0m')
    quit(0)


if __name__ == "__main__":
    main()
