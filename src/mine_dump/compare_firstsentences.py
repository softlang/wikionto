from data import DATAP
import csv
import os

#fnew = open(DATAP + '/dump/articles_annotated.csv', 'w', encoding='UTF-8')
for filename in os.listdir(DATAP + '/dump/articles_annotated_pre'):
    if filename.endswith(".csv"):
        print("Reading " + filename)
        f = open(DATAP + '/dump/articles_annotated_pre/' + filename, 'r', encoding='UTF-8')
        dialect = csv.Sniffer().sniff(f.read())
        reader = csv.DictReader(f,
                                fieldnames=['title', 'first_sentence', 'first_sentence2', 'infoboxnames', 'urlwords'],
                                dialect=dialect)
        for row in reader:
            if 'None' in row:
                raise Exception('Not parsing correctly')
            if row['first_sentence'] != row['first_sentence2']:
                print("----")
                print(row['title'])
                print(row['first_sentence'])
                print(row['first_sentence2'])
                for r in row.items():
                    print(r)
