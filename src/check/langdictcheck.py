from data import DATAP
from json import load, dump


class LangdictCheck:

    def solo(self):
        with open(DATAP + '/langdict.json', 'r', encoding="UTF8") as f:
            langdict = load(f)
            langdict = self.check(langdict)
            f.close()
        with open(DATAP + '/langdict.json', 'w', encoding="UTF8") as f:
            dump(obj=langdict, fp=f, indent=2)
            f.flush()
            f.close()
