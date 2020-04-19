from pymongo import MongoClient
import tkinter as tk
from PIL import Image, ImageTk

client = MongoClient('mongodb+srv://dawid:dawid99@skyrimcluster-j4jje.gcp.mongodb.net/test')
db = client.skyrimDatabase

bg_color = "#717171"
fg_color = "#eeeeee"
font = ("Courier", 20)
small_font = ("Courier", 14)

labels = {
            "name": "Nazwa",
            "basic_attack": "Podstawowy atak",
            "weight": "Waga",
            "value": "Wartość",
            "is_unique": "Czy unikalny",
            "enchantments": "Efekty",
            "enchantment": "Efekty",
            "type": "Typ",
            "is_onehanded": "Czy jednoręczny",
            "basic_armor": "Podstawowa wartość zbroi",
            "is_light": "Czy lekka",
            "type_of_restoring": "Przywraca",
            "effect": "Efekt",
            "description": "Opis",
            "level": "Poziom",
            "mana_cost": "Koszt Many",
            "school_of_magic": "Szkoła"
        }


window = tk.Tk()
window.title("Skyrim app")
window.geometry("800x600+50+50")
canva = tk.Canvas(window, width=800, height=600, background=bg_color)
canva.pack()
load = Image.open("logo.png")
render = ImageTk.PhotoImage(load)


def makeCanva():
    deleteCanva()
    canva.create_image(380, 70, image=render)
    what_label = tk.Label(text="Czego dziś szukamy?", bg=bg_color, fg=fg_color, font=font)
    canva.create_window(400, 200, window=what_label)
    weapon = tk.Button(window, text="Weapons", command=lambda: make_choice_window("weapon"))
    canva.create_window(100, 300, window=weapon)
    armor = tk.Button(window, text="Armors", command=lambda: make_choice_window("armor"))
    canva.create_window(300, 300, window=armor)
    potion = tk.Button(window, text="Potions", command=lambda: make_potion_window())
    canva.create_window(500, 300, window=potion)
    book = tk.Button(window, text="Books", command=lambda: make_book_window())
    canva.create_window(700, 300, window=book)


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

potion_var = tk.StringVar(window)
spell_book_type = tk.StringVar(window)
level_book_type = tk.StringVar(window)


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


statistic_check = tk.IntVar()
s_check = tk.Checkbutton(window, text="Don't care", variable=statistic_check, bg=bg_color,
                         command=get_statistic_entry_disable)
value_check = tk.IntVar()
v_check = tk.Checkbutton(window, text="Don't care", variable=value_check, bg=bg_color,
                         command=get_value_entry_disable)
weight_check = tk.IntVar()
w_check = tk.Checkbutton(window, text="Don't care", variable=weight_check, bg=bg_color,
                         command=get_weight_entry_disable)



#functions

def findWeapon(min_s, max_s, min_v, max_v, min_w, max_w):
    return db.weapons.find({
        "basic_attack": {"$gt":min_s},
        "basic_attack": {"$lt":max_s},
        "value": {"$gt": min_v},
        "value": {"$lt": max_v},
        "weight": {"$gt": min_w},
        "weight": {"$lt": max_w},
    })

def findArmor(min_s, max_s, min_v, max_v, min_w, max_w):
    return db.armor.find({
        "basic_armor": {"$gt": min_s},
        "basic_armor": {"$lt": max_s},
        "value": {"$gt": min_v},
        "value": {"$lt": max_v},
        "weight": {"$gt": min_w},
        "weight": {"$lt": max_w},
    })


