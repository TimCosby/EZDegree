file = open('temp.txt').readlines()
output = open('output.txt', 'w')

for line in file:
    line = "'" + line.replace(';', ',')
    start = 0

    while line.find(',', start) != -1:
        temp = line.find(',', start)
        line = line[:temp] + "'" + line[temp:]

        try:
            line = line[:temp + 3] + "'" + line[temp + 3:]
        except IndexError:
            pass
        start = temp + 2

    output.write(line)