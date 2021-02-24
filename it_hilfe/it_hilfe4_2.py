import csv


class Device:
    def __init__(self, name, user):
        self.name = name
        self.user = user
        self.OS = None

    def __str__(self):
        return f"{self.name}, {self.user}, {self.OS}, {self.__class__.__name__}"

    visible_attr = ["user", "OS"]


class WindowsWorkStation(Device):
    expected_OS = ["Win10", "Win7"]


class WindowsLapTop(Device):
    def __init__(self, name, user):
        super().__init__(name, user)
        self.bitlockkey = 1234
        self.largerBattery = True
        self.upgradedCPU = False
    def __str__(self):
        return f"{self.name}, {self.user}, {self.OS}, {self.__class__.__name__}, largerbattery: {self.largerBattery}, upgradedCPU: {self.upgradedCPU}"
    expected_OS = ["Win10", "Win7"]
    visible_attr = ["user", "OS", "largerBattery", "upgradedCPU"]


class Macbook(Device):
    def __init__(self, name, user):
        super().__init__(name, user)
        self.OS = "MacOS"

    expected_OS = ["MacOS"]


registered_devices = {}
options = ["search by username", "register new", "view all", "change parameter", "delete particular user/device",
           "clear all", "just save",
           "quit program"]  # to extend functionality add new menue options here
valid_devices = [WindowsLapTop, WindowsWorkStation, Macbook]  # to add more classes add class here


def get_available(optionslist):
    a = int(input("\n".join(
        ["{}:{}".format(i + 1, x) if type(x) == str else "{}:{}".format(i + 1, x.__name__) for i, x in
         enumerate(optionslist)]) + "\n>"))
    if a != 0 and a <= len(optionslist):
        return optionslist[a - 1]
    else:
        raise IndexError


def view():
    print('\n\033[92m' + "device name, username, Os, device type, [notes]" + '\033[0m')
    return [x for x in registered_devices.values()] or ["None"]


def register():
    newdevicetype = get_available(valid_devices)
    newdevicename = input("enter devicename \nalready taken: {}\n>".format(
        ', '.join([str(x) for x in list(registered_devices.keys())]) or "None"))
    new = newdevicetype(newdevicename, input("enter username \n>"))
    if newdevicename not in registered_devices.keys():
        # print(type(list(registered_devices.keys())), type(newdevicename))
        if len(newdevicetype.expected_OS) > 1:
            new.OS = get_available(newdevicetype.expected_OS)
        registered_devices[new.name] = new
        return new


def search(username):
    return [x for x in registered_devices.values() if x.user == username]


def change_param(devicename, paramtype):
    a = registered_devices.get(int(devicename))
    print('\033[92m' + "current value:" + '\033[0m', getattr(a, paramtype))
    if paramtype == "OS":
        setattr(a, paramtype, get_available(a.expected_OS))
    else:
        setattr(a, paramtype, input("enter new parameter\n>"))
    return a


def delete(all):
    if not all:
        print('\033[92m' + "delete all related to:" + '\033[0m')
        paramtype = get_available(["username", "devicename"])
    print('\033[91m' + "\nsure about clearing stored data?" + '\033[0m')
    if get_available(["yes", "no"]) == "yes":
        if all:
            with open("../data/names.csv", "r+") as csvfile:
                csvfile.truncate()
                registered_devices.clear()
                print('\033[92m' + "\neverything cleared\n" + '\033[0m')

        else:
            if paramtype == "username":
                if len([registered_devices.pop(int(list(registered_devices.values()).index(x)+1)) for x in search(input('\033[92m' + "enter name you wish to search for" + '\033[0m' + "\n>"))]) == 0:
                    raise KeyError
                else:
                    print('\033[92m' + "\ncleared" + '\033[0m')


            elif paramtype == "devicename":
                registered_devices.pop(int(input('\033[92m' + f"\nenter devicename \navailable: {', '.join([str(x) for x in list(registered_devices.keys())])}" + '\033[0m' + "\n>")))
                print('\033[92m' + "\ncleared" + '\033[0m')


def save():
    with open('../data/names.csv', 'w', newline='') as csvfile:
        fieldnames = ["________name", "username", "OS", "device_type", "notes", ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for x in registered_devices:
            writer.writerow(
                {"________name": registered_devices.get(x).name,
                 "username": getattr(registered_devices.get(x), registered_devices.get(x).visible_attr[0]),
                 "OS": getattr(registered_devices.get(x), registered_devices.get(x).visible_attr[1]),
                 "device_type": registered_devices.get(x).__class__.__name__,
                 "notes": [(a, getattr(registered_devices.get(x), a)) for a in registered_devices.get(x).visible_attr[2:]]
                 })
        csvfile.seek(0)
        csvfile.write("sep = ,\n")
        print('\033[92m' + "\nsaved" + '\033[0m')
        return True


def update():
    try:
        with open("../data/names.csv", "r+") as csvfile:  # update registered_devices
            data = csvfile.readlines()
            if data[0] == "sep = ,\n":  #overwrite sep = \n
                csvfile.seek(0)
                for x in data[1:]:
                    csvfile.write(x)

        with open("../data/names.csv", "r+") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                new = [x for x in valid_devices if x.__name__ == row["device_type"]].pop(0)(row["name"], row["username"])
                new.OS = row["OS"]
                registered_devices[row["name"]] = new
    except IndexError:
        pass  #nothing to update


def main():
    saved = None

    while True:
        try:
            w = get_available(options)
            if len(registered_devices) >= 0:

                if w == "register new":
                    a = register()
                    if a is None:
                        print('\033[91m' + "already taken dev name\n" + '\033[0m')
                    else:
                        print("\n" + str(a) + "\n")
                elif w == "quit program":
                    if not saved:
                        save()
                    print("ended program")
                    break
                    # quit(1)

            if len(registered_devices) != 0:
                if w == "search by username":
                    print("\n"+"".join([str(x) for x in search(input("enter username\n>"))]), "\n" or '\033[91m' + "no match found\n" + '\033[0m')
                elif w == "view all":
                    print("\n".join([str(x) for x in view()]), "\n" )
                elif w == "change parameter":
                    name = input("existent devicenames: {}\nenter devicename you want to change \n> ".format(", ".join([str(x) for x in list(registered_devices.keys())])))
                    paramtype = get_available(registered_devices[int(name)].visible_attr)
                    print('\033[92m' + "\nchanged:\n" + '\033[0m' + str(change_param(name, paramtype)) + "\n")
                elif w == "delete particular user/device":
                    delete(False)
                elif w == "clear all":
                    delete(True)
                elif w == "just save":
                    saved = save()
            else:
                print('\033[91m' + "no device registered yet\n" + '\033[0m')

        except(IndexError, AttributeError):
            print('\033[91m' + "\nindex must belong to range of available choices\n" + '\033[0m')
        except ValueError:
            print('\033[91m' + "\nindex can only be int\n" + '\033[0m')
        except KeyError:
            print('\033[91m' + "\nnot found\n" + '\033[0m')



if __name__ == "__main__":
    try:
        update()
        print('\033[92m' + "welcome to IT service" + '\033[0m')
        main()
    except PermissionError:
        print(
            '\033[91m' + "\ncsv file already opened in another program => close csv file, restart program \n" + '\033[0m')
