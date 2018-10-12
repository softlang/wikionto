from lxml import etree
from json import load
import time
import os
from data import DATAP
from mine_dump import hms_string
import csv

DUMP_PATH = DATAP + '/dump/'
FILENAME_WIKI = 'enwiki-20180901-pages-articles-multistream.xml'
FILENAME_ARTICLES = 'articles.json'
ENCODING = "utf-8"
NS = "{http://www.mediawiki.org/xml/export-0.10/}"
PAGE = NS+"page"
TITLE = NS+"title"
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


def extract_with_xpath(elem, titlexp, textxp, csvwriter):
    r = titlexp(elem)
    if r:
        title = normalize(r[0].text)
        if title in adict:
            r = textxp(elem)
            if r:
                text = r[0].text.replace('\n', '\\n')
                csvwriter.writerow([title, text])
            #extract_seedrecognition()


def extract_features(csvwriter):
    start_time = time.time()
    titlexp = etree.ETXPath("child::"+TITLE)
    textxp = etree.ETXPath("child::"+REV+"/"+TEXT)
    context = etree.iterparse(pathWikiXML, events=('end',), tag=PAGE)
    fast_iter(context,lambda elem: extract_with_xpath(elem, titlexp, textxp, csvwriter))

    elapsed_time = time.time() - start_time
    print("Elapsed time: {}".format(hms_string(elapsed_time)))


if __name__ == "__main__":
    with open(DUMP_PATH+FILENAME_ARTICLES, 'r', encoding=ENCODING) as f:
        adict = load(f)
    with open(DATAP + '/dump/articles.csv', 'w', encoding="UTF8") as f:
        csvwriter = csv.writer(f, delimiter=',',  escapechar=' ',
                            quotechar='|', lineterminator='\n')
        extract_features(csvwriter)
