from xlutils.copy import copy
from xlrd import open_workbook

class User:
    """
    Creates User Object

    Attributes:
    ===========
        @param str _username:
                        username of user
        @param str _password:
                        password of user
        @param Book _write_book:
                        Writable book version of the database
        @param sheet _write_sheet:
                        Writable sheet .xls of _write_book
        @param int _user_row:
                        Row that the user is in, in the database
        @param bool _logged_in:
                        Whether or not the user has logged in successfully
    """

    def __init__(self, username, password):
        self._username = username.strip().lower()
        self._password = password.strip()

        self._write_book = copy(open_workbook('database.xls'))
        self._write_sheet = self._write_book.get_sheet(0)

        self._user_row = 0

        self._logged_in = False
        self._login()

    def _login(self):
        """
        Attempts to log the user in based on given username and password.

        If username does not exist in database, ask user if they want to
        create a new user.

        @return: None
        """
        read_book = open_workbook('database.xls')
        read_sheet = read_book.sheet_by_index(0)

        for row in range(read_sheet.nrows):
            # Checks every row for a corresponding username
            if read_sheet.cell(row, 0).value.lower() == self._username:
                # If username is recognized in the database
                if read_sheet.cell(row, 1).value == self._password:
                    # If password and username are the same as the database
                    self._logged_in = True
                    self._user_row = row
                    print('Successfully logged in!\n')
                    break
                else:
                    # If wrong password was entered
                    raise Exception('Invalid password!')

        if not self._logged_in:
            # If username DNE in database
            ans = input('Do you want to create a new user Y/N\n').lower()
            if 'y' in ans:
                self._create_new_user(read_sheet)

    def _create_new_user(self, read_sheet):
        """
        Creates a new user in the database

        @param sheet read_sheet:
        @return: None
        """
        print('Creating an account\n')
        self._write_sheet.write(read_sheet.nrows, 0, self._username)
        self._write_sheet.write(read_sheet.nrows, 1, self._password)
        self._write_book.save('database.xls')
        self._user_row = read_sheet.nrows
        self._logged_in = True

    def get_logged_in(self):
        """
        Returns whether or not the user successfully logged in.

        @return: bool
        """
        return self._logged_in

    def add_course(self, course, type):
        """
        Add or modify <course> in the user's list of courses

        To-Do:
        Course added from GUI Interface - Would need an add button as course
        and type need to be exact.

        @param str course: course code to be added
        @param str type:
        @return: None
        """

        read_book = open_workbook('database.xls')
        read_sheet = read_book.sheet_by_index(0)

        max_col = read_sheet.ncols
        for column in range(read_sheet.ncols):
            # Finds the user's first empty column or the pre-existing course
            if read_sheet.row(self._user_row)[column].value == '' or read_sheet.row(self._user_row)[column].value.split(':')[0] == course:
                max_col = column
                break

        self._write_sheet.write(self._user_row, max_col, course + ':' + type)
        self._write_book.save('database.xls')

    def get_courses(self):
        """
        Return all courses the user has entered

        @return: list of str
        """
        temp = []
        read_sheet = open_workbook('database.xls').sheet_by_index(0)

        for col in range(2, read_sheet.ncols):
            cell_value = read_sheet.cell(self._user_row, col).value
            if cell_value != '':
                temp.append(cell_value)
            else:
                break

        return temp

    def __str__(self):
        """
        Return user's course list

        @return: str
        """
        temp = ''

        for course in self.get_courses():
            temp += course.split(':')[0] + ', '

        return temp[:-2]


def correction(search):
    """
    Return possible course_codes the user possibly wanted to enter

    @param str search:
    @return: list of str
    """
    from urllib.request import urlopen
    from urllib.request import Request
    import ast

    page = 'https://cobalt.qas.im/api/1.0/courses/filter?q=code:%22' + search + '%22'

    pr = Request(page)
    ### Enters Key
    pr.add_header('Authorization', 'TVwEIjRZP80vhnY8HhM0OzZCMfydh4lA')

    file = urlopen(pr)

    temp = ast.literal_eval(file.read().decode('utf-8'))

    temper = []
    for i in temp:
        temper.append(i['code'])

    return temper

if __name__ == '__main__':
    # Loops until you successfully log in
    while True:
        username = input('Enter your username: ')
        password = input('Enter your password: ')
        try:
            # Logs in
            user = User(username, password)

            # Checks to see if you successfully logged in
            if user.get_logged_in():
                break
        except Exception as e:
            print(e)

    course = None
    while course != 'exit':
        if course is not None:
            user.add_course(course, type)
            print('Courses:', user)

        course = input('What course would you like to add? or do you want to exit?\n')

        if course != 'exit':
            temp = correction(course)

            if not course in temp:
                # If entered is not identical to the database
                print('Did you mean ' + str(temp)[1:-1] + '?')
                course = None
            else:
                type = input('Is the course current/taken/planned\n')