def showDetails(one_weapon):
    y_offset = 25
    offset_of_enchants = 0
    i = 0
    for idx, label in enumerate(one_weapon):
        if label != "_id" and label != "enchantments" and label != "enchantment":
            new_label = tk.Label(window, text="{}: ".format(labels[label]), font=small_font, fg=fg_color, bg=bg_color)
            new_label2 = tk.Label(window, text="{}".format(one_weapon[label]), font=small_font, fg=fg_color,
                                  bg=bg_color)
            canva.create_window(150, 180 + (idx + offset_of_enchants) * y_offset, window=new_label)
            canva.create_window(450, 180 + (idx + offset_of_enchants) * y_offset, window=new_label2)
        elif label == "enchantments" or label == "enchantment":
            new_label = tk.Label(window, text="{}: ".format(labels[label]), font=small_font, fg=fg_color,
                                 bg=bg_color)
            canva.create_window(150, 180 + (idx + offset_of_enchants) * y_offset, window=new_label)
            for i, enchant in enumerate(one_weapon[label]):
                offset_of_enchants = 1
                new_label2 = tk.Label(window, text="{}".format(enchant), font=small_font, fg=fg_color,
                                  bg=bg_color)
                canva.create_window(550, 180 + (idx + i + offset_of_enchants) * y_offset, window=new_label2)
            else:
                offset_of_enchants += i+1
                i+=1
            if i == 0:
                new_label2 = tk.Label(window, text="Brak", font=small_font, fg=fg_color,
                                      bg=bg_color)
                canva.create_window(450, 180 + (idx + i + offset_of_enchants) * y_offset, window=new_label2)


def show(what_kind_of, weapons, func):
    deleteCanva()
    makeImage()
    try:
        record = weapons.next()
        func(record)
        details_button = tk.Button(window, text="Next", command=lambda: show(what_kind_of, weapons, func))
        canva.create_window(450, 480, window=details_button)
    except StopIteration:
        new_label = tk.Label(window, text="Nie ma więcej \nprzedmiotów pasujących \ndo Twoich wymagań", font=font, fg=fg_color,
                             bg=bg_color)
        canva.create_window(400, 180, window=new_label)
    back_button = ""
    if what_kind_of == "armor" or what_kind_of == "weapon":
        back_button = tk.Button(window, text="Back", command=lambda: make_choice_window(what_kind_of))
    elif what_kind_of == "book":
        back_button = tk.Button(window, text="Back", command=lambda: make_book_window())
    elif what_kind_of == "potion":
        back_button = tk.Button(window, text="Back", command=lambda: make_potion_window())
    canva.create_window(200, 500, window=back_button)



def searchFor(what_kind_of):
    deleteCanva()
    makeImage()
    statistic = statistic_check.get()
    value = value_check.get()
    weight = weight_check.get()
    min_s, max_s, min_v, max_v, min_w, max_w = 0, 2000000, 0, 2000000, 0, 2000000

    if statistic == 0:
        if min_entry.get() != "":
            min_s = int(min_entry.get())
        if max_entry.get() != "":
            max_s = int(max_entry.get())
    if value == 0:
        if min_value.get() != "":
            min_v = int(min_value.get())
        if max_value.get() != "":
            max_v = int(max_value.get())
    if weight == 0:
        if min_weight.get() != "":
            min_w = int(min_weight.get())
        if max_weight.get() != "":
            max_w = int(max_weight.get())

    weapon = ""
    if what_kind_of == "weapon":
        weapon = findWeapon(min_s, max_s, min_v, max_v, min_w, max_w)
    elif what_kind_of == "armor":
        weapon = findArmor(min_s, max_s, min_v, max_v, min_w, max_w)
    if weapon is not None:
        show(what_kind_of, weapon, showDetails)
    else:
        new_label = tk.Label(window, text="Brak takiego przedmiotu!", font=font, fg=fg_color, bg=bg_color)
        canva.create_window(380, 200, window=new_label)

    back_button = tk.Button(window, text="Back", command=lambda: make_choice_window(what_kind_of))
    canva.create_window(200, 500, window=back_button)


def showDetailsForBooks(book):
    y_offset = 25
    deleteCanva()
    makeImage()
    description_offset = 0
    for idx, label in enumerate(book):
        if label == "description":
            description_offset = 90
        if label != "_id":
            new_label = tk.Label(window, text="{}: ".format(labels[label]), font=small_font, fg=fg_color,
                                 bg=bg_color)
            new_label2 = tk.Label(window, text="{}".format(book[label]), font=small_font, fg=fg_color,
                                  bg=bg_color)
            canva.create_window(150, 180 + idx * y_offset + description_offset, window=new_label)
            canva.create_window(450, 180 + idx * y_offset + description_offset, window=new_label2)


