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

    def __init__(self, modifier, min, max, courses, exclusions, treatall):
        self._modifier = modifier
        self._courses = courses
        self.exclusions = exclusions if exclusions is not None else set([])
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

    def _get_have(self, used=None):
        used = set() if used is None else used

        if self.modifier[3:7] == 'PASS':
            if self.modifier[-1] == 'X':
                special = 1
            else:
                special = 0

            used = self._get_passed(special, used.copy())

        elif 'CREDITS' in self.modifier:
            if self.modifier[-1] == 'X':
                special = 1
            elif self.modifier[0] == 'X':
                special = 2
            else:
                special = 0

            used = self._get_credits(special, used.copy())

        else:
            raise Exception('Error in base operators', self.modifier)

        self._used_courses = used

        return self._have

    def _get_passed(self, special, used):
        temp_used = used
        passed = 0

        #print('\nV Special:', special)

        for course in self._courses:
            print('Used Courses:', temp_used)
            if not self._treatall and self._max <= passed:
                break

            elif isinstance(course, Requirement):
                if course.need <= course._get_have(temp_used):
                    passed += 1
                    temp_used.update(course._used_courses)

            elif special == 1:
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

            elif special == 0:
                # If checking if the course has been passed
                print('Course:', course)
                if course.passed(exclusions=self.exclusions):
                    passed += 1
                    temp_used.add(course)
                    print('Passed!')
                else:
                    print('Did not pass!')
            else:
                raise Exception('Special is at wrong number', special)

        if self.need <= passed:
            self._reqmet = True

        else:
            self._reqmet = False

        self._have = passed
        return temp_used

    def _get_credits(self, special, used):
        temp_used = used
        credits = 0.0

        for course in self._courses:
            if not self._treatall and self._max <= self.have:
                break

            elif isinstance(course, Requirement):
                if course._max <= course._get_have(temp_used):
                    sub_used = course._used_courses - temp_used

                    count = 0.0
                    for item in sub_used:
                        if count >= course._max:
                            break
                        else:
                            count += item.weight
                    credits += count

                    temp_used.update(course._used_courses)

            elif special == 2:
                if course.passed(exclusions=self.exclusions, inclusions=temp_used):
                    credits += course.weight
                    temp_used.add(course)

            elif special == 1:
                trash = temp_used.copy().update(self.exclusions)
                if course.passed(exclusions=trash):
                    credits += course.weight
                    temp_used.add(course)

            elif special == 0:
                if course.passed(exclusions=self.exclusions):
                    credits += course.weight
                    temp_used.add(course)

            else:
                raise Exception('Special is at wrong number', special)

        if self.need <= credits:
            self._reqmet = True

        else:
            self._reqmet = False

        self._have = credits
        return temp_used

    '''
    def _get_have(self, used=None):
        #print('\n', self._modifier)
        #print('courses:', self._courses)
        used = set([]) if used is None else used

        if self._modifier[3:7] == 'PASS':
            if self._modifier[-1] == 'X':
                self._get_passed(1, self._treatall, used)
            else:
                self._get_passed(0, self._treatall, used)

        elif 'CREDITS' in self.modifier:
            if self._modifier[0] == 'X':
                self._get_credits(2, self._treatall, used)

            elif self.modifier[-1] == 'X':
                self._get_credits(1, self._treatall, used)

            else:
                self._get_credits(0, self._treatall, used)

        elif self._modifier == 'MARK':
            self._get_mark(used)

        elif self._modifier == 'ALLORNOT':
            self._get_all_or_not(used)

        else:
            print(self.modifier)
            raise Exception('Not possible modifier!')

        #print('used', self._used_courses)
        #print(self._reqmet)

        return self._have

    def _get_passed(self, special=0, treatall=False, used=None):
        temp_used = used.copy()  # Which courses have been used (for special conditions)
        passed = 0  # Passed courses counter

        for course in self._courses:
            print('course:', course)
            print('used', temp_used, '\n')
            if not treatall and passed >= self._max:
                # If has passed the limit and is not checking all courses in the requirement
                break

            if isinstance(course, Requirement):
                # If a nested requirement

                course._get_have(temp_used.copy())
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

    def _get_credits(self, special=0, treatall=False, used=None):
        credits = 0.0
        temp_used = used.copy()

        for course in self._courses:
            if not treatall and credits >= self._max:
                # If has passed the limit and is not checking all courses in the requirement
                break

            elif isinstance(course, Requirement):
                course._get_have(temp_used.copy())

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

    def _get_mark(self, used=None):
        if self._courses[0].passed(exclusions=self.exclusions) and self._courses[0].mark >= self._max:
            self._have = 1
            self._used_courses.add(self._courses[0])
            self._reqmet = True
        else:
            self._used_courses = set([])
            self._reqmet = False

    def _get_all_or_not(self, used=None):
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
    '''

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
