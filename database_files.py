from pymongo import MongoClient

client = MongoClient('mongodb+srv://dawid:dawid99@skyrimcluster-j4jje.gcp.mongodb.net/test')
db = client.skyrimDatabase

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


def add_weapon(name, stat, value, weight, type, is_unique, is_onehanded):
    dict = {
        "name": name,
        "basic_attack": stat,
        "weight": weight,
        "value": value,
        "type": type,
        "is_unique": is_unique,
        "is_onehanded": is_onehanded,
        "enchantments": [],
    }
    db.weapons.insert_one(dict)
    return 1