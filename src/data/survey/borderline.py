from data import DATAP,load_articledict
from pandas import read_csv
from json import load

with open("D:/Programming/Repos/wikionto/data/datasets/articledict.json","r",encoding="utf-8") as f:
    ad = load(f)
with open("D:/Programming/Repos/wikionto/data/survey/questions/eval/qid_to_a.json", "r", encoding="utf-8") as f:
    qid_to_article = load(f)
with open("D:/Programming/Repos/wikionto/data/datasets/survey/data_wikitopicsurvey_2019-03-01_12-08.csv", "r", encoding="utf-8") as f:
    df = read_csv(f, sep="\t", quotechar='"', header=0, dtype=str)
df = df.drop(df.index[[0]])
df = df.fillna('0')

print("Fixing emailed issues")
print(df["AD72"])
df.loc[df["CASE"] == '19837', "AD72"] = '1'
print(df["AD72"])

print("-----")
print("Answer counts")
answercolumns = [c for c in df.columns.values if c.startswith('A')]
commentcolumns = [c for c in df.columns.values if c.startswith('ZZ')]

dfanswers = df.filter(items=answercolumns)
dfcomments = df.filter(items=commentcolumns)


print("-----")
print("Agreement Insights")
mixedset = []
agreedset_yes2 = []
agreedset_no2 = []
yesnodict2 = {"yes": 0, "no": 0, "mixed": 0}
agreedset_yes1 = []
agreedset_no1 = []
yesnodict1 = {"yes": 0, "no": 0, "mixed": 0}
for column in answercolumns:
    values = df[column]
    yesnr = len([v for v in values if v == '1' if not ad[qid_to_article[column]]["Seed"]])
    nonr = len([v for v in values if v == '2' if not ad[qid_to_article[column]]["Seed"]])
    if yesnr > 0 and nonr > 0:
        mixedset.append(column)

print("Mixed")
print(len(mixedset))
print(mixedset)

print("-----")
print("Commenting corelation with agreement")
mixcommentnr = 0
for mixcolumn in mixedset:
    text = ""
    text += qid_to_article[mixcolumn]
    mixdf = df[df[mixcolumn] != '0']
    commentcolumn = "ZZ" + mixcolumn[2:] + "_01"
    if commentcolumn in commentcolumns and [c for c in mixdf[commentcolumn].values if c != '0']:
        mixcommentnr += 1
        text += mixdf[commentcolumn].values
    print(text)
