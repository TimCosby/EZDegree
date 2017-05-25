PAGE = 'https://cobalt.qas.im/api/1.0/courses/filter?q=code:%22'
KEY = 'TVwEIjRZP80vhnY8HhM0OzZCMfydh4lA'
from urllib.request import Request
from urllib.request import urlopen
from ast import literal_eval


class Courses:
    def __init__(self):
        self.course_cache = {}

    def add_course(self, course_code, exclusions=None):
        if '*' not in course_code and 'BR' != course_code[:2]:
            page = PAGE + course_code + "%22"
            pr = Request(page)
            pr.add_header('Authorization', KEY)
            raw = urlopen(pr)
            info = literal_eval(raw.read().decode('utf-8'))[0]
        else:
            info = None

        self.course_cache[course_code] = Course(course_code, self.course_cache, exclusions, breadth=info['breadths'] if info is not None else info, times=info['meeting_sections'] if info is not None else info)

    def remove_course(self, course_code):
        try:
            self.course_cache.pop(course_code)
        except KeyError:
            print('Course doesn\'t exist!')

    def change_mark(self, course_code, mark):
        self.course_cache[course_code].mark = mark

    def change_type(self, course_code, type):
        self.course_cache[course_code].type = type

    def __repr__(self):
        return str(self.course_cache)


def is_same(string, other):
    """
    For abstract courses (ie. 'CSC4****')

    @param str string: Abstract Course code 
    @param str other: Another Course code
    @return: bool
    """
    if len(string) - 1 if string[-1] == 'X' else len(string) == len(other):
        if '*' not in other:
            same = True
            for index in range(len(string) - 1 if string[-1] == 'X' else len(string)):
                if string[index] != '*':
                    if string[index] != other[index]:
                        same = False
                        break
            if same:
                return True
    return False


class Course:
    def __init__(self, code, course_cache, exclusions, breadth=None, times=None):
        self.course_code = code
        self.mark = 0
        self.type = 'Planned'

        try:
            if code[6] == 'Y':
                self.weight = 1
            else:
                self.weight = 0.5
        except IndexError:
            self.weight = 0.0

        self.course_count = 1  # Used for abstract courses

        self.exclusions = exclusions
        self.course_cache = course_cache

        self.breadth = breadth  # Not yet implemented
        self.times = times  # Not yet implemented

    def passed(self, exclusions=None, inclusions=None, limit=None, used=None, credits=None):
        if '*' in self.course_code:
            self.weight = 0.0
            self.course_count = 0
            # If an abstract course
            for course in self.course_cache:

                if '*' not in course:

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

            for course in self.course_cache:
                if 'BR' not in course:
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
