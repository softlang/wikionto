from data import DATAP
import csv
import os
import time
from multiprocessing import Pool
from mine_dump import hms_string
from mine_dump.extractors.first_sentence import extract_first_sentence
from mine_dump.extractors.infobox_names import extract_names
from mine_dump.extractors.url_words import extract_urlpattern
import sys


def extract_pre():
    maxInt = sys.maxsize
    decrement = True
    while decrement:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.
        decrement = False
        try:
            csv.field_size_limit(maxInt)
        except OverflowError:
            maxInt = int(maxInt / 10)
            decrement = True
    f = open(DATAP + '/dump/articles.csv', 'r', encoding='UTF-8')
    fnew = open(DATAP + '/dump/articles_annotated_pre.csv', 'w', encoding='UTF-8')
    csvwriter = csv.writer(fnew, delimiter=',', quotechar='|', lineterminator='\n')
    reader = csv.reader(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    newrows = [extract_row(row) for row in reader]
    for row in newrows:
        csvwriter.writerow(row)
    f.close()
    fnew.close()


def extract_row(row):
    title = row[0]
    text = row[1]
    first = extract_first_sentence(text)
    names = extract_names(text)
    urlwords = extract_urlpattern(title)
    return [title, first, names, urlwords]


def extract_nlp2():
    fnew = open(DATAP + '/dump/articles_annotated.csv', 'w', encoding='UTF-8')
    csvwriter = csv.writer(fnew, delimiter=',', quotechar='|', lineterminator='\n')
    for filename in os.listdir(DATAP + '/dump/articles_annotated_pre'):
        if filename.endswith(".csv"):
            print("Reading " + filename)
            f = open(DATAP + '/dump/articles_annotated_pre/' + filename, 'r', encoding='UTF-8')
            reader = csv.reader(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            print("Processing " + filename)
            pool = Pool(processes=4)
            newrows = pool.map(id, [row for row in reader])
            for row in newrows:
                csvwriter.writerow(row)


if __name__ == "__main__":
    # merge_csvs("C:/Programmierung/Repos/WikiOnto/data/dump/articles_annotated_pre",
    #           "C:/Programmierung/Repos/WikiOnto/data/dump/articles_annotated_pre.csv")
    start_time = time.time()
    extract_pre()
    elapsed_time = time.time() - start_time
    print("Elapsed time: {}".format(hms_string(elapsed_time)))
