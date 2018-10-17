from data import DATAP
from json import load

def get_path_to_contents(pid):
    cats = set()
    with open(DATAP+'/dump/tocatlinks_article.json') as f:
        # collect cats at distance 1
        cat_to_a = set(cat_id for cat_id, a_id in load(f).items() if pid == a_id)
    with open(DATAP + '/dump/tocatlinks_category.json') as f:
        cat_to_cat = load(f)
    with open(DATAP + '/dump/article.json') as f:
        adict = load(f)

    contents_id = 3 #TODO

    # collect cats until list is empty
    for cat_id in cat_to_a:
        if cat_id not in cats:
            # get super cats:
            super_cats = set(super_cat for super_cat, cat_id2 in cat_to_cat.items() if cat_id2 == cat_id)

if __name__ == "__main__":
    with open(DATAP + '/dump/category_ids.json') as f:
        ciddict = load(f)
    for cid, name in ciddict:
        if name=="Contents":
            print(cid)