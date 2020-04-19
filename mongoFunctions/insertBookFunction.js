function insertBook(name, level, school_of_magic, mana_cost, description){
    db.books.insert({
        name:name,
        level:level,
        school_of_magic:school_of_magic,
        mana_cost:mana_cost,
        description:description
    })
}