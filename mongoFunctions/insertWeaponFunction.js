function insertWeapon(name, basic_attack, weight, value, is_unique, enchantments, is_onehanded, type){
    db.weapons.insert({
        name: name,
        basic_attack: basic_attack,
        weight: weight,
        value: value,
        is_unique: is_unique,
        enchantments:enchantments,
        is_onehanded:is_onehanded,
        type:type
        }
    )
}