function insertArmor(name, basic_armor, weight, value, is_unique, enchantments, is_light, type){
    db.armor.insert({
        name: name,
        basic_armor: basic_armor,
        weight: weight,
        value: value,
        is_unique: is_unique,
        enchantments:enchantments,
        is_light:is_light,
        type:type
        }
    )
}
