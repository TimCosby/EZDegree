from ast import literal_eval

TEST_PATH = '..\data\\testprograms.txt'
PATH = '..\data\programs.txt'
FINAL_PATH = '..\data\data.dat'


def is_same(string, other):
    """
    For abstract courses (ie. 'CSC4****')

    @param str string: Abstract Course code 
    @param str other: Another Course code
    @return: bool
    """
    try:
        # If the two strings are the same length
        if len(string) - 1 == len(other) if string[-1] == 'X' else len(string) == len(other):

            # If both courses aren't abstract
            if '*' not in other:
                same = True
                # For every index in the course code
                for index in range(len(string) - 1 if string[-1] == 'X' else len(string)):
                    # If the index is not an abstract
                    if string[index] != '*':
                        # If the indexes do not match
                        if string[index] != other[index]:
                            same = False
                            break
                if same:
                    return True
        return False
    except IndexError:
        print('error:', string, other)

def recur(list_, match=None):
    count = 1  # Skip the modifier

    while count != len(list_):
        if isinstance(list_[count], int) or isinstance(list_[count], float):
            # Skips the min value if exists
            pass

        elif isinstance(list_[count], list):
            # If a nested requirement

            temp = recur(list_[count], match=match)  # Go through the nested requirement

            if temp is not None:
                list_[count] = temp

            else:  # If the nested requirement was empty after matching
                list_.pop(count)
                count -= 1

        elif 'ELG' in list_[count]:
            # If a group
            # Get the group code
            tempest = list_[count]
            temp = dict_['ELG'][tempest[tempest.find('[') + 1:tempest.find(']')]]

            temper = recur(temp, match=list_[count][tempest.find(']') + 1:])  # Go through the group, only pulling out whatever matches

            list_.pop(count)  # Get rid of the original value

            for i in range(len(temper)):
                list_.insert(count, temper[i])  # Put in everything matching from the group in the requirement
                count += 1
            count -= 1

        elif match is not None:
            # If needs to look for specific codes
            if not is_same(match, list_[count]):  # If the code does not match remove it
                list_.pop(count)
                count -= 1

        count += 1

    if len(list_) == 2 and (isinstance(list_[-1], int) or isinstance(list_[-1], float)):  # If just contains the modifier and limit
        print(list_[0], 'did1')
        return None

    elif len(list_) == 3 and (isinstance(list_[-2], int) or isinstance(list_[-2], float)):  # If just contains the modifer and min&max limits
        print(list_[0], 'did2', list_[-2])
        return None

    else:
        return list_

if 'y' in input('Test y/n\n').lower():
    file = open(TEST_PATH).readlines()
    test = True
else:
    file = open(PATH).readlines()
    test = False

dict_ = {}

temp = ''

for line in file:
    if line[0] == '@':  # If a comment
        pass

    elif line[0] != '{':
        temp += line.replace('\n', '').replace('	', '')

    else:  # If not a comment, add to the dictionary
        if temp != '':
            dict_.update(literal_eval(temp))

        temp = line.replace('\n', '')

for program in dict_:
    if program != 'ELG':  # If not a group
        recur(dict_[program]['requirements'])

        if not test and not isinstance(dict_[program]['requirements'][-1], int) and not isinstance(dict_[program]['requirements'][-1], float):
            dict_[program]['requirements'].append(len(dict_[program]['requirements']) - 1)  # Add the needed amount to be passed

try:
    dict_.pop('ELG')  # Get rid of groups
except KeyError:
    pass

new_file = open(FINAL_PATH, 'w')
new_file.write(str(dict_))
new_file.close()
