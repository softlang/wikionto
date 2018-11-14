from data import DATAP
from json import load, dump


class ArtdictCheck:

    def solo(self):
        with open(DATAP + '/articledict.json', 'r', encoding="UTF8") as f:
            articledict = load(f)
            articledict = self.check(articledict)
            f.close()
        with open(DATAP + '/articledict.json', 'w', encoding="UTF8") as f:
            dump(obj=articledict, fp=f, indent=2)
            f.flush()
            f.close()

    def dryrun(self):
        with open(DATAP + '/testdict.json', 'r', encoding="UTF8") as f:
            testdict = load(f)
            testdict = self.check(testdict)
            f.close()
        with open(DATAP + '/testdict.json', 'w', encoding="UTF8") as f:
            dump(obj=testdict, fp=f, indent=2)
            f.flush()
            f.close()


class CatdictCheck:
    def solo(self):
        with open(DATAP + '/articledict.json', 'r', encoding="UTF8") as f:
            articledict = load(f)
        with open(DATAP + '/catdict.json', 'r', encoding="UTF8") as f:
            cd = load(f)
            cd = self.check(cd, articledict)
            f.close()
        with open(DATAP + '/catdict.json', 'w', encoding="UTF8") as f:
            dump(obj=cd, fp=f, indent=2)
            f.flush()
            f.close()