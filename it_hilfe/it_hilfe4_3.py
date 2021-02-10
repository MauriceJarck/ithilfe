from tkinter import scrolledtext, messagebox, filedialog
import tkinter as tk
import tkinter.ttk as ttk
import csv


class EmptyFieldError(Exception):
    pass


class AlreadyTakenNameError(Exception):
    pass


class NotSameLengthError(Exception):
    pass


class Device:
    def __init__(self, name, user, OS, comment):
        self.name = name
        self.user = user
        self.OS = OS
        self.comment = comment
        # self.datetime = datetime.today()

    def __str__(self):
        return f"{self.name}, {self.user}, {self.OS}, {self.__class__.__name__}, {self.comment}"

    visible_attr = ["user", "OS", "command"]


class WindowsWorkStation(Device):
    expected_OS = ["Win10", "Win7"]  # extend for more OS options/types


class WindowsLapTop(Device):
    def __init__(self, name, user, OS, comment):
        super().__init__(name, user, OS, comment)
        self.bitlockkey = 1234
        self.largerBattery = True
        self.upgradedCPU = False

    def __str__(self):
        return f"{self.name}, {self.user}, {self.OS}, {self.__class__.__name__}, largerbattery: {self.largerBattery}, upgradedCPU: {self.upgradedCPU}"

    expected_OS = ["Win10", "Win7"]  # extend for more OS options/types
    visible_attr = ["user", "OS", "largerBattery", "upgradedCPU", "comment"]


class Macbook(Device):

    expected_OS = ["MacOS"]  # extend for more OS options/types

class smartphone(Device):
    expected_OS = ["android", "IOs"]


reverse = None
toprocessdata = []
onscreen = {"entry": [], "liBo": [], "radio": [], "textbox": []}
registered_devices = {}
options = ["search by username", "register new", "view all", "change parameter", "quit program"]  # to extend str rep of new menue functionality add here
valid_devices = [WindowsLapTop, WindowsWorkStation, Macbook, smartphone]  # to add more classes add class here


