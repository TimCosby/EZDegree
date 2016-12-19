import os
os.chdir(os.path.dirname(os.getcwd()))

DATA = 'source/raw.dat'
COURSE_COUNT = 23 # Maps how many courses are expected to be read(make len(LINE)-2 when done)
CONDITION_COUNT = 5  # Extends the range of conditions counted by 1(prereq, breadth, etc)

file = open(DATA)
LINE = file.readlines()
file.close()

COURSE_NAMES = LINE[0].split(';')
COURSE_CODES = LINE[1].split(';')
COURSE_NAMES[len(COURSE_NAMES)-1] = COURSE_NAMES[len(COURSE_NAMES)-1][:-1]
COURSE_CODES[len(COURSE_CODES)-1] = COURSE_CODES[len(COURSE_CODES)-1][:-1]


def __read_to_raw():
    """
    (NoneType) - > NoneType

    Optimizes data from data.txt by removing the comments and writing into raw.dat
    Run everytime data.txt is updated.
    """

    file = open('source/data.txt')
    #Making raw.dat file
    raw = open(DATA, 'w')

    for line in file:
        #If the first character of a line isn't '#' and if the length of the
        #line is greater than 1; write the line, else skip it
        if line[0] != '#' and len(line) > 1:
            while ('None' in line) == True:
                #Gets rid of the Nones
                block = line.find('None')
                line = line[:block] + line[block+4:]
            raw.write(line)
    file.close()
    raw.close()


def __organize_names():
    """
    (list of str, list of str) -> dict of str

    Puts the names and codes into a dictionary with course_codes being the
    calling keys for the course_names
    """

    dictionary = {}
    for count in range(len(COURSE_NAMES)):
        """if count == len(COURSE_NAMES)-1:
            # If last course name
            dictionary[COURSE_CODES[count-1][:-1]] = COURSE_NAMES[count][:-1]
        else:"""
        dictionary[COURSE_CODES[count]] = COURSE_NAMES[count]
    return dictionary


def __organize_courses(course_blueprint):
    """
    (list of str) -> dict of str

    Organize all the courses per course code massively by formatting rules
    Dictionary key is the course_code (ie 108H1)

    {'Course_Code': [[breadth][prereq][coreq[exclusion][name]]}, {'Course_Code': [breadth][prereq][coreq][exclusion][name], etc}
    >>> str_array = ['ABS', '201Y1[1,3:abc:def:ghi:Introduction to Indigenous Studies: Foundations, History and Politics]', '205H1[2:ABS201Y1:::Indigenous Worldviews, Spiritual and Healing Traditions']
    >>> __organize_courses(str_array)
    {'201Y1': [['1', '3'], ['abc'], ['def'], ['ghi'], ['Introduction to Indigenous Studies: Foundations, History and Politics']], '205H1': [['2'], ['ABS201Y1'], [], [], ['Indigenous Worldviews, Spiritual and Healing Tradition']]}
    """

    dictionary = {}

    for things in range(1, len(course_blueprint)):
        # For course conditions(skips the course_code at the beginning)
        condition_array = [[], [], [], [], []] # If want to add another value add another [] to this
        # [0] = Breadth, [1] = Pre-Reqs, [2] = Exclusions, [3] = Name
        start_index = 6
        # Tells the program where to read the first value from

        for conditions in range(CONDITION_COUNT): # If want to add another value +1 this
            # Loops 5 times for the 5 values
            if course_blueprint[things][start_index] != ':':
                # If value isn't empty
                if conditions != CONDITION_COUNT - 1:
                    # If not on last loop
                    end_index = course_blueprint[things].find(':', start_index)

                    comma_split = course_blueprint[things][start_index:end_index].split(',')
                    # Splits at every comma to see how many inputs are in each value
                    for i in range(len(comma_split)):
                        # For amount of inputs in each value
                        if comma_split[i] != None:
                            # If the value isn't empty
                            condition_array[conditions].append(comma_split[i])


                    #print(condition_array[conditions])
                    #slash_split = course_blueprint[things][start_index:end_index].split('/')
                    #for i in range(len(slash_split))

                    start_index = end_index + 1
                    # Makes the new start_index the old end_index + 1
                else:
                    # If on last loop the end is shown by a ']'
                    end_index = course_blueprint[things].find(']', start_index)
                    condition_array[conditions].append(course_blueprint[things][start_index:end_index])
            else:
                start_index+=1

        # Adds the conditions to the dictionary sorted by the course_code
        # Makes the course_code the key to call the list of conditions
        dictionary[course_blueprint[things][:5]] = condition_array

    return dictionary


def get_all_breadths():
    """
    (NoneType) -> NoneType

    Returns all courses that count for breadth in their respected categories.
    [br1[courses], br2[courses], etc.
    """

    final_breadths = [[], [], [], [], []]

    for total_course in range(COURSE_COUNT):
        # Loop for each course
        course = LINE[2 + total_course].split(';')

        for i in range(1, len(course)):
            # Loop for every given breadth per course
            end = course[i].find(':')
            if end - 1 != '[':
                # Checks to see if the course counts as breadth
                split_breadths = course[i][6:end].split(',')

                #print(split_breadths) #If program ever breaks down use this to find the error in data.txt

                if split_breadths[0] != '':
                    # If breadth category isn't empty
                    for breadths in range(len(split_breadths)):
                        #Adds the course_code to that breadth
                        final_breadths[int(split_breadths[breadths])-1].append(course[0] + course[i][:5])
    return final_breadths


def get_all_courses():
    """
    (NoneType) -> list of str

    Returns all courses
    """
    courses = []
    for i in range(COURSE_COUNT):
        temp = LINE[2 + i].split(';')

        for count in range(1, len(temp)):
            courses.append(temp[0] + temp[count][:5])
    return courses


def get_name_dictionary():
    """
    (NoneType) -> dict of str

     Returns the name dictionary
    """

    return __organize_names()


def get_course_dictionary():
    """
    (NoneType) -> dict of str

    Returns the course dictionary
    Formats every dictionary into [key: [[breadth], [prereq], [coreq], [exclu], [name]], key: etc]
    """

    course_dict = {}

    for i in range(COURSE_COUNT):
        # Run for every course
        course = LINE[2 + i].split(';')
        course_dict[course[0]] = __organize_courses(course)
    return course_dict


if __name__ == '__main__':
    #Reread data.txt and format it into raw.dat everytime file is run manually
    __read_to_raw()