from Requirement import Requirement
from Course import Courses
from ast import literal_eval
from openpyxl import load_workbook
from Authentication import authenticate

'''
TODO:
1. Make a file to convert ELGs

2. Expand on User

3. Load in all the programs
'''

DEFAULT_PROGRAMS = {}
FILE_NAME = 'database.xlsx'
PAGE = 'https://cobalt.qas.im/api/1.0/courses/filter?q=code:%22'
KEY = 'TVwEIjRZP80vhnY8HhM0OzZCMfydh4lA'
WORKBOOK = load_workbook(FILE_NAME)
WORKSHEET = WORKBOOK.active
USERS = {}


def get_user_lines():
    cell = 0
    row = 2

    while cell is not None:
        cell = WORKSHEET.cell(column=1, row=row).value

        USERS[cell] = row
        row += 1


def initial_setup():
    file = open('programs.txt').readlines()
    for line in file:
        if line[0] == '@':
            pass
        else:
            DEFAULT_PROGRAMS.update(literal_eval(line))

    for program in DEFAULT_PROGRAMS:
        DEFAULT_PROGRAMS[program]['requirements'].append(len(DEFAULT_PROGRAMS[program]['requirements']) - 1)
        #DEFAULT_PROGRAMS[program]['requirements'] = convert_to_obj(DEFAULT_PROGRAMS[program]['requirements'])

    get_user_lines()

initial_setup()


class User:
    def __init__(self, username, password):
        if not authenticate(username, password, USERS, WORKBOOK, WORKSHEET):
            self.logged_in = False
        else:
            self.logged_in = True
            self.username = username

            self._courses = Courses()
            self._taken_courses = {}
            self._programs = {}

    def add_course(self, course_code):
        # Collective courses
        self._courses.add_course(course_code)

        # Local courses
        self._taken_courses[course_code] = self._courses.course_cache[course_code]

        # Database courses
        WORKSHEET.cell(column=2, row=USERS[self.username], value=str([[course.course_code, course.type, course.mark] for course in self._taken_courses.values()]))
        WORKBOOK.save(FILE_NAME)

    def remove_course(self, course_code):
        # Collective courses
        self._courses.remove_course(course_code)

        # Local courses
        self._taken_courses.pop(course_code)

        # Database courses
        WORKSHEET.cell(column=2, row=USERS[self.username], value=[[course.course_code, course.type, course.mark] for course in self._taken_courses.values()])
        WORKBOOK.save(FILE_NAME)

    def set_mark(self, course_code, mark):
        try:
            self._courses.change_mark(course_code, mark)

            WORKSHEET.cell(column=2, row=USERS[self.username], value=str([[course.course_code, course.type, course.mark] for course in self._taken_courses.values()]))
            WORKBOOK.save(FILE_NAME)
        except KeyError:
            print('Course does not exist!')

    def set_type(self, course_code, type):
        try:
            self._courses.change_type(course_code, type)

            WORKSHEET.cell(column=2, row=USERS[self.username], value=str([[course.course_code, course.type, course.mark] for course in self._taken_courses.values()]))
            WORKBOOK.save(FILE_NAME)
        except KeyError:
            print('Course does not exist!')

    def add_program(self, program_code):
        self._programs[program_code] = DEFAULT_PROGRAMS[program_code]
        self._programs[program_code]['requirements'] = convert_to_requirement(DEFAULT_PROGRAMS[program_code]['requirements'], self._courses)

        WORKSHEET.cell(column=3, row=USERS[self.username], value=str(list(self._programs.keys())))
        WORKBOOK.save(FILE_NAME)

    def remove_program(self, program_code):
        self._programs.pop(program_code)

        WORKSHEET.cell(column=3, row=USERS[self.username], value=str(list(self._programs.keys())))
        WORKBOOK.save(FILE_NAME)

    def get_program_requirements(self, program_code):
        return self._programs[program_code]['requirements']


def convert_to_requirement(requirements, courses, exclusions=None):
    """
    Converts each course code into a Course object then the entire requirement
    into a Requirement object while storing all the courses in course_cache

    @param list of str|list requirements: 
    @param Courses courses: Courses object
    @param dict|None exclusions:
    @return: Requirement
    """

    transformed_requirements = []

    if isinstance(requirements[1], tuple):
        start = 2
        if exclusions is None:
            exclusions = requirements[1]
        else:
            exclusions += requirements[1]
    else:
        start = 1
        exclusions = ()

    for item in range(start, len(requirements[1:])):
        # Loop through requirements[start:-1] starting at index 1, ending at -1
        if isinstance(requirements[item], list):
            # If a nested list
            transformed_requirements.append(convert_to_requirement(requirements[item], courses, exclusions=exclusions))  # Give child the same exclusions

        elif requirements[item] in exclusions:
            pass

        elif requirements[item] not in courses.course_cache:
            # If a course code that has not yet been cached
            courses.add_course(requirements[item], exclusions=exclusions)
            courses.course_cache[requirements[item]] = courses.course_cache[requirements[item]]
            transformed_requirements.append(courses.course_cache[requirements[item]])

        else:
            # If course is already cached
            transformed_requirements.append(courses.course_cache[requirements[item]])

    # Turn into a Requirement object
    return Requirement(requirements[0], float(requirements[-1]), transformed_requirements, exclusions=exclusions)


if __name__ == '__main__':

    while True:
        usr = User(input('Username: ').lower(), input('Password: '))

        if usr.logged_in:
            break
        else:
            del usr

    usr.add_program('ASSPE1689')
    usr.add_course('CSC148H1')
    print(usr.get_program_requirements('ASSPE1689'))