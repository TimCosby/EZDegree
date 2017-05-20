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

    def __init__(self, modifier, min, max, courses, exclusions, treatall, only_used, only_unused):
        self._modifier = modifier
        self._courses = courses
        self.exclusions = exclusions if exclusions is not None else set([])
        self._min = min
        self._max = max
        self._treatall = treatall
        self._have = 0.0

        self.only_used = only_used
        self.only_unused = only_unused

        self._used_courses = set([])
        self._reqmet = False

    def _get_modifier(self):
        return self._modifier

    def _get_courses(self):
        return self._courses

    def _get_have(self, used=None):
        used = set() if used is None else used

        if self.modifier[3:7] == 'PASS':
            used = self._get_passed(used.copy())

        elif 'CREDITS' in self.modifier:
            used = self._get_credits(used.copy())

        else:
            raise Exception('Error in base operators', self.modifier)

        self._used_courses = used

        return self._have

    def _get_passed(self, used):
        temp_used = used
        passed = 0

        for course in self._courses:
            print('Used Courses:', temp_used)
            if not self._treatall and self._max <= passed:
                break

            elif isinstance(course, Requirement):
                trash_have = course.have
                if trash_have >= course.need:
                    passed += trash_have
                    temp_used.update(course._used_courses)

            elif self.only_unused:
                # If only checking courses that haven't been used
                print('Course:', course)
                trash = temp_used.copy()
                trash.update(self.exclusions)
                if course.passed(exclusions=trash):
                    passed += 1
                    temp_used.add(course)
                    print('Passed!')
                else:
                    print('Did not pass!')

            else:
                # If checking if the course has been passed
                print('Course:', course)
                if course.passed(exclusions=self.exclusions):
                    passed += 1
                    temp_used.add(course)
                    print('Passed!')
                else:
                    print('Did not pass!')

        if self.need <= passed:
            self._reqmet = True

        else:
            self._reqmet = False

        if passed > self._max:
            self._have = self._max
        else:
            self._have = passed

        return temp_used

    def _get_credits(self, used):
        temp_used = used
        credits = 0.0

        for course in self._courses:
            if not self._treatall and self._max <= credits:
                # If not looking at every course and surpassed the max needed amount of credits
                break

            elif isinstance(course, Requirement):
                # If a nested requirement
                trash_have = course.have
                if trash_have >= course.need:
                    # If requirement passed
                    credits += trash_have  # Add credits from nested requirement
                    temp_used.update(course._used_courses)  # Add the courses used in the nested requirement

            elif self.only_used:
                # If only looking into courses taken already
                if course.passed(exclusions=self.exclusions, inclusions=temp_used):
                    credits += course.weight
                    temp_used.add(course)

            elif self.only_unused:
                trash = temp_used.copy()
                trash.update(self.exclusions)
                if course.passed(exclusions=trash):
                    credits += course.weight
                    temp_used.add(course)

            else:
                if course.passed(exclusions=self.exclusions):
                    credits += course.weight
                    temp_used.add(course)

        if self.need <= credits:
            self._reqmet = True
        else:
            self._reqmet = False

        if credits > self._max:
            self._have = self._max
        else:
            self._have = credits

        return temp_used

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
