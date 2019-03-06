from data import DATAP, load_articledict, save_articledict, backup_articledict
from json import load, dump
from data import start_time, stop_time


class ArtdictCheck:

    def solo(self, backup=True):
        articledict = load_articledict()
        if backup:
            backup_articledict(articledict)
        t = start_time()
        articledict = self.check(articledict)
        stop_time(t)
        save_articledict(articledict)

    def dryrun(self):
        with open(DATAP + '/testdict.json', 'r', encoding="UTF8") as f:
            testdict = load(f)
            testdict = self.check(testdict)
        with open(DATAP + '/testdict.json', 'w', encoding="UTF8") as f:
            dump(obj=testdict, fp=f, indent=2)
            f.flush()


class CatdictCheck:
    def solo(self):
        articledict = load_articledict()
        with open(DATAP + '/catdict.json', 'r', encoding="UTF8") as f:
            cd = load(f)
            cd = self.check(cd, articledict)
        with open(DATAP + '/catdict.json', 'w', encoding="UTF8") as f:
            dump(obj=cd, fp=f, indent=2)
            f.flush()
