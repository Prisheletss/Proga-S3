import sqlite3
import numpy
import copy
from math import *



def sigmoid(x):
    ans = e**(-x)
    ans = 1 / (1+ans)
    return ans



def Calculate(x, W, B):
    x = numpy.array([[i] for i in x])

    #print(x)
    ans = numpy.dot(W, x)
    ans = numpy.add(ans, B)

    ans = [sigmoid(i[0]) for i in ans]
    
    return ans



def accuracy(target, result):
    c = 0
    for j in range(output_len):
        c += (target[j] - result[j])**2

    return c



def grad(target, code):
    global W, B

    result = Calculate(code, W, B)
    c0 = accuracy(target, result)

    dW = []
    dB = []
    step = 1
    
    for i in range(output_len):
        dW.append([])
        for j in range(input_len):
            w = copy.deepcopy(W)
            w[i][j] += step

            result = Calculate(code, w, B)
            c1 = accuracy(target, result)
            #print(c)
            dW[-1].append((c1-c0) / step)

    for i in range(output_len):
        b = copy.deepcopy(B)
        b[i] += step

        result = Calculate(code, W, b)
        c1 = accuracy(target, result)
        dB.append((c1-c0) / step)

    dW = numpy.array(dW)
    dB = numpy.array([[i] for i in dB])

    return dW, dB



#def values_tester()







file = open("weights and biases.txt", 'r')

W = []
B = []


line = file.readline()
line = line.split('\t')
input_len, output_len = map(int, line)


for line in file:
    line = list(map(float, line.split('\t')))
    W.append(line[0:-1])
    B.append([line[-1]])

file.close()


W = numpy.array(W)
B = numpy.array(B)








database = sqlite3.connect("data.db")

cursor = database.cursor()

cursor.execute('SELECT * FROM `trainig_data`')
data = cursor.fetchall()

database.close()




letters = {
    'А': 1,
    'Б': 2,
    'В': 3,
    'Г': 4,
    'Д': 5,
    'Е': 6,
    'Ё': 7,
    'Ж': 7+1,
    'З': 8+1,
    'И': 9+1,
    'Й': 10+1,
    'К': 11+1,
    'Л': 12+1,
    'М': 13+1,
    'Н': 14+1,
    'О': 15+1,
    'П': 16+1,
    'Р': 17+1,
    'С': 18+1,
    'Т': 19+1,
    'У': 20+1,
    'Ф': 21+1,
    'Х': 22+1,
    'Ц': 23+1,
    'Ч': 24+1,
    'Ш': 25+1,
    'Щ': 26+1,
    'Ъ': 27+1,
    'Ы': 28+1,
    'Ь': 29+1,
    'Э': 30+1,
    'Ю': 31+1,
    'Я': 32+1,
    'а': 33+1,
    'б': 34+1,
    'в': 35+1,
    'г': 36+1,
    'д': 37+1,
    'е': 38+1,
    'ё': 40,
    'ж': 39+2,
    'з': 40+2,
    'и': 41+2,
    'й': 42+2,
    'к': 43+2,
    'л': 44+2,
    'м': 45+2,
    'н': 46+2,
    'о': 47+2,
    'п': 48+2,
    'р': 49+2,
    'с': 50+2,
    'т': 51+2,
    'у': 52+2,
    'ф': 53+2,
    'х': 54+2,
    'ц': 55+2,
    'ч': 56+2,
    'ш': 57+2,
    'щ': 58+2,
    'ъ': 59+2,
    'ы': 60+2,
    'ь': 61+2,
    'э': 62+2,
    'ю': 63+2,
    'я': 64+2,
    ' ': 0
}

step = 1



for asdf in range(1):
    print("===== ===== ===== =====")
    print(asdf)
    for i in data:
        print(i[0])
        word = i[0]
        target = i[1::]

        word = word + (20-len(word))*' '
        code = [letters[j]/66 for j in word]
        
        
        """
        print(f"Слово: {word}")
        print("Цель:", end=' ')
        print(*target, sep='\t')
        print("Результат:", end=' ')
        print(*result, sep='\t')
        print("Точность:", c)

        print('')
        """

        result = Calculate(code, W, B)
        c0 = accuracy(target, result)


        
        for i in range(100):
            dW, dB = grad(target, code)

            W -= step*dW
            B -= step*dB



        w = [[float(W[j][k]) for k in range(input_len)] for j in range(output_len)]
        b = [float(B[j][0]) for j in range(output_len)]

        result = Calculate(code, W, B)
        c1 = accuracy(target, result)

        #print(*w, sep='\n')
        #print("\n\n")
        #print(*b)
        #print("\n\n")
        #print(word, c0, c1)

        #print("\n\n\n\n\n\n")

        #print(f"Слово: {word}")
        #print("Цель:", end=' ')
        #print(*target, sep='\t')
        #print("Результат:", end=' ')
        #print(*result, sep='\t')
        #print("Точность:", c0, c1)

        #print('\n\n')





    
try:
    file = open("second generation.txt", 'x')
except FileExistsError:
    file = open("second generation.txt", 'w')



for i in range(output_len):
    print("progress:", i+1, '/', output_len)
    for j in range(input_len):
        file.write(f"{W[i][j]}\t")
    file.write(f"{B[i]}\n")


file.close()










































































































