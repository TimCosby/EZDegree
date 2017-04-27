TAB = '    '


def compile(file, lines):
    final_line = ''
    for line in lines:
        final_line += line.replace(' ', '').replace('\n', '')
    file.write(final_line)


def uncompile(file, line, depth=1):
    line = line[1:-1]
    file.write('[\n')
    while len(line) != 0 and line.find(',') != -1:
        comma = line.find(',')

        if ']' in line[:comma] or ')' in line[:comma]:
            depth -= 1

        file.write(depth*TAB + line[:comma + 1] + '\n')

        if '[' in line[:2] or '(' in line[:2]:
            depth += 1


        line = line[comma + 1:]

    file.write(TAB*(depth-1) + line + '\n')
    file.write(']\n')


if __name__ == '__main__':
    """
    USED TO EASILY SEE WHATS HAPPENING IN COURSE REQUIREMENTS
    """

    FILE_NAME = 'temp_requirements.txt'
    line = open(FILE_NAME).readlines()

    if input('Compile or uncompile?\n').lower() == 'compile':
        compile(open(FILE_NAME, 'w'), line)

    else:
        uncompile(open(FILE_NAME, 'w'), line[0])