class Main(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        # content setup
        self.btregister = tk.Button(root, text="Register", command=lambda: self.register(None)).grid(row=0, column=0)
        self.btsearch = tk.Button(root, text="Search", command=lambda: self.search(None)).grid(row=1, column=0)
        self.btchange_param = tk.Button(root, text="Change", command=lambda: self.change_param(None, True)).grid(row=2, column=0)
        self.btdelete = tk.Button(root, text="Delete selected", command=lambda: self.delete(False)).grid(row=3, column=0)
        self.columns = ('dev name', 'username', 'OS', 'type', 'comment')
        self.treeview = ttk.Treeview(root, height=25, columns=self.columns)

        # Specify attributes of the columns
        self.treeview.column('#0', stretch=tk.YES)
        self.treeview.column('#1', stretch=tk.YES)
        self.treeview.column('#2', stretch=tk.YES)
        self.treeview.column('#3', stretch=tk.YES)
        self.treeview.column('#4', stretch=tk.YES)
        self.treeview.column('#5', stretch=tk.YES)

        self.treeview.grid(row=7, column=1, columnspan=1, sticky='nsew')

        self.id = 0
        self.iid = 0

        # Set the heading

        self.treeview.heading('#0', text='no.')
        self.treeview.heading('#1', text='dev name')
        self.treeview.heading('#2', text='username')
        self.treeview.heading('#3', text='OS')
        self.treeview.heading('#4', text='type')
        self.treeview.heading('#5', text='comment')

        self.treeview.heading(column="#1", command=lambda: self.sort(1))
        self.treeview.heading(column="#2", command=lambda: self.sort(2))
        self.treeview.heading(column="#3", command=lambda: self.sort(3))
        self.treeview.heading(column="#4", command=lambda: self.sort(4))
        self.treeview.heading(column="#5", command=lambda: self.sort(5))

        verscrlbar = ttk.Scrollbar(root, orient="vertical", command=self.treeview.yview)
        verscrlbar.grid(row=7, column=1, sticky="nes")
        self.treeview.configure(yscrollcommand=verscrlbar.set)
        self.entrycount = tk.Label(root, text=f"currently {self.id} entrys")
        self.entrycount.grid(row=8, column=1)

        # menu row setup
        menu = tk.Menu(self)
        self.master.config(menu=menu)
        fileMenu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="save", command=lambda: self.save(False), accelerator="Ctrl+s")
        fileMenu.add_command(label="save as excel csv", command=lambda: self.save(True))
        fileMenu.add_command(label="Delete all", command=lambda: self.delete(True))
        fileMenu.add_command(label="new database", command=lambda: self.newFile(None))
        fileMenu.add_command(label="open database", command=self.browseFiles, accelerator="Crtl+o")
        fileMenu.add_command(label="Exit", command=lambda: self.destroy)

        commandsMenu = tk.Menu(self)
        menu.add_cascade(label="Edit", menu=commandsMenu)
        commandsMenu.add_command(label="register new", command=lambda: self.register(None), accelerator="Ctrl+n")
        commandsMenu.add_command(label="find", command=lambda: self.search(None), accelerator="Ctrl+f")
        commandsMenu.add_command(label="change parameter", command=lambda: self.change_param(None, True), accelerator="Ctrl+d")

        #shortcut binds
        self.bind_all("<Control-n>", lambda x: self.register(None))
        self.bind_all("<Control-f>", lambda x: self.search(None))
        self.bind_all("<Control-d>", lambda x: self.change_param(None, True))
        self.bind_all("<Control-s>", lambda x: self.save(False))
        self.bind_all("<Control-o>", lambda x: self.browseFiles)
        self.bind_all("<Double-Button-1>", lambda x: self.change_param(None, False))


    def validate_data(self, data, command):
        try:
            self.t.Lmessage.config(fg="red")
            for x in data.values():
                if  command == "register":
                    devname = data.get("entry")[0][1].get().split("-")
                    if onscreen.get("entry")[0][1].get() in registered_devices.keys() :
                        raise AlreadyTakenNameError
                    if len([x for x in range(int(devname[0]), int(devname[1])+1)]) != len(data.get("entry")[1][1].get().split(",")):
                        raise NotSameLengthError
                    if len([int(x) for x in range(int(devname[0]), int(devname[1])+1)]) < 0:
                        raise Exception
                elif command == "change_param" and self.t.var.get() == "OS" and data.get("entry")[0][1].get() not in registered_devices.get(data.get("liBo")[0][1].get("anchor")).expected_OS  :
                    raise AttributeError
                for a in x:
                    if  isinstance(a[1], tk.Entry) and a[1].get() == '':
                        raise EmptyFieldError
                    elif isinstance(a[1], tk.Listbox) and a[1].get("anchor") == '':
                        raise EmptyFieldError
                    elif isinstance(a[1], tk.Radiobutton) and self.t.var.get() == "":
                        raise EmptyFieldError
        except NotSameLengthError:
            self.t.Lmessage.config(text="if using multi create range devname == len usernames")
        except EmptyFieldError:
            self.t.Lmessage.config(text="fill all fields")
        except AlreadyTakenNameError:
            self.t.Lmessage.config(text="already taken dev name")
        except AttributeError:
            self.t.Lmessage.config(text="not available OS type")
        except ValueError:
            self.t.Lmessage.config(text="wrong input type")
        except tk.TclError:
            print("!")
        else:
            if command != "change_param":
                getattr(Main, command)(ithilfe, data)
            else:
                self.change_param(data, None)

    def register(self, data):
        if data is None:
            self.t = SubWindow("register", ["enter dev name", "enter username"], ["enter dev type", "enter os"], valid_devices, ["entry", "liBo", "radio", "textbox"], True)
        else:
            try:
                edevname = data.get("entry")[0][1].get().split("-")
                eusername = data.get("entry")[1][1].get().split(",")
                lidevtype = data.get("liBo")[0][1].get("active")
                lios = self.t.var.get()
                comment = data.get("textbox")[0][1].get("1.0", "end-1c")
                gendevnames = [x for x in range(int(edevname[0]), int(edevname[1])+1)]
                print(gendevnames, eusername)
                for x in gendevnames:
                    # print(gendevnames[x], eusername[x])
                    registered_devices[gendevnames[x-1]] = [x for x in valid_devices if x.__name__ == lidevtype].pop(0)(gendevnames[x-1], eusername[x-1], lios, comment)

                self.t.Lmessage.config(text="")
            except tk.TclError:
                pass

            else:
                self.save(False)
                self.update()
                self.t.destroy()

    def search(self, data):
        try:
            if data is None:
                self.t = SubWindow("search", ["enter username"], [], [], ["entry"], False)
            else:
                self.t.Geometry(500, 300)
                self.t.Lmessage.config(fg="black")
                self.t.Lmessage.config(text=",\n ".join([str(x) for x in registered_devices.values() if x.user == data.get("entry")[0][1].get()] or ["nothing found"]))
        except tk.TclError:
            pass

    def change_param(self, data, state):
        if data is None:
            if state:
                self.t = SubWindow("change_param", ["enter new value"], ["choose device", "choose param"], list(registered_devices.keys()), ["liBo", "radio", "entry"], False)
            else:
                self.t = SubWindow("change_param", ["enter new value"], ["chosen device", "choose param"], [str(self.treeview.item(self.treeview.focus()).get("values")[0])], ["liBo", "radio", "entry"], False)

        else:
            devicename = data.get("liBo")[0][1].get("anchor")
            paramtype = self.t.var.get()
            newparam = data.get("entry")[0][1].get()
            a = registered_devices.get(devicename)
            # print("current val:", getattr(a, paramtype))
            setattr(a, paramtype, newparam)
            self.save(False)
            self.update()
            self.t.destroy()
            [onscreen[x].clear() for x in list(onscreen.keys())]

    def browseFiles(self):
        try:
            self.filename = filedialog.askopenfilename(initialdir=r"C:\Users\maurice.jarck\Documents\Projects\it_hilfe\data", title="open database",  filetypes=(("csv files", "*.csv*"), ("all files", "*.*")))
            registered_devices.clear()
            self.update()
        except FileNotFoundError:
            print("File not found")

    def newFile(self, data):
        if data is None:
            self.t = SubWindow("newFile", ["enter new filename"], [], [], ["entry"], False)
        else:
            filename = data.get("entry")[0][1].get()
            newfilepath = filedialog.askdirectory(initialdir="/", title="select directory for new file")

            self.filename = f"{newfilepath}/{filename}.csv"

            self.treeview.delete(*self.treeview.get_children())
            registered_devices.clear()

            with open(f"{self.filename}", 'w', newline='') as csvfile:
                fieldnames = ["name", "username", "OS", "device_type", "extras", "comment"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

            self.update()
            self.t.destroy()

    def save(self, excel):
        with open(f"{self.filename}", 'w', newline='') as csvfile:
            fieldnames = ["name", "username", "OS", "device_type", "extras", "comment" ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for x in registered_devices:
                writer.writerow(
                    {"name": registered_devices.get(x).name,
                     "username": getattr(registered_devices.get(x), registered_devices.get(x).visible_attr[0]),
                     "OS": getattr(registered_devices.get(x), registered_devices.get(x).visible_attr[1]),
                     "device_type": registered_devices.get(x).__class__.__name__,
                     "extras": [(a, getattr(registered_devices.get(x), a)) for a in registered_devices.get(x).visible_attr[2:-1]],
                     "comment": registered_devices.get(x).comment
                     })
            if excel == True:
                csvfile.seek(0)
                csvfile.write("sep = ,\n")

    def update(self):
        # try:
            with open(f"{self.filename}", "r+") as csvfile:  # update registered_devices
                data = csvfile.readlines()
                if data[0] == "sep = ,\n":  # overwrite sep = \n
                    csvfile.seek(0)
                    for x in data[1:]:
                        csvfile.write(x)

            self.treeview.delete(*self.treeview.get_children())

            with open(f"{self.filename}", "r+") as csvfile:
                reader = csv.DictReader(csvfile)
                self.id = 0
                for row in reader:
                    new = [x for x in valid_devices if x.__name__ == row["device_type"]].pop(0)(row["name"], row["username"], row["OS"], row["comment"])
                    registered_devices[row["name"]] = new
                    self.treeview.insert('', 'end',  iid=self.iid, text=str(self.id) ,values=(row["name"], row["username"], row["OS"], row["device_type"], row["comment"]))
                    self.iid = self.iid + 1
                    self.id = self.id + 1
                    self.entrycount.config(text=f"currently {self.id} entrys")

    # except IndexError:
        #     pass  # nothing to update

    def delete(self, all):

        if not all:
            pass
            # row_id = int(self.treeview.focus())
            # selc_dev_name = self.treeview.item(row_id).get("values")[0]
            # print(selc_dev_name)
            # with open(f"{self.filename}", "r+") as csvfile:
            #     reader = csvfile.readlines()
            #     i = 0
            #     for row in reader:
            #         if row.split(",")[0] == (str(selc_dev_name)):
            #             tokeep = reader[reader.index(row)+1:]
            #             for a in row:
            #                 if repr(a) != "\n":
            #                     csvfile.write(" ")
            #                 csvfile.write("\n")
            #             csvfile.seek(i)
            #             for x in tokeep:
            #                 csvfile.write(x)
            #
            #         i += len(row)


            # self.treeview.delete(row_id)




        else:
            MsgBox = tk.messagebox.askquestion('delete everting', 'Are you sure you want to delete everything', icon='warning')
            if MsgBox == 'yes':
                with open(f"{self.filename}", "r+") as csvfile:
                    csvfile.truncate()
                    registered_devices.clear()
                    self.treeview.delete(*self.treeview.get_children())
                    fieldnames = ["name", "username", "OS", "device_type", "extras", "comment"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()

        self.update()

    def sort(self, col):

        a = [(self.treeview.item(x).get("values")[col-1], self.treeview.index(x)) for x in list(self.treeview.get_children())]
        b = sorted(a, key=lambda x: (isinstance(x[0], str), x[0].lower() if isinstance(x[0], str) else x[0]))
        for z in b:
            self.treeview.move(z[1], self.treeview.parent(z[1]), b.index(z))



class SubWindow(tk.Frame):

    def __init__(self, command, entryLabelList, liBoLabelList, liBoValList, order, textbox):
        super().__init__()

        self.command = command
        self.order = order
        self.entryLabelList = entryLabelList
        self.liBoLabelList = liBoLabelList
        self.textbox = textbox

        self.t = tk.Toplevel(self)
        self.t.geometry(f"300x400+{int(root.winfo_screenwidth() / 2 - 150)}+{int(root.winfo_screenheight() / 2) - 150}")
        self.t.iconbitmap(r"../data/favicon.ico")

        self.t.wm_title(command)
        self.t.focus()

        [onscreen[x].clear() for x in list(onscreen.keys())]

        try:
            if self.textbox == True:
                Tlabel = tk.Label(self.t, text="enter comment")
                Tbox = tk.scrolledtext.ScrolledText(self.t, width=12, height=5)
                onscreen.get("textbox").append([Tlabel, Tbox])

            if len(self.entryLabelList) != 0:
                for x in self.entryLabelList:
                    Elabel = tk.Label(self.t, text=x)
                    Entry = tk.Entry(self.t)
                    Entry.focus()
                    onscreen.get("entry").append([Elabel, Entry])

            if len(self.liBoLabelList) != 0:
                liBolabel = tk.Label(self.t,  text=self.liBoLabelList[0])

                self.liBo = tk.Listbox(self.t, selectmode="single", height=4)
                scrollbar = tk.Scrollbar(self.t, orient="vertical")

                self.liBo.config(yscrollcommand=scrollbar.set)
                scrollbar.config(command=self.liBo.yview)

                for x in liBoValList:
                    if isinstance(x, str):
                        self.liBo.insert("end", x)
                    else:
                        self.liBo.insert("end", x.__name__)

                onscreen.get("liBo").append([liBolabel, self.liBo,  scrollbar])

                if command == "register" or "change":
                    self.liBo.bind("<<ListboxSelect>>", self.radioButton)

            line = 0
            for x in self.order:
                for y in onscreen.get(x):
                    for a in y:
                        a.grid(row=line, column=y.index(a))
                    line += 1

        except IndexError:
            print("!!!")

        tk.Button(self.t, text="cancel", command=self.t.destroy).grid(row=13, column=0)
        tk.Button(self.t, text="enter", command=lambda: self.getall(None)).grid(row=13, column=1)
        self.bind_all("<Return>", self.getall)
        self.bind_all("<Escape>", lambda x: self.t.destroy())



        self.Lmessage = tk.Label(self.t, text="", fg="red")
        self.Lmessage.grid(row=12, column=1)


    def getall(self, evt):
        Main.validate_data(ithilfe, onscreen, self.command)

    def radioButton(self, evt):
        # [x[0].destroy() for x in onscreen.get("radio")]
        # onscreen.get("radio").clear()

        self.var = tk.StringVar()
        i = 0

        try:
            li = getattr(globals().get(self.liBo.get("anchor")), "expected_OS")
        except AttributeError:
            li = registered_devices.get(self.liBo.get("anchor")).visible_attr

        for a in li:
            Lradio = tk.Label(self.t, text=self.liBoLabelList[1]).grid(row=6, column=0)
            radio = tk.Radiobutton(self.t, text=a, variable=self.var, value=a)
            radio.grid(row=6 + i, column=1)
            onscreen.get("radio").append([Lradio, radio])
            i += 1


    def Geometry(self, width, height):

        self.t.geometry(f"{width}x{height}+{int(root.winfo_screenwidth() / 2 - width/2)}+{int(root.winfo_screenheight() / 2 - height/2)}")


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
    root.iconbitmap(r"../data/favicon.ico")
    root.title("elp")
    ithilfe = Main(root)
    ithilfe.focus()

    ithilfe.browseFiles()
    root.mainloop()
