from Requirement import Requirement
from Course import Courses
from ast import literal_eval
from openpyxl import load_workbook
from Authentication import authenticate
from copy import deepcopy

'''
TODO:
1. Make a file to convert ELGs

2. Expand on User

3. Load in all the programs
'''

PROGRAM_FILE = 'data\data.dat'  #'data\\testprograms.txt'
DEFAULT_PROGRAMS = literal_eval(open(PROGRAM_FILE).readline())
FILE_NAME = 'data\\database.xlsx'
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

get_user_lines()


class User:
    """
    A unique-user interactive interface
    
    Public Attributes:
    =================
        @param str username: 
            User's username
    
    Private Attributes:
    ==================
        @param bool _logged_in: 
            Whether or not the user successfully logged in
        @param Courses _courses:
            A Courses object containing all functions towards courses
        @param dict _taken_courses:
            A dictionary of Course objects that the user has added
        @param dict _programs:
            A dictionary of program codes that the user has added
    """
    def __init__(self, username, password):
        if not authenticate(username.lower(), password, USERS, WORKBOOK, WORKSHEET):
            self._logged_in = False
        else:
            self._logged_in = True
            self.username = username.lower()

            self._courses = Courses()
            self._taken_courses = {}
            self._programs = {}

            self.initial_courses()
            self.initial_programs()

    def logged_in(self):
        return self._logged_in

    def get_easiest(self):
        values = {'percentage': [], 'completed': []}
        for program in DEFAULT_PROGRAMS:
            temp = self.convert_to_requirement(deepcopy(DEFAULT_PROGRAMS[program]['requirements']))

            percentage = (temp.have / temp.need if temp.need != 0 else 1) * 100  # testing
            completed = temp.need - temp.have

            values['percentage'].append([DEFAULT_PROGRAMS[program]['name'], percentage])
            values['completed'].append([DEFAULT_PROGRAMS[program]['name'], completed])

        values['percentage'].sort(key=lambda x: x[1])
        values['completed'] = sorted(values['completed'], reverse=False, key=lambda x: x[1])
        return values

    def get_courses(self):
        return self._taken_courses

    def get_course(self, course_code):
        return self._taken_courses[course_code]

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

    def get_mark(self, course_code):
        return self._taken_courses[course_code].mark

    def set_mark(self, course_code, mark):
        try:
            self._courses.change_mark(course_code, mark)

            WORKSHEET.cell(column=2, row=USERS[self.username], value=str([[course.course_code, course.type, course.mark] for course in self._taken_courses.values()]))
            WORKBOOK.save(FILE_NAME)
        except KeyError:
            print('Course does not exist!')

    def get_type(self, course_code):
        return self._taken_courses[course_code].type

    def set_type(self, course_code, type):
        try:
            if type == 'Completed' and self._taken_courses[course_code] < 50:
                type = 'Failed'

            self._courses.change_type(course_code, type)

            WORKSHEET.cell(column=2, row=USERS[self.username], value=str([[course.course_code, course.type, course.mark] for course in self._taken_courses.values()]))
            WORKBOOK.save(FILE_NAME)
        except KeyError:
            print('Course does not exist!')

    def get_cgpa(self):
        total = 0
        credits = 0

        for course in self._taken_courses:
            if course.type != 'Dropped':
                # If the course wasn't dropped

                mark = course.mark
                if mark > 84:
                    grade_point = 4.0
                elif mark > 79:
                    grade_point = 3.7
                elif mark > 76:
                    grade_point = 3.3
                elif mark > 72:
                    grade_point = 3.0
                elif mark > 69:
                    grade_point = 2.7
                elif mark > 66:
                    grade_point = 2.3
                elif mark > 62:
                    grade_point = 2.0
                elif mark > 59:
                    grade_point = 1.7
                elif mark > 56:
                    grade_point = 1.3
                elif mark > 52:
                    grade_point = 1.0
                elif mark > 49:
                    grade_point = 0.7
                else:
                    grade_point = 0

                if course.weight == 1:
                    total += 1 * grade_point
                    credits += 1
                else:
                    total += .5 * grade_point
                    credits += .5

        if total != 0:
            return total / credits
        return 0.0

    def add_program(self, program_code):
        if program_code not in self._programs:
            program = deepcopy(DEFAULT_PROGRAMS[program_code])
            self._programs[program_code] = program
            self._programs[program_code]['requirements'] = convert_to_requirement(program['requirements'], self._courses)

            WORKSHEET.cell(column=3, row=USERS[self.username], value=str(list(self._programs.keys())))
            WORKBOOK.save(FILE_NAME)
        else:
            print('Program already added!')

    def get_programs(self):
        return self._programs

    def get_program(self, program_code):
        return self._programs[program_code]

    def remove_program(self, program_code):
        try:
            self._programs.pop(program_code)
        except KeyError:
            print('Program does not exist!')

        WORKSHEET.cell(column=3, row=USERS[self.username], value=str(list(self._programs.keys())))
        WORKBOOK.save(FILE_NAME)

    def get_program_requirements(self, program_code):
        temp = self.convert_to_requirement(deepcopy(DEFAULT_PROGRAMS[program_code]['requirements']))
        temp.have
        return temp

    def initial_courses(self):
        for course_info in literal_eval(WORKSHEET.cell(column=2, row=USERS[self.username]).value):
            self.add_course(course_info[0])
            self.set_type(course_info[0], course_info[1])
            self.set_mark(course_info[0], course_info[2])

    def initial_programs(self):
        for program_code in literal_eval(WORKSHEET.cell(column=3, row=USERS[self.username]).value):
            self.add_program(program_code)

    def convert_to_requirement(self, requirements, exclusions=None, treatall=False, only_used=False, only_unused=False):
        modifier = requirements[0]
        max = requirements[-1]
        min = None
        start_index = 1
        end_index = len(requirements) - 1
        exclusions = set([]) if exclusions is None else exclusions

        if modifier != 'MARK':
            transformed_requirements = []

            if isinstance(requirements[-2], int) or isinstance(requirements[-2], float):
                end_index -= 1
                min = requirements[-2]

            if modifier[0] == 'X':
                only_used = True

            elif modifier[-1] == 'X':
                only_unused = True

            if isinstance(requirements[start_index], tuple):
                for item in requirements[start_index]:
                    if item not in self._courses.course_cache:
                        self._courses.add_course(item)
                    exclusions.add(self._courses.course_cache[item])
                start_index += 1

            if treatall is False and requirements[start_index] == 'TREATALL':
                treatall = True
                start_index += 1

            for index in range(start_index, end_index):
                if isinstance(requirements[index], list):
                    # If a nested requirement
                    transformed_requirements.append(self.convert_to_requirement(requirements[index], exclusions, treatall, only_used, only_unused))

                elif requirements[index] not in self._courses.course_cache:
                    # If a course
                    self._courses.add_course(requirements[index])
                    transformed_requirements.append(self._courses.course_cache[requirements[index]])

                else:
                    transformed_requirements.append(self._courses.course_cache[requirements[index]])

        else:
            self._courses.add_course(requirements[1])
            transformed_requirements = self._courses.course_cache[requirements[1]]

        return Requirement(modifier, min, max, transformed_requirements, exclusions, treatall, only_used, only_unused)


if __name__ == '__main__':

    while True:
        usr = User(input('Username: ').lower(), input('Password: '))

        if usr.logged_in():
            print('Logged in')
            break
        else:
            del usr

    print(usr.get_program_requirements('ASSPE1478'))
