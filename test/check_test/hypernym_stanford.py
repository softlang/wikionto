import unittest
from check.hypernym_stanford import check


class TestPOSHypernyms(unittest.TestCase):

    def test_positive_pattern1(self):
        cl,(pos,cop) = check(("Java_(programming_language)","Java is a general-purpose computer programming language that is "
                                                "concurrent, class-based, object-oriented, and specifically designed "
                                                "to have as few implementation dependencies as possible."))
        self.assertEquals("Java_(programming_language)",cl)
        self.assertEquals(["computer","programming","language","implementation","dependencies"],pos)

    def test_negative_pattern1(self):
        cl, (pos, cop) = check(
            ("Pan", "The pan configuration language allows the definition of machine configuration information and an "
                    "associatedschema with a simple, human-accessible syntax."))
        self.assertEquals("Pan", cl)
        self.assertEquals([], pos)

    def test_positive_pattern2(self):
        self.assertEquals(1,1)

    def test_negative_pattern2(self):
        self.assertEquals(1,1)

    def test_positive_pattern3(self):
        self.assertEquals(1,1)

    def test_negative_pattern3(self):
        self.assertEquals(1,1)

    def test_positive_pattern4(self):
        self.assertEquals(1,1)

    def test_negative_pattern4(self):
        self.assertEquals(1,1)


if __name__ == '__main__':
    TestPOSHypernyms.main()