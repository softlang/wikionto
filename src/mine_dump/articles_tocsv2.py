from data import DATAP
from json import load, dump
import csv


def mine_multistream(adict, csvwriter):
    print()


def annotate_index(adict):
    f = open(DATAP + "/dump/enwiki-20180901-pages-articles-multistream-index.txt", 'r', encoding="UTF8")
    for line in f:
        splits = line.split(":")
        bytestart = splits[0]
        aid = splits[1]
        if aid in adict:
            adict[aid]["byte-index"] = bytestart
    f = open(DATAP + "/dump/articles_inscope", 'w', encoding="UTF8")
    dump(adict, f)


if __name__ == "__main__":
    with open(DATAP + "/dump/articles_inscope", 'r', encoding="UTF8") as f:
        adict = load(f)
    testid = "27701"
    with open(DATAP + "/dump/enwiki-20180901-pages-articles-multistream.xml", 'r', encoding="UTF8") as f:
        f.seek(int(adict[testid]["byte-index"]))
        text = ""
        for c in f.read(100):
            text += c
        print(text)

    # with open(DATAP+"/dump/articles_inscope.json", 'r', encoding="UTF8") as f:
    #    adict = load(f)
    # with open(DATAP + '/dump/articles_inscope.csv', 'w', encoding="UTF8") as f:
    #    csvwriter = csv.writer(f, delimiter=',',  escapechar=' ',
    #                        quotechar='|', lineterminator='\n')
    #    extract_features(csvwriter)