def findBook(min_m, max_m, spell_school, spell_level):
    if spell_school == "" and spell_level == "":
        return db.books.find({
            "mana_cost": {"$gt": min_m},
            "mana_cost": {"$lt": max_m}
        })
    elif spell_school == "":
        return db.books.find({
            "level": spell_level,
            "mana_cost": {"$gt": min_m},
            "mana_cost": {"$lt": max_m}
        })
    elif spell_level == "":
        return db.books.find({
            "school_of_magic": spell_school,
            "mana_cost": {"$gt": min_m},
            "mana_cost": {"$lt": max_m}
        })
    else:
        return db.books.find({
            "level": spell_level,
            "school_of_magic": spell_school,
            "mana_cost": {"$gt": min_m},
            "mana_cost": {"$lt": max_m}
        })


def searchForBooks():
    deleteCanva()
    makeImage()
    value = value_check.get()
    min_v, max_v = 0, 200000
    spell_school = spell_book_type.get()
    spell_level = level_book_type.get()
    if spell_school == "Wszystkie" or spell_school == "Szkoła magii":
        spell_school = ""
    if spell_level == "Wszystkie" or spell_level == "Poziom":
        spell_level = ""

    if value == 0 and min_value.get() != "":
        min_v = (int)(min_value.get())
    if value == 0 and max_value.get() != "":
        max_v = (int)(max_value.get())

    books = findBook(min_v, max_v, spell_school, spell_level)
    if books is not None:
        show("book", books, showDetailsForBooks)
    else:
        new_label = tk.Label(window, text="Brak takiego przedmiotu!", font=font, fg=fg_color, bg=bg_color)
        canva.create_window(380, 200, window=new_label)

    back_button = tk.Button(window, text="Back", command=lambda: make_book_window())
    canva.create_window(200, 500, window=back_button)


def showDetailsForPotions(potion):
    y_offset = 25
    deleteCanva()
    makeImage()
    label_offset = 0
    for idx, label in enumerate(potion):
        if label == "effect":
            label_offset = 1
        if label != "_id":
            new_label = tk.Label(window, text="{}: ".format(labels[label]), font=small_font, fg=fg_color,
                                 bg=bg_color)
            new_label2 = tk.Label(window, text="{}".format(potion[label]), font=small_font, fg=fg_color,
                                  bg=bg_color)
            canva.create_window(150, 180 + (idx + label_offset) * y_offset, window=new_label)
            canva.create_window(450, 180 + (idx + label_offset) * y_offset, window=new_label2)



def findPotion(min_v, max_v, search):
    if search == "":
        return db.potions.find({
            "value": {"$gt": min_v},
            "value": {"$lt": max_v}
        })
    return db.potions.find({
        "type_of_restoring": search,
        "value": {"$gt": min_v},
        "value": {"$lt": max_v}
    })

def searchForPotions():
    deleteCanva()
    makeImage()
    value = value_check.get()
    min_v, max_v = 0, 200000
    type_search = ""
    type_of_potion = potion_var.get()
    if type_of_potion == "Restore Health":
        type_search = "health"
    if type_of_potion == "Restore Mana":
        type_search = "mana"
    if type_of_potion == "Restore Stamina":
        type_search = "stamina"

    if value == 0 and min_value.get() != "":
        min_v = (int)(min_value.get())
    if value == 0 and max_value.get() != "":
        max_v = (int)(max_value.get())

    potions = findPotion(min_v, max_v, type_search)
    if potions is not None:
        show("potion", potions, showDetailsForPotions)
    else:
        new_label = tk.Label(window, text="Brak takiego przedmiotu!", font=font, fg=fg_color, bg=bg_color)
        canva.create_window(380, 200, window=new_label)

    back_button = tk.Button(window, text="Back", command=lambda: make_potion_window())
    canva.create_window(200, 500, window=back_button)


