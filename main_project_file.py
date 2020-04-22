import tkinter as tk
from PIL import Image, ImageTk
import database_files as db_func


bg_color = "#717171"
fg_color = "#eeeeee"
font = ("Courier", 20)
small_font = ("Courier", 14)

#słownik przekształcający nazwy pól kolekcji do postaci czytelnej dla człowieka
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

#główne okienko aplikacji
window = tk.Tk()
window.title("Skyrim app")
window.geometry("800x600+50+50")
canva = tk.Canvas(window, width=800, height=600, background=bg_color)
canva.pack()
load = Image.open("logo.png")
render = ImageTk.PhotoImage(load)


#ekran startowy
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
    add_label = tk.Label(text="Może coś dodać?", bg=bg_color, fg=fg_color, font=font)
    canva.create_window(400, 400, window=add_label)
    add_weapon = tk.Button(window, text="Dodaj broń", command=lambda: add_weapon_window())
    canva.create_window(100, 500, window=add_weapon)
    add_armor = tk.Button(window, text="Dodaj zbroję", command=lambda: add_armor_window())
    canva.create_window(300, 500, window=add_armor)
    add_potion = tk.Button(window, text="Dodaj miksturę", command=lambda: add_potion_window())
    canva.create_window(500, 500, window=add_potion)
    add_book = tk.Button(window, text="Dodaj księgę", command=lambda: add_book_window())
    canva.create_window(700, 500, window=add_book)


def deleteCanva():
    canva.delete("all")


def makeImage():
    canva.create_image(380, 70, image=render)


min_entry = tk.Entry(window)
max_entry = tk.Entry(window)
min_weight = tk.Entry(window)
max_weight = tk.Entry(window)
min_value = tk.Entry(window)
max_value = tk.Entry(window)

potion_var = tk.StringVar(window)
spell_book_type = tk.StringVar(window)
level_book_type = tk.StringVar(window)


#obsługa checków Don't care
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
#koniec checków


#funkcja przeskakująca po wszystkich dokumentach z danego query
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


#obłusga broni i zbroi
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

    print(min_v, max_v)

    weapon = ""
    if what_kind_of == "weapon":
        weapon = db_func.findWeapon(min_s, max_s, min_v, max_v, min_w, max_w)
    elif what_kind_of == "armor":
        weapon = db_func.findArmor(min_s, max_s, min_v, max_v, min_w, max_w)
    if weapon is not None:
        show(what_kind_of, weapon, showDetails)
    else:
        new_label = tk.Label(window, text="Brak takiego przedmiotu!", font=font, fg=fg_color, bg=bg_color)
        canva.create_window(380, 200, window=new_label)

    back_button = tk.Button(window, text="Back", command=lambda: make_choice_window(what_kind_of))
    canva.create_window(200, 500, window=back_button)
#koniec broni i zbroi


#obsługa książek

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

    books = db_func.findBook(min_v, max_v, spell_school, spell_level)
    if books is not None:
        show("book", books, showDetailsForBooks)
    else:
        new_label = tk.Label(window, text="Brak takiego przedmiotu!", font=font, fg=fg_color, bg=bg_color)
        canva.create_window(380, 200, window=new_label)

    back_button = tk.Button(window, text="Back", command=lambda: make_book_window())
    canva.create_window(200, 500, window=back_button)

#koniec książek

#obsługa potionków

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

    potions = db_func.findPotion(min_v, max_v, type_search)
    if potions is not None:
        show("potion", potions, showDetailsForPotions)
    else:
        new_label = tk.Label(window, text="Brak takiego przedmiotu!", font=font, fg=fg_color, bg=bg_color)
        canva.create_window(380, 200, window=new_label)

    back_button = tk.Button(window, text="Back", command=lambda: make_potion_window())
    canva.create_window(200, 500, window=back_button)

#koniec potionków


def makeLabel(text):
    return tk.Label(window, text=text, bg=bg_color, fg=fg_color)


#widoki wyborów

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

#koniec widoków wyborów

