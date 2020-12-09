import csv


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
options = ["search by username", "register new", "view all", "change parameter", "delete particular user/device", "clear all", "export registered devices as names.csv",  "quit program"]  # to extend functionality add new menue options here
attributes = ["name", "user", "OS", "upgradedCPU", "largerBattery"]  # to extend functionality add new attributes here
valid_OS = {"windows": ["windowsLapTop", "windowsWorkStation"], "apple": ["macbook"], "Linux": ["LinuxWorkstation, LinuxLapTop"]}       # to extend variety of OS add os type as key and vaild devices as value to dict

valid_devices = [windowsLapTop, windowsWorkStation, macbook]  # to add more classes add class here


def getAvailable(list):
    a = int(input("\n" + "\n".join("{}:{}".format(i + 1, x) for i, x in enumerate(list)) + "\n>"))
    if a != 0 and a <= len(list):
        return a
    else:
        raise IndexError


def view():
    print('\033[92m' + "device name, username, Os, device type, [notes]" + '\033[0m')

    for x in registered_devices.keys():
        print(registered_devices.get(x), ",", registered_devices.get(x).__class__.__name__, ",",
              [[y, registered_devices.get(x).__dict__.get(y)] for y in
               list(registered_devices.get(x).__dict__)[3:]])


def register():
    newDeviceType = getAvailable([x.__name__ for x in valid_devices]) - 1
    newDeviceName = int(input('\033[92m' + f"\nenter devicename as int \nalready taken:{''.join(str(list(registered_devices.keys())))}" + '\033[0m' + "\n>"))
    new = valid_devices[newDeviceType](newDeviceName, input('\033[92m' + "\nenter username " + '\033[0m' + "\n>"))
    if newDeviceName not in registered_devices.keys():
        if str(valid_devices[newDeviceType].__name__) in valid_OS.get("windows"):  # extend for more OS options/types
            new.OS = valid_devices[newDeviceType].expected_OS[
                getAvailable(valid_devices[newDeviceType].expected_OS) - 1]
        registered_devices[new.name] = new
    else:
        print('\033[91m' + "\nalready taken dev name\n" + '\033[0m')
    print('\033[92m' + "\nregistered\n" + '\033[0m')

    return [newDeviceType, newDeviceName, new.user, new.OS]  # for testing purposes


def search(username):
    a = [(x, registered_devices.get(x)) for x in registered_devices.keys() if
         registered_devices.get(x).user == username]
    if a:
        return a
    else:
        print('\033[91m' + "no match found\n" + '\033[0m')


def change_param(devicename, paramtype, newparam):
    for x in registered_devices:
        a = registered_devices.get(x)
        if a.name == devicename:
            setattr(a, str(attributes[paramtype]), newparam)
            print("\nchangend: ", a, "\n")
    return (f"{registered_devices.get(devicename).__dict__}")  # for testing purposes


def delete(all, paramtype):
    print('\033[91m' + "\nsure about clearing stored data?" + '\033[0m')
    if getAvailable(["yes", "no"]) == 1:
        if all:
            with open("../data/names.csv", "r+") as csvfile:
                csvfile.truncate()
                registered_devices.clear()
                print('\033[92m' + "\neverthing cleared" + '\033[0m')

        else:
            if paramtype == 1:
                [registered_devices.pop(x[0]) for x in search(input('\033[92m' + "enter name you wish to search for" + '\033[0m' + "\n>"))]

            elif paramtype == 2:
                registered_devices.pop(int(input('\033[92m' + f"\nenter devicename \navailable:{''.join(str(list(registered_devices.keys())))}" + '\033[0m' + "\n>")))
            print('\033[92m' + "\ncleared" + '\033[0m')


def save():
    with open('../data/names.csv', 'w', newline='') as csvfile:
        fieldnames = ["________name", "username", "OS", "device_type", "notes", ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for x in registered_devices:
            writer.writerow(
                {"________name": registered_devices.get(x).name, "username": registered_devices.get(x).user,
                 "OS": registered_devices.get(x).OS,
                 "device_type": registered_devices.get(x).__class__.__name__,
                 "notes": list(registered_devices.get(x).__dict__.keys())[3:]})
        csvfile.seek(0)
        csvfile.write("sep = ,\n")
        print('\033[92m' + "\nsaved" + '\033[0m')
        return True


def update():
    try:
        with open("../data/names.csv", "r+") as csvfile:  # update registered_devices
            data = csvfile.readlines()
            if data[0] == "sep = ,\n":
                csvfile.seek(0)
                for x in data[1:]:
                    csvfile.write(x)

        with open("../data/names.csv", "r+") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:

                new = [x for x in valid_devices if x.__name__ == row["device_type"]].pop(0)(int(row["name"]), row["username"])
                new.OS = row["OS"]
                registered_devices[int(row["name"])] = new
    except IndexError:
        pass


def main():
    saved = None

    while True:
        try:
            w = getAvailable(options)
            if len(registered_devices) >= 0:
                if w == 2:
                    register()
                elif w == 8:
                    if not saved:
                        save()
                    break

            if len(registered_devices) != 0:
                if w == 1:
                    [print("match found: ", str(x[1])) for x in search(input('\033[92m' + "enter name you wish to search for" + '\033[0m' + "\n>"))]
                elif w == 3:
                    view()
                elif w == 4:
                    name = int(input('\033[92m' + f"existent devicenames: {''.join(str(list(registered_devices.keys())))}\nenter devicename of device you want to change \n> " + '\033[0m'))
                    type = getAvailable(list(registered_devices.get(name).__dict__.keys())[1:])
                    change_param(name, type, input('\033[92m' + "enter new parameter > " + '\033[0m'))
                elif w == 5:
                    print('\033[92m' + "delete all realated to:" + '\033[0m')
                    delete(False, getAvailable(["username", "devicename"]))
                elif w == 6:
                    delete(True, None)
                elif w == 7:
                    saved = save()

            else:
                print('\033[91m' + "\nno devices registered yet\n" + '\033[0m')

        except (IndexError, AttributeError):
            print('\033[91m' + "\nindex must belong to range of available choices\n" + '\033[0m')
        except ValueError:
            print('\033[91m' + "\nindex can only be int\n" + '\033[0m')


if __name__ == "__main__":
    try:
        update()
        print('\033[92m' + "welcome to IT service" + '\033[0m')
        main()
    except PermissionError:
        print('\033[91m' + "\ncsv file already opened in another program => close csv file, restart program \n" + '\033[0m')

