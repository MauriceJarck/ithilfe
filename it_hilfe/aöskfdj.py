# import csv
# import random
# from string import ascii_lowercase
#
# os = ["win10", "win7", "macos", "linux"]
# devtype = ["WindowsLapTop", "WindowsWorkStation", "Macbook", "smartphone"]  # to add more classes add class here
#
# with open("../data/new.csv", 'w', newline='') as csvfile:
#     fieldnames = ["name", "username", "OS", "device_type", "extras", "comment"]
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     for x in range(1000):
#         writer.writerow(
#             {"name": x,
#              "username": "".join(random.choice(ascii_lowercase) for x in range(random.randint(5,10))),
#              "OS": os[random.randint(0, len(os)-1)],
#              "device_type": devtype[random.randint(0, len(devtype)-1)],
#              "extras": "extra",
#              "comment": "comment"
#              })
#     csvfile.close()

# with open("../data/registered_devices.csv", 'r+', newline='') as csvfile:
#     reader = csvfile.readlines()
#     i = 0
#     for x in reader:
#         print(x)
#         if x.split(",")[0] == "12":
#             csvfile.seek(i)
#             for a in x:
#                 if repr(a) != "\n":
#                     csvfile.write(" ")
#                 csvfile.write("\n")
#             csvfile.seek(i)
#             csvfile.write("hallo")
#         i += len(x)
#
#     print(i)
def func():
    while True:
        print("hallo")
        return 1

func()