#entersy dodawania
add_stat_entry = tk.Entry(window)
add_value_entry = tk.Entry(window)
add_weight_entry = tk.Entry(window)
add_name_entry = tk.Entry(window)
add_type_entry = tk.Entry(window)
add_school_entry = tk.Entry(window)
add_level_entry = tk.Entry(window)
add_restore_entry = tk.Entry(window)
add_description_entry = tk.Entry(window)
add_is_light = tk.StringVar(window)
add_is_light_dropdown = tk.OptionMenu(window, add_is_light, *["Tak", "Nie"])
add_unique = tk.StringVar(window)
add_is_unique_dropdown = tk.OptionMenu(window, add_unique,*["Tak", "Nie"])

#widoki dodawania
def add_weapon_window():
    deleteCanva()
    makeImage()
    stat_text = makeLabel("Atak:")
    canva.create_window(100, 200, window=stat_text)
    canva.create_window(200, 200, window=add_stat_entry)
    name_text = makeLabel("Nazwa:")
    canva.create_window(100, 300, window=name_text)
    canva.create_window(200, 300, window=add_name_entry)
    weight_text = makeLabel("Waga:")
    canva.create_window(100, 400, window=weight_text)
    canva.create_window(200, 400, window=add_weight_entry)
    value_text = makeLabel("Wartość:")
    canva.create_window(100, 500, window=value_text)
    canva.create_window(200, 500, window=add_value_entry)
    type_text = makeLabel("Typ:")
    canva.create_window(400, 200, window=type_text)
    canva.create_window(500, 200, window=add_type_entry)
    add_unique.set("Czy jest unikalny?")
    canva.create_window(500, 300, window=add_is_unique_dropdown)
    add_is_light.set("Czy jest jednoręczny?")
    canva.create_window(500, 400, window=add_is_light_dropdown)
    add_button = tk.Button(window, text="Dodaj", command=add_weapon)
    canva.create_window(500, 500, window=add_button)
    back_button = tk.Button(window, text="Back", command=makeCanva)
    canva.create_window(200, 550, window=back_button)


def add_armor_window():
    pass


def add_potion_window():
    pass


def add_book_window():
    pass


def makeAddedView():
    deleteCanva()
    makeImage()
    label = tk.Label(text="Dodano ^^", bg=bg_color, fg=fg_color, font=font)
    canva.create_window(300, 300, window=label)
    back_button = tk.Button(window, text="Back", command=makeCanva)
    canva.create_window(200, 550, window=back_button)

#koniec widoków dodawania


#funkcje dodawania
def add_weapon():
    stat, value, weight, name, type = 0,0,0,0,0
    is_unique, is_onehanded = False, False
    is_everything_ok = True
    if add_stat_entry.get() and add_stat_entry.get().isnumeric():
        stat = (int)(add_stat_entry.get())
        is_everything_ok = is_everything_ok and True
    else:
        add_stat_entry.focus_set()
        is_everything_ok = False
    if add_value_entry.get() and add_value_entry.get().isnumeric():
        value = (int)(add_value_entry.get())
        is_everything_ok = is_everything_ok and True
    else:
        add_value_entry.focus_set()
        is_everything_ok = False
    if add_weight_entry.get() and add_weight_entry.get().isnumeric():
        weight = (int)(add_weight_entry.get())
        is_everything_ok = is_everything_ok and True
    else:
        add_weight_entry.focus_set()
        is_everything_ok = False
    if add_name_entry.get():
        name = add_name_entry.get()
        is_everything_ok = is_everything_ok and True
    else:
        add_name_entry.focus_set()
        is_everything_ok = False
    if add_type_entry.get():
        type = add_type_entry.get()
        is_everything_ok = is_everything_ok and True
    else:
        add_type_entry.focus_set()
        is_everything_ok = False
    if add_unique.get() == "Tak":
        is_unique = True
    if add_is_light.get() == "Tak":
        is_onehanded = True

    if is_everything_ok:
       if(db_func.add_weapon(name, stat, value, weight, type, is_unique, is_onehanded) == 1):
           makeAddedView()


makeCanva()
tk.mainloop()
