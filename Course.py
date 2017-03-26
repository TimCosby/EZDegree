class Course:
    """
    Creates Course Object

    Attributes:
    ===========
        @param dict _course_info:
                    All Course Info
        @param str ctype:
                    Current course process (ie. passed/failed)
        @param float cmark:
                    Mark for the course
        @param str ccode:
                    Course code
        @param str cname:
                    Course name
        @param str desc:
                    Course description
        @param str term:
                    Course term
        @param str div:
                    Arts&Sci/Engineering/Music
        @param str department:
                    Department of course (ie. Computer Science)
        @param str prerequisites:
                    Pre-requisites for the course
        @param str exclusions:
                    Exclusions for the course
        @param int level:
                    Course level (ie. 100/200/etc)
        @param str campus:
                    What campus the course is on
        @param str lecture_code:
                    Lecture code user is in (ie. L0101)
        @param int lecture_size:
                    Size of lecture
        @param list of dict lecture_times:
                    List of lecture dates, times, and places
        @param list lecture_instructors:
                    List of profs
        @param list of int breadths:
                    List of what breadth(s) value the course has
    """
    def __init__(self, course_info, lecture_code, ctype, cmark):
        self._course_info = course_info
        self.ctype = ctype
        self.cmark = cmark
        self.ccode = course_info['code']
        self.cname = course_info['name']
        self.desc = course_info['description']
        self.term = course_info['term']
        self.div = course_info['division']
        self.department = course_info['department']
        self.prerequisites = course_info['prerequisites']
        self.exclusions = course_info['exclusions']
        self.level = course_info['level']
        self.campus = course_info['campus']

        lecture_info = self._find_lecture(lecture_code)

        if lecture_info is not None:
            self.lecture_code = lecture_code
            self.lecture_size = lecture_info['size']
            self.lecture_times = lecture_info['times']
            self.lecture_instructors = lecture_info['instructors']
        else:
            print('Invalid course lecture!')

        self.breadths = course_info['breadths']

    def modify(self, lecture_code=None, ctype=None, cmark=None):
        """
        Modifies the course's type and mark values

        @param str lecture_code: Updated Lecture code
        @param str | None ctype: Updated Course Process
        @param float | None cmark: Updated Mark
        @return: None
        """

        # If lecture is changed
        if lecture_code is not None:
            lecture_info = self._find_lecture(lecture_code)

            # If lecture exists, update values
            if lecture_info is not None:
                self.lecture_code = lecture_info['code']
                self.lecture_size = lecture_info['size']
                self.lecture_times = lecture_info['times']
                self.lecture_instructors = lecture_info['instructors']
            else:
                print('Invalid course lecture!')

        if ctype is not None:
            self.ctype = ctype

        if cmark is not None:
            self.cmark = cmark

    def __repr__(self):
        return '(' + str(self._course_info) + ', \'' + str(self.lecture_code) + '\', \'' + str(self.ctype) + '\', ' + str(self.cmark) + ')'

    def _find_lecture(self, lecture_code):
        """
        Find if lecture code is valid
        Return lecture if valid
        Return None if invalid
         
        @param str lecture_code: Lecture code 
        @return: list of dict | None
        """

        for lecture in self._course_info['meeting_sections']:
            # If lecture exists
            if lecture['code'] == lecture_code:
                # If entered lecture code is in
                return lecture

        return None
