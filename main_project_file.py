from pymongo import MongoClient
import tkinter as tk
from PIL import Image, ImageTk
import os

bg_color = "#717171"
fg_color = "#eeeeee"
font = ("Courier", 20)


window = tk.Tk()
window.title("Skyrim app")
window.geometry("800x600+50+50")
canva = tk.Canvas(window, width=800, height=600, background=bg_color)
canva.pack()
load = Image.open("logo.png")
render = ImageTk.PhotoImage(load)


def makeCanva():
    canva.create_image(380, 70, image=render)
    what_label = tk.Label(text="What are we looking for?", bg=bg_color, fg=fg_color, font=font)
    canva.create_window(400, 200, window=what_label)
    weapon = tk.Button(window, text="Weapons", command= lambda: make_choice_window("weapon"))
    canva.create_window(100, 300, window=weapon)
    armor = tk.Button(window, text="Armors", command= lambda: make_choice_window("armor"))
    canva.create_window(300, 300, window=armor)


def deleteCanva():
    canva.delete("all")


def makeImage():
    canva.create_image(380, 70, image=render)


makeCanva()


min_entry = tk.Entry(window)
max_entry = tk.Entry(window)
min_weight = tk.Entry(window)
max_weight = tk.Entry(window)
min_value = tk.Entry(window)
max_value = tk.Entry(window)
name_value = tk.Entry(window)


def get_statistic_entry_disable():
    if statistic_check.get() == 1:
        min_entry.config(state="disabled")
        max_entry.config(state="disabled")
    else:
        min_entry.config(state="normal")
        max_entry.config(state="normal")


def get_value_entry_disable():
    if value_check.get() == 1:
        min_value.config(state="disabled")
        max_value.config(state="disabled")
    else:
        min_value.config(state="normal")
        max_value.config(state="normal")


def get_weight_entry_disable():
    if weight_check.get() == 1:
        min_weight.config(state="disabled")
        max_weight.config(state="disabled")
    else:
        min_weight.config(state="normal")
        max_weight.config(state="normal")


def get_name_entry_disable():
    if name_check.get() == 1:
        name_value.config(state="disabled")
    else:
        name_value.config(state="normal")


statistic_check = tk.IntVar()
s_check = tk.Checkbutton(window, text="Don't care", variable=statistic_check, bg=bg_color,
                         command=get_statistic_entry_disable)
value_check = tk.IntVar()
v_check = tk.Checkbutton(window, text="Don't care", variable=value_check, bg=bg_color,
                         command=get_value_entry_disable)
weight_check = tk.IntVar()
w_check = tk.Checkbutton(window, text="Don't care", variable=weight_check, bg=bg_color,
                         command=get_weight_entry_disable)
name_check = tk.IntVar()
n_check = tk.Checkbutton(window, text="Don't care", variable=name_check, bg=bg_color,
                         command=get_name_entry_disable)



#functions


def searchFor():
    deleteCanva()
    makeImage()
    statistic = statistic_check.get()
    value = value_check.get()
    weight = weight_check.get()
    name = name_value.get()
    min_s, max_s, min_v, max_v, min_w, max_w = 0, 2000000, 0, 2000000, 0, 2000000
    flag = True

    if min_entry.get() == "":
        min_s = 0
        flag = False
    if max_entry.get() == "":
        max_s = 2000000
        flag = False
    if min_weight.get() == "":
        min_w = 0
        flag = False
    if max_weight.get() == "":
        max_w = 2000000
        flag = False
    if min_value.get() == "":
        min_v = 0
        flag = False
    if max_value.get() == "":
        max_v = 2000000
        flag = False
    if name_value.get() == "":
        print("Are you fucking kidding me?")
        flag = False

    if statistic == 0 and flag:
        min_s = int(min_entry.get())
        max_s = int(max_entry.get())
    if value == 0 and flag:
        min_v = int(min_value.get())
        max_v = int(max_value.get())
    if weight == 0 and flag:
        min_w = int(min_weight.get())
        max_w = int(max_weight.get())

    canva.create_image(380, 70, image=render)
    text = f"Your min is {min_s}, your max is {max_s}\n {min_v} {max_v}\n {min_w} {max_w}\n {name}"
    new_label = tk.Label(window, text=text, font=font, fg=fg_color, bg=bg_color)
    canva.create_window(380, 200, window=new_label)


