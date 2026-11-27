import sqlite3

db = sqlite3.connect("../data/training_data.db")

c = db.cursor()

"""
слово 
существительное (сущ)
прилагательное (прил)
числительное (числ)
местоимение (мм)
глагол (глаг)
наречие (нар)
причастие (прич)
деепричастие (дееприч)
союз (союз)
"""

c.execute("DROP TABLE IF EXISTS training_data")

c.execute("""CREATE TABLE training_data (
    id int AUTO INCREMENT PRIMARY KEY,
    word varchar(20),
    noun int(1) DEFAULT 0,
    adjective int(1) DEFAULT 0,
    numeral int(1) DEFAULT 0,
    pronoun int(1) DEFAULT 0,
    verb int(1) DEFAULT 0,
    adverb int(1) DEFAULT 0,
    participle int(1) DEFAULT 0,
    adverbial_participle int(1) DEFAULT 0,
    conjunction int(1) DEFAULT 0
)
""")
db.commit()

files = {
    "сущ": "noun",
    "прил": "adjective",
    "числ": "numeral",
    "мм": "pronoun",
    "глаг": "verb",
    "нар": "adverb",
    "прич": "participle",
    "дееприч": "adverbial_participle",
    "союз": "conjunction"
}

for filename in files:
    print(filename)
    file = open(f"../data/training data/{filename}.txt", 'r', -1, "utf-8")
    comand = "INSERT INTO `training_data` (`word`, " + f"`{files[filename]}`) VALUES"
    t = 0

    for line in file:
        if t != 0:
            comand += ", "
        if '\n' in line:
            line = line[0:-1]
        comand += f"('{line}', 1)"
        t += 1

    comand += ';'
    c.execute(comand)
    db.commit()

db.close()
