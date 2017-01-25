from tkinter import *

class Check_Box_State(Frame):
    def __init__(self, parent=None, checks = [], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.vars=[]


        for pick in checks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, var=var)
            chk.pack(side=side, anchor=anchor, expand=YES)
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)

class GUI_Objects(Frame):

    def __init__(self, parent=None):
        Frame.__init__(self, parent)

    def add_checkbox(self, master, tex='', arr=[]):
        """
        Makes a checkbox on the frame
        tex = Label Name
        arr = Possible inputs

        @param master: Tk
        @param tex: str
        @param arr: inputs
        @return: CheckButton
        """

        Label(master, text=tex).pack(fill=X)
        check_box = Check_Box_State(master, arr)
        check_box.pack()

        return check_box

    def add_scale(self, master, tex='', start=0, end=0):
        Label(master, text=tex).pack(fill=X)
        scale = Scale(master, from_=start, to_=end, orient=HORIZONTAL)
        scale.pack()
        return scale

    def add_text_field(self, master, tex):
        Label(master, text=tex).pack(fill=X)
        search = Entry(master)
        search.pack()
        return search


class Main_Builder(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.gui = GUI_Objects(master)

        self.breadth = self.gui.add_checkbox(master, 'Breadth', [1, 2, 3, 4, 5])

        self.term = self.gui.add_checkbox(master, 'Term', ['Fall', 'Winter'])

        self.course_level = self.gui.add_checkbox(master, 'Course Level', ['100', '200', '300', '400'])

        self.day = self.gui.add_checkbox(master, 'Day of the Week', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])

        self.startime = self.gui.add_scale(master, 'Start After', 1, 24)

        self.endtime = self.gui.add_scale(master, 'End Before', 1, 24)

        self.search = self.gui.add_text_field(master, 'Search for (3 letter course code or name)')

    @property
    def breadth(self):
        return self._breadth
    @breadth.getter
    def breadth(self):
        return list(self._breadth.state())
    @breadth.setter
    def breadth(self, input):
        self._breadth = input

    @property
    def course_level(self):
        return self._course_level
    @course_level.getter
    def course_level(self):
        return list(self._course_level.state())
    @course_level.setter
    def course_level(self, input):
        self._course_level = input

    @property
    def day(self):
        return self._day
    @day.getter
    def day(self):
        return list(self._day.state())
    @day.setter
    def day(self, input):
        self._day = input

    @property
    def endtime(self):
        return self._endtime
    @endtime.getter
    def endtime(self):
        return self._endtime.get()
    @endtime.setter
    def endtime(self, input):
        self._endtime = input

    @property
    def search(self):
        return self._search
    @search.getter
    def search(self):
        return self._search.get()
    @search.setter
    def search(self, input):
        self._search = input

    @property
    def startime(self):
        return self._startime
    @startime.getter
    def startime(self):
        return self._startime.get()
    @startime.setter
    def startime(self, input):
        self._startime = input

    @property
    def term(self):
        return self._term
    @term.getter
    def term(self):
        return list(self._term.state())
    @term.setter
    def term(self, input):
        self._term = input


"""class CouseBuilder(Frame):
    def __init__(self, course_window=None):
        Frame.__init__(self, course_window)

        self.gui = GUI_Objects(course_window)




def course_list(courses):
    course_window = Tk()
"""





def allstates(obj):
    """
    Takes in all the options and runs the output

    @param obj: interface
    @return: NoneType
    """

    from CourseGrabber import make_search
    courses = make_search(obj.breadth, obj.term, obj.course_level, obj.day, obj.startime, obj.endtime, obj.search)

    print(courses)
    for items in courses:
        print(items)

    return courses

if __name__ == '__main__':
    master = Tk()

    interface = Main_Builder(master)

    courses = Button(master, text='SEARCH!', command=lambda: allstates(interface)).pack(side=BOTTOM)

    master.mainloop()
