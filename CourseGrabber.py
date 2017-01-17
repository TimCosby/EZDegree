from urllib.request import Request
from urllib.request import urlopen
import ast

def auto_put(var, name):

    """
    Puts everything into it's correct format to be sent off to the factory.
    var is the list to read positives from
    name is just what the factory(website) wants it to be read as

    :param var: list of int
    :param name: str
    :return: str
    """

    text = ''
    for thing in range(len(var)):
        if var[thing] == True:
            if name == 'breadth':
                thing = str(thing + 1)

            elif name == 'term':
                if thing == 0:
                    thing = '%22Fall%22'
                elif thing == 1:
                    thing = '%22Winter%22'

            elif name == 'level':
                if thing == 0:
                    thing = '100'
                elif thing == 1:
                    thing = '200'
                elif thing == 2:
                    thing = '300'
                elif thing == 3:
                    thing = '400'

            elif name == 'day':
                if thing == 0:
                    thing = '%22Monday%22'
                elif thing == 1:
                    thing = '%22Tuesday%22'
                elif thing == 2:
                    thing = '%22Wednesday%22'
                elif thing == 3:
                    thing = '%22Thursday%22'
                elif thing == 4:
                    thing = '%22Friday%22'

            else:
                raise Exception('Failed to enter assignment', var, name)

            text += name + ':' + thing + '%20OR%20'


    if len(text) != 0 and text[-5:-3] == 'OR':
        text = text[:-8] + '%20AND%20'

    return text


def make_search(breadth, term, course_level, day, startime, endtime, text_search):
    """
    Search hub WOOOAH

    :param breadth: list of int
    :param department: list of int API NOT WORKING
    :param campus: list of int API NOT WORKING
    :param term: list of int
    :param course_level: list of int
    :param day: list of int
    :param startime: list of int
    :param endtime: list of int
    :return: Nonetype
    """

    search = ''

    search += auto_put(breadth, 'breadth')
    search += auto_put(term, 'term')
    search += auto_put(course_level, 'level')
    search += auto_put(day, 'day')
    if startime != endtime and startime < endtime:
        search += 'start:>=%22' + str(startime) + ':00%22%20AND%20'
        search += 'end:<=%22' + str(endtime) + ':00%22%20AND%20'

    #Returns list of courses
    return ping_search(search[:-9], text_search)

def ping_search(search, text_search):
    """
    Gets a list of courses from cobalt using search's text

    :param search: str
    :return: list of str
    """

    if text_search != '':
        text_search = 'code:%22' + str(text_search) + '%22'
        if search != '':
            text_search = '%20AND%20' + text_search
    else:
        text_search = ''

    page = 'https://cobalt.qas.im/api/1.0/courses/filter?q=' + search + text_search + '&limit=100'

    ###  Replace spaces and quotations with their url counterparts
    page = page.replace('"', '%22').replace(' ', '%20')

    pr = Request(page)
    ### Enters Key
    pr.add_header('Authorization', 'TVwEIjRZP80vhnY8HhM0OzZCMfydh4lA')

    file = urlopen(pr)

    # Convert to readible and get coursename
    lines = file.read().decode('utf-8').split('id":"')

    lines.pop(0)

    for index in range(len(lines)):
        # Puts courses into list
        lines[index] = lines[index][:lines[index].find('"')]

    return list(lines)





if __name__ == '__main__':
    #search = 'code:"CSC"%20AND%20name:"Introduction"%20AND%20level:>100'
    search = 'code:"CSC"'#%20AND%20breadth:5%20OR%20breadth:3%20OR%20division:"engineering"'

    page = 'https://cobalt.qas.im/api/1.0/courses/filter?q=code:"Computer science" AND day:"friday"&limit=100'#' + search
    page = page.replace('"', '%22').replace(' ', '%20')
    pr = Request(page)
    pr.add_header('Authorization', 'TVwEIjRZP80vhnY8HhM0OzZCMfydh4lA')

    file = urlopen(pr)

    lines = file.read().decode('utf-8').split('id":"')

    lines.pop(0)

    for index in range(len(lines)):
        # Puts courses into list
        lines[index] = lines[index][:lines[index].find('"')]

    print(lines)