from check.abstract_check import CatdictCheck


class Cycle(CatdictCheck):

    def check(self, catdict, articledict):
        print("Checking for cycles")
        for cat in catdict:
            catdict[cat]["Cycle"] = cycle(cat, catdict)
        return catdict


def cycle(cat, catdict):
    if "subcats" not in catdict[cat]:
        return False
    catfront = catdict[cat]["subcats"]
    visited = set(catfront)
    while catfront:
        if cat in catfront:
            return True
        catfront = [subcat for c in catfront if "subcats" in catdict[c] for subcat in catdict[c]["subcats"] if
                    subcat not in visited]
        visited |= set(catfront)
    return False


if __name__ == "__main__":
    Cycle().solo()
