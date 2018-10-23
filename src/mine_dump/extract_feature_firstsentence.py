from mine_dump.extractors.first_sentence import extract_first_sentence
from data import DATAP
import csv
from json import load

def extract_first_sentence_only():
    with open(DATAP + '/dump/articles.csv', "r", encoding="UTF8") as f:
        scope = load(f)
    f = open(DATAP + '/dump/articles.csv', "r", encoding="UTF8")
    fwrite = open(DATAP + '/dump/articles_firstsentence.csv', "w", encoding="UTF8")
    # dialect = csv.Sniffer().sniff(f.read(1024))
    # dialect.quoting = csv.QUOTE_MINIMAL
    f.seek(0)
    r = csv.reader(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in r:
        try:
            if len(row) != 2:
                print(str(len(row)) + ": " + row[0])
                continue
            title = row[0]
            text = row[1]
            first = extract_first_sentence(text)
            fwrite.write("|" + title + ",|" + first + "|\n")
        except IndexError:
            print(row)


if __name__ == "__main__":
    import sys

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
    extract_first_sentence_only()
