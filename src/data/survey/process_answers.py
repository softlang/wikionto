from pandas import read_csv, value_counts
from data import DATAP, load_articledict, save_articledict
from json import dumps, load

ad = load_articledict()
with open(DATAP + "/survey/questions/eval/qid_to_a.json", "r", encoding="utf-8") as f:
    qid_to_article = load(f)
with open(DATAP + "/survey/data_wikitopicsurvey_2019-03-01_12-08.csv", "r", encoding="utf-8") as f:
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
# print(dfanswers)
# print(dfcomments)

qsets1 = []
qsets2 = []
answercountdict = dict()
for column in answercolumns:
    values = df[column]
    nr = len([v for v in values if v != '0'])
    if nr < 2:
        if column[:2] not in qsets1:
            qsets1.append(column[:2])
    if nr >= 2:
        if column[:2] not in qsets2:
            qsets2.append(column[:2])
    if nr not in answercountdict:
        answercountdict[nr] = 0
    answercountdict[nr] += 1
print(dumps(answercountdict, indent=2))
print(qsets1)
print(qsets2)

print("-----")
print("Answer frequencies")
dfanswers_f = dfanswers.apply(value_counts).T
print(dfanswers_f)

print("-----")
print("Seed article evaluation")
dfseed = dfanswers.filter(regex="0[1-5]")
dfseed = dfseed.apply(value_counts).T
print(dfseed[dfseed['2'] > 0])

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
        yesnodict2["mixed"] += 1
        mixedset.append(column)
    else:
        if yesnr >= 1:
            yesnodict1["yes"] += 1
            agreedset_yes1.append(column)
        elif nonr >= 1:
            yesnodict1["no"] += 1
            agreedset_no1.append(column)
        if yesnr >= 2:
            yesnodict2["yes"] += 1
            agreedset_yes2.append(column)
        elif nonr >= 2:
            yesnodict2["no"] += 1
            agreedset_no2.append(column)

print("-----")
# annotating the dictionary
for column in agreedset_yes2:
    a = qid_to_article[column]
    ad[a]["SL2"] = '1'
for column in agreedset_yes1:
    a = qid_to_article[column]
    ad[a]["SL1"] = '1'
for column in agreedset_no2:
    a = qid_to_article[column]
    ad[a]["SL2"] = '0'
for column in agreedset_no1:
    a = qid_to_article[column]
    ad[a]["SL1"] = '0'
save_articledict(ad)
print("At least two judges")
print(dumps(yesnodict2, indent=2))
print("-----")
print("One judge")
print(dumps(yesnodict1, indent=2))
print("-----")
print("Mixed")
print(mixedset)

print("-----")
print("Commenting corelation with agreement")
mixcommentnr = 0
for mixcolumn in mixedset:
    print(mixcolumn)
    mixdf = df[df[mixcolumn] != '0']
    commentcolumn = "ZZ" + mixcolumn[2:] + "_01"
    if commentcolumn in commentcolumns and [c for c in mixdf[commentcolumn].values if c != '0']:
        mixcommentnr += 1
        print(mixdf[commentcolumn].values)

agreedcommentnr_yes = 0
for acolumn in agreedset_yes2:
    agreedf = df[df[acolumn] != '0']
    commentcolumn = "ZZ" + acolumn[2:] + "_01"
    if commentcolumn in commentcolumns and [c for c in agreedf[commentcolumn].values if c != '0']:
        agreedcommentnr_yes += 1
agreedcommentnr_no = 0
for acolumn in agreedset_no2:
    agreedf = df[df[acolumn] != '0']
    commentcolumn = "ZZ" + acolumn[2:] + "_01"
    if commentcolumn in commentcolumns and [c for c in agreedf[commentcolumn].values if c != '0']:
        agreedcommentnr_no += 1
print("For Mixed: " + str(mixcommentnr))
print("For Agreed on Yes: " + str(agreedcommentnr_yes))
print("For Agreed on No: " + str(agreedcommentnr_no))

print("-----")
print("Seed article test")
CASE_to_seedtest = {}

for index, row in df.iterrows():
    # determine which questions were answered
    for answercolumn in answercolumns:
        if row[answercolumn] != '0':
            setname = answercolumn[:1]
            break
    # determine seed articles in answered questions
    assert len(setname) == 2
    seed_columns = []
    for qid, title in qid_to_article.items():
        if qid.startswith(setname) and ad[title]["Seed"]:
            seed_columns.append(qid)
    # determine whether seed articles were answered correctly
    count_wrong = 0
    for sc in seed_columns:
        if row[sc] != '1':
            count_wrong += 1
    CASE_to_seedtest[row["CASE"]] = count_wrong
print(dumps(CASE_to_seedtest, indent=2))
