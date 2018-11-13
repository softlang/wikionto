from check.abstract_check import CatdictCheck


class CategoryURLPattern(CatdictCheck):

    def check(self, catdict, articledict):
        print("Checking category names")
        ex_pattern = ["Data_types", "lists_of", "comparison", "companies"]
        for c in catdict:
            if any(w in c for w in ex_pattern):
                catdict[c]["ExCatNamePattern"] = 0
            else:
                catdict[c]["IncludedNamePattern"] = 1
        return catdict


if __name__ == "__main__":
    CategoryURLPattern().solo()
