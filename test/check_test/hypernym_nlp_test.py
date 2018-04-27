import unittest
from check.hypernym_nlp_firstsentence import check
from check.hypernym_nlp_summary import check as check2
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
        self.assertEqual(["language"], cop)

    @ignore_warnings
    def test_negative_pattern1(self):
        cl, (pos, cop) = check(
            ("Pan", "The pan configuration language allows the definition of machine configuration information and an "
                    "associatedschema with a simple, human-accessible syntax."))
        self.assertEqual("Pan", cl)
        self.assertEqual([], pos)
        self.assertEqual([], cop)

    @ignore_warnings
    def test_positive_pattern2(self):
        cl, (pos, cop) = check(("ADSL", "ASDL is also a common misspelling of ADSL. Abstract-Type and "
                                        "Scheme-Definition Language  is a computer language developed as part of "
                                        "ESPRIT project GRASPIN, as a basis for generating language-based editors and "
                                        "environments."))
        self.assertEqual("ADSL", cl)
        self.assertEqual(["misspelling"], pos)
        self.assertEqual(["misspelling"], cop)

    @ignore_warnings
    def test_notation(self):
        cl, (pos, cop) = check(("Abstract Syntax Notation One", "Abstract Syntax Notation One  is a standard and "
                                                                "notation"))
        self.assertEqual("Abstract Syntax Notation One", cl)
        self.assertEqual(["notation"], pos)
        self.assertEqual([], cop)  # standard gets tagged as JJ instead of NN as expected

    @ignore_warnings
    def test_html(self):
        cl, (pos,cop) = check(("HTML","HyperText Markup Language  is the standard markup language for creating web "
                                      "pages and web applications."))
        self.assertEqual(['markup', 'language', 'web', 'web'], pos)
        self.assertEqual(["language"], cop)

    @ignore_warnings
    def test_templateengine(self):
        cl, (pos, cop) = check(("Mako", "Mako is a template engine written in Python."))
        self.assertEqual(['template', 'engine'], pos)
        self.assertEqual(["engine"], cop)

    @ignore_warnings
    def test_positive_check2_pattern2(self):
        cl, (pos, cop) = check2(("ADSL", "ASDL is also a common misspelling of ADSL. Abstract-Type and "
                                         "Scheme-Definition Language is a computer language developed as part "
                                         "of ESPRIT project GRASPIN, as a basis for generating language-based editors "
                                         "and environments."))
        self.assertEqual("ADSL", cl)
        self.assertEqual(['misspelling', 'computer', 'language', 'part', 'project', 'basis'], pos)
        self.assertEqual(['misspelling', 'language'], cop)

    @ignore_warnings
    def test_typeerror_check2(self):
        cl, (pos,cop) = check2(("BPML","BPML was a proposed language, but now the BPMI has dropped support for this in "
                                      "favor of BPEL4WS (Business Process Execution Language for Web Services).As of "
                                      "2008, BPML has also been reported to have been deprecated in favor of BPDM ("
                                      "Business Process Definition Metamodel).BPMI took this decision when it was "
                                      "acquired by OMG in order to gain access to its popular specification, "
                                      "BPMN (Business Process Model and Notation)."))
        self.assertEqual(['language', 'support', 'favor', 'BPEL4WS', 'Business', 'Web'], pos)
        self.assertEqual(['language', 'dropped'], cop)


if __name__ == '__main__':
    TestHypernyms.main()
