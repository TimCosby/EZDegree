import IO
import data_manipulation

SEARCH_LIMIT = -1 # Limits how many search results show up #Make a positive number to limit it to that number

def does_course_exist(courses, attempt, entered_courses):
    """
    (list of str, str, list of str) -> str

    Checks to see if entered course exists.
    If more than one instance exists, suggest a list of all the possibilities
    Modifies entered_courses if course exists

    >>> entered_courses = []
    >>> does_course_exist(['ABS100H1','ABS200H1','CSC400H1'], 'ABS2', entered_courses)
    >>> entered_courses
    ['ABS200H1']
    """

    matches = []
    for items in range(len(courses)):
        # Finds all matches of entered string
        if len(matches) == SEARCH_LIMIT or len(attempt) == 0:
            break
        elif attempt == courses[items][:len(attempt)]:
            matches.append(courses[items])

    if len(matches) > 1:
        # If theres more than one match to the entered string
        print('Did you mean:')
        for i in range(len(matches)):
            # Lists possible courses
            if i != len(matches) - 1:
                print(matches[i] + ', ', end='')
            else:
                print('or ' + matches[i])

        # Retests to find the correct course using recursion
        does_course_exist(courses,input('Retype the course:\n').upper(),entered_courses)

    elif attempt == 'EXIT':
        # If exit is performed
        return 'EXIT'

    elif len(matches) == 0:
        # If no course matching the attempt exists
        print('Error: No course found.\n')
        does_course_exist(courses, IO.get_course().upper(), entered_courses)

    else:
        # If only one matching course exists, immediately adds it to the array
        entered_courses.append(matches[0])


if __name__ == '__main__':
    attempt = ''
    courses = data_manipulation.get_all_courses()
    entered_courses = []

    while attempt != ('EXIT'):
        # While exit hasn't been performed
        attempt = IO.get_course().upper()
        # Checks to see if the entered course exists
        does_course_exist(courses, attempt, entered_courses)
    entered_courses.sort()

    print(entered_courses)