def makeLabel(text):
    return tk.Label(window, text=text, bg=bg_color, fg=fg_color)


def make_choice_window(what_kind_of):
    deleteCanva()
    if what_kind_of == "weapon":
        min_text = makeLabel("Min attack")
        max_text = makeLabel("Max attack")
    elif what_kind_of == "armor":
        min_text = makeLabel("Min armor")
        max_text = makeLabel("Max armor")

    x = 200
    y = 300
    z = 400
    makeImage()
    label = ""
    if what_kind_of == "weapons":
        label = tk.Label(text="Weapons", bg=bg_color, fg=fg_color, font=font)
    elif what_kind_of == "armor":
        label = tk.Label(text="Armors", bg=bg_color, fg=fg_color, font=font)
    min_v_text = makeLabel("Min value")
    max_v_text = makeLabel("Max value")
    min_w_text = makeLabel("Min weight")
    max_w_text = makeLabel("Max weight")
    search = tk.Button(window, text="Search!", command=lambda: searchFor(what_kind_of))
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

    #button Search
    canva.create_window(600, 500, window=search)

    #back button
    back_button = tk.Button(window, text="Back", command=makeCanva)
    canva.create_window(200, 500, window=back_button)


def make_potion_window():
    deleteCanva()
    makeImage()
    x = 200
    y = 300
    z = 400
    label = tk.Label(text="Potions", bg=bg_color, fg=fg_color, font=font)
    min_v_text = makeLabel("Min value")
    max_v_text = makeLabel("Max value")
    search = tk.Button(window, text="Search!", command=searchForPotions)
    canva.create_window(380, x - 40, window=label)

    potion_var.set("Potions")
    effects = ["Wszystkie", "Restore Health", "Restore Mana", "Restore Stamina"]

    dropdown = tk.OptionMenu(window, potion_var, *effects)

    # value
    canva.create_window(150, y, window=min_value)
    canva.create_window(400, y, window=max_value)
    canva.create_window(50, y, window=min_v_text)
    canva.create_window(300, y, window=max_v_text)
    canva.create_window(600, y, window=v_check)

    #dropdown
    canva.create_window(150, z, window=dropdown)


    # button Search
    canva.create_window(600, 500, window=search)

    #back button
    back_button = tk.Button(window, text="Back", command=makeCanva)
    canva.create_window(200, 500, window=back_button)

def make_book_window():
    deleteCanva()
    makeImage()
    x = 200
    y = 300
    z = 400
    label = tk.Label(text="Potions", bg=bg_color, fg=fg_color, font=font)
    min_v_text = makeLabel("Koszt many min")
    max_v_text = makeLabel("Koszt many max")
    search = tk.Button(window, text="Search!", command=searchForBooks)
    canva.create_window(380, x - 40, window=label)

    spell_book_type.set("Szkoła magii")
    spells_type = ["Wszystkie", "Przywracanie", "Iluzja", "Przywołanie", "Zniszczenie", "Przemiana"]
    level_book_type.set("Poziom")
    level_type = ["Wszytskie", "Nowicjusz", "Uczeń", "Czeladnik", "Ekspert", "Mistrz"]

    spell_dropdown = tk.OptionMenu(window, spell_book_type, *spells_type)
    level_dropdown = tk.OptionMenu(window, level_book_type, *level_type)

    # mana cost
    canva.create_window(150, y, window=min_value)
    canva.create_window(400, y, window=max_value)
    canva.create_window(50, y, window=min_v_text)
    canva.create_window(300, y, window=max_v_text)
    canva.create_window(600, y, window=v_check)

    # spell dropdown
    canva.create_window(150, z, window=spell_dropdown)

    #level dropdown
    canva.create_window(450, z, window=level_dropdown)

    # button Search
    canva.create_window(600, 500, window=search)

    #back button
    back_button = tk.Button(window, text="Back", command=makeCanva)
    canva.create_window(200, 500, window=back_button)


tk.mainloop()
