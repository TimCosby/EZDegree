from openpyxl import load_workbook
from openpyxl import Workbook
import ast
import degree_search
from urllib.request import Request
from urllib.request import urlopen
from urllib.request import HTTPError
from Course import Course

#Shatter Sort
#Radix Sort
FILE_NAME = 'database.xlsx'
PAGE = 'https://cobalt.qas.im/api/1.0/courses/'
KEY = 'TVwEIjRZP80vhnY8HhM0OzZCMfydh4lA'


class User:
    """
    Private Attributes:
    ==================
        @param Workbook _wb: 
                    Database workbook
        
        @param Worksheet _ws:
                    Database's worksheet
                    
        @param bool _logged_in:
                    Return if user is logged in
                    
        @param int _user_row:
                    Row that the user is located in worksheet
                    
        @param dict _course_list:
                    List of all courses user has taken
                    
    Public Attributes:
    =================
        @param str username:
                    User's name
    """

    def __init__(self, username, password):
        """
        User's Profile
        
        @param str username: 
        @param str password: 
        """

        self._wb = load_workbook(FILE_NAME)
        self._ws = self._wb.active

        self.username = username.lower().split(' ')[0]
        self._logged_in = False

        # Find if the user is already in the system
        if not self._find_user():
            # If registering as a new user
            if 'y' in input('Do you want to register as a new user? Y/N?\n').lower():
                self._ws.cell(column=1, row=self._user_row, value=self.username) # Username
                self._ws.cell(column=2, row=self._user_row, value=password) # Password
                self._ws.cell(column=3, row=self._user_row, value='{}') # Empty course list

                self._wb.save(FILE_NAME)
                self._logged_in = True

        else:
            # If logging in
            if not self._attempt_login(password):
                # If incorrect password
                print('Incorrect Password!')

            else:
                # If correct password
                print('Successfully Logged in!')
                self._logged_in = True

        if self._logged_in:
            # Put together user's profile of courses
            temp = ast.literal_eval(self._ws.cell(column=3, row=self._user_row).value)
            self._course_list = {}
            self._add_pre_courses(temp)
            # Get all programs user is in <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    def add_course(self, course_code, lecture_code, ctype, cmark):
        """
        Adds a course to the user's profile
        
        @param str course_code: Course code of the course
        @param str lecture_code: Lecture code
        @param str ctype: Type of course Planned/Taken/etc
        @param float cmark: Mark in the course
        @return: NoneType
        """

        # See if course exists
        course_info = self._get_course_info(course_code.upper())


        # If course does exist
        if course_info is not None:
            # Get rid of useless info
            course_info.pop('id')

            # See if path is in the dictionary
            try:
                if course_code[3:6] in self._course_list[course_code[:3]]:
                    # If code is already in the list - modify
                    self._course_list[course_code[:3]][course_code[3:6]].modify(lecture_code=lecture_code, ctype=ctype, cmark=cmark)
                else:
                    # If not in list, add to list
                    self._course_list[course_code[:3]].update({course_code[3:6]: Course(course_info, lecture_code=lecture_code, ctype=ctype, cmark=cmark)})

            except KeyError:
                # If node does not exist
                self._course_list[course_code[:3]] = {course_code[3:6]: Course(course_info, lecture_code=lecture_code, ctype=ctype, cmark=cmark)}

            self._ws.cell(column=3, row=self._user_row, value=str(self._course_list))

            self._wb.save(FILE_NAME)

        else:
            print('Invalid course name!')

    def get_loggedin(self):
        """
        Return if user is logged in

        @return: bool 
        """

        return self._logged_in

    def get_courses(self):
        """
        Return all Courses
        
        @return: list of Course 
        """
        rlist = []
        keys = self._course_list.keys()

        for key in keys:
            for item in self._course_list[key]:
                rlist.append(self._course_list[key][item])

        return rlist

    def get_breadths(self):
        """
        Return breadth totals of planned and taken
        
        @return: dict of int
        """
        breadth_totals = {'Taken': [0, 0, 0, 0, 0], 'Planned': [0, 0, 0, 0, 0]}
        courses = self.get_courses()

        for course in courses:
            course_type = course.ctype

            for breadth in course.breadths:
                # C for completed
                if course_type == 'C':
                    breadth_totals['Taken'][breadth - 1] += 1
                # P for planned, A for active
                elif course_type == 'P' or course_type == 'A':
                    breadth_totals['Planned'][breadth - 1] += 1

        return breadth_totals

    def get_course_mark(self, course):
        return self._course_list[course[:3]][course[3:6]].cmark

    def get_cgpa(self):
        total = 0
        credits = 0

        courses = self.get_courses()
        for course in courses:

            mark = course.cmark
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

            if course.ccode[-1] == 'Y':
                total += 1 * grade_point
                credits += 1
            else:
                total += .5 * grade_point
                credits += .5

        if total != 0:
            return total / credits
        return 0.0

    def get_total_credits(self):
        """
        Return total credits
        
        @return: dict of float 
        """
        total = {'Planned': 0, 'Taken': 0}

        courses = self.get_courses()

        for course in courses:
            if course.ccode[-1] == 'Y':
                if course.ctype == 'C':
                    total['Taken'] += 1
                elif course.ctype == 'P' or course.ctype == 'A':
                    total['Planned'] += 1

            else:
                if course.ctype == 'C':
                    total['Taken'] += .5
                elif course.ctype == 'P' or course.ctype == 'A':
                    total['Planned'] += .5

        return total

    def _attempt_login(self, password):
        """
        Return if the user's password is correct

        @param str password: 
        @return: bool
        """
        if self._ws.cell(column=2, row=self._user_row).value == password:
            return True

        return False

    def _find_user(self):
        """
        Return if <username> is registered.

        @return: bool
        """

        cell = 0
        row = 1

        while cell is not None:
            # While a name is in the cell
            cell = self._ws.cell(column=1, row=row).value

            if cell == self.username:
                # If the cell is the username
                self._user_row = row
                return True

            else:
                row += 1

        # If the names did not match the username
        self._user_row = row - 1
        return False

    def _add_pre_courses(self, temp):
        """
        Turns from texted generated values to Course objects

        @return: NoneType
        """

        for key in temp:
            self._course_list[key] = {}
            for item in temp[key]:
                self._course_list[key][item] = Course(temp[key][item][0],
                                                      lecture_code=
                                                      temp[key][item][1],
                                                      ctype=temp[key][item][2],
                                                      cmark=temp[key][item][3])

    def _get_course_info(self, course_code):
        """
        
        @param course_code: 
        @return: 
        
        >>> user = User('Tim', 'Cosby')
        >>> user._get_course_info('CSC148H1F20169')
        """

        try:
            page = PAGE + course_code
            print(page)
            pr = Request(page)
            pr.add_header('Authorization', 'TVwEIjRZP80vhnY8HhM0OzZCMfydh4lA')

            file = urlopen(pr)
            lines = file.read().decode('utf-8')
            lines = ast.literal_eval(lines)

            return lines

        except HTTPError:
            # If course does not exist
            return None


