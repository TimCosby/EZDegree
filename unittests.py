import unittest
import User

USR = User.User('Test', 'Test')
USR.add_course('CSC108H1')
USR.set_mark('CSC108H1', 80)
USR.add_course('CSC148H1')
USR.set_mark('CSC148H1', 80)
USR.add_course('CSC165H1')
USR.set_mark('CSC165H1', 80)


class TestStringMethods(unittest.TestCase):

    def test_credits_max(self):
        results = USR.get_program_requirements('CREDITSMAX')
        self.assertTrue(results._reqmet)

    def test_credits_min(self):
        results = USR.get_program_requirements('CREDITSMIN')
        self.assertTrue(results._reqmet)

    def test_credits_treatall(self):
        results = USR.get_program_requirements('CRTREATALL')
        self.assertTrue(results._reqmet)
        self.assertTrue(len(results._used_courses) == 3)

    def test_credits_only_used(self):
        results = USR.get_program_requirements('CREDITS_ONLYUSED_TRUE')
        self.assertTrue(results._reqmet)

        results = USR.get_program_requirements('CREDITS_ONLYUSED_FALSE')
        self.assertFalse(results._reqmet)

    def test_credits_only_unused(self):
        results = USR.get_program_requirements('CREDITS_ONLYUNUSED_TRUE')
        self.assertTrue(results._reqmet)

        results = USR.get_program_requirements('CREDITS_ONLYUNUSED_FALSE')
        self.assertFalse(results._reqmet)

    def test_credits_exclusions(self):
        results = USR.get_program_requirements('CREDITS_EXCLUSIONS_TRUE')
        self.assertTrue(results._reqmet)

        results = USR.get_program_requirements('CREDITS_EXCLUSIONS_FALSE')
        self.assertFalse(results._reqmet)

    def test_abstract_credit(self):
        results = USR.get_program_requirements('CREDITS_ABSTRACT_TRUE')
        self.assertTrue(results._reqmet)

        results = USR.get_program_requirements('CREDITS_ABSTRACT_TEXTRA')
        self.assertTrue(results._reqmet)

        results = USR.get_program_requirements('CREDITS_ABSTRACT_FALSE')
        self.assertFalse(results._reqmet)

    def test_courses_max(self):
        results = USR.get_program_requirements('COURSESMAX_TRUE')
        self.assertTrue(results._reqmet)

        results = USR.get_program_requirements('COURSESMAX_FALSE')
        self.assertFalse(results._reqmet)

    def test_courses_min(self):
        results = USR.get_program_requirements('COURSESMIN_TRUE')
        self.assertTrue(results._reqmet)

        results = USR.get_program_requirements('COURSESMIN_FALSE')
        self.assertFalse(results._reqmet)

    def test_courses_treatall(self):
        results = USR.get_program_requirements('COTREATALL')
        self.assertTrue(results._reqmet)
        self.assertTrue(len(results._used_courses) == 3)

    def test_courses_only_used(self):
        results = USR.get_program_requirements('COURSES_ONLYUSED_TRUE')
        self.assertTrue(results._reqmet)

        results = USR.get_program_requirements('COURSES_ONLYUSED_FALSE')
        self.assertFalse(results._reqmet)

    def test_courses_only_unused(self):
        results = USR.get_program_requirements('COURSES_ONLYUNUSED_TRUE')
        self.assertTrue(results._reqmet)

        results = USR.get_program_requirements('COURSES_ONLYUNUSED_FALSE')
        self.assertFalse(results._reqmet)

    def test_courses_exclusions(self):
        results = USR.get_program_requirements('COURSES_EXCLUSIONS_TRUE')
        self.assertTrue(results._reqmet)

        results = USR.get_program_requirements('COURSES_EXCLUSIONS_FALSE')
        self.assertFalse(results._reqmet)

    def test_abstract_course(self):
        results = USR.get_program_requirements('COURSES_ABSTRACT_TRUE')
        self.assertTrue(results._reqmet)

        results = USR.get_program_requirements('COURSES_ABSTRACT_FALSE')
        self.assertFalse(results._reqmet)

    def test_breadth(self):
        results = USR.get_program_requirements('BREADTH_TRUE')
        self.assertTrue(results._reqmet)

        results = USR.get_program_requirements('BREADTH_FALSE')
        self.assertFalse(results._reqmet)

    def mark(self):
        results = USR.get_program_requirements('MARK_TRUE')
        self.assertTrue(results._reqmet)

        results = USR.get_program_requirements('MARK_FALSE')
        self.assertFalse(results._reqmet)


if __name__ == '__main__':
    unittest.main()
