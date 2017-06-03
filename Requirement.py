from Course import Course

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
        @param int _requirements_met:
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

    def __init__(self, modifier, min, max, courses, exclusions, treatall, only_used, only_unused, taken_courses, breadth):
        self._modifier = modifier
        self._courses = courses
        self._exclusions = exclusions if exclusions is not None else set([])
        self._min = min
        self._max = max

        self._credits_have = 0.0
        self._requirements_met = 0

        self._only_used = only_used
        self._only_unused = only_unused
        self._treatall = treatall

        self._used_courses = set([])
        self._reqmet = False
        self._taken = taken_courses
        self._breadth_count = breadth

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
        self._credits_have = 0.0
        self._requirements_met = 0

        for course in self._courses:
            if not self._treatall:
                # If not looking at every course possible
                if credits and self._credits_have >= self._max:
                    # If looking at credits count
                    break
                elif not credits and self._requirements_met >= self._max:
                    # If looking at passed courses count
                    break

            if isinstance(course, Requirement):
                # If a nested requirement
                course._update(used)  # Get the amount of the required satisfied

                if course._reqmet:  # If the amount satisfied is enough to satisfy
                    self._credits_have += course._credits_have
                    self._requirements_met += 1
                    used.update(course._used_courses)

            elif course[:2] == 'BR':
                # If a Breadth requirement
                self._credits_have += self._breadth_count[int(course[2]) - 1]

            elif '*' in course:
                # If a Abstract course
                for taken_course in self._taken:
                    # For every course which has been taken

                    if taken_course not in self._exclusions and self._taken[taken_course].is_passed() and is_same(course, taken_course):
                        # If course meets regular and abstract course requirements
                        self._add_to_requirement(taken_course, used)
                        break

            elif course in self._taken and course not in self._exclusions and self._taken[course].is_passed():
                # If a Regular course
                self._add_to_requirement(course, used)

        if credits and self.need <= self._credits_have:
            # If satisfied the requirement
            self._reqmet = True

            if self._credits_have > self._max:  # Makes it so cannot get the max of what we're looking for
                self._credits_have = self._max

        elif not credits and self.need <= self._requirements_met:
            # If satisfied the requirement
            self._reqmet = True

            if self._requirements_met > self._max:  # Makes it so cannot get the max of what we're looking for
                self._requirements_met = self._max

        else:
            # If did not satisfy the requirement
            self._reqmet = False

        return used

    def _get_min_mark(self, used):
        """
        Return list of courses used in the requirement
        Used to update the requirements of a min mark requirement

        :param set of str used: Courses previously used in other requirements
        :return: set of str
        """

        self._requirements_met = 0
        self._credits_have = 0.0

        if self._courses in self._taken and self._taken[self._courses].mark >= self.need:
            self._reqmet = True
            self._add_to_requirement(self._courses, used)

        else:
            self._reqmet = False

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

        if 'CREDITS' in self._modifier:
            return self._credits_have

        elif self._modifier == 'MARK':
            if self._courses in self._taken:
                return self._taken[self._courses]
            else:
                return 0

        else:
            return self._requirements_met

    def _add_to_requirement(self, course, used):
        """
        Regulate the adding of requirements

        :param str course: Course Code
        :param set of str used: Set of courses which have been previously used
        :return: NoneType
        """

        if self._only_used and course in used:
            self._credits_have += self._taken[course].weight
            self._requirements_met += 1

        elif self._only_unused and course not in used:
            self._credits_have += self._taken[course].weight
            self._requirements_met += 1
            used.add(course)

        else:
            self._credits_have += self._taken[course].weight
            self._requirements_met += 1
            used.add(course)

    modifier = property(_get_modifier)
    courses = property(_get_courses)
    update = property(_update)
    need = property(_get_need)
    have = property(_get_have)

    def __repr__(self):
        return 'Requirements(' + self._modifier + ' | N: ' + str(self.need) + ', H: ' + str(self.have) + ')'




# NEED A PRETTY SOPHISTICATED SYSTEM WHERE IT FINDS A MIN AND MAX OF COURSES NEEDED TO BE TAKEN