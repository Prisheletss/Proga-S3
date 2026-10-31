from random import *



try:
    file = open("weights and biases.txt", 'x')
except FileExistsError:
    file = open("weights and biases.txt", 'w')



input_len = 20 # макс длина слова на вход (симв)
output_len = 9 # сущ, прил, числ, мм, глаг, нар, прич, дееприч, союз


file.write(f"{input_len}\t{output_len}\n")

for _ in range(output_len):
    print("progress:", _+1, '/', output_len)
    for _ in range(input_len):
        file.write(f"{10*(random()-0.5)}\t")
    file.write(f"{random()}\n")


file.close()
