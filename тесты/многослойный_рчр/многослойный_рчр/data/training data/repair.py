file = open("прич.txt", 'r')
line = file.readline()
file.close()
line = line.replace(' ', '\n')

file = open("прич.txt", 'w')
file.write(line)
file.close()