def make_choice_window(what_kind_of):
    deleteCanva()
    if what_kind_of == "weapon":
        min_text = tk.Label(window, text="Min attack", bg=bg_color, fg=fg_color)
        max_text = tk.Label(window, text="Max attack", bg=bg_color, fg=fg_color)
    elif what_kind_of == "armor":
        min_text = tk.Label(window, text="Min armor", bg=bg_color, fg=fg_color)
        max_text = tk.Label(window, text="Max armor", bg=bg_color, fg=fg_color)

    x = 200
    y = 300
    z = 400
    makeImage()
    label = tk.Label(text="Weapons", bg=bg_color, fg=fg_color, font=font)
    min_v_text = tk.Label(window, text="Min value", bg=bg_color, fg=fg_color)
    max_v_text = tk.Label(window, text="Max value", bg=bg_color, fg=fg_color)
    min_w_text = tk.Label(window, text="Min weigth", bg=bg_color, fg=fg_color)
    max_w_text = tk.Label(window, text="Max weight", bg=bg_color, fg=fg_color)
    name_text = tk.Label(window, text="Maybe by name?", bg=bg_color, fg=fg_color)
    search_weapons = tk.Button(window, text="Search!", command=searchFor)
    canva.create_window(380, x - 40, window=label)


    #main
    canva.create_window(150, x, window=min_entry)
    canva.create_window(400, x, window=max_entry)
    canva.create_window(50, x, window=min_text)
    canva.create_window(300, x, window=max_text)
    canva.create_window(600, x, window=s_check)

    #value
    canva.create_window(150, y, window=min_value)
    canva.create_window(400, y, window=max_value)
    canva.create_window(50, y, window=min_v_text)
    canva.create_window(300, y, window=max_v_text)
    canva.create_window(600, y, window=v_check)

    #weight
    canva.create_window(150, z, window=min_weight)
    canva.create_window(400, z, window=max_weight)
    canva.create_window(50, z, window=min_w_text)
    canva.create_window(300, z, window=max_w_text)
    canva.create_window(600, z, window=w_check)

    #name
    canva.create_window(100, 500, window=name_text)
    canva.create_window(250, 500, window=name_value)
    canva.create_window(400, 500, window=n_check)

    #button Search
    canva.create_window(600, 500, window=search_weapons)


tk.mainloop()



'''Previous versions'''

''''#weapons
y=200
weapon_label = tk.Label(text="Weapons", bg=bg_color, fg=fg_color)
weapon_min_entry = tk.Entry(window)
weapon_max_entry = tk.Entry(window)
weapon_min_text = tk.Label(window, text="Min attack", bg=bg_color, fg=fg_color)
weapon_max_text = tk.Label(window, text="Max attack", bg=bg_color, fg=fg_color)
search_weapons = tk.Button(window, text="Search for weapon", command=searchForWeapon)
canva.create_window(380, y-40, window=weapon_label)
canva.create_window(150, y, window=weapon_min_entry)
canva.create_window(400, y, window=weapon_max_entry)
canva.create_window(50, y, window=weapon_min_text)
canva.create_window(300, y, window=weapon_max_text)
canva.create_window(600, y, window=search_weapons)


#armor
y = 280
armor_label = tk.Label(text="Armors", bg=bg_color, fg=fg_color)
armor_min_entry = tk.Entry(window)
armor_max_entry = tk.Entry(window)
armor_min_text = tk.Label(window, text="Min armor", bg=bg_color, fg=fg_color)
armor_max_text = tk.Label(window, text="Max armor", bg=bg_color, fg=fg_color)
search_armor = tk.Button(window, text="Search for armor", command=searchForArmor)
canva.create_window(380, y-40, window=armor_label)
canva.create_window(150, y, window=armor_min_entry)
canva.create_window(400, y, window=armor_max_entry)
canva.create_window(50, y, window=armor_min_text)
canva.create_window(300, y, window=armor_max_text)
canva.create_window(600, y, window=search_armor)


#weight
y = 360
weight_label = tk.Label(text="Weight", bg=bg_color, fg=fg_color)
weight_min_entry = tk.Entry(window)
weight_max_entry = tk.Entry(window)
weight_min_text = tk.Label(window, text="Min weight", bg=bg_color, fg=fg_color)
weight_max_text = tk.Label(window, text="Max weight", bg=bg_color, fg=fg_color)
search_weight = tk.Button(window, text="Search for weight", command=searchForWeight)
canva.create_window(380, y-40, window=weight_label)
canva.create_window(150, y, window=weight_min_entry)
canva.create_window(400, y, window=weight_max_entry)
canva.create_window(50, y, window=weight_min_text)
canva.create_window(300, y, window=weight_max_text)
canva.create_window(600, y, window=search_weight)'''

'''def searchForArmor():
    min = armor_min_entry.get()
    max = armor_max_entry.get()
    new_window = tk.Tk()
    text = f"Your min is {min}, your max is {max}"
    new_label = tk.Label(new_window, text=text).pack()


def searchForWeight():
    min = weight_min_entry.get()
    max = weight_max_entry.get()
    new_window = tk.Tk()
    text = f"Your min is {min}, your max is {max}"
    new_label = tk.Label(new_window, text=text).pack()'''
