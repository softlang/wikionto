from data import DATAP
from json import load, dump
from mine_dump import start_time, stop_time
import sys


def get_path_to_contents_categories():
    with open(DATAP + '/dump/tocatlinks_category.json') as f:
        cat_to_cat = load(f)
        cat_to_cat = {int(key): [int(v) for v in values] for key, values in cat_to_cat.items()}
    pathdict = dict()
    CONTENTS_ID = 14105005
    pathdict[CONTENTS_ID] = []
    front = [[CONTENTS_ID]]
    while front:
        path0 = front[0]
        front = front[1:]
        head = path0[0]
        if head not in cat_to_cat:
            continue
        for nextcat in cat_to_cat[head]:
            if nextcat in path0:
                continue
            if nextcat in pathdict:
                pathdict[nextcat] = list(set(pathdict[nextcat] + path0))
            else:
                pathdict[nextcat] = path0
            front = [([nextcat] + path0)] + front

    with open(DATAP + '/dump/tocatlinks_category_allpaths.json', "w", encoding="UTF8") as f:
        dump(pathdict, f)


def get_path_to_contents_article(spid, cat_to_cat_reverse, cat_front):
    pid = int(spid)
    cat_results = set()
    cat_front = set(cat_id for cat_id, a_ids in cat_front.items() if pid in a_ids)
    CONTENTS_ID = 14105005

    cat_results |= cat_front
    while True:
        new_cat_front = set()
        # collect cats until list is empty
        for cat_id in cat_front:
            temp = set(super_cat for super_cat in cat_to_cat_reverse[cat_id] if super_cat not in cat_results
                       and super_cat != CONTENTS_ID)
            new_cat_front |= temp
        if not new_cat_front:
            break
        cat_results |= new_cat_front
        cat_front = new_cat_front
        # print(len(cat_results))
    return cat_results


if __name__ == "__main__":
    t = start_time()
    get_path_to_contents_categories()
    stop_time(t)