class Program:
    def __init__(self):
        # Make a text file of this pre-made
        pass


def correction(search):
    """
    Return possible course_codes the user possibly wanted to enter

    @param str search:
    @return: list of str
    """
    from urllib.request import urlopen
    from urllib.request import Request
    import ast

    page = 'https://cobalt.qas.im/api/1.0/courses/filter?q=code:%22' + search + '%22'

    pr = Request(page)
    ### Enters Key
    pr.add_header('Authorization', 'TVwEIjRZP80vhnY8HhM0OzZCMfydh4lA')

    file = urlopen(pr)

    temp = ast.literal_eval(file.read().decode('utf-8'))

    temper = []
    for i in temp:
        temper.append(i['code'])

    return temper

if __name__ == '__main__':
    details = None

    while True:
        # Run till correct login details have been entered

        details = User(input('Enter Username: '), input('Enter Password: '))

        if not details.get_loggedin():
            del details  # Delete the failed object
        else:
            break

    while True:
        course_code = input('Enter a course: ')
        ctype = input('Type: ')
        cmark = input('Mark: ')
        lecture_code = input('Lecture: ')

        if course_code != '' and ctype != '' and cmark != '' and lecture_code != '':
            details.add_course(course_code, lecture_code=lecture_code, ctype=ctype, cmark=float(cmark))

            if details._course_list[course_code[:3]][course_code[3:6]].lecture_code is None:
                del details._course_list[course_code[:3]][course_code[3:6]]

        print(details.get_courses())
        print(details.get_breadths())
        print(details.get_total_credits())
        print(details.get_cgpa())

'''
if __name__ == '__main__':
    # Loops until you successfully log in
    while True:
        username = input('Enter your username (Between 2-20 characters no ! characters): ')
        password = input('Enter your password: ')
        try:
            # Logs in
            user = User(username, password)

            # Checks to see if you successfully logged in
            if user.get_logged_in():
                break
        except Exception as e:
            print(e)

    course = mark = type = None
    while course != 'exit':
        if course is not None:
            user.add_course(course, type, mark)
            print('Courses:', user)

        course = input('What course would you like to add? or do you want to exit?\n')

        if course != 'exit':
            temp = correction(course)

            if not course.upper() in temp:
                # If entered is not identical to the database
                print('Did you mean ' + str(temp)[1:-1] + '?')
                course = None
            else:
                type = input('Is the course planned/current/passed/failed/dropped\n')
                if 'passed' in type.lower():
                    mark = float(input('What mark did you recieve?\n'))
'''