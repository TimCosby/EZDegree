from openpyxl import load_workbook
from openpyxl import Workbook
import ast
import degree_search
from urllib.request import Request
from urllib.request import urlopen
from urllib.request import HTTPError
from urllib.request import URLError
from Course import *
from copy import deepcopy

##### TO DO ######
# 1. Make a pre-load file for all the functions that only need to happen to
#    update the system (ie. Creating the tree of all the courses - Check
#
# 2. Make a tree as shown in OneNote - Check
#
# 3. When adding a program only add the program code to the user's file - Check
#
# 4. In get_program_req etc. grab from the program tree instead of sudo shiz
#
# 5. Update To Do list
#
# 6. Seperate build tree by mutating the existing tree - Check
#
# 7. For this, cache all the instances of a single course as one object so
#    there's no need to search the entire tree to update all of them - Check
#
# 8. Deal with adding to program requirements that have ****s in them (ie. USA4****

#Shatter Sort
#Radix Sort
FILE_NAME = 'database.xlsx'
PAGE = 'https://cobalt.qas.im/api/1.0/courses/'
KEY = 'TVwEIjRZP80vhnY8HhM0OzZCMfydh4lA'
WORKBOOK = load_workbook(FILE_NAME)
WORKSHEET = WORKBOOK.active
PROGRAM_TREE = eval(open('data.dat', 'r').readline())


