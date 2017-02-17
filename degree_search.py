import ast
file = open('test.txt')

lines = {}

for x in range(5):
    lines.update(ast.literal_eval(file.readline()))

file.close()

def search(key_word, all=False, name=False, id=False, type=False, desc=False,
           fce=False, br1=False, br2=False, br3=False, br4=False):
    """
    Search through all records for key_word in selected bool(s)

    @param str key_word:
    @param bool all:
    @param bool name:
    @param bool id:
    @param bool type:
    @param bool desc:
    @param bool fce:
    @param bool br1:
    @param bool br2:
    @param bool br3:
    @param bool br4:
    @return: list of str
    """

    if isinstance(key_word, str):
        result = set([])

        keys = lines.keys()

        if all or name:
            for key in keys:
                if key_word.lower() in get_req(key, name=True).lower():
                    result.add(key)
        if all or id:
            for key in keys:
                if key_word.lower() in get_req(key, id=True).lower():
                    result.add(key)
        if all or type:
            for key in keys:
                if key_word.lower() in get_req(key, type=True).lower():
                    result.add(key)
        if all or desc:
            for key in keys:
                if key_word.lower() in get_req(key, desc=True).lower():
                    result.add(key)
        if all or fce:
            for key in keys:  # Make it breadth1 etc
                if 'breadth' in key_word.lower():
                    i = key_word.lower().count('breadth')
                    for breadth in range(i):
                        pass
                        #go ot index of breadth and find a number after it
                        #if theres a letter before a number then return all breadths
        if all or br1:
            for key in keys:
                if key_word.lower() in get_req(key, br1=True).lower():
                    result.add(key)
        if all or br2:
            for key in keys:
                if key_word.lower() in get_req(key, br2=True).lower():
                    result.add(key)
        if all or br3:
            for key in keys:
                if key_word.lower() in get_req(key, br3=True).lower():
                    result.add(key)
        if all or br4:
            for key in keys:
                if key_word.lower() in get_req(key, br4=True).lower():
                    result.add(key)

        return list(result)
    else:
        raise Exception('Invalid keyword!')

def get_req(program, name=True, id=False, type=False, desc=False, fce=False,
            br1=False, br2=False, br3=False, br4=False):
    """
    Get values for a single key

    @param str program:
    @param bool name:
    @param bool id:
    @param bool type:
    @param bool desc:
    @param bool fce:
    @param bool br1:
    @param bool br2:
    @param bool br3:
    @param bool br4:
    @return: str | list of str | list of bool
    """

    key = ''
    if name == True:
        key += 'Name'
    if id == True:
        key += 'ID'
    if type == True:
        key += 'Type'
    if desc == True:
        key += 'Description'
    if fce == True:
        key += 'FCE'
    if br1 == True:
        key += '1'
    if br2 == True:
        key += '2'
    if br3 == True:
        key += '3'
    if br4 == True:
        key += '4'

    if key == '':
        raise Exception('Insufficient inputs!')
    elif key in lines[program].keys():
        return lines[program][key]
    else:
        raise Exception('You may only have one input!')


if __name__ == '__main__':
    program = 'Astronomy & Astrophysics Major'
    #result = get_req(program, type=True)
    result = search('Astro', name=True)

    print(result)
