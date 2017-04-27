# NEED:
# MAX FCE
# MIN FCE
# MAX CREDITS
# MIN CREDITS
# MAX PASSING
# MIN PASSING
# MIN MARK
# EXCLUSIONS
# ABSTRACTS

# EXCLUSIONS -> ABSTRACTS -> MIN/MAX

# [Modifier, [courses]]

# Exclusions: in tuples

# Abstracts: has *s in them

# ['PASS', ('CSC4****'), blah, 2]

# min will return the most possible
# max will only return the set


class Requirement:
    """
    Attributes:
    ==========
        @param str modifier: The type of requirement for the group
        @param float need: Amount of modifier needed
        @param list of Course courses: Courses to be tested
    """

    def __init__(self, modifier, need, courses, exclusions=None):
        self._modifier = modifier
        self._courses = courses
        self.exclusions = exclusions if exclusions is not None else ()
        self._need = need

    def _get_have(self, list_=None):
        """
        Returns the amount of courses meeting the requirement of self

        @param list of Course|Requirement list_:
        @return: float
        """
        if list_ is None:
            list_ = self._get_courses()

        if self.modifier == 'MAXPASS' or self.modifier == 'MINPASS':
            return self._courses_passed(list_)

        elif self.modifier == 'MAXCREDITS' or self.modifier == 'MINCREDITS':
            return self._credits_passed(list_)

        elif self.modifier == 'MINMARK':
            return self._above_mark(list_)

    def _courses_passed(self, list_):
        """
        Return if the Courses in list_ meet self.need's requirements

        @param list of Course|Requirement list_: 
        @return: int
        """

        temp_passed = 0
        temp_credits = 0.0

        for item in list_:
            if isinstance(item, Requirement):
                temp = item.have

                if item.modifier == 'MINMARK' and temp[0] != 0 or temp[0 if item.modifier[3:] == 'CREDITS' else 1] >= item.need:
                    temp_passed += 1
                    temp_credits += temp[0]

            elif item.passed and item.course_code not in self.exclusions:
                temp_passed += 1
                temp_credits += item.weight

        if self.modifier == 'MINPASS' or temp_passed <= self.need:
            return temp_credits, temp_passed
        else:
            return temp_credits, self.need

    def _credits_passed(self, list_):
        temp_credits = 0.0

        for item in list_:
            if isinstance(item, Requirement):
                temp = item.have

                if temp[0] >= item.need:
                    temp_credits += temp[0]

            elif item.passed and item.course_code not in self.exclusions:
                temp_credits += item.weight

        if self.modifier == 'MINCREDITS' or temp_credits < self.need:
            return temp_credits, None
        else:
            return self.need, None

    def _above_mark(self, list_):
        if list_[0].mark >= self.need:
            return list_[0].weight, 1
        else:
            return 0.0, 0

    def _get_modifier(self):
        return self._modifier

    def _get_courses(self):
        return self._courses

    def _get_need(self):
        return self._need

    def _get_passed(self):

        if self.modifier == 'MAXPASS' or self.modifier == 'MINPASS':
            return self._get_have(self._get_courses())[1] >= self._need

        elif self.modifier == 'MAXCREDITS' or self.modifier == 'MINCREDITS':
            return self._get_have(self._get_courses()) >= self._need

    modifier = property(_get_modifier)
    courses = property(_get_courses)
    have = property(_get_have)
    need = property(_get_need)
    passed = property(_get_passed)

    def __repr__(self):
        return 'Requirements(' + self.modifier + ' | N: ' + str(self.need) + ', H: ' + str(self.have) + ')'





#if __name__ == '__main__':
    #usr = User()
