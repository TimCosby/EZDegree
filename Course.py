
class Courses:
    def __init__(self):
        self.course_cache = {}

    def add_course(self, course_code, exclusions=None):
        self.course_cache[course_code] = Course(course_code, self.course_cache, exclusions)

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
    if len(string) == len(other):
        if '*' not in other:
            same = True
            for index in range(len(string)):
                if string[index] != '*':
                    if string[index] != other[index]:
                        same = False
                        break
            if same:
                return True
    return False


class Course:
    def __init__(self, code, course_cache, exclusions):
        self.course_code = code
        self.mark = 0
        self.type = 'Planned'

        if code[6] == 'Y':
            self.weight = 1
        else:
            self.weight = 0.5

        self.exclusions = exclusions
        self.course_cache = course_cache

        self.breadth = None  # Not yet implemented

    def _passed(self):
        if '*' in self.course_code:
            # If an abstract course
            for course in self.course_cache:
                if is_same(self.course_code, course) and self.course_cache[course].passed:
                    return True
            return False

        elif self.course_code[:2] == 'BR':
            # If a certain breadth # is required is required
            total_breath = 0
            needed_breadth = int(self.course_code[3])
            for course in self.course_cache:
                if self.course_cache[course].breadth == self.course_code[2]:
                    total_breath += 1
                    if total_breath >= needed_breadth:
                        return True
            return False

        else:
            return self.mark >= 50

    passed = property(_passed)

    def __repr__(self):
        return 'Course(' + self.course_code + ')'