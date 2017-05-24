from Course import is_same
from ast import literal_eval


def recur(requirements, special, destroy=None):
    index = 0
    while index < len(requirements):
        if isinstance(requirements[index], int) or isinstance(requirements[index], float) or 'PASS' in requirements[index] or 'CREDITS' in requirements[index] or 'MARK' in requirements[index]:
            pass

        elif isinstance(requirements[index], list):
            requirements[index] = recur(requirements[index], special, destroy=destroy)
            if len(requirements[index]) == 2:
                requirements.pop(index)
                index -= 1

        elif destroy is not None:
            if not is_same(destroy, requirements[index]):
                requirements.pop(index)
                index -= 1

        elif 'ELG' in requirements[index]:
            requirements[index] = recur(special['ELG'][requirements[index][4:7]], special, destroy=requirements[index][8:])
            requirements[index].append(len(requirements[index]) - 1)

        index += 1

    return requirements

lines = open('programs.txt').readlines()

#special = literal_eval(lines[1])

final = {}

for line in lines[2:]:
    if line != '' and '@' not in line:
        print(line)
        final.update(literal_eval(line))

for program in final:
    #recur(final[program]['requirements'], special)
    final[program]['requirements'].append(len(final[program]['requirements']) - 1)

from os.path import join
from os import pardir
open(join(pardir, 'data\\data.dat'), 'w').write(str(final))