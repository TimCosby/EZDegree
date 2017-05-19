from Course import Course


class Requirement:
    """
    Attributes:
    ==========
        @param str modifier: 
                        The type of requirement for the group
        @param float|None min: 
                        Minimum amount of modifier needed (If none then don't care about minimum)
        @param float max:
                        Maximum amount of modifer needed
        @param list of Course courses: 
                        Courses required
        @param bool treatall:
                        Whether or not all courses need to be tested
    """

    def __init__(self, modifier, min, max, courses, exclusions=None, treatall=False):
        self._modifier = modifier
        self._courses = courses
        self.exclusions = exclusions if exclusions is not None else ()
        self._min = min
        self._max = max
        self._treatall = treatall
        self._have = 0

        self._used_courses = set([])
        self._reqmet = False

    def _get_modifier(self):
        return self._modifier

    def _get_courses(self):
        return self._courses

    def _get_have(self):
        if self._modifier[3:7] == 'PASS':
            if self._modifier[-1] == 'X':
                self._get_passed(1, self._treatall)
            else:
                self._get_passed(0, self._treatall)

        elif 'CREDITS' in self.modifier:
            if self._modifier[0] == 'X':
                self._get_credits(2, self._treatall)

            elif self.modifier[-1] == 'X':
                self._get_credits(1, self._treatall)

            else:
                self._get_credits(0, self._treatall)

        elif self._modifier == 'MARK':
            self._get_mark()

        elif self._modifier == 'ALLORNOT':
            self._get_all_or_not()

        else:
            print(self.modifier)
            raise Exception('Not possible modifier!')

        return self._have

    def _get_passed(self, special=0, treatall=False):
        temp_used = set([])  # Which courses have been used (for special conditions)
        passed = 0  # Passed courses counter

        for course in self._courses:
            if not treatall and passed >= self._max:
                # If has passed the limit and is not checking all courses in the requirement
                break

            if isinstance(course, Requirement):
                # If a nested requirement

                course._used_courses = temp_used.copy()
                course._get_have()
                if course._reqmet:
                    # If nested requirement passes
                    passed += 1
                    temp_used.update(course._used_courses)

            elif special == 1:
                # If a special requirement
                if course.passed(exclusions=set(self.exclusions).copy().update(temp_used)):
                    # If the course has not yet been use and is passed or is being taken
                    passed += 1
                    temp_used.add(course)

            elif course.passed(exclusions=self.exclusions):
                # If the course has been passed or is being taken
                passed += 1
                temp_used.add(course)

        if (self._min is not None and passed >= self._min) or passed >= self._max:
            # If courses meet the requirement
            self._reqmet = True
            self._have = passed
            self._used_courses = temp_used

        else:
            # If courses don't meet the requirement
            self._reqmet = False
            self._used_courses = []

    def _get_credits(self, special=0, treatall=False):
        credits = 0.0
        temp_used = set([])

        for course in self._courses:
            if not treatall and credits >= self._max:
                # If has passed the limit and is not checking all courses in the requirement
                break

            elif isinstance(course, Requirement):
                course._used_courses = temp_used.copy()
                course._get_have()

                if course._reqmet:
                    sub_used = course._used_courses - temp_used
                    for subcourse in sub_used:
                        credits += subcourse.weight

                    temp_used.update(sub_used)

            elif special == 2 and course.passed(inclusions=temp_used, exclusions=self.exclusions):
                temp_used.add(course)
                credits += course.weight

            elif special == 1 and course.passed(exclusions=set(self.exclusions).copy().update(temp_used)):
                temp_used.add(course)
                credits += course.weight

            elif course.passed(exclusions=self.exclusions):
                credits += course.weight

        if (self._min is not None and credits >= self._min) or credits >= self._max:
            # If courses meet the requirement
            self._have = credits
            self._reqmet = True
            self._used_courses = temp_used

        else:
            # If courses don't meet the requirement
            self._reqmet = False
            self._used_courses = set([])

    def _get_mark(self):
        if self._courses[0].passed(exclusions=self.exclusions) and self._courses[0].mark >= self._max:
            self._have = 1
            self._used_courses.add(self._courses[0])
            self._reqmet = True
        else:
            self._used_courses = set([])
            self._reqmet = False

    def _get_all_or_not(self):
        temp_used = set([])

        for course in self._used_courses:
            if isinstance(course, Requirement):
                course._used_courses = temp_used.copy()
                course._get_have()

                if not course._reqmet:
                    self._reqmet = False
                    self._used_courses = set([])
                    return None
                
                else:
                    temp_used.add(course._used_courses)

            elif not course.passed(exclusions=self.exclusions):
                self._reqmet = False
                self._used_courses = set([])
                return None

        self._have = len(self.courses)
        self._reqmet = True
        self._used_courses = temp_used 

    def _get_need(self):
        return self._min if self._min is not None else self._max

    modifier = property(_get_modifier)
    courses = property(_get_courses)
    have = property(_get_have)
    need = property(_get_need)

    def __repr__(self):
        return 'Requirements(' + self.modifier + ' | N: ' + str(self._max) + ', H: ' + str(self.have) + ')'





#if __name__ == '__main__':
    #usr = User()
