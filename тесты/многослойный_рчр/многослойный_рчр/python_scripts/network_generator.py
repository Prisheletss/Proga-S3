from random import *
import sqlite3
import os


print('Оставить файл для бд по умолчанию "network"? \n'
      'Введите "0", если хотите выбрать другой файл')
_ = input()
if _ == "0":
    db_file = input("Введите новое имя файла: ")
    db_file = "../data/" + db_file
else:
    print("Все данные из предыдущей версии будут потерянны")
    db_file = "../data/network.db"

try:
    _ = open(db_file, 'x')
except FileExistsError:
    os.remove("../data/network.db")


db = sqlite3.connect(db_file)
c = db.cursor()



print("\nОставить слои матрицы по умолчанию? \n"
      'Введите "0", если нет')
_ = input()

neurons = None
if _ == "0":
    neurons = input("Введите через пробел размеры всех слоёв")
    neurons = list(map(int, neurons.split(' ')))
else:
    neurons = [
        20,  # макс длина слова на вход (20 букв)
        32,
        32,
        9  # сущ, прил, числ, мм, глаг, нар, прич, дееприч, союз
    ]



"""
file.write(f"{len(neyrons)}\n")

for i in range(len(neyrons) - 1):
    print(i + 1, '/', len(neyrons) - 1)
    file.write('\n')
    file.write(f"{neyrons[i]} {neyrons[i + 1]}\n")

    for _ in range(neyrons[i + 1]):
        for _ in range(neyrons[i]):
            file.write(f"{10 * (random() - 0.5)}\t")
        file.write(f"{10 * (random() - 0.5)}\n")

file.close()
"""


c.execute(
"CREATE TABLE all_matrices ("
"   id int AUTO INCREMENT PRIMARY KEY,"
"   size_x int,"
"   size_y int"
");"
)



for i in range(len(neurons)-1):
    request = f"CREATE TABLE m_{i} (row_num float AUTO INCREMENT PRIMARY KEY, "

    for j in range(neurons[i]):
        request += f"col_{j} float"
        request += ',' if (j < neurons[i]-1) else ");"

    c.execute(request)

    request = f"INSERT INTO m_{i} VALUES "
    for j in range(neurons[i+1]):
        request += f"({j}, "
        for k in range(neurons[i]):
            request += f"{10*random() - 5}"
            request += ',' if (k < neurons[i]-1) else ')'
        request += ", " if (j < neurons[i+1]-1) else ';'

    c.execute(request)




db.commit()
db.close()