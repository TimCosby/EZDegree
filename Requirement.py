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

        self._credits_have = 0.0
        self._courses_have = 0

        self.only_used = only_used
        self.only_unused = only_unused
        self._treatall = treatall

        self._used_courses = set([])
        self._reqmet = False

    def _get_modifier(self):
        return self._modifier

    def _get_courses(self):
        return self._courses

    def _get_have(self, used=None):
        used = set() if used is None else used

        if self.modifier[3:7] == 'PASS':
            temp = self._get_stuff(used.copy(), False)

            if self._reqmet:
                self._used_courses = temp

            return self._courses_have

        elif 'CREDITS' in self.modifier:
            used = self._get_stuff(used.copy(), True)

            self._used_courses = used

            return self._credits_have

        #elif 'MARK' == self.modifier:
        #    used = self._get_min_mark(used.copy())

        else:
            raise Exception('Error in base operators', self.modifier)

    def _get_stuff(self, used, credits=False):
        self._credits_have = 0.0
        self._courses_have = 0

        for course in self._courses:
            if not self._treatall:
                # If not looking at every course possible
                if credits and self._credits_have >= self._max:
                    # If looking at credits count
                    break
                elif not credits and self._courses_have >= self._max:
                    # If looking at passed courses count
                    break

            if isinstance(course, Requirement):
                # If a nested requirement
                trash = course.have  # Get the amount of the required satisfied
                if trash >= course.need:  # If the amount satisfied is enough to satisfy
                    self._credits_have += course._credits_have
                    self._courses_have += course._courses_have

            elif self.only_used:
                # If looking at only courses that were previously used in requirements
                if course.passed(exclusions=self.exclusions, inclusions=used):
                    # If the course passed
                    self._credits_have += course.weight
                    self._courses_have += 1

            elif self.only_unused:
                # If looking at only courses that were previously unused in requirements
                trash = used.update(self.exclusions)
                if course.passed(exclusions=trash):
                    # If the course passed
                    used.add(course)
                    self._credits_have += course.weight
                    self._courses_have += 1

            elif course.passed(exclusions=self.exclusions):
                # If the course passed
                used.add(course)
                self._credits_have += course.weight
                self._courses_have += 1

        if credits and self.need <= self._credits_have:
            # If satisfied the requirement
            self._reqmet = True

            if self._credits_have > self._max:  # Makes it so cannot get the max of what we're looking for
                self._credits_have = self._max

        elif not credits and self.need <= self._courses_have:
            # If satisfied the requirement
            self._reqmet = True

            if self._courses_have > self._max:  # Makes it so cannot get the max of what we're looking for
                self._courses_have = self._max

        else:
            # If did not satisfy the requirement
            self._reqmet = False

        return used

    def _get_need(self):
        return self._min if self._min is not None else self._max

    modifier = property(_get_modifier)
    courses = property(_get_courses)
    have = property(_get_have)
    need = property(_get_need)

    def __repr__(self):
        return 'Requirements(' + self.modifier + ' | N: ' + str(self._max) + ', H: ' + str(self.have) + ')'




# NEED A PRETTY SOPHISTICATED SYSTEM WHERE IT FINDS A MIN AND MAX OF COURSES NEEDED TO BE TAKEN