class Login:
    def __init__(self, username, password):
        self.username = username.lower()
        self.password = password

        self._user_row = None

        if self._valid_characters():
            response = self._find_user()
            if response[0]:
                # If valid user

                if WORKSHEET.cell(column=2, row=response[1]).value == self.password:
                    # If password is correct
                    self._user_row = response[1]

            elif 'y' in input('Do you want to create a new user? Y/N').lower():
                self._user_row = response[1]

    @property
    def get_row(self):
        return self._user_row

    def _valid_characters(self):
        if ' ' in self.username:
            print('Invalid username characters!')
            return False

        elif ' ' in self.password:
            print('Invalid password characters!')
            return False

        else:
            return True

    def _find_user(self):
        """
        Return if <username> is registered.

        @return: bool
        """

        cell = 0
        row = 1

        while cell is not None:
            # While a name is in the cell
            cell = WORKSHEET.cell(column=1, row=row).value

            if cell == self.username:
                # If the cell is the username
                return True, row

            else:
                row += 1

        # If the names did not match the username
        return False, row - 1


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

        login_response = Login(username, password).get_row

        if login_response is not None:
            print('Successfully logged in!')

            self._logged_in = True
            self._user_row = login_response
            self._course_list = {}

            # Get user programs
            self._program_list = ast.literal_eval(WORKSHEET.cell(column=4, row=self._user_row).value)

            self._program_course_cache = {}
            self._user_program_tree = deepcopy(PROGRAM_TREE)
            self._program_tree = self._build_tree()

            # Put together user's profile of courses
            temp = ast.literal_eval(WORKSHEET.cell(column=3, row=self._user_row).value)
            self._add_pre_courses(temp)

            print('protree',self._program_tree)

        else:
            print('Incorrect Login!')
            self._logged_in = False

    def _update_inner_nodes(self, root=None):
        """
        Update which nodes in a group in the tree are satisfied by their courses
        
        @param dict root: 
        @return: NoneType
        """

        for child in root:
            # For CourseNode in dict
            if child.course_code is None:
                # If child is a node, get the total credits from its child courses
                child.have = self._update_program_nodes(root=child.children)

                if child.have >= child.need:
                    # If the sum credits from its child courses satisfies its requirements
                    child.requirement = True

    def _update_program_nodes(self, root=None):
        """
        Update which nodes in the tree are satisfied by their courses
        
        @param None | dict root: root dictionary looking 
        @return: 
        """
        total = 0

        if root is None:
            # If the dict of all programs
            for program in self._program_tree:

                self._update_program_nodes(root=self._program_tree[program])
        else:
            # If a single program or node dict
            try:
                # Tries to recurse through the groups of courses
                self._update_inner_nodes(root=root['lists'])

                # Adds up the total credits taken in the group
                total += sum([i.need for i in root['lists'] if i.requirement is True])

            except: pass

            # Adds up the total single credits taken in the dictionary
            total += sum([root[i].need for i in root if i != 'list' and isinstance(root[i], CourseNode) and root[i].requirement is True])

            return total

    def _update_program_courses(self, course, add):
        """
        Updates the tree with new requirements
        aka add or remove a course taken value from tree
        
        @param str course: course code
        @param bool add: True if adding False if removing 
        @return: 
        """
        # Later make this only for if course is Completed
        # Make a system to update breadth requirements

        try:
            if add:
                # Completes requirement
                self._program_course_cache[course].requirement = True
            else:
                # Uncompletes requirement
                self._program_course_cache[course].requirement = False

        except KeyError: pass

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
        course_info = self._get_course_info(course_code)

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

            WORKSHEET.cell(column=3, row=self._user_row, value=str(self._course_list))
            self._update_program_courses(course_code[:8], True)
            self._update_program_nodes()
            #self._program_tree = self._build_tree()
            WORKBOOK.save(FILE_NAME)

        else:
            print('Invalid course name!')

    def add_program(self, program_code):
        """
        Adds a program to the user's profile
        
        @param str program_code: 
        @return: NoneType
        """

        # Only add if program is not already in
        if program_code in PROGRAM_TREE:
            if program_code not in self._program_list:
                self._program_list.append(program_code)

                # Update database
                WORKSHEET.cell(column=4, row=self._user_row, value=str(self._program_list))
                WORKBOOK.save(FILE_NAME)
        else:
            print('Invalid Program!')

    def remove_course(self, course_code):
        """
        Delete a course from the list
        
        @param str course_code: Course code (ie. CSC148) 
        @return: NoneType
        """
        del self._course_list[course_code[:3]][course_code[3:6]]

        # Update database
        WORKSHEET.cell(column=3, row=self._user_row, value=str(self._course_list))
        self._update_program_courses(course_code[:8], False)
        self._update_program_nodes()
        WORKBOOK.save(FILE_NAME)

    def remove_program(self, program_code):
        """
        Delete a course from the list

        @param str program_code: Code for the program 
        @return: NoneType
        """

        try:
            self._program_list.remove(program_code)

            # Update database
            WORKSHEET.cell(column=4, row=self._user_row, value=str(self._program_list))
            WORKBOOK.save(FILE_NAME)
        except ValueError:
            print('Program does not exist')

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

    def get_programs(self):
        """
        Return a list of taken programs
        
        >>> usr=User('Tim', 'Cosby')
        >>> usr.add_program('ASMAJ0135')
        >>> usr.get_programs()
        """
        return self._program_list

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

    def get_program_req(self, program_code):
        """
        
        @param program_code: 
        @return: 
        
        >>> usr = User('Tim', 'Cosby')
        >>> usr.get_program_req('ASMAJ1423')
        """
        return self._program_tree[program_code]

    def get_easiest(self, ratio=True):
        """
        Return easiest to get courses
        
        @return: list
        """
        totals = {}

        def eval_totals(totals, temp):
            """
            Add to the total need and have
            
            @param dict of int totals: 
            @param list of CourseNode | CourseNode temp: 
            @return: 
            """

            if temp.requirement is True:
                # If the group requirements have been met
                totals[program][0] += temp.need
                totals[program][1] += temp.need
            else:
                # If the group requirements have yet to be met
                totals[program][0] += temp.need
                totals[program][1] += temp.have

            return totals

        for program in self._program_tree:
            # For each program
            totals[program] = [0, 0]

            for i in self._program_tree[program]:
                # For each course
                temp = self._program_tree[program][i]

                if isinstance(temp, list):
                    # If grouped courses
                    for node in temp:
                        totals.update(eval_totals(totals, node))

                else:
                    # If a CourseNode
                    totals.update(eval_totals(totals, temp))

        # Index 0: name, 1: need, 2: have, 3: ratio, 4: need-to-get
        sorted_totals = [[i] + totals[i] for i in totals]
        sorted_totals = [i + [i[2] / i[1]] + [i[1] - i[2]] for i in sorted_totals]

        if ratio:
            index = 3
        else:
            index = 4

        sorted_totals.sort(reverse=True, key=lambda x: x[index])
        return sorted_totals

    def _add_pre_courses(self, temp):
        """
        Turns from texted generated values to Course objects
        Only runs at startup

        :param dict temp:
        @return: NoneType
        """

        for key in temp:
            # For each program
            self._course_list[key] = {}
            for item in temp[key]:
                # For each course
                self._course_list[key][item] = Course(temp[key][item][0], lecture_code=temp[key][item][1], ctype=temp[key][item][2], cmark=float(temp[key][item][3]))

                # Tell the tree that the course is true
                self._update_program_courses(temp[key][item][0]['code'][:-1], True)
        # Update the nodes in the tree for the new course additions
        self._update_program_nodes()

    def _recur(self, courses):
        """
        Recursively format dictionary into computer readable
        
        @param list | tuple courses: 
        @return: dict
        """
        temp = {}

        for course in courses:
            if isinstance(course, int):
                # If the number of courses needed to be taken in a list of courses
                pass

            elif isinstance(course, list):
                # If a list of ATLEAST this many courses in this list need to be taken
                need = course[-1]  # Get the number of courses needed (routinely stored at the end of the list)
                children = self._recur(course)  # Recurses through the list to get its children

                try:
                    # If list is already in the dictionary add a new Node to the list
                    temp['lists'].append(CourseNode(None, need=need, children=children))

                except KeyError:
                    # If list is not yet in the dictionary add a new Node in a new list
                    temp['lists'] = [CourseNode(None, need=need, children=children)]

            elif isinstance(course, tuple):
                # If a tuple of this AND this course need to be taken
                need = len(courses)  # Get the number of courses needed (All courses in the tuple are needed)
                children = self._recur(course)  # Recurses through the list to get its children

                try:
                    # If list is already in the dictionary add a new Node to the list
                    temp['lists'].append(CourseNode(None, need=need, children=children))

                except KeyError:
                    # If list is not yet in the dictionary add a new Node in a new list
                    temp['lists'] = [CourseNode(None, need=need, children=self._recur(course))]

            elif course[:2] == 'BR':
                # Creates the new node for the tree
                temp_course = CourseNode('\'' + course[:-1] + '\'', need=float(course[3:]))

                if course[:3] not in self._program_course_cache:
                    # If breadth is not yet cached
                    self._program_course_cache[course[:-1]] = temp_course

                # Ties all like-courses to the same id
                temp[course[:-1]] = self._program_course_cache[course[:-1]]

            else:
                # If just a regular course

                if course[-2] == 'H' or course[-2] == '*':
                    # If a half course or non-specific
                    need = .5
                else:
                    # If a year course
                    need = 1

                # Creates the new node for the tree
                temp_course = CourseNode('\'' + course + '\'', need=need)

                if course not in self._program_course_cache:
                    # If course is not yet cached
                    self._program_course_cache[course] = temp_course

                # Ties all like-courses to the same id
                temp[course] = self._program_course_cache[course]

        return temp

    def _build_tree(self):
        """
        Builds the program tree
        Only runs at start up
        
        @return: dict
        """

        tree = {}

        for program in PROGRAM_TREE:
            # Add all the level courses together into one big list
            courses = self._user_program_tree[program][1]
            courses.extend(self._user_program_tree[program][2])
            courses.extend(self._user_program_tree[program][3])
            courses.extend(self._user_program_tree[program][4])

            # Get the proper dictionary format
            tree.update({program: self._recur(courses)})

        return tree

    def _get_course_info(self, course_code):
        """
        Returns course data from api or None if it either doesn't exist or have no internet
        
        @param course_code: 
        @return: dict | None
        
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
        except URLError:
            print('No Internet!')
            return None


class Program:
    def __init__(self, program_code):
        # Make a text file of this pre-made
        self.program_code = program_code
        self.name = PROGRAMS[program_code]['name']
        self.type = PROGRAMS[program_code]['type']
        self.description = PROGRAMS[program_code]['description']
        self.fce = PROGRAMS[program_code]['fce']
        self.level1 = PROGRAMS[program_code][1]
        self.level2 = PROGRAMS[program_code][2]
        self.level3 = PROGRAMS[program_code][3]
        self.level4 = PROGRAMS[program_code][4]

        self.course_requirements = self.level1 + self.level2 + self.level3 + self.level4

    def __repr__(self):
        return '{\'name\': \'' + str(self.name) + '\', \'id\': \'' + str(self.program_code) + '\', \'type\': \'' + str(self.type) + '\', \'description\': \'' + str(self.description) + '\', \'fce\': ' + str(self.fce) + ', 1: ' + str(self.level1) + ', 2: ' + str(self.level2) + ', 3: ' + str(self.level3) + ', 4: ' + str(self.level4) + '}'


class ProgramNode:
    def __init__(self, program_dict):
        self.program_name = program_dict['name']
        self.program_id = program_dict['id']
        self.program_type = program_dict['type']
        self.description = program_dict['description']
        self.fce = program_dict['fce']
        self.level1 = program_dict[1]
        self.level2 = program_dict[2]
        self.level3 = program_dict[3]
        self.level4 = program_dict[4]
        self.course_requirements = self.level1 + self.level2 + self.level3 + self.level4
        self.courses = {}


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
        details.add_course('MAT235Y1Y20169', 'L0101', 'C', 50)
        print(details.get_easiest())
        course_code = input('Enter a course: ')
        ctype = input('Type: ')
        cmark = input('Mark: ')
        lecture_code = input('Lecture: ')

        if course_code != '' and ctype != '' and cmark != '' and lecture_code != '':
            details.add_course(course_code, lecture_code=lecture_code, ctype=ctype, cmark=float(cmark))

            if details._course_list[course_code[:3]][course_code[3:6]].lecture_code is None:
                del details._course_list[course_code[:3]][course_code[3:6]]

        #print(details.get_breadths())
        #print(details.get_total_credits())
        #print(details.get_cgpa())
        #print(details.add_course('CSC401H1S20171', 'L0101', 'C', 100 ))
        #print(details.get_program_req('ASMAJ1423'))
        #print([i.ccode for i in details.get_courses()])

