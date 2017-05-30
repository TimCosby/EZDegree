from urllib.request import Request
from urllib.request import urlopen
from ast import literal_eval
import ssl
PAGE = 'https://cobalt.qas.im/api/1.0/courses/filter?q=code:%22'
KEY = 'TVwEIjRZP80vhnY8HhM0OzZCMfydh4lA'


class Courses:
    """
    Course handler

    Public Attributes:
    ==================
        @param dict course_cache:
            Dictionary of course objects made
    """
    def __init__(self, taken_courses):
        self.course_cache = {}
        self.taken_courses = taken_courses

    def add_course(self, course_code):
        """
        Make <course_code> into a Course object

        :param str course_code: Course to add
        :return: None
        """

        if course_code not in self.course_cache:
            if '*' not in course_code and 'BR' != course_code[:2]:
                try:
                    page = PAGE + course_code + "%22"
                    pr = Request(page)
                    pr.add_header('Authorization', KEY)
                    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
                    raw = urlopen(pr, context=context)
                    info = literal_eval(raw.read().decode('utf-8'))[0]
                except IndexError:
                    info = None
            else:
                info = None

            self.course_cache[course_code] = Course(course_code, self.course_cache, self.taken_courses, breadth=info['breadths'] if info is not None else info, times=info['meeting_sections'] if info is not None else info)

        else:
            print('not', course_code)
            print('Course is already added!')

    def remove_course(self, course_code):
        """
        Remove the <course_code> object

        :param str course_code: Course to remove
        :return: None
        """

        try:
            self.course_cache.pop(course_code)
        except KeyError:
            print('Course doesn\'t exist!')

    def change_mark(self, course_code, mark):
        """
        Modify <course_code>'s Course object to <mark>

        :param str course_code: Course to modify
        :param float mark: Mark to change to
        :return: None
        """

        self.course_cache[course_code].mark = mark

    def get_mark(self, course_code):
        """
        Return the mark of <course_code>'s Course object

        :param str course_code:
        :return: float
        """

        return self.course_cache[course_code].mark

    def change_type(self, course_code, type):
        """
        Modify <course_code>'s Course object to <type>

        :param str course_code: Course to modify
        :param str type: Type to change to
        :return: None
        """

        self.course_cache[course_code].type = type

    def get_type(self, course_code):
        """
        Return the type of <course_code>'s Course object

        :param str course_code:
        :return: str
        """

        return self.course_cache[course_code].type

    def __repr__(self):
        return str(self.course_cache)


def is_same(string, other):
    """
    For abstract courses (ie. 'CSC4****')

    @param str string: Abstract Course code 
    @param str other: Another Course code
    @return: bool
    """

    # If the two strings are the same length
    if len(string) - 1 if string[-1] == 'X' else len(string) == len(other):

        # If both courses aren't abstract
        if '*' not in other:
            same = True
            # For every index in the course code
            for index in range(len(string) - 1 if string[-1] == 'X' else len(string)):
                # If the index is not an abstract
                if string[index] != '*':
                    # If the indexes do not match
                    if string[index] != other[index]:
                        same = False
                        break
            if same:
                return True
    return False


class Course:
    """
    Private Attributes:
    ==================
        @param str course_code:
            Code for the course
        @param float mark:
            Mark for the course
        @param str type:
            Type of the course
        @param float weight:
            GPA weight of the course
        @param dict course_cache:
            Copy of course_cache
        @param list of str taken_courses:
            List of courses the user has taken
        @param list of int breadth:
            List of breadth count for course
        @param dict times:
            Dictionary of times the course takes place
    """
    def __init__(self, code, course_cache, taken_courses, breadth=None, times=None):
        self.course_code = code
        self.mark = 0.0
        self.type = 'Planned'

        try:
            if code[6] == 'Y':
                self.weight = 1.0
            else:
                self.weight = 0.5
        except IndexError:
            self.weight = 0.0

        self.course_count = 1  # Used for abstract courses

        self.taken_courses = taken_courses
        self.course_cache = course_cache

        self.breadth = breadth  # Not yet implemented
        self.times = times  # Not yet implemented

    def passed(self, exclusions=None, inclusions=None, limit=None, used=None, credits=False):
        """
        Return if the the course passes or not

        :param set exclusions: Courses that are not valid to pass
        :param set inclusions: Courses that are the only ones which are valid to pass
        :param float limit: Limit of how much should be checked (for abstract courses)
        :param set used: Set of courses used in previous requirements
        :param bool credits: If looking for course count or amount of credits
        :return: bool
        """
        if '*' in self.course_code:
            self.weight = 0.0
            self.course_count = 0
            # If an abstract course
            for course in self.taken_courses:

                passed = True
                if exclusions is not None and self.course_cache[course] in exclusions:
                    passed = False

                if inclusions is not None and self.course_cache[course] not in inclusions:
                    passed = False

                #print(course, exclusions)

                if passed and self.course_cache[course].passed and is_same(self.course_code, course):
                    #print('made it')
                    self.weight += self.course_cache[course].weight  # Since any course can potentially satisfy
                    self.course_count += 1

                    if used is not None:
                        used.add(self.course_cache[course])

                    if self.course_code[-1] == 'X' or (credits and self.weight >= limit) or (not credits and self.course_count >= limit):
                        break

            return self.weight != 0.0

        elif self.course_code[:2] == 'BR':
            # If a certain breadth # is required is required
            total_breadth = 0

            for course in self.taken_courses:
                passed = True
                if exclusions is not None and self.course_cache[course] in exclusions:
                    passed = False

                if inclusions is not None and self.course_cache[course] not in inclusions:
                    passed = False

                if passed and self.course_cache[course].breadth is not None and int(self.course_code[-1]) in self.course_cache[course].breadth:
                    total_breadth += 1

                    if self.course_code[-1] == 'X':
                        break

            return total_breadth != 0

        else:
            passed = True
            if exclusions is not None and self in exclusions:
                passed = False

            if inclusions is not None and self not in inclusions:
                passed = False

            if passed and self.mark >= 50:
                if used is not None:
                    used.add(self)

                return True
            else:
                return False

    def __repr__(self):
        return 'Course(' + self.course_code + ')'
