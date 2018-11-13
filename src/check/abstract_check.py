from data import DATAP
from json import load, dump


class ArtdictCheck:

    def solo(self):
        with open(DATAP + '/langdict.json', 'r', encoding="UTF8") as f:
            langdict = load(f)
            langdict = self.check(langdict)
            f.close()
        with open(DATAP + '/langdict.json', 'w', encoding="UTF8") as f:
            dump(obj=langdict, fp=f, indent=2)
            f.flush()
            f.close()

    def dryrun(self):
        with open(DATAP + '/testdict.json', 'r', encoding="UTF8") as f:
            langdict = load(f)
            langdict = self.check(langdict)
            f.close()
        with open(DATAP + '/testdict.json', 'w', encoding="UTF8") as f:
            dump(obj=langdict, fp=f, indent=2)
            f.flush()
            f.close()


class CatdictCheck:
    def solo(self):
        with open(DATAP + '/langdict.json', 'r', encoding="UTF8") as f:
            langdict = load(f)
        with open(DATAP + '/catdict.json', 'r', encoding="UTF8") as f:
            cd = load(f)
            cd = self.check(cd, langdict)
            f.close()
        with open(DATAP + '/catdict.json', 'w', encoding="UTF8") as f:
            dump(obj=cd, fp=f, indent=2)
            f.flush()
            f.close()