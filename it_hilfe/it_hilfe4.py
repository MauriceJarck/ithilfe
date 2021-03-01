registered_devices = {}


class Device:
    def __init__(self, name, user):
        self.name = name
        self.user = user
        self.OS = None

    def __str__(self):
        return f"{self.name}, {self.user}, {self.OS}, {self.__class__.__name__}"


class WindowsWorkStation(Device):
    expected_OS = ["Win10", "Win7"]


class WindowsLapTop(Device):
    expected_OS = ["Win10", "Win7"]


class Macbook(Device):
    expected_OS = ["MacOS"]


def get_available(message, optionslist, notallowed=None, allowed=None):
    count, vals = 0, []
    for b in range(len(optionslist)):
        while count < 3:
            try:
                if len(optionslist[b]) != 0:
                    a = int(input(message[b] + "\n" + "\n".join(["{}:{}".format(i + 1, x) if isinstance(x, str) else "{}:{}".format(i + 1, getattr(x, '__name__', x)) for i, x in enumerate(optionslist[b])])+"\n>"))
                    if a > len(optionslist[b]) or a <= 0:
                        print("\ninvalid index\n")
                    else:
                        vals.append(optionslist[b][a - 1])
                        break
                else:
                    d = input(message[b]+"\n>")
                    if notallowed is not None and d in notallowed:
                        print("\nalready taken dev name\n")
                    elif allowed is not None and d not in allowed:
                        print("\nnot available or nothing registered\n")
                    elif d != "":
                        vals.append(d)
                        break
            except ValueError:
                print("\nwrong data type\n")
            count += 1
    return vals


def view():
    return [x for x in registered_devices.values()] or ["\nnothing registered yet\n"]


def register():
    a = get_available([f"enter devname\nalready taken: {','.join(list(registered_devices.keys())) or 'None'}", "enter devtype", "enter username"], [[], [WindowsLapTop, WindowsWorkStation, Macbook], []], notallowed=registered_devices.keys())
    b = get_available(["enter os"], [a[1].expected_OS])
    new = a[1](a[0], a[2])
    new.OS = b[0]
    registered_devices[new.name] = new
    return [new]


def search():
    a = input(f"enter username to search for\navailable: {','.join(list(registered_devices.keys())) or 'None'}\n>")
    return [x for x in registered_devices.values() if x.user == a] or ["\nnothing found\n"]


def change_param():
    devname = get_available([f"enter devname to change\navailable: {','.join(list(registered_devices.keys())) or 'None'}"], [[]], allowed=registered_devices.keys())
    c = registered_devices.get(devname[0])
    paramtype = get_available(["enter paramtype to change"], [["user", "OS"]])
    newval = get_available(["enter new val"], [c.expected_OS if paramtype[0] == "OS" else []])
    setattr(c, paramtype[0], newval[0])
    return [c]


def main():
    print("welcome to IT service\n")
    while True:
        try:
            print("".join(str(get_available(["enter no fitting to your needs"], [[search, register, view, change_param, quit]])[0]()[0]))+"\n")
        except IndexError:
            print("thats it\n")


if __name__ == '__main__':
    main()