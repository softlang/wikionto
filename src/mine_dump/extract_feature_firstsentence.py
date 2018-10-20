from mine_dump.extractors.first_sentence import extract_first_sentence
from data import DATAP
import csv


def extract_first_sentence_only():
    f = open(DATAP + '/dump/articles.csv', "r", encoding="UTF8")
    fwrite = open(DATAP + '/dump/articles_firstsentence.csv', "w", encoding="UTF8")
    dialect = csv.Sniffer().sniff(f.read(1024))
    dialect.quoting = csv.QUOTE_MINIMAL
    f.seek(0)
    r = csv.reader(f, dialect, delimiter=',', quotechar='|')
    for row in r:
        try:
            title = row[0]
            text = row[1]
            first = extract_first_sentence(text)
            fwrite.write("|" + title + ",|" + first + "|\n")
        except IndexError:
            print(row)


if __name__ == "__main__":
    extract_first_sentence_only()
