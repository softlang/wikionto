import unittest
from check.pos_firstsentence import HypNLPSent
from check.pos_firstsentence_auto import HypNLPSent as HypNLPSent2
from check.pos_summary import check_single as check2
from test import ignore_warnings
import requests


class TestHypernyms(unittest.TestCase):

    @ignore_warnings
    def test_positive_pattern1(self):
        session = requests.Session()
        cl, (pos, cop) = HypNLPSent().check_single(
            ("Java_(programming_language)", "Java is a general-purpose computer programming language that is "
                                            "concurrent, class-based, object-oriented, and specifically designed "
                                            "to have as few implementation dependencies as possible.", session))
        self.assertEqual("Java_(programming_language)", cl)
        self.assertEqual((["computer", "programming", "language", "implementation"], 'isa'), pos)
        self.assertEqual(["language"], cop)

    @ignore_warnings
    def test_negative_pattern1(self):
        session = requests.Session()
        cl, (pos, cop) = HypNLPSent().check_single(
            ("Pan", "The pan configuration language allows the definition of machine configuration information and an "
                    "associatedschema with a simple, human-accessible syntax.", session))
        self.assertEqual("Pan", cl)
        self.assertEqual((['pan', 'configuration', 'language'], 'The'), pos)
        self.assertEqual([], cop)

    @ignore_warnings
    def test_positive_pattern2(self):
        session = requests.Session()
        cl, (pos, cop) = HypNLPSent().check_single(
            ("ADSL", "ASDL is also a common misspelling of ADSL. Abstract-Type and "
                     "Scheme-Definition Language  is a computer language developed as part of "
                     "ESPRIT project GRASPIN, as a basis for generating language-based editors and "
                     "environments.", session))
        self.assertEqual("ADSL", cl)
        self.assertEqual((["misspelling", 'ADSL'], 'isa'), pos)
        self.assertEqual(["misspelling"], cop)

    @ignore_warnings
    def test_notation(self):
        session = requests.Session()
        cl, (pos, cop) = HypNLPSent().check_single(
            ("Abstract Syntax Notation One", "Abstract Syntax Notation One  is a standard and "
                                             "notation", session))
        self.assertEqual("Abstract Syntax Notation One", cl)
        self.assertEqual((["notation"], 'isa'), pos)
        self.assertEqual([], cop)  # standard gets tagged as JJ instead of NN as expected

    @ignore_warnings
    def test_html(self):
        session = requests.Session()
        cl, (pos, cop) = HypNLPSent().check_single(
            ("HTML", "HyperText Markup Language  is the standard markup language for creating web "
                     "pages and web applications.", session))
        self.assertEqual((['markup', 'language', 'web', 'web'], 'isa'), pos)
        self.assertEqual(["language"], cop)

    @ignore_warnings
    def test_templateengine(self):
        session = requests.Session()
        cl, (pos, cop) = HypNLPSent().check_single(("Mako", "Mako is a template engine written in Python.", session))
        self.assertEqual((['template', 'engine', 'Python'], 'isa'), pos)
        self.assertEqual(["engine"], cop)

    @ignore_warnings
    def test_positive_check2_pattern2(self):
        session = requests.Session()
        cl, (pos, cop) = check2(("ADSL", "ASDL is also a common misspelling of ADSL. Abstract-Type and "
                                         "Scheme-Definition Language is a computer language developed as part "
                                         "of ESPRIT project GRASPIN, as a basis for generating language-based editors "
                                         "and environments.", session))
        self.assertEqual("ADSL", cl)
        self.assertEqual(
            [['misspelling', 'ADSL'], 'isa', ['computer', 'language', 'part', 'ESPRIT', 'project', 'GRASPIN', 'basis'],
             'isa'], pos)
        self.assertEqual(['misspelling', 'language'], cop)

    @ignore_warnings
    def test_typeerror_check2(self):
        session = requests.Session()
        cl, (pos, cop) = check2(
            ("BPML", "BPML was a proposed language, but now the BPMI has dropped support for this in "
                     "favor of BPEL4WS (Business Process Execution Language for Web Services).As of "
                     "2008, BPML has also been reported to have been deprecated in favor of BPDM ("
                     "Business Process Definition Metamodel).BPMI took this decision when it was "
                     "acquired by OMG in order to gain access to its popular specification, "
                     "BPMN (Business Process Model and Notation).", session))
        self.assertEqual(
            [['language', 'BPMI', 'support', 'favor', 'BPEL4WS', 'Business', 'Execution', 'Language', 'Web'], 'isa', [],
             '', [], ''], pos)
        self.assertEqual(['language', 'dropped'], cop)

    @ignore_warnings
    def test_sndsent(self):
        session = requests.Session()
        cl, (pos, cop) = HypNLPSent().check_single(("SubRip", "SubRip is a software program for Windows which rips "
                                                              "subtitles and their timings from video. It is free "
                                                              "software, released under the GNU GPL. SubRip is also "
                                                              "the name of the widely used and broadly compatible "
                                                              "subtitle text file format created by this software."
                                                    , session))
        self.assertEqual((['software', 'program', 'Windows', 'video'], 'isa'), pos)
        cl, (pos, cop) = check2(("SubRip", "SubRip is a software program for Windows which rips "
                                           "subtitles and their timings from video. It is free "
                                           "software, released under the GNU GPL. SubRip is also "
                                           "the name of the widely used and broadly compatible "
                                           "subtitle text file format created by this software.", session))
        self.assertEqual(([['software', 'program', 'Windows', 'video'], 'isa', ['GNU', 'GPL'], 'isa',
                           ['subtitle', 'text', 'file', 'format', 'software'], 'isanameof']), pos)

    @ignore_warnings
    def test_Smarty(self):
        session = requests.Session()
        cl, (pos, cop) = HypNLPSent().check_single(("Smarty", "Smarty is a web template system written in PHP. Smarty "
                                                              "is primarily promoted as a tool for separation of "
                                                              "concerns.Smarty is intended to simplify "
                                                              "compartmentalization, allowing the front-end of a web "
                                                              "page to change separately from its back-end. Ideally, "
                                                              "this lowers costs and minimizes the efforts associated "
                                                              "with software maintenance. Smarty generates web "
                                                              "content through the placement of special Smarty tags "
                                                              "within a document. These tags are processed and "
                                                              "substituted with other code. Tags are directives for "
                                                              "Smarty that are enclosed by template delimiters. These "
                                                              "directives can be variables, denoted by a dollar sign "
                                                              ", functions, logical or loop statements. Smarty allows "
                                                              "PHP programmers to define custom functions that can be "
                                                              "accessed using Smarty tags.", session))
        self.assertEqual((['web', 'template', 'system', 'PHP'], 'isa'), pos)
        self.assertEqual(["system"], cop)

    @ignore_warnings
    def test_templateengineCap(self):
        session = requests.Session()
        cl, (pos, cop) = HypNLPSent().check_single(("FreeMarker", "FreeMarker is a Java-based Template Engine, "
                                                                  "originally focusing on dynamic web page generation "
                                                                  "with MVC software architecture. However, "
                                                                  "it's a general purpose template engine, "
                                                                  "with no dependency on servlets or HTTP or HTML, "
                                                                  "and so it's often used for generating source code, "
                                                                  "configuration files or e-mails. FreeMarker is Free "
                                                                  "software.", session))
        self.assertEqual(
            (['Template', 'Engine', 'web', 'page', 'generation', 'MVC', 'software', 'architecture'], 'isa'), pos)
        self.assertEqual([], cop)

    @ignore_warnings
    def test_yacc(self):
        session = requests.Session()
        cl, (pos, cop) = check2(("Yacc", "Yacc is a computer program for the Unix operating "
                                         "system. It is a Look Ahead Left-to-Right  parser "
                                         "generator, generating a parser, the part of a compiler "
                                         "that tries to make syntactic sense of the source code, "
                                         "specifically a LALR parser, based on an analytic grammar "
                                         "written in a notation similar to Backus–Naur Form . Yacc "
                                         "itself used to be available as the default parser "
                                         "generator on most Unix systems, though it has since been "
                                         "supplanted as the default by more recent, "
                                         "largely compatible, programs.", session))
        self.assertEqual([['computer', 'program', 'Unix', 'operating', 'system'], 'isa',
                          ['Look', 'Ahead', 'Left-to-Right', 'parser', 'generator', 'parser', 'part', 'compiler',
                           'sense', 'source', 'code',
                           'LALR',
                           'parser', 'grammar', 'notation', 'Backus', 'Naur', 'Form'], 'isa',
                          [], ''], pos)
        self.assertEqual(['program', 'generator'], cop)

    @ignore_warnings
    def test_racket(self):
        session = requests.Session()
        cl, (pos, cop) = HypNLPSent().check_single(
            ("Racket", "Racket  is a general purpose, multi-paradigm programming language in the "
                       "Lisp-Scheme family.", session))
        self.assertEqual((['purpose', 'programming', 'language', 'Lisp-Scheme', 'family'], 'isa'), pos)
        self.assertEqual(['purpose'], cop)

    @ignore_warnings
    def test_pan(self):
        session = requests.Session()
        cl, (pos, cop) = HypNLPSent().check_single(
            ("Pan", "The pan  configuration language allows the definition of machine configuration information."
             , session))
        self.assertEqual((['pan', 'configuration', 'language'], 'The'), pos)
        self.assertEqual([], cop)

    @ignore_warnings
    def test_isabelle(self):
        session = requests.Session()
        cl, (pos, cop) = HypNLPSent().check_single(
            ("Isabelle", "The Isabelle theorem prover is an interactive theorem prover.", session))
        self.assertEqual((['theorem', 'prover'], 'The'), pos)
        self.assertEqual(['prover'], cop)

    @ignore_warnings
    def test_islandgrammar(self):
        session = requests.Session()
        cl, (pos, cop) = HypNLPSent().check_single(
            ("Island_grammar",
             "An island grammar is a grammar that only describes a small chunk of the underlying language.", session))
        self.assertEqual((['grammar', 'chunk', 'language'], 'isa'), pos)
        self.assertEqual(['grammar'], cop)

    @ignore_warnings
    def test_ATS(self):
        session = requests.Session()
        cl, (pos, cop) = HypNLPSent().check_single(
            ("ATS",
             "ATS  is a programming language designed to unify programming with formal specification.", session))
        self.assertEqual((['programming', 'language', 'programming', 'specification'], 'isa'), pos)
        self.assertEqual(['language'], cop)

    @ignore_warnings
    def test_negative_pattern_auto(self):
        session = requests.Session()
        cl, (pos, cop) = HypNLPSent2().check_single(
            ("Pan", "The pan configuration language allows the definition of machine configuration information and an "
                    "associatedschema with a simple, human-accessible syntax.", session))
        self.assertEqual("Pan", cl)
        self.assertEqual(['pan', 'configuration', 'language'], pos["The"])

    @ignore_warnings
    def test_negative_pattern_auto(self):
        session = requests.Session()
        cl, (pos, cop) = HypNLPSent2().check_single(
            ("Perl6", "Perl 6 is a member of the Perl family of programming languages.", session))
        self.assertEqual("Perl6", cl)
        self.assertEqual(['family', 'languages'], pos["ismemberof"])

if __name__ == '__main__':
    TestHypernyms.main()
