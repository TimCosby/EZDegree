from ast import literal_eval
from copy import deepcopy
from Course import CourseNode

TEST_COURSES = {'CSC108', 'CSC401', 'ENG250Y1'}

class Programs:
    def __init__(self):
        self.programs = self._get_programs()
        self._extras = self.programs.pop('ELG')

        for program in self.programs:
            # For each program
            for index in range(1, 5):
                # For each level of requirements, replace the extra group of courses with their proper courses
                self.programs[program][index] = self._define_requirements(self.programs[program][index])

        open('data.dat', 'w').write(str(self.programs))

    def _remove_not_matching(self, index, char, courses, istuple=False):
        """
        
        @param int index: 
        @param str char: 
        @param list | tuple courses: 
        @return: list | None
        """
        if isinstance(courses, tuple):
            # Get the absolute length needed in the tuple (ie. If one course goes, they all go)
            abs_length = len(courses)


        course = 0
        while len(courses) != course:
            # While there are more courses to look at

            if isinstance(courses[course], int):
                # When the input is a indicator about how many courses are needed from the list
                pass

            elif isinstance(courses[course], list) or isinstance(courses[course], tuple):
                # If a group of courses
                if isinstance(courses[course], tuple):
                    result = self._remove_not_matching(index, char, courses[course], istuple=True)  # Recurse through the lists
                else:
                    result = self._remove_not_matching(index, char, courses[course])  # Recurse through the lists

                if result is not None:
                    # If the list didn't come back empty
                    courses[course] = result

                else:
                    # If the list is empty then remove it *boom*
                    courses.pop(course)
                    course -= 1

            elif courses[course][index] != char:
                # Remove the course doesn't have <char> at the proper index
                courses.pop(course)
                course -= 1

            course += 1


        if len(courses) == 0:
            # If the list of courses is completely empty - remove it
            return None

        elif isinstance(courses, tuple) and len(courses) != abs_length:
            # If a group(tuple) of courses that do not have their original amount of courses needed to group
            return None

        elif isinstance(courses[-1], int) and len(courses) - 1 < courses[-1]:
            # If a list of courses with less courses than needed from the group
            return None

        if istuple:
            return tuple(courses)
        else:
            return courses  # If there's no problems with the group of courses

    def _define_requirements(self, requirements, istuple=False):
        """
        Searches through program requirements and replaces any group requirements with the proper courses
        Return the updated list
        
        @param list | tuple requirements: A single level of a program's requirements
        @return: list
        """

        temp = []

        for course in requirements:
            # For course in requirements

            if isinstance(course, int):
                # If the number of courses needed in the square brackets
                temp.append(course)

            elif isinstance(course, list):
                # If defined grouped courses that have to be taken together
                temp.append(self._define_requirements(course))

            elif isinstance(course, tuple):
                temp.append(self._define_requirements(course, istuple=True))

            elif course[:3] == 'ELG':
                # If course is shortened for a group of courses

                temp_courses = deepcopy(self._extras[course[4:7]][:])  # Do the most frustrating copy of a list ever

                for index in range(8):
                    # For each character in a course code
                    char = course[8 + index]

                    if char == '*':
                        # If required character is not defined
                        pass

                    else:
                        # Get rid of all courses that do not have the character in the proper index
                        self._remove_not_matching(index, char, temp_courses)

                        if temp_courses is None:
                            # If the list comes back empty
                            break

                if temp_courses is not None:
                    # If the list didn't come back empty
                    temp += temp_courses

            else:
                # If a regular course
                temp.append(course)

        if istuple:
            return tuple(temp)
        else:
            return temp

    def _get_programs(self):
        """
        Get a dictionary of all programs
        
        :param Program self:
        @return: dict
        """
        file = open('programs.txt', 'r').readlines()  # Get programs
        programs = {}

        for line in file:
            if line[0] != '@':
                programs.update(literal_eval(line))  # Convert non-comments to dictionaries

        return programs

    def __str__(self):
        return str(self.programs)

if __name__ == '__main__':
    Programs()