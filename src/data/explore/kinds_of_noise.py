from data import DATAP
from json import load

f = open(DATAP + "/catdict.json", "r")
cd = load(f)
noise = [(c, cd[c]["#NonSLs"]) for c in cd if cd[c]["#SLs"] == 0 and cd[c]["#NonSLs"] > 1000]

