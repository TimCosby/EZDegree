
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
        self.time = None  # Not yet implemented

    def passed(self, exclusions=None, inclusions=None):
        if '*' in self.course_code:
            self.weight = 0.0
            # If an abstract course
            for course in self.course_cache:
                passed = True
                if exclusions is not None and course in exclusions:
                    passed = False

                if inclusions is not None and course not in inclusions:
                    passed = False

                if passed and is_same(self.course_code, course) and self.course_cache[course].passed:
                    self.weight += course.weight  # Since any course can potentially satisfy

                    if self.course_code[-1] != 'X':
                        break

            return self.weight != 0.0

        elif self.course_code[:2] == 'BR':
            # If a certain breadth # is required is required
            total_breath = 0
            self.weight = 0.0

            for course in self.course_cache:
                passed = True
                if exclusions is not None and course in exclusions:
                    passed = False

                if inclusions is not None and course not in inclusions:
                    passed = False

                if passed and self.course_cache[course].breadth == self.course_code[-1]:
                    total_breath += 1
                    self.weight += course.weight

                    if self.course_code[-1] != 'X':
                        break

            return self.weight != 0.0

        else:
            passed = True
            if exclusions is not None and self in exclusions:
                passed = False

            if inclusions is not None and self not in inclusions:
                passed = False

            return passed and self.mark >= 50

    def __repr__(self):
        return 'Course(' + self.course_code + ')'
