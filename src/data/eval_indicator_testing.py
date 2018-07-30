from json import load
from data import DATAP
from pandas import read_csv
from io import StringIO

f = open(DATAP + '/olangdict.json', 'r', encoding="UTF8")
ld = load(f)

posseed = set(l for l in ld if ld[l]["ValidInfobox"] == 1)
negseed = set(l for l in ld if ld[l]["negativeSeed"] == 1)

inds = ["URLBracesPattern", "In_Wikipedia_List", "POS"]
csvtext = ""
for p in inds:
    tp = len(set(l for l in posseed if ld[l][p] == 1))
    fn = len(set(l for l in posseed if ld[l][p] == 0))
    tn = len(set(l for l in negseed if ld[l][p] == 0))
    fp = len(set(l for l in negseed if ld[l][p] == 1))

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)

    csvtext += p + "," + str(tp) + "," + str(fp) + "," + str(tn) + "," + str(fn) + "," + str(precision) + "," + str(
        recall) + "\n"
headers = ["TP", "FP", "TN", "FN", "Prec", "Rec"]
print(csvtext)
dtypes = dict()
for v in headers:
    dtypes[v] = int
dtypes["Name"] = str
dtypes["Prec"] = float
dtypes["Rec"] = float
df = read_csv(StringIO(csvtext), delimiter=',', names=headers)
print(df.to_latex(header=True))

print("Complementary")
tp = len(set(l for l in posseed if any(ld[l][p] == 1 for p in inds)))
fn = len(set(l for l in posseed if not any(ld[l][p] == 1 for p in inds)))
tn = len(set(l for l in negseed if not any(ld[l][p] == 1 for p in inds)))
fp = len(set(l for l in negseed if any(ld[l][p] == 1 for p in inds)))
prec = tp / (tp + fp)
rec = tp / (tp + fn)
print("Complementary & " + str(tp) + " & " + str(fp) + " & " + str(tn) + " & " + str(fn) + " & " + str(
    prec) + " & " + str(rec))

print(len(set(l for l in negseed)))
print(len(set(l for l in posseed)))
print(len(set(l for l in ld if ld[l]["negativeSeedCandidate"] == 1)))

print([l for l in ld if ld[l]["Seed"] == 1 and not "Summary" in ld[l]])

print({l: ld[l] for l in ld if l.startswith("Augmented_Backus")})
