class AlreadyTakenNameError(Exception):
    pass

class NothingRegisteredError(Exception):
    pass

class Device:
    def __init__(self, name, user):
        self.name = name
        self.user = user
        self.OS = None

    def __str__(self):
        return f"{self.name}, {self.user}, {self.OS}, {self.__class__.__name__}"

    visible_attr = ["user", "OS"]  # Attributes available to change for user


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
    visible_attr = ["user", "OS", "largerBattery", "upgradedCPU"]  # Attributes available to change for user


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

    if a > len(optionslist) or a <= 0:
        raise IndexError
    else:
        return optionslist[a - 1]

def view():
    print("\nname, user, OS, devtype, notes")
    return [x for x in registered_devices.values()]


def register(newdevicename, newdevicetype, os, username):
    new = newdevicetype(newdevicename, username)
    new.OS = os
    registered_devices[new.name] = new
    return new


def search(username):
    return [x for x in registered_devices.values() if x.user == username]


def change_param(devicename, paramtype, newval):
    a = registered_devices.get(devicename)
    print("current val:", getattr(a, paramtype))
    setattr(a, paramtype, newval)
    return a

def main():  # to extend menu functionality add here
    while True:
        count = 0
        while count < 3:  # num of tries until you'll get thrown back to options menu
            try:
                if count == 0:
                    w = get_available(options)

                if len(registered_devices) >= 0:
                    if w == "register new":
                        if not locals().get("newdevicetype"):
                            newdevicetype = get_available(valid_devices)
                        if not locals().get("OS"):
                            OS = get_available(newdevicetype.expected_OS)
                        if not locals().get("newdevicename"):
                            newdevicename = input("enter devicename \nalready taken: {}\n>".format(', '.join([str(x) for x in list(registered_devices.keys())]) or "None"))
                            if newdevicename in registered_devices.keys() or newdevicename == "":
                                del newdevicename
                                raise AlreadyTakenNameError
                        if not locals().get("user"):
                            user = input("enter username \n>")
                            if user == "":
                                raise ValueError
                        print("\n" + str(register(newdevicename, newdevicetype, OS, user)) + "\n")
                        break

                    elif w == "quit program":
                        return "end"

                if len(registered_devices) != 0:
                    if w == "search by username":
                        a = search(input(f"enter username to search for, available: {', '.join([str(x) for x in set([x.user for x in list(registered_devices.values())])])}\n>"))
                        if len(a) != 0:
                            print("\n"+"\n".join([str(x) for x in a]))
                        else:
                            count += 1
                            raise KeyError

                    elif w == "view all":
                        print("\n".join([str(x) for x in view()]))

                    elif w == "change parameter":
                        if not locals().get("devicename"):
                            devicename = input("existent devicenames: {}\nenter devicename you want to change \n> ".format(", ".join([str(x) for x in list(registered_devices.keys())])))
                        if devicename not in registered_devices.keys():
                            del devicename
                            raise KeyError
                        if not locals().get("paramtype"):
                            paramtype = get_available(registered_devices[devicename].visible_attr)

                        if paramtype == "OS":
                            os = get_available(registered_devices.get(devicename).expected_OS)
                        else:
                            os = input("enter new parameter\n>")

                        print("\n" + str(change_param(devicename, paramtype, os)) + "\n")
                        break
                else:
                    raise NothingRegisteredError

            except NothingRegisteredError:
                print('\033[91m' + "no device registered yet\n" + '\033[0m')
            except ValueError:
                print('\033[91m' + "\nindex can only be int, retry:\n" + '\033[0m')
                count += 1
            except IndexError:
                print('\033[91m' + "\nindex must belong to range of available choices, retry:\n" + '\033[0m')
                count += 1
            except AlreadyTakenNameError:
                print('\033[91m' + "already taken dev name\n" + '\033[0m')
                count += 1
            except KeyError:
                print('\033[91m' + "nothing found\n" + '\033[0m')
                count += 1
            except UnboundLocalError:
                break

        try:
            if w == "register new":
                del newdevicename, newdevicetype, OS, user
            elif w == "change parameter":
                del devicename, paramtype
        except UnboundLocalError:
            print("del problem")

if __name__ == "__main__":
    print("welcome to IT service\ntype no. of what you wish to do\n")
    main()