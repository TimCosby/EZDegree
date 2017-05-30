from Course import Course


class Requirement:
    """
    Private Attributes:
    ==================
        @param str _modifier:
            The type of requirement for the group
        @param Courses _courses:
            A copy of the course_cache
        @param list of Course _exclusions:
            A list of courses the requirement isn't valid for
        @param float|None _min:
            Minimum amount of modifier needed (If none then don't care about minimum)
        @param float _max:
            Maximum amount of modifier needed
        @param float _credits_have:
            Credit count for the requirement
        @param int _courses_have:
            Course count for the requirement
        @param bool _only_used:
            If requirements are only checking courses that have been used in previous requirements
        @param bool _only_unused:
            If requirements are only checking courses that have not been used in previous requirements
        @param bool _treatall:
            Whether or not all courses need to be tested
        @param set _used_courses:
            A set of all courses that have been used in the requirement
        @param bool _reqmet:
            Whether or not the requirement conditions have been met
    """

    def __init__(self, modifier, min, max, courses, exclusions, treatall, only_used, only_unused):
        self._modifier = modifier
        self._courses = courses
        self._exclusions = exclusions if exclusions is not None else set([])
        self._min = min
        self._max = max

        self._credits_have = 0.0
        self._courses_have = 0

        self._only_used = only_used
        self._only_unused = only_unused
        self._treatall = treatall

        self._used_courses = set([])
        self._reqmet = False

    def _update(self, used=None):
        """
        Update the requirements in the Requirement object

        :param set of Course used: Courses previously used in other requirements
        :return: None
        """

        used = set() if used is None else used

        if self.modifier[3:7] == 'PASS':
            temp = self._get_stuff(used.copy(), False)

            if self._reqmet:
                self._used_courses = temp

        elif 'CREDITS' in self.modifier:
            used = self._get_stuff(used.copy(), True)

            if self._reqmet:
                self._used_courses = used

        elif 'MARK' == self.modifier:
            used = self._get_min_mark(used.copy())

            if self._reqmet:
                self._used_courses = used

        else:
            raise Exception('Error in base operators', self.modifier)

    def _get_modifier(self):
        """
        Return modifier

        i.e. MAXPASS, MAXCREDITS, etc

        :return: str
        """

        return self._modifier

    def _get_courses(self):
        """
        Return list of courses|nested requirements needed for the requirement

        :return: list of Course|Requirement
        """

        return self._courses

    def _get_stuff(self, used, credits=False):
        """
        Return list of courses used in the requirement
        Used to update the requirements in credits/pass/etc.

        :param set of Course used: Courses previously used in other requirements
        :param bool credits: Whether or not searching for course count or amount of credits
        :return: set of Course
        """

        self._credits_have = 0.0
        self._courses_have = 0
        any_false = False

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
                #print('nested')
                # If a nested requirement
                course._update(used)  # Get the amount of the required satisfied

                if course._reqmet:  # If the amount satisfied is enough to satisfy
                    self._credits_have += course._credits_have
                    self._courses_have += 1
                    used.update(course._used_courses)
                else:
                    any_false = True

            elif self._only_used:
                #print(course)
                # If looking at only courses that were previously used in requirements
                if course.passed(exclusions=self._exclusions, inclusions=used, limit=self._max - self._credits_have if credits else self._max - self._courses_have, credits=credits):
                    # If the course passed
                    self._credits_have += course.weight
                    self._courses_have += course.course_count
                else:
                    any_false = True

            elif self._only_unused:
                #print(course)
                # If looking at only courses that were previously unused in requirements
                trash = used.copy()
                trash.update(self._exclusions)
                if course.passed(exclusions=trash, limit=self._max - self._credits_have if credits else self._max - self._courses_have, used=used, credits=credits):
                    # If the course passed
                    self._credits_have += course.weight
                    self._courses_have += course.course_count

                else:
                    any_false = True

            elif course.passed(exclusions=self._exclusions, limit=self._max - self._credits_have if credits else self._max - self._courses_have, used=used, credits=credits):
                #print(course)
                # If the course passed
                self._credits_have += course.weight
                self._courses_have += course.course_count

            else:
                any_false = True

        if credits and self.need <= self._credits_have:
            # If satisfied the requirement
            self._reqmet = not any_false

            if self._credits_have > self._max:  # Makes it so cannot get the max of what we're looking for
                self._credits_have = self._max

        elif not credits and self.need <= self._courses_have:
            # If satisfied the requirement
            self._reqmet = not any_false

            if self._courses_have > self._max:  # Makes it so cannot get the max of what we're looking for
                self._courses_have = self._max

        else:
            # If did not satisfy the requirement
            self._reqmet = False

        return used

    def _get_min_mark(self, used):
        """
        Return list of courses used in the requirement
        Used to update the requirements of a min mark requirement

        :param set of Course used: Courses previously used in other requirements
        :return: set of Course
        """

        if self._courses.mark >= self.need:
            self._reqmet = True
            used.add(self._courses)
            self._courses_have = 1
            self._credits_have = self._courses.weight

        else:
            self._reqmet = False
            self._courses_have = 0
            self._credits_have = 0.0

        return used

    def _get_need(self):
        """
        Return needed credits | count of courses to fulfill the requirement

        :return: int | float
        """

        return self._min if self._min is not None else self._max  # Get the min if it exist

    def _get_have(self):
        """
        Return credits | count of courses met so far in the requirement

        :return: int | float
        """

        return self._credits_have if 'CREDITS' in self.modifier else self._courses.mark if self.modifier == 'MARK' else self._courses_have

    modifier = property(_get_modifier)
    courses = property(_get_courses)
    update = property(_update)
    need = property(_get_need)
    have = property(_get_have)

    def __repr__(self):
        return 'Requirements(' + self.modifier + ' | N: ' + str(self.need) + ', H: ' + str(self.have) + ')'




# NEED A PRETTY SOPHISTICATED SYSTEM WHERE IT FINDS A MIN AND MAX OF COURSES NEEDED TO BE TAKEN