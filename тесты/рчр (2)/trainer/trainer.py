from consts import *





glob_W_s = []
glob_B_s = []
neurons = []








def Init(filename):
    global glob_W_s, glob_B_s, neurons

    glob_W_s = []
    glob_B_s = []
    neurons = []
    
    file = open(f"{filename}.txt", 'r')
    amount = int(file.readline())

    for _ in range(amount-1):
        line = file.readline()
        w = []
        b = []

        line = file.readline()
        line = line.split(' ')
        line = list(map(str.strip, line))
        inp, out = list(map(int, line))
        if len(neurons) == 0:
            neurons += [inp, out]
        else:
            neurons.append(out)

        for i in range(out):
            line = file.readline()
            line = list(map(float, line.split('\t')))
            w.append(line[0:-1])
            b.append([line[-1]])

        glob_W_s.append(numpy.array(w))
        glob_B_s.append(numpy.array(b))


    file.close()





def sigmoid(x):
    x = 1 + e**(-x)
    return 1/x





def Calculate_layer(x: list, W, B):
    x = numpy.array(x)
    y = numpy.dot(W, x)
    y = numpy.add(y, B)

    y = [sigmoid(i[0]) for i in y]
    return y





def Calculate_all(x: list, W_s, B_s):
    global neurons

    for i in range(len(neurons)-1):
        W = W_s[i]
        B = B_s[i]

        x = Calculate_layer(x, W, B)

    return x





def coder(word):
    word = word + (20-len(word))*' '
    word = [letters[i] for i in word]

    code = []
    for i in word:
        c = '0'*i + '1'
        c = c + (34-len(c))*'0'
        c = [int(j) for j in c]
        code += c

    return code





def error_value(target, result):
    c = 0
    for j in range(len(result)):
        c += (target[j] - result[j]) ** 2

    return c





def gradient(x, target):
    global glob_W_s, glob_B_s, neurons

    result = Calculate_all(x, glob_W_s, glob_B_s)
    c0 = error_value(target, result)

    dW_s = []
    dB_s = []
    step = 0.1

    for i in range(len(neurons)-1):
        #print(i+1, '/', len(neurons)-1)
        dW = []
        dB = []

        for j in range(neurons[i+1]):
            #print('\t', j + 1, '/', neurons[i+1])
            dW.append([])
            for k in range(neurons[i]):
                W_s = copy.deepcopy(glob_W_s)
                W_s[i][j][k] += step

                result = Calculate_all(x, W_s, glob_B_s)
                c1 = error_value(target, result)
                dW[-1].append((c1-c0) / step)

            B_s = copy.deepcopy(glob_B_s)
            B_s[i][j][0] += step

            result = Calculate_all(x, glob_W_s, B_s)
            c1 = error_value(target, result)
            dB.append([(c1 - c0) / step])

        dW_s.append(numpy.array(dW))
        dB_s.append(numpy.array(dB))


    return dW_s, dB_s





def study(train_data):
    global glob_W_s, glob_B_s, neurons

    step = 0.1

    word = train_data[0]
    target = train_data[1::]

    code = coder(word)
    result = Calculate_all(code, glob_W_s, glob_B_s)
    c = error_value(target, result)


    try:
        accuracy_graph = open("accuracy_graph.txt", 'x')
    except FileExistsError:
        accuracy_graph = open("accuracy_graph.txt", 'a')

    accuracy_graph.write(f"{c}\n")
    accuracy_graph.close()


    dW_s, dB_s = gradient(code, target)

    for i in range(len(glob_W_s)):
        #print(dW_s[i])
        glob_W_s[i] -= step * dW_s[i]
        glob_B_s[i] -= step * dB_s[i]





def test(word):
    global glob_W_s, glob_B_s

    code = coder(word)

    result = Calculate_all(code, glob_W_s, glob_B_s)
    print(word, "--", parts[result.index(max(result))])





database = sqlite3.connect("../data.db")

cursor = database.cursor()

cursor.execute('SELECT * FROM `training_data`')
data = cursor.fetchall()

database.close()

#t = 0
while True:
    Init("../neyrons")
    train = data[randint(0, len(data) - 1)]

    #if (t % 2) == 0:
    word = train[0]
    test(word)
    print('\n')
    #t = 0

    study(train)
    #t += 1

    try:
        file = open("../neyrons.txt", 'x')
    except FileExistsError:
        file = open("../neyrons.txt", 'w')



    file.write(f"{len(neurons)}\n")

    for i in range(len(neurons) - 1):
        print(i + 1, '/', len(neurons) - 1)
        file.write('\n')
        file.write(f"{neurons[i]} {neurons[i + 1]}\n")

        for j in range(neurons[i + 1]):
            for k in range(neurons[i]):
                file.write(f"{glob_W_s[i][j][k]}\t")
            file.write(f"{glob_B_s[i][j][0]}\n")

    file.close()









    

    

    
    












