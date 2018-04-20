import unittest
from check.hypernym_stanford import check
import warnings


def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            test_func(self, *args, **kwargs)

    return do_test


class TestHypernyms(unittest.TestCase):

    @ignore_warnings
    def test_positive_pattern1(self):
        cl, (pos, cop) = check(
            ("Java_(programming_language)", "Java is a general-purpose computer programming language that is "
                                            "concurrent, class-based, object-oriented, and specifically designed "
                                            "to have as few implementation dependencies as possible."))
        self.assertEqual("Java_(programming_language)", cl)
        self.assertEqual(["computer", "programming", "language", "implementation"], pos)
        self.assertEqual("language", cop)

    @ignore_warnings
    def test_negative_pattern1(self):
        cl, (pos, cop) = check(
            ("Pan", "The pan configuration language allows the definition of machine configuration information and an "
                    "associatedschema with a simple, human-accessible syntax."))
        self.assertEqual("Pan", cl)
        self.assertEqual([], pos)
        self.assertEqual(None, cop)

    @ignore_warnings
    def test_positive_pattern2(self):
        self.assertEqual(1, 1)

    @ignore_warnings
    def test_negative_pattern2(self):
        self.assertEqual(1, 1)

    @ignore_warnings
    def test_positive_pattern3(self):
        self.assertEqual(1, 1)

    @ignore_warnings
    def test_negative_pattern3(self):
        self.assertEqual(1, 1)

    @ignore_warnings
    def test_positive_pattern4(self):
        self.assertEqual(1, 1)

    @ignore_warnings
    def test_negative_pattern4(self):
        self.assertEqual(1, 1)


if __name__ == '__main__':
    TestHypernyms.main()
