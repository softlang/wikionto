from data import DATAP
from data import load_articledict
import csv
import json
from multiprocessing import Pool

DUMPP = "S:\Data\Wikipedia\dumps"


def getlists():
    ad = load_articledict()
    lists = [a for a in ad if "List_of" in a]

    ids = json.load(open(DUMPP + "/article_ids.json", "r"))

    linkdict = {}
    with open(DUMPP + "/pagelinks.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        x = 0
        for row in reader:
            x += 1
            if x % 100000 == 0:
                print(x)
            from_id = row[0]
            to_title = row[1]
            if from_id not in ids:
                continue
            from_title = ids[from_id]
            if from_title in lists:
                if from_title not in linkdict:
                    linkdict[from_title] = []
                if to_title in ad:
                    linkdict[from_title].append(to_title)
    with open(DATAP + "/listlinks.json", "w", encoding="utf-8") as f:
        json.dump(linkdict, f)


if __name__ == '__main__':
    getlists()
