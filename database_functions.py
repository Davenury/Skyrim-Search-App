from pymongo import MongoClient

client = MongoClient('mongodb+srv://dawid:dawid99@skyrimcluster-j4jje.gcp.mongodb.net/test')
db = client.skyrimDatabase

#finding functions
def findWeapon(min_s, max_s, min_v, max_v, min_w, max_w):
    return db.weapons.find({
        "basic_attack": {"$gte":min_s, "$lte":max_s},
        "value": {"$gte": min_v, "$lte": max_v},
        "weight": {"$gte": min_w, "$lte": max_w},
    })


def findArmor(min_s, max_s, min_v, max_v, min_w, max_w):
    return db.armor.find({
        "basic_armor": {"$gte": min_s, "$lte": max_s},
        "value": {"$gte": min_v, "$lte": max_v},
        "weight": {"$gte": min_w, "$lte": max_w},
    })


def findBook(min_m, max_m, spell_school, spell_level):
    if spell_school == "" and spell_level == "":
        return db.books.find({
            "mana_cost": {"$gte": min_m, "$lte": max_m}
        })
    elif spell_school == "":
        return db.books.find({
            "level": spell_level,
            "mana_cost": {"$gt": min_m, "$lt": max_m}
        })
    elif spell_level == "":
        return db.books.find({
            "school_of_magic": spell_school,
            "mana_cost": {"$gt": min_m, "$lt": max_m}
        })
    else:
        return db.books.find({
            "level": spell_level,
            "school_of_magic": spell_school,
            "mana_cost": {"$gt": min_m, "$lt": max_m}
        })


def findPotion(min_v, max_v, search):
    if search == "":
        return db.potions.find({
            "value": {"$gt": min_v, "$lt": max_v}
        })
    return db.potions.find({
        "type_of_restoring": search,
        "value": {"$gt": min_v, "$lt": max_v}
    })
#end of finding functions

#add functions
def add_weapon(name, stat, value, weight, type, is_unique, is_onehanded, enchant1, enchant2):
    dict = {
        "name": name,
        "basic_attack": stat,
        "weight": weight,
        "value": value,
        "type": type,
        "is_unique": is_unique,
        "is_onehanded": is_onehanded,
        "enchantment": [enchant1, enchant2],
    }
    db.weapons.insert_one(dict)
    return 1


def add_armor(name, stat, value, weight, type, is_unique, is_light, enchant1, enchant2):
    dict = {
        "name": name,
        "basic_armor": stat,
        "weight": weight,
        "value": value,
        "type": type,
        "is_unique": is_unique,
        "is_light": is_light,
        "enchantments": [enchant1, enchant2],
    }
    db.armor.insert_one(dict)
    return 1


def add_book(name, mana_cost, level, school_of_magic, description):
    dict = {
        "name": name,
        "level": level,
        "school_of_magic": school_of_magic,
        "mana_cost": mana_cost,
        "description": description
    }
    db.books.insert_one(dict)
    return 1


def add_potion(name, type_of_restoring, weight, value, effect):
    dict ={
        "name": name,
        "type_of_restoring": type_of_restoring,
        "weight": weight,
        "value": value,
        "effect": effect
    }
    db.potions.insert_one(dict)
    return 1
#end of add functions


#modify functions
def modify_weapon(id, name, stat, value, weight, type, is_unique, is_onehanded, enchant1, enchant2):
    my_query = {"_id" : id}
    new_values = { "$set" : {
        "name": name,
        "basic_attack": stat,
        "weight": weight,
        "value": value,
        "type": type,
        "is_unique": is_unique,
        "is_onehanded": is_onehanded,
        "enchantment": [enchant1, enchant2],
    }}
    db.weapons.update_one(my_query, new_values)
    return 1


def modify_armor(id, name, stat, value, weight, type, is_unique, is_light, enchant1, enchant2):
    my_query = {"_id":id}
    new_values = {"$set":{
        "name" : name,
        "basic_armor" : stat,
        "weight": weight,
        "value": value,
        "type": type,
        "is_unique": is_unique,
        "is_light": is_light,
        "enchantment": [enchant1, enchant2],
    }}
    db.armor.update_one(my_query, new_values)
    return 1


def modify_potion(id, name, restore, weight, value, effect):
    my_query = {"_id": id}
    new_values = {"$set":{
        "name": name,
        "type_of_restoring": restore,
        "weight": weight,
        "value": value,
        "effect": effect
    }}
    db.potions.update_one(my_query, new_values)
    return 1


def modify_book(id, name, cost, level, school, description):
    my_query = {"_id": id}
    new_values = {"$set" : {
        "name": name,
        "level": level,
        "school_of_magic": school,
        "mana_cost": cost,
        "description": description
    }}
    db.books.update_one(my_query, new_values)
    return 1


def delete_weapon(weapon):
    my_query = {"_id" : weapon["_id"]}
    db.weapons.delete_one(my_query)
    return 1


def delete_armor(armor):
    my_query = {"_id": armor["_id"]}
    db.armor.delete_one(my_query)
    return 1


def delete_book(book):
    my_query = {"_id": book["_id"]}
    db.books.delete_one(my_query)
    return 1


def delete_potion(potion):
    my_query = {"_id": potion["_id"]}
    db.potions.delete_one(my_query)
    return 1