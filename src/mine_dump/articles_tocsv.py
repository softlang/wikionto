from lxml import etree
from json import load
import time
import os
from data import DATAP
from mine_dump import start_time, stop_time
import csv

DUMP_PATH = DATAP + '/dump/'
FILENAME_WIKI = 'enwiki-20180901-pages-articles-multistream.xml'
FILENAME_ARTICLES = 'articles_inscope.json'
ENCODING = "utf-8"
NS = "{http://www.mediawiki.org/xml/export-0.10/}"
PAGE = NS+"page"
TITLE = NS+"title"
ID = NS+"id"
REV = NS+"revision"
TEXT = NS+"text"
pathWikiXML = os.path.abspath(DUMP_PATH+FILENAME_WIKI)


def strip_tag_name(tag):
    t = tag
    idx = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t


def normalize(title):
    return title.replace(" ", "_")


def fast_iter(context, func):
    for event, elem in context:
        func(elem)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context


def extract_with_xpath(elem, idexp, titlexp, textxp, csvwriter):
    title_elem = titlexp(elem)
    aid_elem = idexp(elem)
    if title_elem:
        aid = aid_elem[0].text
        if aid in adict:
            text_elem = textxp(elem)
            if text_elem:
                title = normalize(title_elem[0].text)
                text = text_elem[0].text.replace('\n', '\\n')
                csvwriter.writerow([aid, title, text])
            #extract_seedrecognition()


def extract_features(csvwriter):
    t = start_time()

    idexp = etree.ETXPath("child::"+ID)
    titlexp = etree.ETXPath("child::"+TITLE)
    textxp = etree.ETXPath("child::"+REV+"/"+TEXT)
    context = etree.iterparse(pathWikiXML, events=('end',), tag=PAGE)
    fast_iter(context,lambda elem: extract_with_xpath(elem, idexp, titlexp, textxp, csvwriter))

    stop_time(t)


if __name__ == "__main__":
    with open(DUMP_PATH+FILENAME_ARTICLES, 'r', encoding=ENCODING) as f:
        adict = load(f)
    with open(DATAP + '/dump/articles_inscope.csv', 'w', encoding="UTF8") as f:
        csvwriter = csv.writer(f, delimiter=',',  escapechar=' ',
                            quotechar='|', lineterminator='\n')
        extract_features(csvwriter)
