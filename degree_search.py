import ast
file = open('programs.txt')
lines = {}
for x in range(5):
    lines.update(ast.literal_eval(file.readline()))
file.close()

def search(key_word, all=False, name=False, id=False, type=False, desc=False):
    """
    Search through all records for key_word in selected categorie(s)

    @param str key_word:
    @param bool all:
    @param bool name:
    @param bool id:
    @param bool type:
    @param bool desc:
    @return: list of str

    >>> search('astro major', name=True, type=True)
    ['Astronomy & Astrophysics Major']
    """

    if isinstance(key_word, str):
        result = set([])
        name_set = set([])
        id_set = set([])
        type_set = set([])
        desc_set = set([])

        keys = lines.keys()

        for key in keys:
            for word in key_word.split():
                if all or name:
                    if word.lower() in get_req(key, name=True).lower():
                        name_set.add(key)
                if all or id:
                    if word.lower() in get_req(key, id=True).lower():
                        id_set.add(key)
                if all or type:
                    if word.lower() in get_req(key, type=True).lower():
                        type_set.add(key)
                if all or desc:
                    if word.lower() in get_req(key, desc=True).lower():
                        desc_set.add(key)

        # Only have the same outputs
        #print(name_set, id_set, type_set, desc_set)
        if name or all:
            result = result.union(name_set)
        if id or all:
            if len(result) == 0:
                result = result.union(id_set)
            else:
                result = result.intersection(id_set)
        if type or all:
            if len(result) == 0:
                result = result.union(type_set)
            else:
                result = result.intersection(type_set)
        if desc_set or all:
            if len(result) == 0:
                result = result.union(desc_set)
            else:
                result = result.intersection(desc_set)

        # Combine all outputs
        return list(result)
    else:
        raise Exception('Invalid keyword!')

def get_req(program, name=False, id=False, type=False, desc=False, fce=False,
            yr1=False, yr2=False, yr3=False, yr4=False):
    """
    Get specific requirements for a specific program offered

    @param str program:
    @param bool name:
    @param bool id:
    @param bool type:
    @param bool desc:
    @param bool fce:
    @param bool yr1:
    @param bool yr2:
    @param bool yr3:
    @param bool yr4:
    @return: str | list of str | list of bool
    """

    key = []
    if name == True:
        key.append('Name')
    if id == True:
        key.append('ID')
    if type == True:
        key.append('Type')
    if desc == True:
        key.append('Description')
    if fce == True:
        key.append('FCE')
    if yr1 == True:
        key.append('1')
    if yr2 == True:
        key.append('2')
    if yr3 == True:
        key.append('3')
    if yr4 == True:
        key.append('4')

    if key == []:
        raise Exception('Insufficient inputs!')
    elif len(key) == 1:
        return lines[program][key[0]]
    else:
        raise Exception('You may only have one input!')


if __name__ == '__main__':
    program = 'Astronomy & Astrophysics Minor'
    result = get_req(program, type=True)
    #result = search('astro minor', name=True, type=True)

    print(result)
