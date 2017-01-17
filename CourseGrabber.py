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

    lista = ["ABS", "USA", "ANA", "ANT", "FAH", "ARH", "AST", "BCH", "CTA", "CSB", "CHM", "CIN", "CLA", "COL", "CSC", "EDU", "CAS", "CRI", "DTS", "DRM", "ESS", "EAS", "EEB", "ECO", "IRE", "ENG", "ENV", "ETH", "EUR", "FOR", "FRE", "GGR", "GER", "HIS", "HPS", "HMB", "IMM", "IMC", "INI", "ITA", "CJS", "LMP", "LAS", "LIN", "MAT", "MST", "MGY", "MUS", "NMC", "NEW", "NFS", "PCJ", "PHC", "PCL", "PHL", "PHY", "PSL", "POL", "PSY", "PPG", "RLG", "RSM", "SDS", "SLA", "SOC", "SAS", "SPA", "SMC", "STA", "TRN", "UNI", "VIC", "WGS", "WDW"]
    listb = ["Aboriginal Studies", "American Studies", "Anatomy", "Anthropology", "Art", "Archaeology", "Astronomy and Astrophysics", "Biochemistry", "Canadian Institute for Theoretical Astrophysics", "Cell and Systems Biology", "Chemistry", "Cinema Studies", "Classics", "Comparative Literature", "Computer Science", "Concurrent Teacher Education Program", "Contemporary Asian Studies", "Criminology and Sociolegal Studies", "Diaspora and Transnational Studies", "Drama, Theatre and Performance Studies", "Earth Sciences", "East Asian Studies", "Ecology & Evolutionary Biology", "Economics", "Employment Relations, Centre for Industrial Relations and Human Resources", "English", "Environment, School of", "Ethics, Centre for", "European Studies", "Forestry", "French", "Geography", "German", "History", "History and Philosophy of Science and Technology", "Human Biology", "Immunology", "Impact Centre", "Innis College", "Italian", "Jewish Studies", "Laboratory Medicine and Pathobiology", "Latin American Studies", "Linguistics", "Mathematics", "Medieval Studies, Centre for", "Molecular Genetics and Microbiology", "Music", "Near & Middle Eastern Civilizations", "New College", "Nutritional Science", "Peace, Conflict and Justice Studies", "Pharmaceutical Chemistry", "Pharmacology", "Philosophy", "Physics", "Physiology", "Political Science", "Psychology", "Public Policy", "Religious Studies", "Rotman Commerce", "Sexual Diversity Studies, Mark S. Bonham Centre", "Slavic Languages and Literature", "Sociology", "South Asian Studies", "Spanish", "St. Michaels College", "Statistical Sciences", "Trinity College", "University College", "Victoria College", "Women and Gender Studies", "Woodsworth College"]

    #Returns list of courses
    return ping_search(search[:-9], text_search)

def ping_search(search, text_search):
    """
    Gets a list of courses from cobalt using search's text

    :param search: str
    :return: list of str
    """

    if text_search != '':
        if len(text_search) == 3:
            text_search = 'code:%22' + text_search + '%22'
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

    page = 'https://cobalt.qas.im/api/1.0/courses/filter?q=code:"CSC"&limit=100'#' + search
    page = page.replace('"', '%22').replace(' ', '%20')
    pr = Request(page)
    pr.add_header('Authorization', 'TVwEIjRZP80vhnY8HhM0OzZCMfydh4lA')

    file1 = urlopen(pr)

    page = 'https://cobalt.qas.im/api/1.0/courses/search?q="COMPUTER"&limit=100'
    page = page.replace('"', '%22').replace(' ', '%20')
    pr = Request(page)
    pr.add_header('Authorization', 'TVwEIjRZP80vhnY8HhM0OzZCMfydh4lA')

    file2 = urlopen(pr)

    lines1 = file1.read().decode('utf-8').split('id":"')
    lines2 = file2.read().decode('utf-8').split('id":"')

    lines1.pop(0)
    lines2.pop(0)

    for index in range(len(lines1)):
        # Puts courses into list
        lines1[index] = lines1[index][:lines1[index].find('"')]

    for index in range(len(lines2)):
        # Puts courses into list
        lines2[index] = lines2[index][:lines2[index].find('"')]

    setf = list(set(lines1).intersection(lines2))

    print(setf)