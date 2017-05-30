from Requirement import Requirement
from Course import Courses
from ast import literal_eval
from openpyxl import load_workbook
from Authentication import authenticate
from copy import deepcopy
from copy import copy

'''
TODO:
1. PORT INTO ANOTHER LANGUAGE BECAUSE PYTHON SUCKS AT MULTITASKING
    a) Multi-thread
    b) Prioritize taken programs

2. Load in all the programs
    a) Hell on earth
    
3. Make it so that when a new course is added all ABSTRACT courses are gone through and add it to their special list of some sort

4. Make it so that there is a breadth counter
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
        @param list _taken_courses:
            A list of Course objects that the user has added
        @param list _taken_programs:
            A list of program codes that the user has added
        @param dict _program_requirement_cache:
            A dictionary of Requirement objects for their respective programs
    """
    def __init__(self, username, password):
        if not authenticate(username.lower(), password, USERS, WORKBOOK, WORKSHEET):
            self._logged_in = False
        else:
            self._logged_in = True
            self.username = username.lower()

            self._courses = Courses()
            self._taken_courses = []
            self._taken_programs = []
            self._program_requirement_cache = {}

            self.initial_courses()
            self.initial_programs()
            self.initial_program_cache()

    def logged_in(self):
        """
        Return if the user is logged in or not

        :return: bool
        """

        return self._logged_in

    def _update_requirements(self):
        """
        Update all program requirement objects

        :return: None
        """

        for requirement in self._program_requirement_cache:
            self._program_requirement_cache[requirement].update

    # ============= ADD METHODS ================== #

    def add_program(self, program_code):
        """
        Add <program_code> to the user's taken programs

        :param str program_code: Program code to add
        :return: None
        """

        if program_code not in self._taken_programs:
            WORKSHEET.cell(column=3, row=USERS[self.username], value=str(self._taken_programs))
            WORKBOOK.save(FILE_NAME)

        else:
            print('Program already added!')

    def add_course(self, course_code, initial=False):
        """
        Add <course_code> to the user's taken courses

        :param str course_code: Course to add
        :param bool initial: If doing the initial startup - don't bother updating all the requirements since they aren't made yet
        :return: None
        """

        # Collective courses
        self._courses.add_course(course_code)

        # Local courses
        self._taken_courses.append(course_code)

        # Database courses
        WORKSHEET.cell(column=2, row=USERS[self.username], value=str([[course_code, self._courses.get_type(course_code), self._courses.get_mark(course_code)] for course_code in self._taken_courses]))
        WORKBOOK.save(FILE_NAME)
        if not initial:
            self._update_requirements()

    # ============= REMOVE METHODS ================== #

    def remove_program(self, program_code):
        """
        Remove <program_code> from user's taken programs

        :param str program_code: Program to remove
        :return: None
        """

        try:
            self._taken_programs.remove(program_code)

            WORKSHEET.cell(column=3, row=USERS[self.username], value=str(self._taken_programs))
            WORKBOOK.save(FILE_NAME)

        except KeyError:
            print('Program does not exist!')

    def remove_course(self, course_code):
        """
        Remove <course_code> from user's taken courses

        :param str course_code: Course to remove
        :return: None
        """

        try:
            # Collective courses
            self._courses.remove_course(course_code)

            # Local courses
            self._taken_courses.remove(course_code)

            # Database courses
            WORKSHEET.cell(column=2, row=USERS[self.username], value=str([[course_code, self._courses.get_type(course_code), self._courses.get_mark(course_code)] for course_code in self._taken_courses]))
            WORKBOOK.save(FILE_NAME)
            self._update_requirements()

        except Exception:
            pass

    # ============= GET METHODS ================== #

    def get_programs(self):
        """
        Return program names

        :return: list of str
        """

        return self._taken_programs

    def get_program(self, program_code):
        """
        Return <program_code>'s program information

        :param str program_code: Program to get information from
        :return: dict of str
        """

        temp = copy(DEFAULT_PROGRAMS[program_code])
        temp.pop('requirements')
        return temp

    def get_program_requirements(self, program_code):
        """
        Return Requirement for <program_code>

        :param str program_code: Program to get requirements for
        :return: Requirement
        """

        return self._program_requirement_cache[program_code]

    def get_courses(self):
        """
        Return a list of all courses the user is taking

        :return: list of str
        """
        return self._taken_courses

    def get_course(self, course_code):
        """
        Return <course_code>'s course object

        :param str course_code: Course data is desired of
        :return: Course
        """

        return self._courses.course_cache[course_code]

    def get_mark(self, course_code):
        """
        Return mark for <course_code>

        :param str course_code: Course desired mark is in
        :return: float
        """

        return self._taken_courses[course_code].mark

    def get_type(self, course_code):
        """
        Return type for <course_code>

        :param str course_code: Course desired type is in
        :return: str
        """

        return self._taken_courses[course_code].type

    def get_easiest(self):
        """
        Return a list of easiest to get programs by percentage and courses needed

        :return: dict of list
        """

        values = {'percentage': [], 'to_finish': []}

        for program in self._program_requirement_cache:  # For every program
            shortened = self._program_requirement_cache[program]

            percentage = (shortened.have / shortened.need if shortened.need != 0 else 1) * 100  # Get percentage completed
            to_finish = shortened.need - shortened.have  # Get amount of requirements needed to finish

            values['percentage'].append([DEFAULT_PROGRAMS[program]['name'], percentage])
            values['to_finish'].append([DEFAULT_PROGRAMS[program]['name'], to_finish])

        values['percentage'].sort(key=lambda x: x[1])  # Sort from Highest -> Lowest
        values['to_finish'] = sorted(values['to_finish'], reverse=False, key=lambda x: x[1])  # Sort from Least -> Most

        return values

    def get_cgpa(self):
        """
        Return current grade point average from courses taken

        :return: float
        """

        total = 0
        credits = 0

        for course in self._taken_courses:
            course = self._courses.course_cache[course]
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

    # ============= SET METHODS ================== #

    def set_mark(self, course_code, mark):
        """
        Set the mark of <course_code> to <mark>

        :param str course_code: Course to change
        :param float mark: Mark of course
        :return: None
        """

        try:
            self._courses.change_mark(course_code, mark)

            WORKSHEET.cell(column=2, row=USERS[self.username], value=str([[course_code, self._courses.get_type(course_code), self._courses.get_mark(course_code)] for course_code in self._taken_courses]))
            WORKBOOK.save(FILE_NAME)
            self._update_requirements()

        except KeyError:
            print('Course does not exist!')

    def set_type(self, course_code, type):
        """
        Set the type of <course_code> to <type>

        :param str course_code: Course to change
        :param str type: Type of course
        :return: None
        """

        try:
            if type == 'Completed' and self._taken_courses[course_code] < 50:
                type = 'Failed'

            self._courses.change_type(course_code, type)

            WORKSHEET.cell(column=2, row=USERS[self.username], value=str([[course_code, self._courses.get_type(course_code), self._courses.get_mark(course_code)] for course_code in self._taken_courses]))
            WORKBOOK.save(FILE_NAME)
            self._update_requirements()

        except KeyError:
            print('Course does not exist!')

    # ============= INITIAL OBJECT METHODS ================== #

    def initial_courses(self):
        """
        Add all pre-existing user programs

        :return: None
        """
        for course_info in literal_eval(WORKSHEET.cell(column=2, row=USERS[self.username]).value):
            self.add_course(course_info[0], initial=True)
            self.set_type(course_info[0], course_info[1])
            self.set_mark(course_info[0], course_info[2])

    def initial_programs(self):
        """
        Add all pre-existing user programs

        :return: None
        """

        for program_code in literal_eval(WORKSHEET.cell(column=3, row=USERS[self.username]).value):
            self.add_program(program_code)

    def initial_program_cache(self):
        """
        Convert all the pre-existing user data into requirement objects

        :return: None
        """
        for program in DEFAULT_PROGRAMS:
            self._program_requirement_cache[program] = self.convert_to_requirement(deepcopy(DEFAULT_PROGRAMS[program]['requirements']))
        self._update_requirements()

    def convert_to_requirement(self, requirements, exclusions=None, treatall=False, only_used=False, only_unused=False):
        """
        Converts data into an requirement object

        :param list of str requirements: Courses that are needed for the program
        :param list of str|None exclusions: Courses that cannot be used for this part of the requirement
        :param bool treatall: If all courses are being looked through and marked as used
        :param bool only_used: If only courses that have previously been used are being used
        :param bool only_unused: If only courses that have previously not been used are being used
        :return: Requirement
        """

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
            if requirements[1] not in self._courses.course_cache:
                self._courses.add_course(requirements[1])

            transformed_requirements = self._courses.course_cache[requirements[1]]

        return Requirement(modifier, min, max, transformed_requirements, exclusions, treatall, only_used, only_unused)


if __name__ == '__main__':
    import time

    start = time.time()
    while True:
        start = time.time()
        usr = User(input('Username: ').lower(), input('Password: '))

        if usr.logged_in():
            print('Startup Time:', time.time() - start, 'seconds')
            print('Logged in')
            break
        else:
            print('Incorrect login!\n')
            del usr

    start = time.time()

    print(usr.get_program_requirements('ASSPE0115'))

    usr.remove_course('MAT223H1')

    print('Update Time:', time.time() - start, 'seconds')

    start = time.time()

    print(usr.get_easiest())

    print('Get easiest time:', time.time() - start, 'seconds')
