from Course import CourseNode


def _recur(courses, course_cache):
    """
    Recursively format dictionary into computer readable

    @param list | tuple courses: 
    @return: dict
    """
    temp = {}

    for course in courses:
        if isinstance(course, int):
            # If the number of courses needed to be taken in a list of courses
            pass

        elif isinstance(course, list):
            # If a list of ATLEAST this many courses in this list need to be taken
            need = course[-1]  # Get the number of courses needed (routinely stored at the end of the list)
            children = _recur(course, course_cache)  # Recurses through the list to get its children

            try:
                # If list is already in the dictionary add a new Node to the list
                temp['lists'].append(CourseNode(None, need=need, children=children))

            except KeyError:
                # If list is not yet in the dictionary add a new Node in a new list
                temp['lists'] = [CourseNode(None, need=need, children=children)]

        elif isinstance(course, tuple):
            # If a tuple of this AND this course need to be taken
            need = len(courses)  # Get the number of courses needed (All courses in the tuple are needed)
            children = _recur(course, course_cache)  # Recurses through the list to get its children

            try:
                # If list is already in the dictionary add a new Node to the list
                temp['lists'].append(CourseNode(None, need=need, children=children))

            except KeyError:
                # If list is not yet in the dictionary add a new Node in a new list
                temp['lists'] = [CourseNode(None, need=need, children=_recur(course, course_cache))]

        elif course[:2] == 'BR':
            # Creates the new node for the tree
            temp_course = CourseNode('\'' + course[:-1] + '\'', need=float(course[3:]))

            if course[:3] not in course_cache:
                # If breadth is not yet cached
                course_cache[course[:-1]] = temp_course

            # Ties all like-courses to the same id
            temp[course[:-1]] = course_cache[course[:-1]]

        else:
            # If just a regular course

            if course[-2] == 'H' or course[-2] == '*':
                # If a half course or non-specific
                need = .5
            else:
                # If a year course
                need = 1

            # Creates the new node for the tree
            temp_course = CourseNode('\'' + course + '\'', need=need)

            if course not in course_cache:
                # If course is not yet cached
                course_cache[course] = temp_course

            # Ties all like-courses to the same id
            temp[course] = course_cache[course]

    return temp


def build_tree(program_tree, course_cache):
    """
    Builds the course requirements and caches like-courses together
    Only runs at start up

    @return: dict
    """

    tree = {}

    for program in program_tree:
        # Add all the level courses together into one big list
        courses = []
        courses.extend(program_tree[program][1])
        courses.extend(program_tree[program][2])
        courses.extend(program_tree[program][3])
        courses.extend(program_tree[program][4])

        # Get the proper dictionary format
        tree.update({program: _recur(courses, course_cache)})

    return tree
