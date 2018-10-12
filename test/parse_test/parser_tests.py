import unittest
from mine_dump.extract_features import extract_first_sentence, extract_infobox_names, extract_hypernyms
import mine_dump.my_parsers as myparser
from test import ignore_warnings
from pathlib import Path


class TestParsing(unittest.TestCase):

    @ignore_warnings
    def test_sentence_autism(self):
        text = Path('autism').read_text(encoding='UTF-8')
        fs = extract_first_sentence(text)
        self.assertTrue('{{' not in fs)

    @ignore_warnings
    def test_sentence2_autism(self):
        text = Path('autism').read_text(encoding='UTF-8')
        fs = myparser.extract_first_sentence(text)
        self.assertEqual('Autism,"         Autism is a developmental disorder characterized by troubles with social '
                         'interaction and communication and by restricted and repetitive behavior.', fs)

    @ignore_warnings
    def test_infobox_autism(self):
        text = Path('autism').read_text(encoding='UTF-8')
        # print(text)
        names = extract_infobox_names(text)
        self.assertEqual('infobox medical condition (new)\\n', names)

    @ignore_warnings
    def test_infobox2_autism(self):
        text = Path('autism').read_text(encoding='UTF-8')
        # print(text)
        names = myparser.extract_names(text)
        self.assertEqual('infobox medical condition', names)

    @ignore_warnings
    def test_sentence_opendocument(self):
        text = Path('opendocument').read_text(encoding='UTF-8')
        fs = extract_first_sentence(text)
        exp = "The Open Document Format for Office Applications (ODF), also known as OpenDocument, is a " \
              "ZIP-compressedExtract an odt file with unzip on Linux to see the actual resource hierarchy XML-based " \
              "file format for spreadsheets, charts, presentations and word processing documents."
        self.assertEqual(exp, fs)

    @ignore_warnings
    def test_sentence2_opendocument(self):
        text = Path('opendocument').read_text(encoding='UTF-8')
        fs = myparser.extract_first_sentence(text)
        exp = "The Open Document Format for Office Applications , also known as OpenDocument, is a " \
              "ZIP-compressed XML-based " \
              "file format for spreadsheets, charts, presentations and word processing documents."
        self.assertEqual(exp, fs)

    @ignore_warnings
    def test_sentence2_ankara(self):
        text = Path('Ankara').read_text(encoding='UTF-8')
        fs = myparser.extract_first_sentence(text)
        exp = "Ankara , historically known as Ancyra and Angora, is the capital of the Republic of Turkey."
        self.assertEqual(exp, fs)

    @ignore_warnings
    def test_sentence_blacksabath(self):
        text = Path('blacksabath').read_text(encoding='UTF-8')
        fs = extract_first_sentence(text)
        exp = "Black Sabbath were an English rock band, formed in Birmingham in 1968, by guitarist and main " \
              "songwriter Tony Iommi, bassist and main lyricist Geezer Butler, drummer Bill Ward and singer " \
              "Ozzy Osbourne."
        self.assertEqual(exp, fs)

    @ignore_warnings
    def test_sentence2_blacksabath(self):
        text = Path('blacksabath').read_text(encoding='UTF-8')
        fs = myparser.extract_first_sentence(text)
        exp = "Black Sabbath were an English rock band, formed in Birmingham in 1968, by guitarist and main " \
              "songwriter Tony Iommi, bassist and main lyricist Geezer Butler, drummer Bill Ward and singer " \
              "Ozzy Osbourne."
        self.assertEqual(exp, fs)

    @ignore_warnings
    def test_hyp_opendocument(self):
        text = Path('opendocument').read_text(encoding='UTF-8')
        fs = myparser.extract_first_sentence(text)
        exp = "The Open Document Format for Office Applications , also known as OpenDocument, is a " \
              "ZIP-compressed XML-based " \
              "file format for spreadsheets, charts, presentations and word processing documents."
        self.assertEqual(exp, fs)
        hyps = extract_hypernyms(fs)
        self.assertEqual('file,format,word,processing; isa', hyps)

    @ignore_warnings
    def test_infobox_opendocument(self):
        text = Path('opendocument').read_text(encoding='UTF-8')
        # print(text)
        names = extract_infobox_names(text)
        self.assertEqual('infobox, infobox, infobox, infobox', names)

    @ignore_warnings
    def test_infobox2_opendocument(self):
        text = Path('opendocument').read_text(encoding='UTF-8')
        # print(text)
        names = myparser.extract_names(text)
        self.assertEqual('infobox, infobox, infobox, infobox', names)

    @ignore_warnings
    def test_infobox2_ankara(self):
        text = Path('Ankara').read_text(encoding='UTF-8')
        # print(text)
        names = myparser.extract_names(text)
        self.assertEqual('infobox settlement, infobox', names)

    @ignore_warnings
    def test_infobox_xml(self):
        text = Path('XML').read_text(encoding='UTF-8')
        # print(text)
        names = extract_infobox_names(text)
        self.assertEqual('infobox file format, infobox technology standard', names)

    @ignore_warnings
    def test_infobox2_xml(self):
        text = Path('XML').read_text(encoding='UTF-8')
        # print(text)
        names = myparser.extract_names(text)
        self.assertEqual('infobox file format, infobox technology standard', names)


if __name__ == '__main__':
    TestParsing.main()
