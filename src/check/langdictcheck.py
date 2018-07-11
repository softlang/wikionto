from data import DATAP
from json import load, dump


class LangdictCheck:

    def solo(self):
        with open(DATAP + '/olangdict.json', 'r', encoding="UTF8") as f:
            langdict = load(f)
            langdict = self.check(langdict)
            f.close()
        with open(DATAP + '/olangdict.json', 'w', encoding="UTF8") as f:
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
