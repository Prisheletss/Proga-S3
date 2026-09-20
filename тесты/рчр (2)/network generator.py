from random import *



try:
    file = open("neyrons.txt", 'x')
except FileExistsError:
    file = open("neyrons.txt", 'w')



neyrons = [
    20*34, # макс длина слова на вход (20 симв, 33 букв, 1 пробел)
    256,
    50,
    9 # сущ, прил, числ, мм, глаг, нар, прич, дееприч, союз
]


file.write(f"{len(neyrons)}\n")



for i in range(len(neyrons)-1):
    print(i+1, '/', len(neyrons)-1)
    file.write('\n')
    file.write(f"{neyrons[i]} {neyrons[i+1]}\n")
    
    for _ in range(neyrons[i+1]):
        for _ in range(neyrons[i]):
            file.write(f"{10*(random()-0.5)}\t")
        file.write(f"{10*(random()-0.5)}\n")






file.close()
