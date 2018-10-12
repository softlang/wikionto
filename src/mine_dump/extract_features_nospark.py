from data import DATAP
import csv
import os
import time
from multiprocessing import Pool


def extract_nlp2():
    fnew = open(DATAP + '/dump/articles_annotated.csv', 'w', encoding='UTF-8')
    csvwriter = csv.writer(fnew, delimiter=',', quotechar='"', lineterminator='\n')
    for filename in os.listdir(DATAP + '/dump/articles_annotated_pre'):
        if filename.endswith(".csv"):
            print("Reading " + filename)
            f = open(DATAP + '/dump/articles_annotated_pre/' + filename, 'r', encoding='UTF-8')
            reader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            print("Processing " + filename)
            pool = Pool(processes=4)
            newrows = pool.map(modify_row_nouns, [row for row in reader])
            for row in newrows:
                csvwriter.writerow(row)

if __name__ == "__main__":
    # merge_csvs("C:/Programmierung/Repos/WikiOnto/data/dump/articles_annotated_pre",
    #           "C:/Programmierung/Repos/WikiOnto/data/dump/articles_annotated_pre.csv")
    start_time = time.time()

    elapsed_time = time.time() - start_time
    print("Elapsed time: {}".format(hms_string(elapsed_time)))