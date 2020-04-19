function insertPotion(name, type_of_restoring, weight, value, effect){
    db.potions.insert({
        name: name,
        type_of_restoring: type_of_restoring,
        weight:weight,
        value:value,
        effect:effect
        }
    )
}

insertPotion("Misktura pomniejszego uleczenia", "health", 0.5, 17, "Przywraca 25 punktów zdrowia")